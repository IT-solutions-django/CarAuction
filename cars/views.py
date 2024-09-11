from django.shortcuts import render
from cars.models import Car


def index(request):
    cars = Car.objects.select_related('model_id', 'mark_id', 'country_id').all()

    return render(request, 'index.html', {'cars': cars})
