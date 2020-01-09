#!/bin/bash

docker run \
    -d \
    -ti \
    --rm \
    --mount type=bind,source=/tmp,target=/tmp \
    --name collectordb -p 50000:50000 collector/db
