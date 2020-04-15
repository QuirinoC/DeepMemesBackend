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

@app.route('/classify', methods=['POST'])
def upload_image():
    print(request)
    return jsonify({
        'message' : 'ok'
    })
 
app.run('0.0.0.0', '8080', debug=True)