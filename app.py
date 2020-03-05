from flask import Flask, jsonify, make_response, request, render_template, Response

app = Flask(__name__)

@app.route('/')
def register():
    return 'servidorino funcionarino'

@app.route('/upload', methods=['GET'])
def getImageLink():
    return 'Imagen bien chida'

@app.route('/upload', methods=['POST'])
def postImageLink():
    req       = request.json
    test      = req.get("test")
    print(test)
    return test

app.run('0.0.0.0', '8080', debug=True)