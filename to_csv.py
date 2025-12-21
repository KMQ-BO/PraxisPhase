import pandas as pd
import os

df = pd.read_excel("gt.xlsx")
df = df.rename(columns={"Text": "text"})

folders = ["words", "words_2", "words_3", "words_4"]

rows = []

for i, text in enumerate(df["text"], start=1):
    image_name = f"word_{i:04}.png"


    for folder in folders:
        rows.append({
            "image": f"{folder}/{image_name}",
            "text": text
        })

final_df = pd.DataFrame(rows)
final_df.to_csv("labels_all.csv", index=False, encoding="utf-8-sig")

print("Done")
