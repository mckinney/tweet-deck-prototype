import re

def fix_nan_in_json(input_file, output_file):
    """
    Replace all NaN values with null in JSON file.
    """
    print(f"Reading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Replacing NaN with null...")
    # Replace NaN with null (JSON standard)
    content = re.sub(r'\bNaN\b', 'null', content)
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Done! All NaN values replaced with null")

if __name__ == "__main__":
    input_file = "data/trends_data.json"
    output_file = "data/trends_data.json"  # Overwrite the same file
    
    fix_nan_in_json(input_file, output_file)