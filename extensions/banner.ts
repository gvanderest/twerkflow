import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

/**
 * banner.ts — bundled twerk extension
 *
 * Displays the TWERK version banner via the pi TUI on session start instead of
 * printing it to stdout before the TUI initialises.
 *
 * The version is injected by bin/twerk.js via the TWERK_VERSION environment
 * variable so the extension stays decoupled from package.json.
 */
export default function (pi: ExtensionAPI) {
  pi.on("session_start", (_event, ctx) => {
    const version = process.env.TWERK_VERSION;
    if (version) {
      ctx.ui.notify(`TWERK v${version}`, "info");
    }
  });
}
