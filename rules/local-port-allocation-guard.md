# Global Rule — Local Port Allocation & Collision Guard

## Core Mandate
Whenever you create, scaffold, configure, or launch any local server, development server, backend API, WebSocket server, daemon, or microservice for ANY program or project:
- **Strictly prohibit picking arbitrary, hardcoded, or collision-prone default ports** (such as `3000`, `5000`, `5173`, `8000`, `8080`, etc.) without verification.
- **Mandatory Registry Consultation:** Check the central registry at `~/.gemini\config\local-ports-registry.json` before assigning any port.
- **Mandatory Collision Verification:** Check both the central registry (static record) AND live system status (runtime listener) to guarantee the port has never been used by another project and is not currently held by any process.

---

## 1. Dedicated Port Blocks by Project Type
When allocating a new port, select exclusively from the safe assigned blocks in order:

1. **Desktop & Electron Backends (`31000 - 31999`):**
   - For companion Python/Node/Go servers, daemons, and APIs powering Electron or desktop apps.
2. **Web & Fullstack Dev Servers (`32000 - 32999`):**
   - For web apps, Vite servers, Next.js, FastHTML, Dash, Streamlit, and local browser tools.
3. **Automation, MCP & CLI Services (`33000 - 33999`):**
   - For MCP servers, background scraping/worker processes, and automated agent tools.
4. **Media, WebSockets & Streaming (`34000 - 34999`):**
   - For audio/video feeds, real-time socket connections, and game sync servers.

---

## 2. Allocation & Verification Protocol

Before writing configuration or server startup code:
1. **Read Central Registry:**
   - Inspect `~/.gemini\config\local-ports-registry.json`.
   - Any port listed under `allocated_projects` or `reserved_system_ports` is strictly occupied.
2. **Select Candidate Port:**
   - Identify the lowest unassigned number within the appropriate category block (e.g., `31001`, `31002`...).
3. **Live System Verification:**
   - Execute a quick PowerShell check to confirm the port is not actively listening:
     ```powershell
     Get-NetTCPConnection -LocalPort <candidate_port> -ErrorAction SilentlyContinue
     ```
   - If a listener exists, increment by 1 and re-check until a completely free port is verified.
4. **Record the Allocation:**
   - Immediately update `~/.gemini\config\local-ports-registry.json` with:
     - `port`: The chosen integer.
     - `project_name`: Name of the new program.
     - `path`: Absolute directory path of the project.
     - `category`: The category key (e.g. `desktop_electron_backends`).
     - `type`: Specific service type (e.g. `FastAPI Backend`, `Express Bridge`).
     - `status`: `active`.
     - `assigned_date`: Current date (YYYY-MM-DD).
   - Sync the corresponding row in `~/.gemini\config\LOCAL_PORTS_DIRECTORY.md`.

---

## 3. Code-Level Resilience Requirement
Whenever writing server startup scripts or backend entry points:
- Provide an environment variable or config fallback for the port (e.g., `PORT = int(os.getenv("PORT", 31001))`).
- If feasible for the runtime framework, implement automatic retry or port fallback logic so that if the designated port is unexpectedly blocked at launch, the application gracefully handles it and reports the diagnostic clearly.

