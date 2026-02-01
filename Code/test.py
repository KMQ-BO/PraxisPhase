from pathlib import Path                 # Sauberes Arbeiten mit Pfaden/Ordnern
from PIL import Image                   # Bilder öffnen/konvertieren/skalieren

from laia.scripts.htr.decode_ctc import run as decode_ctc  # CTC-Decoding: macht aus Bildern Text (Inference)
import laia.common.arguments as args     # Laia-Parameterklassen (CommonArgs, DataArgs, DecodeArgs, ...)

def main():
    input_folder = Path("31")           # Ordner mit den Originalbildern (Input)
    out_folder = Path("31_processed")   # Ordner für vorbereitete/normalisierte Bilder (Output)
    img_list = Path("img_list.txt")     # Datei mit Bild-IDs, die Laia decodieren soll

    syms = "syms_de.txt"                # Alphabet/Zeichenliste (muss zum trainierten Modell passen)
    model_filename = "model_de"         # Modellname/Datei-Prefix (Architekturdefinition)
    checkpoint = "epoch=9-lowest_va_cer-v2.ckpt"  # Trainierte Gewichte (Checkpoint) für die Vorhersage

    lm_path = "LM_de.gz"                # Pfad zum Language Model (z. B. KenLM)
    tokens_path = "tokens.txt"          # Tokenliste für LM (Mapping der Zeichen/Token)
    lexicon_path = "lexicon_gt.txt"     # Lexikon/Wortliste zur Einschränkung/Verbesserung des Decodings

    # --- Bilder vorbereiten (Normierung für das Modell) ---
    out_folder.mkdir(exist_ok=True)     # Output-Ordner anlegen, falls er fehlt

    ids = []                            # Liste der Bild-IDs (ohne Endung), die in img_list.txt geschrieben werden
    for file in sorted(input_folder.iterdir()):  # Alle Dateien im Input-Ordner durchgehen (sortiert)
        if file.suffix.lower() not in [".png", ".jpg"]:  # Nur PNG/JPG verarbeiten
            continue

        img = Image.open(file).convert("L")      # Bild öffnen und in Graustufen umwandeln ("L")
        factor = 128 / img.height               # Skalierungsfaktor: Höhe auf 128 px bringen
        new_w = int(img.width * factor)         # Neue Breite proportional anpassen (Seitenverhältnis bleibt)
        img = img.resize((new_w, 128))          # Bild auf (neue Breite, 128) skalieren

        new_id = file.stem + "_neu"             # Neue Bild-ID (stem = Dateiname ohne Endung)
        out_path = out_folder / (new_id + ".png")  # Zielpfad im Output-Ordner
        img.save(out_path)                      # Normalisiertes Bild speichern

        ids.append(new_id)                      # ID speichern (Laia erwartet IDs ohne Endung)
        print("Bearbeitet:", out_path)          # Statusausgabe

    # Liste der zu decodierenden Bilder schreiben (eine ID pro Zeile)
    with open(img_list, "w", encoding="utf-8") as f:
        for i in ids:
            f.write(i + "\n")

    print("Starte PyLaia...")                   # Startmeldung

    # --- Decoding / Inference: Bilder -> Text ---
    decode_ctc(
        syms=syms,                              # Alphabet/Zeichenliste
        img_dirs=[str(out_folder)],             # Ordner mit den vorbereiteten Bildern
        img_list=str(img_list),                 # Datei mit Bild-IDs (welche Dateien decodiert werden)

        common=args.CommonArgs(
            train_path=".",                     # Basisordner (hier aktuelles Verzeichnis)
            experiment_dirname=".",             # Experiment-Ordner (hier ebenfalls aktuelles Verzeichnis)
            model_filename=model_filename,      # Modell-Definition/Name
            checkpoint=checkpoint,              # Welche Gewichte geladen werden sollen
        ),

        data=args.DataArgs(
            batch_size=8,                       # Wie viele Bilder pro Batch decodiert werden
            color_mode="L",                     # Graustufen-Modus (muss zu convert("L") passen)
            reading_order="LTR",                # Leserichtung: Left-to-Right
           #num_workers=0,                      # Datenlade-Worker (0 = stabil auf macOS)
        ),

        trainer=args.TrainerArgs(
            gpus=1,                             # GPU-Decoding 
        ),

        decode=args.DecodeArgs(
            use_language_model=True,            # LM in Beam Search aktivieren
            language_model_path=lm_path,        # LM-Datei
            language_model_weight=0.8,          # Einfluss des LM (höher = stärkerer LM-Einfluss)
            tokens_path=tokens_path,            # Tokens/Alphabet fürs LM
            lexicon_path=lexicon_path,          # Lexikon für erlaubte Wörter (optional, je nach Setup)

            convert_spaces=True,                # Behandelt spezielle Space-Tokens -> echte Leerzeichen
            input_space="<space>",              # Token, das im Modell als Leerzeichen gilt
            output_space=" ",                   # Ausgabezeichen für Leerzeichen
            join_string="",                     # Verbindet Tokens ohne Extra-Zeichen (normal für Text)
        ),
    )
    print("Fertig!")                            # Abschlussmeldung
if __name__ == "__main__":                      # Startpunkt, wenn Skript direkt ausgeführt wird
    main()
