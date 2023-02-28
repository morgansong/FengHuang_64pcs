import serial
import struct



class CubicCBHCHO:

    STATUS_LIST = ['OK', 'Sensor anomaly', 'High alcohol env', 'High HCHO env',
                   'Unknown error', 'Unknown error', 'Unknown error', 'Unknown error']

    def __init__(self, com_port):
        self.ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)      # Strict timing needed

    def get_measurement_value(self):
        send_data = struct.pack('<BBBB', 0x11, 0x01, 0x01, 0xed)

        self.ser.write(send_data)

    def receive_packet(self, payload_length=None):
        if payload_length:
            read_size = payload_length
        else:
            read_size = 16
        read_data = self.ser.read(size=read_size)
        # logging.debug('Recieved {} bytes {}'.format(len(read_data), read_data.hex()))
        data = list(read_data)
        return data

    def get_new_measurements(self):
        self.get_measurement_value()
        data = self.receive_packet() 
        try:
            data = struct.unpack('>HBHHHHHBBB', bytearray(data))
            if data[0] == 0x160d:  # is HCHO
                return ([('C_HCHO_(ppb)', data[2]),
                        ('C_VOC_(ppm)', data[3] / 1000.0),
                        ('C_TVOC_(ppm)', data[6] / 1000.0),
                        ('T_(C)', data[4]/10.0),
                        ('RH_(%)', data[5]/10.0),
                        ('Status', self.STATUS_LIST[data[7]]),
                        ])
        except:
            print('No new cubic HCHO value data')
            return None



    def close(self):
        print('serial is closed')
        self.ser.close()

