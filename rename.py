import os
import csv
import argparse
import re
from fuzzywuzzy import process

# CSV files
csv_file_path = "episodes.csv"
results_csv_path = "output/results.csv"
outlier_csv = 'output/outlier.csv'
errors_csv = 'output/errors.csv'
# Check if prior results, outliers, or errors files exist and remove
if os.path.exists(errors_csv):
    os.remove(errors_csv)
if os.path.exists(results_csv_path):
    os.remove(results_csv_path)
if os.path.exists(outlier_csv):
    os.remove(outlier_csv)

# Normalize episode title for matching
def normalize_title(title):
    # Convert to lower case
    title = title.lower()
    # Replace or remove specific punctuation (e.g., hyphens, apostrophes, question marks)
    title = title.replace("-", " ").replace("'", "").replace("?", "")
    # Remove non-alphanumeric characters (optional, be cautious with this)
    title = re.sub(r'\W+', ' ', title)
    # Trim extra spaces
    title = ' '.join(title.split())
    return title

# Replace or remove characters not allowed in Windows filenames
def sanitize_filename(filename):
    # Replace or remove characters not allowed in Windows filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

# Function to read episode information from a CSV file
def read_episodes_from_csv(csv_file_path):
    episodes = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        while True:
            try:
                code = next(file).strip()
                title = next(file).strip()
                air_date = next(file).strip()
                # Extract year from air_date
                year = air_date.split(',')[-1].strip()

                # Normalize title for consistent matching
                normalized_title = normalize_title(title)
                episodes.append((code, normalized_title, title, year))  # Keep both normalized and original title
            except StopIteration:
                # End of file
                break
            except Exception as e:
                print(f"Error reading file: {e}")
                break
    return episodes

# Function to list files in a directory
def list_files_in_directory(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# Function to use fuzzywuzzy for title matching
def find_best_match(file_title, file_year, episodes):
    # Adjust the logic to also consider the year for a better match
    best_match = None
    highest_score = 0
    for code, norm_title, orig_title, year in episodes:
        # Use fuzzy matching to get a score based on the title similarity
        score = process.extractOne(file_title, [norm_title])[1]
        # Prioritize matches that also have the same year
        if norm_title == file_title and file_year == year:
            score += 50  # Arbitrarily boost the score for year matches
        if score > highest_score:
            highest_score = score
            best_match = (code, norm_title, orig_title, year)
    if highest_score > 90:  # Keep the threshold as before but adjust if necessary
        return best_match
    return None

def get_series_title_by_year(year):
    year = int(year)  # Ensure the year is an integer
    if 1940 <= year <= 1967:
        return "Tom and Jerry"
    elif year == 1975:
        return "The Tom & Jerry Show"
    elif 1990 <= year <= 1993:
        return "Tom and Jerry Kids Show"
    elif 2005 <= year <= 2008:
        return "Tom and Jerry Tales"
    else:
        return None  # For years that don't match any known series

# Main function to rename files based on episode information
def rename_files(directory_path, csv_file_path, results_csv_path, actually_rename, errors_csv):
    episodes = read_episodes_from_csv(csv_file_path)
    errors = []
    # Map normalized titles to their code, original title, and year for matching
    title_to_code_year = {norm_title: (code, orig_title, year) for code, norm_title, orig_title, year in episodes}

    files = list_files_in_directory(directory_path)
    results = []
    for file_name in files:
        parts = file_name.rsplit('[', 1)
        if len(parts) == 2:
            title_with_number = parts[0].strip()
            title = ' '.join(title_with_number.split()[1:])  # Remove leading number
            file_year = parts[1].rstrip('].avi')  # Extract the year from the file name
            series_title = get_series_title_by_year(file_year)  # Determine the series title based on the year
            
            if series_title is None:
                print(f"Year {file_year} does not match any known series, skipping: {file_name}")
                continue  # Skip files that don't match any known series based on year
            
            norm_title = normalize_title(title)
            best_match = find_best_match(norm_title, file_year, episodes)
            if best_match:
                code, _, orig_title, year = best_match
                sanitized_title = sanitize_filename(orig_title)  # Sanitize the title
                new_name = f"{series_title}.{code}.{sanitized_title}.{year}.avi"
                results.append((file_name, new_name))
                if actually_rename:
                    original_full_path = os.path.join(directory_path, file_name)
                    new_full_path = os.path.join(directory_path, new_name)
                    try:
                        os.rename(original_full_path, new_full_path)
                    except Exception as e:
                        error_message = f"Error renaming {file_name} to {new_name}: {e}"
                        print(error_message)
                        errors.append((file_name, new_name, str(e)))
                        continue
            else:
                results.append((file_name, "No match found. Skipping."))

    # After processing all files, write results and errors to their respective CSV files
    with open(results_csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Original Name", "New Name"])
        writer.writerows(results)

    if errors:  # If there were any errors, write them to errors.csv
        with open(errors_csv, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Original Name", "Attempted New Name", "Error"])
            writer.writerows(errors)

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Rename files based on episode information.")
parser.add_argument("directory_path", type=str, help="Path to the episodes folder.")
parser.add_argument("--run", action="store_true", help="Actually rename the files. Without this, the script will only perform a dry run.")
args = parser.parse_args()

# Call the function with the provided arguments
rename_files(args.directory_path, csv_file_path, results_csv_path, args.run, errors_csv)


def verify_results(results_csv_path, outlier_csv):
    review_list = []
    unmatched_files = []

    # Read results and compare original vs. new names
    with open(results_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_name = row['Original Name'].rsplit('[', 1)[0].strip()
            new_name = row['New Name']
            if "No match found. Skipping." in new_name:
                unmatched_files.append({"Original Name": original_name, "New Name": "No match found"})
            elif not new_name.startswith("Tom and Jerry.") or original_name.lower() not in new_name.lower():
                review_list.append(row)

    # Combine the review list and unmatched files list for the outlier report
    outlier_report = unmatched_files

    # Write outlier report to a separate CSV if there are mismatches or unmatched files
    if outlier_report:
        with open(outlier_csv, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Original Name', 'New Name'])
            writer.writeheader()
            writer.writerows(outlier_report)
    else:
        print("No mismatches found.")

# Ensure to pass the 'outlier_csv' variable to the verify_results function call
verify_results(results_csv_path, outlier_csv)

