#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Process the sample.csv file to add addresses based on TWD97 coordinates.
Using pandas for CSV processing.
"""

import os
import pandas as pd
from reverse_geocode import twd97_to_address

def process_coordinates_file(input_file, output_file):
    """
    Process a CSV file with TWD97 coordinates and add addresses using pandas.
    
    Args:
        input_file (str): Path to the input CSV file with X, Y coordinates
        output_file (str): Path to the output CSV file with addresses
    """
    print(f"Processing {input_file}...")
    
    # Read the input CSV file using pandas with special handling for spaces in column names
    df = pd.read_csv(input_file)
    
    # Clean column names (strip whitespace)
    df.columns = [col.strip() for col in df.columns]
    
    print(f"Found {len(df)} coordinates to process.")
    
    # Create a new Address column
    df['Address'] = None
    
    # Process each row to get addresses
    total = len(df)
    for i, row in df.iterrows():
        # Strip whitespace from values and convert to float
        x = float(str(row['X']).strip())
        y = float(str(row['Y']).strip())
        
        # Get address from coordinates
        address = twd97_to_address(x, y)
        df.at[i, 'Address'] = address
        
        # Show progress
        print(f"Processing coordinate {i+1}/{total}: ({x}, {y}) → {address}")
    
    # Write to output CSV file
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\nProcessing complete. Results saved to {output_file}")

def main():
    """
    Main function to process the sample.csv file and generate result.csv
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output file paths
    input_file = os.path.join(script_dir, 'sample.csv')
    output_file = os.path.join(script_dir, 'result.csv')
    
    # Process the file
    process_coordinates_file(input_file, output_file)

if __name__ == "__main__":
    main()