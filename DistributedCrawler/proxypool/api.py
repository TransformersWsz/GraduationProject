from flask import Flask, g
from .db import RedisClient

__all__ = ['app']

app = Flask(__name__)

def get_conn():
    if not hasattr(g, "redis"):
        g.redis = RedisClient()
    return g.redis

@app.route("/")
def index():
    return '<h1>Welcome to Proxy Pool System</h1>'

@app.route("/random")
def get_proxy():
    """
    获取一个随机代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route("/count")
def get_count():
    """
    获取代理池中的代理个数
    :return: 代理个数
    """
    conn = get_conn()
    return str(conn.count())



