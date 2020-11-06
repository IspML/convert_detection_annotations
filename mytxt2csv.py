# coding: utf-8

import pandas as pd
from os import PathLike
from PIL import Image
import os, io, cv2

train_rat  = 0.85
base_dir = '/root/bw/datasets/DOTAv1_val/'
txt_dir  = base_dir + 'labelTxt_v1/'
img_dir  = base_dir + 'images/'
train_csv  = base_dir  + 'train.csv'
val_csv    = base_dir  + 'val.csv'
src_txts = [fn[:-4] for fn in os.listdir(txt_dir) if fn[-4:]=='.txt'] # no suffix!
train_num = len(src_txts) * train_rat # val_num = len() - train_num

def check_jpg(path):
    ''' 检查jpeg(JFIF/Exif)文件是否损坏 '''
    try:
        fileObj = open(path, 'rb')  # 以二进制形式打开
        buf = fileObj.read()
        if not buf.startswith(b'\xff\xd8'):  # 是否以\xff\xd8开头
            print('bad begin')
            return False
        elif buf[6:10] in (b'JFIF', b'Exif'):  # JFIF/Exif的ASCII码
            print('bad format')
            return False
        elif not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):  # 是否以\xff\xd9结尾
            print('bad end')
            return False
        else:
            try:
                Image.open(fileObj).verify()
            except Exception as e:
                print('Image.open:', e)
                return False
    except Exception as e:
        print('file open:', e)
        return False
    return True

def append_csv(txt_fn, img_fn, target):
    with open(txt_fn, 'r', encoding='utf-8-sig') as f:
        for line in f.readlines()[2:]: # ignore the leading lines!
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            line = line.split(' ')[:-2] # remove the tailing labels
            line = ','.join(line)
            if target.lower() == 'train':
                with open(train_csv, 'a', encoding='utf-8-sig') as f:
                    f.write(img_fn + ',' + line + ',object\n')
            else:
                with open(val_csv, 'a', encoding='utf-8-sig') as f:
                    f.write(img_fn + ',' + line + ',object\n')

for i,fname in enumerate(src_txts):
    img_fn = img_dir + fname + '.jpg'
    txt_fn = txt_dir + fname + '.txt'
    # if not check_jpg(img_fn): continue # the txt dosenot have a good jpg
    # ---
    if i <= train_num: # train data set
        append_csv(txt_fn, img_fn, 'train')
    else: # val data set
        append_csv(txt_fn, img_fn, 'val')

print(f'{train_csv} and {val_csv} are created.')
