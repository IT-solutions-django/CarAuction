from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarAuction.settings')

django.setup()

from review_company.models import Company, Review

driver = webdriver.Safari()

driver.get('https://2gis.ru/vladivostok/geo/3518965490157296')

time.sleep(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

soup = BeautifulSoup(driver.page_source, 'html.parser')

rating = soup.find('div', class_='_y10azs').text

driver.get('https://2gis.ru/vladivostok/firm/3518965490157296/tab/reviews')

time.sleep(3)

soup_2 = BeautifulSoup(driver.page_source, 'html.parser')

reviews_count = soup_2.find('span', class_='_1xhlznaa').text

reviews_elements = driver.find_elements(By.XPATH, "//div[contains(@class, '_49x36f')]")
reviews = [review.text for review in reviews_elements]

driver.quit()

company, _ = Company.objects.get_or_create(name='2GIS')

Review.objects.get_or_create(company=company, avg_review=rating, count_review=reviews_count, reviews=reviews)
