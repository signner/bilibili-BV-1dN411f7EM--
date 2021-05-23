import requests#需要安装requests模块，详情百度pip安装
import json#下面会用到
import xlsxwriter
import math
import time
from jsonpath import jsonpath
from datetime import datetime
import sched
import time

# 初始化sched模块的 scheduler 类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)

# 默认参数60s
def main(inc=60):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, execPy, (inc,))
    schedule.run()
    
def execPy(inc):
    _pn=1
    _ps=10
    _size=1
    url='https://api.bilibili.com/x/v2/reply/reply?pn='+str(_pn)+'&type=1&oid=502970935&ps='+str(_ps)+'&root=4532333218&_=1621744010556'
    _json=requests.get(url)#这里返回的json数据

    workbook = xlsxwriter.Workbook('school.xlsx')#建立文件
    worksheet = workbook.add_worksheet('school') # 建立sheet
    #worksheet.write('school') 
    worksheet.write(0,0,'序号')
    worksheet.write(0,1,'mid')
    worksheet.write(0,2,'用户')
    worksheet.write(0,3,'等级')
    worksheet.write(0,4,'时间')
    worksheet.write(0,5,'评论')

    _jsonTxt=json.loads(_json.text)
    _page=jsonpath(_jsonTxt,'$..page')
    #print(_page[0].get('count'))
    _pages=math.ceil(_page[0].get('count')/_page[0].get('size'))
    #print(_pages)
    for i in range(_pages):
        _pn=i+1
        url='https://api.bilibili.com/x/v2/reply/reply?pn='+str(_pn)+'&type=1&oid=502970935&ps='+str(_ps)+'&root=4532333218&_=1621744010556'
        _json=requests.get(url)#这里返回的json数据
        _jsonTxt=json.loads(_json.text)
        _replies=jsonpath(_jsonTxt,'$..replies')
        print(len(_replies[0]))
        _i=i
        for i, val in enumerate(_replies[0]):
            print("序号：%s" %(str(_i*_ps+i+1)))
            member=val['member']
            print("mid：%s" %member['mid'])
            print("用户：%s" %member['uname'])
            level=member['level_info']
            print("等级：%s" %level['current_level'])
            print("评论：%s" %val['content']['message'])
            print("时间：%s" %time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(val['ctime'])))
            f1=str.find(val['content']['message'],"学校")!=-1
            f2=str.find(val['content']['message'],"学院")!=-1
            f3=str.find(val['content']['message'],"教育")!=-1
            f4=str.find(val['content']['message'],"职业")!=-1
            if f1 or f2 or f3 or f4:
                worksheet.write(_size,0,str(_i*_ps+i+1))
                worksheet.write(_size,1,member['mid'])
                worksheet.write(_size,2,member['uname'])
                worksheet.write(_size,3,level['current_level'])
                worksheet.write(_size,4,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(val['ctime'])))
                worksheet.write(_size,5,val['content']['message'])
                _size=_size+1
                
    schedule.enter(inc, 0, execPy, (inc,))
    workbook.close()
    print("===============>  over")


main(40)
