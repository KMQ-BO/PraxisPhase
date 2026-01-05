
- Dieses Projekt hilft dabei, Trainingsdaten für ein Modell  vorzubereiten.
  
  
- Was das Projekt macht:

1) Schneidet aus Seitenbildern Textzeilen heraus und speichert sie als PNG.

2) Skaliert alle Wortbilder auf eine einheitliche Höhe von 128 px.

3) Erstellt aus einer Referenz-Datei (referenzdaten.xlsx) Trainingsdateien:

   1- train.csv (Bildpfad + Text)

   2- train.txt

   3- train_ids.txt (nur Bild-IDs ohne Endung)

   4- train_test.txt (tokenisierte Zeichenfolge mit <space>)
   

- Voraussetzungen:

1) Python (Version bis 3.10)

2) Bibliotheken: opencv-python, numpy, pandas, openpyxl (für Excel-Import)

  - Installation der erforderlichen Bibliotheken: pip install opencv-python numpy pandas openpyxl


- Pipeline: Schritt für Schritt
    1) Wortbilder aus Seiten schneiden (Datein -> pdf_bilder_konverter.py, seite_vertikal_teilen.py, woerter_aus_seiten_extrahieren.py)
      Diese Scripte laden Seitenbilder und schneiden Bereiche zwischen erkannten Linien aus.
      Ergebnis: PNGs in einem Ordner wie words/ mit Namen word_0001.png, word_0002.png, …

    2) Alle Wortbilder auf eine Höhe bringen (Datei -> woerterbilder_hoehe_128_scalieren.py) 
      Dieses Script nimmt Bilder aus einem Eingabeordner  und skaliert auf eine feste Höhe (TARGET_H = 128).
      Die Breite wird angepasst.
    
    3) train.csv aus Referenzdaten + Ordnern erstellen (Datei-> trainings_csv_erstellen.py):
        Liest referenzdaten.xlsx, Erstellt Zeilen für mehrere Bildordner und Schreibt train.csv
    
    4) csv_zu_trainings_txt.py :
        Liest train.csv , train.txt erstellen
 
    5) train_ids_generieren.py:
        Liest train.txt, Schreibt nur den Bildpfad ohne .png in train_ids.txt
    
        Praktisch, wenn man nur IDs braucht .
    
    6) train_txt_tokenizer.py:
        Liest train.txt, Tokenisiert auf Zeichenebene und nutzt <space> zwischen Wörtern
        
        
    
