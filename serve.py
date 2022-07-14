import sys
import pprint
import json
from flask import Flask, request
from PIL import Image
import torch

app = Flask("Image analyzer")

model = torch.hub.load('ultralytics/yolov5', 'yolov5x')  # or yolov5n - yolov5x6, custom

@app.route('/',  methods = ['POST'])
def index():
    img = Image.open(request.files['image'].stream)
    results = model(img)
    return pprint.pformat(results.pandas().xyxy[0])

app.run(host='0.0.0.0', port=5000)
