#!/usr/bin/env bash
# Smoke-check the HireForce vision service (expects it on VISION_URL).

set -euo pipefail

VISION_URL="${VISION_URL:-http://localhost:8001}"
VISION_URL="${VISION_URL%/}"

echo "Checking ${VISION_URL}/health ..."
health="$(curl -fsS "${VISION_URL}/health")"
echo "health: ${health}"

python - <<'PY' "${health}"
import json, sys
payload = json.loads(sys.argv[1])
if not payload.get("ok") or not payload.get("ready"):
    raise SystemExit("vision /health reported not ready")
print(f"detector={payload.get('detector')} version={payload.get('version')}")
PY

# 1x1 PNG — valid decode path, zero faces expected.
TINY_PNG_B64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

echo "Checking ${VISION_URL}/detect ..."
headers=(-H "Content-Type: application/json")
if [[ -n "${VISION_SHARED_SECRET:-}" ]]; then
  headers+=(-H "X-Vision-Secret: ${VISION_SHARED_SECRET}")
fi

detect="$(curl -fsS "${VISION_URL}/detect" "${headers[@]}" \
  -d "{\"frames\":[\"${TINY_PNG_B64}\"],\"checks\":[\"face_count\"]}")"
echo "detect: ${detect}"

python - <<'PY' "${detect}"
import json, sys
payload = json.loads(sys.argv[1])
if "face_count" not in payload or "per_frame" not in payload:
    raise SystemExit("vision /detect missing required fields")
print("vision smoke check passed")
PY
