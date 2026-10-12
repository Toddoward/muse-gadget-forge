# Changelog

## Unreleased

- Skill name is now `muse-gadget-forge` (lowercase-hyphen, the Agent Skills convention).
- The Gadget SDK token no longer goes through chat: the user drops it in `.gadget-token` in the shared
  folder; Muse moves it to `/build` unread and appends it to the build's `sdkconfig`.

## 0.1.0 — 2026-10-12

First public release.

- `SKILL.md`: Muse sets up ESP-IDF v6.0.1 on its muse-local-gateway workbench by itself, then
  builds, flashes and reads a Muse Gadget SDK device, following the SDK's own `AGENTS.md`.
  Rules for flashing, erasing, tokens and anything physical.
- Logo: the shared `>_` mark (generated in muse-local-gateway `docs/media/make_logo.py`).
- `tests/smoke.py`: the same procedure on a real host, in the gateway's default `isolated` mode.
