import re

INPUT = "train.txt"         
OUTPUT = "train_test.txt"

SPACE_TOKEN = "<space>"

REMOVE_PUNCT = True
punct_re = re.compile(r"[.,;:!?\"()\[\]{}]")

def tokenize_text(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    s = s.lower()

    if REMOVE_PUNCT:
        s = punct_re.sub("", s)

    out = []
    for wi, word in enumerate(s.split(" ")):
        if wi > 0:
            out.append(SPACE_TOKEN)
        out.extend(list(word))
    return " ".join(out)

bad = 0
written = 0

with open(INPUT, "r", encoding="utf-8") as f_in, \
     open(OUTPUT, "w", encoding="utf-8") as f_out:

    for line in f_in:
        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            bad += 1
            continue

        img_path, txt = parts[0], parts[1]


        if img_path.endswith(".png"):
            img_path = img_path[:-4]

        txt = txt.strip()
        if not txt:
            bad += 1
            continue

        tok = tokenize_text(txt)
        f_out.write(f"{img_path} {tok}\n")
        written += 1

print("written:", written, "bad/skipped:", bad)
print("output file:", OUTPUT)
