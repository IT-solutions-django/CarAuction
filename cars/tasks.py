from celery import shared_task
from cars.models import Car, Currency, UniqueMarkModel
import requests
from decimal import Decimal
from django.apps import apps


# Таска для получения списка машин по марке, цвету и другим параметрам
@shared_task
def update_or_create_model(model_class_name, name_field, true_param=None):
    model_class = apps.get_model('cars', model_class_name)

    cars = Car.objects.select_related(name_field, 'model_id', 'mark_id').all()

    mark_car_map = {}

    for car in cars:
        if true_param:
            if hasattr(car, true_param):
                true_param_value = getattr(car, true_param)
            else:
                true_param_value = None
        else:
            true_param_value = None

        if true_param_value is None or true_param_value == '':
            mark = getattr(car, name_field).name
        else:
            mark = true_param_value

        if mark not in mark_car_map:
            mark_car_map[mark] = set()

        mark_car_map[mark].add(f'{car.mark_id.name} {car.model_id.name} {car.year}')

    for mark, car_set in mark_car_map.items():
        car_str = ', '.join(str(car) for car in car_set)
        model_class.objects.update_or_create(
            name=mark,
            defaults={'cars': car_str}
        )


@shared_task
def update_all_models():
    update_or_create_model.delay('UniqueMarkModel', 'mark_id')
    update_or_create_model.delay('UniqueCarColor', 'color_id', 'true_color')


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
