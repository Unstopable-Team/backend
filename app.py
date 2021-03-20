from flask import Flask, render_template, session, copy_current_request_context
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

# Librabry for WebSocket
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

# Librabry for RestAPI
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserManagement, UserLogin, UserLogout, TokenRefresh
from blacklist import BLACKLIST



async_mode = None
app = Flask(__name__)
load_dotenv(".env", verbose=True)

# Load config from setting.py
app.config.from_object("setting.DevelopmentConfig")
api = Api(app)

# Initilize websocket
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


jwt = JWTManager(app)
db = MongoEngine(app)

# This method will check if a token is blacklisted, 
# and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

api.add_resource(UserManagement, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/token')

# Testing websocket site
@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


# Socket connection implementation
@socket_.on('notification', namespace='/forecast')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('critical_notification', namespace='/forecast')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socket_.on('disconnect_request', namespace='/forecast')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    socket_.run(app, debug=True)
