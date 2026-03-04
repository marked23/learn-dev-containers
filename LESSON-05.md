# Lesson 5: Lifecycle Scripts

## Three Layers of Setup — And a Gap

So far we've built our environment in layers:

1. **Base image** (`FROM`) — the OS, Python, PyTorch
2. **Dockerfile `RUN`** — system packages like `jq`, `tree`
3. **Features** — tools like `gh` CLI

All three are baked into the image at build time. But what about setup that depends on your *project* — like installing Python packages from `requirements.txt` or running a database migration? Those can't go in the Dockerfile because they depend on your source code, which isn't available during the image build.

That's the gap lifecycle scripts fill.

## The Lifecycle Timeline

Here's when each hook fires, in order:

```
1. initializeCommand    ← runs on your HOST machine, before anything else
2. Docker builds the image (Dockerfile + Features)
3. Container is created from the image
4. onCreateCommand      ← runs inside the container, once, on first creation
5. updateContentCommand ← runs after onCreateCommand (and on later content updates)
6. postCreateCommand    ← runs after updateContentCommand, once, on first creation
7. postStartCommand     ← runs every time the container starts
8. postAttachCommand    ← runs every time VS Code attaches to the container
```

In practice, you'll mostly use three of these.

## The Three You'll Actually Use

### `postCreateCommand` — The Workhorse

Runs once, after the container is created. This is where you install project dependencies:

```json
{
  "postCreateCommand": "pip install -r requirements.txt"
}
```

**When it runs:** After the first "Reopen in Container" or "Rebuild Container." Not on subsequent starts — only on creation.

**Use it for:** `pip install`, `npm install`, `cargo build`, database setup, any one-time project initialization.

### `postStartCommand` — Every Boot

Runs every time the container starts (including the first time):

```json
{
  "postStartCommand": "echo 'Container started at' $(date)"
}
```

**When it runs:** Every start. If you stop and restart the container, this fires again.

**Use it for:** Starting background services, refreshing tokens, printing status info.

### `postAttachCommand` — Every VS Code Connection

Runs each time VS Code attaches to the container:

```json
{
  "postAttachCommand": "git status"
}
```

**When it runs:** Every time VS Code connects — including reconnects after a window reload.

**Use it for:** Displaying a welcome message, checking environment health.

## The Two You Might Occasionally Use

### `initializeCommand` — Runs on the Host

Runs on your local machine *before* the container is built:

```json
{
  "initializeCommand": "echo 'About to build the dev container...'"
}
```

**Use it for:** Checking prerequisites on the host, pulling credentials, generating config files that the build needs.

### `onCreateCommand` — First Creation Only

Similar to `postCreateCommand` but runs earlier in the sequence. In practice, `postCreateCommand` is more commonly used because it runs after everything else is set up.

## Multiple Commands

You can chain commands with `&&`:

```json
{
  "postCreateCommand": "pip install -r requirements.txt && python setup.py"
}
```

Or use an array for clarity (each element runs sequentially):

```json
{
  "postCreateCommand": ["pip install -r requirements.txt", "python setup.py"]
}
```

Or use an object to run commands in parallel with labels:

```json
{
  "postCreateCommand": {
    "python-deps": "pip install -r requirements.txt",
    "node-deps": "npm install"
  }
}
```

The object form is nice for multi-language projects where installs don't depend on each other.

## What Happens on Rebuild?

| Event | What fires |
|---|---|
| First "Reopen in Container" | All hooks in order |
| Stop and restart container | `postStartCommand` + `postAttachCommand` |
| Reload VS Code window | `postAttachCommand` only |
| "Rebuild Container" | All hooks in order (it's a fresh container) |

This is why `postCreateCommand` is the right place for `pip install` — it only runs when the container is new, not on every start.

## A Practical Example

Let's add a `requirements.txt` and a `postCreateCommand` to our project so Python dependencies install automatically.

## Our Updated Config

```json
{
  "name": "Learn Dev Containers",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": ["anthropic.claude-code"],
      "settings": {
        "editor.formatOnSave": true,
        "files.trimTrailingWhitespace": true
      }
    }
  },
  "mounts": [
    "source=devcontainers-extensions,target=/root/.vscode-server/extensions,type=volume",
    "source=claude-config,target=/root/.claude,type=volume"
  ]
}
```

## Try It

After rebuilding, check that the packages from `requirements.txt` are installed:

```bash
pip list    # should show requests and any other packages listed
```

Edit `requirements.txt`, add a new package, then Rebuild Container — the `postCreateCommand` runs again and picks it up.

## Key Takeaways

- Lifecycle scripts automate project setup that can't be baked into the image
- `postCreateCommand` is the most important — use it for dependency installation
- `postStartCommand` runs on every start; `postAttachCommand` on every VS Code attach
- Commands can be strings, arrays (sequential), or objects (parallel)
- These scripts run inside the container, except `initializeCommand` which runs on the host
