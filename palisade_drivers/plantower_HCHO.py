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


class PlantowerHCHO:

    def __init__(self, com_port):
        self.ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)      # Strict timing needed

    def get_measurement_value(self):
        send_data = struct.pack('<BBBBBBB', 0x42, 0x4d, 0x01, 0x00, 0x00, 0x00, 0x90)
        if sys.version_info[0] > 2:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data.hex()))
        else:
            logging.debug('Send {} bytes {}'.format(len(send_data), send_data))

        self.ser.write(send_data)

    def receive_packet(self, payload_length=None):
        if payload_length:
            read_size = payload_length
        else:
            read_size = 10
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
            data = struct.unpack('>BBBBBBHH', bytearray(data))
            if data[3] == 0x14:  # is HCHO
                divisor = float(10 ** (data[5] - 1))
                value = data[6] / divisor
                return OrderedDict([('Epoch_UTC', time.time()), ('C_HCHO_(mg/m3)', value)])
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
    sensor = PlantowerHCHO(port)
    logger = create_datalogger(hardware_name="Plantower DS-HCHO", sensor_id=port)

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
