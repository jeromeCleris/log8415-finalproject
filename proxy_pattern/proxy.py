import pymysql
import pandas as pd
import sshtunnel
import logging
import random
from sshtunnel import SSHTunnelForwarder


#constants
#nodes addresses, users, key file path
nodes = ["54.164.78.84", "52.202.89.63", "44.212.34.166", "44.210.127.255"]
masterPrivateIP = "10.0.1.202"
sshUser = "ubuntu"
mysqlUser = "root"
mysqlPassword = "asd123"
privateKeyFilePath = "/home/jerome/.ssh/log8415-finalprojet-keypair.pem"

def execQuery(query):
    return pd.read_sql_query(query, sqlConnection)

def remotePrivateIp(nodeIndex):
    return '127.0.0.1' if nodeIndex == 0 else masterPrivateIP

def openTunnel(nodeIndex):

    sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    global tunnel
    tunnel = SSHTunnelForwarder(
        (nodes[nodeIndex], 22),
        ssh_username=sshUser,
        ssh_pkey=privateKeyFilePath,
        remote_bind_address= (remotePrivateIp(nodeIndex) , 3306)
    )
    
    tunnel.start()
    print(tunnel.local_bind_address)

def mysqlConnect(nodeIndex):
    global sqlConnection
    sqlConnection = pymysql.connect(
        host=remotePrivateIp(nodeIndex),
        user="root",
        passwd=mysqlPassword,
        db="sakila",
        port=tunnel.local_bind_port
    )

#Random mode => route to random node
def proxyRandom(query):
    nodeIndex = random.randint(0,3)
    return routeQuery(nodeIndex)

#default mode => route to Master node(nodes[0])
def proxyDefault(query):
    nodeIndex = 0
    return routeQuery(nodeIndex)

#Ping mode => route to lowest ping from nodes
def proxyPing(query):
    return

def routeQuery(nodeIndex):
    openTunnel(nodeIndex)
    mysqlConnect(nodeIndex)
    queryResults = execQuery(query)
    sqlConnection.close()
    tunnel.stop()
    return queryResults

def main():
    print("testing tunnels")
    proxyDefault("select * from actor limit 10")

if __name__ == "__main__":
    main()