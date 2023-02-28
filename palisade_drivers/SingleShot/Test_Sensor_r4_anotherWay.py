import time
import Singleshot_dart_WZS
import Singleshot_cubic_CB


port_list = ["/dev/device2", "/dev/device3","/dev/device4", "/dev/device5"]


DeviceName_list = []
UART_list = []
num_device = 0


#start Measurement
for k in range(len(port_list)):
    print(port_list[k])
    try:
        dart = Singleshot_dart_WZS.dart_WZS(port_list[k])
        
        Check = False
        for i in range(3):
            time.sleep(2)
            read = dart.get_new_measurements()
            print('read:',read)
            if read:
                Check = True
                break
            else:
                Check = False
                
        print('Check1:',Check)
        if Check:
            print("has found dart at ",port_list[k])
            num_device = num_device + 1
            DeviceName_list.append('dart')
            UART_list.append(dart)
        else:
            dart.close()
            
            cubic = Singleshot_cubic_CB.CubicCBHCHO(port_list[k])
            
            Check = False
            for i in range(3):
                time.sleep(2)
                read = cubic.get_new_measurements()
                print('read:',read)
                if read:
                    Check = True
                    break
                else:
                    Check = False
                    
            print('Check2:',Check)
            if Check:
                print("has found cubic at ",port_list[k])
                num_device = num_device + 1
                DeviceName_list.append('cubic')
                UART_list.append(cubic)
                
    except Exception as e:
        print(e)
        print(port_list[k], " has no device")



time.sleep(2)
print(UART_list)
print(DeviceName_list)
print(num_device)




while True:
    data = {}
    
    time.sleep(2)
    
    for i in range(len(UART_list)):
        try:
            result_dict = UART_list[i].get_new_measurements()
            
            # print(result_dict)
            
            if DeviceName_list[i] == 'dart':
                if result_dict:
                    data['dart'] = [result_dict[1][1]]
                    
            if DeviceName_list[i] == 'cubic':
                if result_dict:
                    data['cubic'] = [result_dict[0][1],result_dict[4][1],result_dict[3][1]]
        except Exception as e:
            print(e)
            
        if len(data)==num_device:
            print(data)
            