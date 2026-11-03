#!/usr/bin/env python3
"""
Split an xlsx file into multiple CSV files by worksheet.

Usage:
    python split_xlsx_to_csvs.py input.xlsx [output_dir]

If output_dir is not specified, CSVs will be saved in the same directory 
as the input file.
"""

import pandas as pd
import sys
import os


def split_xlsx(input_file, output_dir=None):
    """
    Split an Excel file into multiple CSV files, one per worksheet.
    
    Args:
        input_file (str): Path to the input Excel file (.xlsx or .xls)
        output_dir (str | None): Directory to save the CSV files
    
    Returns:
        list[str]: List of paths to the created CSV files
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Create output directory if needed
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    output_path = os.path.join(output_dir, "output")
    os.makedirs(output_path, exist_ok=True)
    
    # Read the Excel file and get all sheet names
    try:
        with pd.ExcelFile(input_file) as xl:
            all_sheet_names = xl.sheet_names
            
            if not all_sheet_names:
                print(f"Error: No sheets found in '{input_file}'")
                sys.exit(1)
            
            # Read and save each sheet individually
            for sheet_name in all_sheet_names:
                excel_df = pd.read_excel(input_file, sheet_name=sheet_name)
                csv_path = os.path.join(output_path, f"{sheet_name}.csv")
                excel_df.to_csv(csv_path, index=False)
                print(f"Created: {csv_path}")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        sys.exit(1)
    
    # Check if it's a multi-sheet workbook or single sheet
    if isinstance(excel_df, dict):
        # Multi-sheet workbook
        worksheets = excel_df.keys()
        for sheet_name in sorted(worksheets):
            csv_path = os.path.join(output_path, f"{sheet_name}.csv")
            excel_df[sheet_name].to_csv(csv_path, index=False)
            print(f"Created: {csv_path}")
    else:
        # Single sheet workbook - use index.name as fallback for .name attribute
        try:
            sheet_name = excel_df.name
        except AttributeError:
            sheet_name = excel_df.index.name if excel_df.index.name else "sheet1"
        csv_path = os.path.join(output_path, f"{sheet_name}.csv")
        excel_df.to_csv(csv_path, index=False)
        print(f"Created: {csv_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_xlsx_to_csvs.py input.xlsx [output_dir]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    split_xlsx(input_file, output_dir)


if __name__ == "__main__":
    main()
