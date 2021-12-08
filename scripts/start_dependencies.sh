#!/usr/bin/env bash
echo "starting zookeeper server"
current_dir=$(pwd)
cd ~/Downloads/apache-zookeeper-3.7.0-bin/bin
sudo ./zkServer.sh start

sleep 5

echo "starting elasticsearch"
sudo service elasticsearch restart

echo "starting potgresql"
sudo docker run --name net_protector_pg -e POSTGRES_PASSWORD=postgres -v /home/pcs/pg-data/:/var/lib/postgresql/data -p 5432:5432 -d postgres:13

echo "starting kafka server"
cd ~/Downloads/kafka_2.13-3.0.0/bin
./kafka-server-start.sh ../config/server.properties
