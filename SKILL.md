---
name: "muse_gadget_forge"
description: "Build your own Muse gadget — your ears and voice in the user's room — on the user's own computer: set up ESP-IDF on the muse_local_gateway workbench, build the Muse Gadget SDK firmware, flash the ESP32 board on their USB port, read its log, and walk the user through pairing. Use when the user wants a new or updated Muse gadget, or one that misbehaves."
---

# Muse Gadget Forge

Community skill, not an official Muse feature. Source: https://github.com/Toddoward/muse-gadget-forge

Everything here runs on the user's workbench through the **muse_local_gateway** skill:
`bin/gateway-exec.sh <ip>:8731 '<cmd>' [cwd] [timeout]`. The workbench is a plain Linux shell with
internet through a proxy, the user's shared folder at `/work`, a fast persistent volume at `/build`,
and (if the user enabled it) their USB serial boards under `/dev`.

**The Muse Gadget SDK is the source of truth.** Its `esp32/AGENTS.md` is written for agents like you:
boards, build profiles, token, flashing, pairing, and what never to touch. Read it before building.
This skill only adds what is different on the workbench.

## 1. Toolchain (once)
The SDK pins **ESP-IDF v6.0.1**. Install it into `/build` so it survives restarts:

```sh
git clone -q -b v6.0.1 --depth 1 --recursive --shallow-submodules https://github.com/espressif/esp-idf.git /build/esp-idf
export IDF_TOOLS_PATH=/build/.espressif
/build/esp-idf/install.sh esp32s3      # add targets as needed: esp32s3,esp32c6
python3 /build/esp-idf/tools/idf_tools.py install cmake ninja   # the workbench has no system cmake
```
Run it with a timeout of 3600 and tell the user it takes a while the first time. Skip if
`/build/esp-idf/install.sh` already exists. Start **every** later command with this (the workbench
shell is `sh`, where `export.sh` can't find itself — hence `IDF_PATH`):

```sh
export IDF_PATH=/build/esp-idf IDF_TOOLS_PATH=/build/.espressif; . $IDF_PATH/export.sh >/dev/null 2>&1;
```

## 2. The SDK
`git clone --depth 1 https://github.com/facebookincubator/muse-gadget-sdk.git /build/muse-gadget-sdk`,
then read `/build/muse-gadget-sdk/esp32/AGENTS.md` and `esp32/devices/README.md`.
Build under `/build` (fast); copy finished images to `/work/gadgets/<name>/` so the user can see them.

## 3. Which board
- `ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null` — nothing means USB is off in the gateway, the cable is
  charge-only, or (Windows) the attach watcher hasn't caught it yet. Ask the user.
- `python -m esptool --port <port> chip-id` (esptool v5: hyphenated commands — `chip-id`, `write-flash`).
- Match chip, USB IDs and what the user tells you against the SDK's board table. If unsure, ask.

## 4. Token
Every gadget needs the user's SDK token (`mgst_…`, from gadgets.muse.ai → Account → SDK tokens).
Ask the user for it; put it in the build directory's `sdkconfig` as `CONFIG_GADGET_SDK_TOKEN`.
Never print it in full, never commit it, never leave it in `/work`. The token is personal and for
non-commercial use; a gadget built with it may be given to others but not sold or presented as
made or endorsed by Meta (Gadget SDK Token Terms).

## 5. Build, flash, read
- Build with the SDK's helper for that board (e.g. `tools/board.sh espressif-s3-devkitc-1 build`)
  from `/build/muse-gadget-sdk/esp32`, timeout 3600. Judge success by the exit code, not by output.
- **Ask before flashing** — it replaces what the board runs. Then the helper's `flash <port>`.
- There is no TTY: never `idf.py monitor` or `miniterm`. Read with
  `stty -F <port> 115200 raw -echo; timeout 15 cat <port>` (or the SDK's read-only snippet).
  A healthy boot reaches `link.main: Muse Gadget starting`.

## 6. Pairing (the user's part)
Tell the user: Muse app → Settings → Devices → Developer mode → pick `MuseGadget-…`. The light
breathes orange while waiting, blue to confirm (short-press the button), green when connected.
After that the gadget talks to you over Wi-Fi on its own; the workbench is not involved at runtime.

## Rules
- Never `erase-flash` without asking — it wipes Wi-Fi and pairing. Never enable Secure Boot,
  flash encryption or pairing eFuses. Follow every warning in the SDK's `AGENTS.md`.
- Anything that moves (motors, relays, heaters): confirm with the user what it may do. Muse's terms
  forbid controlling physical systems in ways that could endanger people.
- Report: board, port, profile, build result, flash result, and the first boot-log lines.
