from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time


def geocode_locations(locations_with_context):
    """
    Geocode a list of locations along with their context using Nominatim.
    """
    geolocator = Nominatim(user_agent="meplapy_geocoder")
    geocoded_locations_with_context = {}

    for loc, context in locations_with_context:
        try:
            location = geolocator.geocode(loc)
            if location:
                geocoded_locations_with_context[loc] = ([location.latitude, location.longitude], context)
            time.sleep(1)  # To prevent overwhelming the geocoding service
        except Exception as e:
            print(f"Error geocoding {loc}: {e}")

    return geocoded_locations_with_context