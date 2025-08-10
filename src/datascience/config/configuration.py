from src.datascience.constants import * 
from src.datascience.utils.common import read_yaml, create_directories
from src.datascience.entity.config_entity import (DataIngestionConfig, 
                                                  DataValidationConfig, 
                                                  DataTransformationConfig, 
                                                  ModelTrainerConfig, 
                                                  ModelEvaluationConfig,
                                                  DataExtractionConfig,
                                                  ETLDataTransformationConfig,
                                                  ETLDataLoadingConfig)
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


    def get_data_extraction_config(self) -> DataExtractionConfig:
        config = self.config.etl_data_extraction

        data_extraction_config = DataExtractionConfig(
            lat = config.lat,
            lon = config.lon,
            start_offset_days = config.start_offset_days,
            end_offset_days = config.end_offset_days
        )

        return data_extraction_config
    
    def get_etl_data_transformation_config(self) -> ETLDataTransformationConfig:
        config = self.config.etl_data_transformation

        etl_data_transformation_config = ETLDataTransformationConfig()

        return etl_data_transformation_config
    
    def get_etl_data_loading_config(self) -> ETLDataLoadingConfig:
        config = self.config.data_loading

        etl_data_loading_config = ETLDataLoadingConfig(
            port = config.port
        )

        return etl_data_loading_config


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            local_data_file = config.local_data_file,
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir =  config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )
        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir= config.root_dir,
            data_path=config.data_path,
            test_size=config.test_size,
            random_state=config.random_state
        )
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            model_name = config.model_name,
            cross_validation = int(config.cross_validation),
            scoring= config.scoring,
            available_models = config.available_models,
            target_column = config.target_column,   

            params = params
        )
        return model_trainer_config
    
    
    def get_model_evaluation_config(self)-> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.ElasticNet
        schema = self.schema.TARGET_COLUMN
        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            test_data_path = config.test_data_path,
            model_path = config.model_path,
            all_params = params,
            metric_file_name = config.metric_file_name,
            target_column = schema.name,
            mlflow_uri="https://dagshub.com/armandoalbornoz/datascienceendtoend1.mlflow"
        )

        return model_evaluation_config