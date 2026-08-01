import fitz
import os
from pathlib import Path
def Pdf_to_text(filename:str):
    Path("text_of_pdf").mkdir(exist_ok=True)   
    text_output=f"./text_of_pdf/{filename}_output.txt"
    if os.path.exists(text_output):
        return False
    else:
        try:
            path=f"./files/{filename}"
            doc = fitz.open(path)
            with open(text_output, "w", encoding="utf-8") as f:
                for page_num,page in enumerate(doc,start=1):
                    f.write(f"====Page {page_num}====\n")
                    f.write(page.get_text())
            doc.close()
            return True
        except Exception as e:
            return "File not found"

