from src.datascience import logger
from src.datascience.pipeline.data_ingestion import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation import DataValidationTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = DataIngestionTrainingPipeline()
    obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 

STAGE_NAME = "Data Validation Stage"


try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = DataValidationTrainingPipeline()
    obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 
