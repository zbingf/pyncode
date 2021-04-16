# -*- coding: utf-8 -*-
# python 2.7
# 关于时间序列 timeseries 的相关计算函数

import logging
import os
current_path = r'D:\github\pyncode'
os.chdir(current_path)
logging.basicConfig(level=logging.INFO, filename='debug.log')



def ts_extend(tartsobj, tsobj1, tsobj2):
	# 时域数据拼接
	# 将tsobj2 接到 tsobj1 后面 赋予 tartsobj
	# tartsobj 属性 继承 tsobj1
	# 通道数 需保持一直

	list1 = getTS(tsobj1)
	list2 = getTS(tsobj2)
	for n in range(len(list1)):
		list1[n].extend(list2[n])
	
	# 数据拼接
	putTS(tartsobj,tsobj1,list1)

	return None


#获取\赋值时序信号数据
def putTS(tsobj,tartsobj,list1):
	# 对时间序列进行赋值
	# 复制tartsobj属性 到 tsobj中
	# 将列表list1 作为数据 导入 tsobj中
	import array
	num = len(list1)
	mdobj = tsobj.GetMetaData()
	tarmdobj = tartsobj.GetMetaData()

	if type(list1[0]) == list :
		tsobj.SetChannelCount(num)
		len_value = len(list1[0])
		for n in range(num):
			tsobj.CopyAttributes(tartsobj, n, n)
			tsobj.CopyMetaData(tartsobj, n, n)
			tsobj.SetPointCount(n, len_value)
			arr1 = array.array('f', list1[n])
			tsobj.PutValues(n, 0, len_value,arr1)
	else:
		tsobj.SetChannelCount(1)
		tsobj.CopyAttributes(tartsobj, 0, 0)
		tsobj.CopyMetaData(tartsobj, 0, 0)
		tsobj.PutValues(0, num, 1, list1)

	name = tarmdobj.GetItem(-1, 'TestName')
	mdobj.SetItem(-1, 'InputTestInfo', 'TestName', 'string', name)

	return None


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

def cal_rms_delta_percent(list1,list2):
	'''
		误差均方根 / 目标均方根
	'''
	# 等长评估, 以最短的为主
	n_l1 = len(list1[0])
	n_l2 = len(list2[0])
	if n_l1 > n_l2 :
		for line in list1:
			del line[n_l2:]
	elif n_l1 < n_l2:
		for line in list2:
			del line[n_l1:]

	values_delta = cal_rms_delta(list1,list2)
	values_target = cal_rms(list2)

	list3 = [ n1/n2 for n1,n2 in zip(values_delta,values_target)]

	return list3

def cal_rms_percent(list1,list2):
	'''
		测量均方根 / 目标信号均方根
	'''
	# 等长评估, 以最短的为主
	n_l1 = len(list1[0])
	n_l2 = len(list2[0])
	if n_l1 > n_l2 :
		for line in list1:
			del line[n_l2:]
	elif n_l1 < n_l2:
		for line in list2:
			del line[n_l1:]

	data = []
	data1 = cal_rms(list1)
	data2 = cal_rms(list2)
	for n in range(len(data1)):
		data.append(data1[n]/data2[n])

	return data

def cal_max_percent(list1,list2):
	'''
		测量信号最大值 / 目标信号最大值
	'''
	# 等长评估, 以最短的为主
	n_l1 = len(list1[0])
	n_l2 = len(list2[0])
	if n_l1 > n_l2 :
		for line in list1:
			del line[n_l2:]
	elif n_l1 < n_l2:
		for line in list2:
			del line[n_l1:]

	maxs1 = [max(line) for line in list1]
	maxs2 = [max(line) for line in list2]
	values = [ max1 / max2 for max1,max2 in zip(maxs1,maxs2)]

	return values

def cal_min_percent(list1,list2):
	'''
		测量信号最小值 / 目标信号最小值
	'''
	# 等长评估, 以最短的为主
	n_l1 = len(list1[0])
	n_l2 = len(list2[0])
	if n_l1 > n_l2 :
		for line in list1:
			del line[n_l2:]
	elif n_l1 < n_l2:
		for line in list2:
			del line[n_l1:]

	mins1 = [min(line) for line in list1]
	mins2 = [min(line) for line in list2]
	values = [ min1 / min2 for min1,min2 in zip(mins1,mins2)]

	return values

def cal_pdi_relative(list1,list2):
	'''
		测量信号PDI / 目标信号PDI
	'''
	# 等长评估, 以最短的为主
	n_l1 = len(list1[0])
	n_l2 = len(list2[0])
	if n_l1 > n_l2 :
		for line in list1:
			del line[n_l2:]
	elif n_l1 < n_l2:
		for line in list2:
			del line[n_l1:]

	damage1 = cal_pdi(list1)
	damage2 = cal_pdi(list2)

	values = [ d1/d2 for d1,d2 in zip(damage1,damage2)]

	return values

# def cal_pdi_relative2(list1,list2):
# 	'''
# 		测量信号PDI / 目标信号PDI
# 	'''
# 	damage1 = cal_pdi2(list1)
# 	damage2 = cal_pdi2(list2)

# 	values = [ d1/d2 for d1,d2 in zip(damage1,damage2) ]

# 	return values

def cal_pdi(list1,b=5000.0,k=-5.0):
	'''
		伪损伤
	'''
	import math

	A = math.log10(b)
	B = 1.0/k

	damage = [ sum( [ 1/10**((math.log10(abs(n))-A)/B) for n in line if n!=0 ] ) for line in list1]

	return damage

# def cal_pdi2(list1,b=5000,k=-5):
# 	'''
# 		伪损伤
# 	'''
# 	import math

# 	A = math.log10(b)
# 	B = 1/k

# 	damage = [ sum( [ 1/10**((math.log10(abs(n-min(line)))-A)/B) for n in line if n-min(line)!=0 ] ) for line in list1]

# 	return damage


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
			temp = list1[n][n1]**2 / len_value
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



