# 前端页面编辑
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin

from aTravel.UserInfo import UserInfo
from aTravel.UserInfo1 import UserInfo1
from aTravel.dd_yiqun import jdyiqun
from aTravel.reason import generate_coherent_recommendation
from aTravel.sqlsqlit import sqlinfo
import json
from sklearn.neighbors import KNeighborsClassifier
# 用户id
x = [
    [1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
     [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
     [21], [22], [23], [24], [25], [26], [27], [28], [29], [30],
     [31], [32], [33], [34], [35], [36], [37], [38], [39], [40],
     [41], [42], [43], [44], [45], [46], [47], [48], [49], [50],
     [51], [52], [53], [54], [55], [56], [57], [58], [59], [60]
]
# 每个用户喜欢的城市，一一对应，用于预测用户喜欢的城市
y = [
    'beijing', 'beijing', 'beijing', 'beijing', 'beijing',
    'beijing', 'beijing', 'beijing', 'beijing', 'beijing',
    'changsha', 'changsha', 'changsha', 'changsha', 'changsha',
    'changsha', 'changsha', 'changsha', 'changsha', 'changsha',
    'xian', 'xian', 'xian', 'xian', 'xian', 'xian', 'xian', 'xian',
    'xian', 'xian', 'sanya', 'sanya', 'sanya', 'sanya', 'sanya',
    'sanya', 'sanya', 'sanya', 'sanya', 'sanya', 'shanghai',
    'shanghai', 'shanghai', 'shanghai', 'shanghai', 'shanghai',
    'shanghai', 'shanghai', 'shanghai', 'shanghai', 'hangzhou',
    'hangzhou', 'hangzhou', 'hangzhou', 'hangzhou', 'hangzhou',
    'hangzhou', 'hangzhou', 'hangzhou', 'hangzhou'
]


class biginfo:
    city = ''
    num_jd = 0
    num_food = 0
    num_hotle = 0
    play_day = 0
    price = 0
    jdpath = []
    foodpath = []
    hotlepath = []
    datpath = []
    trfic = ''
    bool_food = 1
    his = []
    reason = []


class biginfo1:
    city = ''
    num_jd = 0
    num_food = 0
    num_hotle = 0
    play_day = 0
    price = 0
    jdpath = []
    foodpath = []
    hotlepath = []
    datpath = []
    trfic = ''
    bool_food = 1
    his = []
    reason = []


class search:
    searchinfo = ''


class newuserinfo:
    name=''
    tel=''
    img =''
    id=-1


class quanju:
    play_day =0


# request：http协议，用户通过客户端（如浏览器）输入URL，向服务端发送http请求，服务端处理请求，包装成http响应发送回客户端。
# 客户端接收响应后，根据响应内容（如HTML、图片等）渲染页面，展示给用户。
def reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
    # print(name, pwd)
    # 载入模板，填充上下文，再返回由它生成的 HttpResponse 对象
    return render(request, 'dataTest.html')


# 暂时只能计算同年同月的天数
def days(st, et):
    num1 = int(st[8]) * 10 + int(st[9])
    num2 = int(et[8]) * 10 + int(et[9])
    # print num1,num2
    return num2 - num1


# 推荐系统页面：获取用户需求，根据景点类型和景点评分召回可以推荐的所有景点
# 使用蚁群算法结合需求求解最后得到旅游推荐路径
# 记录最后推荐线路中一共多少景点、所有景点id列表、目的城市、美食数量和美食id列表、
# 酒店数量和酒店id列表、最后开销、游玩天数和每天id、推荐后的多少条线路以及每条线路景点id列表、交通方式
# 一共记录2种推荐结果，为biginfo和biginfo1
def index(request):
    # 如果请求是post方式且有数据
    if request.method == "POST" and request.POST:
        # 获取用户请求数据，城市，人数，游玩天数，预算，交通方式，游玩方式，酒店预算，游玩天数，是否推荐特色菜
        # todo print(request.POST)查看在页面返回的参数
        print(request.POST)
        city = request.POST["city"]
        people = 3
        daytime_unicode = request.POST["post_fields"].encode("utf-8")
        pay = int(request.POST["post_fields[lyys]"])
        traffic = request.POST["post_fields[jcyq]"]
        play_mode = request.POST["post_fields[ycyq]"]
        hotel_price = request.POST["post_fields[jdlc]"]
        play_day = int(request.POST['post_fields'])
        quanju.play_day = play_day
        recommend_food = request.POST["post_fields[ycyq1]"]

        if recommend_food == '推荐特色菜':
            biginfo.bool_food = 1
            biginfo1.bool_food = 1
        else:
            biginfo.bool_food = 0
            biginfo1.bool_food = 0
        if play_mode == "精品游玩":
            play_mode = 1
        else:
            play_mode = 0

        # print("从用户端得到数据", city, people, daytime_unicode, pay, traffic,
        # play_mode, hotel_price, play_day, biginfo.bool_food)

        # 获取用户选择的景点类型，
        # todo 推荐理由根据推荐类型改变
        jd_type_name = request.POST.getlist("post_fields[jqdz][]")
        biginfo.reason = jd_type_name
        biginfo1.reason = jd_type_name
        jd_type = []
        jd_type1 = []
        for type_name in jd_type_name:
            if type_name == "现代风情":
                jd_type.append(1)
            if type_name == "历史风情":
                jd_type.append(2)
            if type_name == "当地特色":
                jd_type.append(3)
            if type_name == "博物馆":
                jd_type.append(4)
            if type_name == "当地动物园":
                jd_type.append(5)
            if type_name == "游乐中心":
                jd_type.append(6)
            if type_name == "历史伟人":
                jd_type.append(7)
            if type_name == "当地公园":
                jd_type.append(8)
            if type_name == "植物园":
                jd_type.append(9)
            if type_name == "国内名校":
                jd_type.append(10)
            if type_name == "购物中心":
                jd_type.append(11)
            if type_name == "当地剧院":
                jd_type.append(12)
            if type_name == "当地古镇":
                jd_type.append(13)
            if type_name == "红色文化":
                jd_type.append(14)
            if type_name == "体育公园":
                jd_type.append(15)
            if type_name == "宗教圣地":
                jd_type.append(16)
        jd_type1 = jd_type
        # 这里有参数需要修改，加入判断路径了
        # 将以上获得的数据传递给userinfo对象
        user_info = UserInfo(city, people, daytime_unicode, pay, traffic, jd_type, int(play_mode))
        # todo 根据游玩方式，选择召回所有要推荐的景点id列表
        user_info.find_id()
        # todo 使用蚁群算法，找到一组由景点id组成的旅游路径
        a = jdyiqun()
        ks = a.ant_colony(user_info)
        h = []

        for index, item in enumerate(ks):
            # 根据多少天，选择多少种推荐结果
            if index < quanju.play_day:
                h.append(item)
        # 记录景点路径
        user_info.day_path = h
        # 所有推荐线路中一共有多少个景点
        biginfo.num_jd = user_info.last_path()
        # print("lucheng",user_info.daypath)
        # print(user_info.foodarry, user_info.hotlelist)
        # print("出行天数", user_info.datytime)
        # print ("预计花费", user_info.pay)

        # todo 推荐结果存储到biginfo
        # 所有符合条件的景点
        biginfo.his = user_info.find_id()
        # 目的城市
        biginfo.city = city
        # 推荐多少种食物
        biginfo.num_food = len(user_info.food_array)
        # 推荐多少种酒店
        biginfo.num_hotle = len(user_info.hotel_array)
        # biginfo.price = user_info.pay + user_info.datytime*500
        # 预算
        biginfo.price = user_info.pay
        # 游玩天数日期id
        biginfo.datpath = []
        for i in range(1, user_info.day_time + 1):
            biginfo.datpath.append(i)
        # 一共玩多少天
        biginfo.play_day = user_info.day_time
        # 经过蚁群推荐后的旅游线路和每个线路的景点id
        biginfo.jdpath = user_info.day_path
        # 推荐食物id列表
        biginfo.foodpath = user_info.food_array
        # 推荐酒店id列表
        biginfo.hotlepath = user_info.hotel_array
        # 出行方式
        biginfo.trfic = user_info.traffic

        shuinfo1 = UserInfo1(city, people, daytime_unicode, pay, traffic, jd_type1, int(play_mode))
        shuinfo1.find_id()
        a1 = jdyiqun()
        ks1 = a.ant_colony(shuinfo1)
        h1 = []

        for index, item in enumerate(ks1):
            if index < quanju.play_day:
                h1.append(item)

        shuinfo1.day_path = h1
        biginfo1.num_jd = shuinfo1.last_path()

        # 推荐结果存储到biginfo1

        biginfo1.city = city
        biginfo1.num_food = len(shuinfo1.food_array)
        biginfo1.num_hotle = len(shuinfo1.hotel_array)
        biginfo1.price = shuinfo1.pay
        biginfo1.datpath = []
        biginfo1.play_day = shuinfo1.day_time
        for i in range(1, shuinfo1.day_time + 1):
            biginfo1.datpath.append(i)
        biginfo1.jdpath = shuinfo1.day_path
        biginfo1.foodpath = shuinfo1.food_array
        biginfo1.hotlepath = shuinfo1.hotel_array
        biginfo1.trfic = user_info.traffic
        print(biginfo.foodpath, biginfo.hotlepath)
        print(biginfo1.foodpath, biginfo1.hotlepath)
        # 转到result2页面处理最终推荐结果
        return HttpResponseRedirect('result2')

    return render(request, 'index.html', locals())


# 结果显示页面：把经过蚁群算法推荐得到的结果传递给html
# 将酒店、美食、景点信息整合好，通过页面展示出来
def result(request):
    # userinfo.playday = days(userinfo.startTime,userinfo.endTime)
    # test1 = Jdinfo.objects.get(city='beijing',id=4)
    # test2 = test1.city
    # return render(request,'result2.html',{'test1':test1,'test2':test2})
    sh = sqlinfo()
    test2 = biginfo.city
    hs = [{}]
    fos = [{}]
    hos = [{}]
    los = [{}]
    # print (hs)

    hs1 = [{}]
    fos1 = [{}]
    hos1 = [{}]
    los1 = [{}]

    # 根据景点类型获得推荐理由，为一连串长文本
    resontence = generate_coherent_recommendation(biginfo.reason)
    # print("*******", resontence)

    # print("我需要的：", biginfo.jdpath)
    a1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    jdintr = str(biginfo.his).replace('[', '').replace(']', '').replace('0', '').replace(',', '')
    fdintr = str(biginfo.foodpath).replace('{', '').replace('}', '').replace(',', '')
    # user_id = newuserinfo.id
    # 每一次推荐，把当前推荐时间、符合该用户的景点、食物写进数据库中作为用户历史数据
    user_id = newuserinfo.id
    sh.write_his(a1, user_id, jdintr, fdintr)

    # 获取结果页面的酒店信息
    cnt = 1
    flag = 1
    for i in biginfo.hotlepath:
        # 获取酒店名称、介绍、图片
        re = sh.find_hoteinfo(i)
        if flag == 1:
            for w in re:
                hos = [{'id': cnt, 'name': w[0], 'intr': w[1], 'img': w[2]}]
            flag = 2
        else:
            for w in re:
                hos.append({'id': cnt, 'name': w[0], 'intr': w[1], 'img': w[2]})
        cnt += 1

    # 获取结果页面的美食信息
    sf = 1
    cnt = 1
    flag = 1
    for i in biginfo.foodpath:
        if sf > 3:
            cnt += 1
            sf = 1
        sh = sqlinfo()
        # 获取美食名称、介绍、图片
        re = sh.find_foodinfo(i)
        if flag == 1:
            for w in re:
                hong = w[1].replace('\\n', '').replace('\\r', '')
                fos = [{'id': cnt, 'name': w[0], 'intr': hong, 'img': w[2]}]
            flag = 2
        else:
            for w in re:
                hong = w[1].replace('\\n', '').replace('\\r', '')
                fos.append({'id': cnt, 'name': w[0], 'intr':hong, 'img': w[2]})
        sf += 1

    # 获取结果页面的景点信息
    cnt = 1
    flag = 1
    kh = 1
    for i in biginfo.jdpath:
        for j in i:
            for k in j:
                if k != 0:
                    sh = sqlinfo()
                    # 获取景点名称、等级、图片、介绍、推荐游玩时间、地址、经纬度、景点特色
                    re = sh.find_jdinfo(k)
                    # http://webapi.amap.com/theme/v1.3/markers/n/mark_b2.png
                    string = 'http://webapi.amap.com/theme/v1.3/markers/n/mark_r.png'
                    # string ='http://amappc.cn-hangzhou.oss-pub.aliyun-inc.com/lbs/static/img/marker.png'
                    print(f"从数据库提取的景点数据re是{re}")
                    if flag == 1:
                        for w in re:
                            print(f"从re提取的景点数据w是{w}")
                            hong = w[5].replace('\\n', '').replace('\\r', '')
                            hs = [{'id': cnt, 'jiname': w[0], 'grade': w[1], 'img1': w[2], 'img2': w[3],
                                   'img3': w[4], 'intr': hong, 'time': w[6], 'where': w[7], 'feature': w[10]}]
                            # print ("log2++++",w[5].replace('\r',''))
                            los = [{'icon': string, 'position': [float(w[9]), float(w[8])], 'name': w[0]}]
                        flag = 2
                    else:
                        for w in re:
                            hong = w[5].replace('\\n', '').replace('\\r','')
                            # print("hhhhhhh1",hong)
                            hs.append({'id': cnt, 'jiname': w[0], 'grade': w[1], 'img1': w[2], 'img2': w[3],
                                       'img3': w[4], 'intr':hong, 'time': w[6], 'where': w[7], 'feature': w[10]})
                            # print ("w[8] of  type",type(w[8]))
                            # con1 = float(w[8])
                            # print ("con1",con1)
                            los.append({'icon': string,
                                        'position': [float(w[9]), float(w[8])], 'name': w[0]})
                            # print ( type( los[0]['position'][1] ) )
                    kh += 1
        cnt += 1
        # print(cnt)
    # print("datpath", biginfo.datpath)
    # print("los", los)

    # 推荐理由更新
    final_text = "为您推荐如下的旅游线路。本条旅游路线包括了："
    resontence = []
    length = 1
    for travel in hs:
        resontence.append(travel['feature'])
        if length != len(hs):
            resontence.append("、")
            length += 1
    final_text += " ".join(resontence)
    final_text += "希望能为您的出行提供帮助。"

    # 第二条路线
    # 酒店
    cnt1 = 1
    flag1 = 1
    for i in biginfo1.hotlepath:
        sh1 = sqlinfo()
        re = sh1.find_hoteinfo(i)
        if flag1 == 1:
            for w in re:
                hos1 = [{'id': cnt1, 'name': w[0], 'intr': w[1], 'img': w[2]}]
            flag1 = 2
        else:
            for w in re:
                hos1.append({'id': cnt1, 'name': w[0], 'intr': w[1], 'img': w[2]})
        cnt1 += 1

    # 美食
    sf1 = 1
    cnt1 = 1
    flag1 = 1
    for i in biginfo1.foodpath:
        if sf1 > 3:
            cnt1 += 1
            sf1 = 1
        sh1 = sqlinfo()
        re = sh1.find_foodinfo(i)
        if flag1 == 1:
            for w in re:
                hong = w[1].replace('\\n', '').replace('\\r', '')
                fos1 = [{'id': cnt1, 'name': w[0], 'intr': hong, 'img': w[2]}]
            flag1 = 2
        else:
            for w in re:
                hong = w[1].replace('\\n', '').replace('\\r', '')
                fos1.append({'id': cnt1, 'name': w[0], 'intr': hong, 'img': w[2]})
        sf1 += 1

    # 景点
    cnt1 = 1
    flag1 = 1
    kh1 = 1
    for i in biginfo1.jdpath:
        # print (i)
        for j in i:
            # print (j)
            for k in j:
                if k != 0:
                    sh = sqlinfo()
                    re = sh.find_jdinfo(k)
                    # http://webapi.amap.com/theme/v1.3/markers/n/mark_b2.png
                    string = 'http://webapi.amap.com/theme/v1.3/markers/n/mark_r.png'
                    # string ='http://amappc.cn-hangzhou.oss-pub.aliyun-inc.com/lbs/static/img/marker.png'

                    if flag1 == 1:
                        for w in re:
                            hong = w[5].replace('\\n', '').replace('\\r', '')
                            hs1 = [{'id': cnt1, 'jiname': w[0], 'grade': w[1], 'img1': w[2], 'img2': w[3],
                                    'img3': w[4], 'intr': hong, 'time': w[6], 'where': w[7], 'feature': w[10]}]
                            # print ("log2++++",w[5].replace('\r',''))
                            los1 = [{'icon': string, 'position': [float(w[9]), float(w[8])], 'name': w[0]}]
                        flag1 = 2
                    else:
                        for w in re:
                            hong = w[5].replace('\\n', '').replace('\\r', '')
                            # print("hhhhhhh1",hong)
                            hs1.append({'id': cnt1, 'jiname': w[0], 'grade': w[1], 'img1': w[2], 'img2': w[3],
                                        'img3': w[4], 'intr': hong, 'time': w[6], 'where': w[7], 'feature': w[10]})
                            # print ("w[8] of  type",type(w[8]))
                            # con1 = float(w[8])
                            # print ("con1",con1)
                            los1.append({'icon': string,
                                         'position': [float(w[9]), float(w[8])]
                                            , 'name': w[0]})
                            # print ( type( los[0]['position'][1] ) )
                    kh1 += 1
        cnt1 += 1

    # 推荐理由更新
    final_text1 = "为您推荐如下的旅游线路。本条旅游路线包括了："
    resontence = []
    length = 1
    for travel in hs1:
        resontence.append(travel['feature'])
        if length != len(hs1):
            resontence.append("、")
            length += 1
    final_text1 += " ".join(resontence)
    final_text1 += "希望能为您的出行提供帮助。"

    # 每个景点的经纬度转换为json列表
    los_log_lat = {"log": [], "lat": []}
    los1_log_lat = {"log": [], "lat": []}
    for re in los:
        los_log_lat["log"].append(re['position'][0])
        los_log_lat["lat"].append(re['position'][1])
    for re1 in los1:
        los1_log_lat["log"].append(re1['position'][0])
        los1_log_lat["lat"].append(re1['position'][1])
    # print("biginfo为经过index后的推荐结果，为：\n", biginfo)
    # print("test2为：", test2)
    # print("hs为：", hs)
    # print("fos为：", fos)
    # print("hos为：", hos)
    # print("los为(json版本)：", json.dumps(los))
    # print("hs1为：", hs1)
    # print("fos1为：", fos1)
    # print("hos1为：", hos1)
    # print("los1为：", los1)
    # print("playday为：", quanju.play_day)
    # print("resontence为：", resontence)
    # dumps是将python对象转成json格式的字符串，主要格式是dumps(obj)
    # print(f"los_log_lat是{los_log_lat}")
    # print(f"los1_log_lat是{los1_log_lat}")

    return render(request, 'result2.html',
                  {'biginfo': biginfo, 'test2': test2, 'hs': hs, 'fos': fos, 'hos': hos,
                   'los_log_lat': los_log_lat,
                   'biginfo1': biginfo1, 'hs1': hs1, 'fos1': fos1, 'hos1': hos1,
                   'los1_log_lat': los1_log_lat,
                   'playday': quanju.play_day, 'resontence': final_text, 'resontence1': final_text1})


def addindex_number(request):
    number = random.randint(0, 100)
    value = {'title': number}
    return render(request, 'addindex_number.html', context=value)


# 主页面：根据已有用户的id，使用k-聚类预测其喜欢的城市
# 提取该城市景点、美食、酒店信息传递至html渲染
# 在主页面展示其喜欢城市的景区、美食、酒店
def addindex(request):
    # 当URLconf文件匹配到用户输入的路径后，会调用对应的view函数，并将HttpRequest对象(即request)作为第一个参数传入该函数。
    if request.method == "POST" and request.POST:
        # HttpRequest.POST返回一个 querydict ，该对象包含了所有的HTTP POST参数，通过 表单 上传的所有 字符 都会保存在该属性中。
        searchinfo = request.POST["searchinfo"]
        search.searchinfo = searchinfo
        # 将用户请求重定向到另一个 URL，即search视图
        return HttpResponseRedirect('search')

    jdk = [{}]
    fdk = [{}]
    hdk = [{}]

    estimator = KNeighborsClassifier(n_neighbors=3)
    user_id = newuserinfo.id
    s = random.randint(1, 60)
    p = 0
    # 默认用户类id为-1
    if user_id == -1:
        s = random.randint(1, 60)
        # print(s)
        s = [[s]]
    else:
        # 寻找数据库中已有的用户id
        ks = sqlinfo().find_userlike(user_id)
        for w in ks:
            p = w[0]
        s = [[int(p)]]
        # print(s)

    # s = [[s]]
    # 2.使用fit方法进行训练，x为二维，y为一维
    estimator.fit(x, y)
    # 3.数据预测,将测试集的特征值传入，根据先前计算出的模型，来预测所给测试机的目标值，注意参数为二维[[]]
    # todo 注意载入的用户id，若是用户则会从数据库导出该用户的信息
    # ret1 = estimator.predict(s)
    ret1 = "guilin"
    # print("预测喜欢的城市", ret1)

    # 根据城市取出地区的景点，食物，酒店
    # todo 修改数据后，更改提取的键值
    jdinfo = sqlinfo().hot_jdinfo(ret1)
    fdinfo = sqlinfo().index_foodinfo()
    hotleinfo = sqlinfo().index_hotleinfo()

    # 取出景点、食物、酒店的各个信息
    # todo 修改数据后，更改存储展示数据的字典
    for w in jdinfo:
        jdk.append({'jiname': w[0],
                    'jwhere': w[1][0:11],
                    'intr': w[3].replace(" ", '').replace('\\n', '').replace('\\r', '')[0:35] + "...",
                    'img1': w[2],
                    'id': w[4]})
    jdk.pop(0)

    for w in fdinfo:
        fdk.append({"fname": w[0],
                    "intr": w[1].replace(" ", '').replace('\\n', '').replace('\\r', '')[0:35]+"...",
                    "img": w[2]})
    fdk.pop(0)

    for w in hotleinfo:
        hdk.append({"img": "https:"+w[2]})
    hdk.pop(0)

    # 统计数量
    # todo 修改数据后，更改计算总量
    jd_num = sqlinfo().all_num("jdinfo")
    food_num = sqlinfo().all_num("foodinfo")
    hotle_num = sqlinfo().all_num("hotleinfo")
    cdk = {"jd": jd_num, "food": food_num,"hotle": hotle_num}

    return render(request,
                  'addindex.html',
                  {'indexinfo': jdk, 'foodinfo': fdk, 'hotleinfo': hdk, 'userinfo': newuserinfo, 'cdk': cdk})


def login(request):
    # indexinfo = sqlinfo().hot_jdinfo()
    if request.method == "POST" and request.POST:
        name = request.POST['name']
        password = request.POST['password1']
        sh = sqlinfo()
        if(len(list(sh.yanzhe_user(name,password)))):
            for item in sh.yanzhe_user(name,password):
                # id,name,tel,password,img
                newuserinfo.id = item[0]
                newuserinfo.name = item[1]
                newuserinfo.tel =item[2]
                newuserinfo.img=item[4]
            return HttpResponseRedirect('addindex')
        else:
            messages.success(request, '密码错误')
    return render(request, 'login.html')


def jdhtml(request):
    jdk = []
    jdinfo = sqlinfo().all_jdinfo()
    for w in jdinfo:
        jdk.append({'jiname': w[0], 'jwhere': w[1][0:13],
                    'intr': w[3].replace(" ", '').replace('\\n', '').replace('\\r', '')[0:35] + "...", 'img1': w[2], 'id':w[6]})
    return render(request, 'jdhtml.html',{'jdinfo':jdk,'userinfo':newuserinfo})



def jdDetails(request,id):
    sh = sqlinfo()
    if request.method == "POST" and request.POST:
        text = request.POST['messgae']
        a1 = datetime.datetime.now().strftime('%Y-%m-%d')
        jd_id = id
        user_id = newuserinfo.id
        sh.write_comm(text,a1,jd_id,user_id)
    jdk ={}

    jdinfo = sh.find_detailjdinfo(id)
    cdk =[]
    cominfo =sh.find_detailcomminfo(id);

    for w in jdinfo:
        jdk['jiname']=w[0]
        jdk['jwhere'] =w[1]
        jdk['intr'] = w[3].replace(" ", '').replace('\\n', '').replace('\\r', '')
        jdk['img1'] =w[2]
        jdk['img2']=w[4]
        jdk['img3']=w[5]

    for h in cominfo:
        cdk.append({'commentinfo':h[0],'datetime':h[1],'img':h[2],'username':h[3]})
        # commentinfo,datetime,userinfo.img

    return render(request,'jdDetails.html',{'jdinfo':jdk,'cominfo':cdk,'userinfo':newuserinfo})


def search(request):

    ah = sqlinfo()
    jdinfo = ah.search_info(search.searchinfo)
    jdk = []
    fdk = []
    hdk = []
    for w in jdinfo:
        jdk.append({'jiname': w[0], 'jwhere':w[1][0:13] ,'intr': w[3].replace(" ",'').replace('\\n', '').replace('\\r','')[0:35]+"...", 'img1': w[2],'id':w[4]})
    foodinfo = ah.search_foodinfo(search.searchinfo)
    for w in foodinfo:
        fdk.append({"fname":w[0],"intr":w[1].replace(" ",'').replace('\\n', '').replace('\\r','')[0:35]+"...","img":w[2]})
    hotleinfo =ah.search_hotleinfo(search.searchinfo)
    for w  in hotleinfo:
        hdk.append({"img":"https:"+w[2],'name':w[0],'intr':w[1]})


    return render(request,'search.html',{'indexinfo':jdk,'foodinfo':fdk,'hotleinfo':hdk,'userinfo':newuserinfo})

def profile(request):
    return  render(request,'profile.html',{'userinfo':newuserinfo})

def regist(request):
    bh = sqlinfo()
    if request.method == "POST" and request.POST:
        username = request.POST['abcd']
        tell = request.POST['tell']
        password = request.POST['rfg']
        img ='https://dimg04.c-ctrip.com/images/t1/headphoto/057/777/943/0b93f8268d5546308915f4f9fcaa9483.jpg'
        user_like = random.randint(1, 10)
        bh.write_user(username,img,tell,password,user_like)
        messages.success(request, '注册成功')

    return  render(request,'login.html')

@xframe_options_exempt
def adminindex(request):
    return  render(request,'adminindex.html')

@xframe_options_sameorigin
# 异步跳转
def adminjdlist(request):
    jdk = []
    jdinfo = sqlinfo().all_jdinfo()
    for w in jdinfo:
        jdk.append({'jiname': w[0], 'jwhere': w[1][0:13],
                    'intr': w[3].replace(" ", '').replace('\\n', '').replace('\\r', '')[0:35] + "...", 'img1': w[2],
                    'id': w[6],'jdtype':w[7],'grade':w[8]})
    return  render(request,'adminjdlist.html',{'jdinfo':jdk})


@xframe_options_sameorigin
# 异步跳转
def adminfoodlist(request):
    fdk = []
    fdinfo = sqlinfo().all_foodinfo()
    for w in fdinfo:
        fdk.append({"fname": w[0], "intr": w[1].replace(" ", '').replace('\\n', '').replace('\\r', '')[0:35] + "...",
                    "img": w[2],'city':w[3],'id':w[4]})
    return  render(request,'adminfoodlist.html',{'foodinfo':fdk})


@xframe_options_sameorigin
# 异步跳转
def adminuserlist(request):
    udk = []
    uinfo = sqlinfo().all_userinfo()
    for w in uinfo:
        udk.append({'id':w[0],'name':w[1],'tel':w[2],'img':w[3]})
    return  render(request,'adminuserlist.html',{'userinfo':udk})


def faq(request):
    sh = sqlinfo()
    hisinfo = sh.find_userallhsitory(newuserinfo.id)
    jdk =[]

    date = []
    strjdk=[]
    for w  in hisinfo:
        flag = []
        for z in w[2].split(' '):
            for ks in sh.find_jdname(z):
                flag.append(str(ks).replace('(', '').replace(')', '').replace(',', '').replace("'", ''))
        strjdk.append({'jdinfo':flag,'date':w[4]})
    return render(request,'faq.html',{"item":strjdk})





