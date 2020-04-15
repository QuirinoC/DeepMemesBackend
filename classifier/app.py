from flask import Flask, jsonify, make_response, request, render_template, Response

from mongoengine import *
import os

from flask_cors import CORS, cross_origin

connection = connect('deep_memes_database',
        host='deep_memes_database',
        port=27017
        )
#connect('deep_memes_database')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

class Submission(Document):
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))

@app.route('/')
def root():
    return jsonify('Classifier API')

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

@app.route('/classify', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not image:
        return jsonify({
            'message' : 'error: No image sent'
        })

    res = process_image(image)
    
    return res
 
app.run('0.0.0.0', '8080', debug=True)