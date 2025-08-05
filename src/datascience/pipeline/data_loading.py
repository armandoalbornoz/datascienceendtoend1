from src.datascience.config.configuration import ConfigurationManager
from src.datascience.components.data_loading import DataLoading
from src.datascience import logger
import pandas as pd

STAGE_NAME = "ETL Data Loading Stage"

class DataLoadingTrainingPipeline:
    def __init__(self, data: pd.DataFrame):
        self.data = data # data we will load
    def run(self) -> pd.DataFrame:
        try:
            config= ConfigurationManager()
            data_loading_config = config.get_etl_data_loading_config()
            data_loading = DataLoading(config=data_loading_config, data=self.data)
            data_loading.connect()
            data_loading.create_weather_table()
            data_loading.insert_data()
        except Exception as e:
            raise e