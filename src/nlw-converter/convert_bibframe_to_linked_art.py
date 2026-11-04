#!/usr/bin/env python3
"""
Convert Bibframe CSV files to Linked Art JSON-LD format.

This script reads CSV data from the bibliography output directory and
converts it to proper Linked Art RDF/JSON-LD format with namespace URIs.

Usage:
    python convert_bibframe_to_linked_art.py --input-dir <csv_dir> --output-file <json_file>
"""

import csv
import json
import sys
from pathlib import Path



def convert_bibliography_csv_to_linked_art(input_dir: str) -> tuple[dict[str, int], list[dict]]:
    """Convert CSV files to Linked Art JSON format."""

    input_path = Path(input_dir)
    results = {}
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
    
    # Find all CSV files in the bibliography directory  
    csv_files = sorted([f for f in input_path.glob("*2024.csv")])
    
    if not csv_files:
        print("No CSV files found matching *2024.csv pattern")
        return results
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    all_records = []
    
    for csv_file in csv_files:
        filename = csv_file.name
        print(f"\nProcessing: {filename}")
        
        try:
            records = csv_to_dict_records(str(csv_file))
            
            if not records:
                print(f"  Warning: No valid records found")
                continue
            
            results[filename] = len(records)
            print(f"  Converted {len(records)} records")
            all_records.extend(records)
        
        except Exception as e:
            print(f"  Error processing '{filename}': {e}")

    return results, all_records


def csv_to_dict_records(csv_path: str) -> list[dict]:
    """Parse CSV file into bibliographic record dictionaries."""
    
    records = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            mms_id = row.get('MMS ID', '').strip()

            if not mms_id:
                continue

            title = row.get('Title', '').strip()

            if not title:
                continue

            # Extract creator/imprint info (may contain commas)
            creator_imprint = ' '.join(row.get('Creator / Imprint', '').split())

            records.append({
                "mms_id": mms_id,
                "title": title,
                "creator_imprint": creator_imprint.strip(),
            })
    
    return records


def convert_to_linked_art_format(records: list[dict]) -> dict:
    """Convert records to proper Linked Art JSON-LD format."""

    linked_art_data = {
        "@context": {
            "la": "http://linkedart.eu/vocab/",
            "@vocab": "http://linkedart.eu/"
        },
        "@graph": []
    }
    
    for record in records:
        # Create an object entry
        obj = {
            "@id": f"http://linkedart.eu/{record['mms_id']}",
            "@type": "la:Artwork"
        }
        
        if record.get("title"):
            obj["la:title"] = record["title"]
        if record.get("creator_imprint"):
            obj["la:creatorImprint"] = record["creator_imprint"]
        if record.get("subject"):
            obj["la:subject"] = record["subject"]
        if record.get("language"):
            obj["la:language"] = record["language"]
        
        linked_art_data["@graph"].append(obj)
    
    return linked_art_data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert bibliographic CSV files to Linked Art format"
    )
    parser.add_argument(
        "--input-dir", 
        "-i",
        default="C:/Users/Alast/repos/nlw-converter/data/bibliography-of-welsh-printed-material/output",
        help="Directory containing input CSV files"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        help="Output JSON file path"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Converting Bibliographic CSV to Linked Art Format")
    print("=" * 60)
    
    # Convert all files
    results, all_records = convert_bibliography_csv_to_linked_art(args.input_dir)

    total_records = sum(results.values())
    print(f"\nTotal records converted: {total_records}")

    if total_records > 0:
        json_output_path = f"{args.input_dir}/linked-art-records.json"

        linked_art_data = convert_to_linked_art_format(all_records)

        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(linked_art_data, f, indent=2, ensure_ascii=False)

        print(f"\nOutput written to '{json_output_path}'")
    else:
        print("\nNo records converted")
    
    print("=" * 60)
