import pandas as pd

# ------------------------------
# 1. Load data
# ------------------------------
# Distance file (suburbs with distance from CBD)
distance_df = pd.read_csv(
    r'C:\Users\asany\DV2_Maihemuti\data\Melbourne Suburbs by Distance & Direction from CBD.csv'
)
distance_df.columns = ['Postcode', 'Suburb', 'Distance_km', 'Direction']
distance_df = distance_df[['Suburb', 'Distance_km']].drop_duplicates()

# CLUE restaurants file
clue_df = pd.read_csv(
    r'C:\Users\asany\DV2_Maihemuti\data\restaurants.csv',
    low_memory=False
)

# ------------------------------
# 2. Aggregate venue counts by 'CLUE small area'
# ------------------------------
venue_counts = clue_df.groupby('CLUE small area').size().reset_index(name='venue_count')

# ------------------------------
# 3. Manual mapping from CLUE small area → standard suburb name (for distance lookup)
# ------------------------------
# This is the key: we know the exact 13 areas, so we map each to a suburb name in the distance CSV.
mapping = {
    'Melbourne (CBD)': 'Melbourne',
    'Melbourne (Remainder)': 'Melbourne',        # same as CBD? Actually remainder is still Melbourne
    'Carlton': 'Carlton',
    'Docklands': 'Docklands',
    'East Melbourne': 'East Melbourne',
    'Kensington': 'Kensington',
    'North Melbourne': 'North Melbourne',
    'Parkville': 'Parkville',
    'Port Melbourne': 'Port Melbourne',
    'South Yarra': 'South Yarra',
    'Southbank': 'Southbank',
    'West Melbourne (Industrial)': 'West Melbourne',
    'West Melbourne (Residential)': 'West Melbourne'
}

venue_counts['Suburb_lookup'] = venue_counts['CLUE small area'].map(mapping)

# Drop if any missing (shouldn't happen)
venue_counts = venue_counts.dropna(subset=['Suburb_lookup'])

# ------------------------------
# 4. Join with distance data using the lookup suburb name
# ------------------------------
combined = pd.merge(
    venue_counts,
    distance_df,
    left_on='Suburb_lookup',
    right_on='Suburb',
    how='left'
)

# Keep only needed columns
combined = combined[['CLUE small area', 'Suburb_lookup', 'venue_count', 'Distance_km']]
combined.columns = ['CLUE_Area', 'Suburb', 'venue_count', 'distance_km']

# ------------------------------
# 5. Save result
# ------------------------------
output_path = r'C:\Users\asany\DV2_Maihemuti\data\combined_13_suburbs.csv'
combined.to_csv(output_path, index=False)
print("✅ Combined data saved to:", output_path)
print("\n📊 Result preview:")
print(combined)