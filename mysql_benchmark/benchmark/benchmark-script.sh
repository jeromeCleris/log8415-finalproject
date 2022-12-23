#!/bin/bash
# Script to run locally to benchmark standalone MySQL and cluster
# Requires sysbench package installed and sysbench user created on each databases
# Requires possible remote access

echo "Running benchmark on standalone MySQL instance:"

# Gathering inputs for standalone instance access
echo "Username: "
read user

echo "Password: "
read -s password

echo "MySql server Ip address: "
read ip_address

#Preparing/running/cleaning benchmark workload
sysbench oltp_read_write --table-size=1000000 --mysql-host=$ip_address --mysql-db=sakila --mysql-user=$user --mysql-password=$password prepare
sysbench oltp_read_write --table-size=1000000 --threads=6 --time=60 --mysql-host=$ip_address --mysql-db=sakila --mysql-user=$user --mysql-password=$password run
sysbench oltp_read_write --mysql-host=$ip_address --mysql-db=sakila --mysql-user=$user --mysql-password=$password cleanup

echo "Running benchmark on cluster:"
# Gathering inputs for cluster access
echo "Username: "
read user_cluster

echo "Password: "
read -s password_cluster

echo "MySql server Ip address: "
read ip_address_cluster

#Preparing/running/cleaning benchmark workload
sysbench oltp_read_write --table-size=1000000 --mysql-host=$ip_address_cluster --mysql-db=sakila --mysql-user=$user_cluster --mysql-password=$password_cluster prepare
sysbench oltp_read_write --table-size=1000000 --threads=6 --time=60 --mysql-host=$ip_address_cluster --mysql-db=sakila --mysql-user=$user_cluster --mysql-password=$password_cluster run
sysbench oltp_read_write --mysql-host=$ip_address_cluster --mysql-db=sakila --mysql-user=$user_cluster --mysql-password=$password_cluster cleanup
