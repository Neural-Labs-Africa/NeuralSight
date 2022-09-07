import wandb
run = wandb.init()
artifact = run.use_artifact('mrdvince/covid/run_2ba5zc6f_model:v2', type='model')
artifact_dir = artifact.download()