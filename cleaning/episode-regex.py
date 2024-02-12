import re
import os

# File paths
input_file_path = 'cleaning\\to_clean.csv'
output_file_path = 'cleaning\\cleaned.csv'

# Check if cleaned.csv exists and delete it if it does
if os.path.exists(output_file_path):
    os.remove(output_file_path)

# Read the content from the input file
with open(input_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Remove the header
text = re.sub(r'^\s*Name\s+First Aired\s+Runtime\s+Image\s*\n', '', text, flags=re.MULTILINE)

# Adjusted regex pattern to clean up and format the text
pattern = r'(S\d+E\d+)\s+([^\t\n]+)\s*\n([^\n]+)\n([A-Z]+\n\s*\d+\s*|season finale\n*)?'
replacement = r'\1\n\2\n\3\n'

# Apply the regex to the text
cleaned_text = re.sub(pattern, replacement, text)

# Further clean up to remove any "season finale" that might appear elsewhere
cleaned_text = re.sub(r'\s*season finale\s*\n', '\n', cleaned_text, flags=re.MULTILINE)

# Remove any trailing network name and digits at the end of the file
cleaned_text = re.sub(r'[A-Z]+\n\s*\d+\s*$', '', cleaned_text, flags=re.MULTILINE)

# Write the cleaned and formatted text to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

# Clear the contents of to_clean.csv after successful completion
with open(input_file_path, 'w', encoding='utf-8') as file:
    file.write('')

print(f"Cleaned text has been written to {output_file_path} and {input_file_path} has been cleared.")
