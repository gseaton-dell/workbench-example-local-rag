#!/bin/bash
set -e

# Install deps to run the API in a seperate venv to isolate different components
conda create --name api-env -y python=3.10 pip
/opt/conda/envs/api-env/bin/pip install fastapi==0.109.2 uvicorn[standard]==0.27.0.post1 python-multipart==0.0.7 langchain==0.0.335 langchain-community==0.0.19 openai==1.11.1 unstructured[all-docs]==0.12.4 sentence-transformers==2.3.1 llama-index==0.9.44 dataclass-wizard==0.22.3 pymilvus==2.3.1 opencv-python==4.8.0.76 hf_transfer==0.1.5 text_generation==0.6.1

# Install deps to run the UI in a seperate venv to isolate different components
conda create --name ui-env -y python=3.10 pip
/opt/conda/envs/ui-env/bin/pip install dataclass_wizard==0.22.2 gradio==4.2.0 jinja2==3.1.2 numpy==1.25.2 protobuf==3.20.3 PyYAML==6.0 uvicorn==0.22.0

jupyter labextension disable "@jupyterlab/apputils-extension:announcements"

jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
