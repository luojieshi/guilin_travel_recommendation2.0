# 路由文件夹，配置后端接口，映射网址路由
""""guilin_travel_recommendation2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from aTravel import views

# 将特定的URL映射到视图函数：
# 要在浏览器中访问我们设置的视图view，我们需要将其映射到一个 URL。为此我们需要定义一个 URL 配置，使服务端接收请求返回响应
# 简称为 "URLconf"。这些 URL 配置是在每个 Django 应用程序内部定义的，它们是名为 urls.py 的 Python 文件。

urlpatterns = [

    # include()函数将tinymce应用的urls.py文件引入到主urls.py文件中，
    # 并将URL前缀设置为’tinymce/’（使用正则匹配）。
    # 这样，当用户访问以’tinymce/’开头的URL时，Django将会将请求交给tinymce应用中定义的视图函数处理。
    # url()将对应的路径请求映射到视图函数中处理

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^$', views.addindex, name='addindex'),
    url(r'^result', views.result, name='result2'),
    url('reg/', views.reg, name='check'),
    url(r'^index', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^jdhtml', views.jdhtml, name='jdhtml'),
    url(r'^jdDetails/(?P<id>\d+)/$', views.jdDetails, name='jdDetails'),
    url(r'^search', views.search, name='search'),
    url(r'^addindex$', views.addindex, name='addindex'),
    url(r'^addindex[0-99]', views.addindex_number, name='addindex_number'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^regist', views.regist, name='regist'),
    url(r'^admin', views.adminindex, name='admin'),
    url(r'^jdinfo', views.adminjdlist, name='adminjd'),
    url(r'^foodinfo', views.adminfoodlist, name='adminfd'),
    url(r'^userinfo', views.adminuserlist, name='adminur'),
    url(r'^faq', views.faq, name='faq'),

    # path('addindex/',views.addindex),
    # path('index/', views.index),
    # path('^login/', views.login),
    # path('register/', views.register),
    # path('jdhtml/', views.jdhtml),
    # path('jdDetails/', views.jdDetails),
    # path('admin/', admin.site.urls),
]

# url是Django早期版本中使用的URL配置方式，它使用正则表达式来匹配URL模式。
# path是Django 2.0版本中引入的新的URL配置方式，它使用字符串模式来匹配URL。
# include：当为多个应用构建多个URLconf时，应该始终使用include()来使程序清晰可维护。唯一的例外是admin.site.urls，它是Django为默认管理站点提供的预构建URLconf。
