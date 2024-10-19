import re
import requests
import pandas as pd


def extract_ip_addresses(text):
    """
    Extracts all IP addresses from the text using a regular expression.
    """
    print("Extracting IP-addresses...")
    # This regex pattern will match valid IPv4 addresses in the text
    ip_pattern = re.compile(
        r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    )

    # Find all matches for IP addresses in the text
    ip_addresses_all = ip_pattern.findall(text)

    # Remove any obviously invalid IPs, e.g., those with octets > 255 (basic validation)
    ip_addresses = [ip for ip in ip_addresses_all if all(0 <= int(octet) <= 255 for octet in ip.split('.'))]

    print(ip_addresses)
    return ip_addresses

def geolocate_ip(ip_address):
    print("Geolocating IP addresses")
    try:
        # Use the ipwho.is endpoint format
        response = requests.get(f"https://ipwho.is/{ip_address}")
        data = response.json()  # Parse response as JSON

        if data.get("success"):  # Check if the request was successful
            if data.get("latitude") and data.get("longitude"):
                return (data["latitude"], data["longitude"]), data
            else:
                print(f"Could not geolocate IP {ip_address}")
                return None
        else:
            print(f"Failed to geolocate IP {ip_address}: {data.get('message')}")
            return None
    except requests.RequestException as e:
        print(f"Request failed for IP {ip_address}: {e}")
        return None


def save_ip_info_to_csv(geocoded_ips_with_context, file_name="ip-scan.csv"):
    """
    Save the geolocated IP addresses information to a CSV file.

    Parameters:
        geocoded_ips_with_context (list): A list of tuples containing geocoded IP details.
        file_name (str): The name of the CSV file to save the data (default is 'ip-scan.csv').
    """
    # Prepare a list to hold the data
    data = []

    # Iterate through the list of geocoded IPs
    for coordinates, ip_data in geocoded_ips_with_context:
        if isinstance(ip_data, dict):  # Ensure ip_data is a dictionary
            entry = {
                "IP Address": ip_data.get('ip', 'N/A'),
                "Country": ip_data.get('country', 'N/A'),
                "Region": ip_data.get('region', 'N/A'),
                "City": ip_data.get('city', 'N/A'),
                "Latitude": ip_data.get('latitude', 'N/A'),
                "Longitude": ip_data.get('longitude', 'N/A'),
                "ISP": ip_data.get('connection', {}).get('isp', 'N/A'),
                "Coordinates": f"{coordinates[0]}, {coordinates[1]}"  # String format for coordinates
            }
            data.append(entry)
        else:
            print("Invalid IP data format.")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False)

    print(f"IP information saved to {file_name}")