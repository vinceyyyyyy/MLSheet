import json
import os
import pickle

import pandas as pd

from utils import PredictionRequestBody, PredictionResponseBody, Model


def lambda_handler(event: dict, _) -> dict:
    """Lambda handler for the predict function.
    This function returns a result, along with all columns that are not specified in input_cols.

    :param event: API Gateway Lambda Proxy Input Format: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    :param _: Lambda Context runtime methods and attributes: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :return: API Gateway Lambda Proxy Output Format: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    request_body: PredictionRequestBody = json.loads(event["body"])
    df = pd.DataFrame(request_body["Values"], columns=request_body["ColumnNames"])

    # locate model file
    model_path = f"{os.getenv('FUNCTION_DIR')}/model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

     # Load the model
    with open(model_path, "rb") as f:
        try:
            model: Model = pickle.load(f)
            print("Model loaded")
        except Exception as e:
            raise RuntimeError(f"Loading model failed: {e}")

    # Check if implementation is correct
    if not isinstance(model, Model):
        raise RuntimeError("Model object is not the right type")

    # Run prediction
    prediction_result = model.predict(df[model.input_columns])

    # if only one series is returned, convert it to a dataframe with name as result
    if isinstance(prediction_result, pd.Series):
        prediction_result = prediction_result.to_frame("result")

    total_result = pd.concat([df.drop(columns=model.input_columns), prediction_result], axis=1)

    # Attach unused columns to result. Most likely those are used as id.
    result_body: PredictionResponseBody = total_result.to_dict(orient="list")

    return {
        "statusCode": 200,
        "body": json.dumps(result_body)
    }

