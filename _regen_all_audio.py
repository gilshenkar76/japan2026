"""Regenerate all 3 MP3s using Microsoft Edge TTS – Dmitry Neural voice."""
import asyncio, edge_tts, pathlib, re

VOICE = "ru-RU-DmitryNeural"

def extract_text(py_file):
    src = pathlib.Path(py_file).read_text(encoding="utf-8")
    m = re.search(r'(?:text|text_ru)\s*=\s*"""(.*?)"""', src, re.DOTALL)
    return m.group(1).strip() if m else None

chureito_text = extract_text("_gen_chureito_audio.py")
kawaguchi_text = extract_text("_gen_kawaguchi_audio.py")

oshino_text = """
Добро пожаловать в Осино Хаккай — деревню восьми источников у подножия горы Фудзи.

Название переводится просто: «восемь морей Осино».
Восемь кристально чистых прудов, питаемых талыми водами Фудзи.
Вода здесь фильтруется через вулканические породы на протяжении более восьмидесяти лет,
прежде чем выйти на поверхность. Поэтому она настолько прозрачная,
что видно дно даже на глубине нескольких метров.

Осино Хаккай — это не просто природная достопримечательность.
Это место, которое японцы считают священным.
Источники связаны с синтоистскими традициями и верой в то,
что вода несёт в себе жизненную силу.

Обратите внимание на традиционные соломенные крыши домов вокруг.
Такой стиль называется гассё-дзукури.
Он характерен для старых японских горных деревень.
Эти дома сохранились здесь как напоминание о том,
как выглядела Япония несколько веков назад.

Если повезёт с погодой, над деревней будет видна гора Фудзи.
Её отражение в прозрачных прудах — один из самых узнаваемых видов района Кавагути.

Местные торговцы предлагают традиционные закуски и сувениры.
Попробуйте местный тофу или кириданго — рисовые шарики на шпажке.
Это несложная, но очень японская еда.

Осино Хаккай напоминает о том, что в Японии природа и культура неотделимы друг от друга.
Каждый камень, каждый источник, каждое дерево здесь несёт в себе историю.

Наслаждайтесь этим тихим и красивым местом.
"""

JOBS = [
    ("mp3/Chureito Pagoda.mp3",  chureito_text),
    ("mp3/Oshino Hakkai.mp3",    oshino_text.strip()),
    ("mp3/Lake Kawaguchi.mp3",   kawaguchi_text),
]

async def generate(path, text):
    comm = edge_tts.Communicate(text, VOICE)
    await comm.save(path)
    mb = round(pathlib.Path(path).stat().st_size / 1024 / 1024, 1)
    print(f"  ✓  {path}  ({mb} MB)")

async def main():
    await asyncio.gather(*[generate(p, t) for p, t in JOBS if t])

print(f"Generating with voice: {VOICE}")
asyncio.run(main())
print("All done.")
