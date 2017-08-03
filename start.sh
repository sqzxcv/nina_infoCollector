#!/bin/bash

export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh

git pull

workon scrapyd_py3.6.1 
pip install -r requirements.txt
echo "当前执行路径" + $(pwd)
pm2 reload ecosystem.config.js --env production
# pm2 reload start.py -x --interpreter /root/Envs/scrapyd_py3.6.1/bin/python