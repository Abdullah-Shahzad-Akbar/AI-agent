import os
from pathlib import Path
import shutil

def check_file(file):
    Path("files").mkdir(exist_ok=True)
    path=r"./files"
    filesname=os.listdir(path)
    if file.filename in filesname:
        return file.filename
    else:
        save_path = Path("files") / file.filename
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file.filename
        