import os
from src.datascience import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from src.datascience.entity.config_entity import DataTransformationConfig

class DataTransformation:
    """
    Component for data transformation operations including train-test split.
    """
 
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_split_(self):
        """
        Split the data into training and testing sets.

        Raises:
            FileNotFoundError: If the data file doesn't exists
            Exception: If there is an error during splitting
        """

        try:
            # Load data    
            logger.info(f"Loading data from: {self.config.data_path}")
            data = pd.read_csv(self.config.data_path)

            if "Id" in data.columns:
                data = data.drop("Id", axis=1)
                # Save cleaned dataset
                data_path = self.config.data_path
                data.to_csv(data_path, index=False)
                logger.info(f"Cleaned full dataset saved to {data_path}")

            logger.info(f"Data loaded successfully. Original shape: {data.shape}")
            

            # Split the data into train and test
            logger.info(f"Splitting the data")
            train, test = train_test_split(data, test_size= self.config.test_size, random_state=self.config.random_state)
            logger.info("Splitted data into training and test sets")


            train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index = False)
            test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index = False)

            print(f"Files saved to: {self.config.root_dir}")
            logger.info(train.shape)
            logger.info(test.shape)

            print(train.shape)
            print(test.shape)

        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during train-test split: {e}")
            raise