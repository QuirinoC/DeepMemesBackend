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

class Submission(Document):
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))

@app.route('/')
def register():
    return 'Servidorino APIrino'

@app.route('/submission', methods=['GET'])
def getImageLink():
    res = {}
    return '\n'.join(((submissions.link + ":" + submissions.tags[0] + "\n") for submissions in Submission.objects()))

@app.route('/submission', methods=['POST'])
def postImageLink():
    req       = request.json
    submission= Submission(link = req.get("link"))
    submission.tags = req.get("tags").split(",")
    submission.save()
    return make_response("<h1>"+submission.link+"</h1>")

@app.route('/submission/relatedto')
def submissionRelatedTo():
    res = []
    queries = request.args["tags"].split(",")
    for submission in Submission.objects:
        for tag in submission.tags:
            for query in queries:
                if tag == query:
                    res.append(submission.link)
    return jsonify(res)
 
app.run('0.0.0.0', '8080', debug=True)