from collections import namedtuple
import glob
import os
import re
from io import BytesIO
from pathlib import Path
from typing import Tuple
from app.inf.chest_xray_abn import chest_abn_model
from app.inf.covid import covid_model

from PIL import Image

image_dir = os.path.join(os.path.dirname(__file__), "../../", "images")


def model_selection(covid: bool):
    """Return either covid or the vin big yolo model"""
    if covid:
        return covid_model()
    return chest_abn_model()


def increment_path(path, exist_ok=False, sep="", mkdir=False):
    # Increment file or directory path, i.e. runs/exp --> runs/exp{sep}2, runs/exp{sep}3, ... etc.
    path = Path(path)  # os-agnostic
    if path.exists() and not exist_ok:
        suffix = path.suffix
        path = path.with_suffix("")
        dirs = glob.glob(f"{path}{sep}*")  # similar paths
        matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]  # indices
        n = max(i) + 1 if i else 2  # increment number
        path = Path(f"{path}{sep}{n}{suffix}")  # update path
    if not path.exists() and mkdir:
        path.mkdir(parents=True, exist_ok=True)  # make directory
    return path


def read_imagefile(data) -> Image.Image:
    img_stream = BytesIO(data)
    img = Image.open(img_stream)
    return img


def predict(
    thres: namedtuple, bytes, patient_id: str, covid: bool
) -> Tuple[BytesIO, str]:
    img = read_imagefile(bytes.file.read())
    filename = bytes.filename
    filename_path = os.path.join(f"{image_dir}/{filename}")
    # cv2.imwrite(filename_path, img)
    img.save(f"{filename_path}")
    model = model_selection(covid=covid)
    model.conf = thres.conf_thres
    model.iou = thres.iou_thres
    results = model(filename_path, size=640)
    save_dir = increment_path(f"runs/{patient_id}", sep=".", mkdir=True)
    results.save(save_dir=save_dir)
    results.crop(save=True, save_dir=save_dir)

    return (
        (save_dir, filename),
        list(Path(save_dir).glob("crops/*/*")),
        results.pandas().xyxy[0][["confidence", "name"]].to_json(orient="records"),
    )
