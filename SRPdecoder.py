# -*- coding: utf-8 -*-
"""

--encoding--
    flips: 2
    flops: 1

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
    def GetStimLists(self, signalChannel, numStims, avgLength, flipTimeStamps, flopTimeStamps):
        flips = []
        flops = []
        for i in range(len(flopTimeStamps)):
            if self.StimLength(flopTimeStamps[i]) < 0.5*avgLength:
                for j in range(numStims):
                    flips.append(signalChannel[flipTimeStamps[i+j][0]:flipTimeStamps[i+j][0]+self.stimLength])
                for j in range(numStims - 1):
                    flops.append(signalChannel[flopTimeStamps[1+i+j][0]:flopTimeStamps[1+i+j][0] + self.stimLength])
                flops.append(signalChannel[flipTimeStamps[i + numStims - 1][0] + self.stimLength:flipTimeStamps[i + numStims-1][0]+2* self.stimLength])
                
        return flips, flops
    
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
    def StimsPerSession(self, flipLengths, flopLengths, avgLength):
        start = 0
        end = 0
        while(flopLengths[start] > avgLength*0.5):
            start += 1
        while(flipLengths[end] < avgLength*1.5):
            end += 1
        return end - start + 1
        
    #Make this take and return list of lists for using more than 2 channels (maybe a dictionary)
    def GetStimLengths(self, flipTimeStamps, flopTimeStamps):
        flipLengths = [self.StimLength(flip) for flip in flipTimeStamps]
        flopLengths = [self.StimLength(flop) for flop in flopTimeStamps]
        return flipLengths, flopLengths
        
    #takes a list of encoding channels and gives the code at sample point i
    def Decode(self, i, channels):
        return sum(2**a for (a,j) in enumerate([channel[i] for channel in channels]) if j > self.voltageThreshold)
    
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
        return zip(rise, fall)
        
    #gives average stim length. input must be in a list, i.e. f([flipTimeStamps]) or f([flipTimes, flopTimes]) but not f(flipTimeStamps)
    def AvgStimLength(self, timeStampsLists):
        return sum(sum(y-x for (x,y) in stampsList)/len(stampsList) for stampsList in timeStampsLists)/len(timeStampsLists)
        
    def StimLength(self, stim):
        return stim[1]- stim[0]
        

if __name__ == "__main__":
    f = ChannelPlot.ChannelPlot()
    f.setFilename('C:/Users/Jesse/Documents/New folder (2)/Flip Flop Dilution test/M_t21_90d_500ms_5ff_30block_data.bin')
    f.setDataType('<d')
    f.openDataFile()

    signalChannel = f.data[0]
    timingChannel = f.data[3]
    codeChannels = [f.data[4], f.data[5]]

    SRP = SRPdecoder()
    timeCodes = SRP.GetCodeList(signalChannel, codeChannels)
    flopTimeStamps = SRP.GetTimeStamps(1, timeCodes)
    flipTimeStamps = SRP.GetTimeStamps(2, timeCodes)
    flipLengths, flopLengths = SRP.GetStimLengths(flipTimeStamps, flopTimeStamps)
    avgLength = SRP.AvgStimLength([flipTimeStamps, flopTimeStamps])
    stimsPerSession = SRP.StimsPerSession(flipLengths, flopLengths, avgLength)
    flips, flops = SRP.GetStimLists(signalChannel, stimsPerSession, avgLength, flipTimeStamps, flopTimeStamps)
    print flips
    flipavgs = SRP.GetAverages(flips, stimsPerSession)
    flopavgs = SRP.GetAverages(flops, stimsPerSession)
    
    plt.figure(2)
#    for i in range(len(flipavgs)):
#        plt.plot(flipavgs[i])
    plt.plot(flopavgs[0])
    
    plt.figure(3)
    
    plt.plot(flipavgs[0])
        
    plt.figure(3)
#    for i in range(len(flipavgs)):
#        plt.plot(flopavgs[i])