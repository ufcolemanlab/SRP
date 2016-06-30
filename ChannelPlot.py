# -*- coding: utf-8 -*-
"""
Script for opening binary data files (viewing little endian doubles) from neuroGUI using numpy

Created on Mon May 11 13:04:54 2015

@author: Jesse Trinity (Coleman Lab)
"""


import numpy as np
import matplotlib.pyplot as plt

class ChannelPlot:
    def __init__(self):
        self.totalChannels = 8
        self.filename = ''
        self.dataType = '<d'
        self.data = [0]
        
        #filename = '4031B_45deg_Day1_data.bin'
        #totalChannels = 8

    def setTotalChannels(self, n):
        self.totalChannels = n

    def setFilename(self, name):
        self.filename = name

    def setDataType(self, dt):
        self.dataType = dt

    def openDataFile(self):
        
        self.data = np.fromfile(str(self.filename), dtype = np.dtype(self.dataType))
        #truncate the data file to handle bad input
        while(len(self.data) % self.totalChannels != 0):
            self.data = self.data[0:len(self.data)-1]
        self.data = self.data.reshape(len(self.data)/self.totalChannels, self.totalChannels)
        self.data = np.transpose(self.data)

    def plotData(self):
        plt.figure(1)
        for i in range(0, self.totalChannels):
            plt.subplot(self.totalChannels, 1, i + 1)
            plt.plot(self.data[i])
    
        plt.show()

    def saveToCSV(self, name):
        np.savetxt(name, self.data, delimiter = ',')

    def openAndPlot(self):
        self.openDataFile()
        self.plotData()

if __name__ == "__main__":
    dataImport = ChannelPlot()
    dataImport.setFilename('C:/Users/Jesse/Documents/Python Scripts/test/M_SRP11_45d_135d_d6_awake_132_data.bin')
    dataImport.setDataType('<d')
    dataImport.openAndPlot()


