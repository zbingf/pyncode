# -*- coding: utf-8 -*-
import logging
import os
import json
import subprocess
from pprint import pprint, pformat

log_path = 'py_temp.txt'
with open(log_path,'w') as f : pass
logging.basicConfig(level=logging.INFO, filename=log_path)


def glyphscript(engineState):
	# 主函数

	ts_in0 = engineState.GetInputTimeSeries(0)
	ts_in1 = engineState.GetInputTimeSeries(1)

	ts_out0 = engineState.GetOutputTimeSeries(0)

	list2d_0 = get_ts_data(ts_in0)
	list2d_1 = get_ts_data(ts_in1)

	list2d_new = []
	for line0, line1 in zip(list2d_0, list2d_1):
		line_new = []
		for n0, n1 in zip(line0, line1):
			n = n0 + n1
			line_new.append(n)
		list2d_new.append(line_new)

	str_log = pformat(list2d_new)
	logging.info(str_log)

	os.popen(log_path)

	output_ts_data(ts_out0, ts_in0, list2d_new)

	return ''


def output_ts_data(tsobj, tartsobj, list1):
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

def get_ts_data(tsobj):
	"""
		获取 time series 数据
		转化为列表导出	
	"""
	num = tsobj.GetChannelCount()
	list1 = []
	for n in range(num):
		listnum = tsobj.GetPointCount(n)
		list_temp = tsobj.GetValuesAsList(n,0,listnum)
		list1.append(list_temp)

	return list1

