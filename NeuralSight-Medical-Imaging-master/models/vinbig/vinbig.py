import wandb
run = wandb.init()
artifact = run.use_artifact('droid/yolov5_vinbg/run_1jbt575j_model:v7', type='model')
artifact_dir = artifact.download()