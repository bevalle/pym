# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:24:58 2017

@author: valle
"""

import tkFileDialog # boite de dialogue pour recherche dossier
import os
import numpy as np
import cv2
import glob # recherche images
import shutil
from Tkinter import *
import csv


execfile("PYM.py")

# Prompt directory 
root = Tk()
root.withdraw()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Select directory:')

# Define include_holes value according to method  
  
include_holes = 1 # highest area (lettuce in field)
include_holes = 0 # counting white pixels (other cases)

PYM_folder(dirname, include_holes)
