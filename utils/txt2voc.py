#! /usr/bin/python
# -*- coding:UTF-8 -*-
import os, sys
import glob
from PIL import Image

# VEDAI 图像存储位置
src_img_dir = "../data/images"
# VEDAI 图像的 ground truth 的 txt 文件存放位置
src_txt_dir = "../data/txt"
src_xml_dir = "../data/xml"
src_name_dir = "../data/txt/classes.txt"

if not os.path.exists(src_xml_dir):
    os.makedirs(src_xml_dir)


def get_classes(classes_path):
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


name = get_classes(src_name_dir)

img_Lists = glob.glob(src_img_dir + '/*.jpg')

img_basenames = []
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = []
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)
# print(img_names)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img + '.jpg'))
    width, height = im.size

    # open the crospronding txt file
    if os.path.exists(src_txt_dir + '/' + img + '.txt'):
        gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()
        print(gt)
        # write in xml file
        # os.mknod(src_xml_dir + '/' + img + '.xml')
        xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>VOC2007</folder>\n')
        xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')

        # write the region of image on xml file
        for img_each_label in gt:

            spt = img_each_label.split(' ')  # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
            x = round(float(spt[1]) * width)
            y = round(float(spt[2]) * height)
            w = round(float(spt[3]) * width)
            h = round(float(spt[4]) * height)
            xml_file.write('    <object>\n')
            xml_file.write('        <name>' + str(name[int(spt[0])]) + '</name>\n')
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write('            <xmin>' + str(round(x-1-w/2)) + '</xmin>\n')
            xml_file.write('            <ymin>' + str(round(y-1-h/2)) + '</ymin>\n')
            xml_file.write('            <xmax>' + str(round(x-1+w/2)) + '</xmax>\n')
            xml_file.write('            <ymax>' + str(round(y-1+h/2)) + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            xml_file.write('    </object>\n')

        xml_file.write('</annotation>')

        print(src_txt_dir + '/' + img + '.txt')
    else:
        continue
