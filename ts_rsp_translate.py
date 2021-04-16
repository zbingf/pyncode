# -*- coding: utf-8 -*-
# python 2.7
'''
	修改 TS 数据 , 用于 RPC3 数据生成
	包括:
		samplerate 采样频率
		确认是否 首尾数据调0
	一个输入通道 TimeSeris
	一个输出通道 TimeSeris
'''
import logging
import os
current_path = r'D:\github\pyncode'
os.chdir(current_path)
logging.basicConfig(level=logging.INFO, filename='debug.log')

def glyphscript(engineState):
	'''
		主函数
	'''
	# 输入参数
	is_zero = True
	samplerate_new = 511.85

	tsin1 = engineState.GetInputTimeSeries(0)
	tsout1 = engineState.GetOutputTimeSeries(0)
	list1 = getTS(tsin1)
	if is_zero:
		for line in list1:
			line[0] = 0
			line[-1] = 0

	putTS(tsout1,tsin1,list1)
	n_channel = tsin1.GetChannelCount()
	for n in range(n_channel):
		tsout1.SetSampleRate(n,samplerate_new)

	logging.shutdown()
	return ''


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
