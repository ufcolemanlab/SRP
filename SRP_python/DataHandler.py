# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:19:44 2016

@author: Jesse
"""
import ChannelPlot as cp
import SRPdecoder2 as SRP
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle

class DataHandler:
    def __init__(self):
        
        self.fileData = dict()
        
        self.filenames = dict()
        
        self.fileVars = dict()
        #data channels
        
        #default values
        self.stimLength = 500
        self.baseline = 25
        self.num_channels = 4
        
        #data of interest
        self.timeCodes = dict()

        self.avgAmplitudes = dict()
        self.stimTimeStamps = dict()
        self.stimLengths = dict()
        self.stim_avgs = dict()
        self.amplitudes = dict()
        self.orient_avgs = dict()
        self.orient_amplitudes = dict()
        self.total_avgs = dict()
        self.total_amplitudes = dict()
        self.grand_avgs = dict()
        self.grand_amps = dict()
    
    # (full path, number of encoding channels, length of stimulus window in ms, length of window to calculate stim baseline)
    def add_file(self, filename):
        
        #get all encoding channels by default and allow user to display relevant data?
        fn = os.path.basename(filename)
        
        self.filenames[fn] = filename
        
        stimCodes = [i + 1 for i in range(self.num_channels)]
        self.fileVars[fn] = {"num_channels":self.num_channels, "stimCodes":stimCodes, "stimLength":self.stimLength, "baseline":self.baseline}        
        
        f = cp.ChannelPlot()
        f.setFilename(filename)
        f.setDataType('<d')
        f.openDataFile()
        
        self.fileData[fn] = f.data
    
    def process_file(self, filename, num_channels, stimLength, baseline):
        
        stimCodes = [i + 1 for i in range(num_channels)]
        
        signalChannel = self.fileData[filename][0]
#        timingChannel = f.data[3]
        codeChannels = {4 + i:self.fileData[filename][4 + i] for i in range(num_channels)}
    
        d = SRP.SRPdecoder()
        d.baseline = baseline
        d.stimLength = stimLength
        
        timeCodes = d.GetCodeList(signalChannel, codeChannels)
        stimTimeStamps = {code:d.GetTimeStamps(code, timeCodes) for code in stimCodes}

        stimLengths = {code:d.GetStimLengths(stimTimeStamps[code]) for code in stimTimeStamps}
        
        avgLength = d.AvgStimLength(stimTimeStamps)
        stimsPerSession = d.StimsPerSession(stimLengths, avgLength)
        
        stims = d.GetStimLists(signalChannel, stimsPerSession, avgLength, stimTimeStamps)
        stim_avgs = {code:d.GetAverages(stims[code], stimsPerSession) for code in stims}
        
        orient_avgs = dict()
        for key in stim_avgs:
            if int(key) % 2 != 0:
                orient_avgs[key] = d.CombineAvgs(stim_avgs, key, key + 1)
        
        self.stimTimeStamps[filename] = stimTimeStamps
        self.timeCodes[filename] = timeCodes
        self.stimLengths[filename] = stimLengths
        self.stim_avgs[filename] = stim_avgs
        self.orient_avgs[filename] = orient_avgs
        self.total_avgs[filename] = self.get_grand_avgs(stim_avgs)
        self.grand_avgs[filename] = self.get_grand_avgs(orient_avgs)
        
    def get_grand_avgs(self, avg_list):
        total_avg = dict()
        for key in avg_list:
            avgs = np.zeros(len(avg_list[key][0]))
            for i in range(len(avg_list[key])):
                avgs += avg_list[key][i]
            avgs /= len(avg_list[key])
            total_avg[key] = [avgs]
        return total_avg
        
    def clear_all(self):
        self.fileData.clear()        
        self.filenames.clear()        
        self.fileVars.clear()
        self.timeCodes.clear()
        self.avgAmplitudes.clear()
        self.stimTimeStamps.clear()
        self.stimLengths.clear()
        self.stim_avgs.clear()
        self.amplitudes.clear()
        self.orient_avgs.clear()
        self.orient_amplitudes.clear()
        self.total_avgs.clear()
        self.total_amplitudes.clear()
        self.grand_avgs.clear()
        self.grand_amps.clear()
    
    #len(dh.stim_avgs['M_SRP11_45d_135d_d6_awake_132_data.bin'][1][0]) = 500
    #dict(filenames) dict(keycodes) list(stim averages)
    # 1 file, 4 keycodes, 5 stim blocks, 500 ms each
    def get_amplitudes(self, source, dest, lower, upper):
        dest.clear()
        for filename in source:
            dest[filename] = dict()
            for stim in source[filename]:
                
                #change list to dict with timestamp key
                dest[filename][stim] = dict()
                for i in range(len(source[filename][stim])):
                    array = source[filename][stim][i]

                    min_x = array[lower:upper].argmin()
                    min_y = array[lower:upper][min_x]
                    max_x = array[min_x + lower:upper].argmax()
                    max_y = array[min_x + lower:upper][max_x]
                    dest[filename][stim][i] = {"units":["mV","ms"],
                        "amplitude":max_y-min_y,"min_x":min_x + lower, "min_y":min_y,
                        "max_x":max_x + min_x + lower, "max_y":max_y, "lower":lower, "upper":upper, "waveform":array}
    
    def set_amplitude(self, source, dest, lower, upper, key, stim_type, block):
        array = source[key][stim_type][block]
        min_x = array[lower:upper].argmin()
        min_y = array[lower:upper][min_x]
        max_x = array[min_x + lower:upper].argmax()
        max_y = array[min_x + lower:upper][max_x]
        dest[key][stim_type][block] = {"units":["V","ms"],
            "amplitude":max_y-min_y,"min_x":min_x + lower, "min_y":min_y,
            "max_x":max_x + min_x + lower, "max_y":max_y, "lower":lower, "upper":upper, "waveform":array}
    
    def set_grand_amp(self, source, dest, lower, upper, filename):
        dest[filename] = dict()
        for stim in source[filename]:
            
            #change list to dict with timestamp key
            dest[filename][stim] = dict()
            for i in range(len(source[filename][stim])):
                array = source[filename][stim][i]

                min_x = array[lower:upper].argmin()
                min_y = array[lower:upper][min_x]
                max_x = array[min_x + lower:upper].argmax()
                max_y = array[min_x + lower:upper][max_x]
                dest[filename][stim][i] = {"units":["V","ms"],
                    "amplitude":max_y-min_y,"min_x":min_x + lower, "min_y":min_y,
                    "max_x":max_x + min_x + lower, "max_y":max_y, "lower":lower, "upper":upper, "waveform":array}
    
                       
    #graphs all channels in binary data file
    def graph_raw(self, filename):
        f = cp.ChannelPlot()
        f.data = self.fileData[filename]
        f.plotData()
    
    def graph_all(self):
        for fn in self.stim_avgs:
            for i in range(len(self.stim_avgs[fn])):
                plt.figure(i+1)
                for j in range(len(self.stim_avgs[fn][i+1])):
                    plt.plot(self.stim_avgs[fn][i+1][j])
                    plt.plot(self.amplitudes[fn][i+1][j]["min_x"],self.amplitudes[fn][i+1][j]["min_y"], 
                             marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                    plt.plot(self.amplitudes[fn][i+1][j]["max_x"],self.amplitudes[fn][i+1][j]["max_y"], 
                             marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)
    
    def detect_channels(self, filename):
        num_channels = 0
        d = SRP.SRPdecoder()
        detected = d.GetCodeList(self.fileData[filename][0],{4 + i:self.fileData[filename][4 + i] for i in range(4)})
        for i in range(8):
            if detected.count(i + 1) > 150:
                num_channels += 1
        return num_channels
            

       
if __name__ == "__main__":
    
    filename= 'C:/Users/Jesse/Documents/Python Scripts/test/M_SRP11_45d_135d_d6_awake_132_data.bin'
    fn = os.path.basename(filename)
    dh = DataHandler()
    dh.add_file(filename)
    dh.process_file(fn, 4, dh.stimLength, dh.baseline)
    dh.get_amplitudes(dh.stim_avgs, dh.amplitudes, 25, 250)
    dh.graph_raw(fn)
    
    print dh.detect_channels(fn)
    
    dh.graph_all()
    
        


