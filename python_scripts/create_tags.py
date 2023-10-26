from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv
import os, time

load_dotenv()

ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
training_key = os.environ["VISION_TRAINING_KEY"]
project_id = os.environ["VISION_PROJECT_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

print("Importing project...")
project = trainer.get_project(project_id=project_id)

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
