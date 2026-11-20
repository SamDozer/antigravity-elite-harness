# Local Port Allocation Directory

Central registry of assigned ports across user projects and system services to prevent port collisions.

---

## 📌 1. Allocated Projects

| Port | Project Name | Path | Category | Status |
| :---: | :--- | :--- | :--- | :---: |
| *None yet* | - | - | - | - |

---

## 🛡️ 2. Dedicated Safe Blocks for New Projects

When initializing or running new local servers, assign ports strictly from the dedicated blocks:

| Port Range | Category | Usage |
| :---: | :--- | :--- |
| **31000 - 31999** | **Desktop & Electron Backends** | Python, Node.js, and background workers for desktop apps |
| **32000 - 32999** | **Web & Fullstack Dev Servers** | Vite, Next.js, FastAPI, Flask, and local web apps |
| **33000 - 33999** | **Automation & MCP Servers** | AI agent sidecars, MCP tools, and daemon scripts |
| **34000 - 34999** | **Media, WebSockets & Streaming** | Real-time audio/video sync, WebSockets, and bridges |

---

## ⚠️ 3. System Reserved Ports
Ports 135, 139, 445, 1433, 3000, 3306, 5000, 5173, 5432, 6379, 8000, 8080, and 11434 are reserved system/service ports.
