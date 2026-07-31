import pandas as pd

# Read Excel file
xl = pd.ExcelFile('prep_days/Japan_Attractions_Master_Final_v4.xlsx')

print("\n" + "="*100)
print("📊 JAPAN 2026 TRIP - COMPLETE ATTRACTION OVERVIEW")
print("="*100 + "\n")

for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet_name)
    
    print(f"\n🏙️  {sheet_name.upper()}")
    print("-" * 100)
    
    # Filter attractions in itinerary
    in_itinerary = df[df['In Itinerary'] == 'Yes']
    not_in_itinerary = df[df['In Itinerary'] != 'Yes']
    
    print(f"✅ IN ITINERARY ({len(in_itinerary)} attractions):")
    for idx, row in in_itinerary.iterrows():
        rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
        hours = row['Opening Hours'] if pd.notna(row['Opening Hours']) else "N/A"
        att_type = row['Attraction Type'] if pd.notna(row['Attraction Type']) else "N/A"
        area = row['Area'] if pd.notna(row['Area']) else "N/A"
        print(f"  • {row['Attraction']:40} | {rating} | {att_type:15} | {area:15} | {hours}")
    
    print(f"\n❌ NOT IN ITINERARY ({len(not_in_itinerary)} attractions):")
    for idx, row in not_in_itinerary.iterrows():
        rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
        att_type = row['Attraction Type'] if pd.notna(row['Attraction Type']) else "N/A"
        print(f"  • {row['Attraction']:40} | {rating} | {att_type:15}")
    
    print("\n")

print("\n" + "="*100)
print("📈 SUMMARY BY CITY")
print("="*100 + "\n")

for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet_name)
    in_count = len(df[df['In Itinerary'] == 'Yes'])
    total = len(df)
    print(f"{sheet_name:15} | ✅ In Itinerary: {in_count:2} | Total Available: {total:2}")
