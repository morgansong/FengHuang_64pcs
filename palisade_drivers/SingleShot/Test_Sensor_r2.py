import time
import Singleshot_dart_WZS
import Singleshot_cubic_CB




dart_list = ["/dev/device3", "/dev/device5"]
cb_list = ["/dev/device2", "/dev/device4"]


dart = []
cubic = []

num_device = 0 

#start Measurement
try:
    dart.append(Singleshot_dart_WZS.dart_WZS(dart_list[0]))
    num_device = num_device + 1
    print("found: ", dart_list[0])
except:
    pass

try:
    dart.append(Singleshot_dart_WZS.dart_WZS(dart_list[1]))
    num_device = num_device + 1
    print("found: ", dart_list[1])
except:
    pass

try:
    cubic.append(Singleshot_cubic_CB.CubicCBHCHO(cb_list[0]))
    num_device = num_device + 1
    print("found: ", cb_list[0])
except:
    pass

try:
    cubic.append(Singleshot_cubic_CB.CubicCBHCHO(cb_list[1]))
    num_device = num_device + 1
    print("found: ", cb_list[1])
except:
    pass


while True:
    data = {}
    
    try:
        time.sleep(2)
        try: 
            result_dict_d = dart[0].get_new_measurements()
            if result_dict_d:
                data['dart'] = [result_dict_d[1][1]]
        except:
            pass
            
        try: 
            result_dict_d = dart[1].get_new_measurements()
            if result_dict_d:
                data['dart'] = [result_dict_d[1][1]]
        except:
            pass
            
        try:
            result_dict_c = cubic[0].get_new_measurements()
            if result_dict_c:
                # print(result_dict_c)
                
                data['cubic'] = [result_dict_c[0][1],result_dict_c[4][1],result_dict_c[3][1]]
        except:
            pass
            
        try:
            result_dict_c = cubic[1].get_new_measurements()
            if result_dict_c:
                # print(result_dict_c)
                
                data['cubic'] = [result_dict_c[0][1],result_dict_c[4][1],result_dict_c[3][1]]
        except:
            pass
            
        if len(data)==num_device:
            print(data)
        
    except KeyboardInterrupt:
        time.sleep(0.1)
        dart.close()
        cubic.close()
