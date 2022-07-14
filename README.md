# A SimpleFlaskPytorchServer

What is this?

It allows you to run a python3-flask server that accepts incoming images, analyzes
them with a network from the Torch-Hub (yolo in the default case) and gives out a
CSV file with all the information needed for drawing bounding boxes.

# Run it like this:

```command
python3 serve.py
```

and you can test it like this (make sure the server runs first):

```command
bash test.sh /absolute/path/to/any_image.jpg
```
