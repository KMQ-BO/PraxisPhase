INPUT = "train.txt"          
OUTPUT = "train_ids.txt"   

written = 0

with open(INPUT, "r", encoding="utf-8") as f_in, \
     open(OUTPUT, "w", encoding="utf-8") as f_out:
          
     # Jede Zeile aus train.txt durchgehen
    for line in f_in:
        line = line.strip()
        if not line:
            continue

        img_path = line.split(maxsplit=1)[0] # Erstes Wort nehmen
       
        if img_path.endswith(".png"):
            img_path = img_path[:-4]     # ".png" entfernen

        f_out.write(img_path + "\n")
        written += 1

print("Done")

