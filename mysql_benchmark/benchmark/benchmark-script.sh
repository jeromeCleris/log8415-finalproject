#!/bin/bash
# Script to run locally to benchmark standalone MySQL and cluster
# Requires sysbench package installed

echo "Running benchmark on standalone MySQL instance:"

echo "Username: "
read user

echo "Password: "
read -s password

echo "MySql server Ip address: "
read ip_address

sysbench oltp_read_write --table-size=1000000 --mysql-host=$ip_address --mysql-db=sakila --mysql-user=$user --mysql-password=$password prepare
sysbench oltp_read_write --table-size=1000000 --threads=6 --time=60 --mysql-host=$ip_address --mysql-db=sakila --mysql-user=$user --mysql-password=$password run