# Generated by Django 2.0 on 2019-06-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20190620_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]
