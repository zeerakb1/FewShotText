import csv
import json
import argparse

def helper(input_csv_file, output_jsonl_file):
    with open(input_csv_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with open(output_jsonl_file, mode='w', encoding='utf-8') as jsonl_file:
            for row in csv_reader:
                text = row['text']
                label = "Harmful" if row['label'] == '1' else "Harmless"
                
                # Modfy the key based on the label in your CSV file
                jsonl_data = {"sentence": text, "label": label}
                
                jsonl_file.write(json.dumps(jsonl_data) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to JSONL with label transformation.')
    parser.add_argument('input_csv', type=str, help='The input CSV file name')
    parser.add_argument('output_jsonl', type=str, help='The output JSONL file name')

    args = parser.parse_args()

    helper(args.input_csv, args.output_jsonl)
