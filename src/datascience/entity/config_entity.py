from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataExtractionConfig:
    """
    Configuration class for data Extraction parameters.

    Attributes:
        lat: 
        lon: 
        start_offset_days: 
        end_offset_days: 
    """

@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion parameters.

      Attributes:
        root_dir: Directory where validation artifacts will be stored
        source_URL: URL of the zip file we want to download
        local_data_file: File path of the downloaded zip file
        unzip_dir: File path of the dir that will contain our data
    """
    
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

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
    """
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    alpha: float
    l1_ratio: float
    target_column: str

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