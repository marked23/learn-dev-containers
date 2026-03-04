# Start from NVIDIA's PyTorch image (CUDA 12.8, Python 3.12)
FROM nvcr.io/nvidia/pytorch:25.01-py3

# Install additional system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        jq \
        tree \
    && rm -rf /var/lib/apt/lists/*
