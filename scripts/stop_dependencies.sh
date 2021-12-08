#!/usr/bin/env bash
echo "stopping zookeeper server"
current_dir=$(pwd)
cd ~/Downloads/apache-zookeeper-3.7.0-bin/bin
sudo ./zkServer.sh stop

sleep 5

echo "stopping elasticsearch"
sudo service elasticsearch stop

echo "stopping potgresql"
sudo docker stop net_protector_pg
sudo docker rm net_protector_pg

echo "stopping kafka"
cd ~/Downloads/kafka_2.13-3.0.0/bin
./kafka-server-stop.sh ../config/server.properties
