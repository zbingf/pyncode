"""
	关联py:
		ts_data_compare_output.py

	对比数据,生成pdf

	读取json数据:
		主参数
		main_dic = {
			csv_path0 : str
			csv_path1 : str
			pdi_dic0 : {
				slope 		: [float, float, ...]
				rms 		: [float, float, ...]
				intercept	: [float, float, ...]
				min 		: [float, float, ...]
				max 		: [float, float, ...]
				damage 		: [float, float, ...]
				testname 	: str
				chantitle 	: [str, str, ...]
				samplerate 	: [float, float, ...]
				block_size 	: int
				hz_range 	: [0, 50]
			}
			pdi_dic1 : { ... }
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
# json_path = r'D:\github\pyncode\ts_data_compare_output_main.json'
docx_path = json_path[:-4]+'docx'
figpath = json_path[:-5]

# json读取
with open(json_path, "r") as f:
	main_dic = json.load(f)


csv_path0 	= main_dic['csv_path0']
csv_path1 	= main_dic['csv_path1']
pdi_dic0 	= main_dic['pdi_dic0']
pdi_dic1 	= main_dic['pdi_dic1']

block_size 	= [pdi_dic0['block_size'],pdi_dic1['block_size']]
hz_range 	= pdi_dic0['hz_range']

logging.info(f'{main_dic}')

data0,titles0 = csv2data(csv_path0, isTitle=True)
data1,titles1 = csv2data(csv_path1, isTitle=True)

logging.info('line {}'.format(len(data0[0])))
logging.info('len {}'.format(len(data0)))
logging.info('titles0 {}'.format(len(titles0)))

fig_paths = plot.plot_ts_hz(data0, data1, samplerate=[pdi_dic0['samplerate'][0], pdi_dic1['samplerate'][0]], 
	block_size=block_size,
	res_x=None, target_x=None, ylabels=None, xlabel=None,
	nums=[1,1], figpath=figpath, isShow=None, isHzPlot=True, isTsPlot=True, 
	hz_range=hz_range, legend=[pdi_dic0['testname'], pdi_dic1['testname']], size_gain=0.6)

line_hz_set = f'\tPSD 设置 :\n\t\thz_range [{hz_range[0]},{hz_range[1]}] , block_size [{block_size[0]},{block_size[1]}]'


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#	word 编写
obj = office_docx.DataDocx(docx_path)

line_title = 'A({}) vs. B({}) '
title = line_title.format(pdi_dic0['testname'], pdi_dic1['testname'])

obj.add_heading(title, level=0, size=20)
obj.add_heading('数据对比', level=1, size=15)

list_title = ['chantitle','damage','max','min','rms']

# 汇总表格
list_compare = []
for loc in range(len(pdi_dic1['chantitle'])):
	# 表格
	list_0 	= copy.deepcopy(list_title)
	list_1 	= [pdi_dic0[key][loc] for key in list_title]
	list_2 	= [pdi_dic1[key][loc] for key in list_title]
	list_3 	= ['A / B']
	for value_a, value_b in zip(list_1[1:], list_2[1:]):
		list_3.append( value_a / value_b )
	list_compare.append(list_3)

for loc in range(len(list_compare)):
	list_compare[loc][0] = pdi_dic0['chantitle'][loc]

obj.add_table(f'相对比例-汇总 A/B', value2str_list2([list_title]+list_compare,3))
obj.add_page_break()

for loc in range(len(pdi_dic1['chantitle'])):
	
	obj.add_list_bullet('A : '+pdi_dic0['chantitle'][loc], size=14)
	# 时域图
	obj.add_docx_figure(fig_paths[loc], f'时域图 {loc+1}', width=17)
	# 频域图
	obj.add_docx_figure(fig_paths[loc+len(pdi_dic1['chantitle'])], f'频域图 {loc+1}', width=17)
	# 另起一页
	obj.add_page_break()
	# 注释
	obj.add_paragraph(
		'设置:'
		)
	line_pdi_set = '\t{} :\n\t\tsamplerate 采样频率 {} Hz\n\t\tPDI设置: slope斜率 {} , intercept截距 {}'
	obj.add_paragraph(
		line_pdi_set.format(pdi_dic0['chantitle'][loc],pdi_dic0['samplerate'][loc],pdi_dic0['slope'][loc],pdi_dic0['intercept'][loc])
		)
	obj.add_paragraph(
		line_pdi_set.format(pdi_dic1['chantitle'][loc],pdi_dic1['samplerate'][loc],pdi_dic1['slope'][loc],pdi_dic1['intercept'][loc])
		)
	obj.add_paragraph(line_hz_set)

	# 表格
	list_0 	= copy.deepcopy(list_title)
	list_1 	= [pdi_dic0[key][loc] for key in list_title]
	list_2 	= [pdi_dic1[key][loc] for key in list_title]
	list_1[0] = 'A:'+list_1[0]
	list_2[0] = 'B:'+list_2[0]
	list_3 	= ['A / B']
	for value_a, value_b in zip(list_1[1:], list_2[1:]):
		list_3.append( value_a / value_b )

	str_list 	= [list_0, list_1, list_2, list_3]
	
	obj.add_table(f'表格{loc+1}', value2str_list2(str_list,3))

	# 另起一页
	obj.add_page_break()

obj.save()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# 转存PDF
office_docx.doc2pdf(docx_path)
os.system(docx_path[:-4]+'pdf')

# 删除多余文档
del_paths = fig_paths+[json_path, csv_path0, csv_path1]
for path in del_paths:
	del_file(path)
	logging.info(f'del : {path}')


logging.info('End')
logging.shutdown()