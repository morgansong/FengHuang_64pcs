from smbus2 import SMBus,i2c_msg
import time 
import RPi.GPIO as GPIO


#read 64bytes data from address 80
#msg = i2c_msg.read(80, 64) 
#bus.i2c_rdwr(msg)


#write some bytes to address 80
#msg = i2c_msg.write(80, [51,23,54])
#bus.i2c_rdwr(msg)


bus = SMBus(1)  # 0=/dev/i2c-0(port I2C0), 1=/dev/i2c-1(port I2C1)


print("setup GPIO")
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# print("set low")
GPIO.output(18, GPIO.LOW)
time.sleep(0.1)

# print("set high")
GPIO.output(18, GPIO.HIGH)

print("cleanup")
GPIO.cleanup()


address = 0x70

def write_data(value):
    global address
    # print(address)
    msg = i2c_msg.write(address, value)
    bus.i2c_rdwr(msg)


def read_numbers_bytes(num):
    global address
    msg = i2c_msg.read(address, num)
    bus.i2c_rdwr(msg)

    data = list(msg) 
    return data
 

def SCD4x_SN_Read(): 
    write_data([0x36,0x82])
    
    time.sleep(0.001)
    Data_Get = read_numbers_bytes(9)
    
    return str(Data_Get[0])+str(Data_Get[1])+str(Data_Get[3])+str(Data_Get[4])+str(Data_Get[6])+str(Data_Get[7])



write_data([0x04])


time.sleep(1)


address = 0x62 


 

try:
    write_data([0x3f,0x86])
    time.sleep(1)
except:
    print("SCD40 already stops period measurement")
 
print(SCD4x_SN_Read())





try:
    write_data([0x21,0xb1])
except:
    print("SCD40 already starts period measurement")
    

while True: 
    time.sleep(5)
    
    try: 
        write_data([0xec,0x05])
        
        # time.sleep(0.01)
        Data_Get = read_numbers_bytes(9)
        
        co2 = int(hex(Data_Get[0]<<8),16)+int(hex(Data_Get[1]),16)
        temp =  -45 + 175.0*(int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16))/65536.0
        humi = 100*(int(hex(Data_Get[6]<<8),16)+int(hex(Data_Get[7]),16))/65536.0
        
        
        print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),"SCD40 CO2: {}, temperature: {}, humidity: {}".format(round(co2,2),round(temp,2),round(humi,2)))
        

    except Exception as e: 
        print(e)
        pass



