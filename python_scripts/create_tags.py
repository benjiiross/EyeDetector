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
project_name = uuid.uuid4()
project = trainer.get_project(project_id="1f803d80-78d5-4291-b386-89353c0ce67f")

tags = trainer.get_tags(project.id)

for tag in tags:
    trainer.delete_tag(project.id, tag.id)
    print(f"Deleted tag {tag.name}")
    time.sleep(0.25)

Disease_Risk_tag = trainer.create_tag(project.id, "Disease_Risk")
DR_tag = trainer.create_tag(project.id, "DR")
ARMD_tag = trainer.create_tag(project.id, "ARMD")
MH_tag = trainer.create_tag(project.id, "MH")
DN_tag = trainer.create_tag(project.id, "DN")
MYA_tag = trainer.create_tag(project.id, "MYA")
BRVO_tag = trainer.create_tag(project.id, "BRVO")
TSLN_tag = trainer.create_tag(project.id, "TSLN")
ERM_tag = trainer.create_tag(project.id, "ERM")
print("Added tags 1/6")
time.sleep(1)

LS_tag = trainer.create_tag(project.id, "LS")
MS_tag = trainer.create_tag(project.id, "MS")
CSR_tag = trainer.create_tag(project.id, "CSR")
ODC_tag = trainer.create_tag(project.id, "ODC")
CRVO_tag = trainer.create_tag(project.id, "CRVO")
TV_tag = trainer.create_tag(project.id, "TV")
AH_tag = trainer.create_tag(project.id, "AH")
print("Added tags 2/6")
time.sleep(1)

ODP_tag = trainer.create_tag(project.id, "ODP")
ODE_tag = trainer.create_tag(project.id, "ODE")
ST_tag = trainer.create_tag(project.id, "ST")
AION_tag = trainer.create_tag(project.id, "AION")
PT_tag = trainer.create_tag(project.id, "PT")
RT_tag = trainer.create_tag(project.id, "RT")
RS_tag = trainer.create_tag(project.id, "RS")
print("Added tags 3/6")
time.sleep(1)

CRS_tag = trainer.create_tag(project.id, "CRS")
EDN_tag = trainer.create_tag(project.id, "EDN")
RPEC_tag = trainer.create_tag(project.id, "RPEC")
MHL_tag = trainer.create_tag(project.id, "MHL")
RP_tag = trainer.create_tag(project.id, "RP")
CWS_tag = trainer.create_tag(project.id, "CWS")
CB_tag = trainer.create_tag(project.id, "CB")
print("Added tags 4/6")
time.sleep(1)

ODPM_tag = trainer.create_tag(project.id, "ODPM")
PRH_tag = trainer.create_tag(project.id, "PRH")
MNF_tag = trainer.create_tag(project.id, "MNF")
HR_tag = trainer.create_tag(project.id, "HR")
CRAO_tag = trainer.create_tag(project.id, "CRAO")
TD_tag = trainer.create_tag(project.id, "TD")
CME_tag = trainer.create_tag(project.id, "CME")
print("Added tags 5/6")
time.sleep(1)

PTCR_tag = trainer.create_tag(project.id, "PTCR")
CF_tag = trainer.create_tag(project.id, "CF")
VH_tag = trainer.create_tag(project.id, "VH")
MCA_tag = trainer.create_tag(project.id, "MCA")
VS_tag = trainer.create_tag(project.id, "VS")
BRAO_tag = trainer.create_tag(project.id, "BRAO")
PLQ_tag = trainer.create_tag(project.id, "PLQ")
time.sleep(1)

HPED_tag = trainer.create_tag(project.id, "HPED")
CL_tag = trainer.create_tag(project.id, "CL")

print("Tags created")
