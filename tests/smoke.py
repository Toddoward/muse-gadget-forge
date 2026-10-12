"""Forge smoke test: does Muse's own procedure (SKILL.md) work in a plain, isolated bench?

  python tests/smoke.py <path-to-muse-local-gateway> [--keep]

Starts the gateway stack (project "mlg-forge-smoke", isolated mode + USB, curl standing in for the
Tailscale sidecar), then does what SKILL.md tells Muse to do: install ESP-IDF v6.0.1 into /build
through the proxy, identify the board, and build the Muse Gadget SDK firmware for an ESP32-S3.
/build is a volume, so a second run skips the install (use `down -v` to start clean).
"""
import json
import os
import subprocess
import sys
import time

GW = os.path.abspath(sys.argv[1])
FILES = ["compose.yaml", "tests/compose.smoke.yaml", "compose.usb.yaml"]
ENV = {**os.environ, "COMPOSE_FILE": "", "MUSE_SHARE": "./shared-smoke"}
IDF = "export IDF_PATH=/build/esp-idf IDF_TOOLS_PATH=/build/.espressif; . $IDF_PATH/export.sh >/dev/null 2>&1; "
failed = []


def dc(*args, check=True):
    cmd = ["docker", "compose", "-p", "mlg-forge-smoke"] + sum((["-f", f] for f in FILES), []) + list(args)
    r = subprocess.run(cmd, cwd=GW, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def curl(*args):
    return dc("exec", "-T", "tailscale", "curl", "-sS", "-m", "90", *args, check=False)


def run(cmd, timeout=600):
    out = curl("-X", "POST", "-H", "Content-Type: application/json", "http://bench:8731/exec",
               "-d", json.dumps({"cmd": cmd, "timeout": timeout, "wait": 50}))
    try:
        v = json.loads(out)
        while v.get("status") == "running":
            time.sleep(10)
            v = json.loads(curl(f"http://bench:8731/exec/{v['id']}"))
        return v
    except (ValueError, KeyError):
        return {"stdout": "", "stderr": out}


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"  -> {json.dumps(detail)[-1500:]}"), flush=True)
    if not ok:
        failed.append(name)


dc("up", "-d", "--build")
for _ in range(60):
    if '"ok": true' in curl("http://bench:8731/health"):
        break
    time.sleep(2)

t0 = time.time()
v = run("test -x /build/esp-idf/install.sh || git clone -q -b v6.0.1 --depth 1 --recursive --shallow-submodules "
        "https://github.com/espressif/esp-idf.git /build/esp-idf; "
        "IDF_TOOLS_PATH=/build/.espressif /build/esp-idf/install.sh esp32s3 > /build/idf-install.log 2>&1; "
        "rc=$?; tail -3 /build/idf-install.log; exit $rc", 3600)
check(f"ESP-IDF v6.0.1 installed through the proxy ({time.time() - t0:.0f} s)", v.get("exit_code") == 0, v)
v = run(IDF + "idf.py --version")
check("idf.py works", "v6.0.1" in v.get("stdout", ""), v)

v = run("ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")
ports = v.get("stdout", "").split()
check("a board is visible", bool(ports), v)
if ports:
    v = run(IDF + f"python -m esptool --port {ports[0]} chip-id")
    check(f"chip-id on {ports[0]}", "Chip type" in v.get("stdout", "") or "Chip is" in v.get("stdout", ""), v)
    print("     " + next((l.strip() for l in v.get("stdout", "").splitlines() if "Chip" in l), ""))

t0 = time.time()
v = run("cd /build && (test -d muse-gadget-sdk || git clone -q --depth 1 https://github.com/facebookincubator/muse-gadget-sdk.git) && "
        "cd muse-gadget-sdk/esp32 && " + IDF +
        "tools/board.sh espressif-s3-devkitc-1 build > /build/gadget-build.log 2>&1; rc=$?; tail -4 /build/gadget-build.log; exit $rc", 3600)
check(f"Muse Gadget SDK firmware builds for ESP32-S3 DevKitC-1 ({time.time() - t0:.0f} s)", v.get("exit_code") == 0, v)

if "--keep" not in sys.argv:
    dc("down", "-v")
print("\nALL PASSED" if not failed else f"\n{len(failed)} FAILED: {failed}")
sys.exit(1 if failed else 0)
