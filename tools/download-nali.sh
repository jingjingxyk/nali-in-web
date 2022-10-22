#!/bin/bash

set -eux

__DIR__=$(
  cd "$(dirname "$0")"
  pwd
)
cd ${__DIR__}

# example use proxy download source code
# shell之变量默认值  https://blog.csdn.net/happytree001/article/details/120980066
# 使用代理下载源码
# sh build-docker.sh --proxy 'http://127.0.0.1:8015'

PROXY_URL=${2:+'http://127.0.0.1:8015'}

export http_proxy=$PROXY_URL
export https_proxy=$PROXY_URL

curl -LO https://github.com/zu1k/nali/releases/download/v0.7.0/nali-linux-amd64-v0.7.0.gz
gzip -d nali-linux-amd64-v0.7.0.gz
chmod a+x nali-linux-amd64-v0.7.0