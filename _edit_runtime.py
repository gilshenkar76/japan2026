import os, re

PATH = 'index.html'
raw = open(PATH, 'rb').read()
crlf = b'\r\n' in raw
s = open(PATH, encoding='utf-8').read()

def sub_once(old, new, regex=False):
    global s
    if regex:
        assert len(re.findall(old, s)) == 1, old
        s = re.sub(old, lambda m: new.replace('\\1', m.group(1)) if '\\1' in new else new, s)
    else:
        assert s.count(old) == 1, old
        s = s.replace(old, new)

css = """
    .transfer-chip{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;justify-self:center;max-width:100%;margin:0;padding:6px 14px;border:1px dashed #94a3b8;border-radius:999px;background:#f8fafc;color:#475569;font-size:12px;font-weight:700;cursor:pointer}
    .transfer-chip .tc-time{color:#e53935;font-weight:900}
    .tleg{display:flex;gap:12px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px;box-shadow:var(--shadow);margin-top:10px}
    .tleg img{width:84px;height:84px;object-fit:cover;border-radius:12px;flex:0 0 auto}
    .tleg-body{min-width:0;flex:1}
    .tleg-time{font-size:12px;font-weight:900;color:#e53935}
    .tleg-title{font-weight:800;font-size:14px;color:#1e293b;margin:2px 0}
    .tleg-route{font-size:12px;color:var(--muted);direction:ltr;text-align:right;margin-bottom:4px}
    .tleg-desc{font-size:12px;color:var(--muted);white-space:pre-line}"""
sub_once(r'(\n    \.transit-meta span\{[^\n]*\})', '\\1' + css, regex=True)

sub_once('<div class="upload-panel hidden" id="transportTransitPanel"></div>',
         '<div class="upload-panel hidden" id="transportLegsPanel"></div>\n\n      <div class="upload-panel hidden" id="transportTransitPanel"></div>')

sub_once("  data[day].events.forEach(e=>{\n",
         "  tl.innerHTML += transferChipsHtml(day, -1);\n  data[day].events.forEach((e, idx)=>{\n")
sub_once("""        ${audioMap[e[1]] ? apPlayerHtml(e[1]) : ''}
      </div>
    </div></div>`;
  });
""", """        ${audioMap[e[1]] ? apPlayerHtml(e[1]) : ''}
      </div>
    </div></div>`;
    tl.innerHTML += transferChipsHtml(day, idx);
  });
""")

sub_once("isGuideDay ? 'openNavGuide()' : ", "")

sub_once("  // Public-transport legs for this day (shown here in the",
         "  renderTransferLegs(day);\n  // Public-transport legs for this day (shown here in the")

js = r"""function transferInfo(t){
  const hint = t.tag || (t.title + ' ' + t.desc);
  const transit = /🚆|🚄|🚈|🚂|🚇|🚌|רכבת|שינקנסן|אוטובוס/.test(hint);
  const taxi = /🚕|🚖|🚐|מונית|שאטל|מיניוואן/.test(hint);
  const walk = /🚶|הליכה|רגלי/.test(hint);
  if (transit) return { icon: '🚆', travel: 'transit' };
  if (taxi) return { icon: '🚕', travel: 'driving' };
  if (walk) return { icon: '🚶', travel: 'walking' };
  return { icon: '🚌', travel: 'transit' };
}

function transferDirectionsUrl(t){
  const origin = t.from ? `&origin=${encodeURIComponent(t.from)}` : '';
  return `https://www.google.com/maps/dir/?api=1${origin}&destination=${encodeURIComponent(t.to)}&travelmode=${transferInfo(t).travel}`;
}

// Compact link shown in the route tab between two stops
function transferChipsHtml(day, idx){
  return (transfersByDay[day] || []).filter(t => t.afterIdx === idx).map(t => {
    const time = t.t.replace('<br>', ' – ');
    const label = t.tag || `${transferInfo(t).icon} ${t.title}`;
    return `<div class="transfer-chip" onclick="showTransportationDetails('${day}')"><span class="tc-time">${time}</span><span>${label}</span></div>`;
  }).join('');
}

function renderTransferLegs(day){
  const panel = document.getElementById('transportLegsPanel');
  if (!panel) return;
  const legs = transfersByDay[day] || [];
  const guideBtn = day === '14'
    ? '<div class="actions" style="margin-top:10px"><button class="btn primary" type="button" onclick="openNavGuide()">📖 מדריך ניווט מלא · 18 שלבים</button></div>'
    : '';
  if (!legs.length && !guideBtn) {
    panel.innerHTML = '';
    panel.classList.add('hidden');
    return;
  }
  panel.innerHTML = '<div class="section-title" style="margin:0;font-size:18px">מעברים בין האטרקציות</div>' + guideBtn + legs.map(t => {
    const route = t.from ? `${t.from} → ${t.to}` : `→ ${t.to}`;
    return `<div class="tleg">
      <img src="${t.img}" alt="" loading="lazy">
      <div class="tleg-body">
        <div class="tleg-time">${t.t.replace('<br>', ' – ')}</div>
        <div class="tleg-title">${t.title}</div>
        <div class="tleg-route">${route}</div>
        <div class="tleg-desc">${t.desc}</div>
        <div class="transit-meta" style="margin-top:6px">${t.tag ? `<span>${t.tag}</span>` : ''}<a class="btn ghost" style="padding:3px 12px;font-size:12px" target="_blank" rel="noopener" href="${transferDirectionsUrl(t)}">🧭 ניווט</a></div>
      </div>
    </div>`;
  }).join('');
  panel.classList.remove('hidden');
}

"""
sub_once("function backToTransportation(){", js + "function backToTransportation(){")

new_text = s
tmp = PATH + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n') as f:
    f.write(new_text)
assert open(tmp, encoding='utf-8').read() == new_text
os.replace(tmp, PATH)
print('written')
