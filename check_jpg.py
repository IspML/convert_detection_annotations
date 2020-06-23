# 从本地判断图片是否损坏
# forked from http://blog.csdn.net/zhuhuahong/java/article/details/82464552

from os import PathLike
from PIL import Image
import os, io, cv2

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

!mogrify -set comment 'Image rewritten with ImageMagick' *.jpg
# according to stackoverflow...

for root, dirs, files in os.walk(r"/root/bw/datasets/SKU110K_fixed/images"):
    for file in files:
        if file[-4:].lower() not in ['.jpg', '.jpeg']: continue
        file_path = os.path.join(root,file)
        print(file_path)
        flag = check_jpg(file_path)
        if flag:
            img = cv2.imread(file_path) # no need
            cv2.imwrite(file_path, img) # ??? ??!
        else:
            print("remove")
            os.remove(file_path)
        print()
