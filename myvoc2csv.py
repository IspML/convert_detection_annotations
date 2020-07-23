# coding: utf-8

import os
import pandas as pd
import xml.etree.ElementTree as ET

base_dir = '/root/bw/datasets/'
src_dir  = base_dir + 'shop100_cigcase/'
dst_csv  = src_dir  + 'shop100_annotation.csv'
src_xmls = [fn[:-4] for fn in os.listdir(src_dir) if fn[-4:]=='.xml'] # no suffix!

records  = []
for filename in src_xmls:
    print(f'processing {filename}')
    tree = ET.parse(src_dir + filename+'.xml')
    size = tree.find('size')  # dimension of the figure
    width, height = int(size.find('width').text), int(size.find('height').text)
    objs = tree.findall('object') # bounding boxs
    #
    for obj in objs:
        bndbox = obj.find('bndbox')
        xmin = max(0,      int(bndbox.find('xmin').text)-1)
        xmax = min(width,  int(bndbox.find('xmax').text))
        ymin = max(0,      int(bndbox.find('ymin').text)-1)
        ymax = min(height, int(bndbox.find('ymax').text))
        if xmax-xmin<=0 or ymax-ymin<=0: continue
        # filename,xmin,ymin,xmax,ymax,label,width,height; same with SKU110K::
        record = [filename+'.jpg', xmin, ymin, xmax, ymax, 'object', width, height]
        bbox = [xmin, xmax, ymin, ymax]
        records.append(record)


print(f'saving to {dst_csv}')
df = pd.DataFrame(records)
df.to_csv(dst_csv, header=False, index=False)
