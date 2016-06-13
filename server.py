#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging

from logging import StreamHandler
from flask import Flask, jsonify, redirect
from flask_cache import Cache
from zhihu_oauth import ZhihuClient

client = ZhihuClient()
client.load_token('token.pkl')

me = client.me()

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
        'author_url': 'http://www.knarfeh.com',
        'people': 'http://zhihu-api.knarfeh.com/people/<people_id>',
        'question': 'http://zhihu-api.knarfeh.com/questions/<int:question_id>',
        'answer': 'http://zhihu-api.knarfeh.com/answers/<int:answer_id>',
        'question_answer': 'http://zhihu-api.knarfeh.com/question/<int:question_id>/answer/<int:answer_id>',
        'topic': 'http://zhihu-api.knarfeh.com/topic/<int:topic_id>',
        'collection': 'http://zhihu-api.knarfeh.com/collection/<int:collection_id>',
        'article': 'http://zhihu-api.knarfeh.com/article/<int:article_id>',
        'columns': 'http://zhihu-api.knarfeh.com/columns/<column_id>',
        'activity': 'http://zhihu-api.knarfeh.com/activity/<people_id>'
    })


# Activity
@cache.cached(timeout=300)
@app.route('/activity/<people_id>', methods=['GET'])
def activity_rout(people_id):
    u"""
    目前最多10条动态
    :param people_id:
    :return:
    """
    people_oauth = client.people(people_id)
    activities = people_oauth.activities
    result = dict()
    i = 0
    for item in activities:
        print item.target
        result[str(i)] = item.target.pure_data
        if i == 10:
            break
        i += 1
    return jsonify(result)


# Article
@cache.cached(timeout=300)
@app.route('/columns/<column_id>', methods=['GET'])
def column_route(column_id):
    u"""

    :param column_id:
    :return:
    """

    return redirect('https://zhuanlan.zhihu.com/api/columns/'+column_id)


@cache.cached(timeout=300)
@app.route('/article/<int:article_id>', methods=['GET'])
def article_route(article_id):
    u"""

    :param article_id:
    :return:
    """
    article_oauth = client.article(article_id)
    return jsonify(article_oauth.pure_data['data'])


@cache.cached(timeout=300)
@app.route('/collection/<int:collection_id>', methods=['GET'])
def collection_info_route(collection_id):
    u"""

    :param collection_id:
    :return:
    """
    collection_oauth = client.collection(collection_id)
    return jsonify(collection_oauth.pure_data['data'])


@cache.cached(timeout=300)
@app.route('/collection/<int:collection_id>/', methods=['GET'])
def collection_answer_route(collection_id):
    u"""

    :param collection_id:
    :return:
    """
    collection_oauth = client.collection(collection_id)
    result = dict()
    result['info'] = collection_oauth.pure_data['data']
    result['data'] = [item.pure_data['cache'] for item in collection_oauth.answers]
    return jsonify(result)


# People
@cache.cached(timeout=300)
@app.route('/people/<people_id>', methods=['GET'])
def people_info_route(people_id):
    u"""
    需要登录状态
    :param people_id:
    :return:
    """
    people_oauth = client.people(people_id)
    return jsonify(people_oauth.pure_data['data'])


@app.route('/topic/<int:topic_id>', methods=['GET'])
def topic_info_route(topic_id):
    u"""

    :param topic_id:
    :return:
    """
    topic_oauth = client.topic(topic_id)
    return jsonify(topic_oauth.pure_data['data'])


@cache.cached(timeout=300)
@app.route('/me', methods=['GET'])
def me_info():
    u"""
    需要登录状态
    :return:
    """
    me_oauth = client.me()
    return jsonify(me_oauth.pure_data['data'])


# Questions
@cache.cached(timeout=300)
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
@cache.cached(timeout=300)
@app.route('/answers/<int:answer_id>', methods=['GET'])
def answer_route(answer_id):
    u"""
    需要登录状态
    :param answer_id:
    :return:
    """
    answer_oauth = client.answer(answer_id)
    return jsonify(answer_oauth.pure_data['data'])


@cache.cached(timeout=300)
@app.route('/question/<int:question_id>/answer/<int:answer_id>', methods=['GET'])
def question_answer_route(question_id, answer_id):
    u"""
    需要登录状态
    :param question_id:
    :param answer_id:
    :return:
    """
    answer_oauth = client.answer(answer_id)
    return jsonify(answer_oauth.pure_data['data'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
