def classify(drone_data):
    """
    Example: Basic classification rule
    """
    if drone_data['height'] > 50 and drone_data['wind_speed'] > 10:
        return "RISKY"
    elif drone_data['gear'] == 0:
        return "LANDING"
    else:
        return "NORMAL"
