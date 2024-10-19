import re


def dms_to_decimal(degrees, minutes=0, seconds=0, direction=''):
    """
    Convert DMS coordinates to decimal degrees.

    Parameters:
        degrees (int): The degrees part.
        minutes (int): The minutes part (default is 0).
        seconds (float): The seconds part (default is 0).
        direction (str): Direction 'N', 'S', 'E', 'W' (default is '').

    Returns:
        float: The decimal degree representation.
    """
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def extract_coordinates_with_context(text):
    """
    Extract coordinates from the text and provide context (±5 words).

    Parameters:
        text (str): The input text to search for coordinates.

    Returns:
        list: A list of tuples with coordinates and their context.
    """
    print("Extracting Coordinates...")
    coordinates_with_context = []

    # Regex patterns for finding coordinates
    coord_pattern_decimal = re.compile(r"(-?\d+\.\d+),\s*(-?\d+\.\d+)")
    coord_pattern_dms = re.compile(r"(\d+\.\d+)°\s*([NS])?\s*,?\s*(\d+\.\d+)°\s*([EW])?")

    # Split the text into words for context extraction
    words = text.split()

    # Search for decimal coordinates
    for match in coord_pattern_decimal.finditer(text):
        latitude, longitude = map(float, match.groups())
        # Get context: ±5 words around the found coordinates
        start_index = max(0, match.start() - 20)
        end_index = min(len(text), match.end() + 20)
        context = text[start_index:end_index]
        coordinates_with_context.append(((latitude, longitude), context))
        print(f"Coordinates identified (Decimal): {latitude}, {longitude}, Context: '{context.strip()}'")

    # Search for DMS coordinates
    for match in coord_pattern_dms.finditer(text):
        lat_deg, lat_dir, long_deg, long_dir = match.groups()
        latitude = dms_to_decimal(float(lat_deg), 0, 0, lat_dir)
        longitude = dms_to_decimal(float(long_deg), 0, 0, long_dir)

        # Get context: ±5 words around the found coordinates
        start_index = max(0, match.start() - 20)
        end_index = min(len(text), match.end() + 20)
        context = text[start_index:end_index]
        coordinates_with_context.append(((latitude, longitude), context))
        print(f"Coordinates identified (DMS): {latitude}, {longitude}, Context: '{context.strip()}'")

    return coordinates_with_context