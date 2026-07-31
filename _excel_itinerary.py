import pandas as pd

# Read Excel file
xl = pd.ExcelFile('prep_days/Japan_Attractions_Master_Final_v4.xlsx')

print("\n" + "="*100)
print("🗾 JAPAN 2026 TRIP - COMPLETE ITINERARY (FROM EXCEL ONLY)")
print("="*100 + "\n")

# Process each city sheet
for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet_name)
    
    # Filter only attractions IN itinerary
    in_itinerary = df[df['In Itinerary'] == 'Yes'].sort_values('Area')
    
    if len(in_itinerary) == 0:
        continue
        
    print(f"\n{'='*100}")
    print(f"🏙️  {sheet_name.upper()}")
    print(f"{'='*100}")
    print(f"\n✅ CONFIRMED ATTRACTIONS ({len(in_itinerary)} total):\n")
    
    # Group by area for better organization
    for area in in_itinerary['Area'].unique():
        area_attractions = in_itinerary[in_itinerary['Area'] == area]
        print(f"\n📍 {area}:")
        print("-" * 100)
        
        for idx, row in area_attractions.iterrows():
            rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
            hours = row['Opening Hours'] if pd.notna(row['Opening Hours']) else "N/A"
            att_type = row['Attraction Type'] if pd.notna(row['Attraction Type']) else "N/A"
            best_time = row['Best Visit Time'] if pd.notna(row['Best Visit Time']) else "Anytime"
            weather = row['Weather Suitability'] if pd.notna(row['Weather Suitability']) else "N/A"
            ticket = row['Ticket Advice'] if pd.notna(row['Ticket Advice']) else "N/A"
            
            print(f"  {rating} {row['Attraction']:35} | {att_type:16} | {hours:20} | {best_time:10}")
            if ticket != "⚪ Not Needed":
                print(f"       💳 Ticket: {ticket}")

print("\n\n" + "="*100)
print("📊 TRIP SUMMARY")
print("="*100 + "\n")

total_all = 0
total_in = 0

for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sheet_name)
    in_count = len(df[df['In Itinerary'] == 'Yes'])
    total = len(df)
    total_all += total
    total_in += in_count
    
    if in_count > 0:
        print(f"  {sheet_name:15} | ✅ In Itinerary: {in_count:2} | Total Available: {total:2} | Coverage: {in_count/total*100:.0f}%")

print(f"\n  {'TOTAL':15} | ✅ In Itinerary: {total_in:2} | Total Available: {total_all:2} | Coverage: {total_in/total_all*100:.0f}%")

print("\n" + "="*100)
