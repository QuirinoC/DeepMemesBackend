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
# connect('deep_memes_database')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# MODELS


class Meme(Document):
    link = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    title = StringField(required=True)
    email = StringField(required=True)
    comments = ListField(StringField(max_length=300))
    likes = IntField(required=True)
    dislikes = IntField(required=True)


class User(Document):
    username = StringField(required=True)
    profilePictureLink = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    email = StringField(required=True)


@app.route('/',  methods=['GET'])
def register():
    return 'Servidorino APIrino'


@app.route('/getUser',  methods=['GET'])
def getUser():
    targetUser = request.args.get('email')
    res = {}
    user = User.objects.get(email=targetUser)
    res['email'] = targetUser
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
    else:
        resLimit = 20
    count = 0
    for meme in Meme.objects:
        for tag in meme.tags:
            for query in queries:
                obj = {"link": meme.link, "title": meme.title, "email": meme.email, "likes": meme.likes,
                       "dislikes": meme.dislikes, "comments": meme.comments, "id": str(meme.id), }
                if tag == query and count < resLimit and obj not in res:
                    res.append(obj)
                    count += 1
                if count >= resLimit:
                    break
    print(res)
    return jsonify(res)


@app.route('/getRandom')
def memeRandom():
    res = []
    burnt = []
    if 'limit' in request.args:
        resLimit = int(request.args["limit"])
    else:
        resLimit = 20
    count = 0
    while count < resLimit:
        if count >= len(Meme.objects):
            break
        target = random.randrange(0, len(Meme.objects), 1)
        if target not in burnt:
            count += 1
            burnt.append(target)

            res.append({"link": Meme.objects[target].link, "title": Meme.objects[target].title, "tags": Meme.objects[target].tags, "email": Meme.objects[target].email,
                        "comments": Meme.objects[target].comments, "likes": Meme.objects[target].likes, "dislikes": Meme.objects[target].dislikes, "id": str(Meme.objects[target].id)})
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
    req = request.json
    user = User(
        username=req["username"],
        email=req["email"],
        profilePictureLink=req["profilePictureLink"],
    )
    user.save()
    return make_response(
        "<h1>" +
        "username: " + user.username + "<br>" +
        "email: " + user.email + "<br>" +
        "profilePictureLink: " + user.profilePictureLink + "<br>" +
        "</h1>")


@app.route('/createMeme', methods=['POST'])
def createMeme():
    req = request.json
    meme = Meme(
        link=req["link"],
        title=req["title"],
        email=req["email"],
        likes=0,
        dislikes=0
    )
    meme.save()
    return make_response(
        "<h1>" +
        "email: " + meme.email + "<br>" +
        "Link: " + meme.link + "<br>" +
        "Title: " + meme.title + "<br>" +
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


# @app.route('/updateUserTags', methods=['POST'])
# def updateUserTags():
#     req = request.json
#     targetUser = req.get("email")
#     tag = req.get("tags")
#     user = User.objects.get(email=targetUser)
#     if(tag not in user.tags):
#         print(user.tags)
#         # user.tags.append(tag)
#     # user.save()
#     return make_response("Success")


@app.route('/reaction', methods=['POST'])
def reaction():
    req = request.json
    targetMeme = req.get("uidMeme")
    targetUser = req.get("email")
    type = req.get("type")

    meme = Meme.objects.get(id=targetMeme)
    if type == 0:
        meme.likes = meme.likes + 1
        user = User.objects.get(email=targetUser)
        for tag in meme.tags:
            if(tag not in user.tags):
                user.tags.append(tag)
        meme.save()
        user.save()
        return make_response("Liked")

    if type == 1:
        meme.dislikes = meme.dislikes + 1
        meme.save()
        return make_response("Disliked")


app.run('0.0.0.0', '8080', debug=True)
