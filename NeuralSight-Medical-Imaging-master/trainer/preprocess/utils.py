import operator
import os
import random
from collections import Counter

import cv2
import numpy as np
import pandas as pd
import pydicom

random.seed(2016)
np.random.seed(2016)

ROOT_PATH = "/home/vinc3/data/"
INPUT_PATH = ROOT_PATH
OUTPUT_PATH = ROOT_PATH + "modified_data_folder/"
if not os.path.isdir(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
MODELS_PATH = ROOT_PATH + "models_inference/"
if not os.path.isdir(MODELS_PATH):
    os.mkdir(MODELS_PATH)
CACHE_PATH = ROOT_PATH + "cache_folder/"
if not os.path.isdir(CACHE_PATH):
    os.mkdir(CACHE_PATH)
FEATURES_PATH = ROOT_PATH + "features_folder/"
if not os.path.isdir(FEATURES_PATH):
    os.mkdir(FEATURES_PATH)
HISTORY_FOLDER_PATH = MODELS_PATH + "history_folder/"
if not os.path.isdir(HISTORY_FOLDER_PATH):
    os.mkdir(HISTORY_FOLDER_PATH)
SUBM_PATH = ROOT_PATH + "subm_folder/"
if not os.path.isdir(SUBM_PATH):
    os.mkdir(SUBM_PATH)


def show_image(im, name="image"):
    cv2.imshow(name, im.astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_image_rgb(im, name="image"):
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    cv2.imshow(name, im.astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_image_16bit(im, name="image"):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_resized_image_16bit(P, w=1000, h=1000):
    res = cv2.resize(P, (w, h), interpolation=cv2.INTER_CUBIC)
    show_image_16bit(res)


def show_resized_image(P, w=1000, h=1000):
    res = cv2.resize(P.astype(np.uint8), (w, h), interpolation=cv2.INTER_CUBIC)
    show_image(res)


def sort_dict_by_values(a, reverse=True):
    sorted_x = sorted(a.items(), key=operator.itemgetter(1), reverse=reverse)
    return sorted_x


def value_counts_for_list(lst):
    a = dict(Counter(lst))
    a = sort_dict_by_values(a, True)
    return a


def save_history_figure(history, path, columns=("acc", "val_acc")):
    import matplotlib.pyplot as plt

    s = pd.DataFrame(history.history)
    plt.plot(s[list(columns)])
    plt.savefig(path)
    plt.close()


def read_single_image(path):
    try:
        img = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
    except Exception:
        print("Fail")
        return np.zeros((512, 512, 3), dtype=np.uint8)

    if len(img.shape) == 2:
        img = np.stack([img, img, img], axis=-1)

    if img.shape[2] == 2:
        img = img[:, :, :1]

    if img.shape[2] == 1:
        img = np.concatenate((img, img, img), axis=2)

    if img.shape[2] > 3:
        img = img[:, :, :3]

    return img


def read_image_bgr_fast(path):
    img2 = read_single_image(path)
    img2 = img2[:, :, ::-1]
    return img2


def dice_metric_score(real, pred):
    assert real.shape == pred.shape
    r = real.astype(np.bool)
    p = (pred > 0.5).astype(np.bool)
    r_sum = r.sum()
    p_sum = p.sum()
    if r_sum == 0 and p_sum == 0:
        return 1.0
    if r_sum == 0:
        return 0.0
    if p_sum == 0:
        return 0.0

    intersection = np.logical_and(r, p).sum()
    return 2 * intersection / (r_sum + p_sum)


def normalize_array(cube, new_max, new_min):
    """Rescale an arrary linearly."""
    minimum, maximum = np.min(cube), np.max(cube)
    if maximum - minimum != 0:
        m = (new_max - new_min) / (maximum - minimum)
        b = new_min - m * minimum
        cube = m * cube + b
    return cube


def get_dicom_as_dict(dicom):
    res = dict()
    keys = list(dicom.keys())
    for k in keys:
        nm = dicom[k].name
        if nm == "Pixel Data":
            continue
        val = dicom[k].value
        res[nm] = val
    return res


def get_color_hsv(cur_class, total_classes):
    step = 180 / total_classes
    i = cur_class
    H = i * step
    S = [200, 225, 255]
    V = [200, 225, 255]
    color = np.array([H, S[i % len(S)], V[(i + 1) % len(V)]], dtype=np.uint8)
    color = color.reshape([1, 1, 3])
    color = cv2.cvtColor(color, cv2.COLOR_HSV2RGB)
    color = tuple(int(i) for i in color.ravel())
    return color


def get_color(class_id):
    if class_id > 14 or class_id < 0:
        print("Error!")
        exit()
    return get_color_hsv(class_id, 14)


def read_xray(
    path, voi_lut=True, fix_monochrome=True, use_8bit=True, rescale_times=None
):
    from pydicom.pixel_data_handlers.util import apply_voi_lut

    dicom = pydicom.read_file(path)

    # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array

    data = data.astype(np.float64)
    if rescale_times:
        data = cv2.resize(
            data,
            (data.shape[1] // rescale_times, data.shape[0] // rescale_times),
            interpolation=cv2.INTER_CUBIC,
        )

    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data

    data = data - np.min(data)
    data = data / np.max(data)

    if use_8bit is True:
        data = (data * 255).astype(np.uint8)
    else:
        data = (data * 65535).astype(np.uint16)

    return data


def get_classes_array():
    train = pd.read_csv(INPUT_PATH + "train.csv")
    res = dict()
    for index, row in train.iterrows():
        class_id = row["class_id"]
        class_name = row["class_name"]
        if class_id not in res:
            res[class_id] = class_name
        else:
            if res[class_id] != class_name:
                print("Error")
    CLASSES = []
    for i in range(15):
        CLASSES.append(res[i])
    return CLASSES


def get_train_test_image_sizes():
    sizes = dict()
    sizes_train = pd.read_csv(OUTPUT_PATH + "image_width_height_train.csv")
    sizes_test = pd.read_csv(OUTPUT_PATH + "image_width_height_test.csv")
    # sizes_external = pd.read_csv(OUTPUT_PATH + 'image_width_height_external.csv')
    sizes_df = pd.concat((sizes_train, sizes_test), axis=0)
    for index, row in sizes_df.iterrows():
        sizes[row["image_id"]] = (row["height"], row["width"])
    return sizes


def check_class_distribution_in_subm(subm_path):
    train = pd.read_csv(subm_path)
    img_ids = train["image_id"].unique()  # noqa
    preds = train["PredictionString"].values
    res = dict()
    for i in range(len(preds)):
        p = preds[i]
        arr = p.split(" ")
        for j in range(0, len(arr), 6):
            if arr[j] not in res:
                res[arr[j]] = 0
            res[arr[j]] += 1
    print(res)


def dice(im1, im2, empty_score=1.0):
    im1 = im1.astype(np.bool)
    im2 = im2.astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_score

    intersection = np.logical_and(im1, im2)
    return 2.0 * intersection.sum() / im_sum
