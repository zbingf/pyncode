# -*- coding: utf-8 -*-
# python 2.7

import logging

"""
Ncode API

MultiColumn GetInputMultiColumn(padIndex)
MultiColumn GetOutputMultiColumn(padIndex)


MultiColumn

integer GetChannelCount()
integer GetChanNumber(chanIndex)
integer GetChanIndex(chanNumber)
string GetChanTitle(chanIndex)
integer GetTableCount(chanIndex)
MultiColumnTable GetTable(chanIndex, tableIndex)
SetChannelCount(numChans)
SetChanNumber(chanIndex, chanNumber)
SetChanTitle(chanIndex, title)
SetTableCount(chanIndex, tablecount)
SetTableCountFixedLength(chanIndex, tablecount)
CopyMetaData(sourceMultiColumn, sourceChanIndex, targetChanIndex)
MetaData GetMetaData()


MultiColumnTable

integer GetColumnCount()
integer GetRowCount()
string GetColKeyword(colIndex)
string GetColTitle(colIndex)
string GetColUnits(colIndex)
string GetColType(colIndex)
GetColHasStatus(colIndex)
dictionary GetColEnumValues(colIndex)
dictionary GetColStatusBitText(colIndex)
value GetValue(colIndex, rowIndex)
integer GetValues(colIndex, startRowIndex, numRows, buffer)
list GetValuesAsList(colIndex, startRowIndex, numRows)
integer GetStatusValue(colIndex, rowIndex)
integer GetStatusValues(colIndex, startRowIndex, numRows, buffer)
list GetStatusValuesAsList(colIndex, startRowIndex, numRows)
SetRowCount(numRows)
AddColumn(type, title, units, keyword, statusInUse)
AddEnumColumn(title, keyword, statusInUse, enumOpts)
SetColStatusBitText(colIndex, bitText)
PutValue(colIndex, rowIndex, value)
PutValues(colIndex, startRowIndex, numRows, buffer)
PutStatusValue(colIndex, rowIndex, value)
PutStatusValues(colIndex, startRowIndex, numRows, buffer)

"""

# import logging
# log_path = 'mc_test.log'
# with open(log_path,'w') as f : pass
# logging.basicConfig(level=logging.INFO, filename=log_path)

# import sys
# sys.path.append(r'D:\github\pyncode')

# import mc_template
# reload(mc_template)

# def glyphscript(engineState):
	
# 	mc_in1  = engineState.GetInputMultiColumn(0)
# 	mc_out1 = engineState.GetOutputMultiColumn(0)
	
# 	mc_template.mc_copy(mc_out1, mc_in1)
	
# 	mc_template.mc_add_mc(mc_out1,mc_out1,5)
# 	mc_template.mc_add(mc_out1, 5, 1e-6)
# 	mc_template.mc_multiply(mc_out1, 5, 2)
# 	mc_template.mc_sub_mc(mc_out1, mc_out1, 5)
	
# 	return ''




def mct_copy(mct_obj, mct_tarobj):
	# MultiColumnTable 数据复制

	logger = logging.getLogger('mct_copy')

	n_col = mct_tarobj.GetColumnCount()
	n_row = mct_tarobj.GetRowCount()
	for n in range(n_col):
		col_key 	= mct_tarobj.GetColKeyword(n)
		col_title 	= mct_tarobj.GetColTitle(n)
		col_units 	= mct_tarobj.GetColUnits(n)
		col_type 	= mct_tarobj.GetColType(n)
		col_status 	= mct_tarobj.GetColStatusBitText(n)
		col_enum_values = mct_tarobj.GetColEnumValues(n)
		list_value 	= mct_tarobj.GetValuesAsList(n, 0, n_row)
		if col_status:
			list_status = mct_tarobj.GetStatusValuesAsList(n, 0, n_row)
			logging.info('list_status:{}'.format(list_status[0:10]))

		if col_type == 'Enum':
			logging.info('col_type is Enum')
			if not col_status:
				mct_obj.AddEnumColumn(col_title, col_key, False, col_enum_values)
			else:
				mct_obj.AddEnumColumn(col_title, col_key, True, col_enum_values)
		else:
			if not col_status:
				logging.info('col_status is empty')
				mct_obj.AddColumn(col_type, col_title, col_units, col_key, False)
			else:
				mct_obj.AddColumn(col_type, col_title, col_units, col_key, True)
		logger.info(list_value)
		# 数据复制
		for num, value in enumerate(list_value):
			mct_obj.PutValue(n, num, value)

		if col_status: # 状态更新
			mct_obj.SetColStatusBitText(n, col_status)
			for num, value in enumerate(list_status):
				mct_obj.PutStatusValue(n, num, value)

		logger.info('col_key:' 		+ col_key)
		logger.info('col_title:'	+ col_title)
		logger.info('col_units:' 	+ col_units)
		logger.info('col_type:' 	+ col_type)
		logger.info('col_status:{}'.format(col_status))
		logger.info('col_enum_values:{}'.format(col_enum_values))
		logger.info('list_value:{}'.format(list_value[0:10]))
		logger.info('n:{}'.format(n))

	return mct_obj

def mc_copy(mc_obj, mc_tarobj):
	# MultiColumn 数据复制
	logger = logging.getLogger('mc_copy')

	mct_tarobj = mc_tarobj.GetTable(0, 0)

	mc_obj.SetChannelCount(1)
	mc_obj.SetChanNumber(0, 1)
	mc_obj.SetChanTitle(0, 'result')
	mc_obj.SetTableCount(0, 1)
	mct_obj = mc_obj.GetTable(0, 0)

	logger.info('copy MultiColumnTable')
	mct_obj = mct_copy(mct_obj, mct_tarobj)

	logger.info('copy MetaData')
	mc_obj.CopyMetaData(mc_tarobj, -1, -1)
	mc_obj.CopyMetaData(mc_tarobj, 0, 0)

	return mc_obj

def mc_multiply(mc_obj, n_loc, gain):
	# MultiColumn 乘以常数
	list1 = mc_get_data(mc_obj, n_loc)
	for n, v1 in enumerate(list1):
		list1[n] *= gain
	mc_set_data(mc_obj, n_loc, list1)

	return None

def mc_add(mc_obj, n_loc, gain):
	# MultiColumn 加上 常数
	
	list1 = mc_get_data(mc_obj, n_loc)
	for n, v1 in enumerate(list1):
		list1[n] += gain
	mc_set_data(mc_obj, n_loc, list1)

	return None

def mc_add_mc(mc_obj, mc_tarobj, n_loc):
	# MultiColumn 相加 并赋值 mc_obj

	list1 = mc_get_data(mc_obj, n_loc)
	list2 = mc_get_data(mc_tarobj, n_loc)
	for n, v2 in enumerate(list2):
		list1[n] += v2
	mc_set_data(mc_obj, n_loc, list1)

	return None

def mc_sub_mc(mc_obj, mc_tarobj, n_loc):
	# MultiColumn 相加 并赋值 mc_obj

	list1 = mc_get_data(mc_obj, n_loc)
	list2 = mc_get_data(mc_tarobj, n_loc)
	for n, v2 in enumerate(list2):
		list1[n] -= v2
	mc_set_data(mc_obj, n_loc, list1)

	return None

def mc_get_data(mc_obj, n_loc):
	# 获取 value 数据

	mct_obj = mc_obj.GetTable(0, 0)
	n_row 	= mct_obj.GetRowCount()
	list1 	= mct_obj.GetValuesAsList(n_loc, 0, n_row)

	return list1

def mc_set_data(mc_obj, n_loc, list1):
	# 赋值 value 数据

	mct_obj = mc_obj.GetTable(0, 0)
	for num, value in enumerate(list1):
		mct_obj.PutValue(n_loc, num, value)

	return None


