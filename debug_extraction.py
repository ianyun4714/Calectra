import pandas as pd

file_path = 'data/Cambium24_Workbook.xlsx'

# Read directly and check what's in the data
df = pd.read_excel(file_path, sheet_name='Data - Time-of-day - Costs', header=4)
print(f"DataFrame shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Forward fill region
df['Region'] = df['Region'].ffill()

# Get CAISO
caiso = df[df['Region'] == 'CAISO'].copy()
print(f"\nCAISO rows: {len(caiso)}")

# Check hour 18
hour_18 = caiso[caiso['Hour'] == 18].iloc[0]
print(f"\nHour 18 CAISO - all columns:")
for col in df.columns:
    val = hour_18[col]
    if pd.notna(val):
        print(f"  {col}: {val}")

# Now let's see what process_data.py is loading
print("\n\nChecking dashboard_data.json:")
import json
with open('dashboard/public/data/dashboard_data.json', 'r') as f:
    data = json.load(f)

lmp = data['lmpAnalysis']['data']
caiso_2050_mid = [x for x in lmp if x['scenario'] == 'MidCase' and x['year'] == 2050 and x['region'] == 'CAISO' and x['month'] == 'January'][0]
print(f"Hour 18 value in dashboard: ${caiso_2050_mid['hourlyData'][18]['cost']:.2f}")

caiso_2025_mid = [x for x in lmp if x['scenario'] == 'MidCase' and x['year'] == 2025 and x['region'] == 'CAISO' and x['month'] == 'January'][0]
print(f"Hour 18 value 2025 in dashboard: ${caiso_2025_mid['hourlyData'][18]['cost']:.2f}")
