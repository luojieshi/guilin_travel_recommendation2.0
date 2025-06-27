import sqlite3


class sqlinfo:
    # 建立和sqlite的链接
    def con(self):
        cx = sqlite3.connect('./DB/travle.db')
        #cu = cx.cursor()
        return cx
    # for i in jdnum:
    #     # print i
    #     sql = "select id,jiname,lon,lat,times from jdinfo where id=:st_id"
    #     results = cu.execute(sql, ({'st_id': i}))
    def find_yiqun(self,i):
        sql = "select id,jiname,lon,lat,times from jdinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': i}))
        self.close_sql(cu,self.con())
        return results

    # 从数据库中取出在目的城市，类型符合的景点的id和评分
    def find_jdtype(self, jdtype, city):
        sql = "select id,sum_sc from jdinfo where jdtype =:st_jdtype and city=:st_city"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_jdtype': jdtype, 'st_city': city}))
        return results

    def find_jdinfo (self,id):
        sql = "select jiname,grade,img1,img2,img3,introudec,times,jdwhere,lon,lat, jdtype1 from jdinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        return results

    def find_foodinfo (self,id):
        sql = "select foodname,introudec,img from foodinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        return results

    def find_hoteinfo(self,id):
        sql = "select hotlename,introudec,img from hotleinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        return results


    def hot_jdinfo(self,city):

        sql = "SELECT jiname,jdwhere,img1,introudec,id FROM jdinfo where city=:city order by RANDOM() LIMIT 16"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'city': city}))
        # self.close_sql(cu, self.con())
        return results

    def index_foodinfo(self):
        sql = "SELECT foodname,introudec,img  FROM foodinfo order by RANDOM() LIMIT 6"
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results

    def  index_hotleinfo(self):
        sql = "SELECT hotlename,introudec,img  FROM hotleinfo LIMIT 30"
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results

    def all_bloginfo(self):
        sql = "SELECT b_content,user_id,hot_index,img1,intr,blog_name,city,user_blog,id FROM bloginfo order by RANDOM() LIMIT 32"
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results

    def all_jdinfo(self):
        sql = "SELECT jiname,jdwhere,img1,introudec,img2,img3,id,jdtype,grade FROM jdinfo"
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results

    def all_hotleinfo(self):
        sql = "SELECT hotlename,introudec,img,id FROM hotleinfo"
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results


    def all_foodinfo(self):
        sql = "SELECT foodname,introudec,img,city,id  FROM foodinfo "
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results

    def all_userinfo(self):
        sql = "SELECT id,name,tel,img  FROM userinfo "
        cu = self.con().cursor()
        results = cu.execute(sql)
        # self.close_sql(cu, self.con())
        return results


    def find_detailjdinfo (self,id):
        sql = "SELECT jiname,jdwhere,img1,introudec,img2,img3,id FROM jdinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        # self.close_sql(cu, self.con())
        return results

    def find_detailbloginfo(self,id):
        sql = "SELECT blog_name,intr,user_blog FROM bloginfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        # self.close_sql(cu, self.con())
        return results

    def find_detailcomminfo (self,id):
        sql = "select commentinfo,datetime,userinfo.img,userinfo.name from comminfo ,userinfo ,jdinfo  WHERE jdinfo.id = comminfo.jd_id and userinfo.id = comminfo.usr_id and jdinfo.id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        # self.close_sql(cu, self.con())
        return results

    def search_info (self,info):

        cu = self.con().cursor()
        results = cu.execute("select jiname,jdwhere,img1,introudec,id from jdinfo where introudec like ?", ('%'+info+'%',))
        # self.close_sql(cu, self.con())
        return results

    def search_foodinfo(self, foodinfo):
        cu = self.con().cursor()
        results = cu.execute("select foodname,introudec,img from foodinfo where foodname like ?", ('%' + foodinfo + '%',))
        # self.close_sql(cu, self.con())
        return results

    def search_hotleinfo(self, info):
        cu = self.con().cursor()
        results = cu.execute("select hotlename,introudec,img  from hotleinfo where hotlename like ?", ('%' + info + '%',))
        # self.close_sql(cu, self.con())
        return results

    def yanzhe_user(self,name,password):
        sql = "SELECT id,name,tel,password,img FROM userinfo where tel=:st_name and password=:st_pass"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_name': name,'st_pass':password}))
        return results

    def write_comm(self,text,times,jd_id,user_id):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into comminfo(usr_id,jd_id,commentinfo,datetime) values (:usr_id,:jd_id,:comm,:datatime)"
        cu = cx.cursor()
        cu.execute(sql, ({'usr_id': user_id,'jd_id':jd_id,'comm':text,'datatime':times}))
        cx.commit()

    def write_blog(self,b_content,img1,admin_cheak,blog_name,intr,user_id):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into bloginfo(b_content,img1,admin_cheak,blog_name,intr,user_id) values (:b_content,:img1,:admin_cheak,:blog_name,:intr,:user_id)"
        cu = cx.cursor()
        cu.execute(sql, ({'b_content': b_content,'img1': img1,'admin_cheak': admin_cheak,'blog_name': blog_name,'intr': intr,'user_id': user_id}))
        cx.commit()  # 事务提交

    def write_userblog(self,user_blog,admin_cheak,blog_name,intr,user_id,img1):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into bloginfo(user_blog,admin_cheak,blog_name,intr,user_id,img1) values (:user_blog,:admin_cheak,:blog_name,:intr,:user_id,:img1)"
        cu = cx.cursor()
        cu.execute(sql, ({'user_blog': user_blog,'admin_cheak': admin_cheak,'blog_name': blog_name,'intr':intr,'user_id': user_id,'img1':img1}))
        cx.commit()  # 事务提交

    def write_user(self, name, img, tel, password,user_like):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into userinfo(name,img,tel,password,user_like) values (:usr_id,:jd_id,:comm,:datatime,:user_like)"
        cu = cx.cursor()
        cu.execute(sql, ({'usr_id': name, 'jd_id': img, 'comm': tel, 'datatime': password,'user_like':user_like}))
        cx.commit()

    def write_comm(self, text, times, jd_id, user_id):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into comminfo(usr_id,jd_id,commentinfo,datetime) values (:usr_id,:jd_id,:comm,:datatime)"
        cu = cx.cursor()
        cu.execute(sql, ({'usr_id': user_id, 'jd_id': jd_id, 'comm': text, 'datatime': times}))
        cx.commit()

    def write_his(self, a1, usr_id, jdintr, fdintr):
        cx = sqlite3.connect('./DB/travle.db')
        sql = "insert into historyinfo(userid,jdintr,foodintr,datetime) values (:usr_id,:jd_id,:comm,:datatime)"
        cu = cx.cursor()
        cu.execute(sql, ({'usr_id': usr_id, 'jd_id': jdintr, 'comm': fdintr, 'datatime': a1}))
        cx.commit()

    def find_userallhsitory(self,user_id):
         sql = "SELECT *  FROM historyinfo "
         cu = self.con().cursor()
         results = cu.execute(sql)
         # self.close_sql(cu, self.con())
         return results

    def find_jdname(self,id):
        sql = "SELECT jiname FROM jdinfo where id=:st_id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_id': id}))
        # self.close_sql(cu, self.con())
        return results

    def find_jdtype1(self,jdtype,city):
        sql = "select id,sum_sc from jdinfo where jdtype1 =:st_jdtype and city=:st_city"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'st_jdtype': jdtype,'st_city': city}))
        #self.close_sql(cu, self.con())
        return results

    def find_userlike(self, id):
        sql = "select user_like from userinfo where id =:id"
        cu = self.con().cursor()
        results = cu.execute(sql, ({'id': id}))
        # self.close_sql(cu, self.con())
        return results

    def all_num(self, keyword):
        sql = "SELECT COUNT(*) FROM {}".format(keyword)
        cu = self.con().cursor()
        cu.execute(sql)
        result = cu.fetchone()  # 获取查询结果的第一行
        count = int(result[0]) if result is not None else 0  # 将结果转换为整数类型
        # self.close_sql(cu, self.con())
        return count

    def all_num_jd(self):
        sql = "SELECT jdtype, COUNT(*) AS quantity FROM jdinfo GROUP BY jdtype ORDER BY COUNT(*) DESC"
        cu = self.con().cursor()
        result = cu.execute(sql)
        return result

    def all_num_user(self):
        sql = "SELECT name, tel ,user_like FROM userinfo"
        cu = self.con().cursor()
        result = cu.execute(sql)
        return result

    def close_sql(self,cu,cx):
        cx.commit()  # 事务提交
        cu.close()  # 关闭游标

        cx.close()  # 关闭数据库
