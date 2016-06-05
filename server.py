#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging

from logging import StreamHandler
from flask import Flask, jsonify
from flask_cache import Cache
from zhihu_oauth import ZhihuClient

client = ZhihuClient()
client.load_token('token.pkl')


cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

file_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


@app.route('/', methods=['GET'])
def index_route():
    return jsonify({
        'author': 'knarfeh',
        'author_url': 'knarfeh.com',
    })


# Questions
@cache.cached(timeout=300)
@app.route('/questions/<int:question>', methods=['GET'])
def question_info_route(question):
    question_oauth = client.question(question)
    return jsonify(question_oauth.pure_data['data'])


if __name__ == '__main__':
    app.run(debug=True)
