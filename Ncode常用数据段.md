# Ncode 2018

## python版本2.7

+ Ncode 数据转换程序调用
```
asciitranslate.exe -h

asciitranslate.exe /inp="D:\207_447.csv" /conv="TimeSeries" /SetupFile="D:\207_447.ats" /prog=1

asciitranslate.exe
ailibr.dll
utlibr.dll
qtutilr.dll

```
+ ats文件格式
``` 

<AsciiTranslateSetup>
   <Version>1</Version>
   <ConvertTo>1</ConvertTo>
   <CreateLogFile>0</CreateLogFile>
   <NumberOfHeaderLines>1</NumberOfHeaderLines>
   <NumberOfChannels>-1</NumberOfChannels>
   <LineNumberForChannelTitles>1</LineNumberForChannelTitles>
   <LineNumberForUnits>0</LineNumberForUnits>
   <TabSeparated>0</TabSeparated>
   <CommaSeparated>1</CommaSeparated>
   <SpaceSeparated>0</SpaceSeparated>
   <SemiColonSeparated>0</SemiColonSeparated>
   <FixedWidth>0</FixedWidth>
   <DecimalCharacter>1</DecimalCharacter>
   <IncludeExclude>0</IncludeExclude>
   <ColumnList></ColumnList>
   <HeaderToMetadata>0</HeaderToMetadata>
   <AutoDetectSampleRate>0</AutoDetectSampleRate>
   <SampleRate>512</SampleRate>            # 采样频率
   <XaxisBase>0</XaxisBase>
   <XaxisTitle>Time</XaxisTitle>
   <XaxisUnits>Seconds</XaxisUnits>
   <OutputNamingMethod>2</OutputNamingMethod>
   <OutputTestName>207_447</OutputTestName>
   <OutputNamingText></OutputNamingText>   # 文件名输入 [前缀\后缀\...]
   <OutputFormat>3</OutputFormat>
</AsciiTranslateSetup>

```


```python
ATS_RSP = """<AsciiTranslateSetup>
   <Version>1</Version>
   <ConvertTo>1</ConvertTo>
   <CreateLogFile>0</CreateLogFile>
   <NumberOfHeaderLines>1</NumberOfHeaderLines>
   <NumberOfChannels>-1</NumberOfChannels>
   <LineNumberForChannelTitles>1</LineNumberForChannelTitles>
   <LineNumberForUnits>0</LineNumberForUnits>
   <TabSeparated>0</TabSeparated>
   <CommaSeparated>1</CommaSeparated>
   <SpaceSeparated>0</SpaceSeparated>
   <SemiColonSeparated>0</SemiColonSeparated>
   <FixedWidth>0</FixedWidth>
   <DecimalCharacter>1</DecimalCharacter>
   <IncludeExclude>0</IncludeExclude>
   <ColumnList></ColumnList>
   <HeaderToMetadata>0</HeaderToMetadata>
   <AutoDetectSampleRate>0</AutoDetectSampleRate>
   <SampleRate>#SampleRate#</SampleRate>
   <XaxisBase>0</XaxisBase>
   <XaxisTitle>Time</XaxisTitle>
   <XaxisUnits>Seconds</XaxisUnits>
   <OutputNamingMethod>2</OutputNamingMethod>
   <OutputTestName>temp</OutputTestName>
   <OutputNamingText></OutputNamingText>
   <OutputFormat>3</OutputFormat>
</AsciiTranslateSetup>
"""
def translate_data_rsp(csv_path, samplerate):

    ats_path = 'RSP_1V1.ats'
    with open(ats_path, 'w') as f:
        f.write(ATS_RSP.replace('#SampleRate#', str(samplerate)))
    ats_path = os.path.abspath(ats_path)

    str_cmd = 'asciitranslate.exe /inp="{}" /conv="TimeSeries" /SetupFile="{}" /prog=1'.format(csv_path, ats_path)
    # os.system(str_cmd)
    with open('_test.bat', 'w') as f:
        f.write(str_cmd)
    os.system('_test.bat')    

    pass
    return None

```







+ 表头
```python
# -*- coding: utf-8 -*-
```


+ 时域列表获取 
  + getTS(tsobj)
  + getTS_channel_name(tsobj)
  + putTS(tsobj,tartsobj,list1)


```python
def getTS(tsobj):
    num = tsobj.GetChannelCount()
    list1 = []
    for n in range(num):
        listnum = tsobj.GetPointCount(n)
        list_temp = tsobj.GetValuesAsList(n, 0, listnum)
        list1.append(list_temp)
    return list1

def getTS_channel_name(tsobj):
    num = tsobj.GetChannelCount()
    list1 = []
    for n in range(num):
        list1.append(tsobj.GetChanTitle(n))
    return list1


def getTS_file_path(tsobj):

    meta_obj = tsobj.GetMetaData()

    return meta_obj.GetItem(0, "InputTestInfo.Path")

def getTS_file_name(tsobj):

    meta_obj = tsobj.GetMetaData()

    return meta_obj.GetItem(0, "InputTestInfo.TestName")

def getTS_samplerate(tsobj):

    meta_obj = tsobj.GetMetaData()
    
    return meta_obj.GetItem(0, "Attributes.SampleRate")


#获取\赋值时序信号数据
def putTS(tsobj,tartsobj,list1):
    # 对时间序列进行赋值
    # 复制tartsobj属性 到 tsobj中
    # 将列表list1 作为数据 导入 tsobj中
    import array
    num = len(list1)
    md_obj1 = tsobj.GetMetaData()
    md_obj2 = tartsobj.GetMetaData()
    
    if type(list1[0]) == list :
        tsobj.SetChannelCount(num)
        len_value = len(list1[0])
        for n in range(num):
            tsobj.CopyAttributes(tartsobj,n,n)
            tsobj.CopyMetaData(tartsobj, n, n)
            tsobj.SetPointCount(n,len_value)
            arr1 = array.array('f',list1[n])
            tsobj.PutValues(n,0,len_value,arr1)
    else:
        tsobj.SetChannelCount(1)
        tsobj.CopyAttributes(tartsobj,0,0)
        tsobj.CopyMetaData(tartsobj, 0, 0)
        tsobj.PutValues(0,num,1,list1)

    a = md_obj2.GetItem(-1, 'TestName')
    md_obj1.SetItem(-1, 'InputTestInfo', 'TestName', 'string', a)
    
    
    tsobj.SetXTitle(tartsobj.GetXTitle())
    tsobj.SetXUnits(tartsobj.GetXUnits())




```





+ 导出CSV数据
  + output_csv_data(file_path, data, titles)

```python
def output_csv_data(file_path, data, titles):

    f = open(file_path, 'w')
    f.write(','.join(titles) + '\n')
    for row in range(len(data[0])):
        for col in range(len(data)):
            f.write(str(data[col][row]) + ',')
        f.write('\n')

    f.close()
    return None
```



+ PDI 伪损伤计算[雨流计数] 
  + cal_rainflow_pdi(list2d, b=5000.0, k=-5.0)

```python

def cal_pdi(list1, b=5000.0, k=-5.0):

    import math

    A = math.log10(b)
    B = 1.0/k

    damage = [ sum( [ 1.0/10.0**((math.log10(abs(n))-A)/B) for n in line if n!=0 ] ) for line in list1]

    return damage


def cal_rainflow_pdi(list2d, b=5000.0, k=-5.0):
    
    new_list2d = []
    for line in list2d:
        try:
            values, means = rainflow_3point(line)
        except:
            values, means = [0.0], [0.0]

        values = [2*n for n in values] 
        new_list2d.append(values)

    return cal_pdi(new_list2d, b, k)

def rainflow_3point(list1):
    newlist = _list_updown(list1)
    num = len(newlist)
    value_max = max(newlist)
    value_loc = newlist.index(value_max)
    l1 = newlist[value_loc:] + newlist[:value_loc+1]
    newlist = _list_updown(l1)
    values, means, rainlist = [],[],[]
    num = len(newlist)
    count = 1
    last_num = 0
    while num > 1:
        if num >1 :
            last_num = len(newlist)
            for n in range(num-2):
                s1 = newlist[n]-newlist[n+1]
                s2 = newlist[n+2]-newlist[n+1]
                e3 = (newlist[n]+newlist[n+1])/2.0
                if s1 > 0 and s2 > 0 and s1 <= s2:
                    values.append(s1/2.0)
                    means.append(e3)
                    del newlist[n+1]
                    del newlist[n]
                    break
        num = len(newlist)
        if last_num == num :
            newlist = _list_updown(newlist)
    return values,means

def _list_updown(list1):
    
    num = len(list1)
    l1 = list1
    l2 = copy.copy(list1)
    for n in range(1,num-1):
        if l1[n-1] < l1[n] and l1[n] < l1[n+1]:
            l2[n] = ''
        elif l1[n-1] > l1[n] and l1[n] > l1[n+1]:
            l2[n] = ''
        elif l1[n-1] == l1[n]:
            l2[n] = ''
    if l2[-2] == l2[-1]:
        l2[-2] = ''
    newlist = [n for n in l2 if n]
    num = len(newlist)
    return newlist

```







