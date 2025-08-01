from src.datascience.constants import * 
from src.datascience.utils.common import read_yaml, create_directories
from src.datascience.entity.config_entity import (DataIngestionConfig)
from src.datascience import logger

class ConfigurationManager:
    """
    Configuration manager for handling YAML configuration files.
    
    This class loads configuration, parameters, and schema files and provides
    methods to retrieve specific configuration objects.
    """
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath= PARAMS_FILE_PATH, schema_filepath = SCHEMA_FILE_PATH ):

        """
        Initialize the ConfigurationManager.
        
        Args:
            config_filepath (Path): Path to the main configuration file
            params_filepath (Path): Path to the parameters file
            schema_filepath (Path): Path to the schema file
        """
          
        try:
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            self.schema = read_yaml(schema_filepath)
            
            # Create artifacts root directory
            create_directories([self.config.artifacts_root])
            logger.info("ConfigurationManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ConfigurationManager: {e}")
            raise


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )

        return data_ingestion_config