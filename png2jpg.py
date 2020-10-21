import os
import cv2 as cv

def png2jpg(img_dir):
    ''' all .png in `img_dir` will be converted to .jpg '''
    files = os.listdir(img_dir)
    for img_file in files:
        if img_file[-4:].lower() != '.png': continue
        image_path = os.path.join(img_dir, img_file)
        new_image_path = image_path[:-4]+'.jpg'
        if os.path.isfile(image_path):
            image = cv.imread(image_path)
            cv.imwrite(new_image_path, image, [cv.IMWRITE_JPEG_QUALITY, 100])
            print(f"processed image : {new_image_path}")

png2jpg('./JPEGImages/')
