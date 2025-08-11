import os
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any, List
from box.exceptions import BoxValueError
import os, subprocess
from pathlib import Path
import streamlit as st



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns a ConfigBox.
    
    Args:
        path_to_yaml (Path): Path to the YAML file
        
    Raises:
        ValueError: If the YAML file is empty
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If there's an error parsing the YAML
        
    Returns:
        ConfigBox: ConfigBox type for attribute-style access
    """
    try:
        if not path_to_yaml.exists():
            raise FileNotFoundError(f"YAML file not found: {path_to_yaml}")
            
        with open(path_to_yaml) as f:
            content = yaml.safe_load(f)
            
        if content is None:
            raise ValueError("YAML file is empty")
            
        logger.info(f"YAML file: {path_to_yaml} loaded successfully")
        return ConfigBox(content)
        
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {path_to_yaml}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading YAML file {path_to_yaml}: {e}")
        raise
    

@ensure_annotations
def create_directories(path_to_directories: List, verbose: bool = True):
    """
    Creates directories from a list of paths.
    
    Args:
        path_to_directories (List[str]): List of directory paths to create
        verbose (bool): Whether to log directory creation. Defaults to True.
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"Created directory at {path}")

    except OSError as e:
        logger.error(f"Error creating directory: {e}")
        raise


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves data to a JSON file.
    
    Args:
        path (Path): Path to the JSON file
        data (dict): Data to be saved in JSON format
        
    Raises:
        TypeError: If data is not JSON serializable
        OSError: If there's an error writing the file
    """
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"json file saved at {path}")
    except TypeError as e:
        logger.error(f"Data is not json serializable: {e}")
        raise
    except OSError as e:
        logger.error(f"Error saving json file {path}: {e}")
        raise


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads data from a JSON file.
    
    Args:
        path (Path): Path to the JSON file
        
    Returns:
        ConfigBox: ConfigBox containing the loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")

        with open(path) as f:
            content = json.load(f)
        logger.info(f"json file loaded successfully from {path}")
        return ConfigBox(content)
    
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading json file {path}: {e}")
        raise


@ensure_annotations
def save_binary(data: Any, path: Path) -> None:
    """
    Saves data to a binary file using joblib.
    
    Args:
        data (Any): Data to be saved (typically ML models)
        path (Path): Path where the binary file will be saved
        
    Raises:
        OSError: If there's an error writing the file
    """
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at {path}")
        
    except Exception as e:
        logger.error(f"Error saving binary file {path}: {e}")
        raise


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.
    
    Args:
        path (Path): Path to the binary file
        
    Returns:
        Any: The loaded data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"Binary file not found: {path}")
            
        data = joblib.load(path)
        logger.info(f"Binary file loaded from {path}")
        return data
        
    except Exception as e:
        logger.error(f"Error loading binary file {path}: {e}")
        raise


@ensure_annotations
def get_env(key: str, default: str = "") -> str:
    # loads streamlit secrets if running in production else load from dotenv
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            val = str(st.secrets[key])
            os.environ[key] = val
            return val
    except Exception:
        pass
    # Use load_env() locally
    return os.getenv(key, default)



MODEL_PATH = "artifacts/model_trainer/best_model.joblib"

def env(k, d=""):
    return st.secrets.get(k, os.getenv(k, d))

@st.cache_resource
def dvc_pull_once():
    # Optional: configure DVC remote creds from secrets (example: DagsHub)
    user = env("DAGSHUB_USERNAME", "")
    token = env("DAGSHUB_TOKEN", "")
    try:
        if user and token:
            subprocess.run(
                ["dvc", "remote", "modify", "dagshub", "auth", "basic"],
                check=True, capture_output=True, text=True
            )
            subprocess.run(
                ["dvc", "remote", "modify", "--local", "dagshub", "user", user],
                check=True, capture_output=True, text=True
            )
            subprocess.run(
                ["dvc", "remote", "modify", "--local", "dagshub", "password", token],
                check=True, capture_output=True, text=True
            )

        res = subprocess.run(["dvc", "pull", "-v"], capture_output=True, text=True)
        return res.returncode, res.stdout, res.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr
