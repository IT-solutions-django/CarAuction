from django.shortcuts import render
from cars.models import Car
from django.core.paginator import Paginator


def index(request):
    cars = Car.objects.select_related('model_id', 'mark_id', 'country_id', 'kuzov_id', 'color_id').all()
    paginator = Paginator(cars, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})


def page_filter(request):
    return render(request, 'page_filter.html')
