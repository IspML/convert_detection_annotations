'''
This script is used for converting SKU110K dataset annotations (in csv)
to Pascal VOC format (in xml).

By BW

Do process the jpgs with `check_jpg()` first!


myVOC:
  annotation.csv  # to be converted
  /Annotations    : *.xml
  /JPEGImages     : *.jpg
  /ImageSets/Main : *.txt
'''

import os, random
import numpy as np
import codecs
import pandas as pd
import json
from glob import glob
import shutil
import subprocess as sub
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from IPython import embed

ann_subpath = 'Annotations/'
xml_subpath = ann_subpath
txt_subpath = 'ImageSets/Main/'
jpg_subpath = 'JPEGImages/'

def generate_ttv_txt(root_path, trainval_percent=0.85, train_percent=0.85):
    ''' 生成: ImageSets/Main/*.txt (*: test, train, val, trainval) '''
    xml_path = root_path+xml_subpath
    txt_path = root_path+txt_subpath
    total_xml = os.listdir(xml_path)
    num = len(total_xml)
    xlist = np.arange(num).tolist()

    tv = np.int(num * trainval_percent)
    tr = np.int(tv * train_percent)
    trainval = random.sample(xlist, tv)
    train = random.sample(trainval, tr)
    print("train and val size", tv)
    print("train size", tr)

    ftrainval = open(os.path.join(txt_path, 'trainval.txt'), 'w')
    ftest = open(os.path.join(txt_path, 'test.txt'), 'w')
    ftrain = open(os.path.join(txt_path, 'train.txt'), 'w')
    fval = open(os.path.join(txt_path, 'val.txt'), 'w')

    for i in xlist:
        name = total_xml[i][:-4] + '\n' # 不加扩展名!
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()


def converting(csv_file, root_path, skiprows=[0], sep='/'): # os.sep
    ''' only 1 function is defined and used here, for converting all the things.  parameters? sorry. '''
    jpg_path = root_path + jpg_subpath
    ann_path = root_path + ann_subpath
    annotations = pd.read_csv(csv_file, skiprows=skiprows, header=None) # filename,xmin,ymin,xmax,ymax,label,width,height
    #
    # save the labels and the image dims. into dicts
    total_csv_annotations = {}
    total_csv_size = {}
    for annotation in annotations.values:
        key = annotation[0].split(sep)[-1] # to obtain the real filename, without the parental folders
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
        fname = filename.split(sep)[-1]
        if not os.path.exists(jpg_path+fname):
            print('[skipped]:', fname)
            continue
        print('processing', fname)
        width, height = total_csv_size[fname]
        channels = 3
        with codecs.open(ann_path+fname.replace(".jpg",".xml"), "w", "utf-8") as xml:
            xml.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xml.write('<annotation>\n')
            xml.write('\t<folder>' + 'myVOC' + '</folder>\n')
            xml.write('\t<filename>' + fname + '</filename>\n')
            xml.write('\t<size>\n')
            xml.write('\t\t<width>'+ str(width) + '</width>\n')
            xml.write('\t\t<height>'+ str(height) + '</height>\n')
            xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
            xml.write('\t</size>\n')
            xml.write('\t\t<segmented>0</segmented>\n')
            #
            if isinstance(label, float): ## empty, no objs
                xml.write('</annotation>')
                continue
            for labels in label:
                xmin = max(0, int(labels[0]))
                ymin = max(0, int(labels[1]))
                xmax = max(0, min(labels[2], width-1))
                ymax = max(0, min(labels[3], height-1))
                label_ = labels[-1]
                if (xmax > xmin) and (ymax > ymin):
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>'+label_+'</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    xml.write('\t\t<truncated>0</truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
            xml.write('</annotation>')


root_path = './'
csv_file = root_path+"annotation.csv"
print("Please copy imgs (jpegs) to: ", root_path + jpg_subpath)
print("Annotation (xmls) will be in: ", root_path + ann_subpath)

#sub.call(f'mkdir -p {root_path}+{jpg_subpath}')
#sub.call(f'mkdir -p {root_path}+{ann_subpath}')
#sub.call(f'mkdir -p {root_path}+{txt_subpath}')
## ^^^ not works on windows. TODO: update it! (manually for now)

print('\n\nProcessing', csv_file)
converting(csv_file, root_path)
print()
generate_ttv_txt(root_path)
print('done')
