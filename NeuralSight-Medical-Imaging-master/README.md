# Nsight

Revolutinizing health care using deeplearning.

## Running locally

1. Clone the repo

### Build the container

> Here am using --platform linux/amd64 because am on m1 and need docker to use the x86_64 image for package installation, this is not necessary

2. docker build --platform linux/amd64 -f Dockerfile . -t nsight

Run the uvicorn server,
the project needs variables set on the cli, these can be passed into the container in different methods from using ".env" file etc

here using an example of passing `PROJECT_NAME=$PROJECT_NAME` environment variable.

3. docker run -e PROJECT_NAME=$PROJECT_NAME --rm nsight /bin/bash -c "uvicorn app.main:app --host 0.0.0.0 --port 80"

## Env variables needed (might have forgotten some just check the error messages)

for the passwords you can use anything if using docker compose it will just spin up containers using the passwords given.

> see # Alternatively (probably more easier) section below

```
STACK_NAME=<STACK_NAME >
PROJECT_NAME=<PROJECT_ >
DOMAIN=<DOMAIN >
SERVER_HOST=<SERVER_HOST >
SERVER_NAME=<SERVER_ >

# POSTGRES
POSTGRES_SERVER=<POSTGRES_SERVER >
POSTGRES_USER=<POSTGRES_USER >
POSTGRES_PASSWORD=<POSTGRES_PASSWORD >
POSTGRES_DB=<POSTGRES_DB >

# CORS
BACKEND_CORS_ORIGINS=["http://localhost",<other domains>]

# USER STUFF
SECRET_KEY=<SECRET_KEY >
FIRST_SUPERUSER=<FIRST_SUPERUSER >
FIRST_SUPERUSER_PASSWORD=<FIRST_SUPERUSER_PASSWORD >

# EMAIL STUFF
SMTP_TLS=<SMTP_TLS >
SMTP_PORT=<SMTP_PORT >
SMTP_HOST=<SMTP_HOST >
SMTP_USER=<SMTP_USER >
SMTP_PASSWORD=<SMTP_PASSWORD >
EMAILS_FROM_EMAIL=<EMAILS_FROM_EMAIL >

# PGADMIN
PGADMIN_LISTEN_PORT=<PGADMIN_LISTEN_PORT >
PGADMIN_DEFAULT_EMAIL=<PGADMIN_DEFAULT_EMAIL >
PGADMIN_DEFAULT_PASSWORD=<PGADMIN_DEFAULT_PASSWORD >
USERS_OPEN_REGISTRATION=<USERS_OPEN_REGISTRATION, True or False>
SENTRY_DSN=<SENTRY_DSN optinal>

# WANDB
WANDB_MODEL=<WANDB_MODEL >
MODEL_NAME=<MODEL_ >
ARTIFACT_DIR =<MODEL_ >
IMAGE_DIR=<IMAGE_DIR >
PROJECT=<PROJECT>
WANDB_KEY=<WANDB_KEY >
ENTITY=<ENTITY >
RUNS=<RUNS >
```

# Alternatively (probably more easier)

Switch to the v0.1 tag. (https://github.com/mrdvince/nsight/tree/v0.1)

The v0.1 has docker compose files included.

Running it should be along the lines of 'docker compose up'

Should ideally build all the containers required for the running the stack

> environment variables above are still required to be set
