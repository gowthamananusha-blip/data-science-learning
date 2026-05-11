import csv
import json
from pathlib import Path

# Create output directory
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# ---------- 1. Read CSV ----------
csv_path = Path("data/raw_data.csv")
data = []

print("Reading CSV file...")
with open(csv_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

print(f"Original rows: {len(data)}")

# ---------- 2. Read JSON ----------
json_path = Path("data/metadata.json")
print("Reading JSON file...")
with open(json_path, 'r', encoding='utf-8') as file:
    metadata = json.load(file)

print(f"Metadata source: {metadata.get('source', 'Unknown')}")

# ---------- 3. Clean missing rows ----------
cleaned_data = []

for row in data:
    # Check for missing values
    has_missing = False
    
    for key, value in row.items():
        # Check empty string, 'missing', or None
        if value == '' or value == 'missing' or value is None:
            has_missing = True
            break
    
    if not has_missing:
        # Convert age to int if needed
        if 'age' in row and row['age']:
            try:
                row['age'] = int(row['age'])
            except:
                pass # Keep as is if can't convert
        
        # Convert score to float if needed
        if 'score' in row and row['score']:
            try:
                row['score'] = float(row['score'])
            except:
                has_missing = True
        
        if not has_missing:
            cleaned_data.append(row)

print(f"Cleaned rows: {len(cleaned_data)}")
print(f"Rows removed: {len(data) - len(cleaned_data)}")

# ---------- 4. Export to CSV ----------
output_path = output_dir / "cleaned_output.csv"

if cleaned_data:
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        # Get field names from first row
        fieldnames = cleaned_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(cleaned_data)
    
    print(f"\nCleaned data saved to: {output_path}")
    
    # Show cleaned data
    print("\n--- Cleaned Data Preview ---")
    for i, row in enumerate(cleaned_data[:5]): # Show first 5 rows
        print(f"Row {i+1}: {row}")
else:
    print("No clean data to save!")

# ---------- 5. Save log file ----------
log_path = output_dir / "cleaning_log.txt"
with open(log_path, 'w', encoding='utf-8') as log:
    log.write(f"Original rows: {len(data)}\n")
    log.write(f"Cleaned rows: {len(cleaned_data)}\n")
    log.write(f"Rows removed: {len(data) - len(cleaned_data)}\n")
    log.write(f"Metadata source: {metadata.get('source', 'N/A')}\n")
    log.write(f"Date created: {metadata.get('date_created', 'N/A')}\n")

print(f"\nCleaning log saved to: {log_path}")

# ---------- 6. Verify output folder contents ----------
print("\n--- Output Folder Contents ---")
for file in output_dir.iterdir():
    print(f" - {file.name}")
