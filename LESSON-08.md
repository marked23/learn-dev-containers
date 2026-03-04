# Lesson 8: Docker Compose Integration

## When One Container Isn't Enough

Everything so far has been a single container — our ROCm/PyTorch environment with tools layered on top. That works great when your project is self-contained.

But real-world projects often need supporting services:
- A web app + PostgreSQL database
- An API server + Redis cache
- A machine learning service + a model-serving API + a message queue

You *could* cram everything into one container, but that's messy and defeats the purpose of containerization. Docker Compose lets you define multiple containers that work together as a group.

## How It Changes `devcontainer.json`

Remember Lesson 3 — you pick exactly one container source. We've used `"image"` and `"build"`. The third option is `"dockerComposeFile"`:

```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspaces/learn-dev-containers"
}
```

Three required fields:
- **`dockerComposeFile`** — path to your Compose file (relative to `.devcontainer/`)
- **`service`** — which service VS Code attaches to. You develop inside this one.
- **`workspaceFolder`** — where your project code lives inside that container

## The Compose File

A `docker-compose.yml` defines your services. Here's a typical setup — an app container plus a PostgreSQL database:

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspaces/learn-dev-containers:cached
    command: sleep infinity

  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Let's break this down.

### The `app` Service (Where You Develop)

```yaml
app:
  build:
    context: ..
    dockerfile: .devcontainer/Dockerfile
  volumes:
    - ..:/workspaces/learn-dev-containers:cached
  command: sleep infinity
```

- **`build`** — builds from our existing Dockerfile. `context: ..` sets the build context to the project root.
- **`volumes`** — mounts your project into the container. With Compose, you manage the workspace mount yourself (dev containers don't auto-mount it like they do in the single-container setup).
- **`command: sleep infinity`** — keeps the container running. Without this, the container would start, have nothing to do, and exit. VS Code needs it alive to attach.
- **`:cached`** — a performance hint for macOS/Windows. On Linux, it has no effect but doesn't hurt.

### The `db` Service (Supporting Service)

```yaml
db:
  image: postgres:16
  restart: unless-stopped
  environment:
    POSTGRES_USER: dev
    POSTGRES_PASSWORD: dev
    POSTGRES_DB: myapp
  volumes:
    - pgdata:/var/lib/postgresql/data
```

- **`image`** — uses the official PostgreSQL 16 image directly, no custom Dockerfile needed.
- **`environment`** — sets env vars that PostgreSQL reads on startup to create a user and database.
- **`volumes`** — a named volume so your database data survives container restarts.
- **`restart: unless-stopped`** — automatically restarts if the container crashes.

### The `volumes` Section

```yaml
volumes:
  pgdata:
```

Declares the named volume used by the `db` service. Same concept as Lesson 7, just defined in Compose syntax instead of `devcontainer.json`.

## Networking Between Services

Docker Compose puts all services on the same network automatically. Your app container can reach the database using the service name as a hostname:

```python
# Inside the app container, connect to PostgreSQL:
connection = psycopg2.connect(
    host="db",       # ← the service name, not localhost
    port=5432,
    user="dev",
    password="dev",
    dbname="myapp"
)
```

No IP addresses, no port forwarding between containers. Just use the service name.

## What Moves Where

When you switch from a single container to Compose, some things move out of `devcontainer.json` and into `docker-compose.yml`:

| Concept | Single Container (`devcontainer.json`) | Compose (`docker-compose.yml`) |
|---|---|---|
| Image/Build | `"image"` or `"build"` | `image:` or `build:` per service |
| Workspace mount | Automatic | You define it in `volumes:` |
| Port mapping | `"forwardPorts"` still works | Can also use `ports:` in Compose |
| Named volumes | `"mounts"` | `volumes:` in Compose |
| Environment variables | `"containerEnv"` | `environment:` per service |

Things that stay in `devcontainer.json`: Features, lifecycle scripts, VS Code customizations, `forwardPorts`.

## A Full Compose-Based `devcontainer.json`

```json
{
  "name": "Learn Dev Containers",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspaces/learn-dev-containers",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8000, 5432],
  "portsAttributes": {
    "8000": {
      "label": "Web App",
      "onAutoForward": "notify"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "silent"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": ["anthropic.claude-code"],
      "settings": {
        "editor.formatOnSave": true,
        "files.trimTrailingWhitespace": true
      }
    }
  }
}
```

Notice: `"build"` is gone (Compose handles it), `"mounts"` is gone (Compose handles it), and `"dockerComposeFile"` + `"service"` + `"workspaceFolder"` are in.

## We're Not Switching (Yet)

This lesson is conceptual. Our single-container setup works fine for learning, and we don't need a database right now. Switching to Compose adds complexity that's only worth it when you genuinely need multiple services.

**No changes to our config this lesson.** When you start a project that needs a database or other supporting services, come back to this pattern.

## When to Switch to Compose

- You need a real database (PostgreSQL, MySQL, MongoDB)
- You need a cache (Redis, Memcached)
- You need a message queue (RabbitMQ, Kafka)
- You need a second service your app talks to (another API, a mock server)
- You need port remapping (Lesson 6 — Compose gives you `"8001:8000"` syntax)

If none of those apply, stick with the single-container setup. Simpler is better.

## Key Takeaways

- Docker Compose orchestrates multiple containers as a group
- `"dockerComposeFile"` replaces `"image"`/`"build"` in `devcontainer.json`
- `"service"` tells VS Code which container to attach to
- Services talk to each other using service names as hostnames
- You manage workspace mounts yourself in the Compose file
- Features, lifecycle scripts, and VS Code customizations stay in `devcontainer.json`
- Don't switch to Compose until you actually need multiple services
