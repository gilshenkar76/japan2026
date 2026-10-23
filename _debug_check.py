import pathlib
s = pathlib.Path("index.html").read_text(encoding="utf-8")
i = s.find("Shinjuku Gyoen National Garden")
print(repr(s[i-260:i+40]))
print("---")
j = s.find("audioMap = {")
print(repr(s[j:j+400]))
