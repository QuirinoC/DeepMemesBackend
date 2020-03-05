from flask import Flask, jsonify, make_response, request, render_template, Response
from mongoengine import *
from models import *
import os

connection = connect('deep_memes_database',
        host='localhost',
        port=27017,username='root',
        password='root',
        authentication_source='admin')
#connect('deep_memes_database')

app = Flask(__name__)

@app.route('/')
def register():
    return 'servidorino funcionarino'

@app.route('/upload', methods=['GET'])
def getImageLink():
    res = {}
    res['status']  = "OK"
    res['message'] = "Link a una foto chida"
    res['quirino'] = "Wapo"
    res = []
    for link in Link.objects():
        res.append(link.Link)
    return '\n'.join(res)

@app.route('/upload', methods=['POST'])
def postImageLink():
    req       = request.json
    link      = req.get("link")
    Link(Link=link).save()
    return make_response("<h1>"+link+"</h1>")

app.run('0.0.0.0', '8080', debug=True)