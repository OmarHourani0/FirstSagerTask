from django.contrib import admin
from .models import DroneData

@admin.register(DroneData)
class DroneDataAdmin(admin.ModelAdmin):
    """
    This class defines what gets displayed in the Django admin interface for the drone data.

    Args:
        DroneData (Class): It is a class where all the attributes are data about the drone.        

    Returns:
        Does not return anything, but it configures the admin interface for the drone data display.

    Raises:
        Cant raise any exceptions, but the DroneData model has to be well defined
    """
    
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
