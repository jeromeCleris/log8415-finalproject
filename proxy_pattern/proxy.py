#Heavily inspired from https://practicaldatascience.co.uk/data-science/how-to-connect-to-mysql-via-an-ssh-tunnel-in-python
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
    """Uses the pandas module to execute the sql query using an existing sql connection

    Parameters:
    query (string): SQL query to run

    Returns:
    Pandas.Dataframe: dataframe containing the query values
    """
    return pd.read_sql_query(query, sqlConnection)

def remotePrivateIp(nodeIndex):
    """Returns the appropriate private ip depending on which instance we are connecting to.
    If on master node, use localhost, else use master private ip

    Parameters:
    nodeIndex (int): identifies the machine we are on

    Returns:
    string: remote private Ip address
    """
    return '127.0.0.1' if nodeIndex == 0 else masterPrivateIP

def openTunnel(nodeIndex):
    """Opens sshTunnel to specific node, binds mysql server address

    Parameters:
    nodeIndex (int): identifies the machine to connect to
    """
    global tunnel
    tunnel = SSHTunnelForwarder(
        (nodes[nodeIndex], 22),
        ssh_username=sshUser,
        ssh_pkey=privateKeyFilePath,
        remote_bind_address= (remotePrivateIp(nodeIndex) , 3306)
    )
    
    tunnel.start()

def mysqlConnect():
    """Creates connection to the remote MySQL cluster
    """
    global sqlConnection
    sqlConnection = pymysql.connect(
        host="127.0.0.1",
        user="sysbench",
        passwd=mysqlPassword,
        db="sakila",
        port=tunnel.local_bind_port
    )

def proxyRandom(query):
    """Randomly chooses a node to route the sql query

    Parameters:
    query (string): SQL query to run

    Returns:
    string: returns string cast of output from the routed query from routeQuery()
    """
    nodeIndex = random.randint(0,3)

    print("Request sent to ", nodeIndex)
    return routeQuery(nodeIndex, query)

def proxyDefault(query):
    """Always chooses the master node to route the sql query

    Parameters:
    query (string): SQL query to run

    Returns:
    string: returns string cast of output from the routed query from routeQuery()
    """
    nodeIndex = 0

    print("Request sent to ", nodeIndex)
    return routeQuery(nodeIndex, query)

def proxyPing(query):
    """Pings all nodes and chooses the one with the lowest latency
    
    Parameters:
    query (string): SQL query to run

    Returns:
    string: returns string cast of output from the routed query from routeQuery()
    """
    pingLatencies = getNodePings()
    nodeIndex = pingLatencies.index(min(pingLatencies))

    print("Request sent to ", nodeIndex)
    return routeQuery(nodeIndex, query)

def getNodePings():
    """Pings all nodes and returns average latencies parsed from response
    
    Returns:
    Array<float>: returns array of latencies recorded from nodes
    """
    latencies = []
    for nodeIP in nodes:
        ping = subprocess.Popen(['ping', '-c', '1', nodeIP], stdout= subprocess.PIPE)
        output = str(ping.communicate()[0])
        time = re.search('(min\/avg\/max\/mdev = )(.*)', output).group(2).split('/')[1]
        latencies.append(time)
    return latencies

#routes query to specific node and executes it
def routeQuery(nodeIndex, query):
    """Opens tunnel to specific node, connects to SQL database and executes query,
    closes MySQL connection and tunnels after response.
    
    Parameters:
    nodeIndex (int): identifies the node to tunnel to
    query (string): SQL query to run

    Returns:
    string: returns string cast the dataframe returned from the query
    """
    openTunnel(nodeIndex)
    mysqlConnect(nodeIndex)
    queryResults = execQuery(query)
    sqlConnection.close()
    tunnel.stop()
    return str(queryResults)

#Test queries to run locally
# curl 127.0.0.1:5000/sql-random?query=select+*+from+actor+limit+10
# curl 127.0.0.1:5000/sql-default?query=select+*+from+actor+limit+10
# curl 127.0.0.1:5000/sql-ping?query=select+*+from+actor+limit+10