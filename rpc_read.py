# -*- coding: utf-8 -*-
'''
	读取 RPC3 格式数据

'''
import sys,os
import struct


def glyphscript(engineState):
	'''
		主函数
		用于ncode中验证函数正确性
	'''
	# 输入参数
	is_zero = True
	samplerate_new = 511.85

	tsin1 = engineState.GetInputTimeSeries(0)
	tsout1 = engineState.GetOutputTimeSeries(0)

	tsin1_metadata = tsin1.GetMetaData()
	# 调用第1通道指定的文件路径
	rpc_path = tsin1_metadata.GetItem(0, 'FilenameWithPath')

	list1 , dic , name_channels = get_rsp_data(rpc_path)

	putTS(tsout1,tsin1,list1)

	return ''

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

def get_rsp_data(rpcFile):
	'''
		读取 RPC3 文件数据

	'''

	rpcFile = os.path.abspath(rpcFile)
	# 判定文件是否存在
	if not(os.path.isfile(rpcFile)): 
		print('RPC File " %s " Not Found' %rpcFile)
		return
	
	# 读取开头数据
	file   = open(rpcFile,'rb')
	r = file.read(512)

	num =  len(r)//128
	dic    = {}
	for i in range(num):
		s = i*128
		e = s + 32
		key = r[s:e]
		key = key.replace(b'\x00',b'').decode()
		if key != '' : 
			v = e+96
			value = r[e:v]
			value = value.replace(b'\x00',b'').decode()
			dic[key] = value

	numHeader = int(dic['NUM_HEADER_BLOCKS'])

	r = file.read(512*(numHeader-1))
	num = len(r)//128 
	for i in range(num):
		s = i*128
		e = s + 32
		key = r[s:e]
		key = key.replace(b'\x00',b'').decode()
		if key != '' : 
			v = e+96
			value = r[e:v]
			value = value.replace(b'\x00',b'').decode()
			dic[key] = value

	# 开头数据解析
	# print(dic)
	# 通道数
	n_channel = int(dic['CHANNELS']) 
	# 通道名称
	name_channels = [ dic['DESC.CHAN_{}'.format(n+1)] for n in range(n_channel)]
	# print(name_channels)
	# SCALE 系数
	scales = [ float(dic['SCALE.CHAN_{}'.format(n+1)]) for n in range(n_channel)]
	# print(scales)
	# frame数
	n_frame = int(dic['FRAMES'])
	frame = int(dic['PTS_PER_FRAME'])
	# group
	group = int(dic['PTS_PER_GROUP'])
	n_group = max(1, int(frame*n_frame//group))
	# print(frame*n_frame,group,n_group)
	if frame*n_frame > n_group*group:
		n_group +=1

	# 数据段读取并解析
	data_list = [ [] for n in range(n_channel) ]

	for n_g in range(n_group):
		for num in range(n_channel):
			cal_n = group
			if n_g == n_group-1:
				# 最后一段数据读取 , 并不一定完整解析
				if frame*n_frame < group*n_group:
					cal_n = frame*n_frame - group*(n_group-1)

			r = file.read(group*2)
			data_raw = struct.unpack('h'*int(group),r)
			for n,temp1 in zip(data_raw,range(cal_n)):
				data_list[num].append(n*scales[num])

	# data_list 各同道数据

	# 关闭文档
	file.close()


	return data_list , dic , name_channels

def cal_compare(list1,list2):
	'''
		数据评估 - 评价数据拟合程度
		list1 与 list2 均为 二维数据
		list2 为目标数据
	'''
	values1 = ts_fun.cal_rms_delta_percent(list1,list2)
	values2 = ts_fun.cal_rms_percent(list1,list2)
	values3 = ts_fun.cal_max_percent(list1,list2)
	values4 = ts_fun.cal_min_percent(list1,list2)
	values5 = ts_fun.cal_pdi_relative(list1,list2)

	# [values1,values2,values3,values4,values5]
	return { 'rms_delta_percent':values1, 'rms_percent':values2 , 
		'max_percent':values3 , 'min_percent':values4 , 
		'pdi_relative':values5 }

def figure_plot(data_list,names,xlabel,ylabel):
	'''
		data_list 为 多通道数据 即 二维数据
	'''
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for n in range(len(data_list)):
		ax.plot(data_list[n])
	ax.legend(names , 	loc = 'upper left' )
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

def cal_rpcs_compare(rpc_path,n_it=100):

	path = os.path.dirname(rpc_path)
	name = os.path.basename(rpc_path)
	target_list , dic , name_channels = get_rsp_data(rpc_path)

	cal_name = ['_{}.rsp'.format(n) for n in range(n_it)]
	cal_lists = []
	result_lists = []
	for num , name_end in enumerate(cal_name):
		new_name = name[:-4] + name_end
		cal_path = os.path.join( path,new_name )
		if os.path.isfile(cal_path) == False:
			break
		list1 , __ , __ = get_rsp_data(cal_path)

		result_lists.append( cal_compare(list1,target_list) )
		cal_lists.append(list1)
		# print(cal_path)

	# 处理计算结果
	n_channel_list = [n for n in range(len(name_channels))]
	rms_delta_percents = [ [ result_lists[n]['rms_delta_percent'][n_chan] for n in range(len(result_lists))]
		for n_chan in n_channel_list ]
	rms_percents = [ [ result_lists[n]['rms_percent'][n_chan] for n in range(len(result_lists))]
		for n_chan in n_channel_list ]
	max_percents = [ [ result_lists[n]['max_percent'][n_chan] for n in range(len(result_lists))]
		for n_chan in n_channel_list ]
	min_percents = [ [ result_lists[n]['min_percent'][n_chan] for n in range(len(result_lists))]
		for n_chan in n_channel_list ]
	pdi_relatives = [ [ result_lists[n]['pdi_relative'][n_chan] for n in range(len(result_lists))]
		for n_chan in n_channel_list ]

	# 作图
	plt.rcParams['font.family']=['sans-serif']
	plt.rcParams['font.sans-serif'] = ['SimHei']
	plt.rcParams['axes.unicode_minus']=False

	figure_plot(rms_delta_percents,name_channels,'迭代次数','误差均方根 / 目标信号均方根')
	figure_plot(rms_percents,name_channels,'迭代次数','测量信号均方根 / 目标信号均方根')
	figure_plot(max_percents,name_channels,'迭代次数','测量信号最大值 / 目标信号最大值')
	figure_plot(min_percents,name_channels,'迭代次数','测量信号最小值 / 目标信号最小值')
	figure_plot(pdi_relatives,name_channels,'迭代次数','测量信号PDI / 目标信号PDI')

	return ''

if __name__ == '__main__':
	import tkinter
	import tkinter.messagebox #这个是消息框，对话框的关键
	import tkinter.filedialog
	tkobj=tkinter.Tk()
	# 隐藏隐藏主窗口
	tkobj.withdraw()

	import matplotlib.pyplot as plt
	import ts_fun
	# 迭代目标数据-文件路径
	# rpc_path = r'E:\workspace\FEMFAT-Lab\six_dof_rig\hight_pass_1HZ.rsp'
	rpc_path = tkinter.filedialog.askopenfilename()
	# rpc_path = r'E:\workspace\FEMFAT-Lab\six_dof_rig\temp.rsp'
	# print(path,name)
	# 迭代次数
	# n_it = 16
	cal_rpcs_compare(rpc_path)

	# print(len(target_list[0]))
	# print(len(cal_lists[0][0]))

	plt.show()