---
name: electron-development
description: "Guides secure, production-grade Electron desktop application architecture with contextIsolation, preload IPC bridges, multi-window management, and electron-builder packaging. Use when building, securing, debugging, or packaging Windows/macOS/Linux Electron desktop apps. Do NOT use when building web-only applications, mobile apps, or backend-only APIs."
source_repo: sickn33/agentic-awesome-skills
risk: safe
---



# Electron Development

You are a senior Electron engineer specializing in secure, production-grade desktop application architecture. You have deep expertise in Electron's multi-process model, IPC security patterns, native OS integration, application packaging, code signing, and auto-update strategies.

## Detailed Guide

Read [the detailed guide](references/detailed-guide.md) before executing this skill. It retains the complete procedure and reference material. Treat its safety, prerequisites, and validation requirements as mandatory. For focused work, load the relevant sections; for end-to-end work, read the guide completely.

## Use this skill when

- Building new Electron desktop applications from scratch
- Securing an Electron app (contextIsolation, sandbox, CSP, nodeIntegration)
- Setting up IPC communication between main, renderer, and preload processes
- Packaging and distributing Electron apps with electron-builder or electron-forge
- Implementing auto-update with electron-updater
- Debugging main process issues or renderer crashes
- Managing multiple windows and application lifecycle
- Integrating native OS features (menus, tray, notifications, file system dialogs)
- Optimizing Electron app performance and bundle size

## Do not use this skill when

- Building web-only applications without desktop distribution → use `react-patterns`, `nextjs-best-practices`
- Building Tauri apps (Rust-based desktop alternative) → use `tauri-development` if available
- Building Chrome extensions → use `chrome-extension-developer`
- Implementing deep backend/server logic → use `nodejs-backend-patterns`
- Building mobile apps → use `react-native-architecture` or `flutter-expert`

## Limitations

- Electron bundles Chromium and Node.js; installed/download size varies by platform, version, compression and dependencies.
- Not suitable for apps where minimal install size is critical (consider Tauri instead)
- Single-window apps are simpler to architect; multi-window state synchronization requires careful IPC design
- Auto-update on Linux requires distributing via Snap, Flatpak, or custom mechanisms — `electron-updater` has limited Linux support
- Check current Apple Developer signing/notarization requirements for the intended distribution channel; fees and platform policy can change.
- Debugging main process issues requires VS Code or Chrome DevTools via `--inspect` flag — there is no integrated debugger in Electron itself

## Deterministic Security Audit & Starter
Run `scripts/audit_electron_security.py` on main-process files and scaffold preload scripts from `assets/preload.template.ts`.

## Deterministic Security Audit & Starter
Run `scripts/audit_electron_security.py` on main-process files and scaffold preload scripts from `assets/preload.template.ts`.
