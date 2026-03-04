# Lesson 6: Port Forwarding

## The Problem

Your app runs inside a container. It starts a web server on port 8000. You open `http://localhost:8000` in your browser on the host. Nothing.

The container has its own network. Port 8000 inside the container isn't the same as port 8000 on your machine. Without port forwarding, they're completely isolated.

## The Fix: `forwardPorts`

```json
{
  "forwardPorts": [8000]
}
```

This tells VS Code: when the container is running, forward port 8000 from the container to port 8000 on your host. Now `http://localhost:8000` in your browser reaches the server inside the container.

Multiple ports work too:

```json
{
  "forwardPorts": [8000, 5432, 6379]
}
```

## Automatic Port Detection

VS Code can also detect ports automatically. When a process inside the container starts listening on a port, VS Code notices and offers to forward it — you've probably seen the "Open in Browser" notification pop up.

You can control this behavior with `"portsAttributes"`:

```json
{
  "forwardPorts": [8000],
  "portsAttributes": {
    "8000": {
      "label": "Web App",
      "onAutoForward": "openBrowser"
    }
  }
}
```

### `onAutoForward` Options

| Value | Behavior |
|---|---|
| `"notify"` | Show a notification (default) |
| `"openBrowser"` | Automatically open in your browser |
| `"openPreview"` | Open in VS Code's built-in Simple Browser |
| `"silent"` | Forward quietly, no notification |
| `"ignore"` | Don't forward this port at all |

### Other Port Attributes

```json
{
  "portsAttributes": {
    "8000": {
      "label": "Web App",
      "protocol": "https",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "silent"
    }
  }
}
```

- **`label`** — a human-readable name shown in VS Code's Ports panel
- **`protocol`** — `"http"` (default) or `"https"`
- **`onAutoForward`** — what to do when the port is detected

## Default Behavior for All Ports

You can set a default for ports you don't explicitly list:

```json
{
  "portsAttributes": {
    "8000": {
      "label": "Web App",
      "onAutoForward": "openBrowser"
    }
  },
  "otherPortsAttributes": {
    "onAutoForward": "silent"
  }
}
```

This is handy when your app spawns random ports (webpack dev server, debugger, etc.) and you don't want a notification for every one.

## A Practical Example

Let's make this concrete. Here's a tiny Python web server to test with:

```python
# server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

print("Server running at http://localhost:8000")
HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler).serve_forever()
```

Note the `"0.0.0.0"` — this tells the server to listen on all network interfaces, not just `127.0.0.1`. Inside a container, if you bind to `127.0.0.1`, the port forward won't reach it because the forwarding comes from a different interface.

## `forwardPorts` vs Docker's `-p` Flag

If you've used Docker before, you might know `docker run -p 8000:8000`. Dev container port forwarding is different:

- Docker's `-p` is set at container creation and can't change
- VS Code's `forwardPorts` is dynamic — it can forward/unforward while the container runs
- VS Code also auto-detects ports, which Docker doesn't do

You don't need `-p` flags with dev containers. `forwardPorts` handles it.

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
  "forwardPorts": [8000],
  "portsAttributes": {
    "8000": {
      "label": "Web App",
      "onAutoForward": "notify"
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
  },
  "mounts": [
    "source=devcontainers-extensions,target=/root/.vscode-server/extensions,type=volume",
    "source=claude-config,target=/root/.claude,type=volume"
  ]
}
```

## Try It

1. Rebuild the container
2. Run `python server.py` in the terminal
3. Open `http://localhost:8000` in your host browser — you should see a directory listing
4. Check the **Ports** tab in VS Code's bottom panel to see the forwarded port

## Key Takeaways

- Containers have their own network — ports aren't accessible from the host by default
- `forwardPorts` bridges container ports to your host machine
- `portsAttributes` controls labels, protocols, and auto-forward behavior
- VS Code can also auto-detect ports when processes start listening
- Bind to `0.0.0.0` inside the container, not `127.0.0.1`, or forwarding won't work
