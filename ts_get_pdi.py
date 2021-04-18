# -*- coding: utf-8 -*-
# 读取PDI计算结果 MetaData
import logging
import os
current_path = r'D:\github\pyncode'
os.chdir(current_path)
with open('debug.log','w') as f : pass
logging.basicConfig(level=logging.INFO, filename='debug.log')


def glyphscript(engineState):
	
	md_obj_in0 = engineState.GetInputMetaData(0)
	chantitles, damages, intercepts, slopes, test_name = get_pdi_metadata(md_obj_in0)

	logging.shutdown()
	return ''


def get_pdi_metadata(md_obj):
	md_obj_in0 = md_obj
	
	num = md_obj_in0.GetChannelCount(0)
	logging.info('num: {}'.format(num))

	chantitles, damages, intercepts, slopes = [], [], [], []
	for n in range(num):
		
		chantitle = md_obj_in0.GetChanTitle(n)
		chantitles.append(chantitle)
		
		damage = md_obj_in0.GetItem(n, 'Damage')
		damages.append(damage)

		intercept = md_obj_in0.GetItem(n, 'Intercept')
		intercepts.append(intercept)
		slope = md_obj_in0.GetItem(n, 'Slope')
		slopes.append(slope)

		logging.info('chantitle: {} ; damage: {}'.format(chantitle,damage))

	test_name = md_obj_in0.GetItem(-1, 'TestName')
	logging.info('TestName:{}'.format(test_name))

	return chantitles, damages, intercepts, slopes, test_name
