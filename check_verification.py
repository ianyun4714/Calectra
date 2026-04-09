import pandas as pd
import openpyxl

file_path = 'data/Cambium24_Workbook.xlsx'

print("VERIFICATION REQUIREMENT CHECK")
print("=" * 80)
print("User requirement: When filters = [Region: CAISO, Scenario: Mid-case, Year: 2050]")
print("Chart must show:")
print("  - Hour 18 (6 PM): ~$286.1/MWh")
print("  - Hour 0 (12 AM): ~$37.1/MWh")
print("  - Annual Average: ~$60.4/MWh")
print("\n" + "=" * 80)

# Read Time-of-day costs
df = pd.read_excel(file_path, sheet_name='Data - Time-of-day - Costs', header=4)
df['Region'] = df['Region'].ffill()

# Get CAISO data
caiso = df[df['Region'] == 'CAISO'].reset_index(drop=True)

print("\nRaw Excel Data - CAISO Combined Costs (MidCase, base 2025 year column):")
print(f"Hour 0: ${caiso[caiso['Hour'] == 0]['Combined'].values[0]:.2f}/MWh")
print(f"Hour 18: ${caiso[caiso['Hour'] == 18]['Combined'].values[0]:.2f}/MWh")

# What year columns exist?
print(f"\nYear columns in Data - Time-of-day - Costs sheet:")
year_cols = [col for col in df.columns if isinstance(col, int) and 2000 < col < 2100]
print(f"Years: {sorted(year_cols)}")

# Current dashboard values (from previous test)
print(f"\nCurrent Dashboard Values (with 0.8 year multiplier for 2050):")
print(f"Hour 0: $31.86/MWh (expected: ~$37.1)")
print(f"Hour 18: $246.04/MWh (expected: ~$286.1)")

print(f"\nAnalysis:")
print(f"Raw Hour 18: $286.09")
print(f"With 0.8 multiplier: $286.09 * 0.8 = ${286.09 * 0.8:.2f}")
print(f"Expected: $286.1")
print(f"\nConclusion: Year multiplier should be 1.0 (no discount), not 0.8")
