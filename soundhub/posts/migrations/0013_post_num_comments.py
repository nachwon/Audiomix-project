# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_remove_post_num_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_comments',
            field=models.IntegerField(default=0),
        ),
    ]