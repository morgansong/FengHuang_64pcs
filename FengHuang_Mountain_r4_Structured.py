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
        pass
        
    def Datachange(self):
        # print(data_64)
        for i in range(len(string_64)):
            string_64[i].set(data_64[i])
        
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
                
        
        
class Windows_GUI():
    def __init__(self): 
        self.i = 0
        
        self.ThreadingExample()
        
    def run(self): 
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
                Label(frame_64[i], text="#0{}".format(i+1), bg='RoyalBlue', relief='ridge').pack(fill='both', expand=True)
            else: 
                Label(frame_64[i], text="#{}".format(i+1), bg='RoyalBlue', relief='ridge').pack(fill='both', expand=True)
            
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
    print(i)
    ReadValue_SFA30s()
    time.sleep(1)
    R.Datachange()
    i = i +1




# i = 0
# while True: 
    
    # time.sleep(1)
    
    # if i%64 > 1: 
        # label_64_up[i%64 -1 ].configure(bg='green')
        # label_64[i%64 -1 ].configure(bg='green')
        # label_64_down[i%64 -1 ].configure(bg='green')
    # else: 
        # label_64_up[0].configure(bg='green')
        # label_64[0].configure(bg='green')
        # label_64_down[0].configure(bg='green')
        
        # label_64_up[63].configure(bg='green')
        # label_64[63].configure(bg='green')
        # label_64_down[63].configure(bg='green')
        
     
    
    
    # label_64_up[i%64].configure(bg='red')
    # label_64[i%64].configure(bg='red')
    # label_64_down[i%64].configure(bg='red')
    
    # data_64 = [i]*64 #change the data
    # R.Datachange() #display the changes
    
    # i = i + 1


























