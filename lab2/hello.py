import random
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Napier'

@app.route('/bye')
def bye_world():
    return 'Goodbye Napier'

@app.route('/random')
def random_world():
    return str (random.randint(1,101)) + 'Napier'

