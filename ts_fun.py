# coding:utf-8
# python 2.7
# 关于时间序列 timeseries 的相关计算函数


def putTS(tsobj,tartsobj,list1):
	# 对时间序列进行赋值
	# 复制tartsobj属性 到 tsobj中
	# 将列表list1 作为数据 导入 tsobj中
	import array
	num = len(list1)
	if type(list1[0]) is list :
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
		tsobj.PutValues(0,num,len_value,list1)

def getTS(tsobj):
	# 获取 time series 数据
	# 转化为列表导出
	num = tsobj.GetChannelCount()
	list1 = []
	for n in range(list1):
		listnum = tsobj.GetPointCount(n)
		list_temp = tsobj.GetValuesAsList(n,0,listnum)
		list1.append(list_temp)
	return list1


'''
相关计算
'''

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

def cal_rms_percent(list1,list2):
	# 计算两个 list 的rms的比值
	data = []
	data1 = cal_rms(list1)
	data2 = cal_rms(list2)
	for n in range(len(data1)):
		data.append(data1[n]/data2[n])
	return data


a = [[1,1,1,1]]
b = [[2,2,2,2]]
print(cal_rms_percent(a,b))
print(cal_rms_delta(a,b))
print(cal_rms(a))






