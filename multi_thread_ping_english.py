# -*- coding: utf-8 -*-
import os
from concurrent.futures import ThreadPoolExecutor
import re
import subprocess
import datetime
import multiprocessing
import sys


def get_system_date():
    ISOTIMEFORMAT = '%Y-%m-%d-%H'
    cur_time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    return cur_time


def read_ip(read_path):
    with open(read_path, 'r') as f:
        return f.readlines()


def write_file(write_path, res):
    with open(write_path, 'a') as file_object:
        file_object.write(res)


# ip_address代表要ping的ip；ip_num代表ping的次数,res代表存放数据的队列
def get_ping_result(ip_address):
    p = subprocess.Popen('ping %s -n 50' % ip_address,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out = p.stdout.read().decode('gbk')
    print(out)
    reg_receive = 'Received = \d{1,2}'
    match_receive = re.search(reg_receive, out)

    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group()[11:])

    if receive_count > 0:  # 接受到的反馈大于0，表示网络通
        reg_min_time = 'Minimum = \d+ms'
        reg_max_time = 'Maximum = \d+ms'
        reg_avg_time = 'Average = \d+ms'

        match_min_time = re.search(reg_min_time, out)
        min_time = int(match_min_time.group()[10:-2])

        match_max_time = re.search(reg_max_time, out)
        max_time = int(match_max_time.group()[10:-2])

        match_avg_time = re.search(reg_avg_time, out)
        avg_time = int(match_avg_time.group()[10:-2])

        return ip_address + ',' + str(receive_count) + ',' + str(min_time) + '/' + str(max_time) + '/' + str(avg_time)
    else:
        return ip_address + ',' + '0' + ',' + 'connection timeout'


def get_tracert_result(ip_address):
    p = subprocess.run('tracert {}'.format(ip_address),
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       shell=True)
    out = p.stdout.decode('gbk')
    print(out)
    return out


def set_call_back(x):
    write_file(get_system_date() + ".txt", x + '\n')


def ping():
    read_path = r'ip.txt'
    ip_list = [ip.replace('\n', '') for ip in read_ip(read_path)]
    print("**********************ping start***********************\n", str(len(ip_list)) + " ip start execute")
    pool = ThreadPoolExecutor(10)
    for data in pool.map(get_ping_result, ip_list):
        write_file(get_system_date() + ".txt", data + '\n')
    print("--------------------ping end------------------------")
    sys.exit()


def tracert():
    read_path = r'ip.txt'
    ip_list = [ip.replace('\n', '') for ip in read_ip(read_path)]
    print("**********************tracert start***********************\n", str(len(ip_list)) + " ip start execute")
    pool = ThreadPoolExecutor(10)
    for data in pool.map(get_tracert_result, ip_list):
        write_file(get_system_date() + ".txt", data + '\n')
    print("--------------------tracert end------------------------")
    sys.exit()


# if need to ping, please annotate tracert().if need to tracert, need to annotate ping()
if __name__ == '__main__':
    ping()
    # tracert()
