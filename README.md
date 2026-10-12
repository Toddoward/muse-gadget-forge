[![English](https://img.shields.io/badge/lang-English-111111?style=flat-square)](README.md)
[![한국어](https://img.shields.io/badge/lang-%ED%95%9C%EA%B5%AD%EC%96%B4-lightgrey?style=flat-square)](README.kr.md)

# Muse Gadget Forge

**Gadgets give Muse ears and a voice. Local Gateway gives it hands and feet.<br>
Forge gives it a workbench — where Muse builds the next gadget itself.**

[![License](https://img.shields.io/badge/license-Apache--2.0-111111?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-111111?style=flat-square)](CHANGELOG.md)
[![Community skill](https://img.shields.io/badge/Muse-community%20skill-lightgrey?style=flat-square)](#faq)

Plug an ESP32 into your computer and ask Muse for a gadget. Muse writes the firmware, builds it with
ESP-IDF, flashes the board on your desk, reads its serial log, and fixes what broke — in a loop,
without you touching a terminal. Then you pair it in the Muse app, and the board talks to Muse on
its own over Wi-Fi.

Forge is an add-on for [**Muse Local Gateway**](https://github.com/Toddoward/muse-local-gateway):
it swaps the gateway's sandboxed shell for one with ESP-IDF v6.0.1 inside. Same locks, same
network mode, same single shared folder — plus your USB board.

> Unofficial community project. Not affiliated with or endorsed by the makers of Muse.

## Install

1. Set up [Muse Local Gateway](https://github.com/Toddoward/muse-local-gateway) and answer **y** to USB.
2. Put this repo next to it and run the installer (pulls ESP-IDF, about 5 GB the first time):

```bash
git clone https://github.com/Toddoward/muse-gadget-forge
./muse-gadget-forge/install.sh ./muse-local-gateway          # Linux
```

```powershell
git clone https://github.com/Toddoward/muse-gadget-forge
.\muse-gadget-forge\install.ps1 .\muse-local-gateway         # Windows
```

3. Tell Muse: *"Install the muse_gadget_forge skill from https://github.com/Toddoward/muse-gadget-forge."*

Remove it with `--remove` (`-Remove` on Windows); the plain shell comes back.

## Boards

| Board | Shows up as | Build | Flash |
|---|---|---|---|
| ESP32-S3, C3, C6 (native USB) | `/dev/ttyACM0` | ✅ ESP-IDF | ✅ |
| ESP32 DevKit (CP210x / CH340) | `/dev/ttyUSB0` | ✅ ESP-IDF | ✅ |
| ESP8266 (NodeMCU, D1 mini) | `/dev/ttyUSB0` | ❌ not in ESP-IDF | ✅ prebuilt images |

Linux and Windows (via usbipd-win). Not macOS — Docker Desktop can't pass USB through.

## What Muse will and won't do

- It asks before flashing — that replaces what the board was running.
- It never erases flash without asking — that wipes Wi-Fi settings and gadget pairing.
- Your Gadget SDK token comes from you, at gadgets.muse.ai, after you read the SDK terms.
- Pairing happens on your phone, in the Muse app. Your computer is the workbench, not a relay:
  once paired, the gadget needs nothing from it.

## FAQ

**Is this official?** No. It builds on the open-source
[Muse Gadget SDK](https://github.com/facebookincubator/muse-gadget-sdk) and on Muse Local Gateway.

**Do I need it to use the Gadget SDK?** No — you can flash by hand. Forge is for letting Muse do the
build-flash-debug loop itself.

## License

[Apache-2.0](LICENSE). "Muse" is a trademark of its owner, used here only to say what this works with.
