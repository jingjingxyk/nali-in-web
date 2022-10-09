#!/bin/bash

set -eux

__DIR__=$(
  cd "$(dirname "$0")"
  pwd
)
cd ${__DIR__}
. venv/bin/activate
python3 -u src/NaliWrap.py

exit 0
socat -d -d -d  TCP-LISTEN:8080,fork,reuseaddr SYSTEM:"python3 src/NaliWrap.py"
# ,crlf,crlf