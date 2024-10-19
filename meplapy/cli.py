import argparse
import os
from meplapy.text_extractor import extract_text_from_pdf, extract_text_from_txt, extract_text_from_csv
from meplapy.ner import extract_locations
from meplapy.geocoder import geocode_locations
from meplapy.mapper import create_map, create_csv
from meplapy.iplookup import extract_ip_addresses, geolocate_ip, save_ip_info_to_csv


def main():
    parser = argparse.ArgumentParser(
        description="Meplapy: Extract, geolocate, and map places mentioned in documents."
    )
    parser.add_argument(
        "input_file", help="Path to the input document (PDF, TXT, or CSV)"
    )
    parser.add_argument(
        "--ner", action='store_true', help="Enable NER for location extraction."
    )
    parser.add_argument(
        "--ip", action='store_true', help="Enable IP address geolocation."
    )

    args = parser.parse_args()

    # Auto-detect file format based on file extension
    file_extension = os.path.splitext(args.input_file)[1].lower()

    if file_extension == ".pdf":
        text = extract_text_from_pdf(args.input_file)
    elif file_extension == ".txt":
        text = extract_text_from_txt(args.input_file)
    elif file_extension == ".csv":
        text = extract_text_from_csv(args.input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF, TXT, or CSV file.")

    # Initialize lists for results
    geocoded_locations = {}
    geocoded_ips_with_context = []

    # Extract locations using NER if the --ner flag is set
    if args.ner:
        print("Extracting Locations using NER...")
        locations = extract_locations(text)

        print("Extracted Locations:")
        for loc in locations:
            print(loc)

        # Geocode the locations
        print("\nGeocoding Locations...")
        geocoded_locations = geocode_locations(locations)
        for loc, coords in geocoded_locations.items():
            print(f"{loc}: {coords}")

    # Extract IP addresses and geolocate them if the --ip flag is set
    if args.ip:
        ip_addresses = extract_ip_addresses(text)
        for ip in ip_addresses:
            geolocation_data = geolocate_ip(ip)
            if geolocation_data:
                geocoded_ips_with_context.append(geolocation_data)

    # Automatically set the output map filename based on the input filename
    output_map = os.path.splitext(args.input_file)[0] + ".html"

    # Save the results if geocoded_locations or geocoded_ips_with_context are not empty
    if geocoded_locations:
        create_csv(geocoded_locations, output_map)
    if geocoded_ips_with_context:
        save_ip_info_to_csv(geocoded_ips_with_context, file_name="ip-scan.csv")

    # Generate a map only if there are geocoded locations or IPs
    if geocoded_locations or geocoded_ips_with_context:
        print(f"\nGenerating map and saving to {output_map}...")
        create_map(geocoded_locations, geocoded_ips_with_context, output_map)
    else:
        print("No locations or IPs to map.")

if __name__ == "__main__":
    main()
