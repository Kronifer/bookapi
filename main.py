from flask import Flask, request, jsonify, render_template
from replit import db

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")


@app.route('/api/v1/data/add', methods=["GET"])
def adddata():
    title = request.args.get("title").lower()
    author = request.args.get("author").lower()
    genre = request.args.get("genre").lower()
    try:
        db[title]
        return "Book has already been added."
    except:
        db[title] = title
        db[title + "@"] = author
        db[title + "^"] = genre
        return ("Data has been added!")


@app.route('/api/v1/data/get', methods=["GET"])
def getdata():
    title = request.args.get("title").lower()
    try:
        tvalue = db[title]
        gvalue = db[title + '^']
        avalue = db[title + '@']
        data = {}
        data.update({"title": tvalue})
        data.update({"author": avalue})
        data.update({"genre": gvalue})
        return jsonify(data)
    except:
        return "That book has not been registered yet. Consider adding it yourself!"


@app.route('/api/v1/data/getbygenre', methods=["GET"])
def getbygenre():
    genre = request.args.get('genre').lower()
    keys = db.keys()
    data = {}
    for key in keys:
        newtitle = ""
        value = db[key]
        badchars = ["@", "^"]
        if value == genre:
            for element in key:
                if element in badchars:
                    pass
                else:
                    newtitle += element
            author = db[newtitle + "@"]

            data.update({newtitle: author})
        else:
            pass
    return jsonify(data)


@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")

@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


app.run(host="0.0.0.0", port="8080")
