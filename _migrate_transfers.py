import json, os, re, sys

PATH = 'index.html'
APPLY = '--apply' in sys.argv

raw = open(PATH, 'rb').read()
crlf = b'\r\n' in raw
text = open(PATH, encoding='utf-8').read()
lines = text.split('\n')

start = next(i for i, l in enumerate(lines) if l.startswith('const data = {'))
end = next(i for i in range(start + 1, len(lines)) if lines[i].rstrip() == '};')

KEEP = {('23', 'קפה / מנוחה / רחצה'), ('27', 'חזרה למלון / מנוחה')}
EXTRA = {('17', 'חזרה למלון'), ('20', 'Kyoto Station → Nara Station'),
         ('20', 'Nara → Kyoto Station'), ('20', 'חזרה למלון')}

day_re = re.compile(r"^\s*'([\d-]+)'\s*:\s*\{\s*title:")
ev_re = re.compile(r'^\s*(\[".*\]),?\s*$')

def is_transfer(day, ev):
    title, img = ev[1], ev[3]
    if title == '__SECTION__' or (day, title) in KEEP:
        return False
    return (day, title) in EXTRA or img.startswith('assets/transfers/')

out, transfers = [], {}
day, kept_count, last_kept = None, 0, -1
for i, l in enumerate(lines):
    if i == end:
        end_out = len(out)
    if not (start < i < end):
        out.append(l)
        continue
    m = day_re.match(l)
    if m:
        day, kept_count, last_kept, kept_events = m.group(1), 0, -1, []
        out.append(l)
        continue
    m = ev_re.match(l)
    if not (m and day):
        out.append(l)
        continue
    ev = json.loads(m.group(1))
    if is_transfer(day, ev):
        prev_q = None
        if last_kept >= 0:
            prev_q = kept_events[last_kept][4]
        transfers.setdefault(day, []).append({
            't': ev[0], 'title': ev[1], 'desc': ev[2], 'img': ev[3], 'to': ev[4],
            'tag': ev[5] if len(ev) > 5 else '', 'afterIdx': last_kept, 'from': prev_q})
        continue
    out.append(l)
    kept_events.append(ev)
    if ev[1] != '__SECTION__':
        last_kept = kept_count
    kept_count += 1

for d, legs in transfers.items():
    print(f'--- day {d}: {len(legs)} transfers')
    for t in legs:
        print('  ', t['afterIdx'], t['t'].replace('<br>', '-'), '|', t['title'])

block = ['', '// Transport legs between stops (moved out of data[day].events; shown in the transport tab)',
         '// afterIdx = index in data[day].events of the stop the leg follows (-1 = before the first stop)',
         'const transfersByDay = {']
day_keys = list(transfers)
for n, d in enumerate(day_keys):
    block.append(f"  '{d}': [")
    for k, t in enumerate(transfers[d]):
        comma = ',' if k < len(transfers[d]) - 1 else ''
        block.append('    ' + json.dumps(t, ensure_ascii=False) + comma)
    block.append('  ]' + (',' if n < len(day_keys) - 1 else ''))
block.append('};')

final = out[:end_out + 1] + block + out[end_out + 1:]
new_text = '\n'.join(final)
print('total moved:', sum(len(v) for v in transfers.values()))
if APPLY:
    tmp = PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n') as f:
        f.write(new_text)
    back = open(tmp, encoding='utf-8').read()
    assert back == new_text and 'const transfersByDay' in back
    os.replace(tmp, PATH)
    print('written')
