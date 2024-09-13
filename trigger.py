# Скрипт для расширения и заполнения полей модели данными пошлины

import os
from datetime import datetime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarAuction.settings')

django.setup()

from cars.models import Car, Currency


def calc_price(price, currency, year, volume, table):
    try:
        if table == "china":
            freight = 15000
            freight_vl = 0
            delivery = 0
            brokerServices = 110_000
            compane_comision = 150_000
            per_price = (35 * price) // 100
            price = price + per_price

        if table == "stats":
            freight_vl = 100_000
            if volume < 1900:
                freight = 100_000
            else:
                freight = 400_000

            delivery = 70_000
            brokerServices = 78_000
            compane_comision = 50_000

        one_rub = currency['jpy'] / 100
        price_rus = round(price / one_rub)
        if table == "china":
            one_rub = currency['cny'] / 100

            price_rus = round(price * one_rub)

        if price_rus < 200000:
            tof = 775
        elif (price_rus < 450000) and (price_rus >= 200000):
            tof = 1550
        elif (price_rus < 1200000) and (price_rus >= 450000):
            tof = 3100
        elif (price_rus < 2700000) and (price_rus >= 1200000):
            tof = 8530
        elif (price_rus < 4200000) and (price_rus >= 2700000):
            tof = 12000
        elif (price_rus < 5500000) and (price_rus >= 4200000):
            tof = 15550
        elif (price_rus < 7000000) and (price_rus >= 5500000):
            tof = 20000
        elif (price_rus < 8000000) and (price_rus >= 7000000):
            tof = 23000
        elif (price_rus < 9000000) and (price_rus >= 8000000):
            tof = 25000
        elif (price_rus < 10000000) and (price_rus >= 9000000):
            tof = 27000
        else:
            tof = 30000

        age = datetime.now().year - year

        if age < 3:
            if volume >= 3500:
                yts = 1235200
            elif (volume >= 3000) and (volume <= 3499):
                yts = 970000
            else:
                yts = 3400
            evroprice = price_rus / currency['eur']
            if evroprice < 8500:
                duty = evroprice * 0.54
                if duty / volume < 2.5:
                    duty = volume * 2.5
            elif (evroprice >= 8500) and (evroprice < 16700):
                duty = evroprice * 0.48
                if duty / volume < 3.5:
                    duty = volume * 3.5
            elif (evroprice >= 16700) and (evroprice < 42300):
                duty = evroprice * 0.48
                if duty / volume < 5.5:
                    duty = volume * 5.5
            elif (evroprice >= 42300) and (evroprice < 84500):
                duty = evroprice * 0.48
                if duty / volume < 7.5:
                    duty = volume * 7.5
            elif (evroprice >= 84500) and (evroprice < 169000):
                duty = evroprice * 0.48
                if duty / volume < 15:
                    duty = volume * 15
            else:
                duty = evroprice * 0.48
                if duty / volume < 20:
                    duty = volume * 20

        elif (age >= 3) and (age < 5):
            if volume >= 3500:
                yts = 1623800
            elif (volume >= 3000) and (volume <= 3499):
                yts = 1485000
            else:
                yts = 5200

            if volume <= 1000:
                duty = volume * 1.5
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 1.7
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 2.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 2.7
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 3
            else:
                duty = volume * 3.6
        elif age >= 5:
            if volume >= 3500:
                yts = 1623800
            elif (volume >= 3000) and (volume <= 3499):
                yts = 1485000
            else:
                yts = 5200

            if volume <= 1000:
                duty = volume * 3
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 3.2
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 3.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 4.8
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 5
            else:
                duty = volume * 5.7

        toll = duty * currency['eur'] + tof

        res_rus = toll + yts + compane_comision + brokerServices
        res_jpn = (freight + delivery + freight_vl + price) * one_rub

        return int(res_rus), int(res_jpn)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cars = Car.objects.all()

    currencies = Currency.objects.values('type', 'value')
    currencies_map = {}

    for currency in currencies:
        currencies_map[currency['type']] = float(currency['value'])

    table_name = 'stats'

    for car in cars:
        res = calc_price(car.finish, currencies_map, car.year, car.eng_v, table_name)
        if res:
            car.expenses_rus, car.expenses_jpn = res[0], res[1]
            car.save()
