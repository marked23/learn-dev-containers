# Lesson 10: Multiple Container Configurations

## One Repo, Multiple Environments

So far we've had a single `devcontainer.json` defining one environment. But what if your project needs to run on different hardware, different runtimes, or different toolchains? The dev container spec supports multiple configurations in the same repository.

## Why Multiple Configs?

**Different hardware targets.** Our repo is a perfect example — we have an AMD GPU (ROCm) and an NVIDIA GPU (CUDA) in the same machine. Each requires a different base image, different drivers, and different runtime flags. One `devcontainer.json` can't serve both.

**Other real-world scenarios:**

- **Frontend vs. backend** — a Node.js container for the React app, a Python container for the API server
- **Different language versions** — test your library against Python 3.10, 3.11, and 3.12
- **Lightweight vs. full** — a minimal container for quick edits and a heavy container with all debugging tools
- **OS variants** — Ubuntu vs. Alpine vs. Fedora for compatibility testing

## The Directory Structure

Instead of a single `.devcontainer/devcontainer.json`, you create named subdirectories:

```
.devcontainer/
├── rocm/
│   ├── devcontainer.json
│   └── Dockerfile
└── nvidia/
    ├── devcontainer.json
    └── Dockerfile
```

Each subdirectory is a self-contained configuration. The directory name becomes the label VS Code shows when it asks which container to open.

Here's what our two configs look like side by side:

| | ROCm | NVIDIA |
|---|---|---|
| **Base image** | `rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.7.1` | `nvcr.io/nvidia/pytorch:25.01-py3` |
| **Runtime flags** | `--device=/dev/kfd --device=/dev/dri --group-add=video` | `--gpus=all` |
| **Extra env vars** | `HSA_OVERRIDE_GFX_VERSION=11.0.0` | (none) |
| **Everything else** | Identical | Identical |

The `customizations`, `features`, `mounts`, `forwardPorts`, and `postCreateCommand` are the same in both. Only the hardware-specific pieces differ. This is the power of multiple configs — share what's common, vary what must be different.

## How VS Code Discovers Configs

VS Code looks for dev container configurations in this order:

1. `.devcontainer/devcontainer.json` — single config (what we used in earlier lessons)
2. `.devcontainer/<name>/devcontainer.json` — multiple named configs

When it finds named subdirectories, it presents a picker so you can choose which environment to open.

## Switching Between Containers in VS Code

This is a two-step process. There is no single "switch container" command — you must exit the current container first, then enter the new one.

### Step 1: Exit the current container

Open the Command Palette (`Ctrl+Shift+P`) and run:

```
Dev Containers: Reopen Folder Locally
```

This closes the container connection and reopens your project on the local filesystem.

### Step 2: Enter the new container

Open the Command Palette again (`Ctrl+Shift+P`) and run:

```
Dev Containers: Reopen in Container
```

VS Code will show a picker listing your named configurations (e.g., "rocm" and "nvidia"). Select the one you want.

### Why two steps?

When you're already inside a container, VS Code doesn't show "Reopen in Container" — it only shows "Reopen Folder Locally." You have to go local first, then choose a new container. It's a known limitation of the current workflow.

## A Practical Example: Our Benchmark

We ran the same `benchmark.py` (matrix multiplication) in both containers without changing a single line of code:

```
# ROCm container — integrated AMD GPU
Device: AMD Radeon Graphics
  1024: 2.7x speedup
  8192: 2.4x speedup

# NVIDIA container — dedicated RTX 5050
Device: NVIDIA GeForce RTX 5050 Laptop GPU
  1024: 29.3x speedup
  8192: 15.2x speedup
```

Same code, same repo, different containers, different hardware. The dev container abstraction made the switch seamless.

## Tips for Multiple Configs

**Use distinct volume names.** Notice our ROCm config mounts `source=devcontainers-extensions` while NVIDIA uses `source=devcontainers-extensions-nvidia`. If both configs shared the same volume name, VS Code extensions compiled for one environment could corrupt the other.

**Keep configs DRY where possible.** If your configs share a lot of common setup, consider a shared `requirements.txt` or shared scripts at the repo root that both `postCreateCommand` hooks can reference. Our both configs already do this — they both run `pip install -r requirements.txt` from the same file.

**Name your containers clearly.** The `"name"` field in each `devcontainer.json` appears in the VS Code title bar. Ours say "Learn Dev Containers (ROCm)" and "Learn Dev Containers (NVIDIA)" so you always know which environment you're in.

## Key Takeaways

- Multiple configs live in named subdirectories under `.devcontainer/`
- Each subdirectory contains its own `devcontainer.json` (and optionally its own `Dockerfile`)
- VS Code presents a picker when multiple configs exist
- Switching containers requires two steps: reopen locally, then reopen in the new container
- Use distinct volume names to keep container-specific data separated
- The same application code runs unchanged across different container environments
