from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.etl_extraction import DataExtraction
from src.datascience import logger
import pandas as pd

STAGE_NAME = "ETL Data Extraction Stage"

class DataExtractionTrainingPipeline:
    def __init__(self):
        pass
    def run(self) -> pd.DataFrame:
        try:
            config= ConfigurationManager()
            data_extraction_config = config.get_data_extraction_config()
            data_extraction = DataExtraction(config=data_extraction_config)
            extracted_data = data_extraction.extract()
            return extracted_data
        except Exception as e:
            raise e

if __name__ == '__main__':
    try:
        logger.info(f"----- Stage {STAGE_NAME} started -----")
        obj = DataExtractionTrainingPipeline()
        obj.run()
        logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
    except Exception as e:
        logger.exception(e)
        raise e 

