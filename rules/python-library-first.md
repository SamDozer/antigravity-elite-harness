---
trigger: always_on
description: "Evaluate appropriate Python libraries, SDKs, packages, and existing tools before implementing any task. Choose the best dependable solution instead of reinventing the wheel."
---

# Python Library-First Evaluation Rule

## Core mandate
Before implementing **any nontrivial task** (coding, debugging, automation, data processing, AI, images, audio, video, 3D, Blender, desktop apps, web apps, tooling, or pipelines), do a brief **Python Library Opportunity Check**. Your goal is to improve quality, correctness, speed, maintainability, and development efficiency—not to add Python dependencies everywhere.

## Mandatory pre-implementation workflow
1. **Understand the task and constraints.** Identify the desired outcome, platform, current language/framework, runtime, performance constraints, offline requirements, security/privacy expectations, licenses, and deployment environment.
2. **Inspect what already exists.** Review the repository, declared dependencies, environment, reusable functions, CLI tools, and the Python standard library. Prefer project-native functionality when it already solves the problem reliably.
3. **Look for library opportunities.** For each meaningful technical subtask, consider whether a mature Python library, SDK, binding, or external tool with Python integration can deliver a better result than fresh custom code. Search local package metadata/documentation first. When web access is available and useful, check official library documentation, PyPI metadata, release activity, and compatibility. Never invent a library, API, version, benchmark, or installation status.
4. **Compare realistic alternatives.** Usually consider 1–3 candidate solutions, including the current stack / built-in approach. Judge: capability fit, output quality, runtime speed, stability, maintainability, documentation, maintenance status, Python and OS compatibility, existing ecosystem fit, installation size, licensing, security risk, and deployment cost. For Blender, additionally assess Blender-version compatibility and `bpy` / add-on limitations.
5. **Make a deliberate decision.** Prefer an existing, well-supported library when it clearly adds value. Prefer standard libraries or existing project code for simple tasks. For JavaScript/browser/mobile-specific features, prefer native APIs or stack-native libraries when Python is the wrong execution environment. Do not force Python into a project where it makes the architecture worse.
6. **Implement safely.** Reuse already-installed dependencies when suitable. Do not install packages globally or change dependency manifests without following the project's approval and dependency-management policies. Use an isolated virtual environment if Python setup is required; pin or constrain versions in the project's normal format, respect lockfiles, and never run unreviewed installation scripts or unsafe commands from arbitrary sources.
7. **Verify results.** Run relevant tests, examples, or minimal integration checks where tools permit. Validate imports, API availability, compatibility, output correctness, performance when relevant, and errors. If a promising package cannot be verified, clearly state the uncertainty and use a dependable fallback.

## Required short decision note
Before major implementation, summarize internally—or briefly in the user-facing plan when helpful:
- **Task:** What needs to be built.
- **Candidates checked:** Existing code / built-ins and relevant libraries.
- **Choice:** Selected approach and why.
- **Dependency impact:** New packages required or none.

Keep this concise; never let research delay a small, obvious change.

## Domains worth checking (examples only, not automatic recommendations)
- **Blender / 3D:** `bpy`, `bmesh`, `mathutils`, `trimesh`, `open3d`, `numpy`, `Pillow`.
- **AI / ML:** `torch`, `transformers`, `scikit-learn`, `onnxruntime`, `sentence-transformers`.
- **Images / computer vision:** `Pillow`, `opencv-python`, `scikit-image`, `imageio`.
- **Audio / speech:** `soundfile`, `librosa`, `pydub`, `torchaudio`, `faster-whisper`.
- **Video:** `ffmpeg-python` (requires FFmpeg), `PyAV`, `moviepy`.
- **Automation / scraping:** `playwright`, `httpx`, `beautifulsoup4`, `pydantic`.
- **Data / scientific work:** `numpy`, `pandas`, `polars`, `scipy`, `matplotlib`.
- **Desktop / UI:** `PySide6`, `customtkinter` (only when Python UI is appropriate).

Examples are starting points, **not** a whitelist, proof of suitability, or a mandate to install them. Always validate current API, support, and project compatibility.

## Non-negotiable safeguards
- **Never** choose a package solely for novelty, popularity, or because it is written in Python.
- **Never** install every candidate; evaluate first, install only what is justified.
- **Never** claim a performance benefit without measurement or credible evidence.
- **Never** compromise security, licenses, privacy, portability, or offline-first requirements just to use a library.
- **Never** replace stable existing code without a clear advantage and appropriate tests.
- **Never** turn a simple task into excessive research; use a quick check and proceed.

**Decision principle:** If a trusted, compatible library materially improves the outcome, use it. Otherwise, use the simplest reliable existing/native solution.

