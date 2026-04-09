import json

# Load the updated data
with open('public/data/dashboard_data.json', 'r') as f:
    data = json.load(f)

# Find CAISO 2050 MidCase January
lmp = data['lmpAnalysis']
caiso_2050 = [item for item in lmp['data'] 
              if item['scenario'] == 'MidCase' 
              and item['year'] == 2050 
              and item['region'] == 'CAISO'
              and item['month'] == 'January'][0]

print("✓ VERIFICATION: CAISO 2050 MidCase January")
print("=" * 70)
print(f"Hour 0 (12 AM):  ${caiso_2050['hourlyData'][0]['cost']:>8.2f}/MWh")
print(f"Hour 18 (6 PM):  ${caiso_2050['hourlyData'][18]['cost']:>8.2f}/MWh")
print()
print(f"Requirements: Hour 0 ~$37.1, Hour 18 ~$286.1")
print()

# Find peak
peak = max(caiso_2050['hourlyData'], key=lambda x: x['cost'])
print(f"Peak: Hour {peak['hour']} = ${peak['cost']:.2f}/MWh")

# Also check 2025 to understand pattern
caiso_2025 = [item for item in lmp['data'] 
              if item['scenario'] == 'MidCase' 
              and item['year'] == 2025 
              and item['region'] == 'CAISO'
              and item['month'] == 'January'][0]

print(f"\nComparison - 2025 MidCase:")
print(f"Hour 0:  ${caiso_2025['hourlyData'][0]['cost']:>8.2f}/MWh")
print(f"Hour 18: ${caiso_2025['hourlyData'][18]['cost']:>8.2f}/MWh")
