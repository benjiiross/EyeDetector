from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv
import os, time, uuid


load_dotenv()

ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
training_key = os.environ["VISION_TRAINING_KEY"]
prediction_key = os.environ["VISION_PREDICTION_KEY"]
prediction_resource_id = os.environ["VISION_PREDICTION_RESOURCE_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": prediction_key}
)
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

print("Importing project...")
project = trainer.get_project(project_id="1f803d80-78d5-4291-b386-89353c0ce67f")

tags = trainer.get_tags(project.id)

for tag in tags:
    trainer.delete_tag(project.id, tag.id)
    print(f"Deleted tag {tag.name}")
    time.sleep(0.25)

tags = [
    "DR",
    "MH",
    "ODC",
    "TSLN",
    "DN",
    "MYA",
    "ARMD",
    "BRVO",
    "ODP",
    "ODE",
    "Disease_Risk",
    "No_Disease",
]

for tag in tags:
    trainer.create_tag(project.id, tag)
    print(f"Created tag {tag}")
    time.sleep(0.25)

print("Done!")
