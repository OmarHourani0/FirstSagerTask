import math

def haversine(lat1, lon1, lat2, lon2):
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
    Example: Basic classification rule
    """
    
    lat1 = 31.000
    lon1 = 39.000
    lat2 = drone_data['latitude']
    lon2 = drone_data['longitude']
    
    distance = haversine(lat1, lon1, lat2, lon2)    
    
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
    
    