import pandas as pd

# Load your original CSV
df = pd.read_csv('data/pedestrian-counts-per-hour.csv')

# Convert Sensing_Date to datetime and extract weekday name
df['Sensing_Date'] = pd.to_datetime(df['Sensing_Date'])
df['weekday'] = df['Sensing_Date'].dt.day_name()

# ---- 1. Full heatmap data (all hours, all days) ----
heatmap = df.groupby(['weekday', 'HourDay'])['Total_of_Directions'].mean().reset_index()
heatmap.columns = ['weekday', 'hour', 'avg_pedestrians']
# Order weekdays properly
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
heatmap['weekday'] = pd.Categorical(heatmap['weekday'], categories=weekday_order, ordered=True)
heatmap.sort_values(['weekday', 'hour'], inplace=True)
heatmap.to_csv('pedestrian_heatmap.csv', index=False)

# ---- 2. Late night data (6pm to 2am) ----
late = df[(df['HourDay'] >= 18) | (df['HourDay'] <= 2)]
late_night = late.groupby(['weekday', 'HourDay'])['Total_of_Directions'].mean().reset_index()
late_night.columns = ['weekday', 'hour', 'avg_pedestrians']
late_night['weekday'] = pd.Categorical(late_night['weekday'], categories=weekday_order, ordered=True)
late_night.sort_values(['weekday', 'hour'], inplace=True)
late_night.to_csv('pedestrian_latenight.csv', index=False)

print("✅ Created pedestrian_heatmap.csv and pedestrian_latenight.csv")