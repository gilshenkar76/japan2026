import os, urllib.request, time

OUT = os.path.join(os.path.dirname(__file__), 'assets', 'hotels')
os.makedirs(OUT, exist_ok=True)

BASE = 'https://upload.wikimedia.org/wikipedia/commons/thumb/'
FILES = {
    'gracery_shinjuku.jpg': '4/4c/Hotel_Gracery_in_Shinjuku%2C_Tokyo%2C_2019_-_015.jpg/960px-Hotel_Gracery_in_Shinjuku%2C_Tokyo%2C_2019_-_015.jpg',
    'monterey_kyoto.jpg': '3/38/Hotel_Monterey_Kyoto_20130202-001.jpg/960px-Hotel_Monterey_Kyoto_20130202-001.jpg',
    'monterey_kyoto_entrance.jpg': 'a/a4/Hotel_Monterey_Kyoto_1F_entrance_20130201-001.jpg/960px-Hotel_Monterey_Kyoto_1F_entrance_20130201-001.jpg',
    'excel_osaka.jpg': '3/32/Osaka_Excel_Hotel_Tokyu.jpg/960px-Osaka_Excel_Hotel_Tokyu.jpg',
    'excel_osaka_2.jpg': 'a/a5/OSAKA_EXCEL_HOTEL_TOKYU.jpg/960px-OSAKA_EXCEL_HOTEL_TOKYU.jpg',
}

for name, path in FILES.items():
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'japan2026-trip-app/1.0 (personal)'})
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
            break
        except Exception as e:
            print(name, 'retry', e)
            time.sleep(5 * (attempt + 1))
    else:
        continue
    with open(os.path.join(OUT, name), 'wb') as f:
        f.write(data)
    print(name, len(data))
    time.sleep(2)
