from django.db import models
from django.contrib.postgres.fields import ArrayField


class Company(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название компании', help_text='Введите название компании')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name


class Review(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Компания',
                                help_text='Введите компанию')
    avg_review = models.CharField(max_length=10, verbose_name='Средняя оценка', help_text='Введите среднюю оценку')
    count_review = models.IntegerField(verbose_name='Количество отзывов', help_text='Введите количество отзывов')
    reviews = ArrayField(
        models.TextField(),
        verbose_name='Отзывы',
        help_text='Введите отзывы'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзывы для компании {self.company.name}'
