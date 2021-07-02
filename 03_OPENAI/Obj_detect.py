from glob import glob
import os
import matplotlib.pyplot as plt

import urllib3
import json
import base64

from PIL import Image, ImageDraw, ImageFont

def detect_image(file_path,apikey_file):
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"

    with open (apikey_file) as kfile:
        etri_key = kfile.read()

    for img_file in glob(file_path):
        _, image_type = os.path.splitext(img_file)
        image_type = 'jpg' if image_type == '.jfif' else image_type[1:]
        with open(img_file,'rb') as file:
            imageContents = base64.b64encode(file.read()).decode("utf8")

        request_json = {"access_key": etri_key,"argument": {"type": image_type,"file": imageContents}}
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json))
        result = json.loads(response.data)

        image = Image.open(img_file)
        obj_list = result['return_object']['data']
        draw = ImageDraw.Draw(image)

        for obj in obj_list:
            name = obj['class']
            x = int(obj['x'])           
            y = int(obj['y'])
            w = int(obj['width'])
            h = int(obj['height'])
            draw.text((x,y),name, font=ImageFont.truetype('malgun.ttf',10),fill=(255,0,0))  
            draw.rectangle(((x,y),(x+w+10,y+h+10)), outline = (255,0,0), width=2)

        plt.imshow(image)
        plt.show()
