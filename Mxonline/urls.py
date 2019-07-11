# -*- coding: utf-8 -*-
"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView  # 处理静态文件
from django.views.static import serve  # 处理静态文件

import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogOutView, IndexView
from Mxonline.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 用''指代根目录，TemplateView.as_view可以将template转换为view
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # 用户登录\注册\修改密码\邮箱验证及验证码url配置
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),  # 验证码
    re_path('user_active/(?P<active_code>.*)', ActiveUserView.as_view(), name='user_active'),
    path('forget', ForgetPwdView.as_view(), name='forgetpwd'),
    re_path('reset/(?P<active_code>.*)', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd', ModifyPwdView.as_view(), name='modify_pwd'),

    # 配置上传文件的处理
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    # 配置静态文件
    re_path('static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),

    # 课程机构url配置
    path('org/', include(('organization.urls', 'organization'), namespace='org')),

    # 课程url配置
    path('course/', include(('courses.urls', 'courses'), namespace='course')),

    # 用户url配置
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),

]

# 全局404页面的配置
handler404 = 'users.views.page_not_found_view'

# 全局500页面的配置
handler500 = 'users.views.server_error_view'
