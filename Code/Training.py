from pathlib import Path

from laia.scripts.htr.create_model import run as create_model
from laia.scripts.htr.train_ctc import run as train_ctc
import laia.common.arguments as args

SYMS_DE = "dataset/syms_de.txt"             
EXP_DIR = "./experiments"          
MODEL_FILENAME = "experiment/model/model"

                    

Path(EXP_DIR).mkdir(parents=True, exist_ok=True)

create_model(
    
    SYMS_DE,
    fixed_input_height=128,
 
    common=args.CommonArgs(
        train_path=EXP_DIR,
        model_filename=MODEL_FILENAME,
    
    ),
    crnn=args.CreateCRNNArgs(
        cnn_num_features=[12, 24, 48, 48], 
        cnn_batchnorm=[True, True, True, True],
    ),   
)


IMG_DIRS = ["dataset"]       
TR_TXT   = "dataset/train.txt"
VA_TXT   = "dataset/val.txt"

def main():
    train_ctc(
        SYMS_DE,
        IMG_DIRS,
        TR_TXT,
        VA_TXT,
        common=args.CommonArgs(
            train_path=EXP_DIR,
            experiment_dirname="experiment",
            checkpoint="weights.ckpt",
            model_filename=MODEL_FILENAME,
        ),
        train=args.TrainArgs(
            pretrain=True,
            freeze_layers=[],
            augment_training=False,
            early_stopping_patience= 5,
        ),
        data=args.DataArgs(batch_size=8,num_workers= 2,reading_order= "LTR"),
        optimizer=args.OptimizerArgs(name="SGD", momentum= 0.8,learning_rate=1e-3),
        trainer=args.TrainerArgs(gpus=0, max_epochs=25),
    )

if __name__ == "__main__":
    main()

