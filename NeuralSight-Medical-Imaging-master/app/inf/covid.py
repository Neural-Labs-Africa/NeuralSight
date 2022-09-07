"""Load covid yolo model"""
import os
import wandb
from app.inf.model import custom

model_name = "best.pt"
artifact_dir = "/app/artifacts"
weights = os.path.join(artifact_dir, f'{os.environ["COVID_MODEL"]}', model_name)
print(weights)
if not os.path.exists(weights):
    wandb.login(key=os.environ["WANDB_KEY"])
    run = wandb.init(project="covid", entity="mrdvince")
    artifact = run.use_artifact(
        f"mrdvince/covid/{os.environ['COVID_MODEL']}", type="model"
    )
    artifact_dir = artifact.download(f"/app/artifacts/{os.environ['COVID_MODEL']}")


def covid_model():
    return custom(path=weights)
