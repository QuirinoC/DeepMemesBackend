from flask import Flask, jsonify, make_response, request, render_template, Response

from mongoengine import *
from models import *
import os
import random

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
    if 'limit' in request.args:
        resLimit = int(request.args["limit"])
    else :
        resLimit = 20
    count = 0
    for submission in Submission.objects:
        for tag in submission.tags:
            for query in queries:
                if tag == query and count < resLimit:
                    res.append(submission.link)
                    count+=1
                if count >= resLimit:
                    break
    return jsonify(res)

@app.route('/submission/random')
def submissionRandom():
    res = []
    burnt = []
    if 'limit' in request.args:
        resLimit = int(request.args["limit"])
    else :
        resLimit = 20
    count = 0
    while count < resLimit:
        if count >= len(Submission.objects):
            break
        target = random.randrange(0,len(Submission.objects), 1)
        if target not in burnt:
            count+=1
            burnt.append(target)
            res.append(Submission.objects[target].link+":"+Submission.objects[target].tags[0])
    return jsonify(res)
 
app.run('0.0.0.0', '8080', debug=True)