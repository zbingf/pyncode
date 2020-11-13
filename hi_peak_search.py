# -*- coding: utf-8 -*-
# python 2.7
# 频域计算
def glyphscript(engineState):
	# 输出打印 子函数

	vprint = lambda value : engineState.JournalOut(str(value))

	pro_dic = engineState.GetPropertySet().GetProperties()
	csv_path =pro_dic['A_CSV_PATH']
	search_dis = int(pro_dic['A_SEARCH_DIS'])
	hz_dis = pro_dic['A_HZ_DIS']
	
	# 读取输入数据
	HI_in1 = engineState.GetInputHistogram(0)
	nlen = HI_in1.GetChannelCount()
	xs,ys = hi_get_data(HI_in1)

	# 波峰取值
	target_x,target_y = [],[]
	for x,y in zip(xs,ys):
		nx,ny,temp = peak_find(x,y,distance=search_dis,xdistance=hz_dis)
		tx,ty = sorted_xy(nx,ny)
		target_x.append(tx)
		target_y.append(ty)

	# 写入数据
	f = open(csv_path,'w')
	str1 = '{},,,'.join([HI_in1.GetChanTitle(n) for n in range(nlen)]) + '\n'
	f.write(str1)
	str1 = 'Hz,,,'*nlen + '\n'
	f.write(str1)
	for n1 in ragne(len(target_x[0])):
		for n2 in ragne(len(target_x)):
			try:
				str1 = '{},{},,'.format(
					str(target_x[n2][n1],
					str(target_y[n2][n1])))
			except:
				str1 = ' , , ,'
			f.write(str1)
		f.write('\n')
	f.close()

	# 打开csv文件
	import os
	os.system(csv_path)
	return ''

def hi_get_data(HIobj):
	'''
		获取 频域信号 数据
	'''
	nlen = HIobj.GetChannelCount()
	xs,ys = [],[]
	for loc in range(nlen):

		matrix1 = HIobj.GetMatrix(loc)
		dic1 = matrix1.GetAttributes()
		xlen = dic1['XBinCount']
		xstart = dic1['XMin']
		xend = dic1['XMax']

		xs.append([(float(xend-xstart)/float(xlen-1)*nnum) for num in range(xlen)])
		ys.append([matrix1.GetXBin(num) for num in range(xlen)])

	return xs,ys

# 子函数
list2str = lambda list1: ','.join([str(n) for n in list1])

def sorted_xy(xlist,ylist):
	'''从小到大排序'''
	dic1 = {x:y for x,y in zip(xlist,ylist)}
	# 排序
	x = sorted(dic1, key=lambda x:dic1[x], reverse=True)
	y = [dic1[xn] for xn in x]
	return x,y

def json_write(values):
	'''Json 记录'''
	json_path = r'text.txt'
	import json
	with open(json_path,'w') as f:
		json.dump(values,f)

	return True

def diff(list1):
	'''
		列表数值 差分 
		后一位减前一位
	'''
	return [list1[n+1]-list1[n] for n in range(len(list1)-1)]

def listloc(list1,locs):
	'''获取指定位置列表数据'''
	return [list1[n] for n in locs]

def data_peak_find(list1,distance = 2)
	'''
		使用三点数据对列表进行检索 ,返回潜在波峰位置
		当前：寻找波峰
		可用于：查找波峰、波谷
		list1 数据段 y
		distance 数据点间隔，默认2 
	'''
	list_loc = []
	for d in range((len(list1)-(distance*2))):
		up = d
		mid = d+distance
		down = d+distance*2
		# j1 = (list1[up]>list1[mid])*(list1[down]>list1[mid]) # 波谷寻找
		j2 = (list1[up]<list1[mid])*(list1[down]<list1[mid]) # 波峰寻找

		if j2:
			list_loc.append(mid)
	return list_loc

def peak_find(xlist,ylist,distance=2,xdistance=2):
	'''波峰寻找'''
	list_loc = data_peak_find(ylist,distance=distance)
	new_xlist = listloc(xlist,list_loc)
	diff_x = diff(new_xlist)
	nlens = []
	for it in range(100):
		nlens.append(len(diff_x))
		loc0 = []
		num = 0
		jump = False
		for n in range(len(diff_x)):
			if jump:
				jump = False
				continue
			if diff_x[n] < xdistance:
				# 间距国小
				if ylist[list_loc[n+1]] - ylist[list_loc[n]] >0:
					# 后一位大于前一位 删除前一位
					loc0.append(n)
				else:
					loc0.append(n+1)
				num += 1
				jump = True
		for n in sorted(loc0,reverse=True):
			del list_loc[n]

		if num == 0:
			break

		new_xlist = listloc(xlist,list_loc)
		diff_x = diff(new_xlist)
	new_ylist = listloc(ylist,list_loc)
	
	return new_xlist,new_ylist,nlens
