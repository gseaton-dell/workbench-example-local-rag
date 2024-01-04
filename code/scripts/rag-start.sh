#!/bin/bash

# Start milvus
echo "Starting Milvus"
/opt/conda/bin/milvus-server --data /mnt/milvus/ &
pid1=$!

# Start API
echo "Starting API"
cd /project/code/ && /opt/conda/envs/api-env/bin/python -m uvicorn chain_server.server:app --port=8000 --host='0.0.0.0' &
pid2=$!

# Start Inference Server
echo "Starting Inference Server"
text-generation-launcher --model-id $MODEL_ID --port 9090 &
pid3=$!


# Now, wait for each command to complete
if ! wait $pid1; then
    echo "Milvus failed"
    exit 1
fi

if ! wait $pid2; then
    echo "API failed"
    exit 1
fi

if ! wait $pid3; then
    echo "Inference server failed"
    exit 1
fi

echo "RAG system ready"
