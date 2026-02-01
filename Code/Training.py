from pathlib import Path  # Pfad-Handling (Ordner erstellen, Dateien referenzieren)

from laia.scripts.htr.create_model import run as create_model  # Erstellt die Modell-Architektur (CRNN) basierend auf dem Alphabet
from laia.scripts.htr.train_ctc import run as train_ctc        # Trainiert das Modell mit CTC-Loss (HTR ohne Zeichen-Alignment)
import laia.common.arguments as args                           # Parameter-Container (CommonArgs, TrainArgs, ...)

SYMS_DE = "dataset/syms_de.txt"          # Alphabet/Zeichenliste: definiert, welche Zeichen das Modell ausgeben darf
EXP_DIR = "./experiments"               # Basisordner für Experimente (Logs, Modelle, Checkpoints)
MODEL_FILENAME = "experiment/model/model"  # Zielpfad/Prefix für die Modell-Dateien (relativ zu train_path)
IMG_DIRS = ["dataset"]         # Ordner mit den Trainingsbildern
TR_TXT   = "dataset/train.txt" # Liste: Bildpfad + Transkription (Train)
VA_TXT   = "dataset/val.txt"   # Liste: Bildpfad + Transkription (Validation)

Path(EXP_DIR).mkdir(exist_ok=True)  # Erstellt EXP_DIR falls nicht vorhanden

create_model(
    SYMS_DE,                              # Liest das Alphabet ein -> bestimmt Output-Klassen des CTC-Modells
    fixed_input_height=128,               # Normiert alle Inputbilder auf Höhe 128 px (Breite bleibt variabel)
    common=args.CommonArgs(
        train_path=EXP_DIR,               # Root-Verzeichnis, in dem Laia Dateien ablegt
        model_filename=MODEL_FILENAME,    # Wo die Modellbeschreibung/Dateien gespeichert werden
    ),
    crnn=args.CreateCRNNArgs(
        cnn_num_features=[12, 24, 48, 48],        # CNN-Filter pro Block (Modellkapazität)
        cnn_batchnorm=[True, True, True, True],   # BatchNorm pro CNN-Block (stabileres Training)
    ),
)

def main():
    train_ctc(
        SYMS_DE,                   # Alphabet/Zeichenliste (muss zum Modell/Checkpoint passen)
        IMG_DIRS,                  # Bildordner
        TR_TXT,                    # Trainings-Labels
        VA_TXT,                    # Validierungs-Labels
        common=args.CommonArgs(
            train_path=EXP_DIR,                # Root für alle Outputs
            experiment_dirname="experiment",   # Unterordnername des Experiments
            checkpoint="epoch=99-lowest_va_cer.ckpt",         # Lädt alte Gewichte und trainiert weiter (Resume/Fine-Tuning)
            model_filename=MODEL_FILENAME,     # Modellpfad/Prefix (Architekturdatei)
        ),
        train=args.TrainArgs(
            pretrain=True,                # Start nicht "komplett neu" (hier praktisch: Training auf Basis geladener Gewichte)
            freeze_layers=["conv"],       # eine Layer eingefroren
            augment_training=True,        # eine Datenaugmentation 
            early_stopping_patience=5,    # Stoppt, wenn Val-Metrik 5 Epochen nicht besser wird
        ),
        data=args.DataArgs(
            batch_size=8,                 # 8 Zeilen/Bilder pro Update
            num_workers=2,                # 2 Worker fürs Laden/Preprocessing
            reading_order="LTR",          # Leserichtung: Left-to-Right
        ),
        optimizer=args.OptimizerArgs(
            name="SGD",                   # Optimizer: Stochastic Gradient Descent
            momentum=0.9,                 # Momentum zur Stabilisierung/Beschleunigung
            learning_rate=1e-3,           # Lernrate 0.001
            weight_l2_penalty=0.0001,
        ),
        trainer=args.TrainerArgs(
            gpus=1,                       # GPU-Training 
            max_epochs=25,                # Maximal 25 Epochen
        ),
    )
if __name__ == "__main__":  # Startet main() nur, wenn das Skript direkt ausgeführt wird
    main()
