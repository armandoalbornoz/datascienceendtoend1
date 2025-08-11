import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from src.datascience.utils.common import get_env
from src.datascience import logger
from src.datascience.entity.config_entity import ETLDataLoadingConfig

load_dotenv()

class DataLoading:
    """
    Component for data loading operations including loading the data to an RDS instance
    """
    def __init__(self, config: ETLDataLoadingConfig, data: pd.DataFrame):

        self.config = config
        self.data = data

        self.config = {
            'host': get_env("POSTGRES_HOST"),
            'port': int(self.config.port),
            'database': get_env("POSTGRES_DB"),
            'user': get_env("POSTGRES_USER"),
            'password': get_env("POSTGRES_PASSWORD")
        }

        self.connection = None
        logger.info("PostgreSQL connection manager initialized")

    def connect(self):
        try:
            if self.connection is None or self.connection.closed:
                self.connection = psycopg2.connect(**self.config)
                logger.info("Successfully connected to PostgreSQL database")
            
            return self.connection
            
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            raise
    
    def disconnect(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("PostgreSQL connection closed")

    def create_weather_table(self):
        features = [
            "temperature_2m", "relative_humidity_2m", "precipitation", "cloud_cover",
            "wind_speed_10m", "wind_direction_10m", "shortwave_radiation",
            "surface_pressure", "sunshine_duration", "et0_fao_evapotranspiration"
        ]

        try:
            self.connect()

            columns = ["date DATE PRIMARY KEY"]

            for feat in features:
                for hour in range(1, 25):
                    col_name = f"{feat}_{hour}"
                    columns.append(f"{col_name} FLOAT")


            create_table_sql = f""" 
            CREATE TABLE IF NOT EXISTS  weather_data (
                {', '.join(columns)}
            );
            """
            # Execute the SQL to create the table

            with self.connection.cursor() as cur:
                cur.execute(create_table_sql)
                self.connection.commit()
            

            logger.info(f"Weather table created")   

        except psycopg2.Error as e:
            logger.error(f"PostgreSQL error creating weather table: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating weather table: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
            return False

    def insert_data(self):
        try:
            self.connect()

            columns = self.data.columns.tolist()
            columns_sql = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))

            insert_sql = f"""
            INSERT INTO weather_data ({columns_sql})
            VALUES %s
            ON CONFLICT (date) DO NOTHING;
            """

            # Convert DataFrame to list of tuples
            values = [tuple(row) for row in self.data.to_numpy()]

            with self.connection.cursor() as cur:
                execute_values(cur, insert_sql, values)
                self.connection.commit()
            logger.info("Data inserted successfully")

        except Exception as e:
            logger.error(f"Error inserting data into PostgreSQL: {e}")
            self.connection.rollback()
        