# -*- coding: utf-8 -*-
# 读取PDI计算结果 MetaData

import logging
import os
import json
import subprocess

current_path = r'D:\github\pyncode'
os.chdir(current_path)
log_path = 'ts_data_scatter_plot_output.log'
with open(log_path,'w') as f : pass
logging.basicConfig(level=logging.INFO, filename=log_path)


"""
	main_dic = {
		csv_path0 : str
		csv_path1 : str
		ts_dic0 : {
			rms 		: [float, float, ...]
			min 		: [float, float, ...]
			max 		: [float, float, ...]
			testname 	: str
			chantitle 	: [str, str, ...]
			samplerate 	: [float, float, ...]
		}
		ts_dic1 : { ... }
	}
"""

def glyphscript(engineState):
	# 主函数

	ts_obj_in0 = engineState.GetInputTimeSeries(0)
	ts_obj_in1 = engineState.GetInputTimeSeries(1)
	json_path = 'ts_data_scatter_plot_output.json'
	output_ts_data(json_path, ts_obj_in0, ts_obj_in1)

	return ''

# 导出PDI数据
def output_ts_data(json_path, ts_obj_in0, ts_obj_in1):

	md_obj_in0 = ts_obj_in0.GetMetaData()
	md_obj_in1 = ts_obj_in1.GetMetaData()

	ts_dic0 = get_ts_metadata(md_obj_in0)
	ts_dic1 = get_ts_metadata(md_obj_in1)

	data0 = getTS(ts_obj_in0)
	data1 = getTS(ts_obj_in1)

	csv_path0 = os.path.abspath('xs.csv')
	csv_path1 = os.path.abspath('ys.csv')

	data2csv(csv_path0, data0, ts_dic0['chantitle'])
	data2csv(csv_path1, data1, ts_dic1['chantitle'])

	# 所有数据
	main_dic = {
		'csv_path0':csv_path0,
		'csv_path1':csv_path1,
		'ts_dic0':ts_dic0,
		'ts_dic1':ts_dic1,
	}

	# 数据保存
	json_path = os.path.abspath(json_path)
	with open(json_path,"w") as f:
		json.dump(main_dic, f)

	# 运行
	proc = subprocess.Popen('python data_scatter_plot_input_cal.py {}'.format(json_path))
	# proc = subprocess.Popen('data_compare_input_cal {}'.format(json_path))

	logging.info('csv_path0 : {}'.format(csv_path0))
	logging.info('csv_path1 : {}'.format(csv_path1))

	logging.info('End')
	logging.shutdown()
	return ''


def get_ts_metadata(md_obj):
	"""
	ts_dic = {
		rms 		: [float, float, ...]
		min 		: [float, float, ...]
		max 		: [float, float, ...]
		testname 	: str
		chantitle 	: [str, str, ...]
		samplerate 	: [float, float, ...]
	}
	"""
	md_obj_in0 = md_obj
	
	num = md_obj_in0.GetChannelCount(0)
	logging.info('num: {}'.format(num))

	chantitles = []
	maxs, mins, rmss = [], [], []
	ts_dic = {}
	names = ['chantitle','max','min','rms','samplerate']

	for n in range(num):
		if n == 0:
			for name in names:
				ts_dic[name] = []

		chantitle = md_obj_in0.GetChanTitle(n)
		ts_dic['chantitle'].append(chantitle)

		for name in names[1:]:
			ts_dic[name].append(md_obj_in0.GetItem(n, name))

	test_name = md_obj_in0.GetItem(-1, 'TestName')
	ts_dic['testname'] = test_name
	# logging.info('TestName:{}'.format(test_name))

	logging.info('ts_dic : {}'.format(ts_dic))

	return ts_dic

# 输出ts
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

# 获取ts
def getTS(tsobj):
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

# 数据转csv
def data2csv(csv_path, data, chantitles=None): # 数据导出为csv格式
	"""
		csv_path 	目标csv路径
		data 	list(list) 		二维数组
		chantitles 	list 			一位数组（标题前缀）
	"""
	if chantitles == None :
		chantitles = ['n' for n in range(len(data))]

	f = open(csv_path,'w')
	f.write(','.join(chantitles))
	f.write('\n')
	for n in range(len(data[0])):
		for loc in range(len(data)):
			f.write(str(data[loc][n]))
			f.write(',')
		f.write('\n')
	f.close()

	return True

