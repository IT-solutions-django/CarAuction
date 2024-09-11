from django.urls import path
from cars.api.v1.views import ListPrivodView, ListKPPView, ListColorView, ListModelView

app_name = 'cars'

urlpatterns = [
    path('privod/', ListPrivodView.as_view(), name='privod'),
    path('kpp/', ListKPPView.as_view(), name='kpp'),
    path('color/', ListColorView.as_view(), name='color'),
    path('model/', ListModelView.as_view(), name='model'),
]
