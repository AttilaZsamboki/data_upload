from django.contrib import admin
from .models import DatauploadTabletemplates

# Register your models here.


class DatauploadTabletemplatesAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(DatauploadTabletemplates, DatauploadTabletemplatesAdmin)
