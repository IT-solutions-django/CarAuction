from django.db import models


class Chanel(models.Model):
    url = models.URLField(verbose_name='Сслыка на канал', help_text='Введите ссылку на канал')

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return self.url


class PlayList(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название плей-листа', help_text='Введите название плей-листа')
    playlist_id = models.CharField(max_length=255, verbose_name='ID плейлиста', help_text='Введите ID плейлиста')
    chanel = models.ForeignKey('Chanel', on_delete=models.CASCADE, verbose_name='Канал', help_text='Введите канал')

    class Meta:
        verbose_name = 'Плей-лист'
        verbose_name_plural = 'Плей-листы'

    def __str__(self):
        return f'Название плей-листа: {self.name} | Канал: {self.chanel.url}'


class Video(models.Model):
    title = models.CharField(max_length=512, verbose_name='Название видео', help_text='Введите название видео')
    description = models.TextField(verbose_name='Описание видео', help_text='Введите описание видео')
    playlist = models.ForeignKey('PlayList', on_delete=models.CASCADE, verbose_name='Плей-лист',
                                 help_text='Укажите плей-лист')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'Плей-лист: {self.playlist.name} | Название видео: {self.title}'
