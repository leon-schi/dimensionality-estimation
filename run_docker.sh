#!/bin/bash

mkdir results
docker build -t rw_experiments --no-cache --network=host .
docker run -v $(pwd)/results:/results rw_experiments:latest
