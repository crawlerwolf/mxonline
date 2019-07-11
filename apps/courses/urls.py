# -*- coding: utf-8 -*-
# author = minjie
from django.urls import path, re_path

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, VideoPlayView

urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),

    # 课程详情页
    re_path('detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name='course_detail'),

    # 课程章节详情页
    re_path('info/(?P<course_id>\d+)', CourseInfoView.as_view(), name='course_info'),

    # 课程评论
    re_path('comment/(?P<course_id>\d+)', CourseCommentView.as_view(), name='course_comment'),

    # 添加课程评论
    path('add_comment', AddCommentView.as_view(), name='add_comment'),

    # 课程播放页
    re_path('video/(?P<video_id>\d+)', VideoPlayView.as_view(), name='video_play'),

]