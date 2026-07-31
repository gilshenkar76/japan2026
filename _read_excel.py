import pandas as pd

# Read Excel file
xl = pd.ExcelFile('prep_days/Japan_Attractions_Master_Final_v4.xlsx')
print("Sheet names:", xl.sheet_names)
print("\n" + "="*80 + "\n")

# Read each sheet
for sheet_name in xl.sheet_names:
    print(f"\n📋 SHEET: {sheet_name}")
    print("="*80)
    df = pd.read_excel(xl, sheet_name=sheet_name)
    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)}\n")
    print(df.to_string())
    print("\n" + "="*80 + "\n")
