# -*- coding: utf-8 -*-
# author = minjie
from django.urls import path, re_path

from .views import UserInfoView, UploadImageView, UpDataPwdView, SendEmailCodeView
from .views import UpDateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 用户信息
    path('info', UserInfoView.as_view(), name='users_info'),

    # 用户头像上传
    path('image/upload', UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    path('updata/pwd', UpDataPwdView.as_view(), name='updata_pwd'),

    # 用户个人中心发送修改邮箱验证码
    path('sendemail_code', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 用户个人中心修改邮箱
    path('update_email', UpDateEmailView.as_view(), name='update_email'),

    # 用户个人中心我的课程
    path('mycourse', MyCourseView.as_view(), name='mycourse'),

    # 用户个人中心我收藏的机构
    path('myfav/org', MyFavOrgView.as_view(), name='myfav_org'),

    # 用户个人中心我收藏的讲师
    path('myfav/teacher', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 用户个人中心我收藏的课程
    path('myfav/course', MyFavCourseView.as_view(), name='myfav_course'),

    # 用户个人中心我的消息
    path('mymessage', MyMessageView.as_view(), name='mymessage'),

]