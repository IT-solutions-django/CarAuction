from selenium import webdriver
from bs4 import BeautifulSoup
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarAuction.settings')

django.setup()

from review_company.models import Company, Review

driver = webdriver.Safari()

driver.get('https://yandex.ru/maps/org/batareyka25rus/23383064574/?ll=131.874975%2C43.110073&z=17')

driver.implicitly_wait(10)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

rating = soup.find('span', class_='business-rating-badge-view__rating-text').text

title = soup.find('div', class_='tabs-select-view__title _name_reviews')
review_count = title.find('div', class_='tabs-select-view__counter').text

driver.get('https://yandex.ru/maps/org/batareyka25rus/23383064574/reviews/?ll=131.874975%2C43.110073&z=7')

driver.implicitly_wait(10)

html_2 = driver.page_source

soup_2 = BeautifulSoup(html_2, 'html.parser')

reviews = [review.text for review in soup_2.find_all('span', class_='business-review-view__body-text')][:10]

driver.quit()

company, _ = Company.objects.get_or_create(name='Яндекс')

Review.objects.get_or_create(company=company, avg_review=rating, count_review=review_count, reviews=reviews)
