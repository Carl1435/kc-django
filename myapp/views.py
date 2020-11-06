
from django.shortcuts import render

from django.views.decorators.http import require_http_methods

from django.core import serializers

from django.http import JsonResponse
import csv
import urllib.parse
import pymysql
import json
#数据库处理的库
import pandas as pd
import pymysql.cursors
import re
#
from django.http import HttpResponse
import MySQLdb
#from myapp.models import day
# from strategy.models import day_table
import heapq

import xlrd
from datetime import datetime
from datetime import timedelta
import time
# Create your views here.

import numpy as np

import numpy as np

@require_http_methods(["GET"])
def add_zd(request):
    month=request.GET.get('month')
    day=request.GET.get('day')
    hour=request.GET.get('hour')
    mymin=request.GET.get('min')
    year=request.GET.get('year')
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    upnum=0
    downnum=0
    nonum=0
    dm=[]
    zdf=[]
    zf=[]
    vol=[]
    new=[]
    lb=[]
    detail=[0,0,0,0,0,0,0,0,0,0,0]
    i2=0
    for i1 in table_list:
        # i2+=1
        # if(i2>20):
        #     break
        name=i1
        if name[0:2]!='day':
            continue
        if name=='min000062':
            break
        sql='SELECT * FROM '+name+' WHERE `index`=\"'+year+'-'+month+'-'+day+'\"'
        #a=pd.read_sql(sql,db) 
        cursor.execute(sql)   
        data = cursor.fetchone()
        # json1=a.to_json(orient ='split', force_ascii = False)#转化为json字符串
        # json2=json.loads(json1)#转化为json对象
        if(data is None):
            continue
        close1=data[1]
        
        name=name.replace('day','min')
        sql='SELECT * FROM '+name+' WHERE time=\''+year+'-'+month+'-'+day+' '+hour+':'+mymin+':00\''
        cursor.execute(sql)   
        data2 = cursor.fetchone()
        if(data2 is None):
            continue
        close2=data2[1]
        high=data2[3]
        low=data2[4]
        amo=data2[6]
        cha=float(close2)-float(close1)
        zdf.append(round(cha*100/float(close1),2))
        cha2=float(high)-float(low)
        zf.append(round(cha2*100/float(close1),3))#round(cha2*100/float(close1),3)
        vol.append(float(data[6]))
        new.append(round(float(close2),2))
        dm.append(name.replace('min',''))
        close1=float(close1)
        if cha>0:
            upnum+=1
            if cha/close1<0.03:
                detail[6]+=1
            elif cha/close1<0.05:
                detail[7]+=1
            elif cha/close1<0.07:
                detail[8]+=1
            elif cha/close1<0.1:
                detail[9]+=1
            elif cha/close1>=0.1:
                detail[10]+=1
        elif cha<0:
            downnum+=1
            if cha/close1>-0.03:
                detail[1]+=1
            elif cha/close1>-0.05:
                detail[2]+=1
            elif cha/close1>-0.07:
                detail[3]+=1
            elif cha/close1>-0.1:
                detail[4]+=1
            elif cha/close1<=-0.1:
                detail[0]+=1
        else:
            nonum+=1
            detail[5]+=1
    mystr=''
    mystr=mystr+getstr(dm,zdf,new,1,zdf)
    mystr=mystr+getstr(dm,zdf,new,0,zdf)
    mystr=mystr+getstr(dm,zf,new,1,zdf)
    mystr=mystr+getstr(dm,vol,new,1,zdf)
    mystr=mystr[:-1]
    response='{\"data\":['+str(max(detail))+','+str(upnum)+','+str(downnum)+','+str(nonum)#str(max(detail))
    for i in detail:
        response=response+','+str(i)
    response=response+'],'
    response=response+'\"data2\":['+mystr+']}'
    out2=json.loads(response)
    return JsonResponse(out2)
def getstr(list1,list2,list3,judge,list4):
    mystr=''
    if(judge==1):
        index=list(map(list2.index, heapq.nlargest(3, list2)))
        for i in index:
            mystr=mystr+'[\"'+list1[i]+'\"'+','+'\"'+str(list1[i])+'\"'+','+str(list3[i])+','+str(list2[i])+','
            if list4[i]>0:
                mystr=mystr+'1],'
            elif list4[i]==0:
                mystr=mystr+'2],'
            else:
                mystr=mystr+'3],'
    else:
        index=list(map(list2.index, heapq.nsmallest(3, list2)))
        for i in index:
            mystr=mystr+'[\"'+str(list1[i])+'\"'+','+'\"'+str(list1[i])+'\"'+','+str(list3[i])+','+str(list2[i])+','
            if list4[i]>0:
                mystr=mystr+'1],'
            elif list4[i]==0:
                mystr=mystr+'2],'
            else:
                mystr=mystr+'3],'
    return mystr
@require_http_methods(["GET"])
def add_datamain(request):
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )
    name="沪深A股"
    cursor = db.cursor()
    sql='SELECT * FROM '+name
    cursor.execute(sql)   
    data = cursor.fetchall()
    upnum=0
    downnum=0
    nonum=0
    detail=[0,0,0,0,0,0,0,0,0,0,0]
    num=-1
    data=list(data)
    for i in data:
        num+=1
        data[num]=list(data[num])
        i=list(i)
        if '-' in i:
            for i2 in range(len(i)):
                if((i[i2]=='-')|(i[i2]=='-%')):
                        data[num][i2]=0
            if(data[num][4]!=0):
                data[num][4]=float(data[num][4][:-1])
            if(data[num][8]!=0):
                data[num][8]=float(data[num][8][:-1])
            data[num][7]=float(data[num][7])
            data[num][13]=float(data[num][13])
            continue
        else:
            data[num][4]=float(i[4][:-1])
            data[num][8]=float(i[8][:-1])
        data[num][7]=float(i[7])
        data[num][13]=float(i[13])
        cha=float(data[num][4])/100
        if cha>0:
            upnum+=1
            if cha<0.03:
                detail[6]+=1
            elif cha<0.05:
                detail[7]+=1
            elif cha<0.07:
                detail[8]+=1
            elif cha<0.1:
                detail[9]+=1
            elif cha>=0.1:
                detail[10]+=1
        elif cha<0:
            downnum+=1
            if cha>-0.03:
                detail[4]+=1
            elif cha>-0.05:
                detail[3]+=1
            elif cha>-0.07:
                detail[2]+=1
            elif cha>-0.1:
                detail[1]+=1
            elif cha<=-0.1:
                detail[0]+=1
        else:
            nonum+=1
            detail[5]+=1
    response='{\"data\":['+str(max(detail))+','+str(upnum)+','+str(downnum)+','+str(nonum)#str(max(detail))
    for i in detail:
        response=response+','+str(i)
    response=response+'],'
    data=sorted(data,key=lambda x: x[4],reverse=True)
    mystr=''
    mystr+=addstr(data,4)
    data=sorted(data,key=lambda x: x[4],reverse=False)
    mystr+=addstr(data,4)
    data=sorted(data,key=lambda x: x[8],reverse=True)
    mystr+=addstr(data,8)
    data=sorted(data,key=lambda x: x[7],reverse=True)
    mystr+=addstr(data,7)
    data=sorted(data,key=lambda x: x[13],reverse=True)
    mystr+=addstr(data,13)
    response=response+'\"data2\":['+mystr[:-1]+']}'
    #print(response)
    out2=json.loads(response)
    return JsonResponse(out2,safe=False)

def addstr(data,num):
    stradd=''
    for i in range(3):
        if(data[i][4]>0):
            stradd+='["'+str(data[i][1])+'",'+'\"'+str(data[i][2])+'\",'+''+str(data[i][3])+','+''+str(data[i][num])+',1],'
        elif(data[i][4]<0):
            stradd+='["'+str(data[i][1])+'",'+'\"'+str(data[i][2])+'\",'+''+str(data[i][3])+','+''+str(data[i][num])+',0],'
    return stradd
@require_http_methods(["GET"])
def add_zxzs(request):#沪深指数折线
    kind=request.GET.get('kind')
    if kind=='0':
        name='上证指数'
    elif kind=='1':
        name='深圳指数'
    else:
        pass
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql='SELECT * FROM '+name
    cursor.execute(sql)
    data2 = cursor.fetchall()
    str1="["
    str2="["
    str3="["
    for i in data2:
        str1+="["+str(i[0])+","+str(i[2])+"],"
        str2+="["+str(i[0])+","+str(i[3])+"],"
        str3+="["+str(i[0])+","+str(i[4])+"],"
    str1=str1[:-1]
    str2=str2[:-1]
    str3=str3[:-1]
    str1+=']'
    str2+=']'
    str3+=']'
    response='{\"data1\":'+str1+",\"data2\":"+str2+",\"data3\":"+str3+',\"data4\":['
    sql='SELECT * FROM '+name+" order by price"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[2])+','
    sql='SELECT * FROM '+name+" order by vol"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[3])+',' 
    sql='SELECT * FROM '+name+" order by unknow"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[4])+','
    sql='SELECT * FROM '+name+" order by price desc"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[2])+','
    sql='SELECT * FROM '+name+" order by vol desc"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[3])+','
    sql='SELECT * FROM '+name+" order by unknow desc"
    cursor.execute(sql)
    data2=cursor.fetchone()
    response+=str(data2[4])+"]}"
    print(response)
    out2=json.loads(response)
    return JsonResponse(out2)
@require_http_methods(["GET"])
def js_hsb(request):#红三兵
    daystart=request.GET.get('start')
    dayfin=request.GET.get('fin')
    zq_kind=int(request.GET.get('zq_kind'))#1,7,30
    zq_long=int(request.GET.get('zq_long'))#1,2,3,4,5
    # daystart='2010-01-05'
    # dayfin='2011-06-09'
    # zq_kind=1
    # zq_long=5
    mystr='['
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    order=0
    for i1 in table_list:
        if (i1[0:3]!='day'):
            continue
        elif(i1[0:3]=='min'):
            break
        if(i1=='day000011'):
            break
        order+=1
        cost=0
        earn=[0,0,0,0,0]
        sql="select * from "+i1+" where `index` between \'"+daystart+"\' and \'"+dayfin+"\'"
        cursor.execute(sql)   
        data = cursor.fetchall()
        zd=[]
        for i in data:
            zd.append(int(i[1]<i[2]))
        for i in range((len(zd)-8)):
            if(j_hsb(zd,i,data,zq_kind,zq_long)):
                if(len(zd)>i+7+zq_kind*zq_long):#在要判断的周期内
                    cost+=float(data[i+7][1])
                    for i2 in range(zq_long):
                        earn[i2]+=float(data[i+7+(i2+1)*zq_kind][2])
        mystr=mystr+"["+"\""+i1+"\""+','+"\""+i1+"\""+','+str(order)+','
        if(cost==0):
            for i in range(7):
                mystr=mystr+"\"-\","
            mystr=mystr[:-1]
        else:
            sum=0
            for i in range(6):
                if i<zq_long:
                    num=round((earn[i]-cost)*100/cost,2)
                    mystr=mystr+str(num)+","
                    sum+=earn[i]
                else:
                    mystr=mystr+"\"-\","
            mystr=mystr+str(round((sum-cost*zq_long)/(cost*zq_long)*100,2))
        mystr=mystr+'],'
    mystr=mystr[:-1]
    mystr=mystr+']'
    out2=json.loads(mystr)
    return JsonResponse(out2,safe=False)
def j_hsb(zd,i,data,zq_kind,zq_long):
    judge=(zd[i]+zd[i+1]+zd[i+2]+zd[i+3]+zd[i+4])<=2
    judge=judge and zd[i+5]==1 and zd[i+6]==1 and zd[i+7]==1#连涨3天
    maxlist=[]
    for i2 in range(5):
        if zd[i+i2]==0:
            maxlist.append(data[i+i2][3])
    judge=judge and (float(data[i+7][5])>float(max(maxlist)))
    return judge
@require_http_methods(["GET"])
def add_stockdetail(request):
    name=request.GET.get('name')
    day=request.GET.get('day')
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    table1=''
    while(table1==None or table1==''):
        sql = "select * from "+name+" where `index` = \'"+day+"\' "
        cursor.execute(sql)
        table1 = cursor.fetchone()
        day=date_add(day)
    day2=date_add(day,-10)
    table2=''
    sql="select * from "+name+" where `index` between \'"+day2+"\' and \'"+day+"\'"
    cursor.execute(sql)   
    table2= cursor.fetchall()
    print(table2[len(table2)-3])
    str="["
    for i in table1[1:]:
        str=str+i+','
    str+=table2[len(table2)-3][2]+']'
    out2=json.loads(str)
    return JsonResponse(out2,safe=False)
def date_add(date_str, days_count=1):#实现日期加一
    date_list = time.strptime(date_str, "%Y-%m-%d")
    y, m, d = date_list[:3]
    delta = timedelta(days=days_count)
    date_result = datetime(y, m, d) + delta
    date_result = date_result.strftime("%Y-%m-%d")
    return date_result
@require_http_methods(["GET"])
def add_stockdayK(request):#
    daystart=request.GET.get('start')
    dayfin=request.GET.get('fin')
    name=request.GET.get('name')
    kind=request.GET.get('kind')
    # daystart='2014-05-06'
    # dayfin='2015-05-06'
    # name='day000001'
    # kind='365'
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql="select * from "+name+" where `index` between \'"+daystart+"\' and \'"+dayfin+"\'"
    cursor.execute(sql)   
    data = cursor.fetchall()
    str1='['
    order=0
    high=[]
    low=[]
    date_list = time.strptime(data[0][0], "%Y-%m-%d")
    y0,mo,d0=date_list[:3]
    w0=date_list[6]
    open=data[0][1]
    if(kind=='1'):
        for i in data:
            str2='['+'\"'+i[0]+'\"'+','+i[1]+','+i[2]+','+i[3]+','+i[4]+'],'
            str1+=str2
    elif(kind=='7'):
        for i in data:
            date_list = time.strptime(i[0], "%Y-%m-%d")
            high.append(i[3])
            low.append(i[4])
            if(date_list[6]<w0):
                str2='['+'\"'+i0[0]+'\"'+','+open+','+i0[2]+','+max(high)+','+min(low)+'],'
                str1+=str2
                high=[]
                low=[]
                open=i[1]
            w0=date_list[6]
            i0=i
    elif(kind=='30'):
        for i in data:
            date_list = time.strptime(i[0], "%Y-%m-%d")
            high.append(i[3])
            low.append(i[4])
            if(date_list[1]!=mo):
                str2='['+'\"'+i0[0]+'\"'+','+open+','+i0[2]+','+max(high)+','+min(low)+'],'
                str1+=str2
                mo=date_list[1]
                high=[]
                low=[]
                open=i[1]
            i0=i
    elif(kind=='91'):
        for i in data:
            date_list = time.strptime(i[0], "%Y-%m-%d")
            high.append(i[3])
            low.append(i[4])
            if(date_list[1] in [1,4,7,10] and date_list[2]==1):
                str2='['+'\"'+i[0]+'\"'+','+open+','+i[2]+','+max(high)+','+min(low)+'],'
                str1+=str2
                open=i[1]
                high=[]
                low=[]
    elif(kind=='365'):
        for i in data:
            date_list = time.strptime(i[0], "%Y-%m-%d")
            high.append(i[3])
            low.append(i[4])
            if(date_list[0]!=y0):
                str2='['+'\"'+i0[0]+'\"'+','+open+','+i0[2]+','+max(high)+','+min(low)+'],'
                str1+=str2
                y0=date_list[0]
                high=[]
                low=[]
                open=i[1]
            i0=i
    str1=str1[:-1]
    str1+=']'
    out2=json.loads(str1)
    return JsonResponse(out2,safe=False)
@require_http_methods(["GET"])
def enter(request):#登录注册功能
    kind=request.GET.get('kind')
    name=request.GET.get('name')
    password=request.GET.get('password')
    db = pymysql.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )
    cursor = db.cursor()
    if kind=='1':
        sql="SELECT * FROM user WHERE name ='"+name+"'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==0:
            sql='INSERT INTO user (name,password) values('+name+','+password+')'
            cursor.execute(sql)
            db.commit()
            restr='注册成功'
        else:
            restr='已存在'
    elif kind=='2':
        sql="SELECT * FROM user WHERE name='"+name+"'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==0:
            restr='无此用户'
        else:
            if data[0][2]==password:
                restr='登录成功'
            else:
                restr="密码错误"
    cursor.close()
    db.close()
    restr='["'+restr+'"]'
    out2=json.loads(restr) 
    return JsonResponse(out2,safe=False)
@require_http_methods(["GET"])
def js_hsb_code(request):#红三兵
    daystart=request.GET.get('start')
    dayfin=request.GET.get('fin')
    zq_kind=int(request.GET.get('zq_kind'))#1,7,30
    zq_long=int(request.GET.get('zq_long'))#1,2,3,4,5
    code=request.GET.get('stock')
    # daystart='2010-01-05'
    # dayfin='2011-06-09'
    # zq_kind=1
    # zq_long=5
    mystr='['
    order=1
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql="select * from day"+code+" where `index` between \'"+daystart+"\' and \'"+dayfin+"\'"
    cursor.execute(sql)   
    data = cursor.fetchall()
    zd=[]
    for i in data:
        zd.append(int(i[1]<i[2]))
    for i in range((len(zd)-8)):
        if(j_hsb(zd,i,data,zq_kind,zq_long)):
            if(len(zd)>i+4+zq_kind*zq_long):
                sum=0
                mystr+="[\""+code+"\",\""+code+"\","+str(order)+","
                order+=1
                for i2 in range(6):
                    if(i2<zq_long):
                        earn=float(data[i+7+(i2+1)*zq_kind][2])
                        cost=float(data[i+7][1])
                        num=round((earn-cost)*100/cost,2)
                        sum+=num
                        mystr+=str(num)+','
                    else:
                        mystr+="\"-\","
                mystr=mystr+str(round(sum/zq_long,2))+",\""+data[i+5][0]+'\"],'
    mystr=mystr[:-1]+']'
    out2=json.loads(mystr)
    return JsonResponse(out2,safe=False)
@require_http_methods(["GET"])
def add_business(request):
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql="select * from 行业排行 limit 6"
    cursor.execute(sql)   
    data = cursor.fetchall()
    mystr="["
    for i in range(len(data)):
        mystr+="[["+data[i][7]+",0,"+data[i][8]+"],[\""+data[i][1]+"\",\""+data[i][2]+"%\"],[\""+data[i][3]+"\",\""+data[i][4]+"%\"]],"
    mystr=mystr[:-1]+"]"
    out2=json.loads(mystr)
    return JsonResponse(out2,safe=False)
@require_http_methods(["GET"])
def bk_stockdata(request):
    kind=int(request.GET.get('kind'))
    kind2=int(request.GET.get('kind2'))
    bk=request.GET.get('bk_name')
    bk=str(bk)
    bk=urllib.parse.unquote(bk)
    bus1=["沪深A股","B股","上证A股","深证A股","中小板","创业版","科创板"]
    bus2=['hy','gn','dy']
    if bk=="所有板块":
        bk=""
    name1=bus1[kind-1]
    name2=bus2[kind2-1]
    db = MySQLdb.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )#建立链接
    cursor = db.cursor()
    sql="select code,abbreviation,ZXJ,ZD,ZDF from "+name1+" where "+name2+" like '%"+bk+"%'"
    cursor.execute(sql)   
    data = cursor.fetchall()
    mystr=data.__str__()
    mystr=mystr.replace("(","[")
    mystr=mystr.replace(")","]")
    mystr=mystr.replace("'","\"")
    out2=json.loads(mystr)
    return JsonResponse(out2,safe=False)