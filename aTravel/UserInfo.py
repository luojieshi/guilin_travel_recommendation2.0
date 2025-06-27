import random

from aTravel.sqlsqlit import sqlinfo


def judge(i):
    ty_name = 0
    if i == 1:
        ty_name = "现代风情"
    if i == 2:
        ty_name = "历史风情"
    if i == 3:
        ty_name = "当地特色"
    if i == 4:
        ty_name = "博物馆"
    if i == 5:
        ty_name = "当地动物园"
    if i == 6:
        ty_name = "游乐中心"
    if i == 7:
        ty_name = "历史伟人"
    if i == 8:
        ty_name = "当地公园"
    if i == 9:
        ty_name = "植物园"
    if i == 10:
        ty_name = "国内名校"
    if i == 11:
        ty_name = "购物中心"
    if i == 12:
        ty_name = "当地剧院"
    if i == 13:
        ty_name = "当地古镇"
    if i == 14:
        ty_name = "红色文化"
    if i == 15:
        ty_name = "体育公园"
    if i == 16:
        ty_name = "宗教圣地"
    return ty_name


class UserInfo:
    def __init__(self, city, people, daytime, pays, traffic, jd_type, play_mode):
        # 旅行出发城市
        self.city = city
        # 旅行人数
        self.people = people
        # 旅行时间
        self.day_time = daytime
        # 旅行花费
        self.pay = pays
        # 交通方式
        self.traffic = traffic
        # 景点类型数组[1,2,3,4,5]
        self.jd_type = jd_type
        # 0为快速游，1为精致游
        self.play_mode = play_mode
        # 推荐后的景点路径
        self.test_array = [3, 4, 7, 8, 10, 12, 15, 19, 29, 21]
        self.jd_array = []
        # 推荐后的多少条线路以及每条线路景点id列表（20：一条线路上最多有20个景点tip：虽然也不会到20的说）
        self.day_path = [[0 for i in range(20)] for i in range(len(self.jd_array))]  # 每日的路径规划
        self.food_array = []  # 推荐后的美食
        self.hotel_array = []  # 推荐后的酒店

    # 函数目的：召回所有要推荐的景点id列表
    def find_id(self):
        # dis：目标景点的id列表
        dis = []
        sh = sqlinfo()
        # 精致旅游
        if self.play_mode == 1:
            for i in self.jd_type:
                # 从数据库找出符合类型且在目的城市的景点id、评分列表
                re = sh.find_jdtype(judge(i), self.city)
                for j in re:
                    k = list(j)
                    dis.append(k[0])
        # 快速旅游
        else:
            tmp = []
            for i in range(1, 17):
                tmp.append(0)
            for i in self.jd_type:
                cnt = 0
                sh = sqlinfo()
                type_name = judge(i)
                # 从数据库找出符合类型且在目的城市的景点id、评分列表
                qs = sh.find_jdtype(type_name, self.city)
                # cnt为有多少个符合这个类型的景点
                for j in qs:
                    cnt += 1
                # tmp为1-16种景点类型列表，统计对应类型的景点有多少个
                tmp[int(i - 1)] = cnt

            # 遍历每个景点类型
            fl = 1
            for i in tmp:
                # 如果这个类型的景点有0-3个，获取现这个景点id列表
                if 0 < i <= 3:
                    re = sh.find_jdtype(judge(fl), self.city)
                    for j in re:
                        k = list(j)
                        dis.append(k[0])
                # 如果这个类型的景点超过3个
                if i > 3:
                    re = sh.find_jdtype(judge(fl), self.city)
                    # bos字典：每个景点对应的评分，从高到低排序，优先选择高评分的景点
                    bos = {}
                    for j in re:
                        k = list(j)
                        bos[k[0]] = float(k[1])
                    bos = sorted(bos.items(), key=lambda x: x[1], reverse=True)
                    # 最少选择3个景点
                    i_num = int(i / 3)
                    if i_num <= 3:
                        i_num = 3
                    for j in range(i_num):
                        dis.append(bos[j][0])
                fl += 1

        self.jd_array = dis
        return self.jd_array

    def food_recommendation(self, l1, l2):
        h = set()
        # 推荐合适数量的美食
        fl = self.day_time * 3
        if self.day_time * 3 > (l2 - l1 + 1):
            fl = (l2 - l1 + 1)
        # 随机选择该城市的一种食物id
        while len(h) < fl:
            h.add(random.randint(l1, l2))
        return h

    def hotel_recommendation(self, l1, l2):
        h = set()
        while len(h) < self.day_time:
            h.add(random.randint(l1, l2))
        # print(h)
        return h

    # 函数目的：获取目的城市的食物id列表
    def food(self):
        if self.city == 'beijing':
            self.food_array = self.food_recommendation(1, 15)
        else:
            if self.city == 'changsha':
                self.food_array = self.food_recommendation(16, 26)
            else:
                if self.city == 'shanghai':
                    self.food_array = self.food_recommendation(27, 41)
                else:
                    if self.city == 'hangzhou':
                        self.food_array = self.food_recommendation(42, 55)
                    else:
                        if self.city == 'chengdu':
                            self.food_array = self.food_recommendation(91, 105)
                        else:
                            if self.city == 'guangzhou':
                                self.food_array = self.food_recommendation(56, 78)
                            else:
                                if self.city == 'shenzhen':
                                    self.food_array = self.food_recommendation(79, 90)
                                else:
                                    if self.city == 'sanya':
                                        self.food_array = self.food_recommendation(106, 21)
                                    else:
                                        if self.city == 'xian':
                                            self.food_array = self.food_recommendation(123, 143)
                                        else:
                                            if self.city == 'cangzhou':
                                                self.food_array = self.food_recommendation(144, 146)
                                            else:
                                                if self.city == 'guilin':
                                                    self.food_array = self.food_recommendation(147, 161)
        return self.food_array

    # 函数目的：获取目的城市的酒店id列表
    def hotel_id(self):
        if self.city == 'beijing':
            self.hotel_array = self.hotel_recommendation(1, 25)
        else:
            if self.city == 'changsha':
                self.hotel_array = self.hotel_recommendation(26, 49)
            else:
                if self.city == 'shanghai':
                    self.hotel_array = self.hotel_recommendation(50, 74)
                else:
                    if self.city == 'hangzhou':
                        self.hotel_array = self.hotel_recommendation(75, 103)
                    else:
                        if self.city == 'chengdu':
                            self.hotel_array = self.hotel_recommendation(104, 128)
                        else:
                            if self.city == 'shenzhen':
                                self.hotel_array = self.hotel_recommendation(129, 153)
                            else:
                                if self.city == 'guangzhou':
                                    self.hotel_array = self.hotel_recommendation(154, 178)
                                else:
                                    if self.city == 'sanya':
                                        self.hotel_array = self.hotel_recommendation(222, 245)
                                    else:
                                        if self.city == 'xian':
                                            self.hotel_array = self.hotel_recommendation(179, 210)
                                        else:
                                            if self.city == 'cangzhou':
                                                self.hotel_array = self.hotel_recommendation(246, 270)
                                            else:
                                                if self.city == 'guilin':
                                                    self.hotel_array = self.hotel_recommendation(272, 296)
        return self.hotel_array

    # 函数目的：计算最后的费用，更改self.pay变量
    def add_pay(self):
        self.pay = 0
        if self.city == 'beijing':
            if self.traffic == "火车":
                self.pay += 400
            else:
                if self.traffic == "特价票":
                    self.pay += 700
                else:
                    if self.traffic == "高铁":
                        self.pay += 1400
                    else:
                        if self.traffic == "机票":
                            self.pay += 2000
            self.pay += (500 * self.day_time)
        else:
            if self.city == 'changsha':
                if self.traffic == "火车":
                    self.pay += 300
                else:
                    if self.traffic == "特价票":
                        self.pay += 480
                    else:
                        if self.traffic == "高铁":
                            self.pay += 700
                        else:
                            if self.traffic == "机票":
                                self.pay += 800
                self.pay += (300 * self.day_time)
            else:
                if self.city == 'shanghai':
                    if self.traffic == "火车":
                        self.pay += 360
                    else:
                        if self.traffic == "特价票":
                            self.pay += 800
                        else:
                            if self.traffic == "高铁":
                                self.pay += 900
                            else:
                                if self.traffic == "机票":
                                    self.pay += 1400
                    self.pay += (500 * self.day_time)
                else:
                    if self.city == 'hangzhou':
                        if self.traffic == "火车":
                            self.pay += 400
                        else:
                            if self.traffic == "特价票":
                                self.pay += 490
                            else:
                                if self.traffic == "高铁":
                                    self.pay += 700
                                else:
                                    if self.traffic == "机票":
                                        self.pay += 800
                    else:
                        if self.city == 'guilin':
                            if self.traffic == "火车":
                                self.pay += 300
                            else:
                                if self.traffic == "特价票":
                                    self.pay += 450
                                else:
                                    if self.traffic == "高铁":
                                        self.pay += 600
                                    else:
                                        if self.traffic == "机票":
                                            self.pay += 900
                        self.pay += (300 * self.day_time)
        return self.pay

    # 函数目的：返回所有推荐线路中一共有多少个景点，同时根据目的城市
    # 确定推荐的美食、酒店id，根据选择的出行方式和城市计算花费
    def last_path(self):
        # cnt：当前第几天
        cnt = 1
        flag = 0
        # 选取第i种推荐线路
        for i in self.day_path:
            # 取出列表
            for j in i:
                # 遍历该旅游线路中每个景点id
                for k in j:
                    # 如果id不为0证明是一个景点
                    if k != 0:
                        flag += 1
                        # sh = sqlinfo()
                        # re = sh.find_jdinfo(k)
                        # for w in re :
                        #    print (w)
            cnt += 1
        self.day_time = cnt - 1
        self.food()
        self.hotel_id()
        self.add_pay()
        # print("当前获取的美食信息", self.food_array)
        # print("获取当前酒店信息", self.hotel_array)
        return flag


if __name__ == '__main__':
    test_a = UserInfo('beijing', 5, 4, 0, "火车", [5, 15])
    hotel_array = test_a.hotel_id()
    pay = test_a.add_pay()
    # a.find_id()
    print("shu", test_a.find_id())
    print(hotel_array, pay)
