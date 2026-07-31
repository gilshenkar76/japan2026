from pypdf import PdfReader
r = PdfReader(r"C:\Users\gshenkar\OneDrive - Intel Corporation\VSCode\japan2026\Yamato_Luggage_Transfer_Guide_HE.pdf")
for i, p in enumerate(r.pages, 1):
    print(f"----- PAGE {i} -----")
    print(p.extract_text())
