import pandas as pd
import re
import json

def clean_text(text):
    """
    Clean text data by fixing encoding issues and normalizing whitespace.
    """
    if pd.isna(text):
        return text
    
    # Convert to string if not already
    text = str(text)
    
    # Fix the specific encoding issues in your data
    # Note: The order matters here!
    replacements = {
        '‚Äë': "' ",  # apostrophe followed by space (soft‚Äëgirly → soft 'girly)
        '‚Äî': " ",   # em-dash becomes space
        '‚Äú': "'",   # opening quote
        '‚Äù': "'",   # closing quote
        '‚Äô': "'",   # apostrophe
        '‚Äì': "-",   # en-dash
        '‚òï': '',    # Remove broken emoji
        '‚ú®': '',    # Remove broken emoji
        '✨': '',      # Remove working emoji too
        '💕': '',      # Remove working emoji too
        '🌸': '',      # Remove working emoji too
        '☀️': '',      # Remove working emoji too
        'üòÖüíª': '', # Remove this specific garbled text
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove any remaining garbled characters (non-ASCII printable characters)
    # This keeps letters, numbers, punctuation, and spaces
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    
    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = text.strip()  # Remove leading/trailing whitespace
    
    return text

def clean_csv(input_file, output_csv, output_json):
    """
    Read CSV, clean the trend_description column, and save to CSV and JSON.
    """
    # Read the CSV with proper encoding handling
    print(f"Reading {input_file}...")
    try:
        # Try UTF-8 first
        df = pd.read_csv(input_file, skipinitialspace=True, encoding='utf-8')
    except UnicodeDecodeError:
        # Fall back to latin1 if UTF-8 fails
        print("UTF-8 failed, trying latin1...")
        df = pd.read_csv(input_file, skipinitialspace=True, encoding='latin1')
    
    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()
    
    # Clean the trend_description column
    print("Cleaning trend_description column...")
    if 'trend_description' in df.columns:
        df['trend_description'] = df['trend_description'].apply(clean_text)
    
    # Optional: Clean other text columns
    text_columns = ['name', 'type', 'trend_description']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Save the cleaned data with UTF-8 encoding
    print(f"Saving cleaned CSV to {output_csv}...")
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    # Convert to JSON - replace NaN with null
    print(f"Converting to JSON...")
    trends_data = df.where(pd.notnull(df), None).to_dict('records')
    
    print(f"Saving JSON to {output_json}...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(trends_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Done! Created {len(trends_data)} trends")
    print(f"✓ CSV: {output_csv}")
    print(f"✓ JSON: {output_json}")
    
    return df

# Example usage
if __name__ == "__main__":
    # Specify your input and output file paths
    input_file = "data/trends_data.csv"
    output_csv = "data/trends_data_cleaned.csv"
    output_json = "data/trends_data.json"
    
    # Clean the CSV and create JSON
    cleaned_df = clean_csv(input_file, output_csv, output_json)
    
    # Display first few rows to verify
    print("\nFirst few rows of cleaned data:")
    print(cleaned_df.head())
    
    # Display a sample trend_description
    if 'trend_description' in cleaned_df.columns:
        print("\nSample cleaned trend_description:")
        print(cleaned_df['trend_description'].iloc[0])