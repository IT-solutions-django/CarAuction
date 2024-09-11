from django.urls import path
from cars.views import index

app_name = 'cars'

urlpatterns = [
    path('products/', index, name='product')
]
