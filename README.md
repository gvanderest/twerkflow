# twerk

> A personal CLI harness built on top of [pi](https://github.com/earendil-works/pi-coding-agent).

```bash
npm install -g twerk
twerk
```

---

## What it is

`twerk` wraps pi's TUI and makes it easy to install with opinionated defaults, bundled skills, and a managed workflow mode — all isolated from your existing pi configuration.

It is **not** a replacement for pi. It is a thin layer on top of it.

---

## Inspiration

twerk is heavily inspired by **[gsd-2](https://github.com/gsd-build/gsd-2)** in both concept and approach. The idea of wrapping an agent foundation with an opinionated workflow layer, shipping skills and extensions as first-class primitives, and separating "direct use" from "managed workflow" all come from gsd-2.

I built twerk to understand those ideas from the inside — this is a learning project as much as a tool. If you want the more fully-featured, battle-tested version of this concept, go use gsd-2.

---

## How it works

Running `twerk` launches pi's full TUI pointed at `~/.twerk/` instead of `~/.pi/agent/`. Your pi config is untouched.

```
~/.twerk/
  settings.json          # pi settings (model, theme, auth, packages)
  twerk.settings.json    # twerk-specific config
  auth.json              # written by /login
  extensions/            # your custom extensions
  skills/                # your custom skills
  sessions/              # session history
```

Twerk's own bundled skills and extensions live inside the npm package and update automatically with the package. Your custom resources in `~/.twerk/` layer on top.

## Two modes

| | How | What |
|---|---|---|
| **Direct** | `twerk` | Full pi TUI. Use it exactly like pi. |
| **Managed** | `/twerk` inside the TUI | Opinionated workflow mode. |

The managed workflow (`/twerk`) is the reason this tool exists. Direct mode is just pi with twerk's defaults loaded.

## Config override

```bash
TWERK_AGENT_DIR=/path/to/custom twerk
```

---

## License

[MIT](./LICENSE)

---

## Acknowledgements

Built on [pi](https://github.com/earendil-works/pi-coding-agent) by Earendil Works.  
Inspired by [gsd-2](https://github.com/gsd-build/gsd-2).
