# End-to-end Machine Learning and Data Science Project 

### Workflows-ML Pipeline:

The core stages of the pipeline are:

    1. Data Ingestion – Load raw data from source.

    2. Data Validation – Check schema, types, missing values, and integrity.

    3. Data Transformation – Feature engineering, encoding, scaling.

    4. Model Training – Train the model using configurable algorithms and parameters.

    5. Model Evaluation – Evaluate model performance and compare with baseline.

## Workflows



### For each of the above we have to do the following

    1. Update config.yaml – Central configuration for data paths, model directories, etc.

    2. Update schema.yaml – Define expected data schema and column types.

    3. Update params.yaml – Set hyperparameters for training and evaluation.

    4. Define entity classes – Use Pydantic or data classes to structure input/output.

    5. Configure the Configuration Manager in src/config – Load and parse YAML configurations.

    6. Implement or update components – Logic for ingestion, transformation, training, etc.

    7. Build/update the pipeline – Chain components together in a clean workflow.

    8. Update main.py – Entry point for triggering the pipeline.