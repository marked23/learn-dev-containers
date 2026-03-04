# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a learning repository. The goal is to teach the user about **dev containers** (Development Containers) from the ground up. The user's starting knowledge: dev containers are Docker containers.

## What Are Dev Containers

Dev containers are a specification (devcontainers.json) for defining reproducible, containerized development environments. Key concepts to teach progressively:

1. **Foundation**: Dev containers wrap a Docker container with IDE/editor integration (primarily VS Code). They are *not* just Docker containers — they add a standardized configuration layer on top.
2. **devcontainer.json**: The central config file (lives in `.devcontainer/devcontainer.json`). Defines the image, extensions, settings, ports, mounts, and lifecycle scripts.
3. **Images & Dockerfiles**: Can use pre-built Microsoft/community images or a custom Dockerfile.
4. **Features**: Reusable, shareable units of installation logic (e.g., adding Node, Python, or CLI tools) that compose into the container without modifying the Dockerfile.
5. **Lifecycle scripts**: `postCreateCommand`, `postStartCommand`, `postAttachCommand` — hooks for setup at different stages.
6. **Port forwarding**: Automatically forward container ports to the host.
7. **Volumes & mounts**: Persist data and share files between host and container.
8. **Docker Compose integration**: For multi-container setups (e.g., app + database).
9. **Dev Container CLI** (`devcontainer` npm package): Build and run dev containers outside of VS Code.

## Teaching Approach

- Build examples incrementally in this repo, starting simple and adding complexity.
- Each example or lesson can live in its own subdirectory with its own `.devcontainer/` folder.
- Explain *why*, not just *how* — connect each concept to real development workflow benefits.
- The user can open any subdirectory in VS Code and use "Reopen in Container" to try it.

## Prerequisites

The user needs Docker installed and running, plus VS Code with the "Dev Containers" extension (`ms-vscode-remote.remote-containers`).
