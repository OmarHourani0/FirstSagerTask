import math


def haversine(lat1, lon1, lat2, lon2):
    """
    Function that calulates the distance between two points.
    
    The two points are given by their latitude and longitude. The function will find the distance between them using the Haversine formula.
    The first point is the reference point which is set in Amman, and the second point is where the drone is located.

    Args:
        lat1 (float): Latitude of the reference point.
        lon1 (float): Longitude of the reference point.
        lat2 (float): Latitude of the drone.
        lon2 (float): Longitude of the drone.

    Returns:
        ReturnType: The distance between the refrence point and the drone in kilometers is returned as a float.

    Raises:
        ExceptionType: The function does not raise any exceptions per design.
    """
    
    R = 6371  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def classify(drone_data):
    """
    This function gives classifications to drones

    The classifications are based on the drone data. And they are "Danger - High Elevation", 
    "Danger - High Speed", "Warning - Near Height Limit", "Landing", and "All Good".

    Args:
        drone_data (dictionary): It is all the data of the drone.

    Returns:
        ReturnType: Function returns a string that is the classification of the drone.

    Raises:
        ExceptionType: Function does not raise any exceptions per design.
    """

    if drone_data['elevation'] > 500:
        return "DANGER - HIGH ELEVATION"
    elif drone_data['gear'] == 0 and drone_data['elevation'] < 5:
        return "LANDING"
    elif drone_data['vertical_speed'] > 25:
        return "DANGER - HIGH SPEED"
    elif drone_data['is_near_area_limit'] == 1:
        return "WARNING - NEAR AREA LIMIT"
    elif drone_data['is_near_height_limit'] == 1:
        return "WARNING - NEAR HEIGHT LIMIT"
    else:
        return "All Good"
