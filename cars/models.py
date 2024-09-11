from django.db import models
from django.contrib.postgres.fields import ArrayField


class Car(models.Model):
    auction_date = models.DateField(verbose_name='Дата аукциона')
    auction = models.CharField(max_length=1024, verbose_name='Название аукциона')
    year = models.IntegerField(verbose_name='Год автомобиля')
    eng_v = models.IntegerField()
    pw = models.CharField(max_length=256, blank=True, null=True)
    grade = models.CharField(max_length=1024, null=True, blank=True)
    mileage = models.IntegerField(verbose_name='Пробег')
    equip = models.CharField(max_length=256)
    rate = models.CharField(max_length=10)
    finish = models.IntegerField()
    images = ArrayField(
        models.URLField(),
        size=3,
        verbose_name='Фотографии'
    )
    true_priv = models.CharField(max_length=512)
    true_color = models.CharField(max_length=512)
    model_id = models.ForeignKey('Model', on_delete=models.CASCADE, verbose_name='Модель автомобиля')
    mark_id = models.ForeignKey('Mark', on_delete=models.CASCADE, verbose_name='Марка автомобиля')
    kuzov_id = models.ForeignKey('Kuzov', on_delete=models.CASCADE, verbose_name='Кузов автомобиля')
    color_id = models.ForeignKey('Color', on_delete=models.CASCADE, verbose_name='Цвет автомобиля', blank=True,
                                 null=True)
    kpp_type = models.ForeignKey('KppType', on_delete=models.CASCADE, verbose_name='КПП автомобиля')
    priv_id = models.ForeignKey('Privod', on_delete=models.CASCADE, verbose_name='Привод автомобиля', blank=True,
                                null=True)
    country_id = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна автомобиля')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.auction} | {self.auction_date} | {self.mark_id.name} | {self.model_id.name}'


class Model(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название модели автомобиля')

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'

    def __str__(self):
        return self.name


class Mark(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название марки автомобиля')

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'

    def __str__(self):
        return self.name


class Kuzov(models.Model):
    name = models.CharField(max_length=512, verbose_name='Название кузова автомобиля')

    class Meta:
        verbose_name = 'Кузов автомобиля'
        verbose_name_plural = 'Кузова автомобилей'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название цвета автомобиля')

    class Meta:
        verbose_name = 'Цвет автомобиля'
        verbose_name_plural = 'Цвета автомобилей'

    def __str__(self):
        return self.name


class KppType(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название КПП автомобиля')

    class Meta:
        verbose_name = 'Вид КПП автомобиля'
        verbose_name_plural = 'Виды КПП автомобилей'

    def __str__(self):
        return self.name


class Privod(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название привода автомобиля')

    class Meta:
        verbose_name = 'Вид привода автомобиля'
        verbose_name_plural = 'Виды приводов автомобилей'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название страны автомобиля')

    class Meta:
        verbose_name = 'Страна автомобиля'
        verbose_name_plural = 'Страны автомобилей'

    def __str__(self):
        return self.name
