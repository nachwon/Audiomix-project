# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 12:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_post_mixed_tracks2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mixedtrack',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='mixedtrack',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='mixed_tracks2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='mixed_tracks',
        ),
        migrations.AddField(
            model_name='post',
            name='mixed_tracks',
            field=models.ForeignKey(default='51', on_delete=django.db.models.deletion.CASCADE, related_name='mixed_tracks', to='posts.CommentTrack'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MixedTrack',
        ),
    ]
