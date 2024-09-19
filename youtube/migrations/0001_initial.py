# Generated by Django 5.1.1 on 2024-09-18 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chanel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='Введите ссылку на канал', verbose_name='Сслыка на канал')),
            ],
            options={
                'verbose_name': 'Канал',
                'verbose_name_plural': 'Каналы',
            },
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название плей-листа', max_length=256, verbose_name='Название плей-листа')),
                ('playlist_id', models.CharField(help_text='Введите ID плейлиста', max_length=255, verbose_name='ID плейлиста')),
            ],
            options={
                'verbose_name': 'Плей-лист',
                'verbose_name_plural': 'Плей-листы',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название видео', max_length=512, verbose_name='Название видео')),
                ('description', models.TextField(help_text='Введите описание видео', verbose_name='Описание видео')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
            },
        ),
        migrations.CreateModel(
            name='ChannelPlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtube.chanel')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youtube.playlist')),
            ],
        ),
        migrations.AddField(
            model_name='chanel',
            name='playlists',
            field=models.ManyToManyField(help_text='Выберите плей-лист', related_name='channels', through='youtube.ChannelPlayList', to='youtube.playlist', verbose_name='Плей-лист'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='video',
            field=models.ManyToManyField(help_text='Выберите видео', related_name='playlists', to='youtube.video', verbose_name='Видео'),
        ),
    ]
