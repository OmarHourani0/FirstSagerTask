from django.db import models

class DroneData(models.Model):
    
    """
    The class defines the types of data that will be stored in the database for each drone.

    Args:
        No parameters are required to initialize this class.

    Returns:
        ReturnType: The class does not return anything, but it defines the structure of the drone data model.

    Raises:
        Cant raise any excpection but the model has to be well defined.
        And the database has to be properly configured to store this data.
    """
    
    drone_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Position & motion
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    height = models.FloatField()
    height_limit = models.FloatField()
    home_distance = models.FloatField()
    horizontal_speed = models.FloatField()
    vertical_speed = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()

    # Status flags & modes
    gear = models.IntegerField()
    is_near_area_limit = models.BooleanField()
    is_near_height_limit = models.BooleanField()
    rc_lost_action = models.IntegerField()
    rid_state = models.BooleanField()
    rth_altitude = models.FloatField()

    # Storage
    storage_total = models.BigIntegerField()
    storage_used = models.BigIntegerField()

    # Flight summary
    total_flight_distance = models.FloatField()
    total_flight_sorties = models.IntegerField()
    total_flight_time = models.FloatField()

    # Misc
    track_id = models.CharField(max_length=255, blank=True)

    # Your classification result
    classification = models.CharField(max_length=100, null=True, blank=True)
