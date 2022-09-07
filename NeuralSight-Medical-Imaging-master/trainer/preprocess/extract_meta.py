import glob
import os

import cv2
import pandas as pd
import pydicom
from tqdm.auto import tqdm

from utils import INPUT_PATH, OUTPUT_PATH, get_dicom_as_dict


def extract_meta(type="train"):
    files = glob.glob(INPUT_PATH + "{}/*.dicom".format(type))
    dt = []
    for f in tqdm(files, total=len(files)):
        id = os.path.basename(f)[:-6]
        dicom = pydicom.dcmread(f)
        dict1 = get_dicom_as_dict(dicom)
        dict1["image_id"] = id
        dt.append(dict1)
    s = pd.DataFrame(dt)
    s.to_csv(OUTPUT_PATH + "dicom_properties_{}.csv".format(type), index=False)

    print(s.describe())


def extract_width_height(type="train"):
    files = glob.glob(INPUT_PATH + "{}/*.dicom".format(type))
    out = open(OUTPUT_PATH + "image_width_height_{}.csv".format(type), "w")
    out.write("image_id,width,height\n")
    for f in tqdm(files, total=len(files)):
        dicom = pydicom.dcmread(f)
        image = dicom.pixel_array
        height, width = image.shape
        out.write("{},{},{}\n".format(os.path.basename(f)[:-6], width, height))
    out.close()


def extract_width_height_external(type="external"):
    files = glob.glob(INPUT_PATH + "nih/*.png".format(type))  # noqa
    out = open(OUTPUT_PATH + "image_width_height_{}.csv".format(type), "w")
    out.write("image_id,width,height\n")
    for f in tqdm(files, total=len(files)):
        image = cv2.imread(f, 0)
        height, width = image.shape
        out.write("{},{},{}\n".format(os.path.basename(f)[:-4], width, height))
    out.close()


if __name__ == "__main__":
    extract_meta("train")
    extract_meta("test")
    extract_width_height("train")
    extract_width_height("test")
