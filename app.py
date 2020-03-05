from flask import Flask, jsonify, make_response, request, render_template, Response

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
    res = jsonify(res)
    return make_response(res)

@app.route('/upload', methods=['POST'])
def postImageLink():
    req       = request.json
    link      = req.get("link")
    print(link)
    return make_response("<h1>"+link+"</h1>")

app.run('0.0.0.0', '8080', debug=True)