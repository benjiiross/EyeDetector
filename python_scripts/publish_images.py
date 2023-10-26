from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
)
from msrest.authentication import ApiKeyCredentials
from msrest.exceptions import HttpOperationError
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
training_key = os.environ["VISION_TRAINING_KEY"]
project_id = os.environ["VISION_PROJECT_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

print("Importing project...")
project = trainer.get_project(project_id=project_id)

df = pd.read_csv("RFMiD_Training_Labels.csv")

# keep only DR, MH, ODC, TSLN, DN, MYA, ARMD, BRVO, ODP, ODE and Disease_Risk as per the notebook
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
tags = trainer.get_tags(project.id)
base_image_location = os.path.join(os.getcwd(), "images")
image_list = []

for i, row in df.iterrows():
    file_name = f"{row['ID']}.png"

    # take only the tags that are 1
    image_tags = row.drop(["ID"])
    image_tags = image_tags[image_tags == 1]

    # map tags to tag ids since we need to pass tag ids to the API
    tag_ids = []
    for tag in image_tags.index:
        # search for the tag inside tags
        for t in tags:
            if t.name == tag:
                tag_ids.append(t.id)

    # if no disease, add the No_Disease tag
    if len(tag_ids) == 0:
        for t in tags:
            if t.name == "No_Disease":
                tag_ids.append(t.id)

    image_path = os.path.join(base_image_location, file_name)

    # add the image to the list
    with open(image_path, "rb") as image_contents:
        image_list.append(
            ImageFileCreateEntry(
                name=file_name,
                contents=bytearray(image_contents.read()),
                tag_ids=tag_ids,
            )
        )

print("Uploading images...")

# we cannot send all images at once, so we will send them in batches of 64
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

print("Done!")
