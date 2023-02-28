#!/usr/bin/python 
#coding: utf-8
# import RPi.GPIO as GPIO
import datetime
from Driver_Sensors import SFA30, I2C_Handler 
import time
import datetime
import serial
import numpy as np
import os
from tkinter import *
from tkinter import messagebox , filedialog
import threading


##Global parameters defination
data_64 = [0]*64  # the value of all 64pcs units
color_64 = ["green"]*64  # the value of all 64pcs units
string_64 = [] #list of all 64pcs StringVar()
label_64 = [] #list of all 64pcs labels




class ReadValue_SFA30s():
    def __init__(self):
        #initialing the sensor
        pass
        
        
        
        
class GUI_DataShow():
    def __init__(self):
        pass
        
    def Datachange(self):
        for i in range(len(string_64)):
            string_64[i].set( "port {}\n".format(i+1)+ str(data_64[i]))
        
        
        
        
class Windows_GUI():
    def __init__(self): 
        self.i = 0
        
        self.ThreadingExample()
        
    def run(self): 
        root = Tk()
        root.attributes('-fullscreen', True)
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
                my_string_var.set(8*j+i)
                
                l = Label(frameList[j], textvariable= my_string_var, bg='green',font=("微软雅黑", 10))
                
                l.pack(side='left',fill='both', expand=True)
                
                string_64.append(my_string_var)
                label_64.append(l)
                
        root.mainloop()
        
    def ThreadingExample(self):
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True
            thread.start()

##Running the GUI interface
Windows_GUI()



##Reading and update the value
R = GUI_DataShow()


i = 0 
while True: 
    
    time.sleep(1)
    
    if i%64 > 1: 
        label_64[i%64 -1 ].configure(bg='green',font=("微软雅黑", 10))
    else: 
        label_64[0].configure(bg='green',font=("微软雅黑", 10))
        label_64[63].configure(bg='green',font=("微软雅黑", 10))
        
        
    R.Datachange()
    
    
    label_64[i%64].configure(bg='red',font=("微软雅黑", 10,'bold'))
    
    data_64 = [i]*64
    
    i = i + 1


























