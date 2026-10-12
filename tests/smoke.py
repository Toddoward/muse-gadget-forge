"""Forge smoke test on a real Docker host with a board plugged in.

  python tests/smoke.py <path-to-muse-local-gateway> [--keep]

Starts the gateway stack under project "mlg-forge-smoke" with USB + this forge, using the gateway's
smoke override (curl in place of the Tailscale sidecar), then checks the toolchain and the board.
"""
import json
import os
import subprocess
import sys
import time

GW = os.path.abspath(sys.argv[1])
FORGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "compose.forge.yaml")
FILES = ["compose.yaml", "tests/compose.smoke.yaml", "compose.usb.yaml", FORGE]
ENV = {**os.environ, "COMPOSE_FILE": "", "MUSE_SHARE": "./shared-smoke"}
failed = []


def dc(*args, check=True):
    cmd = ["docker", "compose", "-p", "mlg-forge-smoke"] + sum((["-f", f] for f in FILES), []) + list(args)
    r = subprocess.run(cmd, cwd=GW, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        sys.exit(f"FAILED: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def run(cmd, timeout=120):
    out = dc("exec", "-T", "tailscale", "curl", "-sS", "-m", "180", "-X", "POST", "-H", "Content-Type: application/json",
             "http://bench:8731/exec", "-d", json.dumps({"cmd": cmd, "timeout": timeout, "wait": 50}), check=False)
    try:
        v = json.loads(out)
    except ValueError:
        return {"stdout": "", "stderr": out}
    while v.get("status") == "running":
        v = json.loads(dc("exec", "-T", "tailscale", "curl", "-sS", f"http://bench:8731/exec/{v['id']}", check=False))
    return v


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"  -> {detail}"))
    if not ok:
        failed.append(name)


dc("up", "-d")
for _ in range(60):
    if '"ok": true' in dc("exec", "-T", "tailscale", "curl", "-sS", "http://bench:8731/health", check=False):
        break
    time.sleep(2)

v = run("idf.py --version")
check("ESP-IDF v6.0.1 in the bench", "v6.0.1" in v.get("stdout", ""), v)
v = run("esptool.py version")
check("esptool available", v.get("exit_code") == 0, v)
v = run("ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null")
ports = v.get("stdout", "").split()
check("a board is visible", bool(ports), v)
if ports:
    v = run(f"esptool.py --port {ports[0]} chip_id")
    check(f"chip_id on {ports[0]}", "Chip is" in v.get("stdout", "") or "Chip type" in v.get("stdout", ""), v)
    print("     " + next((l for l in v.get("stdout", "").splitlines() if "Chip" in l), ""))
v = run("mkdir -p /build/hello && cp -r $IDF_PATH/examples/get-started/hello_world /work/hello_world"
        " && idf.py -C /work/hello_world -B /build/hello set-target esp32s3 >/dev/null && idf.py -C /work/hello_world -B /build/hello build | tail -3", 900)
check("hello_world builds for esp32s3", v.get("exit_code") == 0 and "build" in v.get("stdout", "").lower(), v)

if "--keep" not in sys.argv:
    dc("down", "-v")
print("\nALL PASSED" if not failed else f"\n{len(failed)} FAILED: {failed}")
sys.exit(1 if failed else 0)
