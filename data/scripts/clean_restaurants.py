import pandas as pd

# ================== CONFIG ==================
input_file = 'data/restaurants.csv'
output_file = 'data/restaurants_clean.csv'
# ===========================================

print("Reading and cleaning restaurants data...")

# Try to read the file, skipping bad header lines
try:
    # Read all lines and find where real data starts
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the first line that looks like a proper header
    header_line = None
    start_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('Census year') or 'Census_year' in line or 'Longitude' in line:
            header_line = line.strip()
            start_index = i
            break
    
    if header_line is None:
        # Fallback: assume header starts around line 11-12
        start_index = 11
    
    # Read the data using pandas from the correct starting point
    df = pd.read_csv(input_file, skiprows=start_index)
    
    # Clean column names
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        'Number of seats': 'Number_of_seats',
        'Number_of_seats': 'Number_of_seats',
        'Longitude': 'Longitude',
        'Latitude': 'Latitude'
    })
    
    # Keep only relevant columns
    keep_cols = ['Trading_name', 'CLUE_small_area', 'Number_of_seats', 
                 'Longitude', 'Latitude', 'Industry_ANZSIC4_description']
    
    available_cols = [col for col in keep_cols if col in df.columns]
    df_clean = df[available_cols].copy()
    
    # Drop rows with missing coordinates
    df_clean = df_clean.dropna(subset=['Longitude', 'Latitude'])
    
    # Convert seats to numeric
    if 'Number_of_seats' in df_clean.columns:
        df_clean['Number_of_seats'] = pd.to_numeric(df_clean['Number_of_seats'], errors='coerce')
    
    print(f"✅ Cleaned data: {len(df_clean)} restaurants loaded")
    print(df_clean.head())
    
    # Save clean version
    df_clean.to_csv(output_file, index=False)
    print(f"✅ Clean file saved as: {output_file}")
    
except Exception as e:
    print(f"❌ Error: {e}")