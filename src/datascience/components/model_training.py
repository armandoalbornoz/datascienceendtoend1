import pandas as pd
import os
from src.datascience import logger
from sklearn.linear_model import ElasticNet
import joblib
from src.datascience.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    """
    Component for training machine learning models.
    """
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def train(self):
        """
        Trains the ElasticNet model and saves it.
        
        Raises:
            FileNotFoundError: If training or testing data files don't exist
            Exception: If there's an error during training
        """
        try:

            train_data = pd.read_csv(self.config.train_data_path)
            test_data = pd.read_csv(self.config.test_data_path)

            train_x = train_data.drop([self.config.target_column], axis=1)
            test_x  = test_data.drop([self.config.target_column], axis=1)
            train_y = train_data[self.config.target_column]
            test_y = test_data[self.config.target_column]

            lr = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio, random_state=42)
            lr.fit(train_x, train_y)
            logger.info("Model training completed")

            joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise
        