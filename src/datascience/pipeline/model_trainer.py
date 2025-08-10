from src.datascience.config.configuration import ConfigurationManager
from src.datascience import logger
from src.datascience.components.model_training import ModelTrainer

STAGE_NAME = "Model Training Stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass
    def run(self):
        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.train()
        except Exception as e:
            raise e 

if __name__ == '__main__':
    try:
        logger.info(f"----- Stage {STAGE_NAME} started -----")
        obj = ModelTrainingPipeline()
        obj.run()
        logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
    except Exception as e:
        logger.exception(e)
        raise e 

