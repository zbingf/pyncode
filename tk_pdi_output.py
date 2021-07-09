# -*- coding: utf-8 -*-
# 读取PDI计算结果 MetaData
import logging
import os
import json
import subprocess

# current_path = r'D:\github\pyncode'
# os.chdir(current_path)
log_path = 'ts_pdi_output.log'
with open(log_path,'w') as f : pass
logging.basicConfig(level=logging.INFO, filename=log_path)

"""
pdi_dic = {
	slope 		: [float, float, ...]
	rms 		: [float, float, ...]
	intercept	: [float, float, ...]
	min 		: [float, float, ...]
	max 		: [float, float, ...]
	damage 		: [float, float, ...]
	testname 	: str
	chantitle 	: [str, str, ...]
	samplerate 	: [float, float, ...]
	block_size	: int
	hz_range 	: [float, float]
}
"""


def glyphscript(engineState):
	# 主函数

	ts_obj_in0 = engineState.GetInputTimeSeries(0)

	output_pdi_data(ts_obj_in0)

	return ''

# 导出PDI数据
def output_pdi_data(ts_obj_in0):

	md_obj_in0 = ts_obj_in0.GetMetaData()

	pdi_dic0 = get_pdi_metadata(md_obj_in0)

	pdi_dic0['block_size'] 	= 1024

	pdi_dic0['hz_range'] 	= [0,50]
	
	data0 = getTS(ts_obj_in0)

	# 数据保存
	json_path = os.path.abspath(pdi_dic0['testname']+'_pdi.json')
	with open(json_path,"w") as f:
		json.dump(pdi_dic0, f)

	logging.info('End')
	logging.shutdown()
	return ''

def get_pdi_metadata(md_obj):
	"""
	pdi_dic = {
		slope 		: [float, float, ...]
		rms 		: [float, float, ...]
		intercept	: [float, float, ...]
		min 		: [float, float, ...]
		max 		: [float, float, ...]
		damage 		: [float, float, ...]
		testname 	: str
		chantitle 	: [str, str, ...]
		samplerate 	: [float, float, ...]
	}
	"""
	md_obj_in0 = md_obj
	
	num = md_obj_in0.GetChannelCount(0)
	logging.info('num: {}'.format(num))

	chantitles, damages, intercepts, slopes = [], [], [], []
	maxs, mins, rmss = [], [], []
	pdi_dic = {}
	names = ['chantitle','damage','intercept','slope','max','min','rms','samplerate']

	for n in range(num):
		if n == 0:
			for name in names:
				pdi_dic[name] = []

		chantitle = md_obj_in0.GetChanTitle(n)
		pdi_dic['chantitle'].append(chantitle)

		for name in names[1:]:
			pdi_dic[name].append(md_obj_in0.GetItem(n, name))

	test_name = md_obj_in0.GetItem(-1, 'TestName')
	pdi_dic['testname'] = test_name
	# logging.info('TestName:{}'.format(test_name))

	logging.info('pdi_dic : {}'.format(pdi_dic))

	return pdi_dic

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

