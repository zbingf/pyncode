# -*- coding: utf-8 -*-
'''
平顺性计算
输入频域数据
导出数据


'''
RIDE = [
	# 下限频率,上限频率,wk*1000,wd*1000,wc*1000
	[0.45,0.57,418,853,843],
	[0.57,0.71,459,944,929],
	[0.71,0.9,477,992,972],
	[0.9,1.12,482,1011,991],
	[1.12,1.4,484,1008,1000],
	[1.4,1.8,494,968,1007],
	[1.8,2.24,531,890,1012],
	[2.24,2.8,631,776,1017],
	[2.8,3.55,804,642,1022],
	[3.55,4.5,967,512,1024],
	[4.5,5.6,1039,409,1013],
	[5.6,7.1,1054,323,974],
	[7.1,9,1036,253,891],
	[9,11.2,988,212,776],
	[11.2,14,902,161,647],
	[14,18,768,125,512],
	[18,22.4,636,100,409],
	[22.4,28,513,80,325],
	[28,35.5,405,63.2,256],
	[35.5,45,314,49.4,199],
	[45,56,246,38.8,156],
	[56,71,186,29.5,118],
	[71,90,132,21.1,84.4],
	]
# 加权系数选择
UPPER = [2,1,1] # 靠背
MIDDLE = [1,1,0] # 坐垫
LOWER = [0,0,0] # 地板
# 轴加权系数
UPPER_k = [0.8,0.5,0.4] # 靠背
MIDDLE_k = [1,1,1] # 坐垫
LOWER_k = [0.25,0.25,0.4] # 地板

def glyphscript(engineState):
	hi_in = engineState.GetInputHistogram(0)
	meta_out = engineState.GetOutputMetaData(0)
	list1,list2 = getHI(hi_in)
	engineState.JournalOut('{}'.format(list1[0]))

	delta_n = list2[0]['XBinSize']
	engineState.JournalOut('{}'.format(delta_n))

	av = ride_xyz_cal(list1,delta_n,'upper')
	engineState.JournalOut('{}'.format(av))

	# tsin2 = engineState.GetInputTimeSeries(0)
	# tsout = engineState.GetOutputTimeSeries(0)
	# putTS(tsout,tsin2,list1)

	return ''


def getHI(hiobj):
	# 获取 频域数据 数据
	# 二维数据(通道,数据)
	# 转化为列表导出

	num = hiobj.GetChannelCount()
	list1 = []
	list2 = []
	for n in range(num):
		listtemp = []
		temp = hiobj.GetMatrix (n)
		dic1 = temp.GetAttributes()
		xnum = dic1['XBinCount']
		for x in range(xnum):
			listtemp.append(temp.GetXBin(x))
		list1.append(listtemp)
		list2.append(dic1)

	return list1,list2

def ride_xyz_cal(list1,dh,acctype):
	'''
		输入三向加速、频率间隔、加速度位置
		指定list1 顺序为 x、y、z
		输出该点加权加速度
	'''

	x,y,z = list1
	
	if acctype.lower() == 'upper':
		ax = ride_single_cal(x,dh)[UPPER[0]]**2 * UPPER_k[0]**2
		ay = ride_single_cal(y,dh)[UPPER[1]]**2 * UPPER_k[1]**2
		az = ride_single_cal(z,dh)[UPPER[2]]**2 * UPPER_k[2]**2
	elif acctype.lower() == 'middle':
		ax = ride_single_cal(x,dh)[MIDDLE[0]]**2 * MIDDLE_k[0]**2
		ay = ride_single_cal(y,dh)[MIDDLE[1]]**2 * MIDDLE_k[1]**2
		az = ride_single_cal(z,dh)[MIDDLE[2]]**2 * MIDDLE_k[2]**2
	elif acctype.lower() == 'lower':
		ax = ride_single_cal(x,dh)[LOWER[0]]**2 * LOWER_k[0]**2
		ay = ride_single_cal(y,dh)[LOWER[1]]**2 * LOWER_k[1]**2
		az = ride_single_cal(z,dh)[LOWER[2]]**2 * LOWER_k[2]**2

	av = (ax+ay+az)**0.5

	return av

def ride_single_cal(list1,dh):
	'''
		输入加速度数据
		输出三向加速度 加权

	'''
	ajs = []
	ajks ,ajds , ajcs = [],[],[]
	for line in RIDE:
		lower = round(line[0]/dh)
		upper = round(line[1]/dh)
		if lower == upper:
			values = []
		else:
			values = list1[int(lower):int(upper)]
		if values:
			aj = (sum(values)*dh)**0.5
			ajk = (aj*line[2]/1000)**2
			ajd = (aj*line[3]/1000)**2
			ajc = (aj*line[4]/1000)**2
			ajs.append(aj)
			ajks.append(ajk)
			ajds.append(ajd)
			ajcs.append(ajc)
	awk = sum(ajks)**0.5
	awd = sum(ajds)**0.5
	awc = sum(ajcs)**0.5

	# print(awk)
	# print(awd)
	# print(awc)
	# print(len(ajs))
	return [awk,awd,awc]

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