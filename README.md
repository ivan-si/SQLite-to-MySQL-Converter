# SQLite to MySQL Dump Converter

## Overview

`sqlite2mysql` is a Python script that converts SQLite database dump files to MySQL-compatible dump files. It handles various SQLite-specific syntax and converts it to MySQL-compatible SQL statements while ensuring file integrity and preserving the original database content.

## Features

- Converts SQLite dump files to MySQL dump files
- Maintains database content integrity
- Filters out non-essential database management statements
- Handles table creation and insertion statements
- Removes SQLite-specific pragmas and transactions
- Converts boolean representations
- Replaces SQLite-specific keywords
- Validates input and output file paths
- Prevents unintended code injection or extra content modification

## Content Integrity Assurance

The script includes several safeguards to ensure the integrity of the database dump:

- Explicitly filters out potentially problematic statements like `BEGIN TRANSACTION`, `COMMIT`, and `sqlite_sequence`
- Removes `PRAGMA` statements that might contain system-specific configurations
- Preserves all original data insertion statements
- Does not modify the actual data content of the dump
- Provides a clean, consistent translation from SQLite to MySQL syntax

## Prerequisites

- Python 3.x
- No additional libraries required beyond standard Python libraries

## Usage

```bash
python sqlite2mysql.py <input_sqlite_dump> <output_mysql_dump>
```

### Arguments

- `<input_sqlite_dump>`: Path to the input SQLite dump file
- `<output_mysql_dump>`: Path to the output MySQL dump file

### Example

```bash
python sqlite2mysql.py database.sqlite database_mysql.sql
```

## Restrictions

- Input file must exist
- Input and output files must be different
- Works best with standard SQLite dump files

## Error Handling

- Checks for non-existent input files
- Prevents overwriting input file
- Provides clear error messages

## License

MIT Licence

## Contributing

Contributions are welcome. Please submit pull requests or open issues on the project repository.
