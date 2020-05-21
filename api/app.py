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

# MODELS
class Meme(Document):
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    title = StringField(required=True)
    idUser = StringField(required=True)
    comments = ListField(StringField(max_length=300))
    likes = IntField(required=True)
    dislikes = IntField(required=True)

class User(Document):
    idUser = StringField(required=True)
    username = StringField(required=True)
    profilePictureLink = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    email = StringField(required=True)

@app.route('/',  methods=['GET'])
def register():
    return 'Servidorino APIrino'

@app.route('/getUser',  methods=['GET'])
def getUser():
    targetUser = request.args.get('uid')
    res = {}
    user = User.objects.get(idUser=targetUser)
    res['email'] = user.email
    res['username'] = user.username
    res['profilePictureLink'] = user.profilePictureLink
    res['tags'] = user.tags
    return jsonify(res)

@app.route('/getRelatedTo')
def memeRelatedTo():
    res = []
    queries = request.args["tags"].split(",")
    if 'limit' in request.args:
        resLimit = int(request.args["limit"])
    else :
        resLimit = 20
    count = 0
    for meme in Meme.objects:
        for tag in meme.tags:
            for query in queries:
                if tag == query and count < resLimit:
                    res.append(meme.link)
                    count+=1
                if count >= resLimit:
                    break
    return jsonify(res)

@app.route('/getRandom')
def memeRandom():
    res = []
    burnt = []
    if 'limit' in request.args:
        resLimit = int(request.args["limit"])
    else :
        resLimit = 20
    count = 0
    while count < resLimit:
        if count >= len(Meme.objects):
            break
        target = random.randrange(0,len(Meme.objects), 1)
        if target not in burnt:
            count+=1
            burnt.append(target)
            res.append(Meme.objects[target].link+":"+Meme.objects[target].tags[0])
    return jsonify(res)

@app.route('/getComments')
def getComments():
    targetMeme = request.args.get('memeUid')
    meme = Meme.objects.get(id=targetMeme)
    return jsonify(meme.comments)

@app.route('/getReactions')
def getReactions():
    targetMeme = request.args.get('memeUid')
    res = {}
    meme = Meme.objects.get(id=targetMeme)
    res['likes'] = meme.likes
    res['dislikes'] = meme.dislikes
    return jsonify(res)

@app.route('/createUser', methods=['POST'])
def createUser():
    req       = request.json
    user      = User(
        idUser             = req.get("idUser"),
        username           = req.get("username"),
        email              = req.get("email"),
        profilePictureLink = req.get("profilePictureLink"),
    )
    user.save()
    return make_response(
    "<h1>" + 
            "userId: "              + user.idUser  + "<br>" +
            "username: "            + user.username  + "<br>" +
            "email: "               + user.email  + "<br>" +
            "profilePictureLink: "  + user.profilePictureLink  + "<br>" +
    "</h1>")

@app.route('/createMeme', methods=['POST'])
def createMeme():
    req       = request.json
    meme      = Meme(
        link     = req.get("link"),
        title    = req.get("title"),
        idUser   = req.get("idUser"),
        likes    = 0,
        dislikes = 0
    )
    meme.save()
    return make_response(
    "<h1>" + 
            "userId: " + meme.idUser + "<br>" +
            "Link: "   + meme.link  + "<br>" +
            "Title: "  + meme.title + "<br>" +
    "</h1>")

@app.route('/createComment', methods=['POST'])
def createComment():
    req = request.json
    targetMeme = req.get("uidMeme")
    comment = req.get("comment")

    meme = Meme.objects.get(id=targetMeme)
    meme.comments.append(comment)
    meme.save()
    return make_response("Success")

@app.route('/reaction', methods=['POST'])
def reaction():
    req = request.json
    targetMeme = req.get("uidMeme")
    targetUser = req.get("uidUser")
    type       = req.get("type")

    meme = Meme.objects.get(id=targetMeme)
    if type == 0:
        meme.likes = meme.likes + 1
        user = User.objects.get(id=targetUser)
        for tag in meme.tags:
            user.tags.append(tag)
        meme.save()
        user.save()
        return make_response("Liked")
    
    if type == 1:
        meme.dislikes = meme.dislikes + 1
        meme.save()
        return make_response("Disliked")
 
app.run('0.0.0.0', '8080', debug=True)