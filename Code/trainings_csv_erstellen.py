import pandas as pd
import os

df = pd.read_excel("referenzdaten.xlsx")
df = df.rename(columns={"Text": "text"})

folders = ["words","words_2","words_3","words_4","words_5","words_6","words_7"]

rows = []

for i, text in enumerate(df["text"], start=1):
    image_name = f"word_{i:04}"


    for folder in folders:
        rows.append({
            "image": f"{folder}/{image_name}",
            "text": text
        })

final_df = pd.DataFrame(rows)
final_df.to_csv("train.csv", index=False, encoding="utf-8-sig")

print("Done")
