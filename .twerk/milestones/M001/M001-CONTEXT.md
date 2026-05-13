# M001 — twerk: Core Harness

**Status:** Planning  
**Date:** 2026-05-13

---

## What We're Building

`twerk` is a personal-first, publicly distributable CLI harness that wraps [pi](https://github.com/earendil-works/pi-coding-agent) and makes it easy to install and extend with opinionated defaults, bundled skills, and a managed workflow mode.

```bash
npm install -g twerk
twerk
```

That's it. The user lands in pi's full TUI, pointed at `~/.twerk/` instead of `~/.pi/agent/`.

---

## Goals

- Zero-friction install via npm
- Full pi TUI, not a custom interface — twerk rides on top
- Config isolation: `~/.twerk/` never collides with `~/.pi/agent/`
- Two modes: direct use (default) and managed workflow (`/twerk` command)
- Bundled skills/extensions always in sync with installed twerk version
- User skills/extensions layer cleanly on top of bundled ones
- Public npm distribution, personal-first design

---

## Architecture

### Binary

`twerk` is a Node.js CLI binary (npm `bin` entry). It uses pi's SDK directly — `InteractiveMode` from `@earendil-works/pi-coding-agent` — not a shell wrapper around the `pi` CLI.

### Config Directory

| Env Var | Default | Passed to SDK as |
|---|---|---|
| `TWERK_AGENT_DIR` | `~/.twerk` | `agentDir` |

`~/.twerk/` mirrors pi's `agentDir` layout exactly:

```
~/.twerk/
  settings.json          # pi's settings — pi's turf, user edits freely
  twerk.settings.json    # twerk's settings — applied via applyOverrides() at boot
  auth.json              # written by /login, read by pi's AuthStorage
  extensions/            # user's custom extensions (layered on top of bundled)
  skills/                # user's custom skills (layered on top of bundled)
  sessions/              # session files
  AGENTS.md              # optional global context file
```

### Settings Layering

At boot, twerk:
1. Constructs `SettingsManager.create(cwd, agentDir)` — reads `settings.json`
2. Reads `twerk.settings.json` from `agentDir`
3. Calls `settingsManager.applyOverrides(twerkSettings)` to layer twerk's config on top

**`settings.json`** — pi's turf. Model, theme, compaction, retry, packages, auth. User edits this directly or via `/settings` inside the TUI.

**`twerk.settings.json`** — twerk's turf. Which twerk extensions are active, twerk-specific defaults, future managed workflow config. Not touched by pi.

### Bundled Resources

Twerk's own skills and extensions live inside the npm package. The binary resolves them relative to `__dirname` and passes them to `DefaultResourceLoader` via `additionalExtensionPaths` and the skills equivalent.

```
twerk (npm package)
  bin/
    twerk.js             # entry point
  extensions/            # bundled extensions (always current with installed version)
  skills/                # bundled skills (always current with installed version)
```

User resources in `~/.twerk/extensions/` and `~/.twerk/skills/` are loaded on top. Bundled resources are never written to `~/.twerk/` — they live in the package and update automatically with `npm update -g twerk`.

### Two Modes

| Mode | How to invoke | What it is |
|---|---|---|
| **Direct** | `twerk` | Full pi TUI with twerk config + bundled resources. Equivalent to using pi directly. |
| **Managed** | `/twerk` inside the TUI | Extension command registered by a bundled extension. Activates the opinionated managed workflow. |

Mode 2 (`/twerk`) is implemented as a pi extension command — TypeScript, registered at boot, invoked as a slash command inside the running TUI. Details of the managed workflow are deferred to future milestones.

### First-Run Init

On first launch, if `~/.twerk/` doesn't exist:
1. Create `~/.twerk/`
2. Write a minimal `twerk.settings.json` scaffold
3. Print a one-line hint: `Run /login to authenticate.`
4. Launch the TUI normally

No wizard, no interactive init flow. Pi's `/login` handles auth.

---

## Package Shape

```json
{
  "name": "twerk",
  "version": "0.1.0",
  "bin": { "twerk": "./bin/twerk.js" },
  "dependencies": {
    "@earendil-works/pi-coding-agent": "*"
  }
}
```

---

## Out of Scope (M001)

- Managed workflow implementation (content of `/twerk` command) — future milestone
- Custom themes or branding
- Team/shared config
- Any UI beyond what pi's TUI provides
