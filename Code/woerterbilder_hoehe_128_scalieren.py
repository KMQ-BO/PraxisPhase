import os, glob
import cv2

INPUT_DIR = "words_7*"           
OUTPUT_DIR = "words_7"
os.makedirs(OUTPUT_DIR, exist_ok=True)
TARGET_H = 128

exts = ("*.png","*.jpg")
paths = []

for e in exts:
    paths += glob.glob(os.path.join(INPUT_DIR, e))

for src in paths:
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    
    h, w = img.shape[:2]

    scale = TARGET_H / float(h)
    new_w = max(1, int(round(w * scale)))

    if scale < 1.0:
        interp = cv2.INTER_AREA 
    else : 
        interp = cv2.INTER_CUBIC
        
    out = cv2.resize(img, (new_w, TARGET_H), interpolation=interp)

    rel = os.path.relpath(src, INPUT_DIR)
    dst = os.path.join(OUTPUT_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    cv2.imwrite(dst, out)

print("DONE")
