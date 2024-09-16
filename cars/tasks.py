from celery import shared_task
from cars.models import Car, Currency, UniqueMarkModel
import requests
from decimal import Decimal
from django.apps import apps
from django.db.models.fields.related import ForeignKey


# Таска для получения уникальных марок, моделей, цветов и других параметров
@shared_task
def update_or_create_model(model_class_name, field_name, true_parameter=None):
    model_class = apps.get_model('cars', model_class_name)
    if model_class_name == 'UniqueCarModel':
        cars = Car.objects.select_related('mark_id').all()
        list_parameters = {}
        for car in cars:
            field_value = getattr(car, field_name).name
            if field_value not in list_parameters:
                list_parameters[field_value] = car.mark_id.name

        for model_name, mark_name in list_parameters.items():
            model_class.objects.get_or_create(name=model_name, mark_name=mark_name)
    else:
        field = Car._meta.get_field(field_name)

        if isinstance(field, ForeignKey):
            cars = Car.objects.select_related(field_name).all()
        else:
            cars = Car.objects.all()

        list_parameters = []

        for car in cars:
            if true_parameter is not None and hasattr(car, true_parameter):
                true_value = getattr(car, true_parameter)
                if true_value:
                    list_parameters.append(true_value)
            else:
                field_value = getattr(car, field_name)
                if isinstance(field_value, ForeignKey):
                    list_parameters.append(field_value.name if field_value else None)
                else:
                    list_parameters.append(field_value)

        unique_parameters = set(filter(None, list_parameters))

        for param in unique_parameters:
            model_class.objects.get_or_create(name=param)


@shared_task
def update_all_models():
    update_or_create_model.delay('UniqueMarkModel', 'mark_id')
    update_or_create_model.delay('UniqueCarColor', 'color_id', 'true_color')
    update_or_create_model.delay('UniqueCarKpp', 'kpp_type', 'true_kpp')
    update_or_create_model.delay('UniqueCarPrivod', 'priv_id', 'true_priv')
    update_or_create_model.delay('UniqueCarModel', 'model_id')
    update_or_create_model.delay('UniqueCarPw', 'pw')


# Таска для парсинга валют
@shared_task
def parsing_currency():
    url = 'http://auc.autocenter25.com/currency'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        for currency_type, value in data.items():
            if currency_type != 'date':
                Currency.objects.update_or_create(
                    type=currency_type,
                    defaults={'value': Decimal(value)}
                )
