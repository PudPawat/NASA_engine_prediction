#!/usr/bin/env python3
"""
Convert Turbofan Engine Degradation Simulation Dataset from .txt to .csv format.

This script converts all training, test, and RUL files from space-separated
text format to CSV format with proper column headers.
"""

import pandas as pd
from pathlib import Path
import os

# Define data path
data_path = Path('dataset/6.+Turbofan+Engine+Degradation+Simulation+Data+Set/6. Turbofan Engine Degradation Simulation Data Set/CMAPSSData')

# Column names with actual field names
op_settings = ['Altitude', 'Mach', 'TRA']
sensors = ['T2', 'T24', 'T30', 'T50', 'P2', 'P15', 'P30', 'Nf', 'Nc', 'epr', 'Ps30', 'phi', 
           'NRf', 'NRc', 'BPR', 'farB', 'htBleed', 'Nf_dmd', 'PCNfR_dmd', 'W31', 'W32']
column_names = ['unit', 'time'] + op_settings + sensors

# RUL column name
rul_column = ['RUL']

# Dataset identifiers
datasets = ['FD001', 'FD002', 'FD003', 'FD004']

def convert_file(input_file, output_file, column_names, file_type='data'):
    """
    Convert a space-separated text file to CSV format.
    
    Parameters:
    -----------
    input_file : Path
        Path to input .txt file
    output_file : Path
        Path to output .csv file
    column_names : list
        List of column names for the CSV
    file_type : str
        Type of file ('data' for train/test, 'rul' for RUL files)
    """
    try:
        if file_type == 'rul':
            # RUL files have a single column
            df = pd.read_csv(input_file, sep=r'\s+', header=None, names=rul_column)
        else:
            # Train/test files have multiple columns
            df = pd.read_csv(input_file, sep=r'\s+', header=None, names=column_names)
        
        # Save as CSV
        df.to_csv(output_file, index=False)
        print(f"✓ Converted: {input_file.name} -> {output_file.name}")
        return True
    except Exception as e:
        print(f"✗ Error converting {input_file.name}: {str(e)}")
        return False

def main():
    """Main function to convert all dataset files to CSV."""
    
    # Check if data path exists
    if not data_path.exists():
        print(f"Error: Data path not found: {data_path}")
        print("Please make sure you're running this script from the project root directory.")
        return
    
    print("="*70)
    print("Turbofan Dataset Converter: .txt to .csv")
    print("="*70)
    print(f"Data path: {data_path}\n")
    
    converted_count = 0
    total_count = 0
    
    # Convert training files
    print("Converting training files...")
    for dataset in datasets:
        train_file = data_path / f'train_{dataset}.txt'
        if train_file.exists():
            csv_file = data_path / f'train_{dataset}.csv'
            if convert_file(train_file, csv_file, column_names, 'data'):
                converted_count += 1
            total_count += 1
        else:
            print(f"⚠ Warning: {train_file.name} not found")
    
    # Convert test files
    print("\nConverting test files...")
    for dataset in datasets:
        test_file = data_path / f'test_{dataset}.txt'
        if test_file.exists():
            csv_file = data_path / f'test_{dataset}.csv'
            if convert_file(test_file, csv_file, column_names, 'data'):
                converted_count += 1
            total_count += 1
        else:
            print(f"⚠ Warning: {test_file.name} not found")
    
    # Convert RUL files
    print("\nConverting RUL files...")
    for dataset in datasets:
        rul_file = data_path / f'RUL_{dataset}.txt'
        if rul_file.exists():
            csv_file = data_path / f'RUL_{dataset}.csv'
            if convert_file(rul_file, csv_file, rul_column, 'rul'):
                converted_count += 1
            total_count += 1
        else:
            print(f"⚠ Warning: {rul_file.name} not found")
    
    # Summary
    print("\n" + "="*70)
    print("Conversion Summary")
    print("="*70)
    print(f"Total files processed: {total_count}")
    print(f"Successfully converted: {converted_count}")
    print(f"Failed: {total_count - converted_count}")
    print(f"\nCSV files saved in: {data_path}")
    print("="*70)

if __name__ == "__main__":
    main()
