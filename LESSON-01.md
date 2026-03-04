# Lesson 1: Foundation — What Dev Containers Actually Are

## The Architecture

When you click "Reopen in Container," VS Code splits itself in two:

```
┌─────────────────────────┐      ┌──────────────────────────────┐
│     YOUR MACHINE        │      │      DOCKER CONTAINER        │
│                         │      │                              │
│  VS Code UI (window)    │◄────►│  VS Code Server              │
│  (runs natively)        │      │  (runs inside container)     │
│                         │      │                              │
│  Your project files ────┼──────┼► /workspaces/your-project    │
│  (on your disk)         │ mount│  (visible inside container)  │
│                         │      │                              │
│                         │      │  Terminal, debugger, linter,  │
│                         │      │  language runtime — all here │
└─────────────────────────┘      └──────────────────────────────┘
```

- **The UI** stays on your host machine (the window you see)
- **The Server** runs inside the container (file ops, terminal, extensions, language features)

It feels like normal VS Code because it *is* — the UI just talks to a server that happens to be inside a container.

## The Specification

Dev containers are an open specification at [containers.dev](https://containers.dev), not a VS Code-only feature. GitHub Codespaces, JetBrains, and the standalone CLI all support the same spec.

## The Minimal Config

Created at `.devcontainer/devcontainer.json`:

```json
{
  "name": "Learn Dev Containers",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu"
}
```

Two fields are all you need:
- **`name`** — human-readable label, shown in the VS Code window title
- **`image`** — the Docker image. The `base:ubuntu` image is Microsoft's starter image with git, curl, and a non-root `vscode` user pre-installed

## Try It

1. Open this folder in VS Code
2. `Ctrl+Shift+P` → "Reopen in Container"
3. Wait for the image to pull and container to build (first time only)

Once inside, open the terminal and verify:
- `whoami` → `vscode` (default non-root user)
- `cat /etc/os-release` → Ubuntu
- `pwd` → `/workspaces/learn-dev-containers`
- `ls` → your project files, mounted from the host

## Getting Back Out

`Ctrl+Shift+P` → "Reopen Folder Locally" — returns to your normal local environment. The container stops but isn't deleted, so reopening is fast next time.

## Key Takeaways

- VS Code runs its server inside the container; only the UI is on your host
- Your files are mounted in, not copied — changes are reflected immediately on both sides
- The entire dev environment is defined by one JSON file that lives in your repo
- Dev containers are an open spec, not locked to any single editor
