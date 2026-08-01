import base64
import os
filepath=r"./files"
def binay_reader(filename):
    imagepath=f"{filepath}/{filename}"
    if filename.split(".")[-1] in ["png","jpg","jpeg"]: 
        with open(imagepath, "rb") as f:
            image_bytes = f.read()
        image_base64=base64.b64encode(image_bytes).decode("utf-8")
        return image_base64
    else:
        return "image is not valid"