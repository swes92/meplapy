import folium
from folium import IFrame
import pandas as pd


def create_map(geocoded_locations_with_context, output_file):
    """
    Generate an interactive map with the geocoded locations and their context.
    """
    # Create a map centered at an arbitrary starting location (this can be customized)
    map_object = folium.Map(location=[20, 0], zoom_start=2)

    # Add markers for each location with its context
    for loc, data in geocoded_locations_with_context.items():
        coordinates, context = data

        # Create a custom HTML popup with adjustable size and content
        popup_content = f"<b>Location:</b> {loc}<br><b>Context:</b> {context}"

        # Use IFrame to control the dimensions of the popup
        iframe = IFrame(popup_content, width=250, height=120)
        popup = folium.Popup(iframe, max_width=300)  # Max width for resizing

        # Add the marker with the custom popup
        folium.Marker(
            location=coordinates,
            popup=popup,
            tooltip=loc
        ).add_to(map_object)

    map_object.save(output_file)

def create_csv(geocoded_locations_with_context, input_file_name):
    """
    Save the geocoded locations and their context to a CSV file.

    Parameters:
        geocoded_locations_with_context (dict): A dictionary containing locations,
                                                 their coordinates, and context.
        input_file_name (str): The name of the input file to derive the output CSV file name.
    """
    # Prepare data for CSV
    csv_data = []

    # Append to CSV data
    for loc, data in geocoded_locations_with_context.items():
        coordinates, context = data
        csv_data.append({"NER": loc, "Geocoded Location": coordinates, "Context": context})

    # Save to CSV file with the same name as the input file
    output_csv_file = f"{input_file_name.rsplit('.', 1)[0]}.csv"  # Remove extension and add .csv
    pd.DataFrame(csv_data).to_csv(output_csv_file, index=False)

    print(f"Data saved to '{output_csv_file}'")

# Example of how to use the functions:
# map_obj = create_map(geocoded_locations_with_context)
# map_obj.save("map.html")
# create_csv(geocoded_locations_with_context, input_file_name)
