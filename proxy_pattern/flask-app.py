from flask import Flask
import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

@app.route('/sql-random', methods = ['POST', 'GET'])
def sql():
    query = request.args['query']
    return query

@app.route('/sql-default', methods = ['POST', 'GET'])
def sql():
    query = request.args['query']
    return query

@app.route('/sql-ping', methods = ['POST', 'GET'])
def sql():
    query = request.args['query']
    return query