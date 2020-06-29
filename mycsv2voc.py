'''
This script is used for converting SKU110K dataset annotations (in csv)
to the VOC format (in xml).

By BW

Do process the jpgs with `check_jpg()` first!
'''

import os
import numpy as np
import codecs
import pandas as pd
import json
from glob import glob
import shutil
from sklearn.model_selection import train_test_split
from IPython import embed

def converting(csv_file, root_path):
    ''' only 1 function is defined and used here, for converting all the things.  parameters? sorry. '''
    #
    ann_path = root_path + 'Annotations/'
    jpg_path = root_path + 'images/'
    annotations = pd.read_csv(csv_file, header=None) # filename,xmin,ymin,xmax,ymax,label,width,height for SKU110K
    #
    # save the labels and the image dims. into dicts
    total_csv_annotations = {}
    total_csv_size = {}
    for annotation in annotations.values:
        key = annotation[0].split(os.sep)[-1] # to obtain the real filename, ie, to delete the parental folders.
        value = annotation[1:6]
        width, height = annotation[6:]
        if key in total_csv_annotations.keys():
            total_csv_annotations[key].append(value) # append to the list. OK??
        else:
            total_csv_annotations[key] = [value]
            total_csv_size[key] = (width, height)
    # ---
    # write labels into xml
    for filename, label in total_csv_annotations.items():
        if not os.path.exists(jpg_path+filename):
            print('[skipped]:', filename)
            continue
        print('processing', filename)
        width, height = total_csv_size[filename]
        channels = 3
        with codecs.open(ann_path+filename.replace(".jpg",".xml"), "w", "utf-8") as xml:
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'UAV_data' + '</folder>\n')
            xml.write('\t<filename>' + filename + '</filename>\n')
            xml.write('\t<source>\n')
            xml.write('\t\t<database>The UAV autolanding</database>\n')
            xml.write('\t\t<annotation>UAV AutoLanding</annotation>\n')
            xml.write('\t\t<image>flickr</image>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t</source>\n')
            xml.write('\t<owner>\n')
            xml.write('\t\t<flickrid>NULL</flickrid>\n')
            xml.write('\t\t<name>ChaojieZhu</name>\n')
            xml.write('\t</owner>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>'+ str(width) + '</width>\n')
            xml.write('\t\t<height>'+ str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            #
            if isinstance(label, float): ## empty
                xml.write('</annotation>')
                continue
            for labels in label:
                xmin = int(labels[0])
                ymin = int(labels[1])
                xmax = min(labels[2], width-1)
                ymax = min(labels[3], height-1)
                label_ = 'bottle' # labels[-1]
                if (xmax > xmin) and (ymax > ymin):
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>'+label_+'</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>1</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            xml.write('</annotation>')

root_path = '/root/bw/datasets/SKU110K_fixed/'
anno_path = root_path + 'Annotations/'
for csv_file in [anno_path + "annotations_test.csv",
                 anno_path + "annotations_train.csv",
                 anno_path + "annotations_val.csv"]:
    print('\n\nProcessing', csv_file)
    converting(csv_file, root_path)

