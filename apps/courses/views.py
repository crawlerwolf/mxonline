# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMinxin
# Create your views here.


class CourseListView(View):

    def get(self, request):
        # 所有课程按加入时间排序
        all_courses = Course.objects.all().order_by('-add_time')

        # 热门课程按点击数排序
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 搜索关键词
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = Course.objects.filter(
                Q(name__icontains=search_keywords)
                | Q(desc__icontains=search_keywords)
                | Q(detail__icontains=search_keywords)
            )

        # 课程排序
        sort_type = request.GET.get('sort', '')
        if sort_type:
            if sort_type == 'students':
                # 取出学习人数并排序（倒序）
                all_courses = all_courses.order_by('-students')
            elif sort_type == 'hot':
                # 取出热门课程数并排序（倒序）
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort_type,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            # 课程收藏判断
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course = True
            # 机构收藏判断
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMinxin, View):
    """
    章节详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否关联了此课程
        has_course = UserCourse.objects.filter(user=request.user, course=course)
        if not has_course:
            has_course = UserCourse(user=request.user, course=course)
            has_course.save()
            # 学习人数加1
            course.students += 1
            course.save()
            
        # 获取学过此课程所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 获取学过此课程所有用户的ID
        user_ids = [user_course.user_id for user_course in user_courses]
        # 获取学过此课程所有用户的课程
        all_users_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取学过此课程所有用户学习过的其他所有课程的ID
        course_ids = [user_course.course.id for user_course in all_users_courses if
                      user_course.course.id != int(course_id)]
        # 获取学过此课程所有用户学习过的其他所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMinxin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 获取学过此课程所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 获取学过此课程所有用户的ID
        user_ids = [user_course.id for user_course in user_courses]
        # 获取学过此课程所有用户的课程
        all_users_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取学过此课程所有用户学习过的其他所有课程的ID
        course_ids = [user_course.course.id for user_course in all_users_courses if
                      user_course.course.id != int(course_id)]
        # 获取学过此课程所有用户学习过的其他所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        course_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.all().order_by('add_time')

        # 对评论进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(course_comments, 5, request=request)
        course_comment = p.page(page)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'course_comments': course_comment,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论添加失败！"}', content_type='application/json')


class VideoPlayView(View):
    """
    课程视频
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 查询用户是否关联了此课程
        has_course = UserCourse.objects.filter(user=request.user, course=course)
        if not has_course:
            has_course = UserCourse(user=request.user, course=course)
            has_course.save()
            # 学习人数加1
            course.students += 1
            course.save()

        # 获取学过此课程所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 获取学过此课程所有用户的ID
        user_ids = [user_course.user_id for user_course in user_courses]
        # 获取学过此课程所有用户的课程
        all_users_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取学过此课程所有用户学习过的其他所有课程的ID
        course_ids = [user_course.course.id for user_course in all_users_courses if
                      user_course.course.id != int(video.lesson.course.id)]
        # 获取学过此课程所有用户学习过的其他所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
            'video': video,
        })
