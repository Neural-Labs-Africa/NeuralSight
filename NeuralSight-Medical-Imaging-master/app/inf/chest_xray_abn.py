"""load vin big chest xray model"""
import os
from app.inf.model import custom

import wandb

model_name = "best.pt"
artifact_dir = "/app/artifacts"
image_dir = os.path.join(os.path.dirname(__file__), "../../", "images")
weights = os.path.join(
    os.path.dirname(__file__),
    "../../",
    artifact_dir,
    f"{os.environ['WANDB_MODEL']+'/'+model_name}",
)
if not os.path.exists(weights):
    wandb.login(key=os.environ["WANDB_KEY"])
    run = wandb.init(project="prod_yolo")
    artifact = run.use_artifact(
        f"droid/yolov5_vinbg/{os.environ['WANDB_MODEL']}", type="model"
    )
    artifact_dir = artifact.download(f"/app/artifacts/{os.environ['WANDB_MODEL']}")


def chest_abn_model():
    return custom(path=weights)
