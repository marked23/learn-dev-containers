# Lesson 3: Images & Dockerfiles

## What We Had

Up to now, our `devcontainer.json` used `"image"` to pull a pre-built image directly:

```json
{
  "image": "rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.7.1"
}
```

Docker pulls the image as-is. No build step, no customization at the Docker layer.

## The Problem

What if you need system packages that aren't in your base image? For example, `jq` (a JSON processor) or `tree` (directory visualization). You could install them manually every time the container is created, but that defeats the purpose of a reproducible environment.

## The Solution: A Dockerfile

Instead of pointing `devcontainer.json` at an image, point it at a Dockerfile that *starts from* your image and adds what you need.

### Step 1: Create `.devcontainer/Dockerfile`

```dockerfile
FROM rocm/pytorch:rocm7.2_ubuntu24.04_py3.12_pytorch_release_2.7.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        jq \
        tree \
    && rm -rf /var/lib/apt/lists/*
```

Line by line:
- **`FROM`** — the base image. This is the same image we were using before.
- **`RUN`** — executes a command during the build. Here we install two packages.
- **`apt-get update`** — refreshes the package index so `apt` knows what's available.
- **`--no-install-recommends`** — skip optional packages to keep the image smaller.
- **`rm -rf /var/lib/apt/lists/*`** — clean up the package index cache. It's only needed during install.

The `\` and `&&` chain everything into a single `RUN` layer. Fewer layers = smaller image — because the cleanup (`rm -rf`) happens in the same layer as the install, so the deleted files never occupy space in the final image.

You can use multiple `RUN` lines for readability — group them by purpose:

```dockerfile
# System packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends jq tree \
    && rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip install numpy pandas

# Configuration
RUN echo "alias ll='ls -la'" >> /root/.bashrc
```

Each `RUN` gets its own cached layer, so changing your pip packages won't re-run the apt install.

### Why `apt-get` and not `apt`?

In your terminal, `apt` is nicer — it has progress bars and color. But `apt` itself warns: *"apt does not have a stable CLI interface."* Its output format can change between versions. `apt-get` has a stable, scriptable interface — use it in Dockerfiles and any other automated scripts.

### Step 2: Update `devcontainer.json`

Replace `"image"` with `"build"`:

```json
{
  "build": {
    "dockerfile": "Dockerfile"
  }
}
```

The `"dockerfile"` path is relative to the `.devcontainer/` directory. Since our Dockerfile is at `.devcontainer/Dockerfile`, just `"Dockerfile"` works.

## `"image"` vs `"build"` — When to Use Which

| Use `"image"` when... | Use a Dockerfile when... |
|---|---|
| The base image already has everything you need | You need extra system packages |
| You want the fastest possible container startup | You need to match a production base image |
| You're prototyping or experimenting | You need reproducible, pinned system deps |
| Features (Lesson 4) can fill the gaps | You need OS-level configuration changes |

Rule of thumb: **start with `"image"`, switch to a Dockerfile when you need something `"image"` alone can't give you.**

## How the Build Cache Works

Docker caches each layer (each `FROM`, `RUN`, `COPY`, etc.). When you rebuild:

1. If a layer hasn't changed, Docker reuses the cached version — instant.
2. If a layer changes, Docker rebuilds *that layer and everything after it*.

This means order matters in your Dockerfile. Put things that change rarely (base image, system packages) at the top and things that change often at the bottom.

```
FROM ...           ← rarely changes (cached)
RUN apt-get ...    ← rarely changes (cached)
COPY . .           ← changes often (rebuilt every time)
```

## Build Arguments (Optional)

You can pass build-time variables:

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "args": {
      "EXTRA_PACKAGES": "htop vim"
    }
  }
}
```

And use them in the Dockerfile:

```dockerfile
ARG EXTRA_PACKAGES=""
RUN apt-get update && apt-get install -y $EXTRA_PACKAGES
```

This keeps the Dockerfile flexible without hardcoding choices.

## What Changed in Our Config

Our full `devcontainer.json` now looks like this:

```json
{
  "name": "Learn Dev Containers",
  "build": {
    "dockerfile": "Dockerfile"
  },
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

The only change: `"image": "rocm/pytorch:..."` became `"build": { "dockerfile": "Dockerfile" }`. Everything else — customizations, mounts — stays exactly the same.

## Try It

After this change, **Rebuild Container** (`Ctrl+Shift+P` → "Rebuild Container"). Then verify:

```bash
jq --version    # should work now
tree --version  # should work now
python3 --version  # still there from the base image
```

## Key Takeaways

- `"image"` pulls a pre-built image; `"build"` builds one from a Dockerfile
- The Dockerfile goes in `.devcontainer/` alongside `devcontainer.json`
- `FROM` sets the base; `RUN` adds your customizations on top
- Docker's layer cache makes rebuilds fast when only lower layers change
- Everything else in `devcontainer.json` works identically with either approach
