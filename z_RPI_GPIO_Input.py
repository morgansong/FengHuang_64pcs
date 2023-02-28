import RPi.GPIO as GPIO
import time




pinReset = 21 #pin40 - BCM21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pinReset, GPIO.IN)


print('soft started: ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('connect pin40 to GND')
# print('connect pin40 to 3.3v')


print('scripter is running')


while True:
    input_value = GPIO.input(pinReset)
    
    # if input_value==0:
    
    if input_value==1: 
        print(str(input_value))
        print('i got you')
    
    time.sleep(1)









