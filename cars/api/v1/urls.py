from django.urls import path
from cars.api.v1.views import ListColorView, ListDetailView, ListUniqueMarkModelView, ListNotDetailView

app_name = 'cars'

urlpatterns = [
    path('color/', ListColorView.as_view(), name='color'),
    path('<str:field_name>/', ListDetailView.as_view(), name='field_name'),
    path('v2/unique_mark_model/', ListUniqueMarkModelView.as_view(), name='unique_mark_model'),
    path('v3/not_detail/<str:field_name>/', ListNotDetailView.as_view(), name='not_detail')
]
