"""Extract text from the Russian Yamato guide PDF for translation."""
from pypdf import PdfReader
from pathlib import Path

src = Path(r"C:\Users\gshenkar\OneDrive - Intel Corporation\VSCode\japan2026\Yamato_Luggage_Transfer_Guide_RU.pdf")
reader = PdfReader(str(src))
for i, page in enumerate(reader.pages, 1):
    print(f"===== PAGE {i} =====")
    print(page.extract_text() or "(no extractable text)")
