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

	list1 = get_rsp_data(rpc_path)

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


	return data_list  

if __name__ == '__main__':
	# if len(sys.argv) < 2:
	# 	print("\n\n A .rpc file needed")
	# 	sys.exit()  
	rpc_path = r'E:\workspace\FEMFAT-Lab\six_dof_rig\hight_pass_1HZ.rsp'
	rpc_path = r'E:\workspace\FEMFAT-Lab\six_dof_rig\temp.rsp'
	get_rsp_data(rpc_path)

	# path:E:\Software\MSC.Software\Adams\2019\adamssdk\include



