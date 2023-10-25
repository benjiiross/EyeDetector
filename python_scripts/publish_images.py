from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
    Region,
)
from msrest.authentication import ApiKeyCredentials
from dotenv import load_dotenv
import pandas as pd
import os, time
from msrest.exceptions import HttpOperationError


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

df = pd.read_csv("RFMiD_Training_Labels.csv")
# create a list of the image IDs
image_ids = df["ID"].tolist()

# keep only DR, MH, ODC, TSLN, DN, MYA, ARMD, BRVO, ODP, ODE and Disease_Risk
tags = [
    "ID",
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
]

df = df[tags]

print("Adding images...")

base_image_location = os.path.join(os.getcwd(), "images")


# ge tags from azure
tags = trainer.get_tags(project.id)

# go through each image and add it to the project
image_list = []

for i, row in df.iterrows():
    file_name = f"{row['ID']}.png"

    image_tags = row.drop(["ID"])
    image_tags = image_tags[image_tags == 1]

    # map tags to tag ids
    tag_ids = []
    for tag in image_tags.index:
        # search for the tag inside tags
        for t in tags:
            if t.name == tag:
                tag_ids.append(t.id)

    if len(tag_ids) == 0:
        for t in tags:
            if t.name == "No_Disease":
                tag_ids.append(t.id)

    image_path = os.path.join(base_image_location, file_name)

    with open(image_path, "rb") as image_contents:
        image_list.append(
            ImageFileCreateEntry(
                name=file_name,
                contents=bytearray(image_contents.read()),
                tag_ids=tag_ids,
            )
        )

print("Uploading images...")
for i in range(0, len(image_list), 64):
    print(f"Uploading batch {i // 64 + 1}...")
    batch = image_list[i : i + 64]
    try:
        upload_result = trainer.create_images_from_files(
            project.id, ImageFileCreateBatch(images=batch)
        )
    except HttpOperationError as e:
        print(e.response.text)
        exit(-1)

print("Training...")
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)
