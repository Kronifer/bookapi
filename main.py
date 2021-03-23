#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, send_file, abort
import pymongo
import os
import time

def main():

    app = Flask(__name__)

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    client = pymongo.MongoClient(
        os.getenv("MKEY")
    )

    db = client.Bookapi

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route('/api/v1/add', methods=['GET'])
    def adddata():
        title = request.args.get('title').lower()
        book = db.Books.find_one({'title': title}, {'_id': 0})
        print(book)
        if book is not None:
            return 'Book has already been added.'
        else:
            author = request.args.get('author').lower()
            genre = request.args.get('genre').lower()
            publisher = request.args.get('publisher').lower()
            yearpublished = int(request.args.get('pubyear'))
            data = {}
            data.update({'title': title})
            data.update({'author': author})
            data.update({'genre': genre})
            data.update({'publisher': publisher})
            data.update({'year published': yearpublished})
            db.Books.insert_one(data)
            return 'Data has been added!'

    @app.route('/api/v1/get', methods=['GET'])
    def getdata():
        title = request.args.get('title').lower()
        collection = db.Books
        doc = collection.find_one({'title': title}, {'_id': 0})
        if doc is None:
            return 'Book is not registered.'
        else:
            return jsonify(doc)

    @app.route('/api/v1/getbygenre', methods=['GET'])
    def getbygenre():
        genre = request.args.get('genre').lower()
        collection = db.Books
        docs = collection.find({'genre': genre}, {'_id': 0})
        data = []
        for document in docs:
            data.append(document)
        return jsonify(data)

    @app.route('/api/v1/getbyauthor', methods=['GET'])
    def getbyauthor():
        author = request.args.get('author').lower()
        collection = db.Books
        docs = collection.find({'author': author}, {'_id': 0})
        data = []
        for document in docs:
            data.append(document)
        return jsonify(data)

    @app.route('/api/v1/getall', methods=["GET"])
    def getall():
        bookData = db.Books
        docs = bookData.find({}, {"_id": 0})
        docList = []
        for x in docs:
            docList.append(x)
        return jsonify(docList)

    @app.route('/about', methods=['GET'])
    def about():
        return render_template('about.html')
        
    @app.route("/coffee")
    def coffee():
        abort(418)

    @app.route('/admin/shutdown', methods=['GET'])
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.errorhandler(404)
    def error404(e):
        return render_template('404.html')

    @app.errorhandler(500)
    def error500(e):
        return render_template("500.html")

    @app.route("/jstest", methods=["GET"])
    def test():
        return render_template("test.html")

    @app.route('/robots.txt', methods=["GET"])
    def robots():
        return send_file("templates/robots.txt")
    
    app.run('0.0.0.0', port='5000')

