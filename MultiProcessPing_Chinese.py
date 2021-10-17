# -*- coding: utf-8 -*-
import os
import subprocess
import re
import datetime
import multiprocessing
import sys


def GetSystemDate():
    ISOTIMEFORMAT = '%Y-%m-%d-%H'
    cur_time = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    return cur_time

def ReadIP(read_path):
    with open(read_path, 'r') as f:
        return f.readlines()

def WriteFile(write_path, res):
    with open(write_path, 'a') as file_object:
        file_object.write(res)

#ip_address代表要ping的ip；ip_num代表ping的次数,res代表存放数据的队列
def get_ping_result(ip_address):
    p = subprocess.Popen('ping %s -n 50' %ip_address,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    out = p.stdout.read().decode('gbk')
    print(out)
    reg_receive = '已接收 = \d{1,2}'
    match_receive = re.search(reg_receive, out)

    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group()[6:])

    if receive_count > 0:  #接受到的反馈大于0，表示网络通
        reg_min_time = '最短 = \d+ms'
        reg_max_time = '最长 = \d+ms'
        reg_avg_time = '平均 = \d+ms'

        match_min_time = re.search(reg_min_time, out)
        min_time = int(match_min_time.group()[5:-2])

        match_max_time = re.search(reg_max_time, out)
        max_time = int(match_max_time.group()[5:-2])

        match_avg_time = re.search(reg_avg_time, out)
        avg_time = int(match_avg_time.group()[5:-2])

        return ip_address+','+str(receive_count)+','+str(min_time)+'/'+str(max_time)+'/'+str(avg_time)
    else:
        return ip_address+','+'0'+','+'connection timeout'


def SetCallBack(x):
    WriteFile(GetSystemDate()+".txt",x+'\n')

def main():
    read_path = r'ip.txt'
    ip_list = ReadIP(read_path)
    print("**********************执行开始***********************\n",str(len(ip_list))+"个IP开始执行")
    pool = multiprocessing.Pool(processes=50)
    for i in range(len(ip_list)):
        t=pool.apply_async(func=get_ping_result,args=(ip_list[i].replace('\n', ''),),
        callback = SetCallBack)
    pool.close();
    pool.join();
    print("--------------------执行结束------------------------")
    sys.exit()


if __name__ == '__main__':
    main()
