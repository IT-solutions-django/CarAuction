from django.contrib import admin
from cars.models import (Car, Color, Country,
                         Model, Mark, Kuzov,
                         KppType, Privod)

admin.site.register(Car)
admin.site.register(Color)
admin.site.register(Country)
admin.site.register(Model)
admin.site.register(Mark)
admin.site.register(Kuzov)
admin.site.register(KppType)
admin.site.register(Privod)
