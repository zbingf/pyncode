# -*- coding: utf-8 -*-
# python 2.7
'''
	等长数据-对比
	
	
'''
import logging
import os
current_path = r'D:\github\pyncode'
os.chdir(current_path)
logging.basicConfig(level=logging.INFO, filename='debug.log')

def glyphscript(engineState):
	'''
		主函数
		两信号差值的 RMS 计算
		时域信号
		两个输入通道 TimeSeris
		一个输出通道 MetaData
	'''
	tsin1 = engineState.GetInputTimeSeries(0)
	tsin2 = engineState.GetInputTimeSeries(1)

	tsin1_meta = tsin1.GetMetaData()
	meta_out_1 = engineState.GetOutputMetaData(0)

	list1 = getTS(tsin1)
	list2 = getTS(tsin2)
	nlist1 = len(list1[0])
	nlist2 = len(list2[0])
	if nlist1 != nlist2:
		num = min(nlist1,nlist2)
		for line1,line2 in zip(list1,list2):
			del line1[num:]
			del line2[num:]

	values1 = cal_rms_delta_percent(list1,list2)
	values2 = cal_rms_percent(list1,list2)
	values3 = cal_max_percent(list1,list2)
	values4 = cal_min_percent(list1,list2)
	values5 = cal_pdi_relative(list1,list2)
	channel_num = int(tsin1.GetChannelCount())

	meta_out_1.SetChannelCount(channel_num)
	for n in range(channel_num):
		meta_out_1.SetChanNumber(n,n)
		meta_out_1.SetChanTitle(n,tsin1_meta.GetChanTitle(n))
		meta_out_1.SetItem(n,'compare','rms_delta_percent','float',values1[n])
		meta_out_1.SetItem(n,'compare','rms_percent','float',values2[n])
		meta_out_1.SetItem(n,'compare','rms_max_percent','float',values3[n])
		meta_out_1.SetItem(n,'compare','rms_min_percent','float',values4[n])
		meta_out_1.SetItem(n,'compare','pdi_relative','float',values5[n])

	cal_pdi(list1,b=5000.0,k=-5.0)
	
	logging.shutdown()
	return ''

def cal_rms_delta_percent(list1,list2):
	'''
		误差均方根 / 目标均方根
	'''
	values_delta = cal_rms_delta(list1,list2)
	values_target = cal_rms(list2)

	list3 = [ float(n1)/float(n2) for n1,n2 in zip(values_delta,values_target)]

	return list3

def cal_rms_percent(list1,list2):
	'''
		测量均方根 / 目标信号均方根
	'''
	data = []
	data1 = cal_rms(list1)
	data2 = cal_rms(list2)
	for n in range(len(data1)):
		data.append( float(data1[n]) / float(data2[n]) )

	return data

def cal_max_percent(list1,list2):
	'''
		测量信号最大值 / 目标信号最大值
	'''
	maxs1 = [max(line) for line in list1]
	maxs2 = [max(line) for line in list2]
	values = [ float(max1) / float(max2) for max1,max2 in zip(maxs1,maxs2)]

	return values

def cal_min_percent(list1,list2):
	'''
		测量信号最小值 / 目标信号最小值
	'''
	mins1 = [min(line) for line in list1]
	mins2 = [min(line) for line in list2]
	values = [ float(min1) / float(min2) for min1,min2 in zip(mins1,mins2)]

	return values

def cal_pdi_relative(list1,list2):
	'''
		测量信号PDI / 目标信号PDI
	'''
	damage1 = cal_pdi(list1)
	damage2 = cal_pdi(list2)

	values = [ float(d1)/float(d2) for d1,d2 in zip(damage1,damage2)]

	return values

def cal_pdi(list1,b=5000.0,k=-5.0):
	'''
		伪损伤
	'''
	import math

	A = math.log10(b)
	B = 1.0/k

	damage = [ sum( [ 1.0/10.0**( (math.log10(abs(n))-A)/float(B) ) for n in line if n!=0 ] ) for line in list1]

	return damage

def putTS(tsobj,tartsobj,list1):
	# 对时间序列进行赋值
	# 复制tartsobj属性 到 tsobj中
	# 将列表list1 作为数据 导入 tsobj中
	import array
	num = len(list1)
	if type(list1[0]) == list :
		tsobj.SetChannelCount(num)
		len_value = len(list1[0])
		for n in range(num):
			tsobj.CopyAttributes(tartsobj,n,n)
			tsobj.SetPointCount(n,len_value)
			arr1 = array.array('f',list1[n])
			tsobj.PutValues(n,0,len_value,arr1)
	else:
		tsobj.SetChannelCount(1)
		tsobj.CopyAttributes(tartsobj,0,0)
		tsobj.PutValues(0,num,1,list1)

def getTS(tsobj):
	# 获取 time series 数据
	# 转化为列表导出
	num = tsobj.GetChannelCount()
	list1 = []
	for n in range(num):
		listnum = tsobj.GetPointCount(n)
		list_temp = tsobj.GetValuesAsList(n,0,listnum)
		list1.append(list_temp)
	return list1

# 相关计算
def cal_rms(list1):
	# RMS 均方根计算
	# 二维数组 
	nlist = len(list1)
	len_value = len(list1[0])
	data = []
	for n in range(nlist):
		templist = []
		for n1 in range(len_value):
			temp = float(list1[n][n1])**2.0 / float(len_value)
			templist.append(temp)
		value1 = sum(templist) ** 0.5
		data.append(value1)
	return data

def cal_delta(list1,list2):
	# 计算两组数据的差值
	# list1 - list2 
	nlist = len(list1)
	len_value = len(list1[0])
	data = [] # 重新创立数组
	for n in range(nlist):
		templist = []
		for n1 in range(len_value):
			templist.append(list1[n][n1]-list2[n][n1])
		data.append(templist)
	return data

def cal_rms_delta(list1,list2):
	# 计算 两个list的差值 对应的 rms
	list3 = cal_delta(list1,list2)
	data = cal_rms(list3)
	return data
