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
import os
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

# read in the csv file
df = pd.read_csv("RFMiD_Training_Labels.csv")

# create a list of the image IDs
image_ids = df["ID"].tolist()

# create a list of the tags
tags = df.columns.tolist()
tags.remove("ID")

base_image_location = os.path.join(os.getcwd(), "images")

print("Adding images...")

# go through each image and add it to the project
image_list = []
for image_id in image_ids:
    file_name = f"{str(image_id)}.png"  # Adjust the file extension as needed
    # Assuming your CSV contains the tag IDs in the same order as 'tags' list
    tag_ids = [
        tag_id
        for tag_id, tag_value in zip(tags, df.iloc[image_id - 1].tolist()[1:])
        if tag_value == 1
    ]

    # Construct the full path to the image file
    image_path = os.path.join(base_image_location, file_name)

    # Check if the image file exists before adding it
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_contents:
            image_list.append(
                ImageFileCreateEntry(
                    name=file_name,
                    contents=bytearray(image_contents.read()),
                    tag_ids=tag_ids,
                )
            )
    else:
        print(f"Image file not found: {image_path}")

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


if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)
