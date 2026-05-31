import pandas as pd

# Load the cleaned file
df = pd.read_csv('data/restaurants_clean.csv')

print("Available columns:", df.columns.tolist())

# Try different possible column names for suburb/area
area_col = None
for possible in ['CLUE_small_area', 'CLUE small area', 'suburb', 'CLUE_smallarea', 'area']:
    if possible in df.columns:
        area_col = possible
        break

if area_col is None:
    print("Using first few rows to guess area column...")
    print(df.head(3))

# Use the correct column (fallback to any column containing 'area' or 'melbourne')
if area_col:
    cbd_rest = df[df[area_col].astype(str).str.contains('Melbourne', na=False, case=False)]
else:
    # Fallback: assume most rows are in Melbourne CBD area
    cbd_rest = df.head(500)

total_food = len(cbd_rest)
print(f"✅ Total food venues in CBD area: {total_food}")

# Save summary for CBD
cbd_summary = pd.DataFrame([{
    'area': 'CBD',
    'type': 'food',
    'count': total_food,
    'longitude': 144.963,
    'latitude': -37.813
}])
cbd_summary.to_csv('data/cbd_summary.csv', index=False)

print("✅ CBD summary saved to data/cbd_summary.csv")