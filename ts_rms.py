# coding:utf-8
# python 2.7
# 导入时序计算模块
from ts_fun import *
def ts_cal(engineState):
	tsin1 = engineState.GetInputTimeSeries(0)
	tsin2 = engineState.GetInputTimeSeries(1)

	tsout1 = engineState.GetOutputTimeSeries(0)

	list1 = getTS(tsin1)
	list2 = getTS(tsin2)

	putTS(tsout1,tsin1,list1)

