#!/usr/bin/env bash
# Adds the forge to an existing muse-local-gateway install (Linux/macOS).
#   ./install.sh ../muse-local-gateway            add
#   ./install.sh ../muse-local-gateway --remove   back to the plain bench
set -euo pipefail
die() { echo "ERROR: $*" >&2; exit 1; }
gw="$(cd "${1:?usage: install.sh <path-to-muse-local-gateway> [--remove]}" && pwd)"
forge="$(cd "$(dirname "$0")" && pwd)/compose.forge.yaml"
[ -f "$gw/.env" ] || die "set up muse-local-gateway first ($gw/.env not found)"

# Rewrite COMPOSE_FILE in place; keep .env's permissions (it holds the Tailscale key).
line=$(grep '^COMPOSE_FILE=' "$gw/.env") || die "no COMPOSE_FILE in $gw/.env"
files=$(printf '%s' "${line#COMPOSE_FILE=}" | tr ';' '\n' | grep -v 'compose.forge.yaml' | paste -sd';' -)
[ "${2:-}" = "--remove" ] || files="$files;$forge"
tmp=$(mktemp "$gw/.env.XXXX"); chmod 600 "$tmp"
sed "s#^COMPOSE_FILE=.*#COMPOSE_FILE=$files#" "$gw/.env" > "$tmp" && mv "$tmp" "$gw/.env"

grep -q 'compose.usb.yaml' "$gw/.env" || echo "Note: USB serial is off in the gateway. Re-run its setup (delete .env first) and answer y to USB."
echo "Pulling ESP-IDF (about 5 GB the first time)..."
(cd "$gw" && docker compose up -d)
(cd "$gw" && docker compose exec -T bench idf.py --version) || die "bench did not come up with ESP-IDF"
