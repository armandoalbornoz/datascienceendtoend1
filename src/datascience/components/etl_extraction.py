import requests
import pandas as pd
from datetime import datetime, timedelta
import os 
from src.datascience import logger
from dotenv import load_dotenv
from src.datascience.entity.config_entity import DataExtractionConfig

class DataExtraction:
    """
    Component for data Extraction operations. It extracts data from the open meteo API.
    """

    def __init__(self, config: DataExtractionConfig):
        """
        Initialize DataExtraction with configuration.
        
        Args:
            config (DataExtractionConfig): Configuration object containing data extraction parameters
        """
        self.config = config
    
    def extract(self) -> pd.DataFrame:
        """
        Performs the extraction process
        
        Raises:
            Exception: If there's an error with the API
        """

        try: 
            END_DATE = datetime.today().date() - timedelta(days=self.config.end_offset_days)
            START_DATE = END_DATE - timedelta(days=self.config.start_offset_days)

            # Format the date strings
            start = START_DATE.strftime("%Y-%m-%d")
            end = END_DATE.strftime("%Y-%m-%d")

            # (hourly) features we will extract

            HOURLY_FEATURES = [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "shortwave_radiation",
                "surface_pressure",
                "sunshine_duration",
                "et0_fao_evapotranspiration"
            ]

            url = "https://archive-api.open-meteo.com/v1/archive"

            params = {
                "latitude": self.config.lat,
                "longitude": self.config.lon,
                "start_date": start,   
                "end_date": end,
                "hourly": ",".join(HOURLY_FEATURES),
                "timezone": "auto"
            }

            response = requests.get(url=url, params=params)
            return pd.DataFrame(response.json()["hourly"])
        
        except Exception as e:
            logger.error(f"Error getting data from the API {e}")
            raise e
            

