from django.urls import path
from review_company.views import company_reviews_page

app_name = 'review_company'

urlpatterns = [
    path('yandex/', company_reviews_page, {'company_name': 'Яндекс'}, name='yandex'),
    path('2GIS/', company_reviews_page, {'company_name': '2GIS'}, name='2GIS'),
]
