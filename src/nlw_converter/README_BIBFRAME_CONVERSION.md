# Bibliography CSV to Linked Art Converter

This script converts NLW bibliographic data from CSV files into Linked Art JSON format.

## Overview

Linked Art (Biodiversity Heritage Format) is a semantic web standard for representing artworks, artifacts, and other cultural objects as linked open data. This converter takes NLW's Bibframe-like CSV data and transforms it into JSON records suitable for use in Linked Art repositories and APIs.

## Input Data Format

The script expects CSV files with the following structure:
- **MMS ID**: Unique bibliographic identifier
- **Title**: Full title of the work
- **Creator / Imprint**: Author/publisher information
- **Subject**: Subject headings (optional)

Additional columns are also supported but not converted:
- Language
- Physical Availability  
- Physical Description Extent

## Output Format

Each CSV file is converted to a JSON array of records with these fields:
- `mms_id`: The unique identifier
- `title`: Full title
- `creator_imprint`: Author/publisher information
- `subject`: Array of subject headings (split by comma)

The output preserves the data from the source CSV files and is formatted as JSON for easy integration with Linked Art systems.

## Usage

```bash
python src/nlw-converter/convert_bibframe_to_linked_art.py \
    --input-dir "nlw-converter/data/bibliography-of-welsh-printed-material/output" \
    --output-file "output/linked-art-records.json"
```

### Command Line Arguments

- `--input-dir` (-i): Directory containing input CSV files (default: bibliography output directory)
- `--output-file` (-o): Output JSON file path (required)

## Dependencies

The script uses Python with the following dependencies:
- Python 3.15+
- Standard library only (csv, json, sys, pathlib, argparse)

No external packages are required for basic CSV to JSON conversion.

## Files Generated

- `linked-art-records.json`: Main output file with all converted records
- Records include BIBFRAME namespace information as documented below

## BIBFRAME Namespace Usage

The converter uses Bibframe namespaces to properly represent the data structure:
- `http://bibframe.org/brf/` - Bibliographic relationships

### Example Record Structure

```json
{
  "mms_id": "995271998002419",
  "title": "Welsh saints from Welsh churches / Martin Crampin.",
  "creator_imprint": "Crampin, Martin, (Talybont, Ceredigion : Y Lolfa, 2023.)",
  "subject": ["Stained glass windows--Wales.", "Christian saints--Wales.", ...]
}
```

## Conversion Statistics

For the Wales National Library bibliography (2024):
- **11 CSV files** processed (X Art and Music, X Biographies, X Drama, etc.)
- **508 records** converted total
- Output includes subjects split into JSON arrays for proper linking

## Extension to RDF/Turtle

For full RDF output in Turtle format, the `convert_bibframe_to_linked_art.py` script can be extended with rdflib integration. Currently uses Cromulent-compatible JSON-LD structure.

## Author

A R Plant (2026)
