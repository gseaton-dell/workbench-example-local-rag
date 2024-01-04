#!/bin/bash
set -e

# Install deps to run the API in a seperate venv to isolate different components
conda create --name api-env -y python=3.10 pip
/opt/conda/envs/api-env/bin/pip install fastapi uvicorn[standard] python-multipart langchain==0.0.335 openai==0.28.1 unstructured[all-docs] sentence-transformers llama-index==0.8.28 dataclass-wizard pymilvus==2.3.1 opencv-python==4.8.0.76 hf_transfer text_generation

# Install deps to run the UI in a seperate venv to isolate different components
conda create --name ui-env -y python=3.10 pip
/opt/conda/envs/ui-env/bin/pip install dataclass_wizard==0.22.2 gradio==3.39.0 jinja2==3.1.2 numpy==1.25.2 protobuf==3.20.3 PyYAML==6.0 uvicorn==0.22.0

jupyter labextension disable "@jupyterlab/apputils-extension:announcements"

jupyter labextension disable "@jupyterlab/apputils-extension:announcements"