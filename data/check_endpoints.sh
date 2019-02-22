#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" -d @move.json localhost:8080/move
curl -X POST -H "Content-Type: application/json" -d @start.json localhost:8080/start
