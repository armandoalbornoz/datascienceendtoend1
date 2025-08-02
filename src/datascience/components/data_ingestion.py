import os 
import urllib.request as request
from src.datascience import logger
import zipfile
from src.datascience.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    """
    Component for data ingestion operations including downloading and extracting files.
    """
    def __init__(self, config:DataIngestionConfig):

        """
        Initialize DataIngestion with configuration.
        
        Args:
            config (DataIngestionConfig): Configuration object containing data ingestion parameters
        """
             
        self.config = config
    
    def download_file(self) -> None:
        """
        Download file from source URL if it doesn't already exist locally.
        
        Raises:
            Exception: If there's an error downloading the file
        """
        try:
            if not os.path.exists(self.config.local_data_file):
                # Ensure parent directory exists before downloading
                os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
                
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logger.info(f"{filename} download completed!")
            else:
                logger.info(f"File {self.config.local_data_file} already exists!")
                
        except Exception as e:
            logger.error(f"Error downloading file from {self.config.source_URL}: {e}")
            raise


    def extract_zip_file(self):

        """
        Exctract ZIP file to the specified directory.

        Raises:
            FileNotFoundError: If the ZIP file doesn't exist
            zipfile.BadZipFile: If the file is not a valid ZIP file
            Exception: If there's an error extracting the file
        """

        try:
            if not os.path.exists(self.config.local_data_file):
                raise FileNotFoundError(f"ZIP file not found {self.config.local_data_file}")
            
            unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path, exist_ok=True)


            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)

            logger.info(f"ZIP file extracted successfully to {unzip_path}")

        except zipfile.BadZipFile as e:
            logger.error(f"Invalid ZIP file {self.config.local_data_file}: {e}")
            raise
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {e}")
            raise


    def perform_data_ingestion(self) -> None:
        """
        Complete data ingestion process: download and extract.
        
        This method orchestrates the full data ingestion pipeline.
        """

        try:
            logger.info("Starting data ingestion process")
            self.download_file()
            self.extract_zip_file()
            logger.info("Data ingestion process completed successfully") 
        except Exception as e:
            logger.error(f"Data ingestion process failed: {e}")
            raise          


