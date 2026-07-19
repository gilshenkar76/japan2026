from PIL import Image

# Open the PNG file
input_path = r"prep_days/14.11.2026.png"
img = Image.open(input_path)

# Define crop coordinates for each attraction image based on the PNG layout
# Format: (left, top, right, bottom)
attractions = {
    'tokyo_metro': (343, 519, 522, 609),          # Tokyo Metropolitan Government Building
    'shinjuku_gyoen': (343, 641, 522, 741),       # Shinjuku Gyoen National Garden
    'ramen': (343, 768, 522, 868),                # RAMEN bowl
    'romancecar': (343, 894, 522, 974),           # Odakyu Romancecar train
    'aura_tachibana': (343, 1003, 522, 1093)      # Aura Tachibana ryokan
}

# Extract and save each attraction image
for name, coords in attractions.items():
    attraction_img = img.crop(coords)
    output_path = f"assets/maps/day14_{name}.png"
    attraction_img.save(output_path)
    print(f"Saved: {output_path} - {attraction_img.size}")

print("All Day 14 attraction images extracted!")
