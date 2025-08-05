from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_ingestion import DataIngestion
from src.datascience import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    def run(self):
        try:
            config= ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.ingest_data()
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f"----- Stage {STAGE_NAME} started -----")
        obj = DataIngestionTrainingPipeline()
        obj.run()
        logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
    except Exception as e:
        logger.exception(e)
        raise e 

