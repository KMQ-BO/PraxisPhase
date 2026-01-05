import pandas as pd

df = pd.read_csv("train.csv")

df["text"] = df["text"].str.lower()

with open("train.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        f.write(f"{row['image']} {row['text']}\n")


print("DONE")
