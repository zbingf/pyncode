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
from pyadams.file import office_docx, pdf_compare_pdi, file_edit

import importlib
importlib.reload(logging)

with open('data_compare_input_cal.log', 'w') as f : pass
logging.basicConfig(level=logging.INFO, filename='data_compare_input_cal.log')


logger = logging.getLogger('data_compare_input_cal')

#  运行
json_path = sys.argv[1]
# json_path = r'D:\github\pyncode\ts_data_compare_output_main.json'
docx_path = json_path[:-4]+'docx'
fig_path = json_path[:-5]

# json读取
with open(json_path, "r") as f:
	main_dic = json.load(f)

logger.info(f'load json_path : {json_path}')

csv_path0 	= main_dic['csv_path0']
csv_path1 	= main_dic['csv_path1']
pdi_dic0 	= main_dic['pdi_dic0']
pdi_dic1 	= main_dic['pdi_dic1']

pdf_path = pdf_compare_pdi.pdf_compare_pdi_csv(csv_path0, csv_path1, pdi_dic0, pdi_dic1, docx_path, fig_path)

logger.info(f'load pdf_path : {pdf_path}')
os.system(pdf_path)
logger.info(f'End')
logging.shutdown()
