# -*- coding: utf-8 -*-
import logging
import os
import subprocess

current_path = r'D:\github\pyncode'
os.chdir(current_path)
logging.basicConfig(level=logging.INFO, filename='debug.log')

def glyphscript(engineState):
	ts_in0 = engineState.GetInputTimeSeries(0)

	list1 = getTS(ts_in0)
	data2csv('test.csv', list1, reqs=None,comps=None)

	proc = subprocess.Popen('sys_cal.exe aaa bbb')
	
	logging.shutdown()
	return ''

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

def data2csv(csv_path, data, reqs=None,comps=None): # 数据导出为csv格式
	"""
		csv_path 	目标csv路径
		data 	list(list) 		二维数组
		reqs 	list 			一位数组（标题前缀）
		comps 	list 			一维数组（标题后缀）
		example:
			req.comp 	req.comp
			1.1			1.1
			1.1			1.1
	"""
	# drv_path[:-3]+'csv'
	if reqs == None :
		reqs = ['n' for n in range(len(data))]
	if comps == None :
		comps = ['n' for n in range(len(data))]

	f = open(csv_path,'w')
	f.write(
		','.join(['{}.{}'.format(a,b) for a,b in zip(reqs,comps)])
		)
	f.write('\n')
	for n in range(len(data[0])):
		for loc in range(len(data)):
			f.write(str(data[loc][n]))
			f.write(',')
		f.write('\n')
	f.close()

	return True

