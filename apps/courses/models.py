# _*_ coding: utf-8 _*_
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):  # 添加功能 课程
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    # detail = models.TextField(verbose_name=u'课程详情')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300,
            imagePath="courses/ueditor/", filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    degree = models.CharField(verbose_name=u'课程难度', choices=(('cj', u'初级'), ('zj', u'中级'),('gj', u'高级')), max_length=2)
    need_know = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u'课程讲师', null=True, blank=True)
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u'老师告诉你')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'课程封面', max_length=100, null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name=u'课程标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    # 定义后台显示名称
    get_zj_nums.short_description = u'章节数'

    def go_to(self):
        # 防止django文本转换
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</>')
    # 定义后台显示名称
    go_to.short_description = u'跳转'

    def get_learn_users(self):
        # 获取课程学习人数
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):  # 一张表中多个管理器（课程）
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 具有model的功能并且不会再生成表单


class Lesson(models.Model):  # 添加功能 课程章节
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取视频
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):  # 添加功能 章节视频
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):  # 添加功能 视频资源
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
