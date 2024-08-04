import pandas as pd
import json
import argparse

def process_file(excel_path, jsonl_filename, num_rows):
    # Read the Excel file using openpyxl
    data = pd.read_excel(excel_path, engine='openpyxl')
    
    # Filter data by labels and balance the dataset
    harmless = data[data['label'] == 0]
    harmful = data[data['label'] == 1]

    # Limit the data to 'num_rows' for each category if possible
    min_count = min(len(harmless), len(harmful), num_rows//2)
    balanced_data = pd.concat([harmless.head(min_count), harmful.head(min_count)])

    # Open the JSONL file for writing
    with open(jsonl_filename, 'w') as jsonl_file:
        # Iterate through each row in the DataFrame
        for _, row in balanced_data.iterrows():
            # Construct the sentence object
            sentence = {
                "sentence": f"{row['Title']} {row['Description']}",
                "label": "harmless" if row['label'] == 0 else "harmful"
            }
            
            # Write the JSON object to the JSONL file
            jsonl_file.write(json.dumps(sentence) + '\n')

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process an Excel file and output a balanced JSONL file for training.')
    parser.add_argument('excel_path', type=str, help='Path to the input Excel file')
    parser.add_argument('jsonl_filename', type=str, help='Filename for the output JSONL file')
    parser.add_argument('num_rows', type=int, help='Total number of rows to consider for training (equal number of harmless and harmful)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the file
    process_file(args.excel_path, args.jsonl_filename, args.num_rows)

if __name__ == '__main__':
    main()
