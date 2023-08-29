# -*- coding: utf-8 -*-
# 定义
#   输入: 1个TimeSeries  1个MultiColumn
#   输出: 无
# 用途
#   1 根据GraphicalEditor输入MultiColumn的数据段,截取文件
#   2 输出csv文件 [截断后的时域数据] 

import pprint
import copy
import os



def glyphscript(engineState):

    with open('_temp_csv_paths.txt', 'r') as f:
        csv_paths = [v for v in f.read().split('\n') if v]

    damage_2d = []
    names = []
    for csv_path in csv_paths:
        csv_path = csv_path[:-4]+'_PDI.csv'
        channel_titles, damage_1d = read_pdi_csv_path(csv_path)
        damage_2d.append(damage_1d)
        names.append(os.path.basename(csv_path))

    csv_path = r'sum_damage.csv'
    output_csv_data(csv_path, [channel_titles]+damage_2d, ['channel_titles']+names)


    # f = open(r'D:\test.txt', 'w')
    # f.write(','.join(channel_titles)+'\n')
    # for damage_1d in damage_2d:
    #     f.write(','.join([str(v) for v in damage_1d])+'\n')
    # f.write('\n')
    # f.write(','.join(cut_names)+'\n')


    
    
    # f.write(getTS_file_name(tsin1))
    # f.close()
    # 
    return ''


def read_pdi_csv_path(csv_path):
    with open(csv_path, 'r') as f:
        lines = [line for line in f.read().split('\n')[1:] if line]

    titles, damage_1d = [], []
    for line in lines:
        title, damage = line.split(',')
        titles.append(title)
        damage_1d.append(damage)
    return titles, damage_1d


def output_csv_data(file_path, data, titles):

    f = open(file_path, 'w')
    f.write(','.join(titles) + '\n')
    for row in range(len(data[0])):
        for col in range(len(data)):
            f.write(str(data[col][row]) + ',')
        f.write('\n')

    f.close()
    return None




