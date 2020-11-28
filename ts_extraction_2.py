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

def glyphscript(engineState):
	'''
		主函数
		将 TS 数据转化为 adams spline 生成命令
		时域信号
		一个输入通道 TimeSeris
	'''

	ts_in1 = engineState.GetInputTimeSeries(0)
	list1 = getTS(ts_in1)
	ts_in2 = engineState.GetInputTimeSeries(1)
	list2 = getTS(ts_in2)

	# 数据拼接
	putTS(tartsobj,tsobj1,list1)

	return ''





#获取\赋值时序信号数据

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

