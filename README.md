# Tom and Jerry Episode Renamer - Plex
Inspired by: https://github.com/macdonaldr93/rename-looney-tunes-gold-collection-plex

## Overview
This Python script automates the process of renaming Tom and Jerry episode files based on a structured CSV file containing episode metadata (episode code, title, and original air date). The script matches filenames to episode titles, renames files to include the show title, season and episode code, the original title, and the air year, and generates a report of actions taken.

## Features
- **Normalization**: Standardizes episode titles for consistent matching, even with minor variations in spelling or punctuation.
- **Fuzzy Matching**: Utilizes fuzzy matching to find the best match for each file, allowing for some discrepancies between file names and episode titles.
- **Dry Run Mode**: By default, the script simulates renaming for review, ensuring accuracy before making any changes.
- **Flexible Matching**: Adjusts for common variations in naming conventions to improve match accuracy.
- **Report Generation**: Outputs a CSV file detailing the original and new filenames. Generates an outlier report for any mismatches or files that couldn't be matched.

## Dependencies
- Python 3.6 or higher
- `fuzzywuzzy` Python package (including `python-Levenshtein` for speedup)

```bash
pip install -r requirements.txt
```

## Usage
### CLI Arguments
- `directory_path`: Path to the folder containing the episode files to be renamed.
- `--run`: Flag to execute file renaming. Without this, the script performs a dry run.

### Running the Script
Navigate to the script's directory in your terminal, and run:
```bash
python rename.py "path\to\episode\folder"
```

To actually rename the files, include the --run flag:
```bash
python rename.py "path\to\episode\folder" --run
```

### CSV File Format
All episodes pulled off of the TVDB
- https://thetvdb.com/series/tom-and-jerry#seasons
- https://thetvdb.com/series/the-new-tom-and-jerry-show#seasons
- https://thetvdb.com/series/tom-and-jerry-kids-show#seasons
- https://thetvdb.com/series/tom-and-jerry-tales#seasons

The `episodes.csv`` file follow this format:
```bash
S01E01
Episode Title
Original Air Date
```

The **cleaning** folder in the root dir contains the regex script used to clean up copy-pasta-ing from TVDB to get the CSV data.

### Results and Outlier Reports
- `results.csv`: Lists original and new filenames after script execution.
- `outlier.csv`: Contains files that could not be matched or had discrepancies that require review.
- `errors.csv`: Logs any errors encountered during the renaming process, such as files being in use by another process or permission issues.
