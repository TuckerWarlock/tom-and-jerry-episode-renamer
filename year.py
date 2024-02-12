import os
import re

# Define your directory path
directory_path = r"path/to/files"

# Series title based on year
def series_title_by_year(year):
    if 1940 <= year <= 1967:
        return "Tom and Jerry"
    elif year == 1975:
        return "The Tom & Jerry Show"
    elif 1990 <= year <= 1993:
        return "Tom and Jerry Kids Show"
    elif 2005 <= year <= 2008:
        return "Tom and Jerry Tales"
    else:
        return "Tom and Jerry"  # Default, adjust as needed

# Rename files based on year
def rename_files_based_on_year(directory_path):
    for filename in os.listdir(directory_path):
        match = re.search(r'\.(\d{4})\.avi$', filename)
        if match:
            year = int(match.group(1))
            new_series_title = series_title_by_year(year)
            new_filename = re.sub(r'^Tom and Jerry', new_series_title, filename)
            original_full_path = os.path.join(directory_path, filename)
            new_full_path = os.path.join(directory_path, new_filename)
            try:
                os.rename(original_full_path, new_full_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except Exception as e:
                print(f"Error renaming {filename} to {new_filename}: {e}")

# Run the function
rename_files_based_on_year(directory_path)
