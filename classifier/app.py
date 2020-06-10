from flask import Flask, jsonify, make_response, request, render_template, Response
from mongoengine import *
import os
from flask_cors import CORS, cross_origin

import torch
from PIL import Image
from torchvision import transforms
import requests
from io import BytesIO

import urllib

model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet152', pretrained=True)

connection = connect('deep_memes_database',
                     host='deep_memes_database',
                     port=27017
                     )
# connect('deep_memes_database')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def download_image(url: str) -> 'PIL: Image':

    response = requests.get(url)

    img = Image.open(BytesIO(response.content))


def transform_image(input_image: Image) -> 'Tensor':
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    return input_batch


@app.route('/')
def root():
    return jsonify('Classifier API')


@app.route('/classify', methods=['POST'])
def classifier():
    url = request.json.get('url')

    if not url:
        return "URL must be in post body"

    print(f"Processing image: {url}")
    # Download image as tmp
    response = requests.get(url)
    input_image = Image.open(BytesIO(response.content))
    input_batch = transform_image(input_image)

    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)

    predictions = output

    top_labels = torch.topk(output, 10).indices.tolist()

    return jsonify(top_labels[0])


def process_image(image):
    # This function takes in an image as an input and returns the tags of the image as an output
    from random import shuffle
    '''
    To implement
    Response is mocked for now
    '''
    tags = [
        'dog',
        'cat',
        'car',
        'fan',
        'computer',
        'notebook',
        'pen',
        'ice cream',
        'monitor',
        'charge',
        'person',
        'country',
        'bike'
    ]
    # Get 3 random images
    shuffle(tags)
    return jsonify(
        tags[:3]
    )


@app.route('/test', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not image:
        return jsonify({
            'message': 'error: No image sent'
        })

    res = process_image(image)

    return res


app.run('0.0.0.0', '8080', debug=True)
