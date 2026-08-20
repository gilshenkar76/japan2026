import base64, pathlib, re

mp3 = pathlib.Path('assets/audio/chureito_ru.mp3').read_bytes()
b64 = base64.b64encode(mp3).decode()
data_uri = 'data:audio/mpeg;base64,' + b64

html = pathlib.Path('_audio_player.html').read_text(encoding='utf-8')
html2 = re.sub(r'src="[^"]*chureito[^"]*"', f'src="{data_uri}"', html)

if html2 == html:
    print('WARNING: pattern not matched, injecting fresh file')
    fresh = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Pagoda Chureito – Audio Guide</title>
<style>
  body {{ margin:0; background:#0d0d1a; display:flex; justify-content:center;
         align-items:center; min-height:100vh; font-family:Segoe UI,Arial,sans-serif; }}
  .card {{ background:white; border-radius:18px; padding:32px 36px; max-width:500px;
           width:90%; box-shadow:0 8px 40px rgba(0,0,0,.5); text-align:center; }}
  h1 {{ font-size:1.4rem; color:#1a237e; margin:0 0 4px; }}
  .sub {{ font-size:.85rem; color:#888; margin-bottom:24px; }}
  audio {{ width:100%; border-radius:8px; margin-bottom:20px; }}
</style>
</head>
<body>
<div class="card">
  <div style="font-size:3rem">&#x26E9;&#xFE0F;</div>
  <h1>&#x41F;&#x430;&#x433;&#x43E;&#x434;&#x430; &#x427;&#x443;&#x440;&#x435;&#x439;&#x442;&#x43E;</h1>
  <p class="sub">&#x410;&#x443;&#x434;&#x438;&#x43E;&#x433;&#x438;&#x434; &#x43D;&#x430; &#x440;&#x443;&#x441;&#x441;&#x43A;&#x43E;&#x43C; &#x44F;&#x437;&#x44B;&#x43A;&#x435; &middot; ~3 &#x43C;&#x438;&#x43D;&#x443;&#x442;&#x44B;</p>
  <audio controls src="{data_uri}"></audio>
</div>
</body>
</html>"""
    pathlib.Path('_audio_player.html').write_text(fresh, encoding='utf-8')
else:
    pathlib.Path('_audio_player.html').write_text(html2, encoding='utf-8')

size = round(pathlib.Path('_audio_player.html').stat().st_size / 1024)
print(f'Saved _audio_player.html  {size} KB')
