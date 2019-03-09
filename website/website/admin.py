from django.contrib import admin

from website import models

admin.site.register(models.Station)
admin.site.register(models.Company)
admin.site.register(models.SellPoint)
admin.site.register(models.DropOff)
admin.site.register(models.Cup)
admin.site.register(models.CustomUser)