#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import pymongo
import os
import time
from threading import Thread
import sys


def main():

    app = Flask(__name__)

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    client = \
        pymongo.MongoClient('mongodb+srv://APIUSER:book_api@books.1zhnr.mongodb.net/Bookapi?retryWrites=true&w=majority')
    db = client.Bookapi

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route('/api/v1/data/add', methods=['GET'])
    def adddata():
        title = request.args.get('title').lower()
        book = db.Books.find_one({'title': title}, {'_id': 0})
        print (book)
        if book != None:
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

    @app.route('/api/v1/data/get', methods=['GET'])
    def getdata():
        title = request.args.get('title')
        collection = db.Books
        doc = collection.find_one({'title': title}, {'_id': 0})
        if doc == None:
            return 'Book is not registered.'
        else:
            return jsonify(doc)

    @app.route('/api/v1/data/getbygenre', methods=['GET'])
    def getbygenre():
        genre = request.args.get('genre').lower()
        collection = db.Books
        docs = collection.find({'genre': genre}, {'_id': 0})
        data = []
        for document in docs:
            data.append(document)
        return jsonify(data)

    @app.route('/api/v1/data/getbyauthor', methods=['GET'])
    def getbyauthor():
        author = request.args.get('author').lower()
        collection = db.Books
        docs = collection.find({'author': author}, {'_id': 0})
        data = []
        for document in docs:
            data.append(document)
        return jsonify(data)

    @app.route('/about', methods=['GET'])
    def about():
        return render_template('about.html')

    @app.route('/admin/shutdown', methods=['GET'])
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @app.errorhandler(404)
    def error404(e):
        return render_template('404.html')

    def run():
        app.run(host='0.0.0.0', port='8080')

    apiserver = Thread(target=run)
    apiserver.start()


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        main()
        time.sleep(3)
        os.system('curl http://localhost:8080/api/v1/data/get?title=dragonwatch'
                  )
        os.system('curl http://localhost:8080/admin/shutdown')
    elif sys.argv[1] == 'run':
        main()
