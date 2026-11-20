---
trigger: always_on
description: "Use Electron by default for every new application, particularly Windows desktop apps, unless the user explicitly specifies another platform or stack."
---

# Global Rule — Electron-First Application Development

## Core Requirement
- **Electron is the mandatory default application framework.** Whenever the user asks to create, build, prototype, or redesign a **new app/application** without explicitly naming a different target platform, assume a **Windows desktop application built with Electron**.
- Do not independently replace Electron with Tauri, Qt, Tkinter, PySide, WinForms, WPF, Flutter, or another desktop shell because it seems faster, lighter, more popular, or more suitable.
- If the request expressly specifies a **website, web-only app, mobile app, game engine, or a non-Electron technology**, honor that explicit requirement instead. An explicit user instruction always overrides this default.
- **Existing projects:** Respect their existing architecture. Never silently migrate an existing non-Electron codebase to Electron. When the user explicitly requests a migration, proceed with a scoped migration plan.

## Required Structure for New Desktop Apps
- Use Electron with a modern, maintained Node.js LTS version and a package manager appropriate to the project.
- Separate the **main process**, **preload scripts**, and **renderer UI**.
- Choose the renderer framework and styling approach according to the project's complexity, existing dependencies, and any applicable global frontend-design rules. Electron is the app shell; it does not mandate a single CSS or frontend framework.
- Use native desktop capabilities through carefully scoped IPC bridges exposed from preload, not direct Node.js access inside renderer pages.
- Default to `contextIsolation: true`, `nodeIntegration: false`, and sandboxed renderer processes where feasible. Validate IPC inputs and restrict external navigation and permissions.
- Prefer offline-first/local data storage when the requirements do not demand an online backend. Keep secrets out of the renderer.

## Delivery and Packaging
- Set up reproducible development and production scripts, including Electron launch and production build.
- For Windows projects, prepare a proper **.exe** deliverable (using a maintained packaging solution such as electron-builder or Electron Forge), with application icon and sensible metadata when assets are provided.
- A website-only preview is **not** a substitute for the requested desktop executable.
- Test startup, window behavior, IPC flows, file access, and packaged builds when the environment supports testing. Never claim to have produced or tested an executable unless it was actually built/tested.

## Decision Rule
Before implementing any new application, check its explicit platform requirements. If no platform is given, proceed with **Electron for Windows by default**, without asking the user to choose a framework. Briefly note this architectural choice in the implementation plan.

