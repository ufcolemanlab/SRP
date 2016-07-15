# -*- coding: utf-8 -*-
"""
Created on Tue May 24 17:45:55 2016

@author: Jesse
"""

import Tkinter as tk
import ttk
import tkFileDialog
import os

import DictionarySaver as ds
import DataHandler as dh

import matplotlib
matplotlib.use("TkAgg", warn=False)

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


#global figures
LARGE_FONT = ("Verdana", 12)
style.use("bmh")

f = Figure(figsize = (10,5), dpi = 100)
a = f.add_subplot(111)
a.plot([0 for i in range(500)])

Data = dh.DataHandler()

orientations = {1:["A","flop"], 2:["A","flip"], 3:["B","flop"], 4:["B","flip"],
                5:["C","flop"], 6:["C","flip"], 7:["D","flop"], 8:["D","flip"]}
orientation_lookup = {"A":[1,2], "B":[3,4], "C":[4,5], "D":[7,8]}

best_max = 50000

#global animation
def animate(i):
    pass

#main application
class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        oscheck = os.name
        if str.find(oscheck,'posix') < 0:
            tk.Tk.iconbitmap(self, default = "mouse.ico")
        tk.Tk.wm_title(self, "SRP Analysis")
        
        #set resolution scaling
        #self.call('tk', 'scaling', 2.0)
        
        
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, GraphPage):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
       
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
        
#        button2 = ttk.Button(f, text="SRP Analysis",
#                             command = lambda: controller.show_frame(GraphPage))
#        button2.grid(row = 1, column = 1)
        
        button3 = ttk.Button(f, text = "Clear All",
                             command = lambda:  self.clear())
        button3.grid(row = 1, column = 2, padx = 10, pady = 10)
        
#        w = win.winfo_screenwidth()
#        h = win.winfo_screenheight()
        
    #loads data into controller and poplates listbox with filenames
    def load(self):
        
        files = tkFileDialog.askopenfilenames(title='Choose files')
        filelist = list(files) 
        for filename in filelist:
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
        
#        w=root.winfo_screenwidth()
#        h=root.winfo_screenheight()
#        root.geometry("400x300+%d+%d" % ( (w-400)/2, (h-300)/2 ) )
 
        center_anchor = tk.Frame(self)
        center_anchor.pack(anchor = 'center')
        
        #windows
        window1 = tk.Toplevel(self)
        window2 = tk.Toplevel(self)
        window3 = tk.Toplevel(self)
        
        
        #list boxes to the right
        right_panel = tk.Frame(window2)
        right_panel.pack(side = tk.RIGHT)
        
        #graph and control panel to the left
        left_panel = tk.Frame(window3)
        left_panel.pack(anchor = 'center')
        
        #container for control panel
        f1 = tk.Frame(window1)
        f1.pack(side = tk.TOP)
        
        #containers for list boxes
        f2 = tk.Frame(right_panel)
        f2.pack(anchor = 'ne')
        
        f3 = tk.Frame(right_panel)
        f3.pack(side = tk.RIGHT)
        
        #container for plot, toolbar
        f4 = tk.Frame(left_panel)
        f4.pack(anchor = 'center')
        
        f5 = tk.Frame(f4)
        f5.pack(side = tk.BOTTOM)
        
        f6 = tk.Frame(f4)
        f6.pack(side = tk.TOP)
        
        
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
        

        button7 = ttk.Button(f1, text = "Save All",
                             command = lambda: self.save('all'))         
                             
        button7.grid(row = 1, column = 6)
        
        button8 = ttk.Button(f1, text = 'Save Selected',
                             command = lambda: self.save('selected'))
        button8.grid(row = 1, column = 7)
        
        
        stimlabel = tk.Label(f1, text="Stim Length")
        stimlabel.grid(row = 2, column = 0, padx = 10, pady = 10)
        
        self.stimLengthEntry = ttk.Entry(f1, text = "Stim Length")
        self.stimLengthEntry.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.stimLengthEntry.insert(0,500)
        
        baseLabel = tk.Label(f1, text = "Baseline Window")
        baseLabel.grid(row = 2, column = 2, padx = 10, pady = 10)
        
        self.baselineEntry = ttk.Entry(f1, text = "Baseline Window")
        self.baselineEntry.grid(row = 2, column = 3, padx = 10, pady = 10)
        self.baselineEntry.insert(0, 25)
        

        

        #sliding scales for window selection
        self.min_slider = tk.Scale(f1, from_=0, to=500, label = "min window", orient = tk.HORIZONTAL,
                                   command = self.on_slider_move)
        self.min_slider.grid(row = 3, column = 2, padx = 10, pady = 10)
        self.min_slider.set(25)
        
        self.max_slider = tk.Scale(f1, from_=0, to=500, label = "max window", orient = tk.HORIZONTAL,
                                   command = self.on_slider_move)
        self.max_slider.grid(row = 3, column = 3, padx = 10, pady = 10)
        self.max_slider.set(250)
        
#        minLabel = tk.Label(f1, text = "Min: ")
#        minLabel.grid(row = 4, column = 0)
#        
#        self.minVar = tk.StringVar()
#        minDisplay = tk.Label(f1, textvariable = self.minVar)
#        minDisplay.grid(row = 4, column = 1)
#        
#        maxLabel = tk.Label(f1, text = "Max: ")
#        maxLabel.grid(row = 4, column = 2)
#
#        self.maxVar = tk.StringVar()        
#        maxDisplay = tk.Label(f1, textvariable = self.maxVar)
#        maxDisplay.grid(row = 4, column = 3)
#        
#        ampLabel = tk.Label(f1, text = "Amplitude: ")
#        ampLabel.grid(row = 4, column = 4)
#
#        self.ampVar = tk.StringVar()        
#        ampDisplay = tk.Label(f1, textvariable = self.ampVar)
#        ampDisplay.grid(row = 4, column = 5)
        
        
        self.graphBehavior = 'total'
        self.selectionBehavior = 'file'
        self.linewidth = 0.5
        
        #graph novel/familar tick boxes
        self.familiarVar = tk.IntVar()
        self.familiar = tk.Checkbutton(f1, variable = self.familiarVar, command = self.on_familiar_select, text = orientations[1][0])
        self.familiar.grid(row = 3, column = 0)
        self.familiarVar.set(1)
        
        self.novelVar = tk.IntVar()
        self.novel = tk.Checkbutton(f1, variable = self.novelVar, command = self.on_novel_select, text = orientations[3][0])
        self.novel.grid(row = 3, column = 1)
        
        self.mouse_min_var = tk.IntVar()
        self.mouse_max_var = tk.IntVar()
        self.mouse_min_box = tk.Checkbutton(f6, variable = self.mouse_min_var, command = self.on_mouse_min_select, text = 'allow mouse min selection')
        self.mouse_max_box = tk.Checkbutton(f6, variable = self.mouse_max_var, command = self.on_mouse_max_select, text = 'allow mouse max selection')
        self.mouse_min_box.pack(side = tk.LEFT)
        self.mouse_max_box.pack(side = tk.LEFT)
        
        #flip/flop/average radio buttons
        self.stimTypeVar = tk.IntVar()
        self.stimTypeVar.set(3)
        self.R1 = tk.Radiobutton(f1, text = "Flips", variable = self.stimTypeVar, value = 1, command = self.on_stim_select)
        self.R2 = tk.Radiobutton(f1, text = "Flops", variable = self.stimTypeVar, value = 2, command = self.on_stim_select)
        self.R3 = tk.Radiobutton(f1, text = "Average", variable = self.stimTypeVar, value = 3, command = self.on_stim_select)
        self.R1.grid(row = 2, column = 4)
        self.R2.grid(row = 2, column = 5)
        self.R3.grid(row = 2, column = 6)
        
        #amplitude radio buttons
        self.lock_selected = tk.IntVar()
        self.lock_selected.set(2)
        self.unlocked = tk.Radiobutton(f1, text = "set all amplitudes", variable = self.lock_selected, value = 1)
        self.locked = tk.Radiobutton(f1, text = "set amps by file", variable = self.lock_selected, value = 2)
        self.stimlocked = tk.Radiobutton(f1, text = "set amps by session", variable = self.lock_selected, value = 3)
        self.unlocked.grid(row = 3, column = 5)
        self.locked.grid(row = 3, column = 6)
        self.stimlocked.grid(row = 3, column =7)

        #file and stim listboxes
        self.processedList = tk.Listbox(f2,selectmode='extended', exportselection=0, width = 50, height = 10)
        self.processedList.pack(side = tk.RIGHT, padx = 10, pady = 10)
        self.processedList.bind('<<ListboxSelect>>',self.on_file_select)      
        self.selectedFiles = list()
        self.listSelect = False

        
        self.selectedBlocks = tk.Listbox(f3,selectmode='extended', exportselection=0, width = 50, height = 40)
        self.selectedBlocks.pack(side=tk.RIGHT, padx = 10, pady = 10)
        self.selectedBlocks.bind('<<ListboxSelect>>',self.graph_on_select)
        
        #show the figure
        canvas = FigureCanvasTkAgg(f, f4)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, padx = 10, pady = 10, fill = tk.BOTH)
        
        toolbar = NavigationToolbar2TkAgg(canvas, f5)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.BOTTOM)
        
        cid = f.canvas.mpl_connect('button_press_event', self.mouse_select)
        
        w = window1.winfo_screenwidth()
        h = window1.winfo_screenheight()
        window1.geometry("+%d+%d" % ( w/2 - window1.winfo_width()/2, 0))
        window2.geometry("+%d+%d" % ( w - window2.winfo_width(), (h)/2 - window2.winfo_height()/2))
        window3.geometry("+%d+%d" % ( (w)/2 - 500, (h)/2-200))


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
        
        self.graphBehavior = 'total'
        
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
                
        a.legend(fontsize = 6,loc='best')
                
        
    #selects an graphs sessions associated with the slected file name     
    def on_file_select(self, evt):
        self.listSelect = True
        a.clear()
        selection = self.processedList.curselection()
        selection = [self.processedList.get(item) for item in selection]
        
        if self.lock_selected.get() != 3:
            self.selectedBlocks.selection_set(0,tk.END)
        elif self.lock_selected.get() == 3:
            self.selectedBlocks.selection_clear(0, tk.END)
        
        search = self.selectedBlocks.curselection()
        
        for item in search:
            block, key = self.selectedBlocks.get(item).split("  ")
            
            
            if key in selection:
                self.selectedBlocks.selection_set(item)
            elif key not in selection:
                self.selectedBlocks.selection_clear(item)
                
            ori, block = block.split(" ")
            ori = orientation_lookup[ori][0]
            for key in selection:
                for ori in Data.grand_amps[key]:
                    self.min_slider.set(Data.grand_amps[key][ori][0]["lower"])
                    self.max_slider.set(Data.grand_amps[key][ori][0]["upper"])
        #self.graph_selected()
        self.graph_total()
        self.listSelect = False
    
    def set_amplitudes(self):
        
        selection = self.selectedBlocks.curselection()
        
        file_selection = self.processedList.curselection()
        file_selection = [str(self.processedList.get(item)) for item in file_selection]
        
        lower = self.getT2Entry()
        upper = self.getT3Entry()
        
        stimTypeVar = self.stimTypeVar.get()
        if stimTypeVar == 1:
            lookupIndex = 1
        elif stimTypeVar ==2 or stimTypeVar == 3:
            lookupIndex = 0
        
        for item in selection:
            block, key = self.selectedBlocks.get(item).split("  ")
            orientation, block = block.split(" ")
            block = int(block) - 1
            
            if stimTypeVar != 3:
                stim_type = orientation_lookup[orientation][lookupIndex]
                Data.set_amplitude(Data.stim_avgs, Data.amplitudes, lower, upper, key, stim_type, block)
            elif stimTypeVar == 3:
                stim_type = orientation_lookup[orientation][lookupIndex]
                Data.set_amplitude(Data.orient_avgs, Data.orient_amplitudes, lower, upper, key, stim_type, block)
        
        if self.lock_selected.get() == 2 or self.graphBehavior == 'total':
            for key in file_selection:
                Data.set_grand_amp(Data.total_avgs, Data.total_amplitudes, lower, upper, key)
                Data.set_grand_amp(Data.grand_avgs, Data.grand_amps, lower, upper, key)            
        

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
        #self.processedList.selection_clear(0,tk.END)
        self.graphBehavior = 'selected'
        self.lock_selected.set(3)
        
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
            if self.listSelect == False:
                if stimTypeVar != 3:
                    stim_type = orientation_lookup[orientation][lookupIndex]
                    self.min_slider.set(Data.amplitudes[key][stim_type][block]["lower"])
                    self.max_slider.set(Data.amplitudes[key][stim_type][block]["upper"])
                elif stimTypeVar == 3:
                    stim_type = orientation_lookup[orientation][lookupIndex]
                    self.min_slider.set(Data.orient_amplitudes[key][stim_type][block]["lower"])
                    self.max_slider.set(Data.orient_amplitudes[key][stim_type][block]["upper"])
                       
        self.graph_selected()
        
    def save(self, mode):
        self.graph_total
        
        if mode == 'all':
            savedamps = Data.orient_amplitudes.copy()
        elif mode == 'selected':
            savedamps = dict()
            file_selection = self.processedList.curselection()
            file_selection = [str(self.processedList.get(item)) for item in file_selection]
            for fn in file_selection:
                savedamps[fn] = dict()
            
        print "saving amplitude data..."
        for fn in [key for key in savedamps.keys()]:
            c = Data.orient_amplitudes[fn].copy()
            c.update(savedamps[fn])
            savedamps[fn] = c
            for ori in Data.orient_amplitudes[fn]:
                d = Data.orient_amplitudes[fn][ori].copy()
                #d.update(savedamps[fn]['ori'+str(ori)])
                savedamps[fn][orientations[ori][0]] = d
                savedamps[fn][orientations[ori][0]]['total'] = Data.grand_amps[fn][ori][0]
                for trial in Data.orient_amplitudes[fn][ori]:
                    e = Data.orient_amplitudes[fn][ori][trial]
                    #e.update(savedamps[fn]['ori' + str(ori)][trial])
                    print [(i, e[i]) for i in e if i != 'waveform']
                    savedamps[fn][orientations[ori][0]]['trial' + str(trial + 1)] = e
            truncated = fn[:-4]
            savedamps[truncated] = savedamps[fn]
            del savedamps[fn]
            
        save = ds.DictionarySaver()
        try:
            save.saveDictionary(savedamps, Data.amplitudes.keys()[0][:-4])
        except IndexError:
            print "error saving: missing data"

    def on_stim_select(self):
        self.re_graph()
        
    def on_familiar_select(self):
        self.re_graph()
    
    def on_novel_select(self):
        self.re_graph()
    
    def get_amplitudes(self, amplitudes):
        for a, b in amplitudes:
            b.clear()
            Data.get_amplitudes(a, b, self.getT2Entry(), self.getT3Entry())
    

    def mouse_select(self, event):
        mouse_x = event.xdata
        mouse_y = event.ydata
        if type(mouse_x) == None or type(mouse_y) == None:
            return
        if len(self.processedList.get(0, tk.END)) < 1:
            return
            
        if self.graphBehavior == 'total':
            selection = self.processedList.curselection()
            selection = [self.processedList.get(item) for item in selection]
            best_y = best_max
            best_fn = selection[0]
            best_ori = 1
            if self.stimTypeVar.get() == 3:
                for fn in selection:
                    for ori in Data.grand_amps[fn]:
                        this_y = Data.grand_amps[fn][ori][0]['waveform'][int(mouse_x)]
                        if abs(this_y - mouse_y) < abs(best_y - mouse_y):
                            best_y = this_y
                            best_fn = fn
                            best_ori = ori
                if self.mouse_max_var.get() == 1:
                    Data.grand_amps[best_fn][best_ori][0]['max_x'] = mouse_x
                    Data.grand_amps[best_fn][best_ori][0]['max_y'] = best_y
                elif self.mouse_min_var.get() == 1:
                    Data.grand_amps[best_fn][best_ori][0]['min_x'] = mouse_x
                    Data.grand_amps[best_fn][best_ori][0]['min_y'] = best_y
            elif self.stimTypeVar.get() != 3:
                for fn in selection:
                    for ori in Data.total_amplitudes[fn]:
                        orientation = orientations[ori][0]
                        if self.stimTypeVar.get() == 1:
                            orientation = orientation_lookup[orientation][1]
                        elif self.stimTypeVar.get() == 2:
                            orientation = orientation_lookup[orientation][0]
                        
                        this_y = Data.total_amplitudes[fn][orientation][0]['waveform'][int(mouse_x)]
                        if abs(this_y - mouse_y) < abs(best_y - mouse_y):
                            best_y = this_y
                            best_fn = fn
                            best_ori = orientation
                if self.mouse_max_var.get() == 1:
                    Data.total_amplitudes[best_fn][best_ori][0]['max_x'] = mouse_x
                    Data.total_amplitudes[best_fn][best_ori][0]['max_y'] = best_y
                elif self.mouse_min_var.get() == 1:
                    Data.total_amplitudes[best_fn][best_ori][0]['min_x'] = mouse_x
                    Data.total_amplitudes[best_fn][best_ori][0]['min_y'] = best_y
            
                
        elif self.graphBehavior == 'all' or self.graphBehavior == 'selected':
            if self.graphBehavior == 'all':
                selection = self.selectedBlocks.get(0, tk.END)
            elif self.graphBehavior == 'selected':
                selection = self.selectedBlocks.curselection()
                selection = [self.selectedBlocks.get(item) for item in selection]
            #selection = [self.selectedBlocks.get(item) for item in selection]
            
            if len(selection) < 1:
                return
            stim, key = selection[0].split("  ")
            orientation, block = stim.split(" ")
            best_y = best_max
            best_fn = key
            best_ori = orientation_lookup[orientation][0]
            best_session = 0
            if self.stimTypeVar.get() == 3:
                for fn in selection:
                    stim, key = fn.split("  ")
                    orientation, block = stim.split(" ")
                    block = int(block) -1
                    orientation = orientation_lookup[orientation][0]
                    this_y = Data.orient_amplitudes[key][orientation][block]['waveform'][int(mouse_x)]
                    if abs(this_y - mouse_y) < abs(best_y - mouse_y):
                        best_y = this_y
                        best_fn = key
                        best_ori = orientation
                        best_session = block
                if self.mouse_max_var.get() == 1:
                    Data.orient_amplitudes[best_fn][best_ori][best_session]['max_x'] = mouse_x
                    Data.orient_amplitudes[best_fn][best_ori][best_session]['max_y'] = best_y
                elif self.mouse_min_var.get() == 1:
                    Data.orient_amplitudes[best_fn][best_ori][best_session]['min_x'] = mouse_x
                    Data.orient_amplitudes[best_fn][best_ori][best_session]['min_y'] = best_y
            elif self.stimTypeVar.get() != 3:
                for fn in selection:
                    stim, key = fn.split("  ")
                    orientation, block = stim.split(" ")
                    if self.stimTypeVar.get() == 1:
                        orientation = orientation_lookup[orientation][1]
                    elif self.stimTypeVar.get() == 2:
                        orientation = orientation_lookup[orientation][0]
                    block = int(block) - 1
                    this_y = Data.amplitudes[key][orientation][block]['waveform'][int(mouse_x)]
                    if abs(this_y - mouse_y) < abs(best_y - mouse_y):
                        best_y = this_y
                        best_fn = key
                        best_ori = orientation
                        best_session = block
                if self.mouse_max_var.get() == 1:
                    Data.amplitudes[best_fn][best_ori][best_session]['max_x'] = mouse_x
                    Data.amplitudes[best_fn][best_ori][best_session]['max_y'] = best_y
                elif self.mouse_min_var.get() == 1:
                    Data.amplitudes[best_fn][best_ori][best_session]['min_x'] = mouse_x
                    Data.amplitudes[best_fn][best_ori][best_session]['min_y'] = best_y
                    
               
        self.re_graph()
        #a.plot(int(mouse_x), best_y, marker = '+', color = 'blue', markersize = 10, markeredgewidth = 2)
        
        
        #print ('x=%f, y=%f' % (event.xdata, event.ydata))
        
    def on_mouse_min_select(self):
        if self.mouse_min_var.get() == 1:
            self.mouse_max_var.set(0)
            
    def on_mouse_max_select(self):
        if self.mouse_max_var.get() == 1:
            self.mouse_min_var.set(0)
            
    #brings names in controller into listbox
    def process(self):
        for filename in Data.fileData.keys():
            print "processing " + filename + "..."
            stimLength = self.getStimLengthEntry()
            baseline = self.getBaselineEntry()
            
            #need to add channel # selection
            Data.process_file(filename, Data.detect_channels(filename), stimLength, baseline)
#            Data.get_amplitudes(Data.stim_avgs, Data.amplitudes, self.getT2Entry(), self.getT3Entry())
#            Data.get_amplitudes(Data.orient_avgs, Data.orient_amplitudes, self.getT2Entry(), self.getT3Entry())
#            Data.get_amplitudes(Data.total_avgs, Data.total_amplitudes, self.getT2Entry(), self.getT3Entry())
#            Data.get_amplitudes(Data.grand_avgs, Data.grand_amps, self.getT2Entry(), self.getT3Entry())
            self.get_amplitudes([(Data.stim_avgs,Data.amplitudes),(Data.orient_avgs,Data.orient_amplitudes),
                                 (Data.grand_avgs,Data.grand_amps),(Data.total_avgs,Data.total_amplitudes)])
            
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
        
        self.re_graph()
        
        
            
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
    
    def on_slider_move(self, evt):
        if self.lock_selected.get() == 1:
            self.get_amplitudes([(Data.stim_avgs,Data.amplitudes),(Data.orient_avgs,Data.orient_amplitudes),
                                 (Data.grand_avgs,Data.grand_amps),(Data.total_avgs,Data.total_amplitudes)])
        elif self.lock_selected.get() == 2 or self.lock_selected.get() == 3:
            self.set_amplitudes()
        self.re_graph()
            
    def getT2Entry(self):
        maxwin = self.max_slider.get()
        minwin = self.min_slider.get()
        if maxwin <= minwin:
            minwin = 25
            self.min_slider.set(25)
            self.max_slider.set(250)
        
        return minwin
            
    def getT3Entry(self):
        maxwin = self.max_slider.get()
        minwin = self.min_slider.get()
        if maxwin <= minwin:
            maxwin = 250
            self.min_slider.set(25)
            self.max_slider.set(250)
        
        return maxwin
    
    def re_graph(self):
        if self.graphBehavior == 'all':
            self.graph_all()
        elif self.graphBehavior == 'selected':
            self.graph_selected()
        elif self.graphBehavior == 'total':
            self.graph_total()
        
    def view_raws(self):
        try:
            Data.graph_raw(Data.filenames.keys()[0])
        except IndexError:
            print "graphing error: missing data"
            
        
app = Application()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
        