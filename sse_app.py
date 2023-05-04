from flask import Flask, render_template, json, jsonify, request, redirect, url_for
from flask_sse import sse
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://:password@localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    user = db.relationship('User', backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, text, user, pub_date=None):
        self.text = text
        self.user = user
        if not pub_date:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Message %r>' % self.text


@app.route('/', methods=["GET", "POST"])
def auth():
    if request.method == 'POST':
        user_id = request.form.get('comp_select')
        try:
            user_id = int(user_id)
        except ValueError:
            users = User.query.all()
            return render_template("auth.html", error="Выберите пользователя или создайте нового", users=users)
        return redirect(url_for('index', user_id=user_id), 200)
    elif request.method == 'GET':
        users = User.query.all()
        return render_template("auth.html", users=users)


@app.route('/registration/', methods=["GET", "POST"])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        new_user = User(username)
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            error = "Пользователь с таким именем уже существует"
            return render_template("registration.html", error=error)
        return redirect(url_for('index', user_id=new_user.id), 200, )
    elif request.method == 'GET':
        return render_template("registration.html")


@app.route('/chat/<user_id>')
def index(user_id):
    messages = Message.query.all()
    return render_template("index.html", user_id=int(user_id), messages=messages)


@app.route('/publish', methods=["POST"])
def publish():
    data = json.loads(request.data)
    print(data)
    message = Message(
        text=data['text'],
        user=User.query.get(int(data['user_id']))
    )
    db.session.add(message)
    db.session.commit()
    data = {
        'user_id': message.user.id,
        'username': message.user.username,
        'text': message.text,
        'pub_date': message.pub_date
    }
    try:
        # Send to Redis publisher
        sse.publish(data, type="bigboxcode")

        return jsonify(status="success", message="published", data=data)
    except:
        return jsonify(status="fail", message="not published")

# gunicorn sse_app:app --worker-class gevent --bind 127.0.0.1:8000


if __name__ == "__main__":
    app.run(debug=True)
