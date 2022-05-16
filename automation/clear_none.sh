#!/bin/bash
# to clear dangling none images after rebuilding several times
# run on remote
sudo docker rmi $(sudo docker images -f "dangling=true" -q)