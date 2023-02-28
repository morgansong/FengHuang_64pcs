#!/usr/bin/python 
#coding: utf-8
# import RPi.GPIO as GPIO
import datetime
from Driver_Sensors import SFA3x, I2C_Handler 
import time
import datetime
import serial
import numpy as np
import os
from tkinter import *
from tkinter import messagebox , filedialog


##Global parameters defination
data_64 = [0]*64  # the value of all 64pcs units
color_64 = ["green"]*64  # the value of all 64pcs units
label_64 = [] #list of all 64pcs label




class ReadValue_SFA30s():
    def __init__(self):
        #initialing the sensor
        pass



class GUI_DataShow():
    def __init__(self):
        root = Tk()
        root.attributes('-fullscreen', True)
        # root.attributes("-topmost",True)
        
        # root.title("Tool Fenghuang")
        # w = width_1
        # h = length_1
        # x = 0
        # y = 0
        # root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        
        root.overrideredirect(True)  # 去除窗口边框
        
        frameList = []
        ##put 8 raw colomn
        for i in range(8):
            frame = Frame(root, relief='groove',bg='green')
            frame.pack(fill='both', expand=True)
            
            frameList.append(frame)
            
        
        for j in range(len(frameList)):
            for i in range(8):
                my_string_var = StringVar()
                my_string_var.set(8*i+j)
                
                l = Label(frameList[j], textvariable= my_string_var, bg='green')
                
                l.pack(side='left',fill='both', expand=True)
                
                label_64.append(my_string_var)
                
        root.mainloop()
        
    def Datachange(self):
        label_64[0].set( "This is test")
        print('done')
        
        
        
        
        
        
        

R = GUI_DataShow()

for i in range(3):
    print(i)
    time.sleep(1)
    R.Datachange()

# while True: 
    # time.sleep(1)
    
    # R.Datachange()


























