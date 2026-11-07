import os
from PIL import Image

ROOT = os.path.dirname(__file__)
OUT = os.path.join(ROOT, 'assets', 'hotels')

# Square crops for the hotel card thumbnail. Run once after _fetch_hotel_photos.py.
JOBS = [
    (os.path.join(OUT, 'gracery_shinjuku.jpg'), 'gracery_shinjuku.jpg', (280, 380, 960, 1060)),
    (os.path.join(OUT, 'monterey_kyoto.jpg'), 'monterey_kyoto.jpg', (170, 0, 810, 640)),
    (os.path.join(OUT, 'excel_osaka.jpg'), 'excel_osaka.jpg', (140, 0, 860, 720)),
    (os.path.join(ROOT, 'assets', 'attractions', 'day14', 'aura_tachibana.jpg'), 'aura_tachibana.jpg', (130, 0, 850, 720)),
    (os.path.join(ROOT, 'pictures', 'remm plus ginza hotel tokyo.jpg'), 'remm_plus_ginza.jpg', (300, 0, 983, 683)),
]

for src, name, box in JOBS:
    img = Image.open(src).convert('RGB').crop(box).resize((480, 480), Image.LANCZOS)
    tmp = os.path.join(OUT, name + '.tmp')
    img.save(tmp, 'JPEG', quality=85)
    os.replace(tmp, os.path.join(OUT, name))
    print(name)

for extra in ('monterey_kyoto_entrance.jpg', 'excel_osaka_2.jpg'):
    p = os.path.join(OUT, extra)
    if os.path.exists(p):
        os.remove(p)
