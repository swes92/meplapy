import re
import requests

def extract_ip_addresses(text):
    """
    Extract IP addresses from the given text using regular expressions.
    """
    # Regular expression to match IPv4 addresses
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ip_addresses = re.findall(ip_pattern, text)
    return ip_addresses

def geolocate_ip(ip_address):
    """
    Geolocate the given IP address using the ipapi service.
    """
    url = f"http://ipapi.co/{ip_address}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "latitude" in data and "longitude" in data:
            return {
                "ip": ip_address,
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "org": data.get("org", "Unknown")
            }
    return None
