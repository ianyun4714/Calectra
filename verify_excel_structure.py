import pandas as pd
import openpyxl

# Check the actual Excel structure
file_path = 'data/Cambium24_Workbook.xlsx'

print("=" * 80)
print("CAMBIUM24 WORKBOOK - DATA VERIFICATION")
print("=" * 80)

# List all sheets
wb = openpyxl.load_workbook(file_path)
print("\n1. ALL SHEETS:")
for i, sheet in enumerate(wb.sheetnames, 1):
    print(f"   {i}. {sheet}")

# Check Data - Time-of-day - Costs sheet
print("\n2. DATA - TIME-OF-DAY - COSTS SHEET:")
df_hourly = pd.read_excel(file_path, sheet_name='Data - Time-of-day - Costs', header=4)
print(f"   Shape: {df_hourly.shape}")
print(f"   Columns: {list(df_hourly.columns)}")
print(f"\n   CAISO data (expected 24 hours):")
caiso_df = df_hourly[df_hourly['Region'].fillna(method='ffill') == 'CAISO'].copy()
print(f"   Found {len(caiso_df)} rows")
print(f"\n   Hour 0 (12 AM):")
if len(caiso_df) > 0:
    row_0 = caiso_df[caiso_df['Hour'] == 0].iloc[0] if len(caiso_df[caiso_df['Hour'] == 0]) > 0 else None
    if row_0 is not None:
        print(f"   - Combined: ${row_0['Combined']:.2f}/MWh")
        print(f"   - Energy: ${row_0['Energy']:.2f}")
        print(f"   - Capacity: ${row_0['Capacity']:.2f}")
        print(f"   - 2025 value: {row_0.get(2025, 'N/A')}")
        print(f"   - 2050 value: {row_0.get(2050, 'N/A')}")

print(f"\n   Hour 18 (6 PM):")
if len(caiso_df) > 0:
    row_18 = caiso_df[caiso_df['Hour'] == 18].iloc[0] if len(caiso_df[caiso_df['Hour'] == 18]) > 0 else None
    if row_18 is not None:
        print(f"   - Combined: ${row_18['Combined']:.2f}/MWh")
        print(f"   - Energy: ${row_18['Energy']:.2f}")
        print(f"   - Capacity: ${row_18['Capacity']:.2f}")
        print(f"   - 2025 value: {row_18.get(2025, 'N/A')}")
        print(f"   - 2050 value: {row_18.get(2050, 'N/A')}")

# Check Data - Annual - Costs sheet
print("\n3. DATA - ANNUAL - COSTS SHEET:")
df_annual = pd.read_excel(file_path, sheet_name='Data - Annual - Costs', header=4)
print(f"   Shape: {df_annual.shape}")
print(f"   Columns: {list(df_annual.columns)}")
caiso_annual = df_annual[df_annual['Region'].fillna(method='ffill') == 'CAISO'].copy()
if len(caiso_annual) > 0:
    print(f"   CAISO Annual Average:")
    print(f"   - Combined: ${caiso_annual['Combined'].iloc[0]:.2f}/MWh")
    print(f"   - 2025: {caiso_annual[2025].iloc[0]}")
    print(f"   - 2050: {caiso_annual[2050].iloc[0]}")

# Check Scenario Definitions
print("\n4. SCENARIO DEFINITIONS:")
df_scenarios = pd.read_excel(file_path, sheet_name='Scenario Definitions')
print(f"   Shape: {df_scenarios.shape}")
print(f"   Columns: {list(df_scenarios.columns)}")
print(f"   Scenarios: {df_scenarios.iloc[:, 0].tolist()}")

# Check Timezones/GEA
print("\n5. TIMEZONES/GEA:")
df_timezones = pd.read_excel(file_path, sheet_name='Timezones')
print(f"   Shape: {df_timezones.shape}")
print(f"   Regions: {df_timezones.iloc[:, 0].tolist()}")

print("\n" + "=" * 80)
