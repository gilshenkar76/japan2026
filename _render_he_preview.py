import pypdfium2 as pdfium
from pathlib import Path
src = Path(r"C:\Users\gshenkar\OneDrive - Intel Corporation\VSCode\japan2026\Yamato_Luggage_Transfer_Guide_HE.pdf")
out_dir = Path(r"C:\Users\gshenkar\OneDrive - Intel Corporation\VSCode\japan2026\assets\_he_preview")
out_dir.mkdir(parents=True, exist_ok=True)
pdf = pdfium.PdfDocument(str(src))
for i, page in enumerate(pdf, 1):
    img = page.render(scale=2).to_pil()
    p = out_dir / f"page{i}.png"
    img.save(p)
    print(p)
