from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app=Flask(__name__)
app.secret_key="H#LL0!!!!!"
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("home.html")


@socketio.on("connect")
def socketConnect():
    print("Connected")


@socketio.on("getData")
def getData():
    racedata={"driver":"ALB","pos":1}
    emit("getDataEmit",racedata)


if __name__ == '__main__':
    socketio.run(app, debug=True)