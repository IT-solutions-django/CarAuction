# Скрипт для миграции БД в PostgreSQL

import os
from datetime import datetime

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarAuction.settings')

django.setup()

from cars.models import Car, Model, Mark, Kuzov, Privod, KppType, Color, Country
from django.db import connections

with connections['sqlite'].cursor() as cursor:
    cursor.execute(
        "SELECT AUCTION_DATE, AUCTION, MODEL_ID, MARKA_ID, MARKA_NAME, "
        "MODEL_NAME, YEAR, ENG_V, PW, KUZOV, GRADE, COLOR, KPP, KPP_TYPE, PRIV, "
        "MILEAGE, EQUIP, RATE, FINISH, IMAGES FROM stats")
    rows = cursor.fetchall()

    car_priv_types = (
        "FULLTIME4WD",
        "FF,FULLTIME4WD",
        "FULLTIME4WD,PARTTIME",
        "FR,FULLTIME4WD,PARTT",
        "PARTTIME4WD",
        "MIDSHIP",
        "FR,FULLTIME4WD",
        "FR,PARTTIME4WD",
        "FULLTIME4WD,RR",
        "FULLTIME4WD,MIDSHIP"
    )

    car_kpp_types = (
        "F5",
        "I5",
        "F6",
        "F4",
        "5",
        "I6",
        "6",
        "4",
        "C5",
        "F7",
        "D5",
        "7",
        "C4",
        "D6",
        "6MT",
        "5F",
        "5MT",
        "5C",
        "7F",
        "6F",
        "F5MT",
        "I-5",
        "5D",
        "5I",
        "7MT",
        "4MT",
        "4X2",
        "F16",
        "M5",
        "F3",
        "6HL",
        "5FMT",
        "6FMT",
        "4F",
        "5AG",
        "F4AT",
        "5X2",
        "I-6",
        "4C",
        "9HL",
        "8HL",
        "6X2",
        "8X2"
    )

    car_transmission_types = (
        "FA",
        "AT",
        "CA",
        "IA",
        "MT",
        "SQ",
        "IAT",
        "FAT",
        "CAT",
        "SAT",
        "DAT",
        "DA",
        "AGS",
        "DCV",
        "CVT",
        "FMT",
        "X",
        "FM",
        "F"
    )

    car_black_colors = (
        "BLACK M",
        "BLACK PEARL",
        "black two-tone",
        "Mad Black",
        "black chameleon",
        "Nighthawk Black",
        "Black – White",
        "B BLACK",
        "Phantom Black",
        "sapphire black",
        "Crystal Black",
        "Black Metallic",
        "Cosmos Black",
        "Black mica metallic",
        "Night Shadow path",
        "BLACK 2"
    )

    car_colors_white = (
        "Leaf White",
        "white two-tone",
        "White Pearl",
        "white-blue",
        "White-Grey",
        "super white",
        "Brilliant White",
        "Taffeta White",
        "Silky White",
        "white-black",
        "white violet",
        "white-pearl",
        "Brilliant Bra",
        "Iceberg",
        "vanilla",
        "WHITE 2",
        "Alpine White 3",
        "Parushiro 3"
    )

    car_brown_colors = (
        "Prime Brown",
        "Plum Brown",
        "Brown Pearl",
        "BROWN M",
        "D BROWN",
        "Bitter Chocolat",
        "BRONZE",
        "Milk tea",
        "BROWN M2",
        "BROWN 2"
    )

    car_purple_colors = (
        "Purple Pearl",
        "Dark purple",
        "Light Purple",
        "mauve",
        "LAVENDER",
        "VIOLET",
        "PURPLE 2"
    )

    car_green_colors = (
        "D GREEN",
        "Green color",
        "green-two tone",
        "dark green",
        "Mint green",
        "dark green-white",
        "light green",
        "L GREEN",
        "GREEN M",
        "Green / white",
        "lime green",
        "OLIVE",
        "mint",
        "CHAMPAGNE",
        "Cool khaki",
        "KHAKI 2",
        "CHAMPAGNE",
        "Tea 2",
        "L GREEN 2",
        "GREEN 2",
        "D GREEN 2",
        "TURQUOISE 2"
    )

    car_gray_colors = (
        "GRAY M",
        "D GRAY",
        "dark Gray metallic",
        "gray two-tone",
        "gray pearl",
        "L GRAY",
        "Titanium gray",
        "Gray Mica",
        "Meteor Grey",
        "Gun M",
        "charcoal",
        "OPAL",
        "Jinbakku",
        "Ceramic metallic",
        "METALLIC",
        "CERAMIC",
        "GRAY 2",
        "L GRAY 2"
    )

    silver_tuple = (
        "SILVER 2",
        "Bright Silver",
        "Silver Two-tone",
        "silver-dark grey",
        "Steel Silver",
        "Silky Silver",
        "Brilliant Silver",
        "Storm Silver",
        "luna silver",
        "SILVER M",
        "Silver metallic",
        "Aluminum M",
        "Mellow Silver",
        "Cool Silver",
        "dark metal",
        "Titanium",
        "METALLIC"
    )

    blue_tuple = (
        "NAVY BLUE",
        "LIGHT BLUE",
        "L BLUE",
        "BLUE 2",
        "LIGHT BLUE 2",
        "D BLUE 2",
        "BLUE M",
        "D BLUE",
        "dark blue chameleon",
        "blue two-tone",
        "lake blue",
        "Ice Blue Metal",
        "L BLUE 2",
        "sky blue",
        "Blue-green",
        "Deep Blue",
        "NAVY BLUE 2",
        "NAVY BLUE M",
        "Light blue –white",
        "blue-silver",
        "dark blue",
        "blue-white",
        "blue-grey",
        "Aqua mica",
        "Blue acme Shubu",
        "Blue Mica",
        "Aqua Metallic",
        "marine",
        "indigo"
    )

    beige_tuple = (
        "BEIGE M",
        "beige two-tone",
        "light beige",
        "beige/white",
        "Cream beige",
        "Con 2",
        "PEARL 2",
        "PEARL WHITE 2",
        "Pearl – Black",
        "pearl two-tone",
        "pearl gray",
        "EVO KNEE",
        "PEARL WHITE",
        "Crystal Pearl",
        "Radiant evo",
        "CREAM",
        "Ivory Pearl",
        "Cotton Ivory",
        "Ivory Pearl"
    )

    yellow_tuple = (
        "yellow – white",
        "YELLOW 2",
        "Sand",
        "yellow-black",
        "YELLOW GREEN",
        "Banana Shake",
        "key"
    )

    gold_tuple = (
        "GOLD 2",
        "Gold Pearl",
        "gold-silver"
    )

    red_tuple = (
        "RED 2",
        "Red two-tone",
        "red-grey",
        "Mystic Red",
        "dark red",
        "Red Metallic",
        "red metal",
        "Mokoberi",
        "COPPER"
    )

    wine_tuple = (
        "WINE 2",
        "dark wine",
        "DARK RED WINE 2",
        "Wine two-tone",
        "DARK RED WINE",
        "Maroon Brown",
        "Silky Maroon",
        "BORDEAUX",
        "WINE M",
        "red-black",
        "Azuki bean"
    )

    pink_tuple = (
        "PINK 2",
        "pink silver",
        "light pink",
        "Pink two-tone",
        "frosty pink",
        "rose bronze",
        "ROSE 2",
        "Light Rose",
        "smoke rose",
        "Light Rose mica"
    )

    orange_tuple = (
        "Toniko Orange",
        "Orange / White",
        "Sunlight Orange",
        "Orange two-tone",
        "ORANGE 2",
        "peach"
    )

    for row in rows:
        if row[14] == 'RR':
            continue

        model, _ = Model.objects.get_or_create(
            name=row[5]
        )

        mark, _ = Mark.objects.get_or_create(
            name=row[4]
        )

        kuzov, _ = Kuzov.objects.get_or_create(
            name=row[9]
        )

        color, _ = Color.objects.get_or_create(
            name=row[11]
        )

        kpp, _ = KppType.objects.get_or_create(
            name=row[12]
        )

        priv, _ = Privod.objects.get_or_create(
            name=row[14]
        )

        country, _ = Country.objects.get_or_create(
            name='Japan'
        )

        auction_date_str = row[0]
        auction_date = datetime.strptime(auction_date_str, "%Y-%m-%d %H:%M:%S").date()

        images_str = row[19]
        images_array = images_str.split('\n')

        priv_true = ''
        if priv.name in car_priv_types or 'FULLTIME4WD' in priv.name:
            priv_true = 'Полный привод'
        elif priv.name == 'FR':
            priv_true = 'Задний привод'
        elif priv.name == 'FF':
            priv_true = 'Передний привод'

        color_true = ''
        if color.name in car_black_colors:
            color_true = 'Черный'
        elif color.name in car_colors_white:
            color_true = 'Белый'
        elif color.name in car_gray_colors:
            color_true = 'Серый'
        elif color.name in car_green_colors:
            color_true = 'Зеленый'
        elif color.name in car_brown_colors:
            color_true = 'Коричневый'
        elif color.name in car_purple_colors:
            color_true = 'Фиолетовый'
        elif color.name in silver_tuple:
            color_true = 'Серебряный'
        elif color.name in blue_tuple:
            color_true = 'Голубой/Синий'
        elif color.name in beige_tuple:
            color_true = 'Бежевый'
        elif color.name in yellow_tuple:
            color_true = 'Желтый'
        elif color.name in gold_tuple:
            color_true = 'Золотой'
        elif color.name in red_tuple:
            color_true = 'Красный'
        elif color.name in wine_tuple:
            color_true = 'Бордовый'
        elif color.name in pink_tuple:
            color_true = 'Розовый'
        elif color.name in orange_tuple:
            color_true = 'Оранжевый'

        kpp_true = ''
        if kpp.name in car_transmission_types or kpp.name.isalpha():
            kpp_true = 'Автоматическая'
        elif kpp.name in car_kpp_types or not kpp.name.isalpha():
            kpp_true = 'Механическая'

        Car.objects.create(
            auction_date=auction_date,
            auction=row[1],
            model_id=model,
            mark_id=mark,
            year=row[6],
            eng_v=row[7],
            pw=row[8],
            kuzov_id=kuzov,
            grade=row[10],
            color_id=color,
            true_color=color_true,
            kpp_type=kpp,
            true_kpp=kpp_true,
            priv_id=priv,
            true_priv=priv_true,
            mileage=row[15],
            equip=row[16],
            rate=row[17],
            finish=row[18],
            country_id=country,
            images=images_array
        )
