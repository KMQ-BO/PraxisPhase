import pandas as pd

df = pd.read_csv("train.csv")

df["text"] = df["text"].str.capitalize()
#Textdatei erstellen und jede Zeile speichern
with open("train.txt", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():  # Tabelle_Zeilen durchgehen
        f.write(f"{row['image']} {row['text']}\n")


print("DONE")
