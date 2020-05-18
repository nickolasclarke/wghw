#!/bin/bash
docker-compose build
TARGET=$1 docker-compose up