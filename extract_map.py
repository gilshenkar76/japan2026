"""
Extract the walking route map from the bottom-left corner of 14.11.2026.png
ONLY the map visual with colored pins - NO text at all
"""
from PIL import Image
import os

# Paths
input_path = r"prep_days\14.11.2026.png"
output_path = r"assets\maps\day14_walking_map.png"

# Load the image
img = Image.open(input_path)
width, height = img.size

print(f"Original image size: {width}x{height}")

# Extract ONLY the map visual - the street map with numbered colored pins
# Skip: title at top, legend at bottom

left = 20
top = int(height * 0.655)  # Skip title text completely
right = int(width * 0.35)
bottom = int(height * 0.825)  # Before legend text starts

# Crop to get the map
map_section = img.crop((left, top, right, bottom))

# Save without making square - keep original proportions
map_section.save(output_path)
print(f"Map extracted and saved to: {output_path}")
print(f"Extracted map size: {map_section.size[0]}x{map_section.size[1]}")
print("Pure map visual only - all numbered pins included")
