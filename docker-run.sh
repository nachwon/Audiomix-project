#!/bin/bash
docker build -t audiomix -f Dockerfile .
docker run --rm -it -p 8013:80