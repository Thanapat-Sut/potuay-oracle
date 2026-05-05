---
query: "claude-browser-proxy"
target: "Soul-Brews-Studio/claude-browser-proxy"
mode: deep
timestamp: 2026-02-17 14:32
---

# Trace: claude-browser-proxy

**Target**: Soul-Brews-Studio/claude-browser-proxy
**Mode**: deep (5 parallel agents)
**Time**: 2026-02-17 14:32 SEAST

## Summary

Chrome extension (v2.9.39) that bridges Claude Code CLI with Google Gemini via MQTT.
Architecture: `Claude CLI <-> Mosquitto Broker (TCP:1883 + WS:9001) <-> Chrome Extension <-> Gemini Tab`

## Repo Structure

```
claude-browser-proxy/          # 16 files, ~3,600 LOC
├── manifest.json              # MV3 config, v2.9.39
├── background.js              # 1,218 lines - MQTT client + command router
├── content.js                 # 394 lines - DOM injection on Gemini pages
├── sidepanel.js               # 432 lines - Debug UI + state monitoring
├── popup.js                   # 40 lines - Quick status popup
├── popup.html / sidepanel.html / debug.html
├── mqtt.min.js                # Bundled MQTT.js library
├── claude-browser.sh          # 101 lines - CLI wrapper
├── icons/                     # Extension icons
├── README.md                  # 359 lines (EN + TH)
└── LICENSE                    # MIT (2025 Soul Brews Studio)
```

## MQTT Topics

| Topic | Direction | Retained | Purpose |
|-------|-----------|----------|---------|
| `claude/browser/command` | CLI -> Ext | No | Commands |
| `claude/browser/response` | Ext -> CLI | Yes | Results |
| `claude/browser/status` | Ext -> CLI | Yes (LWT) | Online/offline |
| `claude/browser/answer` | Ext -> CLI | Yes | Gemini responses |
| `claude/browser/state` | Ext -> CLI | No | Loading/tool state |
| `claude/browser/page` | Ext -> CLI | Yes | Page URL/title |

## Commands (40+)

- **Tab**: create_tab, list_tabs, focus_tab, new_tab
- **Content**: get_html, get_text, get_url, get_videos, get_state, get_response
- **DOM**: click, clickText, type, find, key, execute
- **Gemini**: chat, select_model, select_mode, wait_response, transcribe
- **Utility**: screenshot, download, inject_badge, inject_response_actions
- **Auto**: auto_inject_start, auto_inject_stop

## Git History

- **43 commits** (2026-01-04 to 2026-01-29)
- **1 contributor**: Nat (nazt, nat.wrw@gmail.com)
- **1 branch**: main
- **No tags, no releases**
- **1 open issue**: Bug: tab variable ReferenceError at line 999

### Development Phases
1. **Jan 04**: Initial build (12 commits, v1.0.0 -> v1.2.0)
2. **Jan 12**: Model selection (5 commits, v1.6.0 -> v1.7.0)
3. **Jan 13**: Rapid iteration (20 commits, v2.3.0 -> v2.6.4)
4. **Jan 14-16**: Refinement (4 commits, v2.6.5 -> v2.6.8)
5. **Jan 29**: Release prep (2 commits, tab management PR + docs)

## GitHub

- **Repo**: Soul-Brews-Studio/claude-browser-proxy
- **Issues**: 1 open (ReferenceError bug)
- **PRs**: 0
- **Releases**: 0
- **License**: MIT

## Cross-Repo References

### oracle-skills-cli (51 files)
- `src/skills/gemini/scripts/*.ts` - 24 TypeScript scripts using MQTT
- `src/skills/deep-research/scripts/deep-research.ts`
- `src/skills/watch/scripts/transcribe.ts`
- `ψ/memory/learnings/` - 12 learning docs
- `ψ/memory/retrospectives/` - 9 retrospectives
- `ψ/inbox/handoff/` - 7 handoff docs
- `package.json` depends on `mqtt@^5.8.0`

### Skill Dependencies
```
/gemini skill  -> gemini scripts -> MQTT -> extension -> Gemini
/watch skill   -> transcribe.ts  -> MQTT -> extension -> Gemini
/deep-research -> deep-research.ts -> MQTT -> extension -> Gemini
/slides skill  -> gemini_chat.py -> mosquitto CLI -> broker
```

### Alternative: dev-browser
- CDP-based approach (Chrome DevTools Protocol)
- Different architecture, not MQTT

## Oracle Memory (30+ files)

### Documentation (ψ/learn/)
- `claude-browser-proxy.md` - Main index
- `2026-02-17/1325_ARCHITECTURE.md` - 1,371 lines
- `2026-02-17/1325_CODE-SNIPPETS.md` - 1,633 lines
- `2026-02-17/1325_QUICK-REFERENCE.md` - 546 lines

### Historical (archived oracle)
- 12 retrospectives tracking v1.0.0 -> v2.6.5 evolution
- 12 learning documents on MQTT patterns
- Track file: `008-claude-browser-proxy.md`

## Key Design Patterns

1. **Stale Message Filtering**: `command.ts < connectedAt` -> ignore
2. **Subscribe-Before-Publish**: CLI subscribes to response topic before publishing command
3. **LWT (Last Will & Testament)**: Auto-offline status on disconnect
4. **Selector Fallback Chain**: Multiple CSS selectors tried in order
5. **MutationObserver**: Auto-inject buttons on DOM changes
6. **Tab Precision**: Commands target specific tabId for multi-tab workflows

## Configuration

```conf
# D:/Claude/.config/mosquitto.conf
allow_anonymous true
listener 1883 localhost      # TCP for CLI/scripts
listener 9001                # WebSocket for Chrome extension
protocol websockets
```

## Version Timeline

| Version | Date | Milestone |
|---------|------|-----------|
| v1.0.0 | 2026-01-04 | Initial extension |
| v1.2.0 | 2026-01-04 | Vanilla JS (dropped React) |
| v1.6.0 | 2026-01-12 | select_model command |
| v2.3.0 | 2026-01-13 | State detection + get_state |
| v2.6.5 | 2026-01-14 | get_response MQTT action |
| v2.6.8 | 2026-01-16 | chat action (all-in-one) |
| v2.9.39 | 2026-01-29 | Tab management + open source prep |
