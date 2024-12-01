import re
import sys
import os
import argparse

def convert_sqlite_to_mysql(sqlite_dump_path, mysql_dump_path):
    with open(sqlite_dump_path, 'r') as input_file, open(mysql_dump_path, 'w') as output_file:
        sys.stdout = output_file
        for line in input_file:
            process = False
            for nope in ('BEGIN TRANSACTION', 'COMMIT', 
                         'sqlite_sequence', 'CREATE UNIQUE INDEX'):
                if nope in line:
                    break
            else:
                process = True
            if not process:
                continue
            # Remove PRAGMA statements
            line = re.sub(r'PRAGMA[^\n]*\n', '', line)
            # Handle CREATE TABLE statements
            create_table_match = re.match(r'CREATE TABLE "?([a-z_]+)"? \((.*)', line)
            if create_table_match:
                table_name = create_table_match.group(1)
                remainder = create_table_match.group(2)
                line = f'DROP TABLE IF EXISTS `{table_name}`; CREATE TABLE IF NOT EXISTS `{table_name}` ({remainder}'
            # Handle INSERT statements
            insert_match = re.match(r'INSERT INTO "?([a-z_]+)"?(.*)', line)
            if insert_match:
                table_name = insert_match.group(1)
                remainder = insert_match.group(2)
                line = f'INSERT INTO `{table_name}`{remainder}'
            # Convert boolean representations
            line = re.sub(r"([^'])'t'(.)", r"\1THIS_IS_TRUE\2", line)
            line = line.replace('THIS_IS_TRUE', '1')
            line = re.sub(r"([^'])'f'(.)", r"\1THIS_IS_FALSE\2", line)
            line = line.replace('THIS_IS_FALSE', '0')
            # Replace SQLite-specific keywords
            line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
            # Replace double quotes with backticks for identifiers
            line = re.sub(r'"([a-z_]+)"', r'`\1`', line)
            # Write the processed line
            print(line, end='')

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Convert SQLite dump to MySQL dump')
    parser.add_argument('input_file', help='Path to the input SQLite dump file')
    parser.add_argument('output_file', help='Path to the output MySQL dump file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input and output file paths
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    if os.path.abspath(args.input_file) == os.path.abspath(args.output_file):
        print("Error: Input and output files must be different.")
        sys.exit(1)
    
    # Convert the dump
    convert_sqlite_to_mysql(args.input_file, args.output_file)
    print(f"Conversion complete. MySQL dump saved to {args.output_file}")

if __name__ == '__main__':
    main()
