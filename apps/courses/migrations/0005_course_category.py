# Generated by Django 2.0 on 2019-06-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=20, verbose_name='课程类别'),
        ),
    ]