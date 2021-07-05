import urllib3
import json
import base64
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt 

def detect_object(img_file, return_image=False):
    with open('etriaikey.txt') as kfile:
        etri_key = kfile.read()
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"

    _, image_type = os.path.splitext(img_file)
    image_type = 'jpg' if image_type == '.jfif' else image_type[1:]
    with open(img_file, 'rb') as file:
        image_contents = base64.b64encode(file.read()).decode("utf8")
    
    request_json = {
        "access_key": etri_key,
        "argument": {
            "type": image_type,
            "file": image_contents
        }
    }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(request_json)
    )
    result = json.loads(response.data)
    '''if not result['return_object']:
        return None'''
    try : 
        obj_list = result['return_object']['data']
    except : 
        return None

    image = Image.open(img_file)
    draw = ImageDraw.Draw(image)
    for obj in obj_list:
        name = obj['class']
        x = int(obj['x'])
        y = int(obj['y'])
        w = int(obj['width'])
        h = int(obj['height'])
        draw.text((x+10,y+10), name, font=ImageFont.truetype('malgun.ttf',20), fill=(255,0,0))
        draw.rectangle(((x,y), (x+w,y+h)), outline=(255,0,0), width=2)
    
    if not return_image:
        plt.figure(figsize=(12,8))
        plt.imshow(image)
        plt.show()
    else:
        img_name = os.path.basename(img_file)
        if not os.path.exists('detected_images'):
            os.mkdir('detected_images')
        filename = f'detected_images/{img_name}'
        image.save(filename)
        return filename