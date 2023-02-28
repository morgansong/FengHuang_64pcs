#!/usr/bin/env python3
__author__ = 'uschoen'
__version__ = '1.0.0'

import serial
import struct
import os
from datalogging import DataLogger
import logging
from collections import OrderedDict
import sys
import time



def create_datalogger(hardware_name, sensor_id):
    header_meta = {
        # 'Product': hardware_name,
        'Hardware': hardware_name,
        'SensorId': sensor_id
    }

    filename = os.path.join(os.getcwd(), 'Data', hardware_name+'_' + str(sensor_id),  '_' + str(sensor_id) + ".edf")
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass
    timefmt = '%Y%m%dT%H%M%SZ'
    rollover = {'when': 'midnight'}
    datalogger = DataLogger(filename,
                            header=header_meta,
                            columnmeta={
                                'Epoch_UTC': {'Source': 'StopWatch', 'SourceType': 'ActualValue', 'Unit': 's'},
                                # 'T': {'Source': 'SHT', 'SourceType': 'ActualValue', 'Unit': 'C'},
                                # 'C': {'Source': 'SHT', 'SourceType': 'ActualValue', 'Unit': 'ticks'},
                            },
                            time_fmt=timefmt,  # format string for the time information in the filename
                            filename_fmt="{time}_{fname}{ext}",
                            strip_time=False,
                            utc=True,
                            **rollover)
    return datalogger


def setup_arg_parser():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", dest="port", default='Com0',
                        help="Port on which Serial is connected ", metavar="PORT")
    args = parser.parse_args()
    return args


class ECSense_TB600B:

    def __init__(self, com_port):
        self.ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)      # Strict timing needed

        self.switch_to_pulling_mode()

    def switch_to_pulling_mode(self):
        send_data = struct.pack('<9B', 0xFF, 0x01, 0x78, 0x41, 0x00, 0x00, 0x00, 0x00, 0x46)
        if sys.version_info[0] > 2:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data.hex()))
        else:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data))

        self.ser.write(send_data)

    def read_gas_concentration(self):
        send_data = struct.pack('<9B', 0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79)
        if sys.version_info[0] > 2:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data.hex()))
        else:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data))

        self.ser.write(send_data)

    def receive_packet(self, payload_length=None):
        if payload_length:
            read_size = payload_length
        else:
            read_size = 9
        read_data = self.ser.read(size=read_size)
        # logging.debug('Recieved {} bytes {}'.format(len(read_data), read_data.hex()))
        data = list(read_data)

        if sys.version_info[0] > 2:
            logging.debug('Recieved {} bytes {}'.format(len(data), '[{}]'.format(', '.join(hex(x) for x in data))))
        else:
            logging.debug('Recieved {} bytes {}'.format(len(data), '[{}]'.format(', '.join(hex(ord(x)) for x in data))))

        return data

    def get_new_measurements(self):
        self.read_gas_concentration()
        data = self.receive_packet()

        try:
            data = struct.unpack('>BBHHHB', bytearray(data))
            if data[1] == 0x86:  # is HCHO
                return OrderedDict([('Epoch_UTC', time.time()), ('C_HCHO_(mg/m3)', data[2]/1000.0), ('C_HCHO_(ppb)', data[4])])
        except:
            logging.error('No new HCHO value data')
            return None

    def close(self):
        logging.error('Close serial connection to Dart sensor')
        self.ser.close()


def main(argv):
    # configure logging handler
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    args = setup_arg_parser()
    port = args.port

    # setup new sensor and logger
    sensor = ECSense_TB600B(port)
    logger = create_datalogger(hardware_name="EC Sense TB-600B", sensor_id=port)

    try:
        while True:
            time.sleep(2)
            result_dict = sensor.get_new_measurements()
            if result_dict:
                logger.log(result_dict)
            print(result_dict)
    except KeyboardInterrupt:
        time.sleep(0.1)
        sensor.close()


if __name__ == '__main__':
    main(sys.argv[1:])
