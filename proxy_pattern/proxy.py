import pymysql
import pandas as pd
import random
from sshtunnel import SSHTunnelForwarder
import subprocess
import re

#constants
#nodes addresses, users, SSHkey file path, db credentials
nodes = ["3.236.100.67", "35.175.103.246", "3.234.214.25", "44.200.189.152"]
masterPrivateIP = "10.0.1.254"
sshUser = "ubuntu"
mysqlUser = "sysbench"
mysqlPassword = "asd123"
privateKeyFilePath = "/home/ubuntu/.ssh/log8415-finalprojet-keypair.pem"

def execQuery(query):
    return pd.read_sql_query(query, sqlConnection)

def remotePrivateIp(nodeIndex):
    return '127.0.0.1' if nodeIndex == 0 else masterPrivateIP

def openTunnel(nodeIndex):
    global tunnel
    tunnel = SSHTunnelForwarder(
        (nodes[nodeIndex], 22),
        ssh_username=sshUser,
        ssh_pkey=privateKeyFilePath,
        remote_bind_address= (remotePrivateIp(nodeIndex) , 3306)
    )
    
    tunnel.start()

def mysqlConnect(nodeIndex):
    global sqlConnection
    sqlConnection = pymysql.connect(
        host="127.0.0.1",
        user="sysbench",
        passwd=mysqlPassword,
        db="sakila",
        port=tunnel.local_bind_port
    )

#Random mode => route to random node
def proxyRandom(query):
    nodeIndex = random.randint(0,3)
    return routeQuery(nodeIndex, query)

#default mode => route to Master node(nodes[0])
def proxyDefault(query):
    nodeIndex = 0
    return routeQuery(nodeIndex, query)

#Ping mode => route to lowest ping from nodes
def proxyPing(query):
    pingLatencies = getNodePings()
    nodeIndex = pingLatencies.index(min(pingLatencies))

    return routeQuery(nodeIndex, query)

def getNodePings():
    latencies = []
    for nodeIP in nodes:
        ping = subprocess.Popen(['ping', '-c', '1', nodeIP], stdout= subprocess.PIPE)
        output = str(ping.communicate()[0])
        time = re.search('(min\/avg\/max\/mdev = )(.*)', output).group(2).split('/')[1]
        latencies.append(time)
    return latencies

def routeQuery(nodeIndex, query):
    openTunnel(nodeIndex)
    mysqlConnect(nodeIndex)
    queryResults = execQuery(query)
    sqlConnection.close()
    tunnel.stop()
    return str(queryResults)

#Test queries
# curl 127.0.0.1:5000/sql-random?query=select+*+from+actor+limit+10
# curl 127.0.0.1:5000/sql-default?query=select+*+from+actor+limit+10
# curl 127.0.0.1:5000/sql-ping?query=select+*+from+actor+limit+10