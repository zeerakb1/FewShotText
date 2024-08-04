import pandas as pd
import json
import argparse

def process_file(excel_path, train_filename, valid_filename, train_rows, valid_rows):
    # Read the Excel file using openpyxl
    data = pd.read_excel(excel_path, engine='openpyxl')
    
    # Filter data by labels and balance the datasets
    harmless = data[data['label'] == 0]
    harmful = data[data['label'] == 1]

    # Calculate minimum count possible for each category in training and validation
    train_min_count = min(len(harmless), len(harmful), train_rows//2)
    valid_min_count = min(len(harmless) - train_min_count, len(harmful) - train_min_count, valid_rows//2)

    # Split data into training and validation sets
    train_data = pd.concat([harmless.head(train_min_count), harmful.head(train_min_count)])
    valid_data = pd.concat([harmless.iloc[train_min_count:train_min_count+valid_min_count], 
                            harmful.iloc[train_min_count:train_min_count+valid_min_count]])

    # Save to JSONL files
    save_jsonl(train_data, train_filename)
    save_jsonl(valid_data, valid_filename)

def save_jsonl(data, filename):
    # Open the JSONL file for writing
    with open(filename, 'w') as file:
        for _, row in data.iterrows():
            # Construct the sentence object
            sentence = {
                "sentence": f"{row['Title']} {row['Description']}",
                "label": "harmless" if row['label'] == 0 else "harmful"
            }
            # Write the JSON object to the JSONL file
            file.write(json.dumps(sentence) + '\n')

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process an Excel file and output balanced JSONL files for training and validation.')
    parser.add_argument('excel_path', type=str, help='Path to the input Excel file')
    parser.add_argument('train_filename', type=str, help='Filename for the output training JSONL file')
    parser.add_argument('valid_filename', type=str, help='Filename for the output validation JSONL file')
    parser.add_argument('train_rows', type=int, help='Total number of rows for the training set (equal number of harmless and harmful)')
    parser.add_argument('valid_rows', type=int, help='Total number of rows for the validation set (equal number of harmless and harmful)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the file
    process_file(args.excel_path, args.train_filename, args.valid_filename, args.train_rows, args.valid_rows)

if __name__ == '__main__':
    main()
