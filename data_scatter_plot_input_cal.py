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
from pyadams.file import office_docx, pdf_scatter_plot

import importlib
importlib.reload(logging)

with open('data_scatter_plot_input_cal.log', 'w') as f : pass
logging.basicConfig(level=logging.INFO, filename='data_scatter_plot_input_cal.log')

logger = logging.getLogger('data_scatter_plot_input_cal')

#  运行
json_path = sys.argv[1]
# json_path = r'D:\github\pyncode\ts_data_scatter_plot_output.json'
docx_path = json_path[:-4]+'docx'
# figpath = json_path[:-5]

# json读取
with open(json_path, "r") as f:
	main_dic = json.load(f)

logger.info(f'load json_path : {json_path}')

csv_path0 	= main_dic['csv_path0']
csv_path1 	= main_dic['csv_path1']
ts_dic0 	= main_dic['ts_dic0']
ts_dic1 	= main_dic['ts_dic1']

pdf_path = pdf_scatter_plot.pdf_scatter_plot(csv_path0, csv_path1, docx_path)
logger.info(f'load pdf_path: {pdf_path}')
os.system(pdf_path)

logger.info('End')
logger.shutdown()
