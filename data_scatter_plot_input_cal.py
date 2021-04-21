"""
	关联py:
		ts_data_scatter_plot_output.py

	对比数据,生成pdf

	散点图生成

	读取json数据:
		主参数
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
import logging
import sys
import json
import re
import os
import copy
from pyadams.datacal import plot
from pyadams.file import office_docx

import importlib
importlib.reload(logging)

with open('data_compare_input_cal.log', 'w') as f : pass
logging.basicConfig(level=logging.INFO, filename='data_compare_input_cal.log')

strlower = lambda st1: re.sub(r'\s','',st1).lower()

# csv读取
def csv2data(csv_path,isTitle=True): 
	"""
		csv_path 	目标csv路径
		isTitle

		data 	list(list) 		二维数组
	"""
	f = open(csv_path,'r')
	with open(csv_path,'r') as f:
		filestr = f.read()
	
	if not isTitle:
		titles = None

	list1 = []
	for loc, line in enumerate(filestr.split('\n')):
		
		if isTitle:
			titles = line.split(',')
			isTitle = False
			continue

		line = strlower(line)
		if line:
			line = [float(value) for value in line.split(',') if value]
			list1.append(line)

	new_list1 = []
	for n0 in range(len(list1[0])):
		line = []
		for n1 in range(len(list1)):
			line.append(list1[n1][n0])
		new_list1.append(line)

	return new_list1,titles

# 数值转化
def value2str_list2(data, nlen=2):
	new_data = []
	for line in data:
		new_line = []
		for value in line:
			if isinstance(value,float):
				if abs(value) < 10**(-(nlen+1)):
					temp = '{' + ':.{}e'.format(nlen) + '}'
					value = temp.format(value)
				else:
					value = round(value,nlen)
			new_line.append(str(value))
		new_data.append(new_line)

	return new_data

# 删除指定文件
def del_file(filepath): 
	try:
		os.remove(filepath)
		return True
	except:
		return False


#  运行
json_path = sys.argv[1]
# json_path = r'D:\github\pyncode\ts_data_scatter_plot_output.json'
docx_path = json_path[:-4]+'docx'
figpath = json_path[:-5]

# json读取
with open(json_path, "r") as f:
	main_dic = json.load(f)

csv_path0 	= main_dic['csv_path0']
csv_path1 	= main_dic['csv_path1']
ts_dic0 	= main_dic['ts_dic0']
ts_dic1 	= main_dic['ts_dic1']

xs,titles_x = csv2data(csv_path0, isTitle=True)
ys,titles_y = csv2data(csv_path1, isTitle=True)

figpaths_list = []
for x, title_x in zip(xs, titles_x):
	figpath = title_x
	figpaths = plot.scatter_ts_single([x]*len(titles_y), ys, [title_x]*len(titles_y), titles_y, 
		figpath=figpath, nums=[1,1], isShow=False, size_gain=0.8, isGrid=True, 
		linewidths=0.5, scatter_s=15)
	figpaths_list.append(figpaths)

logging.info(f'main_dic : {main_dic}')
logging.info(f'titles_x : {titles_x}')
logging.info(f'titles_y : {titles_y}')
logging.info(f'figpaths_list : {figpaths_list}')

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#	word 编写
obj = office_docx.DataDocx(docx_path)
obj.set_page_margin(x=1, y=1)
for num, title_x in enumerate(titles_x):

	for loc in range(len(titles_y)):
		if divmod(loc, 2)[1] == 0 :
			obj.add_heading('X: '+title_x, level=0, size=15)

		obj.add_list_bullet('Y: '+titles_y[loc], size=12)
		
		# 散点图添加
		obj.add_docx_figure(figpaths_list[num][loc], width=16)
		
		# 另起一页
		if divmod(loc, 2)[1] == 1:
			obj.add_page_break()

	if divmod(len(titles_y), 2)[1] == 1 :
		if len(titles_x)-1 !=num:
			obj.add_page_break()

obj.save()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# 转存PDF
logging.info('doc 2 pdf')
office_docx.doc2pdf(docx_path)
os.system(docx_path[:-4]+'pdf')

del_paths = []
for figpaths in figpaths_list:
	del_paths += figpaths

# 删除多余文档
del_paths += [json_path, csv_path0, csv_path1]
for path in del_paths:
	del_file(path)
	logging.info(f'del : {path}')

logging.info('End')
logging.shutdown()