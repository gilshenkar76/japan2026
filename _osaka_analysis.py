import pandas as pd

# Read Osaka sheet
xl = pd.ExcelFile('prep_days/Japan_Attractions_Master_Final_v4.xlsx')
df = pd.read_excel(xl, sheet_name='Osaka')

print("\n" + "="*100)
print("🏙️  OSAKA ITINERARY ANALYSIS")
print("="*100 + "\n")

# Filter attractions in itinerary
in_itinerary = df[df['In Itinerary'] == 'Yes'].sort_values('Real Rating', ascending=False)
not_in_itinerary = df[df['In Itinerary'] != 'Yes'].sort_values('Real Rating', ascending=False)

print(f"✅ IN YOUR ITINERARY ({len(in_itinerary)} attractions)")
print("-" * 100)
for idx, row in in_itinerary.iterrows():
    rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
    hours = row['Opening Hours'] if pd.notna(row['Opening Hours']) else "N/A"
    att_type = row['Attraction Type'] if pd.notna(row['Attraction Type']) else "N/A"
    area = row['Area'] if pd.notna(row['Area']) else "N/A"
    best_time = row['Best Visit Time'] if pd.notna(row['Best Visit Time']) else "N/A"
    weather = row['Weather Suitability'] if pd.notna(row['Weather Suitability']) else "N/A"
    print(f"  {rating} | {row['Attraction']:30} | {area:12} | {att_type:15} | {best_time:10} | {weather}")

print(f"\n\n❌ NOT IN YOUR ITINERARY ({len(not_in_itinerary)} attractions)")
print("-" * 100)
print("🌟 HIGH-RATED OPTIONS YOU'RE MISSING:\n")

# Show high-rated missing attractions
high_rated = not_in_itinerary[not_in_itinerary['Real Rating'] >= 4.7]
for idx, row in high_rated.iterrows():
    rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
    att_type = row['Attraction Type'] if pd.notna(row['Attraction Type']) else "N/A"
    area = row['Area'] if pd.notna(row['Area']) else "N/A"
    ticket = row['Ticket Advice'] if pd.notna(row['Ticket Advice']) else "N/A"
    best_time = row['Best Visit Time'] if pd.notna(row['Best Visit Time']) else "N/A"
    print(f"  {rating} | {row['Attraction']:30} | {area:12} | {att_type:15} | {ticket:15} | {best_time}")

print("\n\n📊 ATTRACTION BREAKDOWN BY TYPE:")
print("-" * 100)
print("\n✅ IN ITINERARY:")
print(in_itinerary['Attraction Type'].value_counts().to_string())

print("\n\n❌ NOT IN ITINERARY:")
print(not_in_itinerary['Attraction Type'].value_counts().to_string())

print("\n\n🎯 AREA COVERAGE:")
print("-" * 100)
print("\n✅ IN ITINERARY:")
print(in_itinerary['Area'].value_counts().to_string())

print("\n\n🏆 TOP 10 HIGHEST-RATED OSAKA ATTRACTIONS (Overall):")
print("-" * 100)
top10 = df.nlargest(10, 'Real Rating')
for idx, row in top10.iterrows():
    rating = f"⭐{row['Real Rating']}" if pd.notna(row['Real Rating']) else "⭐N/A"
    in_it = "✅" if row['In Itinerary'] == 'Yes' else "❌"
    area = row['Area'] if pd.notna(row['Area']) else "N/A"
    print(f"  {in_it} {rating} | {row['Attraction']:30} | {area}")

print("\n" + "="*100)
