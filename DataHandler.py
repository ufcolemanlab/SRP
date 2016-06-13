# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:19:44 2016

@author: Jesse
"""
import ChannelPlot as cp
import SRPdecoder

class DataHandler:
    def __init__(self):
        
        self.fileData = dict()
        #data channels
        self.numCodeChannels = 2
        
        #user variables
        self.stimLength = 500
        self.baseline = 25
        
        #data of interest
        self.flips = dict()
        self.flops = dict()
        self.flipAverages = dict()
        self.flipAverages = dict()
        self.flipAmplitudes = dict()
        self.flopAmplitudes = dict()
        self.avgAmplitudes = dict()
        self.flipTimeStamps = dict()
        self.flopTimeStamps = dict()
    
    def add_file(self, filename):
        f = cp.ChannelPlot()
        f.setFilename(filename)
        f.setDataType('<d')
        f.openDataFile()
        
        self.fileData[filename] = f.data
    
        signalChannel = f.data[0]
        timingChannel = f.data[3]
        codeChannels = [f.data[i] for i in range(4, 4 + self.numCodeChannels)]
    
        SRP = SRPdecoder()
        
        timeCodes = SRP.GetCodeList(signalChannel, codeChannels)
        self.flopTimeStamps[filename] = SRP.GetTimeStamps(1, timeCodes)
        self.flipTimeStamps[filename] = SRP.GetTimeStamps(2, timeCodes)
        
        flipLengths, flopLengths = SRP.GetStimLengths(self.flipTimeStamps[filename], self.flopTimeStamps[filename])
        avgLength = SRP.AvgStimLength([self.flipTimeStamps[filename], self.flopTimeStamps[filename]])
        
        stimsPerSession = SRP.StimsPerSession(flipLengths, flopLengths, avgLength)
        
        flips, flops = SRP.GetStimLists(signalChannel, stimsPerSession, avgLength, self.flipTimeStamps[filename], self.flopTimeStamps[filename])
        self.flipAverages[filename] = SRP.GetAverages(flips, stimsPerSession)
        self.flopAverages[filename] = SRP.GetAverages(flops, stimsPerSession)
        
        
    def load(self, dat):
       


