import time
import Singleshot_dart_WZS
import Singleshot_cubic_CB


port_list = ["/dev/device2", "/dev/device3","/dev/device4", "/dev/device5"]


DeviceName_list = []
UART_list = []
num_device = 0


#start Measurement
for k in range(len(port_list)):
    try:
        cubic = Singleshot_cubic_CB.CubicCBHCHO(port_list[k])
        num_device = num_device + 1
        
        print("has found cubic at ",port_list[k])
        DeviceName_list.append('cubic')
        UART_list.append(cubic)
        print(UART_list)
            
    except Exception as e:
        print(e,' and continue')
        try:
            dart = Singleshot_dart_WZS.dart_WZS(port_list[k])
            num_device = num_device + 1
            
            print("has found dart at ",port_list[k])
            DeviceName_list.append('dart')
            UART_list.append(dart)
            print(UART_list)
        
        except Exception as e:
            print(e)
            print(port_list[k], " has no device")

time.sleep(2)


print(DeviceName_list)

while True:
    data = {}
    print('run')
    
    time.sleep(2)
    
    for i in range(len(UART_list)):
        try:
            result_dict_d = UART_list[i].get_new_measurements()
            
            print(result_dict_d)
            
            if DeviceName_list[i] == 'dart':
                if result_dict_d:
                    data['dart'] = [result_dict_d[1][1]]
                    
            if DeviceName_list[i] == 'cubic':
                if result_dict_d:
                    data['cubic'] = [result_dict_c[0][1],result_dict_c[4][1],result_dict_c[3][1]]
        except:
            pass
            
        if len(data)==num_device:
            print(data)
    