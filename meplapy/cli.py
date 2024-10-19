import argparse
import os
from meplapy.text_extractor import extract_text_from_pdf, extract_text_from_txt, extract_text_from_csv
from meplapy.ner import extract_locations
from meplapy.geocoder import geocode_locations
from meplapy.mapper import create_map, create_csv


def main():
    parser = argparse.ArgumentParser(
        description="Meplapy: Extract, geolocate, and map places mentioned in documents."
    )
    parser.add_argument(
        "input_file", help="Path to the input document (PDF, TXT, or CSV)"
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

    # Extract locations using NER
    locations = extract_locations(text)

    print("Extracted Locations:")
    for loc in locations:
        print(loc)

    # Geocode the locations
    print("\nGeocoding Locations...")
    geocoded_locations = geocode_locations(locations)
    for loc, coords in geocoded_locations.items():
        print(f"{loc}: {coords}")

    # Automatically set the output map filename based on the input filename
    output_map = os.path.splitext(args.input_file)[0] + ".html"

    # Generate a map and save as csv
    print(f"\nGenerating map and saving to {output_map}...")
    create_map(geocoded_locations, output_map)
    create_csv(geocoded_locations, output_map)


if __name__ == "__main__":
    main()
