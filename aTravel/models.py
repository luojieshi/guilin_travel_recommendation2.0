# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from tinymce.models import HTMLField


class Comminfo(models.Model):
    id = models.AutoField(primary_key=True)
    usr_id = models.IntegerField()
    jd_id = models.IntegerField()
    commentinfo = models.TextField(blank=True, null=True)
    datetime = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comminfo'

class Historyinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.IntegerField(blank=True, null=True)
    jdintr = models.TextField(blank=True, null=True)
    foodintr = models.TextField(blank=True, null=True)
    datetime = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historyinfo'
        verbose_name = "历史规划"
        verbose_name_plural = "历史规划"


class Foodinfo(models.Model):
    id = models.AutoField(primary_key=True)
    foodname = models.CharField(max_length=100, blank=True, null=True)
    introudec = models.CharField(max_length=300, blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foodinfo'
        verbose_name = "美食信息"
        verbose_name_plural = "美食信息"


class Hotleinfo(models.Model):
    id = models.AutoField(primary_key=True)
    hotlename = models.CharField(max_length=100, blank=True, null=True)
    introudec = models.CharField(max_length=300, blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'hotleinfo'
        verbose_name = "酒店信息"
        verbose_name_plural = "酒店信息"


class Jdinfo(models.Model):
    id = models.AutoField(primary_key=True)
    jiname = models.CharField(max_length=100, blank=True, null=True)
    jdtype = models.CharField(max_length=30, blank=True, null=True)
    jdwhere = models.CharField(max_length=100, blank=True, null=True)
    times = models.CharField(max_length=30, blank=True, null=True)
    lon = models.CharField(max_length=50, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    sum_sc = models.CharField(max_length=10, blank=True, null=True)
    jd_sc = models.CharField(max_length=10, blank=True, null=True)
    yq_sc = models.CharField(max_length=10, blank=True, null=True)
    xj_sc = models.CharField(max_length=10, blank=True, null=True)
    img1 = models.CharField(max_length=100, blank=True, null=True)
    img2 = models.CharField(max_length=100, blank=True, null=True)
    img3 = models.CharField(max_length=100, blank=True, null=True)
    introudec = models.CharField(max_length=300, blank=True, null=True)
    jdtype1 = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jdinfo'
        verbose_name = "景点信息"
        verbose_name_plural = "景点信息"


class Trficinfo(models.Model):
    id = models.AutoField(primary_key=True)
    trname = models.CharField(max_length=30, blank=True, null=True)
    trtype = models.CharField(max_length=30, blank=True, null=True)
    trprice = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trficinfo'


class Userinfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    tel = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    user_like = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinfo'
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

class Bloginfo(models.Model):
    id = models.AutoField(primary_key=True)
    b_content = models.TextField()
    user_id = models.TextField(blank=True, null=True)
    hot_index = models.TextField(blank=True, null=True)
    admin_cheak = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    img1 = models.TextField(blank=True, null=True)
    intr = models.TextField(blank=True, null=True)
    hit_num = models.TextField(blank=True, null=True)
    blog_name = models.TextField(blank=True, null=True)
    user_blog = HTMLField()


    class Meta:
        managed = False
        db_table = 'bloginfo'
        verbose_name = "攻略信息"
        verbose_name_plural = "攻略信息"

