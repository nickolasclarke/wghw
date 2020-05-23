#!/bin/bash
set -ex
no_target_err="Error: No target directory supplied. Syntax: ./run.sh <target directory path>"
[ -z "$1" ] && echo $no_target_err && exit 1
docker-compose build
TARGET=$1 docker-compose up