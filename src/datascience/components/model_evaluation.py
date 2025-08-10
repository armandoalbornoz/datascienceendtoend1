import os
import pandas as pd
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    average_precision_score,
    RocCurveDisplay,
    PrecisionRecallDisplay,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt
from urllib.parse import urlparse
import mlflow
from pathlib import Path
import mlflow.sklearn
import numpy as np
import joblib
import json
from dotenv import load_dotenv
from src.datascience.entity.config_entity import ModelEvaluationConfig
load_dotenv()

class ModelEvaluation:
    """
    Handles model evaluation after training.

    Methods:
        _init_mlflow():
            Initializes MLflow authentication, tracking URI, and experiment name.
        
        evaluate():
            - Loads the trained model and test dataset.
            - Generates predictions and probability scores.
            - Computes metrics: accuracy, precision, recall, F1, and ROC AUC.
            - Logs metrics and plots (ROC, PR curve, confusion matrix) to MLflow.
            - Saves metrics locally as JSON.
            - Logs the evaluated model to MLflow.
    """

    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def _init_mlflow(self):
        # authentication
        os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
        os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
        mlflow.set_experiment(self.config.experiment_name)


    def evaluate(self):
        self._init_mlflow()

        # Load the model and data
        model = joblib.load(self.config.model_path)
        test_df = pd.read_csv(self.config.test_data_path)

        X_test = test_df.drop(columns=[self.config.target_column])
        y_test = test_df[self.config.target_column].astype(int)

        # Start Evaluation

        with mlflow.start_run(run_name="evaluation"):
            # Link to training run if available

            train_run_id = ""
            try:
                train_run_id = Path(self.config.train_run_id_path).read_text().strip()
            except Exception:
                pass
            
            # Predictions
            if hasattr(model, "predict_proba"):
                y_score = model.predict_proba(X_test)[:, 1]
            elif hasattr(model, "decision_function"):
                y_score = model.decision_function(X_test)
            else:
                y_score = None

            y_pred = model.predict(X_test)
            report = classification_report(y_test, y_pred, output_dict=True)

            metrics = {
                        "accuracy": float(report["accuracy"]),
                        "precision_weighted": float(report["weighted avg"]["precision"]),
                        "recall_weighted": float(report["weighted avg"]["recall"]),
                        "f1_weighted": float(report["weighted avg"]["f1-score"]),
                    }
        
            # we need y_score not to be none in order to be able to calculate roc_auc
            if y_score is not None:
                metrics["roc_auc"] = float(roc_auc_score(y_test, y_score))

            # Log the metrics to mlflow
            mlflow.log_metrics(metrics)

            # save the metrics as artifact

            metrics_path = Path(os.path.join(self.config.root_dir, "test_metrics.json"))
            metrics_blob = {"metrics": metrics, "classification_report": report}
            metrics_path.write_text(json.dumps(metrics_blob, indent=2)) 
            mlflow.log_artifact(str(metrics_path))


            # Plots

            if y_score is not None:
                RocCurveDisplay.from_predictions(y_test, y_score)
                mlflow.log_figure(plt.gcf(), "roc_curve.png")
                plt.close()

                PrecisionRecallDisplay.from_predictions(y_test, y_score)
                mlflow.log_figure(plt.gcf(), "pr_curve.png")
                plt.close()


            ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
            mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
            plt.close()

            # log evaluated model
            mlflow.sklearn.log_model(model, artifact_path="evaluated_model")




    