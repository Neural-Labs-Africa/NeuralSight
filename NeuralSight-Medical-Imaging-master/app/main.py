from fastapi import FastAPI  # File, Response, UploadFile
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from typing import Any


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="""
## NeuralSight API
### Accessing the main image with bounding boxes drawn
once inference is done 
- use the path in the file response dictionary and concatenate that with the filename.
- then append this to the root url e.g `https://prod.api.neurallabs.africa/runs/1234/file.png`

### Getting the cropped regions.
- fetch the crop from the list of image crops returned.
- concat this with the base url e.g `https://prod.api.neurallabs.africa/runs/2323/crops/Aortic enlargement/1.jpg`
    """,
)
app.mount("/runs", StaticFiles(directory="runs", html=True), name="runs")

# setup cors
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["Redirect"])
def redirect_to_docs() -> Any:
    return RedirectResponse(url="redoc")


app.include_router(api_router, prefix=settings.API_V1_STR)
