from django.db import models
from django.contrib.postgres.fields import ArrayField


class NamedEntity(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название', help_text='Введите название')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Car(models.Model):
    auction_date = models.DateField(verbose_name='Дата аукциона', help_text='Выберите дату проведения аукциона')
    auction = models.CharField(max_length=1024, verbose_name='Название аукциона', help_text='Введите название аукциона')
    year = models.IntegerField(verbose_name='Год автомобиля', help_text='Введите год автомобиля')
    eng_v = models.IntegerField()
    pw = models.CharField(max_length=256, blank=True, null=True)
    grade = models.CharField(max_length=1024, null=True, blank=True)
    mileage = models.IntegerField(verbose_name='Пробег', help_text='Введите пробег автомобиля')
    equip = models.CharField(max_length=256)
    rate = models.CharField(max_length=10)
    finish = models.IntegerField()
    expenses_rus = models.IntegerField(verbose_name='Расходы в России', help_text='Введите число расходов в России',
                                       blank=True, null=True)
    expenses_jpn = models.IntegerField(verbose_name='Расходы по стране экспортера',
                                       help_text='Введите число расходов по стране экспортера', blank=True, null=True)
    update_date = models.DateField(auto_now=True, verbose_name='Дата обновления записи')
    images = ArrayField(
        models.URLField(),
        size=3,
        verbose_name='Фотографии',
        help_text='Введите ссылки на изображения автомобиля через запятую'
    )
    true_priv = models.CharField(max_length=512)
    true_color = models.CharField(max_length=512)
    true_kpp = models.CharField(max_length=512)
    model_id = models.ForeignKey('Model', on_delete=models.CASCADE, verbose_name='Модель автомобиля',
                                 help_text='Выберите модель автомобиля')
    mark_id = models.ForeignKey('Mark', on_delete=models.CASCADE, verbose_name='Марка автомобиля',
                                help_text='Выберите марку автомобиля')
    kuzov_id = models.ForeignKey('Kuzov', on_delete=models.CASCADE, verbose_name='Кузов автомобиля',
                                 help_text='Выберите кузов автомобиля')
    color_id = models.ForeignKey('Color', on_delete=models.CASCADE, verbose_name='Цвет автомобиля', blank=True,
                                 null=True, help_text='Выберите цвет автомобиля')
    kpp_type = models.ForeignKey('KppType', on_delete=models.CASCADE, verbose_name='КПП автомобиля',
                                 help_text='Выберите тип КПП')
    priv_id = models.ForeignKey('Privod', on_delete=models.CASCADE, verbose_name='Привод автомобиля', blank=True,
                                null=True, help_text='Выберите тип привода автомобиля')
    country_id = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна автомобиля',
                                   help_text='Выберите страну производителя автомобиля')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f'{self.auction} | {self.auction_date} | {self.mark_id.name} | {self.model_id.name}'


class Model(NamedEntity):
    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'


class Mark(NamedEntity):
    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'


class Kuzov(NamedEntity):
    class Meta:
        verbose_name = 'Кузов автомобиля'
        verbose_name_plural = 'Кузова автомобилей'


class Color(NamedEntity):
    class Meta:
        verbose_name = 'Цвет автомобиля'
        verbose_name_plural = 'Цвета автомобилей'


class KppType(NamedEntity):
    class Meta:
        verbose_name = 'Вид КПП автомобиля'
        verbose_name_plural = 'Виды КПП автомобилей'


class Privod(NamedEntity):
    class Meta:
        verbose_name = 'Вид привода автомобиля'
        verbose_name_plural = 'Виды приводов автомобилей'


class Country(NamedEntity):
    class Meta:
        verbose_name = 'Страна автомобиля'
        verbose_name_plural = 'Страны автомобилей'


class UniqueEntity(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название параметра', help_text='Введите название параметра')
    cars = models.TextField(verbose_name='Список машин', help_text='Введите список машин')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name} | [{self.cars}]'


class UniqueMarkModel(UniqueEntity):
    class Meta:
        verbose_name = 'Список машин по марке'
        verbose_name_plural = 'Списки машин по маркам'


class UniqueCarColor(UniqueEntity):
    class Meta:
        verbose_name = 'Список машин по цвету'
        verbose_name_plural = 'Списки машин по цветам'


class Currency(models.Model):
    type = models.CharField(max_length=128, verbose_name='Тип валюты', help_text='Введите название валюты')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Значение валюты',
                                help_text='Введите значение валюты')
    date = models.DateField(auto_now=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return f'{self.type}:{self.value} | {self.date}'
