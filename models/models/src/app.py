import ipdb
from config import logger, settings
from models.src.helpers.dataloader import Data
from models.src.classesdata import ProblemTypes, HyperParameterDirection, DataFields
from models.src.trainers import LightGBMTrainer


def run_trainer():
    logger.info("Starting Trainer")

    logger.info("Creating Trainer Class")

    PBTYPE = ProblemTypes.BINARY

    # Defining Data Fields
    fields = DataFields(sample_data=True, data_type=PBTYPE.value, path='.', features=[
                        'tst'], target=['tst'], single_file=False)
    # Getting Data
    data = Data(**fields.dict())

    # Creating Trainder
    trainer = LightGBMTrainer(data=data, problemType=PBTYPE)

    # Converting Data to lightgbm
    trainer.convert_to_lgb()

    # Training HyperParameters, Direction Needs to Be and Enum
    logger.info("Starting Hyperparameter Tuning")
    trial = trainer.hyperparametertune(
        eval_rounds=20, stopping_rounds=100, total_trials=100, direction=HyperParameterDirection.MAXIMIZE
    )

    # Training Final Model
    logger.info("Training Final Model")
    model = trainer.train(trial.params, eval_rounds=100, stopping_rounds=10)
    #model= trainer.default_train()

    # Getting Predictions
    logger.info("Making Predictions")
    predictions = trainer.predict(model)
    logger.info(predictions)

    logger.info("Trainer Finished Running")


def main():
    run_trainer()


if __name__ == '__main__':
    main()
