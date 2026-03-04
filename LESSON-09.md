# Lesson 9: The Dev Container CLI

## Dev Containers Without VS Code

Everything so far has been through VS Code — "Reopen in Container," "Rebuild Container," etc. But dev containers aren't a VS Code feature. They're an open spec, and there's a standalone CLI that works with any terminal, any editor, and any CI system.

## Installing the CLI

The CLI is an npm package:

```bash
npm install -g @devcontainers/cli
```

After installation, you have the `devcontainer` command available globally.

(If you don't have Node/npm on your host, you can also install it via Homebrew: `brew install devcontainer`)

## The Core Commands

### `devcontainer up` — Start a Container

```bash
devcontainer up --workspace-folder .
```

This reads your `.devcontainer/devcontainer.json`, builds the image (if using a Dockerfile), creates the container, runs lifecycle scripts, and leaves it running. Equivalent to VS Code's "Reopen in Container" — minus the editor.

### `devcontainer exec` — Run Commands Inside

```bash
devcontainer exec --workspace-folder . python3 --version
devcontainer exec --workspace-folder . pip list
devcontainer exec --workspace-folder . bash
```

Runs a command inside the running container. The last example drops you into an interactive shell.

### `devcontainer build` — Build the Image Only

```bash
devcontainer build --workspace-folder .
```

Builds the image without creating or starting a container. Useful for pre-building images so that `devcontainer up` is faster later, or for validating that your Dockerfile and features work.

## Why Use the CLI?

### 1. CI/CD Pipelines

Your dev container defines your development environment. Why not use that same environment to run your tests in CI? Instead of maintaining a separate CI config that installs the same tools, just reuse the dev container:

```yaml
# GitHub Actions example
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: devcontainers/ci@v0.3
        with:
          runCmd: pytest
```

The `devcontainers/ci` GitHub Action builds your dev container and runs commands inside it. Your CI environment is identical to your dev environment — no more "tests pass locally but fail in CI."

### 2. Editor Independence

Not everyone on your team uses VS Code. The CLI lets anyone use the dev container:

```bash
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash
# Now you're inside the container — use vim, emacs, whatever
```

### 3. Scripting and Automation

Need to run a batch job using your dev environment?

```bash
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . python3 train_model.py
```

Or validate your container builds correctly before pushing changes:

```bash
devcontainer build --workspace-folder . && echo "Build succeeded"
```

## Other Useful Commands

```bash
devcontainer features list          # browse available features
devcontainer templates list         # browse starter templates
devcontainer read-configuration \
  --workspace-folder .              # show the resolved config (after merging defaults)
```

`read-configuration` is handy for debugging — it shows you the final merged config including all defaults that aren't explicit in your `devcontainer.json`.

## Pre-Building Images

For large images (like ours — ROCm/PyTorch is big), the first `devcontainer up` is slow because it pulls and builds everything. You can pre-build and push to a registry:

```bash
# Build and tag the image
devcontainer build --workspace-folder . --image-name myregistry/myproject-dev:latest

# Push to a container registry
docker push myregistry/myproject-dev:latest
```

Then teammates (or CI) pull the pre-built image instead of building from scratch. First startup goes from minutes to seconds.

## How It Relates to Everything We've Learned

The CLI reads the same `devcontainer.json` we've been building throughout this course:

| What we configured | How the CLI uses it |
|---|---|
| `"build": { "dockerfile": "Dockerfile" }` | `devcontainer build` builds this image |
| `"features"` | Installed during `devcontainer up` |
| `"postCreateCommand"` | Runs after `devcontainer up` creates the container |
| `"forwardPorts"` | Port forwarding (though without VS Code UI, you'd use Docker port flags) |
| `"mounts"` | Volumes are created and attached |

Everything works. The CLI just skips the VS Code parts (extensions, settings, editor UI).

## No Config Changes

This is a tools lesson — nothing to change in `devcontainer.json`. The config we've built works with both VS Code and the CLI.

## Key Takeaways

- The `devcontainer` CLI runs dev containers without VS Code
- `devcontainer up` starts, `devcontainer exec` runs commands inside, `devcontainer build` builds the image
- Use it in CI/CD to run tests in the same environment you develop in
- Use it for editor independence — not everyone needs VS Code
- Pre-build images and push to a registry for faster startup across your team
- Your existing `devcontainer.json` works with the CLI unchanged
