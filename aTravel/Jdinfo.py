from aTravel.sqlsqlit import sqlinfo


class Jdinfo:
    def __init__(self,jdname,jdtype,jdtime,lon,lat,sum_sc,jd_sc,yq_sc,xj_sc,img1,img2,img3,intr):
        self.jdname=jdname
        self.jdtype=jdtype
        self.jdtime=jdtime
        self.lon=lon
        self.lat=lat
        self.sum_sc=sum_sc
        self.jd_sc=jd_sc
        self.yq_sc=yq_sc
        self.xj_sc=xj_sc
        self.img1=img1
        self.img2 = img2
        self.img3 = img3
        self.intr = intr

    def hotJD(self):
        sh = sqlinfo()
        jdinfo = sh.hot_jdinfo()
        k ={}
        for r in jdinfo:
            k['']
        return jdinfo

#
# jdinfo =[Jdinfo()]*2
# jdinfo[0].yq_sc=0;
# jdinfo[0].img1=1;

