# -*- coding: utf-8 -*-
# python 2.7
# 20240624

# 根据三点坐标计算平面公式
# 在计算第4点坐标Z4
# 四点分别为 左前,右前,左后,右后
# 坐标:
#   左前,右前 左右对称
#   左后,右后 左右对称

# ======================
# front 前左右间距
wf = 900.0
# rear 后左右间距
wr = 1100.0
# front to rear 前后跨距
l = 1305.0+397.0
# ======================

def glyphscript(engineState):

    tsin1 = engineState.GetInputTimeSeries(0)
    tsout1 = engineState.GetOutputTimeSeries(0)

    list1 = getTS(tsin1)

    FL, FR, RL = list1  # -----------------!!!!!!!!!!

    line = []
    list2 = [line]
    for z1, z2, z3 in zip(FL, FR, RL):
        z4 = calc_z4(z1,z2,z3)
        line.append(z4)

    putTS(tsout1,tsin1,list2)

    return ''

def calc_z4(z1,z2,z3):
    x1,y1 = [0, -0.5*wf]
    x2,y2 = [0, 0.5*wf]
    x3,y3 = [l, -0.5*wr]
    x4,y4 = [l, 0.5*wr]

    A = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
    B = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
    C = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    D = -(A * x1 + B * y1 + C * z1)

    # Ax + By + Cz + D = 0

    z4 = -(A*x4 + B*y4 + D)/C
    return z4

def putTS(tsobj,tartsobj,list1):
    import array
    num = len(list1)
    mdobj = tsobj.GetMetaData()
    tarmdobj = tartsobj.GetMetaData()

    if type(list1[0]) == list :
        tsobj.SetChannelCount(num)
        len_value = len(list1[0])
        for n in range(num):
            tsobj.CopyAttributes(tartsobj, n, n)
            tsobj.CopyMetaData(tartsobj, n, n)
            tsobj.SetPointCount(n, len_value)
            arr1 = array.array('f', list1[n])
            tsobj.PutValues(n, 0, len_value,arr1)
    else:
        tsobj.SetChannelCount(1)
        tsobj.CopyAttributes(tartsobj, 0, 0)
        tsobj.CopyMetaData(tartsobj, 0, 0)
        tsobj.PutValues(0, num, 1, list1)

    name = tarmdobj.GetItem(-1, 'TestName')
    mdobj.SetItem(-1, 'InputTestInfo', 'TestName', 'string', name)

    return None

def getTS(tsobj):
    num = tsobj.GetChannelCount()
    list1 = []
    for n in range(num):
        listnum = tsobj.GetPointCount(n)
        list_temp = tsobj.GetValuesAsList(n,0,listnum)
        list1.append(list_temp)
    return list1
