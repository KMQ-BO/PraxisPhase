
import os
from PIL import Image

folder = "Exemplar_1" 
processed_images = []

for filename in os.listdir(folder):
    path = folder + "/" + filename
    img = Image.open(path).convert("L") 

    factor = 128 / img.height
    new_width = int(img.width * factor)
    img = img.resize((new_width, 128))

   
    new_name = filename.replace(".png", "_neu.png")
    img.save(new_name)

    processed_images.append(new_name)
    print("Fertig bearbeitet:", new_name)


with open("img_list.txt", "w") as f:
    for name in processed_images :
        f.write( name + "\n")


print("Fertig!")
