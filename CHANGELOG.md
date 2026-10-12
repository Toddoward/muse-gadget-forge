# Changelog

## 0.1.0 — 2026-10-12

First public release.

- `compose.forge.yaml`: swaps the muse-local-gateway bench for `espressif/idf:v6.0.1`.
- `install.sh` / `install.ps1`: add or remove the forge in an existing gateway install.
- `SKILL.md` for Muse: identify, build, flash, read serial without a TTY; Gadget SDK notes; flashing rules.
- `tests/smoke.py`: toolchain, board detection and an ESP32-S3 build on a real host.
