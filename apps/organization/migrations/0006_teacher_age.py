# Generated by Django 2.0 on 2019-06-24 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='教师年龄'),
        ),
    ]
