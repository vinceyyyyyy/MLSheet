import json
import os

import dill
import pandas as pd

from interfaces import Model


def lambda_handler(event: dict, _) -> dict:
    """Lambda handler for the cloud_function function.
    This function returns a result, along with all columns that are not specified in input_cols.

    :param event: API Gateway Lambda Proxy Input Format: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    :param _: Lambda Context runtime methods and attributes: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :return: API Gateway Lambda Proxy Output Format: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    request_body = json.loads(event["body"])  # request_body as {column_1: [value1, value2, ...], column_2: [value1, value2, ...], ...}
    df = pd.DataFrame(request_body)

    # locate model file
    model_path = f"{os.getenv('FUNCTION_DIR')}/model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # Load the model
    with open(model_path, "rb") as f:
        try:
            model = dill.load(f)
            print("Model loaded")
        except Exception as e:
            raise RuntimeError(f"Loading model failed: {e}")

    # Check if implementation is correct
    if not isinstance(model, Model):
        raise RuntimeError("Model object is not the right type")

    # Run prediction
    prediction_result = model.run_predict(df[model.input_columns])

    # if only one column is returned, name it as result
    prediction_frame = pd.DataFrame(prediction_result)
    if prediction_frame.shape[1] == 1:
        prediction_frame.columns = ["result"]

    total_result = pd.concat([df.drop(columns=model.input_columns), prediction_frame], axis=1)

    # Attach unused columns to result. Most likely those are used as id.
    response_body = total_result.to_dict(orient="list") # response_body as {column_1: [value1, value2, ...], column_2: [value1, value2, ...], ...}

    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
