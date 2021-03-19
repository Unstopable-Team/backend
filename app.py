from flask import Flask
import time

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello Guys'
