from django.db import models


class Chanel(models.Model):
    url = models.URLField(verbose_name='Сслыка на канал', help_text='Введите ссылку на канал')
    playlists = models.ManyToManyField('PlayList', related_name='channels', verbose_name='Плей-лист',
                                       help_text='Выберите плей-лист', through='ChannelPlayList')

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return self.url


class PlayList(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название плей-листа', help_text='Введите название плей-листа')
    playlist_id = models.CharField(max_length=255, verbose_name='ID плейлиста', help_text='Введите ID плейлиста')
    video = models.ManyToManyField('Video', related_name='playlists', verbose_name='Видео', help_text='Выберите видео')

    class Meta:
        verbose_name = 'Плей-лист'
        verbose_name_plural = 'Плей-листы'

    def __str__(self):
        return f'Название плей-листа: {self.name}'


class ChannelPlayList(models.Model):
    channel = models.ForeignKey('Chanel', on_delete=models.CASCADE)
    playlist = models.ForeignKey('PlayList', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь Канал->Плей-лист'
        verbose_name_plural = 'Связи Каналы->Плей-листы'

    def __str__(self):
        return f'Канал: {self.channel.url} | Плей-лист: {self.playlist.name}'


class Video(models.Model):
    title = models.CharField(max_length=512, verbose_name='Название видео', help_text='Введите название видео')
    description = models.TextField(verbose_name='Описание видео', help_text='Введите описание видео')
    video_id = models.CharField(max_length=255, verbose_name='ID видео', help_text='Введите ID видео')
    url_shorts = models.URLField(max_length=512, blank=True, null=True, verbose_name='Ссылка на скачивание Shorts',
                                 help_text='Ссылка на скачивание видео Shorts')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        playlists_names = ", ".join(playlist.name for playlist in self.playlists.all())
        return f'Название видео: {self.title} | Плейлисты: {playlists_names}'
