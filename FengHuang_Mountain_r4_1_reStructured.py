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
import threading


##Global parameters defination
data_64 = [0]*64  # the value of all 64pcs units
color_64 = ["green"]*64  # the value of all 64pcs units
string_64 = [] #list of all 64pcs StringVar()
label_64 = [] #list of all 64pcs labels
label_64_up = [] #list of all 64pcs labels
label_64_down = [] #list of all 64pcs labels






class ReadValue_SFA30s():
    def __init__(self):
        global data_64
        #initialing the sensor
        import random
        data = [] 
        for i in range(64):
            data.append(random.randint(10,15))
            
        data_64 = data
        
        
        
        
class GUI_DataShow():
    def __init__(self):
        
        self.ThreadingExample()
        
    def Datachange(self):
        while True: 
            ReadValue_SFA30s()
            # print(data_64)
            
            time.sleep(1)
            
            for i in range(len(string_64)):
                string_64[i].set(data_64[i])
            
            # print(data_64)
            
            ##Color Indication
            ##red = data is beyond +/-20% of mean
            middian = np.mean(data_64)
            
            if len(label_64)==64:
                for i in range(len(data_64)):
                    if data_64[i]>middian*1.2 or data_64[i] <middian*0.8:
                        print(round(middian*0.8,1),'---', round(middian*1.2,1),'---', data_64[i])
                        
                        label_64_up[i].configure(bg='red')
                        label_64[i].configure(bg='red')
                        label_64_down[i].configure(bg='red')
                    else:  
                        label_64_up[i].configure(bg='green')
                        label_64[i].configure(bg='green')
                        label_64_down[i].configure(bg='green')
                
    def ThreadingExample(self):
            # print("thread starts")
            thread = threading.Thread(target=self.Datachange, args=())
            thread.daemon = True
            thread.start()
            
            
            
            
root = Tk()
root.attributes('-fullscreen', True)
# root.overrideredirect(True)  # 去除窗口边框

frameList_Row = []
frame_64 = []
##put 8 raw row
for i in range(8):
    frame = Frame(root)
    frame.pack(fill='both', expand=True)
    
    frameList_Row.append(frame)

##put 8 frame in each row
for j in range(len(frameList_Row)):
    for i in range(8):
        f = Frame(frameList_Row[j])
            
        f.pack(side='left',fill='both', expand=True)
        
        frame_64.append(f)
        
for i in range(len(frame_64)):
    if len(str(i+1))==1:
        Label(frame_64[i], text="#0{}".format(i+1), bg='lime', relief='ridge').pack(fill='both', expand=True)
    else: 
        Label(frame_64[i], text="#{}".format(i+1), bg='gray', relief='ridge').pack(fill='both', expand=True)
    
    l1 = Label(frame_64[i], bg='green')
    l1.pack(fill='both', expand=True) #just for UI
    
    my_string_var = StringVar()
    my_string_var.set(data_64[i])
    l = Label(frame_64[i], textvariable= my_string_var, bg='green',font=(15)) #display of values
    l.pack(fill='both', expand=True)
    
    l2 = Label(frame_64[i], bg='green')
    l2.pack(fill='both', expand=True) #just for UI
    
    string_64.append(my_string_var)
    label_64_up.append(l1)
    label_64.append(l)
    label_64_down.append(l2)
    
    
##Reading and update the value
GUI_DataShow()
    
root.mainloop()




