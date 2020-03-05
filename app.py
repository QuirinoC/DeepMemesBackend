from flask import Flask

app = Flask(__name__)

@app.route('/')
def register():
    return 'servidorino funcionarin'

app.run('0.0.0.0', '8080', debug=True)