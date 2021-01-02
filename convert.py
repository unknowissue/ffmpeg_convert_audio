import numpy as np
import os, sys, threading
from datetime import datetime
from dateutil.relativedelta import relativedelta

##文件当前路径
currentVideoPath = os.path.join(sys.path[0])
##第一个参数为需要切换的文件名，python3 convert.py filename.mp4
file_name = sys.argv[1]
##循环控制参数
i = 0

##读取参数文件
with open('time_name.txt', 'r') as f:
    data = f.readlines()  #txt中所有字符串读入data

    ##循环每行
    for line in data:
        #将单个数据分隔开存好
        time_name = line.split()
        ##获取时间
        time_old = time_name[0]
        ##获取分钟数
        s_min = list(map(int, time_name[0].split(':',1)))
        ##分钟数转换为小时数
        hor = s_min[0]//60
        ##实际分钟数
        min = s_min[0]%60
        ##实际秒数
        sec = list(map(int, time_name[0].split(':',1)))[1]
        #print(hor)
        #print(min)
        #print(sec)
        ##时间相见时需要日期，需要拼接
        s_date_time = '2021-01-01 ' + str(hor) + ':' + str(min) + ':' + str(sec)
        d_date_time = datetime.strptime(s_date_time,'%Y-%m-%d %H:%M:%S')
        ##时间获取，-ss %s 参数和文件名需要
        s_time=str(hor) + ':' + str(min) + ':' + str(sec)
        mp3_filename =  time_name[1] + s_time.replace(':','_',2)
        i = i + 1
        ##因为需要两行时间进行对比求差，首行不进行比较
        if i > 1:
            ##求增量 -t 参数需要
            diff_time = (d_date_time - d_old_date_time).seconds - 1
            if diff_time == 0:
                ##时间没有差值：已经读取到最后一行
                os.system('ffmpeg -ss %s  -i %s  -c:v libx264 -c:a aac -strict experimental -b:a 320k -avoid_negative_ts 1  %s.aac' % (s_old_time,file_name,s_old_mp3_filename))
            else:
                ##时间没有差值：存在最后一行
                os.system('ffmpeg -ss %s  -i %s -t %s -c:v libx264 -c:a aac -strict experimental -b:a 320k -avoid_negative_ts 1  %s.aac' % (s_old_time,file_name,diff_time,s_old_mp3_filename))
                #print('ffmpeg -ss %s  -i %s -t %s -c:v libx264 -c:a aac -strict experimental -b:a 320k -avoid_negative_ts 1  %s.aac' % (s_old_time,file_name,diff_time,s_old_mp3_filename))
        d_old_date_time = d_date_time
        s_old_date_time = s_date_time
        s_old_mp3_filename = mp3_filename
        s_old_time= s_time
