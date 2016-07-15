
# -*- coding: utf-8 -*-
"""

--encoding--
    single orientation:
    flips: 2
    flops: 1
    
    n orientations:
    flips = 2*n for each n
    flops = flip - 1 for corresponding flop

flip flop pair begins directly after strobe drops to 0

Created on Fri May 20 14:49:17 2016

@author: Jesse
"""

import ChannelPlot
import numpy as np
import matplotlib.pyplot as plt

class SRPdecoder:
    def __init__(self, *args, **kwargs):

        self.voltageThreshold = 2.5
        self.stimLength = 500
        self.baseline = 25

    #Gives back chunks of the input signalChannel corresponding to flip and flop stim lists
    def GetStimLists(self, signalChannel, numStims, avgLength, stimTimeStamps):
        stims = {code:[] for code in stimTimeStamps}
        for i in range(len(stimTimeStamps[1])):
            if self.StimLength(stimTimeStamps[1][i]) < 0.5*avgLength:
                for k in range(2, len(stims)+1):
                    for j in range(numStims):
                        stims[k].append(signalChannel[stimTimeStamps[k][i+j][0]:stimTimeStamps[k][i+j][0]+self.stimLength])
                for j in range(numStims - 1):
                    stims[1].append(signalChannel[stimTimeStamps[1][1+i+j][0]:stimTimeStamps[1][1+i+j][0] + self.stimLength])
                stims[1].append(signalChannel[stimTimeStamps[2][i + numStims - 1][0] + self.stimLength:stimTimeStamps[2][i + numStims-1][0]+2* self.stimLength])
                
        return stims
    
    #Averages flips/flops in sequential groups of numStims
    def GetAverages(self, flips, numStims):
        avgs = []
        for i in range(0, len(flips), numStims):
            avg = np.zeros(len(flips[0]))
            for j in range(numStims):
                avg += np.array(flips[i+j]-np.average(flips[i+j][:self.baseline]))
            avg /= numStims
            #avg += i*np.ones(len(flips[0]))
            avgs.append(avg)
            
        return avgs
                         
    #Detects the number of stims in a session
    def StimsPerSession(self, stimLengths, avgLength):
    
        total = len(stimLengths[1])
        starts = filter(lambda x: x < 0.5*avgLength, stimLengths[1])
        #print "stims per session: " + str(total / len(starts))
        return total / len(starts)
        
    #Make this take and return list of lists for using more than 2 channels (maybe a dictionary)
    def GetStimLengths(self, flipTimeStamps):
        flipLengths = [self.StimLength(flip) for flip in flipTimeStamps]
        return flipLengths
        
    #takes a list of encoding channels and gives the code at sample point i
    def Decode(self, i, channels):
        return sum(2**a for (a,j) in enumerate([channels[key][i] for key in channels]) if j > self.voltageThreshold)
    
    #Returns a code list corresponding to the sample in the signal
    def GetCodeList(self, signal, channels):
        return[self.Decode(i, channels) for i in range(len(signal))]
            
    #Gives total number of sessions
    def GetTotalSessions(self, flopTimeStamps):
        return sum(self.StimLength(i) < 0.5*self.AvgStimLength([flopTimeStamps]) for i in flopTimeStamps)
    
    #Gives (rise, fall) timestamps corresponding to given code (1 for flop, 2 for flip)
    def GetTimeStamps(self, code, timeCodes):    
        rise = [i for i in range (1, len(timeCodes)) if timeCodes[i] == code and timeCodes[i-1] != code]
        fall = [i for i in range (1, len(timeCodes)) if timeCodes[i] != code and timeCodes[i-1] == code]
        stamps = zip(rise, fall)
        stamps[:] = [x for x in stamps if self.StimLength(x) > 4]
        return stamps
        
    #gives average stim length. input must be in a list, i.e. f([flipTimeStamps]) or f([flipTimes, flopTimes]) but not f(flipTimeStamps)
    def AvgStimLength(self, timeStampsLists):
        return sum(sum(y-x for (x,y) in stampsList)/len(stampsList) for stampsList in timeStampsLists.values())/len(timeStampsLists)
        
    def StimLength(self, stim):
        return stim[1] - stim[0]
    
    def CombineAvgs(self, avgs, code1, code2):
        combined = []
        for i in range(len(avgs[code1])):
            avg = np.mean(np.array([avgs[code1][i], avgs[code2][i]]), axis = 0)
            combined.append(avg)
        return combined
    

if __name__ == "__main__":
    f = ChannelPlot.ChannelPlot()
    f.setFilename('C:/Users/Jesse/Documents/Python Scripts/test/M_SRP11_45d_135d_d6_awake_132_data.bin')
    f.setDataType('<d')
    f.openDataFile()
    f.plotData()
    
    num_channels = 4
    stimCodes = [1,2,3,4]

    signalChannel = f.data[0]
    timingChannel = f.data[3]
    codeChannels = {4 + i:f.data[4 + i] for i in range(num_channels)}

    SRP = SRPdecoder()
    timeCodes = SRP.GetCodeList(signalChannel, codeChannels)
    stimTimeStamps = {code:SRP.GetTimeStamps(code, timeCodes) for code in stimCodes}
    stimLengths = {code:SRP.GetStimLengths(stimTimeStamps[code]) for code in stimTimeStamps}
    
    avgLength = SRP.AvgStimLength(stimTimeStamps)
    stimsPerSession = SRP.StimsPerSession(stimLengths, avgLength)
    
    stims = SRP.GetStimLists(signalChannel, stimsPerSession, avgLength, stimTimeStamps)
    avgs = [SRP.GetAverages(stims[code], stimsPerSession) for code in stims]
    
    plt.figure(4)
    plt.plot(avgs[0][0])
    plt.figure(5)
    plt.plot(avgs[1][0])
    
        
