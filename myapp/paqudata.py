import re
import pandas as pd
import pymysql.cursors
import json
import requests
from bs4 import BeautifulSoup

def paqu(url,name,headers,col,kind2,rule,kind3):
    html=''
    js=''
    try:
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print(e)
    pat = re.compile(rule)#编译正则表达式，供后面使用
    data = pat.findall(html)
    if(len(data)!=0):
        js = json.loads(data[0])#价格 成交量  
        store(js,name,col,kind2,kind3)
def create(name,col,kind):
    db = pymysql.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS "+name)#如果存在table1表，则删除
    sql = "create table "+name+" ("
    for i in range(len(col)):
        sql+=col[i]+" "+kind[i]+","
    sql=sql[:-1]
    sql+=")"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s"%e)
    db.commit()
    #关闭游标连接
    cursor.close()
    # 关闭数据库连接
    db.close()
def store(js,name,col,kind2,kind3):
    db = pymysql.Connect(host="121.36.213.28", port=3306,user="nanhang", password="NanHang@123456",db='gupiao', charset='utf8' )
    sql = "INSERT INTO "+name+" ("
    col=col[1:]
    for i in col:
        sql+=i+','
    sql=sql[:-1]
    sql+=") VALUES ("
    for i in kind2:
        sql+=i+','
    sql=sql[:-1]
    sql+=")"
    cursor = db.cursor()
    for i in range(len(js)):
        #print(i)
        #print(type(js[i]["f3"]))
        if kind3==0:
            data = (str(js[i]["f12"]),str(js[i]["f14"]),str(js[i]["f2"]),str(js[i]["f3"])+ "%",str(js[i]["f4"]),str(js[i]["f5"]),str(js[i]["f6"]),str(js[i]["f7"])\
                + "%",str(js[i]["f15"]),str(js[i]["f16"]),str(js[i]["f17"]),str(js[i]["f18"]),str(js[i]["f10"]),str(js[i]["f20"]),str(js[i]["f21"]),str(js[i]["f8"]),str(js[i]["f23"]),str(js[i]["f100"]),str(js[i]["f102"]),str(js[i]["f103"]))
        elif kind3==1:
            mylist=js[i].split(",")
            data=(mylist[0],mylist[1],mylist[2],mylist[3])
        elif kind3==2:
            data=(str(js[i]["f14"]),str(js[i]["f3"]),str(js[i]["f128"]),str(js[i]["f136"]),str(js[i]["f207"]),str(js[i]["f222"]),str(js[i]["f104"]),str(js[i]["f105"]))
        cursor.execute(sql % data)
    db.commit()
        #print('成功插入', cursor.rowcount, '条数据')
    #关闭游标连接
    cursor.close()
    # 关闭数据库连接
    db.close()
def main():#沪深A股 上证A股 深证A股 新股 两网及退市 风险警示板 深证AB股比价 B股 深股通 沪股通 科创板 中小板 上证AB股比价
# 中小板
# 创业板
# 科创板
# 沪股通
# 深股通
# B股
# 上证AB股比价
    name=["沪深A股","上证A股","深证A股","新股","两网及退市","风险警示板","深证AB股比价","B股","深股通","沪股通","科创板","中小板","上证AB股比价","创业版"]
    first=["http://21.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240216110963949796_1586611666127&pn=",
    "http://21.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://21.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://21.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://21.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
    "http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124022321672832487538_1594253497034&pn=",
   " http://16.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112409790816440904684_1603363401599&pn="]
    final=["&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,"\
                "f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1586611666172",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,"\
                "f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497053",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80&fields=f1,f2,f3,"\
                "f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497055",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f26&fs=m:0+f:8,m:1+f:8&fields=f1,f2,f3,f4,f5,f6,"\
                "f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497057",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+s:3&fields=f1,f2,f3,f4,f5,f6,f7,f8,"\
                "f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497059",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+f:4,m:1+f:4&fields=f1,f2,f3,f4,"\
                "f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497061",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f199&fs=m:0+b:BK0498&fields=f1,f2,f3,f4,f5,f6,f7,"\
                "f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152,f201,f202,f203,f196,f197,f199,f195,f200&_=1594253497063",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:7,m:1+t:3&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497067",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f26&fs=b:BK0804&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497069",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f26&fs=b:BK0707&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497071",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497073",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:13&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1594253497076",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f199&fs=m:1+b:BK0498&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152,f201,f202,f203,f196,f197,f199,f195,f200&_=1594253497065",
            "&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f100,f102,f103,f128,f136,f115,f152&_=1603363401600",
    ]
    headers={"cookie":"emshistory=%5B%22000001%22%5D; waptgshowtime=2020915; _qddaz=QD.qz9sli.kqi3y5.kdceyk01; HAList=a-sh-605128-N%u6CBF%u6D66%2Cf-0-000300-%u6CAA%u6DF1300%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC;\
            em_hq_fls=js; pgv_pvi=3442557952; qgqp_b_id=b031c07b29c5249d6118553f6cedb2f3; st_si=57971832930159; st_sn=6; st_psi=20200915215800589-113200301321-0685347852; st_asi=delete; st_pvi=35862932584956; st_sp=2020-04-18\
             %2007%3A01%3A14; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fcenter%2Fgridlist.html","user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"}
    col=['id','Code','Abbreviation','ZXJ','ZDF','ZD','Volume','AMO','ZF','max','min','open','ZS','LB','SZ','LTSL','HSL','SXL','hy','dy','gn']
    kind=['int auto_increment primary key','char(10)','char(40)','char(10)','char(20)','char(10)','char(10)','char(15)','char(10)','char(10)','char(10)','char(10)','char(10)','char(10)','char(20)','char(15)','char(10)','char(10)','char(15)','char(15)','char(200)']
    kind2=["'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'"]
    rule="\[\{.*?\}\]"
    for num in range(len(name)):
        if(num!=len(name)-1):
            continue
        print(num)
        create(name[num],col,kind)
        for i in range(1,199):
            url = first[num]+str(i)+final[num]
            paqu(url,name[num],headers,col,kind2,rule,0)
    headers={"Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Cookie":"qgqp_b_id=83eeab554d285b7f842f56e44e158da8; em_hq_fls=js; emshistory=%5B%22000016%22%5D; HAList=a-sz-000526-%u7D2B%u5149%u5B66%u5927%2Ca-sz-000016-%u6DF1%u5EB7%u4F73%uFF21; st_si=72275353693422; st_pvi=41442056734534; st_sp=2020-07-08%2020%3A44%3A27; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=1; st_psi=20200915222533449-113200301321-5326226254; st_asi=delete",
            "Host":"push2.eastmoney.com",
            "Referer":"http://quote.eastmoney.com/center/hszs.html",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    url=["http://push2his.eastmoney.com/api/qt/stock/trends2/get?cb=jQuery112403445053667328133_1600238636345&secid=0.399001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11&fields2=f51%2Cf53%2Cf56%2Cf58&iscr=0&ndays=1&_=1600238636348",
    "http://push2his.eastmoney.com/api/qt/stock/trends2/get?cb=jQuery112403223428306211631_1600238879967&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11&fields2=f51%2Cf53%2Cf56%2Cf58&iscr=0&ndays=1&_=1600238880025"]
    name=['深圳指数','上证指数']
    col=['id','time','price','vol','unknow']
    kind=['int auto_increment primary key','char(20)','float(15,2)','float(15,2)','float(15,2)']
    kind2=["'%s'","'%s'","'%s'","'%s'"]
    rule="\[.*?\]"
    # for num in range(len(name)):
    #     create(name[num],col,kind)
    #     paqu(url[num],name[num],headers,col,kind2,rule,1)
    url=["http://15.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124011952185013251881_1602578457370&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f100,f102,f103,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222&_=1602578457371"]
    name=['行业排行']
    col=["id",'business',"buezdf","highest","hzdf","lowest","lzdf","upnum","downnum"]
    kind=['int auto_increment primary key','char(20)','char(10)','char(20)','char(10)','char(20)','char(10)','char(10)','char(10)']
    kind2=["'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'","'%s'"]
    rule="\[\{.*?\}\]"
    # for num in range(len(name)):
    #     create(name[num],col,kind)
    #     paqu(url[num],name[num],headers,col,kind2,rule,2)
if __name__ == '__main__':
    main()