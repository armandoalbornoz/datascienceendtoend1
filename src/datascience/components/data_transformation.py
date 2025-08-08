import os
from src.datascience import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from src.datascience.entity.config_entity import DataTransformationConfig
import numpy as np
from sklearn.preprocessing import StandardScaler

class DataTransformation:
    """
    Component for data transformation operations including feature extraction,
    data transformation, and train-test split.

    Raises:
        FileNotFoundError: If the data file doesn't exists

    """
 
    def __init__(self, config: DataTransformationConfig):
        self.config = config

        try:
            ## Load data
            self.df  = pd.read_csv(self.config.data_path)
            logger.info(f"Loading data from: {self.config.data_path}")
        except Exception as e:
            logger.error(f"Error when loading data during data transformation: {e}")
            raise 
            

    def feature_extraction(self):
        """
        This method perform all sort of feature extraction procedures to the data obtained
        from the API

        Raises:
            Exception: If there is an error during extraction
        """
        try:
            # Obtain target 
            logger.info(f"Adding target to the loaded data")
            precipitation_cols =[f"precipitation_{i}" for i in range(1, 25)]
            self.df["precipitation"] = self.df[precipitation_cols].sum(axis=1)  # Sum the precipitation cols along the rows
            self.df["rain"] = (self.df["precipitation"] > 0).astype(int) # If precipitation is greater than 0 it likely rained
            self.df = self.df.drop(columns=precipitation_cols)
            self.df = self.df.drop(columns=["precipitation"])

            # Remove date  column
            logger.info(f"Removing date column")
            self.df = self.df.drop(columns=["date"])

            # extracting avg from surfa_pressure and temperature_2m
            logger.info(f"Performing feature extraction")
            temp_cols = [col for col in self.df.columns if col.startswith("temperature_2m_")]
            pressure_cols = [col for col in self.df.columns if col.startswith("surface_pressure_")]
            self.df["surface_pressure_avg"] = self.df[pressure_cols].mean(axis=1)
            self.df["temperature_2m_avg"] = self.df[temp_cols].mean(axis=1)
            self.df = self.df.drop(columns=pressure_cols)
            self.df = self.df.drop(columns=temp_cols)

            # Eliminating shortwave_radiation_ due to high correlation with sunshine
            cols = [col for col in self.df.columns if col.startswith("shortwave_radiation_")]
            self.df = self.df.drop(columns=cols)

            # getting daily det0_fao_evapotranspiration and sunshine
            sunshine_cols = [col for col in self.df.columns if col.startswith("sunshine_duration_")] 
            self.df["daily_sunshine"] = self.df[sunshine_cols].sum(axis=1)
            self.df = self.df.drop(columns=sunshine_cols)

            det0_fao_evapotranspiration_cols = [col for col in self.df.columns if col.startswith("et0_fao_evapotranspiration_")]
            self.df["daily_et0_fao_evapotranspiration"] = self.df[det0_fao_evapotranspiration_cols].sum(axis=1)
            self.df = self.df.drop(columns=det0_fao_evapotranspiration_cols)

            # Summarizing instant features

            features = [
            "relative_humidity_2m", "cloud_cover",
            "wind_speed_10m", "wind_direction_10m"
            ]

            for col_name in features:
                cols = [col for col in self.df.columns if col.startswith(col_name)]
                self.df[f"{col_name}_avg"] = self.df[cols].mean(axis=1)
                self.df = self.df.drop(columns=cols)

        except Exception as e:
            logger.error("An error occured while performing feature extraction: {e}")
            raise 

    def feature_transformation(self):
        """
        This method log transforms skewed features, fixes circular features and standardizes
        all but the circular feature

        Exception: If there is an error during transformation
        """
        # Log transform features
        self.df["daily_sunshine"] = np.log1p(self.df["daily_sunshine"])
        self.df["wind_speed_10m_avg"] = np.log1p(self.df["wind_speed_10m_avg"])


        # Standardizes features
        features_to_standardize = [
            "temperature_2m_avg",
            "surface_pressure_avg",
            "relative_humidity_2m_avg",
            "cloud_cover_avg",
            "daily_et0_fao_evapotranspiration",
            "daily_sunshine",
            "wind_speed_10m_avg"
        ]

        scaler =  StandardScaler()
        self.df[features_to_standardize] = scaler.fit_transform(self.df[features_to_standardize])
    
        ## Fixes circular feature
        wind_direction_angles = self.df["wind_direction_10m_avg"]
        self.df["wind_dir_sin"] = np.sin(np.radians(wind_direction_angles))
        self.df["wind_dir_cos"] = np.cos(np.radians(wind_direction_angles))
        self.df = self.df.drop(columns=["wind_direction_10m_avg"])


    def train_test_split_(self):
        """
        Split the data into training and testing sets.

        Raises:
            Exception: If there is an error during splitting
        """

        try:
            # Split the data into train and test
            logger.info(f"Splitting the data")
            train, test = train_test_split(self.df, test_size= self.config.test_size, random_state=self.config.random_state)
            logger.info("Splitted data into training and test sets")

            train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index = False)
            test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index = False)

            print(f"Files saved to: {self.config.root_dir}")
            logger.info(train.shape)
            logger.info(test.shape)
        except Exception as e:
            logger.error(f"Error during train-test split: {e}")
            raise