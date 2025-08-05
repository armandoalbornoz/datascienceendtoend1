## Component-Data Ingestion
import urllib.request as request
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from src.datascience import logger
from src.datascience.entity.config_entity import DataIngestionConfig

class DataIngestion:
    """
    Component for data ingestion operations including querying data from the database and
    saving it as a csv file.
    """
    def __init__(self, config:DataIngestionConfig):

        """
        Initialize DataIngestion with configuration.
        
        Args:
            config (DataIngestionConfig): Configuration object containing data ingestion parameters
        """
             
        self.config = config
    
    def ingest_data(self):
        """
        Gets the data from a RDS instance and saves it to a csv file
        """
        load_dotenv()

        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )   
        
            df = pd.read_sql("SELECT * FROM weather_data", conn) # Get data from databases
            df.to_csv(self.config.local_data_file, index=False) # Save data to csv

                
        except Exception as e:
            logger.error(f"Error  ingesting data: {e}")
            raise