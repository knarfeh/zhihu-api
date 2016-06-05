# coding=utf-8

from __future__ import unicode_literals, print_function

import os

from zhihu_oauth import ZhihuClient


TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login('zhihu2ebook@hotmail.com', 'Zhihu2Ebook')
    client.save_token(TOKEN_FILE)

