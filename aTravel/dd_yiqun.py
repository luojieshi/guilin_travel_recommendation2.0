# encoding:utf-8
import numpy as np
from aTravel.UserInfo import UserInfo
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# dis_jd函数：从各个景点的经纬度中，计算各个景点的距离
def dis_jd(jd_where, city_num):
    num = jd_where.shape[0]
    dis = np.zeros((city_num, city_num))
    for i in range(num):
        for j in range(i, num):
            dis[i][j] = dis[j][i] = np.linalg.norm(jd_where[i] - jd_where[j])
    return dis


# day_best_path函数：为每条推荐结果每天设置合适的游览景点，返回每天该去的景点列表
def day_best_path(road, best_play_time, jd_num, info, day_path, day):
    # 保存景点对应的名称和每个景点花费的时间
    orl = [[0 for i in range(3)] for i in range(len(jd_num))]
    cnt = 0
    for i in road:
        i = int(i)
        orl[cnt] = [info[i][0], info[i][1], info[i][4]]
        cnt += 1

    # 合理规划当天的行程路径，一天不应超过8h
    # 如果游玩超过八小时，将该景点开始考虑下一天
    daytime = 0
    cnt = 0
    k = 0
    for jd in orl:
        if daytime + jd[2] <= best_play_time:
            daytime = daytime + jd[2]
            day_path[cnt][k] = jd[0]
            k += 1
        else:
            day += 1
            daytime = jd[2]
            k = 0
            cnt += 1
            day_path[cnt][k] = jd[0]
            k += 1

    return day_path



class jdyiqun:
    def __init__(self):
        self.path_information = []
        self.last_path = []
        self.lon_lat = []
        self.recommend_path = []

    # ant_colony函数：蚁群算法入口
    def ant_colony(self, jd_id_list):
        # print(f"蚁群算法的原景点序列：{jd_id_list.jd_array}")
        # jd_id_list为UserInfo类
        # 参数初始化
        Q = 1  # 信息素更新参数
        iter = 0   # 迭代计数器
        rho = 0.1  # 信息素的挥发速度
        alpha = 1  # 信息素重要程度因子
        beta = 5  # 启发式函数（能见度）重要程度因子
        day = 1
        best_play_time = 8

        # 传递所有要推荐的景点id数组、计算景点数量、蚂蚁数量、最大迭代次数
        jd_num = jd_id_list.jd_array
        city_num = len(jd_num)
        ant_num = city_num - 2
        iter_max = city_num * city_num

        # n个景点，m只蚂蚁。信息素矩阵nxn，每个城市之间的信息素浓度
        pheromone_table = np.ones((city_num, city_num))
        # 路径记录表，mxn，每个蚂蚁到每个城市
        path_table = np.zeros((ant_num, city_num)).astype(int)
        # 每次迭代，所有蚂蚁走过路径的平均长度
        length_aver = np.zeros(iter_max)
        # 每次迭代，所有蚂蚁走过的路径长度中确认的最佳路径长度和对应路径
        length_best = np.zeros(iter_max)
        path_best = np.zeros((iter_max, city_num))
        # 创建一个二维数组，存储每个景点的相关数据
        info = [[0 for i in range(5)] for i in range(city_num)]
        # 存储用户期望的景点的经纬度
        jd_where = [[0 for i in range(2)] for i in range(city_num)]
        day_path = [[0 for i in range(20)] for i in range(city_num)]

        # 建立和sqlite的链接
        cx = sqlite3.connect('./DB/travle.db')
        cu = cx.cursor()
        cnt = 0
        for i in jd_num:
            # 提取所有景点的id、名字、经纬度、游玩时间
            sql = "select id,jiname,lon,lat,times from jdinfo where id=:st_id"
            results = cu.execute(sql, ({'st_id': i}))
            flag = 0
            for j in results:
                # 往二维数组info里放入每个景点的5个数据
                info[cnt] = [int(j[0]), str(j[1]), float(j[2]), float(j[3]), int(j[4])]
                flag += 1
            cnt += 1
        cu.close()
        cx.commit()
        cx.close()

        # 往经纬度数组jd_where里放入每个景点的经纬度
        cnt = 0
        for i in info:
            jd_where[cnt] = [i[2], i[3]]
            cnt += 1

        jd_where = np.array(jd_where)
        # todo dis_jd：计算各个景点之间距离 nxn
        dist = dis_jd(jd_where, city_num)
        dist_mat = dis_jd(jd_where, city_num)

        # 启发函数矩阵，表示从景点i转移到矩阵j的期望程度
        # np_diagonal([1e10] * city_num)：创建一个nxn的矩阵，对角线全为1e10
        # 当然，一个城市从自己转移到自己的概率是0。至于两个城市间，则看距离(越短越好则倒数)
        heuristics_table = 1.0 / (dist + np.diag([1e10] * city_num) + 0.5)

        while iter < iter_max:
            # 随机产生各个蚂蚁的景点初始位置
            # 蚂蚁-景点矩阵的第一列为随机打乱的景点出发序列
            path_table[:, 0] = np.random.permutation(range(0, city_num))[:ant_num]

            # 计算各个蚂蚁的路径距离
            may_zero_length = np.zeros(ant_num)
            for i in range(ant_num):
                # 当前所在的景点
                may_visiting_cities = path_table[i, 0]
                # 储存未遍历到的景点
                may_unvisited_cities = set(range(city_num))
                # 删除已经遍历的景点
                may_unvisited_cities.remove(may_visiting_cities)

                # 循环n-1次，遍历其余未访问的景点
                for j in range(1, city_num):
                    # 每次用轮盘赌法选择下一个要访问的景点
                    may_list_unvisited_cities = list(may_unvisited_cities)
                    may_mat_unvisited_cities = np.zeros(len(may_list_unvisited_cities))
                    for k in range(len(may_list_unvisited_cities)):
                        # 蚁群算法中确定转移概率的部分。i景点到j景点的转移概率
                        # 由i到j的信息素浓度和启发式函数强度（能见度即距离的倒数）
                        may_mat_unvisited_cities[k] = np.power(
                            pheromone_table[may_visiting_cities][may_list_unvisited_cities[k]],
                            alpha) * np.power(
                            heuristics_table[may_visiting_cities][may_list_unvisited_cities[k]], alpha)

                    # 得到的可能转移景点概率列表累加求和
                    may_mat_cum_sum = (may_mat_unvisited_cities / sum(may_mat_unvisited_cities)).cumsum()
                    may_mat_cum_sum -= np.random.rand()
                    k = may_list_unvisited_cities[(np.where(may_mat_cum_sum > 0)[0])[0]]
                    # 下一轮选中的景点并添加到对应的路径表和距离表中
                    path_table[i, j] = k
                    may_unvisited_cities.remove(k)
                    may_zero_length[i] += dist_mat[may_visiting_cities][k]
                    may_visiting_cities = k
                # 添加到距离表中（包含始末位置的距离)
                may_zero_length[i] += dist_mat[may_visiting_cities][path_table[i, 0]]

            # 更新每次记录的最佳路径和最佳路径长度
            length_aver[iter] = may_zero_length.mean()
            if iter == 0:
                length_best[iter] = may_zero_length.min()
                path_best[iter] = path_table[may_zero_length.argmin()].copy()
            else:
                if may_zero_length.min() > length_best[iter - 1]:
                    length_best[iter] = length_best[iter - 1]
                    path_best[iter] = path_best[iter - 1].copy()
                else:
                    length_best[iter] = may_zero_length.min()
                    path_best[iter] = path_table[may_zero_length.argmin()].copy()

            # 更新信息素
            may_change_information = np.zeros((city_num, city_num))
            # 对蚂蚁走过的路径，使用能见度作为信息素增加的依据
            for i in range(ant_num):
                for j in range(city_num - 1):
                    may_change_information[path_table[i, j]][path_table[i, j + 1]] += Q / (dist_mat[path_table[i, j]][
                        path_table[i, j + 1]] + 0.5)
                may_change_information[path_table[i, j + 1]][path_table[i, 0]] += Q / (dist_mat[path_table[i, j + 1]][
                    path_table[i, 0]] + 0.5)
            # 更新信息素
            pheromone_table = (1 - rho) * pheromone_table + may_change_information
            iter += 1
        # print(f"经过蚁群算法得到的最佳景点路径：{path_best}，路径长度：{length_best}")
        # todo 经过蚁群推荐后得到最佳推荐路线和最佳路线距离，使用day_best_path做出旅行规划结果
        sh = day_best_path(path_best[-1], best_play_time, jd_num, info, day_path, day)
        self.recommend_path = sh
        # print(f"经过day_best_path函数得到的景点路径结果{sh}")
        # 重排最后的推荐结果tmp
        k = 0
        for i in sh:
            if i[0] != 0:
                k += 1
        tmp = [[0 for i in range(20)] for i in range(k)]
        cnt = 0
        for i in sh:
            if i[0] != 0:
                tmp[cnt] = [i]
                cnt += 1
        # print(f"最后返回的景点推荐结果{tmp}")
        self.lon_lat = jd_where
        self.last_path = path_best[-1]
        self.path_information = info

        return tmp

    # 作出找到的最优路径图
    def bestRoad(self,bestpath,lonlat,flag):
        plt.plot(lonlat[:, 0], lonlat[:, 1], 'r.', marker='o', markerfacecolor='red')
        plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f °'))
        plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f °'))
        plt.tight_layout(pad=2)
        # plt.xlim([xmin - 0.05, xmax + 0.05])
        # plt.ylim([ymin - 0.05, ymax + 0.05])
        for i in range(len(bestpath) - 1):
            m = int(bestpath[i])
            n = int(bestpath[i + 1])
            plt.plot([lonlat[m][0], lonlat[n][0]], [lonlat[m][1], lonlat[n][1]], 'k')
        plt.plot([lonlat[int(bestpath[0])][0], lonlat[int(n)][0]], [lonlat[int(bestpath[0])][1], lonlat[int(n)][1]],
                 'b')
        print ("t",lonlat[int(bestpath[0])][0], lonlat[int(n)][0])
        # plt.text(lonlat[int(bestpath[0])][0], lonlat[int(n)][0], 's444', color='r')
        plt.grid(True)
        if flag == 0:
            plt.gca().set_title("The optimum path")
        else:
            plt.gca().set_title("The optimum path of " + str(flag))
        plt.gca().set_xlabel('longitude')
        plt.gca().set_ylabel('latitude')
        plt.show()

    def daypathRoad(self,tx, h_day):
        tm = []
        for i in tx:
            if (i != 0):
                tm.append(i)
        lonlat = [[0 for i in range(2)] for i in range(len(tm))]
        cnt = 0;
        tmpath = []
        for z in tm:
            # 每一个景点的信息
            for i in self.path_information:
                if (i[0] == z):
                    lonlat[cnt] = [i[2], i[3]]

                    tmpath.append(cnt)
                    cnt += 1
        lonlat = np.array(lonlat)
        self.bestRoad(tmpath, lonlat, h_day)


if __name__ == '__main__':
    a = jdyiqun()
    h = a.ant_colony(UserInfo)
    print(a.ant_colony(UserInfo))





