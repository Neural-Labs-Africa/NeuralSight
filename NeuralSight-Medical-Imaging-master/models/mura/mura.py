import wandb
run = wandb.init()
artifact = run.use_artifact('droid/mura/model_best.pth:v0', type='dataset')
artifact_dir = artifact.download()