# Lesson 2: devcontainer.json — The Central Config File

## The Rebuild Problem (Learned the Hard Way)

When you "Rebuild Container," Docker destroys the old container and creates a new one. Anything stored inside the container's filesystem is gone — including Claude sessions, installed extensions, and any other state.

The fix: **named volumes** that store data outside the container:

```json
"mounts": [
  "source=devcontainers-extensions,target=/home/vscode/.vscode-server/extensions,type=volume",
  "source=claude-config,target=/home/vscode/.claude,type=volume"
]
```

Docker manages these volumes separately from the container, so they survive rebuilds. More on mounts in Lesson 7.

## How VS Code Finds the File

VS Code looks in this order:
1. `.devcontainer/devcontainer.json` — the standard location (what we're using)
2. `.devcontainer.json` — in the project root (less common)
3. `.devcontainer/<subfolder>/devcontainer.json` — multiple configs; VS Code prompts you to choose

## Container Source (Pick One)

You always need exactly one of these — they're mutually exclusive:

| Field | Purpose |
|-------|---------|
| `"image"` | Use a pre-built Docker image directly |
| `"build": { "dockerfile": "Dockerfile" }` | Build from a custom Dockerfile (Lesson 3) |
| `"dockerComposeFile"` | Use Docker Compose for multi-container (Lesson 8) |

## Customizations: Extensions and Settings

```json
"customizations": {
  "vscode": {
    "extensions": [
      "streetsidesoftware.code-spell-checker",
      "anthropic.claude-code"
    ],
    "settings": {
      "editor.formatOnSave": true,
      "files.trimTrailingWhitespace": true
    }
  }
}
```

- **Extensions** are installed inside the container automatically. Teammates get the same tools without manual setup.
- **Settings** override your local VS Code settings inside the container only. Your local config is untouched.

Extension IDs are the `publisher.extension-name` strings from the VS Code marketplace.

## Picking a Base Image

Microsoft maintains images designed for dev containers:

| Image | Use case |
|-------|----------|
| `mcr.microsoft.com/devcontainers/base:ubuntu` | General-purpose (what we're using) |
| `mcr.microsoft.com/devcontainers/typescript-node` | Node.js + TypeScript |
| `mcr.microsoft.com/devcontainers/python` | Python |
| `mcr.microsoft.com/devcontainers/rust` | Rust |
| `mcr.microsoft.com/devcontainers/go` | Go |

These come with a non-root `vscode` user, common CLI tools (git, curl), and are optimized for dev container use. Browse them at [containers.dev/collections](https://containers.dev/collections).

You can use any Docker image (e.g., `ubuntu:24.04`), but you'd lose the dev-container-friendly defaults.

## Other Useful Fields

| Field | Purpose |
|-------|---------|
| `"features"` | Composable add-on tools (Lesson 4) |
| `"postCreateCommand"` | Run after container creation (Lesson 5) |
| `"forwardPorts"` | Expose container ports to host (Lesson 6) |
| `"mounts"` | Additional volumes/bind mounts (Lesson 7) |
| `"remoteUser"` | Which user to run as (defaults to `vscode`) |
| `"containerEnv"` | Environment variables in the container |
| `"remoteEnv"` | Environment variables for VS Code's processes only |

## Rebuild vs. Reopen

- **Reopen in Container** — starts an existing container or creates one. Fast.
- **Rebuild Container** — destroys and recreates from scratch. Use when you change `devcontainer.json`. Loses anything not in a volume.
- **Rebuild Without Cache** — re-pulls image, ignores Docker layer cache. Nuclear option.

"Reopen" is turning the car on. "Rebuild" is getting a new car.

## Key Takeaways

- `devcontainer.json` is the single source of truth for the dev environment
- You choose one base (image, Dockerfile, or Compose) and layer everything else on top
- Anything you want to survive a rebuild must be in a volume or mount
- Extensions and settings travel with the project, not with the developer
- After editing the config, **Rebuild Container** to apply changes
