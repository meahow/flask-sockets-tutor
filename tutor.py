from flask import Flask
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)

socketlist = []

@sockets.route('/')
def echo_socket(ws):
    socketlist.append(ws)
    while not ws.closed:
        message = ws.receive()
        if message:
            for s in socketlist:
                s.send(message)
    socketlist.remove(ws)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
