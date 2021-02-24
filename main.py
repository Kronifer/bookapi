from flask import Flask, request, jsonify, render_template
import pymongo
import json

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

client = pymongo.MongoClient("mongodb+srv://APIUSER:book_api@books.1zhnr.mongodb.net/Bookapi?retryWrites=true&w=majority")
db = client.Bookapi

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")


@app.route('/api/v1/data/add', methods=["GET"])
def adddata():
    title = request.args.get("title").lower()
    author = request.args.get("author").lower()
    genre = request.args.get("genre").lower()
    publisher = request.args.get("publisher").lower()
    yearpublished = int(request.args.get("pubyear"))
    data = {}
    data.update({"title": title})
    data.update({"author": author})
    data.update({"genre": genre})
    data.update({"publisher": publisher})
    data.update({"year published": yearpublished})
    db.Books.insert_one(data)
    return "Data has been added!"


@app.route('/api/v1/data/get', methods=["GET"])
def getdata():
    title = request.args.get('title')
    collection = db.Books
    doc = collection.find_one({"title": title}, {"_id": 0})
    if doc == None:
        return "Book is not registered."
    else:
        return jsonify(doc)



@app.route('/api/v1/data/getbygenre', methods=["GET"])
def getbygenre():
    genre = request.args.get('genre').lower()
    collection = db.Books
    docs = collection.find({"genre": genre}, {"_id": 0})
    data = []
    for document in docs:
        data.append(document)
    return jsonify(data)



@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")


@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


app.run(host="0.0.0.0", port="8080")
