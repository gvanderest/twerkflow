#!/usr/bin/env node
/**
 * twerk — entry point
 *
 * Boots pi's full TUI using the @earendil-works/pi-coding-agent SDK, pointed at
 * ~/.twerk (or $TWERK_AGENT_DIR) instead of the default ~/.pi/agent. This gives
 * twerk its own isolated config directory while riding entirely on pi's TUI.
 *
 * Boot sequence:
 *   1. Resolve agentDir (TWERK_AGENT_DIR or ~/.twerk)
 *   2. First-run init: scaffold agentDir + twerk.settings.json if absent
 *   3. Build a CreateAgentSessionRuntimeFactory that:
 *        a. Reads twerk.settings.json and applies it as overrides on top of settings.json
 *        b. Passes bundled extensions + skills from the package to DefaultResourceLoader
 *        c. Layers user resources from agentDir on top automatically
 *   4. Launch InteractiveMode
 */

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "fs";
import { homedir } from "os";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

import {
  createAgentSessionFromServices,
  createAgentSessionRuntime,
  createAgentSessionServices,
  InteractiveMode,
  SessionManager,
  SettingsManager,
} from "@earendil-works/pi-coding-agent";

const __dirname = dirname(fileURLToPath(import.meta.url));
const { version } = JSON.parse(
  readFileSync(join(__dirname, "../package.json"), "utf8")
);

// ── Config dir ────────────────────────────────────────────────────────────────

const agentDir = process.env.TWERK_AGENT_DIR ?? join(homedir(), ".twerk");

// ── First-run init ────────────────────────────────────────────────────────────

if (!existsSync(agentDir)) {
  mkdirSync(agentDir, { recursive: true });

  writeFileSync(
    join(agentDir, "twerk.settings.json"),
    JSON.stringify({}, null, 2) + "\n",
    "utf8"
  );

  console.log("Welcome to twerk! Config created at " + agentDir);
  console.log("Run /login inside the TUI to authenticate.\n");
}

// ── Bundled resource paths ────────────────────────────────────────────────────

// All .ts/.js files in the package's bundled extensions directory.
const bundledExtensionsDir = join(__dirname, "../extensions");
const bundledExtensionPaths = existsSync(bundledExtensionsDir)
  ? readdirSync(bundledExtensionsDir)
      .filter((f) => f.endsWith(".ts") || f.endsWith(".js"))
      .map((f) => join(bundledExtensionsDir, f))
  : [];

// SKILL.md files in each subdirectory of the package's bundled skills directory.
const bundledSkillsDir = join(__dirname, "../skills");
const bundledSkillPaths = existsSync(bundledSkillsDir)
  ? readdirSync(bundledSkillsDir, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => join(bundledSkillsDir, d.name, "SKILL.md"))
      .filter(existsSync)
  : [];

// ── Make version available to bundled extensions ──────────────────────────────

process.env.TWERK_VERSION = version;

// ── Runtime factory ───────────────────────────────────────────────────────────

/**
 * CreateAgentSessionRuntimeFactory
 *
 * Called once on boot and again whenever /new, /resume, /fork, or /clone
 * replaces the active session. The factory is a closure over the process-global
 * inputs above (agentDir, bundled paths).
 */
const createRuntime = async ({ cwd, agentDir: resolvedAgentDir, sessionManager, sessionStartEvent }) => {
  // Resolve the agent dir: the runtime may supply a cwd override but agentDir
  // stays fixed to the twerk dir for the lifetime of the process.
  const effectiveAgentDir = resolvedAgentDir ?? agentDir;

  // 1. Settings: load settings.json (pi's turf) then overlay twerk.settings.json.
  const settingsManager = SettingsManager.create(cwd, effectiveAgentDir);

  const twerkSettingsPath = join(effectiveAgentDir, "twerk.settings.json");
  if (existsSync(twerkSettingsPath)) {
    try {
      const twerkSettings = JSON.parse(readFileSync(twerkSettingsPath, "utf8"));
      if (Object.keys(twerkSettings).length > 0) {
        settingsManager.applyOverrides(twerkSettings);
      }
    } catch {
      // Ignore malformed twerk.settings.json — pi defaults apply.
    }
  }

  // 2. Services: DefaultResourceLoader is built internally by createAgentSessionServices.
  //    additionalExtensionPaths injects bundled extensions; agentDir/extensions/
  //    (user's own) are discovered automatically by the loader.
  const services = await createAgentSessionServices({
    cwd,
    agentDir: effectiveAgentDir,
    settingsManager,
    resourceLoaderOptions: {
      additionalExtensionPaths: bundledExtensionPaths,
      additionalSkillPaths: bundledSkillPaths,
    },
  });

  // 3. Session: wire together the services and session manager.
  const result = await createAgentSessionFromServices({
    services,
    sessionManager,
    sessionStartEvent,
  });

  return {
    ...result,
    services,
    diagnostics: services.diagnostics,
  };
};

// ── Launch ────────────────────────────────────────────────────────────────────

const cwd = process.cwd();

const runtime = await createAgentSessionRuntime(createRuntime, {
  cwd,
  agentDir,
  sessionManager: SessionManager.create(cwd),
});

const mode = new InteractiveMode(runtime, {
  migratedProviders: [],
  modelFallbackMessage: runtime.modelFallbackMessage,
});

await mode.run();
