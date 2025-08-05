from src.datascience.entity.config_entity import ETLDataTransformationConfig
import pandas as pd


class ETLDataTransformation:
    """
    Component for ETL data transformation operations. This transforms our 10 features into 240 features.
    For more info check the correspoding notebook.
    """
        
    def __init__(self, config: ETLDataTransformationConfig, data: pd.DataFrame):
        self.config = config
        self.data = data
    
    def transform(self) -> pd.DataFrame:
        # This line transforms the list of strings data["time"] into a list of datetime64 objets
        # dt.date just extracts the date part. We add this as a new column
        self.data["date"] = pd.to_datetime(self.data["time"]).dt.date

        # Drop the time column 
        self.data = self.data.drop(columns=["time"])

        # Group by date and flatten
        flattened_rows = []
        for date, groupdf in self.data.groupby("date"):
            flat_row = {"date": date}
            for col in groupdf.columns:
                if col == "date":
                    continue
                for i , val in enumerate(groupdf[col].values):
                    flat_row[f"{col}_{i+1}"] = val
            flattened_rows.append(flat_row)

        return pd.DataFrame(flattened_rows)

