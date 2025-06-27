# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class ATravelConfig(AppConfig):
    name = 'aTravel'
    verbose_name = '信息管理'

# 每个应用（app）都需要定义一个 apps.py 文件，用于配置应用的基本信息。
# 如应用的名称、显示名称、图标、默认路径、启动时需要执行的操作等。
# apps.py 文件是一个 Python 模块，需要继承自 django.apps.AppConfig 类，
# 并且定义多种类属性和方法，以便 Django 可以正确地加载和管理应用。
