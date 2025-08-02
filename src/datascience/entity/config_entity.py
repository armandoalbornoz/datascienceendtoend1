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