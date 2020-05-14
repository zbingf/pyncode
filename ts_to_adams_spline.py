# -*- coding: utf-8 -*-
# python 2.7

SPLINE_EDIT = '''
data_element modify spline &
 spline=.{}.{} &
 x={} &
 y={} &
 linear_extrapolate=no &
 units=no_units &
 comments=""
'''

SPLINE_CREATE = '''
data_element create spline &
 spline=.{}.{} &
 x={} &
 y={} &
 linear_extrapolate=no &
 units=no_units &
 comments=""
'''



def cmd_spline_edit(modal_name,spline_name,xlist,ylist):
	'''
		生成cmd命令
		编辑 adams 中的 spline曲线
	'''
	if modal_name[0] == '.':
		modal_name = modal_name[1:]
	if spline_name[0] == '.':
		spline_name = spline_name[1:]
	xstr = translate_list(xlist)
	ystr = translate_list(ylist)
	str1 = SPLINE_EDIT.format(modal_name,spline_name,xstr,ystr)
	return str1

def cmd_spline_create(modal_name,spline_name,xlist,ylist):
	'''
		生成cmd命令
		创建 adams 中的 spline曲线
	'''
	if modal_name[0] == '.':
		modal_name = modal_name[1:]
	if spline_name[0] == '.':
		spline_name = spline_name[1:]
	xstr = translate_list(xlist)
	ystr = translate_list(ylist)
	str1 = SPLINE_CREATE.format(modal_name,spline_name,xstr,ystr)
	return str1

def translate_list(lines):
	str1 = ', '.join([str(n) for n in lines])
	return str1
