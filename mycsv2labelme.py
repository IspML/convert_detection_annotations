'''
This script is used for converting SKU110K dataset annotations (in csv)
to the LabelMe format (in json).

By BW

Do process the jpgs with `check_jpg()` first!
'''

import os
import cv2
import json
import base64
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
from PIL import Image
from IPython import embed
from labelme import utils


def converting(csv_file, image_path):
    ''' only 1 function is defined and used here, for converting all the things.  parameters? sorry. '''
    #
    annotations = pd.read_csv(csv_file, header=None) # filename,xmin,ymin,xmax,ymax,label,width,height for SKU110K
    #
    total_csv_annotations = {}
    total_csv_size = {}
    for annotation in annotations.values:
        key = annotation[0].split(os.sep)[-1] # to obtain the real filename, ie, to delete the parental folders.
        value = annotation[1:6]
        width, height = annotation[6:]
        if key in total_csv_annotations.keys():
            total_csv_annotations[key].append(value)
        else:
            total_csv_annotations[key] = [value]
            total_csv_size[key] = (width, height)
    # -.-
    # -.-
    for key, value in total_csv_annotations.items():
        width, height = total_csv_size[key]
        #
        path2key = image_path+key
        if not os.path.exists(path2key): continue
        labelme_format = {
            "version": "3.6.16",
            "flags": {},
            "lineColor": [0, 255, 0, 128],
            "fillColor": [255, 0, 0, 128],
            "imagePath": key,
            "imageHeight": height,
            "imageWidth": width,
            "imageData": base64.b64encode(np.asarray(Image.open(path2key))).decode('utf-8'),
            "shapes": [{
                    "label": label[4],
                    "line_color": None,
                    "fill_color": None,
                    "shape_type": "rectangle",
                    "points": [[label[0], label[1]], [min(label[2], width-1), min(label[3], height-1)]]
                } for label in value]
        }
        json.dump(labelme_format, open("%s%s"%(image_path, key.replace(".jpg",".json")), "w"), ensure_ascii=False, indent=2)


root_path = '/root/bw/datasets/SKU110K_fixed/'
image_path = root_path + "images/"
annoo_path = root_path + "Annotations/" # anno, original
for csv_file in [annoo_path + "annotations_test.csv",
                 annoo_path + "annotations_train.csv",
                 annoo_path + "annotations_val.csv"]:
    print('\n\nProcessing', csv_file)
    converting(csv_file, image_path) # new labelme anno_path is the image_path

