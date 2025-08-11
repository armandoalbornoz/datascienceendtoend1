# Rain Prediction - End-to-End Machine Learning Pipeline

This project implements an end-to-end machine learning pipeline for rain prediction using historical weather data from [text](https://open-meteo.com/) 
The project handles everything from raw data injestion using an ETL pipeline to deployment.

## Pipeline

1. **Config-First Design**
    - All paths and hyperparameters live in YAML files (`config.yaml` and `params.yaml`)
    - Components of the pipeline read required configuration from entity configuration classes.
    - This type of design allows us to simply modify the configuration files if we want to try something different. For example, we can change date configuration variables to obtain data of the current day, and retrain our models with uptodate data.

2. **Modular Components** 
    - **Data Ingestion**: Reads raw API ouput and saves it to an RDS SQL instace
    - **Data Transformation**: Transforms the data obtained from the Data Ingestion using feature engineering. Splits the data into train.csv and test.csv
    - **Model Trainer**: Runs GridSearchCV over several estimators, logs to MLflow, and saves the best model and other artifacts.
    - **Model EvaluationL**: Evaluates the best model obtained from the training component, and logs several metrics to MLflow.

3. **main.py**

    - This is the central entry point for running the full pipeline. When executed, it reads configuration from YAML files and calls each pipeline stage in sequence:
   - **Data Ingestion**
   - **Data Transformation**
   - **Model Training**
   - **Model Evaluation**


4. **Reproducibility and Traceability**  
   - Models and data versioned in DVC.  
   - Experiment parameters and evaluation metrics tracked with MLflow.

5. **Deployment (Streamlit App)**  
   - On startup, app.py pulls `best_model.joblib` from DVC remote if missing.  
   - Accepts transformed feature inputs, computes predictions and probabilities.  
