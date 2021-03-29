from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'myauth'
urlpatterns = [
    path('', views.主页, name='主页'),
    path('login/', views.登录, name='登录'),
    path('logout/', views.登出, name='登出'),
    path('reg/', views.注册, name='注册'),
    path('user_center/', views.个人中心, name='个人中心'),
    path('user_center/edit_profile', views.编辑信息, name='编辑信息'),
    path('user_center/pwd_change', views.修改密码, name='修改密码'),

]
