#!/bin/bash

IMGPATH=$1

curl \
  -F "image=@${IMGPATH}" \
  localhost:5000
