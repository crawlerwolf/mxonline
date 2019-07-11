# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMinxin


class CustomBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class IndexView(View):
    """
    慕学在线网首页
    """
    def get(self, request):
        # 去除轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogOutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '恭喜你成功注册慕学在线网会员'
            user_message.save()

            # 发送注册激活链接
            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    """
    用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                record.delete()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ResetView(View):
    """
    用户重置密码
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                record.delete()
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class ForgetPwdView(View):
    """
    用户忘记密码
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class UserInfoView(LoginRequiredMinxin, View):
    """
    用户中心用户个人信息
    """
    def get(self, request):
        current_tag = 'UserInfo'
        return render(request, 'usercenter-info.html', {
            'current_tag': current_tag,
        })

    # 修改个人中心用户信息
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMinxin, View):
    """
    用户中心用户头像修改
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']
        #     request.user.image = image
        #     request.user.save()
        #     return HttpResponse('{"status":"success"}', content_type='application/json')


class UpDataPwdView(View):
    """
    用户中心界面修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMinxin, View):
    """
    用户中心发送邮箱验证码
    """
    def get(self, request):
        emali = request.GET.get('email', '')
        if UserProfile.objects.filter(email=emali):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(emali, 'updata_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpDateEmailView(LoginRequiredMinxin, View):
    """
    用户中心修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='updata_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            existed_records.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMinxin, View):
    """
       用户中心用户课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        current_tag = 'UserCourse'
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'current_tag': current_tag,
        })


class MyFavOrgView(LoginRequiredMinxin, View):
    """
       用户中心用户收藏的机构
    """
    def get(self, request):
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_list = [CourseOrg.objects.get(id=fav_org.fav_id) for fav_org in fav_orgs]
        current_tag = 'UserFav'
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_tag': current_tag,
        })


class MyFavTeacherView(LoginRequiredMinxin, View):
    """
       用户中心用户收藏的机构
    """
    def get(self, request):
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_list = [Teacher.objects.get(id=fav_teacher.fav_id) for fav_teacher in fav_teachers]
        current_tag = 'UserFav'
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_tag': current_tag,
        })


class MyFavCourseView(LoginRequiredMinxin, View):
    """
       用户中心用户收藏的机构
    """
    def get(self, request):
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_list = [Course.objects.get(id=fav_course.fav_id) for fav_course in fav_courses]
        current_tag = 'UserFav'
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_tag': current_tag,
        })


class MyMessageView(LoginRequiredMinxin, View):
    """
       用户中心用户消息
    """
    def get(self, request):

        # 将未读信息转为已读信息
        all_message_unread = UserMessage.objects.filter(user=request.user.id, has_read=False).all()
        for message_unread in all_message_unread:
            message_unread.has_read = True
            message_unread.save()

        # 获取所有已读信息
        all_message = UserMessage.objects.filter(user=request.user.id).all()
        # 获取所有已读信息
        all_message = all_message.order_by('-add_time')
        current_tag = 'UserMsg'

        # 对用户信息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_message': messages,
            'current_tag': current_tag,
        })


def page_not_found_view(request, exception=None):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def server_error_view(request, exception=None):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
