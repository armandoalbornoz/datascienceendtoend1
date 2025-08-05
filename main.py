from src.datascience import logger
from src.datascience.pipeline.data_extraction import DataExtractionTrainingPipeline
from src.datascience.pipeline.etl_data_transformation import ETLDataTransformationDataPipeline
from src.datascience.pipeline.data_loading import DataLoadingTrainingPipeline
from src.datascience.pipeline.data_ingestion import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation import DataValidationTrainingPipeline
from src.datascience.pipeline.data_transformation import DataTransformationDataPipeline
from src.datascience.pipeline.model_trainer import ModelTrainingPipeline
from src.datascience.pipeline.model_evaluation import ModelEvaluationPipeline


STAGE_NAME = "ETL Data Extraction Stage"

try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = DataExtractionTrainingPipeline()
    extracted_data = obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 


STAGE_NAME = "ETL Data Transformation Stage"

try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = ETLDataTransformationDataPipeline(data=extracted_data)
    transformed_data = obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 


STAGE_NAME = "ETL Data Loading Transformation Stage"
try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = DataLoadingTrainingPipeline(transformed_data)
    obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 



STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f"----- Stage {STAGE_NAME} started -----")
    obj = DataIngestionTrainingPipeline()
    obj.run()
    logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
except Exception as e:
    logger.exception(e)
    raise e 

#STAGE_NAME = "Data Validation Stage"


# try:
#     logger.info(f"----- Stage {STAGE_NAME} started -----")
#     obj = DataValidationTrainingPipeline()
#     obj.run()
#     logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
# except Exception as e:
#     logger.exception(e)
#     raise e 

# STAGE_NAME = "Data Validation Stage"

# try:
#     logger.info(f"----- Stage {STAGE_NAME} started -----")
#     obj = DataTransformationDataPipeline()
#     obj.run()
#     logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
# except Exception as e:
#     logger.exception(e)
#     raise e 

# STAGE_NAME = "Model Training Stage"


# try:
#     logger.info(f"----- Stage {STAGE_NAME} started -----")
#     obj = ModelTrainingPipeline()
#     obj.run()
#     logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
# except Exception as e:
#     logger.exception(e)
#     raise e 



# STAGE_NAME = "Model Evaluation Stage"

# try:
#     logger.info(f"----- Stage {STAGE_NAME} started -----")
#     obj = ModelEvaluationPipeline()
#     obj.run()
#     logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
# except Exception as e:
#     logger.exception(e)
#     raise e 