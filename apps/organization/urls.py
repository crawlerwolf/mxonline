# -*- coding: utf-8 -*-
# author = minjie
from django.urls import path, re_path

from .views import OrgListView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView
urlpatterns = [

    # 课程机构列表页
    path('list', OrgListView.as_view(), name='org_list'),
    path('add_ask', UserAskView.as_view(), name='add_ask'),
    re_path('home/(?P<org_id>\d+)', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)', OrgCourseView.as_view(), name='org_course'),
    re_path('desc/(?P<org_id>\d+)', OrgDescView.as_view(), name='org_desc'),
    re_path('org_teacher/(?P<org_id>\d+)', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    path('add_fav', AddFavView.as_view(), name='add_fav'),

    # 课程机构讲师列表页
    path('teacher/list', TeacherListView.as_view(), name='teacher_list'),

    # 课程机构讲师详情页
    re_path('teacher/list/detai/(?P<teacher_id>\d+)', TeacherDetailView.as_view(), name='teacher_detail'),

]