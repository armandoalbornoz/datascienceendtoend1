import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from src.datascience import logger
import joblib
from typing import List
from pathlib import Path
import mlflow
import mlflow.sklearn
import os
from dotenv import load_dotenv
import json
from src.datascience.entity.config_entity import ModelTrainerConfig
load_dotenv()

EXPERIMENT_NAME = "rain-prediction"


class ModelTrainer:
    """
    Component for training machine learning models.
    """
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        self.estimators = {}

    def __init_mlflow(self):
        # authentication
        os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
        os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
        mlflow.set_experiment(EXPERIMENT_NAME)

    def _make_estimators(self):
        """
        This method populates self.estimators with object estimators.
        """

        for name in self.config.available_models:
            if name == "logistic_regression":
                self.estimators[name] = LogisticRegression(max_iter=2000)
            elif name == "random_forest":
                self.estimators[name] = RandomForestClassifier(random_state=42, n_jobs=-1)
            elif name == "svm":
                # probability=True so we can use predict_proba for ROC AUC
                self.estimators[name] = SVC(probability=True)
        

    def train(self):
        """
        Trains several models and saves them.
        
        Raises:
            FileNotFoundError: If training or testing data files don't exist
            Exception: If there's an error during training
        """
        try:

            # Set mlflow
            self.__init_mlflow()

            # load data
            train_data = pd.read_csv(self.config.train_data_path)

            train_x = train_data.drop([self.config.target_column], axis=1)
            train_y = train_data[self.config.target_column].astype(int)

            # Obtain estimators
            self._make_estimators()

            # Define Constants
            leaderboard = [] # This will hold a leaderboard of the models we will train
            best_name, best_est, best_score  = None, None, float("-inf")
            best_run_id = ""

             # Use gridSearch with cross validation to train the models and log to MLflow
            for name, estimator in self.estimators.items():
                logger.info(f"Training {name} with GridSearchCV")

                param_grid = self.config.params.model_params.get(name, {})
                grid_search = GridSearchCV(
                    estimator=estimator,
                    param_grid=param_grid,
                    cv=self.config.cross_validation,
                    scoring=self.config.scoring,
                    n_jobs=-1
                )

                with mlflow.start_run(run_name=f"train:{name}") as run:
                    mlflow.log_param("model_name", name)
                    mlflow.log_param("cv_folds", int(self.config.cross_validation))
                    mlflow.log_param("scoring", self.config.scoring)
                    mlflow.log_param("grid_size", len(param_grid) if isinstance(param_grid, dict) else 0)

                    grid_search.fit(train_x, train_y)

                    # Log the best params and CV score
                    mlflow.log_metric("cv_best_score", float(grid_search.best_score_))
                    for param,value in grid_search.best_params_.items():
                        mlflow.log_param(f"best_{param}", value)

                    # Let's save the full cv_results as an artifact
                    cv_results_path = os.path.join(self.config.root_dir, f"{name}_cv_results.json")
                    with open(cv_results_path, "w") as f:
                        json.dump(grid_search.cv_results_, f, default=str, indent=2)
                    mlflow.log_artifact(str(cv_results_path))

                    # Log the best estimator for this model 
                    mlflow.sklearn.log_model(grid_search.best_estimator_, artifact_path=name)

                    leaderboard.append({
                        "model": name,
                        "cv_best_score": float(grid_search.best_score_),
                        "best_params": grid_search.best_params_
                    })

                    # global best tracking 
                    if grid_search.best_score_ > best_score:
                        best_score = grid_search.best_score_
                        best_name, best_est = name, grid_search.best_estimator_
                        best_run_id = run.info.run_id



                    logger.info(f"{name} best params: {grid_search.best_params_}")
                    logger.info(f"{name} best CV score: {grid_search.best_score_:.4f}")

         
            # Save best model locally
            joblib.dump(best_est, os.path.join(self.config.root_dir, self.config.model_name))

            # Save leaderboard
            Path(os.path.join(self.config.root_dir, "cv_leaderboard.json")).write_text(json.dumps(leaderboard, indent=2))

            # Record the training run_id of this MLflow run
            Path(os.path.join(self.config.root_dir, "train_run_id.txt")).write_text(best_run_id)

            logger.info(f"Training complete. Best model: '{best_name}' (CV={best_score:.4f})")
            logger.info(f"Saved best model")
            logger.info(f"Saved leaderboard")
            logger.info(f"Saved train run id to")


        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise
        