from geopy.geocoders import Nominatim

def get_city_coordinates(city: str):
    geolocator = Nominatim(user_agent="astro_service")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None