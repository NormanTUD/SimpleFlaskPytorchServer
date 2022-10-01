import sys
import uuid
import pprint
import json
from flask import Flask, request
from PIL import Image
import torch

import re

class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)

def dier (msg):
    pprint.pprint(msg)

def debug (msg):
    print('Debug: ' + pprint.pformat(msg), file=sys.stderr)

app = Flask("Image analyzer")

#model = torch.hub.load('ultralytics/yolov5', 'yolov5x')  # or yolov5n - yolov5x6, custom
# git clone --depth 1 https://github.com/ultralytics/yolov5.git
model = torch.hub.load("yolov5", 'custom', path="/home/norman/test/randomtest_7954/yolov5/runs/train/exp5/weights/best.pt", source='local')

@app.route('/',  methods = ['GET'])
def index():
    return """
    <h2>Upload a file<h2>
    <form action="/annotarious" method="post" enctype="multipart/form-data">
        Select image to upload:
        <input type="file" name="image" id="image">
        <input type="submit" value="Upload Image" name="submit">
    </form>
    """

@app.route('/annotarious',  methods = ['POST'])
def reveice_ufo_image_annotarious():
    debug("Loading image file")

    try:
        img = Image.open(request.files['image'].stream)
        debug("Running model")
        results = model(img)
        debug("Getting outputs")
        #return pprint.pformat(results.pandas().xywh[0])

        r = results.pandas().xywh[0]

        part_strings = []

        i = 0
        for line in str(r).splitlines():
            if i != 0:
                m = REMatcher(line)

                # 0  519.995667  77.812920  77.668060  72.964615    0.609547      0  stern
                if m.match(r"^\s*(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(.*)\s*$"):
                    nr = int(m.group(1))
                    xcenter = float(m.group(2))
                    ycenter = float(m.group(3))
                    width = float(m.group(4))
                    height = float(m.group(5))
                    confidence = float(m.group(6))
                    classnr = float(m.group(7))
                    name = m.group(8)

                    item_uuid = str(uuid.uuid4())

                    ps = """ {
                        "type": "Annotation",
                        "body": [
                          {
                            "type": "TextualBody",
                            "value": "%s",
                            "purpose": "tagging"
                          }
                        ],
                        "target": {
                          "source": "ai",
                          "selector": {
                            "type": "FragmentSelector",
                            "conformsTo": "http://www.w3.org/TR/media-frags/",
                            "value": "xywh=pixel:%d,%d,%d,%d"
                          }
                        },
                        "@context": "http://www.w3.org/ns/anno.jsonld",
                        "id": "#%s"
                      }
                    """ % (name, round(xcenter), round(ycenter), round(width), round(height), item_uuid)
                    part_strings.append(ps)
                else:
                    print("Line does not match regex:")
                    print(line)

            i = i + 1


        return "[" + ", ".join(part_strings) + "]"

        return """
[
  {
    "type": "Annotation",
    "body": [
      {
        "type": "TextualBody",
        "value": "Vogel",
        "purpose": "tagging"
      }
    ],
    "target": {
      "source": "https://www.ufo-ki.de/annotate/images/156de3674a5c1ed69fb4652b6c5c2c5f.jpg",
      "selector": {
        "type": "FragmentSelector",
        "conformsTo": "http://www.w3.org/TR/media-frags/",
        "value": "xywh=pixel:124,233,59,43"
      }
    },
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "id": "#019a73b3-16ff-4c91-8a25-34fcc729e2b1"
  },
  {
    "type": "Annotation",
    "body": [
      {
        "type": "TextualBody",
        "value": "Vogel",
        "purpose": "tagging"
      }
    ],
    "target": {
      "source": "https://www.ufo-ki.de/annotate/images/156de3674a5c1ed69fb4652b6c5c2c5f.jpg",
      "selector": {
        "type": "FragmentSelector",
        "conformsTo": "http://www.w3.org/TR/media-frags/",
        "value": "xywh=pixel:354,250,57,35"
      }
    },
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "id": "#71adcfcf-672f-4344-910d-f918a6a581ba"
  },
  {
    "type": "Annotation",
    "body": [
      {
        "type": "TextualBody",
        "value": "Vogel",
        "purpose": "tagging"
      }
    ],
    "target": {
      "source": "https://www.ufo-ki.de/annotate/images/156de3674a5c1ed69fb4652b6c5c2c5f.jpg",
      "selector": {
        "type": "FragmentSelector",
        "conformsTo": "http://www.w3.org/TR/media-frags/",
        "value": "xywh=pixel:274,247,53,41"
      }
    },
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "id": "#57f5d3d5-0d2c-4fd5-beef-e051e9226a20"
  }
]
"""
    except Exception as e:
        debug(e)
        return str(e)

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
