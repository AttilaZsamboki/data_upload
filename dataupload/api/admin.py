from django.contrib import admin
from .models import DatauploadTabletemplates, DatauploadTableOverview, DatauploadGroups

# Register your models here.


class DatauploadTabletemplatesAdmin(admin.ModelAdmin):
    save_as = True


class DatauploadTableOverviewsAdmin(admin.ModelAdmin):
    save_as = True


class DatauploadGroupsAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(DatauploadTabletemplates, DatauploadTabletemplatesAdmin)
admin.site.register(DatauploadTableOverview, DatauploadTableOverviewsAdmin)
admin.site.register(DatauploadGroups, DatauploadGroupsAdmin)
