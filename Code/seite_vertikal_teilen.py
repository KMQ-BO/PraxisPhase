import cv2
import os

os.makedirs("R_H_4", exist_ok=True)
# Seiten  durchgehen
for i in range(1, 25):
    img = cv2.imread(f"pages_4/page_{i:03}.png")

    handwritten = img[:, 1300:2400] # alle Zeilen, nur Spalten 1300 bis 2399
    cv2.imwrite(f"R_H_4/page_{i:03}_hw.png", handwritten)

print("DONE")
