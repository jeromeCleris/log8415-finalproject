from flask import Flask, request
from proxy import *

app = Flask(__name__)

@app.route('/sql-random', methods = ['POST', 'GET'])
def sqlRandom():
    query = request.args.get('query')
    return proxyRandom(query)

@app.route('/sql-default', methods = ['POST', 'GET'])
def sqlDefault():
    query = request.args.get('query')
    return proxyDefault(query)

@app.route('/sql-ping', methods = ['POST', 'GET'])
def sqlPing():
    query = request.args.get('query')
    return proxyPing(query)