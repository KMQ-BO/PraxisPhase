import cv2
import numpy as np
import os

os.makedirs("words_4", exist_ok=True)

word_count = 0

for page in range(1, 25):
    img = cv2.imread(f"R_H_4/page_{page:03}_hw.png", 0)

    _, bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (img.shape[1], 2))
    h_lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

    ys = np.where(h_lines.sum(axis=1) > 0)[0]

    splits = np.where(np.diff(ys) > 2)[0] + 1
    groups = np.split(ys, splits)
    line_pos = [int(g.mean()) for g in groups]

    for i in range(len(line_pos) - 1):
        y1, y2 = line_pos[i], line_pos[i + 1]
        piece = img[y1:y2, :]

        if piece.shape[0] > 40:
            word_count += 1
            out = f"test_horizontal/word_{word_count:04}.png"
            cv2.imwrite(out, piece)

print("DONE")
