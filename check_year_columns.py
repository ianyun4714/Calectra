import pandas as pd

file_path = 'data/Cambium24_Workbook.xlsx'

# Read Time-of-day costs
df = pd.read_excel(file_path, sheet_name='Data - Time-of-day - Costs', header=4)
df['Region'] = df['Region'].ffill()

# Get CAISO hour 0 and 18
caiso = df[df['Region'] == 'CAISO'].reset_index(drop=True)

print("EXCEL YEAR COLUMNS - CAISO CAISO Combined Costs")
print("=" * 80)
print(f"{'Hour':<8} {'2025':<12} {'2030':<12} {'2035':<12} {'2040':<12} {'2045':<12} {'2050':<12}")
print("-" * 80)

for hour in [0, 6, 12, 18, 23]:
    row = caiso[caiso['Hour'] == hour].iloc[0]
    print(f"{hour:<8} {row[2025]:<12.2f} {row[2030]:<12.2f} {row[2035]:<12.2f} {row[2040]:<12.2f} {row[2045]:<12.2f} {row[2050]:<12.2f}")

print()
print("BASE 'Combined' COLUMN (appears to be baseline/2025):")
print(f"Hour 0:  ${caiso[caiso['Hour'] == 0]['Combined'].iloc[0]:.2f}/MWh")
print(f"Hour 18: ${caiso[caiso['Hour'] == 18]['Combined'].iloc[0]:.2f}/MWh")
