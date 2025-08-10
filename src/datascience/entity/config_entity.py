from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataExtractionConfig:
    """
    Configuration class for data extraction parameters.

    Attributes:
        lat: The latitude of the location we want to get data from
        lon: The longitude of the location we want to get data from
        start_offset_days: start date is end_date minus this offset
        end_offset_days: End data is based on today minus this offset
    """

    lat: float
    lon: float
    start_offset_days: int
    end_offset_days: int

@dataclass
class ETLDataTransformationConfig:
    """
    Configuration class for ETL data transformation parameters.
    """
    pass


@dataclass
class ETLDataLoadingConfig:
    """
    Configuration class for ETL data loading parameters.
    """
    port: int

@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion parameters.

    Args:
        root_dir (Path): Directory where Ingestion artifacts will be stored
        local_data_file (Path): Path where the data will be stored
    """
    root_dir: Path
    local_data_file: Path
    

@dataclass
class DataValidationConfig:

    """
    Configuration class for data validation operations.
    
    Attributes:
        root_dir: Directory where validation artifacts will be stored
        status_file: Name of the status file to track validation results
        unzip_data_dir: Directory containing the unzipped data to validate
        all_schema: Dictionary containing the expected data schema
    """
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict


@dataclass
class DataTransformationConfig:
    """
    Configuration class for data transformation operations.
    
    Attributes:
        root_dir: Directory where transformation artifacts will be stored
        data_path: Path to the validated data file
        test_size: Proportion of data to use for testing (default: 0.2)
        random_state: Random seed for reproducibility (default: 42)
    """
    root_dir: Path
    data_path: Path
    test_size: float
    random_state: int


@dataclass
class ModelTrainerConfig:
    """
    
    Configuration class for model training operations.

    This class contains all the parameters and paths needed for training
    machine learning models.

    """
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    target_column: str
    cross_validation: int
    scoring: str
    available_models: List[str]
    target_column: str
    params: dict

@dataclass
class ModelEvaluationConfig:    
    """
    Configuration class for model evaluation operations.
    """
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str