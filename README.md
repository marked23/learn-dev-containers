# Learn Dev Containers

A hands-on curriculum for learning [Dev Containers](https://containers.dev/) from the ground up — from "what are these?" to multi-container, multi-GPU configurations.

## What's Inside

**11 progressive lessons** covering every major dev container concept:

| Lesson | Topic |
|--------|-------|
| 0 | Where Dev Containers Fit in Your Workflow |
| 1 | Foundation — What Dev Containers Actually Are |
| 2 | devcontainer.json — The Central Config File |
| 3 | Images & Dockerfiles |
| 4 | Features — Composable Add-Ons |
| 5 | Lifecycle Scripts |
| 6 | Port Forwarding |
| 7 | Volumes & Mounts |
| 8 | Docker Compose Integration |
| 9 | The Dev Container CLI |
| 10 | Multiple Container Configurations |

See [CURRICULUM.md](CURRICULUM.md) for a detailed overview of each lesson's learning objectives.

## GPU Support: NVIDIA and AMD

This repo includes two dev container configurations under `.devcontainer/`, one for each major GPU stack:

| Configuration | Base Image | GPU Stack |
|---------------|-----------|-----------|
| `.devcontainer/nvidia/` | `nvcr.io/nvidia/pytorch:25.01-py3` | CUDA 12.8 |
| `.devcontainer/rocm/` | `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.7.1` | ROCm 7.2 |

Both configurations include PyTorch, GitHub CLI, and the Claude Code VS Code extension.

**If you have both an NVIDIA and AMD GPU in the same machine**, this works fine — you choose which container to open. When VS Code prompts you to reopen in a container, it will show both configurations by name ("Learn Dev Containers (NVIDIA)" and "Learn Dev Containers (ROCm)"). Pick the one matching the GPU you want to use, and the container will be configured with the appropriate drivers, device passthrough, and runtime.

### Opening a Configuration

1. Open this repo in VS Code
2. Press `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**
3. If multiple configurations exist, VS Code will ask you to choose — select **NVIDIA** or **ROCm**

## Practical Examples

- **`server.py`** — A minimal web server for testing port forwarding (Lesson 6)
- **`benchmark.py`** — CPU vs GPU matrix multiplication benchmark that detects your hardware and compares NumPy (CPU) against PyTorch (GPU) performance

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- For NVIDIA: the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- For AMD: ROCm-compatible GPU and kernel drivers ([ROCm installation guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/))

## Getting Started

```bash
git clone <this-repo>
code learn-dev-containers
```

Then use **Reopen in Container** from the command palette. Once inside the container, try:

```bash
# Test port forwarding (Lesson 6)
python server.py

# Run the GPU benchmark
python benchmark.py
```

Start reading from [LESSON-00.md](LESSON-00.md) and work through at your own pace.
