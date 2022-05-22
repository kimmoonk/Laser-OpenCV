# UART Tx/Rx demo
import tkinter as tk
from tkinter import ttk
from turtle import delay

from tkinter import filedialog

import serial
import threading

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np

from PathCodeMaker import *

import cv2
from PIL import Image
import matplotlib.pyplot as plt
import multiprocessing
from PIL import Image, ImageTk
        
import customtkinter

memo = open("code.txt", 'w')

bezier_x = [10.0,10.0,60.0,60.0]
bezier_y = [10.0,60.0,60.0,10.0]
BezierPos_X = []
BezierPos_Y = []
t_count = 0
step = 0.1
t_points = np.arange(0, 1 + step, step)

sentence = ("L" + 
        "X" + str(round(bezier_x[0], 1)).zfill(4) +
        "Y" + str(round(bezier_y[0], 1)).zfill(4) + "\n")
memo.write(sentence)   
memo.write("S1000\n")


for t in t_points:
    BezierPos_X.append(pow(1 - t, 3) * bezier_x[0]
    + 3 * t * pow(1 - t, 2) * bezier_x[1]
    + 3 * pow(t, 2) * (1 - t) * bezier_x[2]
    + pow(t, 3) * bezier_x[3]);
    
    BezierPos_Y.append(pow(1 - t, 3) * bezier_y[0]
    + 3 * t * pow(1 - t, 2) * bezier_y[1]
    + 3 * pow(t, 2) * (1 - t) * bezier_y[2]
    + pow(t, 3) * bezier_y[3]);
    
    sentence = ("L" + 
            "X" + str(round(BezierPos_X[t_count], 1)).zfill(4) +
            "Y" + str(round(BezierPos_Y[t_count], 1)).zfill(4) + "\n")
    memo.write(sentence)    
    print (sentence)

        
    t_count += 1

# sentence = ("L" + 
#         "X" + str(round(BezierPos_X[t_count], 1)).zfill(4) +
#         "Y" + str(round(BezierPos_X[t_count], 1)).zfill(4) + "\n")
# memo.write(sentence)    
# print (sentence)
    
memo.write("S0\n")
memo.write("Z")
    
# sentence = ("L" + 
#             "X" + str(round(curve.start_point.x, 1)).zfill(4) +
#             "Y" + str(round(curve.start_point.y, 1)).zfill(4) + "\n")

#memo.write(sentence)    
#memo.write("S1000\n")