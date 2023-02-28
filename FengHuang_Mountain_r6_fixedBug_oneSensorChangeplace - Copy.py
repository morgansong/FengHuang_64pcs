#!/usr/bin/python 
#coding: utf-8
from Driver_Sensors import SFA3x, I2C_Handler 
import RPi.GPIO as GPIO
from tkinter import *
import numpy as np
import datetime
import threading
import time
import os




print("setup GPIO")
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)



##Global parameters defination
data_raw_64 = ['n.c']*64  # the value of the output of all ports, in case there is no 64 data for example 1 sensor is not connected 
data_location = [] # record all the location where is data
color_64 = ["green"]*64  # the value of all 64pcs units
string_64 = [] #list of all 64pcs StringVar()
label_64 = [] #list of all 64pcs labels
label_64_up = [] #list of all 64pcs labels
label_64_down = [] #list of all 64pcs labels




class ReadMeasurement_SFA3x():
    def __init__(self):
        self.address_TCA9548 = [0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77]
        # self.address_TCA9548 = [0x77]
        self.My_Handler = I2C_Handler.I2C_Handler()
        
        self.SFA3x_handler = SFA3x.SFA3x() 
        
        self.now = datetime.datetime.now()
        self.filename = r'/home/pi/DataLog/Fenghuang_{}_{}_{}_{}_{}_{}.edf'.format(self.now.year, str(self.now.month).zfill(2),str(self.now.day).zfill(2),str(self.now.hour).zfill(2),str(self.now.minute).zfill(2),str(self.now.second).zfill(2))
        
        try: 
            os.mkdir(r"/home/pi/DataLog")
        except Exception as e:
            print("build Failed: ", e)
            
        self.Start_Measurement()
            
    def Start_Measurement(self):
        ##start the measurement for all sensors
        for address in self.address_TCA9548:
            for channel in range(8):
                
                ## try-except is nessary for there is missing  TCA9845
                try: 
                    self.OpenChannel_TCA9548(address, channel)
                    print(address, channel)
                    time.sleep(0.1)
                except Exception as e: 
                    # print("write channel error")
                    # print(e) 
                    pass
                
                # self.SFA3x_handler.SFA3x_start_continuous_measurement()
                # print('SFA3x_start_continuous_measurement')
                # time.sleep(0.01)
                try:
                    self.SFA3x_handler.SFA3x_stop_continuous_measurement()
                    time.sleep(0.1) #delay >500ms 
                    self.SFA3x_handler.SFA3x_start_continuous_measurement()
                    time.sleep(0.1)
                    print('SFA3x_start_continuous_measurement')
                except: 
                    try: 
                        self.SFA3x_handler.SFA3x_start_continuous_measurement()
                        print('SFA3x_start_continuous_measurement')
                    except:
                        pass
                        
    def UpdateValues(self):
        global data_raw_64,data_location
        
        data_raw_64 = [] 
        data_location = []
        
        for kk, address in enumerate(self.address_TCA9548): 
            for channel in range(8):
                # print(address, channel)
                
                ## try-except is nessary for there is missing  TCA9845
                try: 
                    self.OpenChannel_TCA9548(address, channel)
                    time.sleep(0.1)
                except Exception as e: 
                    # print("write channel error")
                    # print(e) 
                    pass
                
                
                try: 
                    read = self.SFA3x_handler.SFA3x_ReadMeasurement()
                    # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()), read)
                    
                    if len(read)==3:
                        data_raw_64.append(round(read[0],1)) #first data is HCHO
                        data_location.append(kk*8+channel) #remember the location where has data
                except:
                    pass
                    
        # print('data_raw_64, data_location', data_raw_64, data_location)
                    
    def OpenChannel_TCA9548(self, address, channel):
        # print("set low")
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.01)
        
        # print("set high")
        GPIO.output(18, GPIO.HIGH)
        
        # print("cleanup")
        # GPIO.cleanup()
        
        # time.sleep(1.0)
        
        if (channel == 0):
            action = 0x01
        elif (channel == 1):
            action = 0x02
        elif (channel == 2):
            action = 0x04
        elif (channel == 3):
            action = 0x08
        elif (channel == 4):
            action = 0x10
        elif (channel == 5):
            action = 0x20
        elif (channel == 6):
            action = 0x40
        elif (channel == 7):
            action = 0x80
        else:
            action = 0x00
        
        self.My_Handler.write_data(address, [action]) #[] is essential
        
        
        
        
class GUI_DataShow():
    def __init__(self):
        
        self.ThreadingExample()
        
    def Datachange(self):
        
        S = ReadMeasurement_SFA3x()
        
        while True:
            
            S.Start_Measurement()
            S.UpdateValues()
            
            print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),'data_raw_64, data_location', data_raw_64, data_location)
            
            time.sleep(0.1)
            
            # print(len(string_64),len(label_64_up),len(label_64),len(label_64_down))
            # string_64[35].set(100.2) #test label length - window twisted
            
            ##change the text display
            
            for kk in range(len(label_64)):
                label_64[kk].configure(bg='white')
                string_64[kk].set('n.c')
                
                for i in range(len(data_location)):
                    if kk == data_location[i]:
                        string_64[kk].set(data_raw_64[i])  
            
            ##Change color display
            ##red = data is beyond +/-20% of mean
            middian = np.mean(data_raw_64)
            
            if len(data_location)>0: #avoid no any sensor connected
                for i in range(len(data_raw_64)):
                    # print(data_location[i])
                    
                    if data_raw_64[i]>middian*1.2 or data_raw_64[i] <middian*0.8:
                        print(round(middian*0.8,1),'---', round(middian*1.2,1),'---', data_raw_64[i])
                        
                        # label_64_up[data_location[i]].configure(bg='red')
                        label_64[data_location[i]].configure(bg='red')
                        # label_64_down[data_location[i]].configure(bg='red')
                    else:  
                        # label_64_up[data_location[i]].configure(bg='green')
                        label_64[data_location[i]].configure(bg='lime')
                        # label_64_down[data_location[i]].configure(bg='green')
            # print('Change is done')
                
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
        Label(frame_64[i], text=" #0{}  ".format(i+1), bg='gray', relief='ridge').pack(fill='both', expand=True) #the blank is to freeze the GUI
    else:
        Label(frame_64[i], text=" #{}  ".format(i+1), bg='gray', relief='ridge').pack(fill='both', expand=True)
    
    # l1 = Label(frame_64[i], bg='green')
    # l1.pack(fill='both', expand=True) #just for UI
    
    my_string_var = StringVar()
    my_string_var.set(data_raw_64[i])
    l = Label(frame_64[i], textvariable= my_string_var,font=(30), relief='ridge', bg='white') #display of values
    l.pack(fill='both', expand=True)
    
    # l2 = Label(frame_64[i], bg='green')
    # l2.pack(fill='both', expand=True) #just for UI
    
    string_64.append(my_string_var)
    # label_64_up.append(l1)
    label_64.append(l)
    # label_64_down.append(l2)
    
##Reading and update the value
GUI_DataShow()


root.mainloop()



##Test sensor without GUI interface
# S = ReadMeasurement_SFA3x()

# while True: 
    # time.sleep(1)
    # S.UpdateValues()
    # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),str(data_raw_64).replace("[","").replace("]",""))



