#!/bin/bash

set -eux

__DIR__=$(
  cd "$(dirname "$0")"
  pwd
)
cd ${__DIR__}

socat -d -d  TCP-LISTEN:8080,fork,reuseaddr,reuseport SYSTEM:"python3 src/NaliWrap.py"
