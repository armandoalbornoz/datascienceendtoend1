from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_validation import DataValidation
from src.datascience import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass
    def run(self):
        try:
            config= ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate()
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f"----- Stage {STAGE_NAME} started -----")
        obj = DataValidationTrainingPipeline()
        obj.run()
        logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
    except Exception as e:
        logger.exception(e)
        raise e 

