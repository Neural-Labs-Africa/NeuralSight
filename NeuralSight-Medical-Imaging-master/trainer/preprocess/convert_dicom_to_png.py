import glob
import os

import cv2
from tqdm.auto import tqdm

from utils import INPUT_PATH, read_xray


def convert_dicom_to_png(type="train", use_8bit=False, div=1):
    files = glob.glob(INPUT_PATH + "{}/*.dicom".format(type))
    if use_8bit is False:
        if div != 1:
            out_folder = INPUT_PATH + "{}_png_16bit_div_{}/".format(type, div)
        else:
            out_folder = INPUT_PATH + "{}_png_16bit/".format(type)
    else:
        if div != 1:
            out_folder = INPUT_PATH + "{}_png_div_{}/".format(type, div)
        else:
            out_folder = INPUT_PATH + "{}_png/".format(type)

    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)
    for f in tqdm(files, total=len(files)):
        id = os.path.basename(f)[:-6]
        out_path = out_folder + "{}.png".format(id)
        if os.path.isfile(out_path):
            continue
        img = read_xray(f, use_8bit=use_8bit, rescale_times=div)
        cv2.imwrite(out_folder + "{}.png".format(id), img)


if __name__ == "__main__":

    convert_dicom_to_png("train", use_8bit=True, div=2)
    convert_dicom_to_png("test", use_8bit=True, div=2)
