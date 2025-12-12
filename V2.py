
import shutil
import os

shutil.copy("/content/pylaia-iam/model", "model")
shutil.copy("/content/pylaia-iam/weights.ckpt", "weights.ckpt")
shutil.copy("/content/pylaia-iam/syms.txt", "syms.txt")

print("Done")

from google.colab import files
from PIL import Image

print("Bitte lade deine Bilder hoch:")
uploaded = files.upload()   

target_height = 128
processed_images = []

for filename in uploaded.keys():
    img = Image.open(filename).convert("L") 

  
    factor = target_height / img.height
    new_width = int(img.width * factor)

   
    img = img.resize((new_width, target_height))

   
    new_name = filename.replace(".png", "_fixed.png")
    img.save(new_name)

    processed_images.append(new_name)
    print("Fertig bearbeitet:", new_name)


with open("img_list.txt", "w") as f:
    for name in processed_images:
        f.write(name + "\n")

print("img_list.txt erstellt.")


print("Starte PyLaia...")

!pylaia-htr-decode-ctc \
  --common.experiment_dirname . \
  --common.model_filename model \
  --common.checkpoint weights.ckpt \
  syms.txt \
  img_list.txt

print("Fertig!")
