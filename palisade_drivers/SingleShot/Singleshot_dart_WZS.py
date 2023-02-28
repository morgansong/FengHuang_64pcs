import serial
import struct


class dart_WZS:
    def __init__(self, com_port):
        self.ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)# Strict timing needed
        
        self.switch_to_pulling_mode()
        
    def switch_to_pulling_mode(self):
        send_data = struct.pack('<9B', 0xFF, 0x01, 0x78, 0x41, 0x00, 0x00, 0x00, 0x00, 0x46)
        self.ser.write(send_data)
        
    def read_gas_concentration(self):
        send_data = struct.pack('<9B', 0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79)
        self.ser.write(send_data)
        
    def receive_packet(self, payload_length=None):
        if payload_length:
            read_size = payload_length
        else:
            read_size = 9
        read_data = self.ser.read(size=read_size)
        data = list(read_data)
        return data
        
    def get_new_measurements(self):
        self.read_gas_concentration()
        data = self.receive_packet()
        try:
            data = struct.unpack('>BBHHHB', bytearray(data))
            if data[1] == 0x86:  # is HCHO
                return [('C_HCHO_(mg/m3)', data[2]/1000.0), ('C_HCHO_(ppb)', data[4])]
        except:
            print('No new dart HCHO value data')
            return None
            
            
    def close(self):
        print('serial is closed')
        self.ser.close()




