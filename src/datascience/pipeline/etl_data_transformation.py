from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.etl_data_transformation import ETLDataTransformation
from src.datascience import logger
from pathlib import Path
import pandas as pd


STAGE_NAME = "Data Validation Stage"

class ETLDataTransformationDataPipeline:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    def run(self):
        try:
            config = ConfigurationManager()
            etl_data_transformation_config = config.get_etl_data_transformation_config()
            etl_data_transformation = ETLDataTransformation(config=etl_data_transformation_config, data=self.data)
            return etl_data_transformation.transform()

        except Exception as e: 
            raise e  
        

