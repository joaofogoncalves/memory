# Image Prompts

## Option 1 (chosen): Screenshot of the roadmap page
Cropped from `https://bridgeport.bridgein.com/roadmap/`, the "Milestone 4.0 — Up next" heading plus the first two full epic cards ("Progressive delivery & safe rollouts" and "Proactive alerting & observability"), each collapsed to their goal statement with the "Issues in this epic" disclosure — no browser chrome, native dark theme. Captured via a scripted Playwright clip against the live page's DOM (`section.milestone` bounding box through the second `article.epic` card), then trimmed and exported to webp.

## Option 2 (not used): Chart — feature-compare
```json
{
  "title": "What breaks trust vs. what 4.0 fixes",
  "subtitle": "BridgePort roadmap — Milestone 4.0",
  "arrowLabel": "closes the gap",
  "left": {
    "label": "The gap",
    "title": "Why teams stay on managed platforms",
    "items": [
      "No audit trail when someone leaves",
      "A bad rollout is a fire drill",
      "Backups nobody's tested a restore on",
      "No SSO, no 2FA",
      "Secrets hardcoded in a compose file"
    ]
  },
  "right": {
    "label": "Milestone 4.0",
    "title": "Closed, epic by epic",
    "items": [
      "Audit-log export",
      "One-click rollback + phased rollouts",
      "Real backup restore, not just backup",
      "SSO + 2FA",
      "Secrets pulled from Vault"
    ]
  }
}
```

## Option 3 (not used): AI conceptual illustration
A single dark-navy keystone or bridge foundation glowing faintly from within with one teal light path running through its structure, holding steady under visible load lines pressing down from above. Minimal, geometric, no human figures, no text overlay, no floating 3D icons. Deep navy background (#0e131e-adjacent), one teal accent (#44d8f1-adjacent) tracing the load path.
Format: 1440x900px (16:10) · PNG or JPG
