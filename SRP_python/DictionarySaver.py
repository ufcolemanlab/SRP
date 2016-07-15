# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 14:35:18 2016

@author: Isaiah Nields
"""

import scipy.io as sio
import tkFileDialog



class DictionarySaver():
    def __init__(self):

        self.file_opt = options = {}             
        options['defaultextension'] = '.mat'        
        options['filetypes'] = [('Matlab file', ".mat")]

    def saveDictionary(self, dictionary,fn):
        
        self.file_opt['initialfile'] = fn
        save_loc = tkFileDialog.asksaveasfilename(**self.file_opt)
        
          
        sio.savemat(save_loc, dictionary)

if __name__ == "__main__":
    X=2
    Y=5
    A = {"X": X, "Y": Y}
    x = DictionarySaver()
    x.saveDictionary(A,"test")