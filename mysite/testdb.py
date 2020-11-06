# -*- coding: utf-8 -*-

from django.http import HttpResponse

from myapp.models import day


from django.shortcuts import render

from django.views.decorators.http import require_http_methods

from django.core import serializers

from django.http import JsonResponse
import csv
from django.db.models import Max
import pymysql
import json
#数据库处理的库
import pandas as pd
import pymysql.cursors
#
from django.http import HttpResponse

from myapp.models import day

from strategy.models import strategy,strategy_code,day_table


@require_http_methods(["GET"])

def testdb1(request):#
    # 初始化
    response = ""
    response1 =""
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    # list = day.objects.all()
    list = day.objects.order_by("-index")[:200]
    # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response2 = Test.objects.filter(id=1)
    #
    # # 获取单个对象
    # response3 = Test.objects.get(id=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    # Test.objects.order_by('name')[0:2]
    # # 数据排序
    # Test.objects.order_by("id")
    #
    # # 上面的方法可以连锁使用
    # Test.objects.filter(name="runoob").order_by("id")

    # 输出所有数据
    i = 200
    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + ' \"x\": \"' + str(i) + '\", \"y\":\"' + var.close + '\"},'
        i -= 1
        # response1 += var.high + " "
    # print(response3)
    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1


    out2 = json.loads(response)
    return JsonResponse(out2)

@require_http_methods(["GET"])
#接收参数，新建策略
def add_strategy(request):

    msg = request.GET.get('msg')
    
    #print(msg[2])
    test=msg.split(",")
    test1 = strategy(strategy_name=test[2],strategy_train_start=test[3],strategy_train_end=test[4],
                     strategy_verify_start=test[5],strategy_verify_end=test[6],strategy_vol_start=test[7],strategy_vol_end=test[8],
                     strategy_amo_start=test[9],strategy_amo_end=test[10],strategy_Model_choose=test[11],strategy_epoch_num_choose=test[12],if_high=test[13],if_low=test[14],if_open=test[15],if_amo=test[16],if_vol=test[17],MSE=-1,strategy_state="未训练")
    test1.save()
    #------------------
    #填充strategy_code
    list = day_table.objects.filter(
        day_avg_amo != "N/A" & day_avg_amo > test[9] & day_avg_amo < test[10] & day_avg_vol < test[8],
        day_avg_vol > test[7])
    for var in list:
        test2=strategy_code(strategy_name=test[2],Code_ID=var.day_Code,pre_close="",mse="")
        test2.save()
    enter_start()

    return JsonResponse({'data': msg})

#查看符合股票
@require_http_methods(["GET"])
def return_Code(request):
    strategy_amo_start = request.GET.get('strategy_amo_start')
    strategy_amo_end = request.GET.get('strategy_amo_end')
    strategy_vol_end = request.GET.get('strategy_vol_end')
    strategy_vol_start = request.GET.get('strategy_vol_start')

    #接收strategy_vol_start=test[7],strategy_vol_end=test[8],strategy_amo_start=test[9],strategy_amo_end=test[10]
    list = day_table.objects.filter(day_avg_amo__gt=strategy_amo_start , day_avg_vol__gt=strategy_vol_start).filter(day_avg_amo__lt=strategy_amo_end , day_avg_vol__lt=strategy_vol_end)

    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + ' \"day_Code\": \"' + var.day_Code + '\",\"day_avg_vol\": \"' + var.day_avg_vol + '\", \"day_avg_amo\":\"' + var.day_avg_amo + '\"},'

        # response1 += var.high + " "
    # print(response3)
    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1

    out2 = json.loads(response)
    return JsonResponse(out2)

#接收策略名返回策略详情
@require_http_methods(["GET"])
def get_strategy(request):

    #接收strategy_vol_start=test[7],strategy_vol_end=test[8],strategy_amo_start=test[9],strategy_amo_end=test[10]
    name = request.GET.get('name')
    list =strategy.objects.filter(strategy_name=name)

    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + '\"strategy_name\": \"' + var.strategy_name +'\" ,\"strategy_train_start\": \"' + var.strategy_train_start +'\", \"strategy_train_end\": \"' + var.strategy_train_end +\
                    '\" ,\"strategy_verify_start\": \"' + var.strategy_verify_start +'\" ,\"strategy_verify_end\": \"' + var.strategy_verify_end +'\" ,\"strategy_vol_start\": \"' + var.strategy_vol_start +\
                    '\", \"strategy_vol_end\": \"' + var.strategy_vol_end +'\", \"strategy_amo_start\": \"' + var.strategy_amo_start+'\" ,\"strategy_amo_end\": \"' + var.strategy_amo_end +\
                    '\" ,\"strategy_Model_choose\": \"'
        if var.strategy_Model_choose==1:
            response1=response1+'cnn模型'
        elif var.strategy_Model_choose==2:
            response1 = response1 + 'bp模型'
        response1=response1+'\" ,\"strategy_epoch_num_choose\": \"'
        if var.strategy_epoch_num_choose == 1:
            response1 = response1 + '500次'
        elif var.strategy_epoch_num_choose == 2:
            response1 = response1 + '750次'
        elif var.strategy_epoch_num_choose == 3:
            response1 = response1 + '1000次'
        response1 = response1 +'\", \"MSE\": \"' + str(var.MSE) +'\",\"strategy_state\": \"'+var.strategy_state +'\",'
        response1 = response1 +  '\"if_high\": '
        if var.if_high==1:
            response1=response1+'\"high\",'
        else:
            response1 = response1 + '\" \",'
        response1=response1+'\"if_low\": '
        if var.if_low==1:
            response1=response1+'\"low\",'
        else:
            response1 = response1 + '\" \",'
        response1 = response1 +'\"if_open\": '
        if var.if_open==1:
            response1=response1+'\"open\",'
        else:
            response1 = response1 + '\" \",'
        response1 = response1  +'\"if_vol\": '
        if var.if_vol == 1:
            response1 = response1 + '\"vol\",'
        else:
            response1 = response1 + '\" \",'
        response1 = response1 +'\"if_amo\": '
        if var.if_amo == 1:
            response1 = response1 + '\"amo\"'
        else:
            response1 = response1 + '\" \"'




        response1=response1+'},'





    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1

    out2 = json.loads(response)
    return JsonResponse(out2)

#接收策略名，将策略状态改为训练中
@require_http_methods(["GET"])
def update_state(request):
    name = request.GET.get('name')
    list = strategy.objects.filter(strategy_name=name)
    for i in list:
        if i.strategy_state == "未训练":
            # 状态改为训练中
            i.strategy_state = "训练中"
            i.save()

            #开始训练

    list = day.objects.order_by("-index")[:200]
    i = 200
    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + ' \"x\": \"' + str(i) + '\", \"y\":\"' + var.close + '\"},'
        i -= 1
        # response1 += var.high + " "
    # print(response3)
    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1

    out2 = json.loads(response)
    return JsonResponse(out2)

    #查询是否为正在训练状态，若是则修改为训练中状态，调用计算mse函数

#返回所有策略名
@require_http_methods(["GET"])
def get_strategy_name(request):
    list = strategy.objects.all()
    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + '\"strategy_name\": \"' + var.strategy_name  + '\"},'

        # response1 += var.high + " "
    # print(response3)
    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1

    out2 = json.loads(response)
    return JsonResponse(out2)
#返回结果
@require_http_methods(["GET"])
def get_result(request):
    name = request.GET.get('name')
    list = strategy_code.objects.filter(strategy_name=name)
    response1 = '{ \"data\":['
    for var in list:
        response1 = response1 + "{" + '\"Code_ID\": \"' + var.Code_ID  +  '\",\"open_start\": \"' + var.open_start  +    '\",\"pre_value\": \"' + var.pre_close  +   '\",\"Difference\": \"' + str(float(var.pre_close)-float(var.open_start))  +  '\",\"mse\": \"' + var.mse+             '\" },'

        # response1 += var.high + " "
    # print(response3)
    response1 = response1[:-1]
    response1 = response1 + "]}"
    response = response1

    out2 = json.loads(response)
    return JsonResponse(out2)



#训练

def train_start(name):
    #查数据库多少种股票符合该策略
    list= strategy_code.objects.filter(strategy_name=name)
    for i in list:


        list1 = strategy.objects.get(strategy_name=i.strategy_name)
        train(i.Code_ID,list1.strategy_train_start,list1.strategy_train_end,list1.strategy_verify_start,list1.strategy_verify_end,
              list1.strategy_Model_choose,list1.strategy_epoch_num_choose,list1.if_open,list1.if_high,list1.if_low,list1.if_vol,list1.if_amo)


        #查

        # get训练集
        # get验证集
        #训练
        #填mse和pre_close


def enter_start():
    list=strategy_code.objects.all()
    for i in list:
        db = pymysql.Connect(host="139.9.169.15", port=3306, user="huawei", password="123456", db='huawei',
                             charset='utf8')  # 建立链接
        sql = "select open from " + i.Code_ID + " where `index`='2017-01-01'"
        a = pd.read_sql(sql, db)
        for k in a.open:
            x = strategy_code(id=i.id, open_start=k)
            x.save()
