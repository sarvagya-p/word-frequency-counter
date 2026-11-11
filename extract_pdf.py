from pypdf import PdfReader

# The file name
reader = PdfReader("sample.pdf") 
all_text = ""

for page in reader.pages:
    txt = page.extract_text()
    if txt:
        all_text += txt + "\n\n"

with open("output2.txt", "w", encoding="utf-8") as f:
    f.write(all_text)