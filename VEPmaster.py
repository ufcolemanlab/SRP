# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:45:55 2016

@author: Jesse
"""

#This is a git test
#testing
import Tkinter as tk
import ttk
import tkFileDialog
import ChannelPlot as cp
import SRPdecoder as SRP
import numpy as np
import os

import DictionarySaver as ds

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
from scipy.io import matlab


#global figures
LARGE_FONT = ("Verdana", 12)
style.use("bmh")

datafile = cp.ChannelPlot()
datafile.setDataType('<d')
        
data = {}
flipAverages = {}
flopAverages = {}
amplitudes = {}

f = Figure(figsize = (6,3), dpi = 100)
a = f.add_subplot(111)
a.plot([0 for i in range(500)])


#global animation
def animate(i):
    pass

#main application
class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
#        decoder = SRP.SRPdecoder()
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, default = "mouse.ico")
        tk.Tk.wm_title(self, "SRP Analysis")
        
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        #self.data = {}
        
        for F in (StartPage, PageOne, GraphPage):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    #loads file into data using channelImport
    def load_files(self):
        datafile = cp.ChannelPlot()
        
        datafile.setDataType('<d')
             
        
        files = tkFileDialog.askopenfilenames(title='Choose files')
        filelist = list(files) 
        for filename in filelist:
                datafile.setFilename(filename)
                datafile.openDataFile()
                #self.data[filename] = datafile.data
                fn = os.path.basename(filename)
                print fn
                data[filename] = datafile.data
                
    
    #plots averages
    
    
#First page when you open the app
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f = tk.Frame(self)
        f.pack(anchor = 'center')
        label = tk.Label(f, text="Start", font = LARGE_FONT)
        label.grid(row = 0, pady= 10, padx = 10, columnspan = 3)
        
        self.loadbox = tk.Listbox(f,selectmode='multiple',exportselection=0, width = 50, height = 10)
        self.loadbox.grid(row = 2, columnspan = 3)
        
        button1 = ttk.Button(f, text="Load",
                           command = lambda: self.load())
        button1.grid(row = 1, column = 0)
        
        button2 = ttk.Button(f, text="SRP Analysis",
                             command = lambda: controller.show_frame(GraphPage))
        button2.grid(row = 1, column = 1)
        
        button3 = ttk.Button(f, text = "Clear All",
                             command = lambda:  self.clear())
        button3.grid(row = 1, column = 2, padx = 10, pady = 10)
        
        
    #loads data into controller and poplates listbox with filenames
    def load(self):
        
        files = tkFileDialog.askopenfilenames(title='Choose files')
        filelist = list(files) 
        for filename in filelist:
                datafile.setFilename(filename)
                datafile.openDataFile()
                data[os.path.basename(filename)] = datafile.data
                
        self.loadbox.delete(0, tk.END)
        for a, b in enumerate(data):
            self.loadbox.insert(a, b)
        
    def clear(self):
        data.clear()
        flipAverages.clear()
        flopAverages.clear()
        self.loadbox.delete(0, tk.END)

#generic page template
class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        
        button1 = ttk.Button(self, text = "Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.pack()
        
#Page for displaying graphs
class GraphPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f1 = tk.Frame(self)
        f1.pack(side = tk.TOP)
        
        f2 = tk.Frame(self)
        f2.pack(anchor = 'ne')
        
        f3 = tk.Frame(self)
        f3.pack(side = tk.RIGHT)
        
        f4 = tk.Frame(self)
        f4.pack(side = tk.BOTTOM)
        
        
        label = tk.Label(f1, text="Graph Page", font = LARGE_FONT)
        label.grid(row = 0, column = 0, columnspan = 5)
        
        #buttons
        button1 = ttk.Button(f1, text = "Back to Home",
                            command = lambda: controller.show_frame(StartPage))
        button1.grid(row = 1, column = 0)
        
        button4 = ttk.Button(f1, text = "Process Loaded Data",
                             command = lambda: self.process())
                             
        button4.grid(row = 1, column = 1)
        
        button2 = ttk.Button(f1, text = "Graph All",
                             command = lambda: self.graph_all())
        button2.grid(row = 1, column = 2)
        
        button3 = ttk.Button(f1, text = "Graph Selected",
                             command = lambda: self.graph_selected())
        button3.grid(row = 1, column = 3)
        
        button5 = ttk.Button(f1, text = "View Raws",
                            command = lambda: self.view_raws())
                            
        button5.grid(row = 1, column = 4)
        
        button6 = ttk.Button(f1, text = "Grand Average",
                             command = lambda: self.graph_total())
                             
        button6.grid(row = 1, column = 5)
        
        button7 = ttk.Button(f1, text = "Save",
                     command = lambda: self.save())
                             
        button7.grid(row = 1, column = 6)
        
        stimlabel = tk.Label(f1, text="Stim Length")
        stimlabel.grid(row = 2, column = 0)
        
        self.stimLengthEntry = ttk.Entry(f1, text = "Stim Length")
        self.stimLengthEntry.grid(row = 2, column = 1)
        self.stimLengthEntry.insert(0,500)
        
        baseLabel = tk.Label(f1, text = "Baseline Window")
        baseLabel.grid(row = 2, column = 2)
        
        self.baselineEntry = ttk.Entry(f1, text = "Baseline Window")
        self.baselineEntry.grid(row = 2, column = 3)
        self.baselineEntry.insert(0, 25)
        
        t2Label = tk.Label(f1, text = "Time 2")
        t2Label.grid(row = 2, column = 4)
        
        self.t2Entry = ttk.Entry(f1, text = "Time 2")
        self.t2Entry.grid(row = 2, column = 5)
        self.t2Entry.insert(0, 25)
        
        t3Label = tk.Label(f1, text = "Time 3")
        t3Label.grid(row = 2, column = 6)
        
        self.t3Entry = ttk.Entry(f1, text = "Time 3")
        self.t3Entry.grid(row = 2, column = 7)
        self.t3Entry.insert(0, 250)
        
        minLabel = tk.Label(f1, text = "Min: ")
        minLabel.grid(row = 4, column = 0)
        
        self.minVar = tk.StringVar()
        minDisplay = tk.Label(f1, textvariable = self.minVar)
        minDisplay.grid(row = 4, column = 1)
        
        maxLabel = tk.Label(f1, text = "Max: ")
        maxLabel.grid(row = 4, column = 2)

        self.maxVar = tk.StringVar()        
        maxDisplay = tk.Label(f1, textvariable = self.maxVar)
        maxDisplay.grid(row = 4, column = 3)
        
        ampLabel = tk.Label(f1, text = "Amplitude: ")
        ampLabel.grid(row = 4, column = 4)

        self.ampVar = tk.StringVar()        
        ampDisplay = tk.Label(f1, textvariable = self.ampVar)
        ampDisplay.grid(row = 4, column = 5)
        
        self.graphBehavior = 'all'
        self.linewidth = 0.5
        
        #temp data
        #listboxes
#        self.stimLength = 500
        
        self.offsetVar = tk.IntVar()
        self.offsetWaveforms = tk.Checkbutton(f1, variable = self.offsetVar, command = self.on_offset_select, text = "Set Average to 0")
        self.offsetWaveforms.grid(row = 3, column = 0)
        
        self.stimTypeVar = tk.IntVar()
        self.stimTypeVar.set(3)
        self.R1 = tk.Radiobutton(f1, text = "Flips", variable = self.stimTypeVar, value = 1, command = self.on_stim_select)
        self.R2 = tk.Radiobutton(f1, text = "Flops", variable = self.stimTypeVar, value = 2, command = self.on_stim_select)
        self.R3 = tk.Radiobutton(f1, text = "Average", variable = self.stimTypeVar, value = 3, command = self.on_stim_select)
        self.R1.grid(row = 3, column = 1)
        self.R2.grid(row = 3, column = 2)
        self.R3.grid(row = 3, column = 3)
        
        
        self.processedList = tk.Listbox(f2,selectmode='extended', exportselection=0, width = 50, height = 10)
        self.processedList.pack()
        self.processedList.bind('<<ListboxSelect>>',self.on_file_select)        
        
        self.selectedBlocks = tk.Listbox(f3,selectmode='extended', exportselection=0, width = 50, height = 50)
        self.selectedBlocks.pack(side=tk.RIGHT)
        self.selectedBlocks.bind('<<ListboxSelect>>',self.graph_on_select)
        
        #show the figure
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, f4)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)
    
    #graphs data from all processed files
    def graph_all(self):
        a.clear()
        amplitudes.clear()
        self.graphBehavior = 'all'
        for key in flipAverages:
            amplitudes[key[:-4]] = dict()
            for i in range(len(flipAverages[key])):
                if self.offsetVar.get() == 1:
                    if self.stimTypeVar.get() == 1:
                        a.plot(flipAverages[key][i]-np.average(flipAverages[key][i]), linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), flipAverages[key][i]-np.average(flipAverages[key][i]))
                    elif self.stimTypeVar.get() ==2:
                        a.plot(flopAverages[key][i]-np.average(flopAverages[key][i]), linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), flopAverages[key][i]-np.average(flopAverages[key][i]))
                    elif self.stimTypeVar.get() == 3:
                        avg = np.mean(np.array([flipAverages[key][i],flopAverages[key][i]]), axis = 0)
                        a.plot(avg-np.average(avg), linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), avg-np.average(avg))
                elif self.offsetVar.get() == 0:
                    if self.stimTypeVar.get() == 1:    
                        a.plot(flipAverages[key][i], linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), flipAverages[key][i])
                    elif self.stimTypeVar.get() == 2:
                        a.plot(flopAverages[key][i], linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), flopAverages[key][i])
                    elif self.stimTypeVar.get() == 3:
                        avg = np.mean(np.array([flipAverages[key][i],flopAverages[key][i]]), axis = 0)
                        a.plot(avg, linewidth = self.linewidth)
                        self.get_minmax(key[:-4], "s" + str(i), avg)
                        
    def graph_total(self):
        a.clear()
        amplitudes.clear()
        selection = self.processedList.curselection()
        selection = [self.processedList.get(item) for item in selection]
        if (len(selection) == 0):
            self.processedList.selection_set(0,tk.END)
            selection = self.processedList.curselection()
            selection = [self.processedList.get(item) for item in selection]
            
        for key in flipAverages:
            if key in selection:
                amplitudes[key[:-4]] = dict()
                if self.stimTypeVar.get() == 1:    
                    avgs = np.zeros(len(flipAverages[key][0]))
                    for i in range(len(flipAverages[key])):
                        avgs += flipAverages[key][i]
                    avgs /= len(flipAverages[key])
                    a.plot(avgs, linewidth = self.linewidth)
                    self.get_minmax(key[:-4],"total", avgs)
                elif self.stimTypeVar.get() ==2:
                    avgs = np.zeros(len(flipAverages[key][0]))
                    for i in range(len(flipAverages[key])):
                        avgs += flopAverages[key][i]
                    avgs /= len(flipAverages[key])
                    a.plot(avgs, linewidth = self.linewidth)
                    self.get_minmax(key[:-4],"total", avgs)
                elif self.stimTypeVar.get() == 3:
                    avgs = np.zeros(len(flipAverages[key][0]))
                    for i in range(len(flipAverages[key])):
                        avgs += np.mean(np.array([flipAverages[key][i],flopAverages[key][i]]), axis = 0)
                    avgs /= len(flipAverages[key])
                    a.plot(avgs, linewidth = self.linewidth, label = key)
                
                    #min max stuff
                    self.get_minmax(key[:-4], "total", avgs)


#        a.legend(loc='upper left', prop={'size':6}, bbox_to_anchor=(1,1))
#        f.tight_layout(pad = 10)
        a.legend(fontsize = 6,loc='best')
                
        
    def get_minmax(self, key, trial, array):
        t2 = self.getT2Entry()
        t3 = self.getT3Entry()
        
        min_x = array[t2:t3].argmin()
        min_y = array[t2:t3][min_x]
        max_x = array[min_x + t2:t3].argmax()
        max_y = array[min_x + t2:t3][max_x]
        a.plot(min_x + t2, min_y, marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
        a.plot(max_x + min_x + t2, max_y, marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)
        
        self.minVar.set(str(min_x + t2) + " , " +str(min_y))
        self.maxVar.set(str(max_x + min_x + t2) + " , " + str(max_y))
        self.ampVar.set(str(max_y-min_y))
        
        amplitudes[key][trial] = {"units":["V","ms"], "amplitude":max_y-min_y,"min_x":min_x + t2, "min_y":min_y, "max_x":max_x + min_x + t2, "max_y":max_y, "waveform":array}
        
    #selects an graphs sessions associated with the slected file name     
    def on_file_select(self, evt):
        a.clear()
        amplitudes.clear()
        selection = self.processedList.curselection()
        selection = [self.processedList.get(item) for item in selection]
        self.selectedBlocks.selection_set(0,tk.END)
        search = self.selectedBlocks.curselection()
        
        for item in search:
            block, key = self.selectedBlocks.get(item).split(" ")
            
            if key in selection:
                self.selectedBlocks.selection_set(item)
            elif key not in selection:
                self.selectedBlocks.selection_clear(item)
        self.graph_selected()
                    
    #decodes a given dataset and returns signal averages
    def decode(self, dat):
        
        decoder = SRP.SRPdecoder()
        decoder.stimLength = self.getStimLengthEntry()
        decoder.baseline = self.getBaselineEntry()
        signalChannel = dat[0]
        #timingChannel = d.data[3]
        codeChannels = [dat[4], dat[5]]
    
        timeCodes = decoder.GetCodeList(signalChannel, codeChannels)
        flopTimeStamps = decoder.GetTimeStamps(1, timeCodes)
        flipTimeStamps = decoder.GetTimeStamps(2, timeCodes)
        flipLengths, flopLengths = decoder.GetStimLengths(flipTimeStamps, flopTimeStamps)
        avgLength = decoder.AvgStimLength([flipTimeStamps, flopTimeStamps])
        stimsPerSession = decoder.StimsPerSession(flipLengths, flopLengths, avgLength)
        flips, flops = decoder.GetStimLists(signalChannel, stimsPerSession, avgLength, flipTimeStamps, flopTimeStamps)
        flipavgs = decoder.GetAverages(flips, stimsPerSession)
        flopavgs = decoder.GetAverages(flops, stimsPerSession)
        
        return flipavgs, flopavgs
        
    #function to graph selected items only
    def graph_selected(self):
        a.clear()
        amplitudes.clear()
        self.graphBehavior = 'selected'
        selection = self.selectedBlocks.curselection()
        for item in selection:
            block, key = self.selectedBlocks.get(item).split(" ")
            amplitudes[key[:-4]] = dict()
            if self.offsetVar.get() == 1:
                if self.stimTypeVar.get() == 1:
                    a.plot(flipAverages[key][int(block) - 1]-np.average(flipAverages[key][int(block) - 1]), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flipAverages[key][int(block) - 1]-np.average(flipAverages[key][int(block) - 1]))
                elif self.stimTypeVar.get() == 2:
                    a.plot(flopAverages[key][int(block) - 1]-np.average(flopAverages[key][int(block) - 1]), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flopAverages[key][int(block) - 1]-np.average(flopAverages[key][int(block) - 1]))
                elif self.stimTypeVar.get() == 3:
                    avg = np.mean(np.array([flipAverages[key][int(block) - 1],flopAverages[key][int(block) - 1]]), axis = 0)
                    a.plot(avg-np.average(avg), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, avg-np.average(avg))
            elif self.offsetVar.get() == 0:
                if self.stimTypeVar.get() == 1:
                    a.plot(flipAverages[key][int(block) - 1], linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flipAverages[key][int(block) - 1])
                elif self.stimTypeVar.get() == 2:
                    a.plot(flopAverages[key][int(block) - 1], linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flopAverages[key][int(block) - 1])
                elif self.stimTypeVar.get() == 3:
                    avg = np.mean(np.array([flipAverages[key][int(block) - 1],flopAverages[key][int(block) - 1]]), axis = 0)
                    a.plot(avg, linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, avg)

    def graph_on_select(self, evt):
        a.clear()
        amplitudes.clear()
        self.graphBehavior = 'selected'
        selection = self.selectedBlocks.curselection()
        for item in selection:
            block, key = self.selectedBlocks.get(item).split(" ")
            amplitudes[key[:-4]] = dict()
            if self.offsetVar.get() == 1:
                if self.stimTypeVar.get() == 1:
                    a.plot(flipAverages[key][int(block) - 1]-np.average(flipAverages[key][int(block) - 1]), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flipAverages[key][int(block) - 1]-np.average(flipAverages[key][int(block) - 1]))
                elif self.stimTypeVar.get() == 2:
                    a.plot(flopAverages[key][int(block) - 1]-np.average(flopAverages[key][int(block) - 1]), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flopAverages[key][int(block) - 1]-np.average(flopAverages[key][int(block) - 1]))
                elif self.stimTypeVar.get() == 3:
                    avg = np.mean(np.array([flipAverages[key][int(block) - 1],flopAverages[key][int(block) - 1]]), axis = 0)
                    a.plot(avg-np.average(avg), linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, avg-np.average(avg))
            elif self.offsetVar.get() == 0:
                if self.stimTypeVar.get() == 1:
                    a.plot(flipAverages[key][int(block) - 1], linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flipAverages[key][int(block) - 1])
                elif self.stimTypeVar.get() == 2:
                    a.plot(flopAverages[key][int(block) - 1], linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, flopAverages[key][int(block) - 1])
                elif self.stimTypeVar.get() == 3:
                    avg = np.mean(np.array([flipAverages[key][int(block) - 1],flopAverages[key][int(block) - 1]]), axis = 0)
                    a.plot(avg, linewidth = self.linewidth)
                    self.get_minmax(key[:-4], "s" + block, avg)
        
    def save(self):
        self.graph_all()
        savedamps = amplitudes.copy()
        
        self.graph_total()
        
        for key in amplitudes:
            c = amplitudes[key].copy()
            c.update(savedamps[key])
            savedamps[key] = c
        
        save = ds.DictionarySaver()
        #print savedamps

        save.saveDictionary(savedamps, data.keys()[0][:-4])
        #matlab.savemat(data.keys()[0], amplitudes)
        
    def on_stim_select(self):
        if self.graphBehavior == 'all':
            self.graph_all()
        elif self.graphBehavior == 'selected':
            self.graph_all()
        
    def on_offset_select(self):
        if self.graphBehavior == 'all':
            self.graph_all()
        elif self.graphBehavior == 'selected':
            self.graph_selected()
    
    #brings names in controller into listbox
    def process(self):
        amplitudes.clear()
        for key in data.keys():
            print "processing " + key + "..."
            entry = data[key]
            flipavgs, flopavgs  = self.decode(entry)
            flipAverages[key] = flipavgs
            flopAverages[key] = flopavgs
            print "done"
    
        self.processedList.delete(0, tk.END)
        self.selectedBlocks.delete(0,tk.END)
        for a, b in enumerate(data):
            self.processedList.insert(a, b)
            
        for a, b in enumerate(flipAverages):
            for i in range(len(flipAverages[b])):
                self.selectedBlocks.insert(tk.END, str(i + 1) + " " + b)
        

        self.graph_all()
        self.graph_total()
        
        
            
    def getStimLengthEntry(self):
        length = self.stimLengthEntry.get()
        if length == '':
            return 500
        try:
            length = int(length)
            return length
        except ValueError:
            print "stim length must be an integer"
            return 500
            
    def getBaselineEntry(self):
        window = self.baselineEntry.get()
        if window == '':
            return 25
        if int(window) == 0:
            return 1
        try:
            window = int(window)
            return window
        except ValueError:
            print "stim length must be an integer"
            return 500
            
    def getT2Entry(self):
        t2 = self.t2Entry.get()
        if t2 == '':
            return 25
        if int(t2) == 0:
            return 1
        try:
            t2 = int(t2)
            return t2
        except ValueError:
            print "time window start must be an integer"
            return 25
            
    def getT3Entry(self):
        t3 = self.t3Entry.get()
        if t3 == '':
            return 25
        if int(t3) == 0:
            return 1
        try:
            t3 = int(t3)
            return t3
        except ValueError:
            print "time window start must be an integer"
            return 25
    
    
    def view_raws(self):
        datafile.plotData()
            
        
        
        
        
app = Application()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
        