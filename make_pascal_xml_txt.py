import os, random
import cv2 as cv
import numpy as np
import xml.etree.ElementTree as ET

'''
pascalDataset:
   /Annotations    : *.xml
   /JPEGImages     : *.jpg
   /ImageSets/Main : *.txt
'''

def generate_ttv_txt(ds_path, trainval_percent=0.8, train_percent=0.8):
    ''' 生成: ImageSets/Main/*.txt (*: test, train, val, trainval) '''

    xml_path = ds_path+'Annotations/'
    txt_path = ds_path+'ImageSets/Main/'

    total_xml = os.listdir(xml_path)
    num = len(total_xml)
    xlist = np.arange(num)

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

generate_ttv_txt('./lic_0924/')
