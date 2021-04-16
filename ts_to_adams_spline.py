# -*- coding: utf-8 -*-
# python 2.7
'''
	将 TS 数据转化为 adams spline 生成命令
	一个输入通道 TimeSeris
	需要编辑:
		cmd_path
		modal_name
		spline_names
'''

import logging
import os
current_path = r'D:\github\pyncode'
os.chdir(current_path)
logging.basicConfig(level=logging.INFO, filename='debug.log')


def glyphscript(engineState):
	'''
		主函数
		将 TS 数据转化为 adams spline 生成命令
		时域信号
		一个输入通道 TimeSeris
	'''
	cmd_path = r'E:\workspace\FEMFAT-Lab\six_dof_rig\test.cmd'
	modal_name = 'six_dof_rig'
	spline_names = ['spline_x','spline_y','spline_z','spline_rx','spline_ry','spline_rz']

	tsin1 = engineState.GetInputTimeSeries(0)
	list1 = getTS(tsin1)

	strlist = []
	is_edit = True
	for line,spline_name in zip(list1,spline_names):
		if is_edit:
			samplerate = tsin1.GetSampleRate(0)
			xlist = [ float(n)/samplerate for n in range(len(line)) ]
			strlist.append( cmd_spline_edit(modal_name,spline_name,xlist,line) )

	str1 = '\n'.join(strlist)

	with open(cmd_path,'w') as f:
		f.write(str1)

	logging.shutdown()
	return ''


SPLINE_EDIT = '''
data_element modify spline &
 spline=.{}.{} &
 x={} &
 y={} &
 linear_extrapolate=no &
 units=no_units &
 comments=""
'''

SPLINE_CREATE = '''
data_element create spline &
 spline=.{}.{} &
 x={} &
 y={} &
 linear_extrapolate=no &
 units=no_units &
 comments=""
'''

def cmd_spline_edit(modal_name,spline_name,xlist,ylist):
	'''
		生成cmd命令
		编辑 adams 中的 spline曲线
	'''
	if modal_name[0] == '.':
		modal_name = modal_name[1:]
	if spline_name[0] == '.':
		spline_name = spline_name[1:]
	xstr = translate_list(xlist)
	ystr = translate_list(ylist)
	str1 = SPLINE_EDIT.format(modal_name,spline_name,xstr,ystr)
	return str1

def cmd_spline_create(modal_name,spline_name,xlist,ylist):
	'''
		生成cmd命令
		创建 adams 中的 spline曲线
	'''
	if modal_name[0] == '.':
		modal_name = modal_name[1:]
	if spline_name[0] == '.':
		spline_name = spline_name[1:]
	xstr = translate_list(xlist)
	ystr = translate_list(ylist)
	str1 = SPLINE_CREATE.format(modal_name,spline_name,xstr,ystr)
	return str1

def translate_list(lines):
	str1 = ', '.join([str(n) for n in lines])
	return str1

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


def csv_xy_read(fiilepath):
	'''
		近适用于 两列数据读取
	'''
	import csv
	x ,y = [] ,[]

	with open(fiilepath,'r') as f:
		reader=csv.reader(f)
		for row in reader:
			x.append(float(row[0]))
			y.append(float(row[1]))
	return x,y

if __name__ == '__main__':

	import matplotlib.pyplot as plt
	# import os.path
	fiilepath = r'E:\ADAMS\test.csv'
	cmdpath = fiilepath[:-4] + '.cmd'
	x,y = csv_xy_read(fiilepath)

	str1 = cmd_spline_create('._rigid_chassis','wind_force',x,y)

	with open(cmdpath,'w') as f:
		f.write(str1)

	# plt.plot(x,y)
	# plt.show()
