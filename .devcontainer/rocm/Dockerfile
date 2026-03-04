# Start from our ROCm/PyTorch base image
FROM rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.7.1

# Install additional system packages
# apt-get update refreshes the package index
# apt-get install -y installs without prompting for confirmation
# rm -rf /var/lib/apt/lists/* cleans up to keep the image smaller
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        jq \
        tree \
    && rm -rf /var/lib/apt/lists/*
