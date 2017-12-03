# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 11:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20171203_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
            options={
                'ordering': ['liked_date'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(related_name='liked_posts', through='posts.PostLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
