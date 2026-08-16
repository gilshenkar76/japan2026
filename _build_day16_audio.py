"""Build _day16_audio.html – day 16 schedule with embedded MP3 players."""
import base64, pathlib

def b64src(path):
    data = pathlib.Path(path).read_bytes()
    return 'data:audio/mpeg;base64,' + base64.b64encode(data).decode()

chureito_src = b64src('mp3/Chureito Pagoda.mp3')
oshino_src   = b64src('mp3/Oshino Hakkai.mp3')

# rows: (time, icon, name, description, audio_src or None)
rows = [
    ("09:00–10:00", "⛩️", "Chureito Pagoda",
     "עלייה לנקודת התצפית עם מבט להר פוג'י – אחד הנופים המצולמים ביותר ביפן",
     chureito_src),
    ("10:30–12:00", "💧", "Oshino Hakkai",
     "כפר מסורתי עם שמונה בריכות מי שלגים צלולות ואווירת פוג'י כפרית",
     oshino_src),
    ("12:15–13:15", "🍂", "Lake Kawaguchi – מסדרון המייפל",
     "הליכה לאורך מסדרון המייפל עם צבעי שלכת ונקודות מבט לאגם",
     None),
    ("13:15–14:15", "🍜", "ארוחת צהריים – Kawaguchiko",
     "הוטו / אודון / סובה מקומי לפני הנסיעה לנגויה",
     None),
    ("14:30–16:20", "🚄", "נסיעה לנגויה",
     "אוטובוס → Mishima → שינקנסן Hikari → Nagoya",
     None),
    ("16:30–17:00", "🏨", "צ'ק-אין – Nagoya JR Gate Tower Hotel",
     "מלון צמוד לתחנת JR המרכזית",
     None),
    ("17:30–22:00", "🌃", "ערב חופשי – Sakae",
     "רחובות מוארים, קניות, מסעדות ואווירת ערב עירונית בנגויה",
     None),
]

def audio_cell(src):
    if src is None:
        return '<td class="td-audio"></td>'
    return f'''<td class="td-audio">
      <audio controls preload="none" src="{src}"></audio>
    </td>'''

row_html = ''
for time, icon, name, desc, src in rows:
    row_html += f'''
    <tr>
      <td class="td-time">{time}</td>
      <td class="td-icon">{icon}</td>
      <td class="td-name">{name}</td>
      <td class="td-desc">{desc}</td>
      {audio_cell(src)}
    </tr>'''

html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>יום 16.11 – פוג'י → נגויה</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#0d0d1a; font-family:'Segoe UI',Arial,sans-serif;
          padding:24px 14px; min-height:100vh; }}
  .card {{ max-width:900px; margin:0 auto; background:white;
           border-radius:18px; overflow:hidden;
           box-shadow:0 8px 40px rgba(0,0,0,.5); }}
  .card-header {{ background:linear-gradient(135deg,#1b5e20,#2e7d32);
                  color:white; padding:16px 24px; }}
  .card-header h1 {{ font-size:1.2rem; margin-bottom:3px; }}
  .card-header p  {{ font-size:.75rem; opacity:.75; }}

  table {{ width:100%; border-collapse:collapse; }}
  thead tr {{ background:#e8f5e9; }}
  thead th {{ padding:10px 14px; font-size:.78rem; font-weight:700;
              color:#2e7d32; text-align:right; border-bottom:2px solid #c8e6c9;
              white-space:nowrap; }}
  tbody tr {{ border-bottom:1px solid #f0f0f0; }}
  tbody tr:hover {{ background:#f1f8e9; }}
  td {{ padding:10px 14px; vertical-align:middle; font-size:.88rem; }}

  .td-time {{ white-space:nowrap; font-weight:700; color:#37474f;
              font-size:.82rem; min-width:105px; }}
  .td-icon {{ font-size:1.3rem; text-align:center; width:38px; padding:0 4px; }}
  .td-name {{ font-weight:600; color:#1b5e20; }}
  .td-desc {{ font-size:.82rem; color:#555; line-height:1.45; }}

  /* audio player cell */
  .td-audio {{ width:260px; padding:6px 10px; }}
  .td-audio audio {{ width:100%; height:36px; border-radius:8px; }}
  .td-audio:empty::after {{
    content:'—'; color:#ccc; font-size:.8rem;
  }}

  /* highlight rows with audio */
  tr:has(.td-audio audio) {{ background:#f9fbe7; }}
  tr:has(.td-audio audio):hover {{ background:#f0f4e3; }}

  tfoot td {{ padding:10px 14px; font-size:.78rem; color:#888;
              background:#f9f9f9; border-top:2px solid #e0e0e0; }}
</style>
</head>
<body>
<div class="card">
  <div class="card-header">
    <h1>&#x1F5FB; יום 16 נובמבר – פוג'י &#x2192; נגויה</h1>
    <p>Chureito Pagoda · Oshino Hakkai · Kawaguchiko · Nagoya JR Gate Tower</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>שעות</th><th></th><th>עצירה</th><th>תיאור</th>
        <th>&#x1F3B5; אודיו</th>
      </tr>
    </thead>
    <tbody>{row_html}
    </tbody>
    <tfoot>
      <tr>
        <td colspan="5">
          &#x1F4CD; 2 קבצי אודיו מחוברים · לחץ ▶ להאזנה
          &nbsp;|&nbsp;
          &#x1F3B5; שאר האטרקציות – ניתן להוסיף קבצים בהמשך
        </td>
      </tr>
    </tfoot>
  </table>
</div>
</body>
</html>"""

out = pathlib.Path('_day16_audio.html')
out.write_text(html, encoding='utf-8')
print(f'Saved {out}  ({round(out.stat().st_size/1024)} KB)')
