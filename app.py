from zipfile import ZipFile
import xml.etree.ElementTree as ET 
from PIL import Image, ImageDraw
import json 
import os
import argparse

parser = argparse.ArgumentParser(description = 'Annotation and resize')


parser.add_argument(
    'imagedir', metavar='IMAGEDIR', type=str,
    help='path to the folder with images'
)

parser.add_argument(
    'xmldir', metavar='XMLDIR', type=str,
    help='path to the folder with xml files'
)

parser.add_argument(
    'outputdir', metavar='OUTPUTDIR', type=str,
    help='path to the output folder where the images and the produced json file will be saved'
)

args = parser.parse_args()
# print(args.imagedir)

zip_files = ['images.zip', 'xmldata.zip']
dirs = [os.getcwd() + '\\' + args.imagedir, os.getcwd() + '\\' + args.xmldir]
images_path = dirs[0]
xml_path = dirs[1]

for z, d in zip(zip_files, dirs):
    with ZipFile(z, 'r') as zipObj:
        zipObj.extractall(path=os.getcwd())

images_path = dirs[0]
xml_path = dirs[1]

result_path = os.path.join(os.getcwd() + '\\' + args.outputdir)

if not os.path.isdir(result_path):
    os.makedirs(args.outputdir, exist_ok=True)

images_list = os.listdir(images_path)

for filename in images_list:
    file_dir = os.path.join(images_path + '\\' + filename)

    if os.path.isfile(file_dir):
        img = Image.open(file_dir)
        d, f = os.path.split(file_dir)
        n = f.split('.')[0]
        
        if img.width > 800 or img.height > 450:
            img_resized = img.resize((800, 450))
            img_resized.save(result_path + '\\' + n + '_resized.jpg', 'JPEG', quality=100)
        else:
            img.save(result_path + '\\' + f, 'JPEG', quality=100)
            
xml_list = os.listdir(xml_path)

final = {}
categories = []
images = []
annotations = []

for xmlname in xml_list:
    tree = ET.parse(xml_path + '\\' + xmlname)
    
    theName = xmlname.split('.')[0]
    
    root = tree.getroot()
    sample_annotations = []
    
    for img in root.iter('size'):
        width = int(img.find('width').text)
        height = int(img.find('height').text)
    
    ratio_width = 800/width
    ratio_height = 450/height
        
    for datapoint in root.iter('bndbox'):
        xmin = int(datapoint.find('xmin').text)
        ymin = int(datapoint.find('ymin').text)
        xmax = int(datapoint.find('xmax').text) 
        ymax = int(datapoint.find('ymax').text) 
        
    if width > 800 and height > 450:
        xmin = xmin * ratio_width
        ymin = ymin * ratio_height
        xmax = xmax * ratio_width
        ymax = ymax * ratio_height

    category = {}
    category['id'] = 0
    category['name'] = None
    categories.append(category)

    image = {}
    image['id'] = theName
    
    if width > 800:
        image['width'] = 800
    else:
        image['width'] = width
        
    if height > 450:
        image['height'] = 450
    else:
        image['height'] = height
        
    image['file_name'] = theName + '.jpg'
    images.append(image)

    annotation = {}
    annotation['id'] = theName
    annotation['image_id'] = theName
    annotation['category_id'] = 0
    annotation['bbox'] = [xmin, ymin, xmax - xmin, ymax-ymin]
    annotations.append(annotation)

final['categories'] = categories
final['images'] = images
final['annotation'] = annotations 

with open(result_path + '\\' + 'final_json.json', "w") as final_json:
    json.dump(final, final_json, indent=2)
    
        
