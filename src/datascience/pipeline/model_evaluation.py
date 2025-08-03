from src.datascience.config.configuration import ConfigurationManager
from src.datascience import logger
from src.datascience.components.model_evaluation import ModelEvaluation

STAGE_NAME = "Model Evaluation Stage"


class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def run(self):
        try: 
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_to_mlflow()
            
        except Exception as e:
            raise e
        
if __name__ == '__main__':
    try:
        logger.info(f"----- Stage {STAGE_NAME} started -----")
        obj = ModelEvaluationPipeline()
        obj.run()
        logger.info(f"----- Stage {STAGE_NAME} completed ----- \n\n")
    except Exception as e:
        logger.exception(e)
        raise e 

