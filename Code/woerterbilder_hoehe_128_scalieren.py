import os, glob
import cv2

INPUT_DIR = "words_7*"           
OUTPUT_DIR = "words_7"
os.makedirs(OUTPUT_DIR, exist_ok=True)
TARGET_H = 128

exts = ("*.png","*.jpg","*.jpeg","*.tif","*.tiff","*.bmp","*.webp")
paths = []
for e in exts:
    paths += glob.glob(os.path.join(INPUT_DIR, "**", e), recursive=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)

for src in paths:
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue
    
    h, w = img.shape[:2]

    scale = TARGET_H / float(h)
    new_w = max(1, int(round(w * scale)))

    interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
    out = cv2.resize(img, (new_w, TARGET_H), interpolation=interp)

    rel = os.path.relpath(src, INPUT_DIR)
    dst = os.path.join(OUTPUT_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    cv2.imwrite(dst, out)

print("DONE")
