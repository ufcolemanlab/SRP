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
import os

import DictionarySaver as ds
import DataHandler as dh

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style




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

Data = dh.DataHandler()

orientations = {1:["A","flop"], 2:["A","flip"], 3:["B","flop"], 4:["B","flip"], 5:["C","flop"], 6:["C","flip"], 7:["D","flop"], 8:["D","flip"]}
orientation_lookup = {"A":[1,2], "B":[3,4], "C":[4,5], "D":[7,8]}

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
        #self.data = dh.DataHandler()
        
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
#                datafile.setFilename(filename)
#                datafile.openDataFile()
#                data[os.path.basename(filename)] = datafile.data
            Data.add_file(filename)
                
        self.loadbox.delete(0, tk.END)
        for a, b in enumerate(Data.fileData):
            self.loadbox.insert(a, b)
        
    def clear(self):
        Data.clear_all()
        for guy in Data.fileData:
            print guy + str(", you shouldn't see this, contact a programmer...")
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
        
        self.familiarVar = tk.IntVar()
        self.familiar = tk.Checkbutton(f1, variable = self.familiarVar, command = self.on_familiar_select, text = orientations[1][0])
        self.familiar.grid(row = 3, column = 0)
        self.familiarVar.set(1)
        
        self.novelVar = tk.IntVar()
        self.novel = tk.Checkbutton(f1, variable = self.novelVar, command = self.on_novel_select, text = orientations[3][0])
        self.novel.grid(row = 3, column = 1)
        
        self.stimTypeVar = tk.IntVar()
        self.stimTypeVar.set(3)
        self.R1 = tk.Radiobutton(f1, text = "Flips", variable = self.stimTypeVar, value = 1, command = self.on_stim_select)
        self.R2 = tk.Radiobutton(f1, text = "Flops", variable = self.stimTypeVar, value = 2, command = self.on_stim_select)
        self.R3 = tk.Radiobutton(f1, text = "Average", variable = self.stimTypeVar, value = 3, command = self.on_stim_select)
        self.R1.grid(row = 3, column = 2)
        self.R2.grid(row = 3, column = 3)
        self.R3.grid(row = 3, column = 4)
        
        
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
  
    def graph_all(self):
        a.clear()
        self.graphBehavior = 'all'
        for fn in Data.fileData:
            if self.stimTypeVar.get() == 1:
                for i in Data.stim_avgs[fn]:
                    if i % 2 == 0:
                        for j in range(len(Data.stim_avgs[fn][i])):
                            a.plot(Data.stim_avgs[fn][i][j], linewidth = self.linewidth)
                            a.plot(Data.amplitudes[fn][i][j]["min_x"],Data.amplitudes[fn][i][j]["min_y"], 
                                 marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                            a.plot(Data.amplitudes[fn][i][j]["max_x"],Data.amplitudes[fn][i][j]["max_y"], 
                                 marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
            elif self.stimTypeVar.get() ==2:
                for i in Data.stim_avgs[fn]:
                    if i % 2 != 0:
                        for j in range(len(Data.stim_avgs[fn][i])):
                            a.plot(Data.stim_avgs[fn][i][j], linewidth = self.linewidth)
                            a.plot(Data.amplitudes[fn][i][j]["min_x"],Data.amplitudes[fn][i][j]["min_y"], 
                                 marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                            a.plot(Data.amplitudes[fn][i][j]["max_x"],Data.amplitudes[fn][i][j]["max_y"], 
                                 marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
            elif self.stimTypeVar.get() ==3:
                for key in Data.orient_avgs[fn]:
                    for i in range(len(Data.orient_avgs[fn][key])):
                        a.plot(Data.orient_avgs[fn][key][i], linewidth = self.linewidth)
                        a.plot(Data.orient_amplitudes[fn][key][i]["min_x"],Data.orient_amplitudes[fn][key][i]["min_y"], 
                             marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.orient_amplitudes[fn][key][i]["max_x"],Data.orient_amplitudes[fn][key][i]["max_y"], 
                             marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                        
                                 
                        
    def graph_total(self):
        
        #get selectiosn
        a.clear()
        selection = self.processedList.curselection()
        selection = [self.processedList.get(item) for item in selection]
        if (len(selection) == 0):
            self.processedList.selection_set(0,tk.END)
            selection = self.processedList.curselection()
            selection = [self.processedList.get(item) for item in selection]
        #print selection
        
        #get novelty choice
        novel = self.novelVar.get()
        familiar = self.familiarVar.get()
            
        for key in Data.grand_avgs:
            if key in selection:
                if self.stimTypeVar.get() == 3:
                    if familiar == 1:
                        a.plot(Data.grand_avgs[key][1][0], label = orientations[1][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.grand_amps[key][1][0]["min_x"],Data.grand_amps[key][1][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.grand_amps[key][1][0]["max_x"],Data.grand_amps[key][1][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                    if novel == 1 and len(Data.grand_avgs[key])>1:
                        a.plot(Data.grand_avgs[key][3][0], label = orientations[3][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.grand_amps[key][3][0]["min_x"],Data.grand_amps[key][3][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.grand_amps[key][3][0]["max_x"],Data.grand_amps[key][3][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                elif self.stimTypeVar.get() == 1:
                    if familiar == 1:
                        a.plot(Data.total_avgs[key][2][0], label = orientations[2][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.total_amplitudes[key][2][0]["min_x"],Data.total_amplitudes[key][2][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.total_amplitudes[key][2][0]["max_x"],Data.total_amplitudes[key][2][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                    if novel == 1 and len(Data.grand_avgs[key])>1:
                        a.plot(Data.total_avgs[key][4][0], label = orientations[4][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.total_amplitudes[key][4][0]["min_x"],Data.total_amplitudes[key][4][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.total_amplitudes[key][4][0]["max_x"],Data.total_amplitudes[key][4][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                        
                elif self.stimTypeVar.get() == 2:
                    if familiar == 1:
                        a.plot(Data.total_avgs[key][1][0], label = orientations[1][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.total_amplitudes[key][1][0]["min_x"],Data.total_amplitudes[key][1][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.total_amplitudes[key][1][0]["max_x"],Data.total_amplitudes[key][1][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                    if novel == 1 and len(Data.grand_avgs[key])>1:
                        a.plot(Data.total_avgs[key][3][0], label = orientations[3][0] +" "+ key, linewidth = self.linewidth)
                        a.plot(Data.total_amplitudes[key][3][0]["min_x"],Data.total_amplitudes[key][3][0]["min_y"], 
                               marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                        a.plot(Data.total_amplitudes[key][3][0]["max_x"],Data.total_amplitudes[key][3][0]["max_y"], 
                               marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                


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
            block, key = self.selectedBlocks.get(item).split("  ")
            
            if key in selection:
                self.selectedBlocks.selection_set(item)
            elif key not in selection:
                self.selectedBlocks.selection_clear(item)
        self.graph_total()
        #self.graph_selected
                    

    #function to graph selected items only
    def graph_selected(self):
        a.clear()
        self.graphBehavior = 'selected'
        selection = self.selectedBlocks.curselection()
        
        stimTypeVar = self.stimTypeVar.get()
        if stimTypeVar == 1:
            lookupIndex = 1
        elif stimTypeVar == 2 or stimTypeVar == 3:
            lookupIndex = 0
            
        for item in selection:
            block, key = self.selectedBlocks.get(item).split("  ")
            orientation, block = block.split(" ")
            block = int(block) - 1
            if stimTypeVar != 3:
                stim_type = orientation_lookup[orientation][lookupIndex]
                a.plot(Data.stim_avgs[key][stim_type][block], linewidth = self.linewidth)
                a.plot(Data.amplitudes[key][stim_type][block]["min_x"],Data.amplitudes[key][stim_type][block]["min_y"], 
                       marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                a.plot(Data.amplitudes[key][stim_type][block]["max_x"],Data.amplitudes[key][stim_type][block]["max_y"], 
                       marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
            elif stimTypeVar == 3:
                stim_type = orientation_lookup[orientation][lookupIndex]
                a.plot(Data.orient_avgs[key][stim_type][block], linewidth = self.linewidth)
                a.plot(Data.orient_amplitudes[key][stim_type][block]["min_x"],Data.orient_amplitudes[key][stim_type][block]["min_y"], 
                       marker = '+', color = 'red', markersize = 10, markeredgewidth = 2)
                a.plot(Data.orient_amplitudes[key][stim_type][block]["max_x"],Data.orient_amplitudes[key][stim_type][block]["max_y"], 
                       marker = '+', color = 'limegreen', markersize = 10, markeredgewidth = 2)  
                

    def graph_on_select(self, evt):
        self.graph_selected()
        
    def save(self):
        self.graph_total
        
        savedamps = Data.orient_amplitudes.copy()
        
        self.graph_total()
        
        for fn in Data.orient_amplitudes:
            c = Data.orient_amplitudes[fn].copy()
            c.update(savedamps[fn])
            savedamps[fn] = c
            for ori in Data.orient_amplitudes[fn]:
                d = Data.orient_amplitudes[fn][ori].copy()
                #d.update(savedamps[fn]['ori'+str(ori)])
                savedamps[fn]['ori' + str(ori)] = d
                savedamps[fn]['ori' + str(ori)]['total'] = Data.grand_amps[fn][ori][0]
                for trial in Data.orient_amplitudes[fn][ori]:
                    e = Data.orient_amplitudes[fn][ori][trial]
                    #e.update(savedamps[fn]['ori' + str(ori)][trial])
                    savedamps[fn]['ori' + str(ori)]['trial' + str(trial)] = e
            truncated = fn[:-4]
            savedamps[truncated] = savedamps[fn]
            del savedamps[fn]
            
            
        
        print savedamps
        save = ds.DictionarySaver()
        save.saveDictionary(savedamps, Data.amplitudes.keys()[0][:-4])

    def on_stim_select(self):
        if self.graphBehavior == 'all':
            self.graph_all()
        elif self.graphBehavior == 'selected':
            self.graph_selected()
        
    def on_familiar_select(self):
        self.graph_total()
    
    def on_novel_select(self):
        self.graph_total()
    
    #brings names in controller into listbox
    def process(self):
        for filename in Data.fileData.keys():
            print "processing " + filename + "..."
            stimLength = self.getStimLengthEntry()
            baseline = self.getBaselineEntry()
            
            #need to add channel # selection
            Data.process_file(filename, Data.detect_channels(filename), stimLength, baseline)
            Data.get_amplitudes(Data.stim_avgs, Data.amplitudes, self.getT2Entry(), self.getT3Entry())
            Data.get_amplitudes(Data.orient_avgs, Data.orient_amplitudes, self.getT2Entry(), self.getT3Entry())
            Data.get_amplitudes(Data.total_avgs, Data.total_amplitudes, self.getT2Entry(), self.getT3Entry())
            Data.get_amplitudes(Data.grand_avgs, Data.grand_amps, self.getT2Entry(), self.getT3Entry())
            
            print "done"
    
        self.processedList.delete(0, tk.END)
        self.selectedBlocks.delete(0,tk.END)
        for a, b in enumerate(Data.fileData):
            self.processedList.insert(a, b)
            
        for a, b in enumerate(Data.stim_avgs):
            for c in Data.stim_avgs[b]:
                for i in range(len(Data.stim_avgs[b][c])):
                    if orientations[c][1] == "flip":
                        self.selectedBlocks.insert(tk.END, orientations[c][0] + " " + str(i+1) + "  " + b)
        

        #self.graph_all()
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
        Data.graph_raw(Data.filenames.keys()[0])
            
        
        
        
        
app = Application()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
        