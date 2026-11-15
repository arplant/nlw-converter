import json
import os
import sys
from pathlib import Path

# Ensure the package path is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.nlw_converter.convert_bibframe_to_linked_art import (
    convert_bibliography_csv_to_linked_art,
    convert_to_linked_art_format,
)

# Sample data simulating two CSV files
SAMPLE_CSV_1 = """
MMS ID,Title,Creator / Imprint
12345,Test Book,John Doe
67890,Another Book,Jane Smith
"""

SAMPLE_CSV_2 = """
MMS ID,Title,Creator / Imprint
11111,Third Book,Emily Johnson
"""

# Write sample CSV files to a temporary directory

def write_temp_csv(tmp_dir: Path, name: str, content: str) -> Path:
    file_path = tmp_dir / name
    file_path.write_text(content.strip(), encoding="utf-8")
    return file_path


def test_conversion_compliance(tmp_path):
    """Verify that output JSON-LD conforms to Linked Art v1 structure."""
    # Create CSV files
    csv1 = write_temp_csv(tmp_path, "X Fiction 2024.csv", SAMPLE_CSV_1)
    csv2 = write_temp_csv(tmp_path, "X Poetry 2024.csv", SAMPLE_CSV_2)

    # Run conversion
    results, records = convert_bibliography_csv_to_linked_art(str(tmp_path))

    # Check that all records are processed
    assert sum(results.values()) == 3
    assert len(records) == 3

    # Convert to Linked Art format
    linked_art = convert_to_linked_art_format(records)

    # Basic compliance checks
    assert "@context" in linked_art
    assert linked_art["@context"] == "https://linkedart.eu/ns/v1/linked-art.json"
    assert "@graph" in linked_art
    assert isinstance(linked_art["@graph"], list)
    assert len(linked_art["@graph"]) == 3

    # Validate each graph object
    for obj in linked_art["@graph"]:
        # Must have an id, type and title or creatorImprint
        assert "id" in obj
        assert obj["id"].startswith("https://linkedart.eu/")
        assert obj.get("type") == "HumanMadeObject"
        # title and creatorImprint are optional but at least one should exist
        assert obj.get("title") or obj.get("creatorImprint")

    # Ensure no empty string keys
    for obj in linked_art["@graph"]:
        for k, v in obj.items():
            assert v != ""

    # Verify JSON is serializable with proper UTF-8
    json_str = json.dumps(linked_art, ensure_ascii=False)
    # Should be a valid UTF-8 string
    json_str.encode("utf-8")

    # If all assertions pass, the test succeeds
