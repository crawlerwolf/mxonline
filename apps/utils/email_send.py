# -*- coding: utf-8 -*-
# author = minjie
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM


def random_str(random_length=8):
    make_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        make_str += chars[random.randint(0, length)]
    return make_str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'updata_email':
        code = random_str(6)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = u'慕学在线网注册激活链接'
        email_body = u'请点击下面的链接激活你的账号: http://127.0.0.1:8000/user_active/{}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = u'慕学在线网账户密码重置链接'
        email_body = u'请点击下面的链接重置账号密码: http://127.0.0.1:8000/reset/{}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'updata_email':
        email_title = u'慕学在线网邮箱修改验证码'
        email_body = u'邮箱验证码: {}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
