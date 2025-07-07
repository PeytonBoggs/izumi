import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import aiplatform
import json

PROJECT_ID = "nsf-2348130-428843"
LOCATION = "us-west1"
ENDPOINT_ID = "7341109285172019200"
DEDICATED_ENDPOINT = "7341109285172019200.us-west1-34568531463.prediction.vertexai.goog"


def predict_large_language_model_sample(
    project_id: str,
    location: str,
    endpoint_id: str,
    prompt: str,
    dedicated_endpoint: str,
):
    vertexai.init(project=project_id, location=location)

    # Construct the prediction endpoint URL
    endpoint_url = f"https://{dedicated_endpoint}/v1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}:predict"

    # Call the endpoint using aiplatform.PredictionServiceClient
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"} # regional endpoint
    predictor = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Explicitly format the instance
    instance = {"content": prompt}
    instances = [instance]

    # Parameters
    parameters = {
        "temperature": 0.2,
        "maxOutputTokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    # Convert parameters to JSON string
    parameters_json = json.dumps(parameters)

    response = predictor.predict(
        endpoint=endpoint_url,
        instances=instances,
        parameters=parameters,
    )

    print("response:", response)

    for prediction in response.predictions:
        print(prediction)


if __name__ == "__main__":
    prompt_text = "What are the current MLB baseball standings?"
    predict_large_language_model_sample(PROJECT_ID, LOCATION, ENDPOINT_ID, prompt_text, DEDICATED_ENDPOINT)
