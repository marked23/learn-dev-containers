# Lesson 0: Where Dev Containers Fit in Your Workflow

## The Key Insight

You start with the container, not the other way around. Dev containers flip the traditional workflow.

Traditional:
1. Install tools on your machine
2. Write code
3. Eventually containerize for deployment

Dev container workflow:
1. Define your dev environment in `.devcontainer/devcontainer.json`
2. Open the folder in VS Code → "Reopen in Container"
3. Write all your code inside the container from the start

## Your Files Stay on Your Machine

Your project folder lives on your host. VS Code mounts it into the container automatically. Files are normal files on disk — visible in your file manager, committable with git from your host. But when you run code, install packages, or use the VS Code terminal, that all happens inside the container.

## Why This Matters

Onboarding without dev containers: "Install Python 3.11, PostgreSQL 15, Redis, these 4 CLI tools, configure these env vars, run these 6 setup commands..."

Onboarding with dev containers: "Clone the repo, open in VS Code, click Reopen in Container. Done."

The dev container *is* the setup instructions, expressed as code.

## Both Patterns Work

- **Greenfield**: Create empty folder → add `.devcontainer/devcontainer.json` → reopen in container → start coding.
- **Existing project**: Add `.devcontainer/` to an existing repo. Nothing changes for people who don't use it.

Dev containers are additive. They don't force anything on team members who prefer their own setup.

## Dev Containers Are Not Production Containers

A dev container is for development — it has editor tools, debuggers, linters, and a full OS. Your production container (a separate `Dockerfile`) should be minimal. These are two different things.
