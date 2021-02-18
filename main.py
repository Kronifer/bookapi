from flask import Flask, request, jsonify
from replit import db

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return "<h1>Home page for book api</h1>"


@app.route('/api/v1/data/add', methods=["GET"])
def adddata():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")
    try:
        db[title]
        return "Book has already been added."
    except:
        db[title] = title
        db[title + "a"] = author
        db[title + "g"] = genre
        return ("Data has been added!")


@app.route('/api/v1/data/get', methods=["GET"])
def getdata():
    title = request.args.get("title")
    tvalue = db[title]
    gvalue = db[title + 'g']
    avalue = db[title + 'a']
    data = {}
    data.update({"title": tvalue})
    data.update({"author": avalue})
    data.update({"genre": gvalue})
    return jsonify(data)


app.run(host="0.0.0.0", port="8080")
