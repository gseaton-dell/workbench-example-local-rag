#!/bin/bash

pkill -SIGINT -f '/opt/conda/bin/milvus-server'
pkill -SIGINT -f "^text-generation-server download-weights"
pkill -SIGINT -f '^text-generation-launcher'
# pkill -SIGINT -f '^/opt/conda/envs/ui-env/bin/python3 -m chatui'
pkill -SIGINT -f '^/opt/conda/envs/api-env/bin/python -m uvicorn chain_server.server:app'