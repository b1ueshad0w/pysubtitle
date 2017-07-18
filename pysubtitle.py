#!/usr/bin/env python
# coding=utf-8

""" pysubtitle.py: This script helps you to adjust the subtitle file
to get synchronous with the movie.

Created by gogleyin on 26/12/2016.
"""

import os
import re
import logging
import argparse
from datetime import datetime, timedelta


logging.basicConfig(level=logging.DEBUG)

TIME_FORMAT = '%H:%M:%S.%f'


def process(file_path, new_file_path, seconds, increase=True, time_format=TIME_FORMAT):
    moment_pattern = '\d+:\d+:\d+\.\d+'
    if not os.path.isfile(file_path):
        logging.error('File not exist: %s' % file_path)
        return
    with open(file_path) as inputFile, open(new_file_path, 'w') as outputFile:
        content = inputFile.read()
        # print content
        matches = re.findall(moment_pattern, content)
        if not matches:
            logging.info('Could not find moment pattern in file content.')
            return
        for match in matches:
            new_time = modify_time_string(match, seconds, increase=increase, time_format=time_format)
            content = content.replace(match, new_time)
        outputFile.write(content)


def modify_time_string(str_time, seconds, time_format=TIME_FORMAT, increase=True):
    some_time = datetime.strptime(str_time, time_format)
    if increase:
        new_time = some_time + timedelta(seconds=seconds)
    else:
        new_time = some_time - timedelta(seconds=seconds)
    new_str_time = new_time.strftime(time_format)

    # '00:01:01:01.100000' ==> '0:01:01:01.10'
    new_str_time = new_str_time.replace('0000', '')
    if new_str_time.startswith('00:'):
        new_str_time = new_str_time[1:]
    return new_str_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', dest='input_file', required=True,
                        help='Path of the subtitle file to modify')
    parser.add_argument('-o', '--output_file', dest='output_file', required=True,
                        help='Path of the output subtitle file')
    parser.add_argument('-s', '--seconds', dest='seconds', required=True, type=int,
                        help='Count of seconds to increase/decrease the subtitle\'s delay.')
    parser.add_argument('-d', '--decrease', dest='decrease', required=False, action='store_true',
                        help='Decrease subtitle\'s delay. If this option is not provided, delay will be increased.')
    parser.add_argument('-f', '--time_format', dest='time_format', required=False, default='%H:%M:%S.%f',
                        help='Time format used by the subtitle file. Do not use this option if you are not familiar with that. It will use "%%H:%%M:%%S.%%f" as the default format if this option is not provided.')
    args = parser.parse_args()
    increase = False if args.decrease else True
    process(args.input_file, args.output_file, args.seconds, increase=increase, time_format=args.time_format)
    # path = '/Users/gogleyin/Downloads/ok.txt'
    # new_file = path + '.new.txt'
    # process(path, new_file, 148, increase=False, time_format=TIME_FORMAT)
