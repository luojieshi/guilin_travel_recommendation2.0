import sqlite3  # 导入sqlite3


class sqlite:
    def search_yiqun(t_id):
        cx = sqlite3.connect('./DB/travle.db')  # 创建数据库，如果数据库已经存在，则链接数据库；如果数据库不存在，则先创建数据库，再链接该数据库。
        cu = cx.cursor()  # 定义一个游标，以便获得查询对象。
        sql = "select lon,lat,times from jdinfo where id:=t_id"
        results = cu.execute(sql)
        cu.close()  # 关闭游标
        cx.commit()  # 事务提交
        cx.close()  # 关闭数据库
        return results

