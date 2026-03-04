# Dev Containers Curriculum

A progressive guide from zero to proficient with dev containers.

---

## Lesson 1: Foundation — What Dev Containers Actually Are

**Concept**: Dev containers are more than Docker containers. They are a specification that combines a Docker container with editor/IDE integration, giving you a reproducible development environment that anyone on your team can launch identically.

**What you'll learn**:
- The difference between running code in a Docker container vs. developing inside one
- How VS Code communicates with the container (VS Code Server runs inside, UI runs on your host)
- The Dev Containers extension and the "Reopen in Container" workflow

**Why it matters**: Without dev containers, "works on my machine" is a constant problem. Dev containers make your environment portable, versioned, and disposable.

---

## Lesson 2: devcontainer.json — The Central Config File

**Concept**: Every dev container is defined by a `devcontainer.json` file, typically at `.devcontainer/devcontainer.json`. This single file tells VS Code what image to use, what tools to install, and how to configure the environment.

**What you'll learn**:
- The minimal required fields (`name`, `image`)
- Where the file lives and how VS Code discovers it
- How to pick a base image (e.g., `mcr.microsoft.com/devcontainers/base:ubuntu`)

**Why it matters**: This is the file you'll edit most. Understanding its structure unlocks everything else.

---

## Lesson 3: Images & Dockerfiles

**Concept**: You can either reference a pre-built image directly in `devcontainer.json` or point to a custom `Dockerfile` when you need more control over what's installed.

**What you'll learn**:
- Using `"image"` for quick setups with Microsoft/community images
- Switching to `"build": { "dockerfile": "Dockerfile" }` for custom environments
- When to use each approach
- How the dev container build cache works

**Why it matters**: Pre-built images get you started fast; custom Dockerfiles let you replicate exact production-like environments or install specialized tools.

---

## Lesson 4: Features — Composable Add-Ons

**Concept**: Features are reusable, shareable chunks of installation logic. Instead of writing Dockerfile instructions to install Node, Python, or the AWS CLI, you declare them in `devcontainer.json` and they get layered in automatically.

**What you'll learn**:
- The `"features"` field in `devcontainer.json`
- Browsing available features at containers.dev/features
- Passing options to features (e.g., choosing a Node version)
- How features compose — order and layering

**Why it matters**: Features eliminate boilerplate Dockerfile code and let you mix-and-match tools without maintaining complex build scripts.

---

## Lesson 5: Lifecycle Scripts

**Concept**: Dev containers provide hooks that run at specific moments: after the container is created, after it starts, and after VS Code attaches to it.

**What you'll learn**:
- `postCreateCommand` — runs once after container creation (install dependencies here)
- `postStartCommand` — runs every time the container starts
- `postAttachCommand` — runs every time VS Code attaches
- `initializeCommand` — runs on the host before the container is built
- `onCreateCommand` — runs inside the container the first time it's created

**Why it matters**: These hooks automate setup steps so you never have to manually run `npm install` or `pip install` after opening a dev container.

---

## Lesson 6: Port Forwarding

**Concept**: When your app inside the container listens on a port, dev containers can automatically detect and forward that port to your host machine so you can access it from your browser.

**What you'll learn**:
- The `"forwardPorts"` field for explicit port forwarding
- Automatic port detection and how to control it with `"portsAttributes"`
- Labels, protocols (http/https), and `onAutoForward` behavior

**Why it matters**: Without port forwarding, a web server running inside a container is unreachable from your host browser. This bridges that gap seamlessly.

---

## Lesson 7: Volumes & Mounts

**Concept**: Containers are ephemeral — when they're rebuilt, data inside is lost. Volumes and mounts let you persist data and share files between the host and container.

**What you'll learn**:
- How your project source code is already mounted (the workspace mount)
- Custom mounts via the `"mounts"` field
- Named volumes for persisting things like package caches across rebuilds
- Bind mounts vs. named volumes and when to use each

**Why it matters**: Without proper mounts, you'd lose caches, databases, and other state every time you rebuild your container, making iteration slow.

---

## Lesson 8: Docker Compose Integration

**Concept**: Real projects often need more than one container — an app server plus a database, a cache, a message queue. Dev containers integrate with Docker Compose to orchestrate multi-container environments.

**What you'll learn**:
- Using `"dockerComposeFile"` instead of `"image"` in `devcontainer.json`
- The `"service"` field to specify which container VS Code attaches to
- Defining supporting services (PostgreSQL, Redis, etc.) in `docker-compose.yml`
- How workspace mounts work with Compose

**Why it matters**: This is how dev containers scale to match real production architectures while keeping the single-command "Reopen in Container" experience.

---

## Lesson 9: The Dev Container CLI

**Concept**: The `devcontainer` CLI (`@devcontainers/cli` npm package) lets you build, run, and manage dev containers outside of VS Code — from any terminal, CI pipeline, or other editor.

**What you'll learn**:
- Installing the CLI: `npm install -g @devcontainers/cli`
- `devcontainer up` — start a dev container from the command line
- `devcontainer exec` — run commands inside a running dev container
- `devcontainer build` — pre-build images for faster startup
- Using dev containers in CI/CD (e.g., GitHub Actions with `devcontainers/ci`)

**Why it matters**: The CLI decouples dev containers from VS Code, making them useful for CI pipelines, other editors, and automated workflows.
