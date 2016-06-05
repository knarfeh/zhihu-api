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


# People
# @cache.cached(timeout=300)
@app.route('/people/<people_id>', methods=['GET'])
def people_info_route(people_id):
    u"""
    需要登录状态
    :param people_id:
    :return:
    """
    people_oauth = client.people(people_id)
    return jsonify(people_oauth.pure_data['data'])


# @cache.cached(timeout=300)
@app.route('/me', methods=['GET'])
def me_info():
    u"""
    需要登录状态
    :return:
    """
    me_oauth = client.me()
    return jsonify(me_oauth.pure_data['data'])


# Questions
# @cache.cached(timeout=300)
@app.route('/questions/<int:question_id>', methods=['GET'])
def question_info_route(question_id):
    u"""
    需要登录状态
    获得该问题的基本信息
    :param question_id:
    :return:
    """
    question_oauth = client.question(question_id)
    return jsonify(question_oauth.pure_data['data'])


@app.route('/questions/<int:question_id>/', methods=['GET'])
def question_answers_route(question_id):
    u"""
    需要登录状态
    获得该问题下的所有答案
    :param question_id:
    :return:
    """
    # NEED test
    question_oauth = client.question(question_id)
    result = dict()
    result['info'] = question_oauth.pure_data['data']
    result['data'] = [item.pure_data['cache'] for item in question_oauth.answers]
    return jsonify(result)


# Answers
# @cache.cached(timeout=300)
@app.route('/answers/<int:answer_id>', methods=['GET'])
def answer_route(answer_id):
    u"""
    需要登录状态
    :param answer_id:
    :return:
    """
    answer_oauth = client.answer(answer_id)
    return jsonify(answer_oauth.pure_data['data'])


if __name__ == '__main__':
    app.run(debug=True)
