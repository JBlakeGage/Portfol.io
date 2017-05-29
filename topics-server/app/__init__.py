from __future__ import absolute_import
import logging
import json
from flask import Flask
from flask_restful import Api
from app.utils.es import Search
from app.topic.analyzer import TopicAnalyzer


logging.basicConfig(level=logging.INFO)

topics_app = Flask(__name__)
api = Api(topics_app)


@topics_app.route('/topics/tfidf/<string:term>', methods=['GET'])
def get_tfidf(term):
    topics = None
    json_data = {}
    try:
        logging.info('Term = {0}'.format(term))
        search = Search()
        if term:
            data = search.get(term)
            if data is not None and len(data) > 0:
                topics = TopicAnalyzer(data)
                json_data = topics.get_tfidf_as_json()
    except Exception, error:
        logging.error('Exception occurred - {0}'.format(str(error)))
    return json_data


@topics_app.route('/topics/lsi/<string:term>', methods=['GET'])
def get_lsi(term):
    topics = None
    json_data = {}
    try:
        logging.info('Term = {0}'.format(term))
        search = Search()
        if term:
            data = search.get(term)
            if data is not None and len(data) > 0:
                topics = TopicAnalyzer(data)
                json_data = topics.get_lsi()
    except Exception, error:
        logging.error('Exception occurred - {0}'.format(str(error)))
    return json_data


@topics_app.route('/topics/lda/<string:term>', methods=['GET'])
def get_lda(term):
    topics = None
    json_data = {}
    try:
        search = Search()
        if term:
            data = search.get(term)
            if data is not None and len(data) > 0:
                topics = TopicAnalyzer(data)
                json_data = topics.get_lda()
    except Exception, error:
        logging.error('Exception occurred - {0}'.format(str(error)))
    return json_data


@topics_app.route('/topics/search/<string:term>', methods=['GET'])
def search(term):
    json_data = {}
    try:
        search = Search()
        if term:
            data = search.get(term)
            json_data = json.dumps(data)
    except Exception, error:
        logging.error('Exception occurred - {0}'.format(str(error)))
    return json_data
