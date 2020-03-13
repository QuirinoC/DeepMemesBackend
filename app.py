from flask import Flask, jsonify, make_response, request, render_template, Response

from mongoengine import *
from models import *
import os

from flask_cors import CORS, cross_origin

connection = connect('deep_memes_database',
        host='deep_memes_database',
        port=27017
        )
#connect('deep_memes_database')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/')
def register():
    return 'DeepMemesBackendAPI'

@app.route('/upload', methods=['GET'])
def getImageLink():
    res = {}
    return '\n'.join((link.Link for link in Link.objects()))

@app.route('/upload', methods=['POST'])
def postImageLink():
    req       = request.json
    link      = req.get("link")
    Link(Link=link).save()
    return make_response("<h1>"+link+"</h1>")

@app.route('/user', methods=['POST'])
def postUser():
    req       = request.json
    link      = req.get("user")
    Link(Link=link).save()
    return make_response("<h1>"+user+"</h1>")

@app.route('/submission/relatedto')
def submissionRelatedTo():
    queries = request.args["tags"].split(",")
    return jsonify(queries)

app.run('0.0.0.0', '8080', debug=True)