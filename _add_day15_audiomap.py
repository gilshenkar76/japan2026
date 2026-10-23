import pathlib, re
p = pathlib.Path("index.html")
s = p.read_text(encoding="utf-8")
m = re.search(r"const audioMap = \{.*?\n\};", s, re.DOTALL)
block = m.group(0)
new_entries = [
    "  'Heiwa no Torii (\u05e9\u05e2\u05e8 \u05d4\u05e9\u05dc\u05d5\u05dd)': 'mp3/Heiwa no Torii.mp3',",
    "  'Owakudani': 'mp3/Owakudani.mp3',",
    "  'Hakone Open-Air Museum': 'mp3/Hakone Open-Air Museum.mp3',",
]
missing = [e for e in new_entries if e.split(":")[0].strip() not in block]
if not missing:
    print("already present")
else:
    new_block = block[:-2] + "\n".join(missing) + "\n};"
    s2 = s[:m.start()] + new_block + s[m.end():]
    p.write_text(s2, encoding="utf-8")
    print("updated:", len(missing))
