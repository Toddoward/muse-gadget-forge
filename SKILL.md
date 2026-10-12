---
name: "muse_gadget_forge"
description: "Build, flash and debug ESP32 firmware — including Muse Gadget SDK gadgets — on boards plugged into the user's own computer, through the muse_local_gateway bench running ESP-IDF. Use when the user wants Muse to make, update, or troubleshoot an ESP32 / ESP32-S3 / C3 / C6 device on their desk."
---

# Muse Gadget Forge

Community skill, not an official Muse feature. Source: https://github.com/Toddoward/muse-gadget-forge
Runs **on top of `muse_local_gateway`**: every command below goes through
`bin/gateway-exec.sh <ip>:8731 '<cmd>' [cwd] [timeout]` from that skill.

## Before anything
1. `gateway-exec.sh <ip>:8731 'idf.py --version'` — expect `ESP-IDF v6.0.1`. If `idf.py` is missing,
   the user has not installed the forge (`install.sh` / `install.ps1` in this repo): tell them.
2. `gateway-exec.sh <ip>:8731 'ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null'` — no output means no board
   is visible: USB is off in the gateway, the cable is charge-only, or (Windows) the attach watcher
   has not run yet. See the gateway's `docs/usb-serial.md`.
3. Identify the chip before building: `python -m esptool --port <port> chip-id`
   (ESP-IDF v6 ships esptool v5: commands use hyphens — `chip-id`, `write-flash`, `erase-flash`). Native USB boards
   (S3/C3/C6) are `ttyACM*`; CP210x/CH340 bridges are `ttyUSB*`.

## Build and flash
- Sources live in `/work/<project>` (the user's shared folder). Build output goes to the fast
  volume: `idf.py -C /work/<project> -B /build/<project> set-target esp32s3` then `... build`.
- Flash: `idf.py -C /work/<project> -B /build/<project> -p <port> flash` (timeout 600).
- Read the log — there is no TTY, so never `idf.py monitor` or `miniterm`:
  `stty -F <port> 115200 raw -echo; timeout 15 cat <port>`
  Boards with native USB reset when flashed; wait 2 s before reading.
- ESP8266 is not supported by ESP-IDF. You can still identify it and flash a prebuilt image with
  `python -m esptool --port <port> write-flash 0x0 <file>.bin`.

## Muse Gadget SDK
- SDK: https://github.com/facebookincubator/muse-gadget-sdk (Apache-2.0). Clone it into
  `/work/muse-gadget-sdk` and follow its ESP32 guide; its `AGENTS.md` files are written for agents.
- Each gadget needs an SDK token from gadgets.muse.ai. The **user** creates it and the user reads
  the Gadget SDK Terms. Tokens are identifiers, not passwords — still, don't echo them into chat
  or commit them. If one leaks, the user revokes it and you rebuild.
- Custom commands: advertise them in `link.register`, handle them in `main/app.c`.
- Pairing happens in the Muse app on the user's phone (Bluetooth LE). After that the board talks
  to Muse over Wi-Fi by itself — the bench is the workbench, not a relay. Never design a flow that
  needs the user's computer at runtime.

## Rules
- **Ask before flashing.** It replaces whatever the board was running.
- **Never `erase-flash` without asking.** It wipes Wi-Fi credentials and gadget pairing (NVS).
- One board per task. If several ports exist, name the one you will use and why.
- Report: chip, port, what was built (commit or file), flash result, and the first lines of the log.
