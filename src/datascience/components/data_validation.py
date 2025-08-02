from src.datascience import logger
from src.datascience.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    """
    Data validation component for validating dataset schema and structure.
    """
    
    def __init__(self, config: DataValidationConfig):
        """
        Initialize DataValidation with configuration.
        
        Args:
            config (DataValidationConfig): Configuration object for data validation
        """
        self.config = config
        logger.info("DataValidation component initialized")


    def validate(self)-> bool:
        """
        Validate that all columns in the dataset match the expected schema.
        
        Returns:
            bool: True if validation passes, False otherwise
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            Exception: If there's an error during validation
        """

        try:
            validation_status = True
            missing_columns = []
            extra_columns = []

            # Read the CSV file
            logger.info(f"Reading CSV file from: {self.config.unzip_data_dir}")

            data = pd.read_csv(self.config.unzip_data_dir)
            actual_columns = list(data.columns)

            expected_columns = self.config.all_schema.keys()

            # Check for missing columns
            missing_columns = [col for col in expected_columns if col not in actual_columns]
            
            # Check for extra columns (found but not expected)
            extra_columns = [col for col in actual_columns if col not in expected_columns]

            if missing_columns:
                validation_status = False
                logger.error(f"Missing columns: {missing_columns}")
            
            if extra_columns:
                logger.warning(f"Extra columns found: {extra_columns}")
                validation_status = False

            status_message = f"Validation status: {validation_status}"

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(status_message)

            logger.info(f"Validation completed. Status: {validation_status}")

            return validation_status
        except FileNotFoundError as e:
            logger.error(f"CSV file not found: {e}")
            self._write_error_status(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during column validation: {e}")
            self._write_error_status(f"Validation error: {e}")
            raise
