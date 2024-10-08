from django.contrib import admin
from cars.models import (Car, Color, Country,
                         Model, Mark, Kuzov,
                         KppType, Privod, UniqueMarkModel,
                         Currency, UniqueCarColor, UniqueCarKpp,
                         UniqueCarPrivod, UniqueCarModel,
                         UniqueCarPw)

admin.site.register(Car)
admin.site.register(Color)
admin.site.register(Country)
admin.site.register(Model)
admin.site.register(Mark)
admin.site.register(Kuzov)
admin.site.register(KppType)
admin.site.register(Privod)
admin.site.register(UniqueMarkModel)
admin.site.register(Currency)
admin.site.register(UniqueCarColor)
admin.site.register(UniqueCarKpp)
admin.site.register(UniqueCarPrivod)
admin.site.register(UniqueCarModel)
admin.site.register(UniqueCarPw)
