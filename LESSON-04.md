# Lesson 4: Features — Composable Add-Ons

## The Problem Features Solve

In Lesson 3, we added `jq` and `tree` by writing `apt-get install` commands in a Dockerfile. That works for simple packages, but what about tools with complex installation steps?

Take the GitHub CLI (`gh`). Installing it manually requires adding a GPG key, configuring a custom apt repository, then installing. That's ~10 lines of Dockerfile commands you'd have to write, test, and maintain. Multiply that by every tool your team needs.

## What Features Are

Features are pre-packaged installation scripts that you declare in `devcontainer.json`. Someone else wrote and maintains the install logic — you just reference it and optionally pass options.

```json
{
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  }
}
```

That single line replaces all the manual install steps. The `{}` means "use default options."

## How to Find Features

Browse the official registry at [containers.dev/features](https://containers.dev/features). Common ones:

| Feature | ID | What it installs |
|---|---|---|
| GitHub CLI | `ghcr.io/devcontainers/features/github-cli:1` | `gh` command |
| Node.js | `ghcr.io/devcontainers/features/node:1` | Node, npm, nvm |
| Common Utilities | `ghcr.io/devcontainers/features/common-utils:2` | zsh, oh-my-zsh, useful shell config |
| Docker-in-Docker | `ghcr.io/devcontainers/features/docker-in-docker:2` | Docker engine inside your container |
| AWS CLI | `ghcr.io/devcontainers/features/aws-cli:1` | `aws` command |

The ID format is `ghcr.io/<org>/<repo>/<feature>:<major-version>`. The `:1` or `:2` is the major version — it auto-updates for minor/patch versions but won't break you with a major version change.

## Passing Options

Features accept options to customize what gets installed. For example, the Node feature lets you pick a version:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    }
  }
}
```

Each feature documents its options on its registry page. Common patterns:
- `"version"` — pick a specific version
- `"installTools"` — include/exclude companion tools
- `"none"` as a version — skip the main install but still get companion tools

## Multiple Features

Just add more entries. They install in the order listed:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true
    }
  }
}
```

## Features vs Dockerfile — When to Use Which

| Use a Feature when... | Use a Dockerfile `RUN` when... |
|---|---|
| A feature exists for the tool you need | The tool is a simple `apt-get install` |
| The install process is complex | No feature exists for it |
| You want automatic version management | You need precise control over the install |
| You want the community to maintain the script | You need to match an exact production setup |

They're not mutually exclusive. You can use both — a Dockerfile for your base and system packages, plus features for tools with complex installs. Features run *after* the Dockerfile build.

## What We're Adding

Let's add the GitHub CLI to our dev container. This is a good example because installing it manually would require multiple steps — exactly the kind of thing features simplify.

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

The build order is:
1. Docker builds the image from the Dockerfile (`FROM` + `RUN apt-get install`)
2. Features install on top of that (`gh` CLI)
3. VS Code extensions install
4. Container is ready

## Try It

After rebuilding, verify:

```bash
gh --version       # installed by the feature
jq --version       # installed by the Dockerfile
tree --version     # installed by the Dockerfile
python3 --version  # from the base image
```

## Key Takeaways

- Features are pre-packaged install scripts declared in `devcontainer.json`
- They handle complex installations that would be tedious to write in a Dockerfile
- Pass options via `{}` objects to customize versions and behavior
- Features and Dockerfiles work together — Dockerfile builds first, features layer on top
- Browse available features at [containers.dev/features](https://containers.dev/features)
- The version in the ID (`:1`, `:2`) is a major version — you get minor/patch updates automatically
