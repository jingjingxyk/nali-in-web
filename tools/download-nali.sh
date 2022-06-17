#!/bin/bash

set -eux

__DIR__=$(
  cd "$(dirname "$0")"
  pwd
)
cd ${__DIR__}

# export http_proxy=http://127.0.0.1:8015
# export https_proxy=http://127.0.0.1:8015

curl -LO https://github.com/zu1k/nali/releases/download/v0.4.2/nali-linux-amd64-v0.4.2.gz
gzip -d nali-linux-amd64-v0.4.2.gz
chmod a+x nali-linux-amd64-v0.4.2