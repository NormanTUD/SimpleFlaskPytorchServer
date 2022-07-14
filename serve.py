import sys
import pprint
import json
from flask import Flask, request
from PIL import Image
import torch

def debug (msg):
    print('Debug: ' + pprint.pformat(msg), file=sys.stderr)

app = Flask("Image analyzer")

model = torch.hub.load('ultralytics/yolov5', 'yolov5x')  # or yolov5n - yolov5x6, custom

@app.route('/',  methods = ['GET'])
def index():
    return """
    <h2>Upload a file<h2>
    <form action="/" method="post" enctype="multipart/form-data">
        Select image to upload:
        <input type="file" name="image" id="image">
        <input type="submit" value="Upload Image" name="submit">
    </form>
    """

@app.route('/',  methods = ['POST'])
def reveice_ufo_image():
    debug("Loading image file")

    try:
        img = Image.open(request.files['image'].stream)
        debug("Running model")
        results = model(img)
        debug("Getting outputs")
        return pprint.pformat(results.pandas().xyxy[0])
    except Exception as e:
        debug(e)
        return str(e)


app.run(host='0.0.0.0', port=5000)
