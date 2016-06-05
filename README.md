# Zhihu API

一个非官方的 知乎 api。

基于[zhihu-oauth](https://github.com/7sDream/zhihu-oauth)，关于 [zhihu-oauth](https://github.com/7sDream/zhihu-oauth) 的介绍见：

* [Game walkthrough - 游戏攻略](http://zhihu-oauth.readthedocs.io/zh_CN/latest/for-dev/oauth/game.html)

### 目录
* [API 用法](#api-usage)
* [说明](#features)
* [安装](#installation)
* [感谢](#contributing)
* [License](#license)

## API 用法
### Demo

todo

### 概述

* GET [`/questions/<question_id>`](#get-questionsquestion_id)

### GET `/questions/<question_id>`

example:


## 说明

## 安装

### 使用 virtualenv

```bash
$ virtualenv ENV
$ source ENV/bin/activate
```

### 解决依赖

```bash
$ pip install -r requirements.txt
```

### 退出虚拟环境

```bash
$ deactivate
```

### 使用方法

* 首先，利用 login_zhihu.py 登录，生成 token.pkl  

```bash
$ python login_zhihu.py
```

* 构建 api 服务

```
$ python server.py
```

## 感谢

* [zhihu-oauth](https://github.com/7sDream/zhihu-oauth)
* [quora-api](https://github.com/csu/quora-api)

## License

[MIT](./LICENSE)

