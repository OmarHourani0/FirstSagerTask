from django.contrib import admin
from .models import DroneData

@admin.register(DroneData)
class DroneDataAdmin(admin.ModelAdmin):
    list_display = (
        'drone_id',
        'latitude',
        'longitude',
        'elevation',
        'height',
        'horizontal_speed',
        'vertical_speed',
        'wind_speed',
        'wind_direction',
        'classification',
    )
    list_filter = ('drone_id', 'classification')
    search_fields = ('drone_id',)
    ordering = ('-drone_id',)
