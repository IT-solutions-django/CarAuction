from django.shortcuts import render
from cars.models import (Car, UniqueMarkModel, UniqueCarColor,
                         UniqueCarKpp, UniqueCarPrivod, UniqueCarModel, UniqueCarPw)
from django.core.paginator import Paginator
from cars.forms import CarFilterForm
from django.db.models import Q
from cars.cars_settings import CarYearEnum, CarEngVEnum


def index(request):
    cars = Car.objects.select_related('model_id', 'mark_id', 'country_id', 'kuzov_id', 'color_id').all()
    paginator = Paginator(cars, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})


def page_filter(request):
    filter_fields = {
        'mark_id': (UniqueMarkModel.objects.values_list('name', flat=True), False, True),
        'color_id': (UniqueCarColor.objects.values_list('name', flat=True), 'true_color', True),
        'kpp_type': (UniqueCarKpp.objects.values_list('name', flat=True), 'true_kpp', True),
        'priv_id': (UniqueCarPrivod.objects.values_list('name', flat=True), 'true_priv', True),
        'model_id': (
            UniqueCarModel.objects.filter(mark_name=(request.GET['mark_id'] if request.GET else '')).values_list('name',
                                                                                                                 flat=True),
            False, True),
        'eng_v': (CarEngVEnum.eng_v_range(), False, False),
        'pw': (UniqueCarPw.objects.values_list('name', flat=True), False, False)
    }

    form = CarFilterForm(request.GET, dynamic_fields=filter_fields)

    cars = Car.objects.select_related('model_id', 'mark_id').all()

    filters = {param: value for param, value in request.GET.items() if param != 'page' and value}

    if filters:
        q_objects = Q()
        year_from = filters.get('year_from', '')
        year_to = filters.get('year_to', '')

        if year_from and year_to:
            q_objects &= Q(year__range=(year_from, year_to))
        elif year_from:
            q_objects &= Q(year__range=(year_from, CarYearEnum.MAX_YEAR.value))
        elif year_to:
            q_objects &= Q(year__range=(CarYearEnum.MIN_YEAR.value, year_to))

        for field, value in filters.items():
            if field in ['year_from', 'year_to']:
                continue
            else:
                if filter_fields[field][1]:
                    q_objects &= Q(**{filter_fields[field][1]: value})
                elif filter_fields[field][2]:
                    q_objects &= Q(**{f'{field}__name': value})
                else:
                    q_objects &= Q(**{field: value})
        cars = cars.filter(q_objects)

    paginator = Paginator(cars, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cars': page_obj,
        'form': form,
    }

    return render(request, 'page_filter.html', context)
