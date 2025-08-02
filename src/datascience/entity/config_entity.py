from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    """Configuration class for data ingestion parameters."""
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

    This class contains all the parameters and paths needed for training
    machine learning models, particularly focused on regression tasks.

    """
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    alpha: float
    l1_ratio: float
    target_column: str