#!/usr/bin/env python3
__author__ = 'uschoen'
__version__ = '1.0.0'


import serial   # pip install pyserial
import struct
import os
import logging
from collections import OrderedDict
import sys
import time


from datalogging import DataLogger   # pip install sensirion-datalogging


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


class CubicCBHCHO:

    STATUS_LIST = ['OK', 'Sensor anomaly', 'High alcohol env', 'High HCHO env',
                   'Unknown error', 'Unknown error', 'Unknown error', 'Unknown error']

    def __init__(self, com_port):
        self.ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)      # Strict timing needed

    def get_measurement_value(self):
        send_data = struct.pack('<BBBB', 0x11, 0x01, 0x01, 0xed)
        if sys.version_info[0] > 2:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data.hex()))
        else:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data))

        self.ser.write(send_data)

    def receive_packet(self, payload_length=None):
        if payload_length:
            read_size = payload_length
        else:
            read_size = 16
        read_data = self.ser.read(size=read_size)
        # logging.debug('Recieved {} bytes {}'.format(len(read_data), read_data.hex()))
        data = list(read_data)

        if sys.version_info[0] > 2:
            logging.debug('Recieved {} bytes {}'.format(len(data), '[{}]'.format(', '.join(hex(x) for x in data))))
        else:
            logging.debug('Recieved {} bytes {}'.format(len(data), '[{}]'.format(', '.join(hex(ord(x)) for x in data))))

        return data

    def get_new_measurements(self):
        self.get_measurement_value()
        data = self.receive_packet()

        try:
            data = struct.unpack('>HBHHHHHBBB', bytearray(data))
            if data[0] == 0x160d:  # is HCHO
                return OrderedDict([('Epoch_UTC', time.time()),
                                    ('C_HCHO_(ppm)', data[2] / 1000.0),
                                    ('C_VOC_(ppm)', data[3] / 1000.0),
                                    ('C_TVOC_(ppm)', data[6] / 1000.0),
                                    ('T_(C)', data[4]/10.0),
                                    ('RH_(%)', data[5]/10.0),
                                    ('Status', self.STATUS_LIST[data[7]]),
                                    ])
        except:
            logging.error('No new HCHO value data')
            return None



    def close(self):
        logging.error('Close serial connection to Plantower sensor')
        self.ser.close()


def main(argv):
    # configure logging handler
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    args = setup_arg_parser()
    port = args.port


    # setup new sensor and logger
    sensor = CubicCBHCHO(port)
    logger = create_datalogger(hardware_name="Cubic CB-HCHO", sensor_id=port)

    # give the sensor time to start up
    time.sleep(0.2)

    try:
        while True:
            time.sleep(2)
            result_dict = sensor.get_new_measurements()
            if result_dict:
                logger.log(result_dict)
            print(result_dict)
    except KeyboardInterrupt:
        # sensor.stop_measurement()
        time.sleep(0.1)
        sensor.close()


if __name__ == '__main__':
    main(sys.argv[1:])
