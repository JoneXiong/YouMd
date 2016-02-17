#!/bin/bash

#ps aux|grep server.py | grep -v grep|awk '{print $2}'|xargs kill -9
nohup python server.py -port 8081  &
