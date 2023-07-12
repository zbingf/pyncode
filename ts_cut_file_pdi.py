# -*- coding: utf-8 -*-
# 定义
#   输入: 1个TimeSeries  1个MultiColumn
#   输出: 无
# 用途
#   1 根据GraphicalEditor输入MultiColumn的数据段,截取文件
#   2 计算PDI损伤
#   3 输出csv文件 [截断后的时域数据] 


import pprint
import copy


def glyphscript(engineState):
    tsin1 = engineState.GetInputTimeSeries(0)
    list1 = getTS(tsin1)
    mobj = engineState.GetInputMultiColumn(0)
    list_range = get_list_range(mobj)
    
    cut_names = ['full']
    list3d = [list1]
    for n_range in list_range:
        list2d = []
        for line in list1:
            list2d.append(line[n_range[0]:n_range[1]])
        list3d.append(list2d)
        cut_names.append(str(n_range[0])+'_'+str(n_range[1]))

    damage_2d = output_csv_list3d(list3d)

    channel_titles = getTS_channel_name(tsin1)
    channel_titles = [str(n)+'_'+v for n,v in enumerate(channel_titles)]

    # f = open(r'D:\test.txt', 'w')
    # f.write(','.join(channel_titles)+'\n')
    # for damage_1d in damage_2d:
    #     f.write(','.join([str(v) for v in damage_1d])+'\n')
    # f.write('\n')
    # f.write(','.join(cut_names)+'\n')
    # f.close()

    n = 0
    for cut_name, list2d in zip(cut_names, list3d):
        csv_path = 'D:\\' + cut_name + '.csv'
        if n > 0:
            output_csv_data(csv_path, list2d, channel_titles)
        n+=1

    csv_path = r'D:\damage.csv'
    # for damage_1d in damage_2d:

    output_csv_data(csv_path, [channel_titles]+damage_2d, ['channel_titles']+cut_names)


    return ''


def output_csv_data(file_path, data, titles):

    f = open(file_path, 'w')
    f.write(','.join(titles) + '\n')
    for row in range(len(data[0])):
        for col in range(len(data)):
            f.write(str(data[col][row]) + ',')
        f.write('\n')

    f.close()
    return None


def getTS_channel_name(tsobj):
    num = tsobj.GetChannelCount()
    list1 = []
    for n in range(num):
        list1.append(tsobj.GetChanTitle(n))
    return list1

def output_csv_list3d(list3d):
    damage_2d = []
    for loc, list2d in enumerate(list3d):
        damage_1d = cal_rainflow_pdi(list2d)
        damage_2d.append(damage_1d)
    
    return damage_2d

def get_list_range(mobj):
    tobj = mobj.GetTable(0, 0)
    n_row = tobj.GetRowCount()
    list_range = []
    for n in range(n_row):
        list_range.append([tobj.GetValue(2, n), tobj.GetValue(3, n)])
    return list_range

def getTS(tsobj):
    num = tsobj.GetChannelCount()
    list1 = []
    for n in range(num):
        listnum = tsobj.GetPointCount(n)
        list_temp = tsobj.GetValuesAsList(n, 0, listnum)
        list1.append(list_temp)
    return list1


def cal_pdi(list1, b=5000.0, k=-5.0):

    import math

    A = math.log10(b)
    B = 1.0/k

    damage = [ sum( [ 1.0/10.0**((math.log10(abs(n))-A)/B) for n in line if n!=0 ] ) for line in list1]

    return damage


def cal_rainflow_pdi(list2d, b=5000.0, k=-5.0):
    
    new_list2d = []
    for line in list2d:
        try:
            values, means = rainflow_3point(line)
        except:
            values, means = [0.0], [0.0]

        values = [2*n for n in values] 
        new_list2d.append(values)

    return cal_pdi(new_list2d, b, k)

def rainflow_3point(list1):
    newlist = _list_updown(list1)
    num = len(newlist)
    value_max = max(newlist)
    value_loc = newlist.index(value_max)
    l1 = newlist[value_loc:] + newlist[:value_loc+1]
    newlist = _list_updown(l1)
    values, means, rainlist = [],[],[]
    num = len(newlist)
    count = 1
    last_num = 0
    while num > 1:
        if num >1 :
            last_num = len(newlist)
            for n in range(num-2):
                s1 = newlist[n]-newlist[n+1]
                s2 = newlist[n+2]-newlist[n+1]
                e3 = (newlist[n]+newlist[n+1])/2.0
                if s1 > 0 and s2 > 0 and s1 <= s2:
                    values.append(s1/2.0)
                    means.append(e3)
                    del newlist[n+1]
                    del newlist[n]
                    break
        num = len(newlist)
        if last_num == num :
            newlist = _list_updown(newlist)
    return values,means

def _list_updown(list1):
    
    num = len(list1)
    l1 = list1
    l2 = copy.copy(list1)
    for n in range(1,num-1):
        if l1[n-1] < l1[n] and l1[n] < l1[n+1]:
            l2[n] = ''
        elif l1[n-1] > l1[n] and l1[n] > l1[n+1]:
            l2[n] = ''
        elif l1[n-1] == l1[n]:
            l2[n] = ''
    if l2[-2] == l2[-1]:
        l2[-2] = ''
    newlist = [n for n in l2 if n]
    num = len(newlist)
    return newlist
