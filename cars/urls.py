from django.urls import path
from cars.views import index, page_filter

app_name = 'cars'

urlpatterns = [
    path('products/', index, name='product'),
    path('filters/', page_filter, name='filters')
]
