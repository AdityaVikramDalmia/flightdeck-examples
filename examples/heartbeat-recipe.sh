#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TOOLS_ROOT=${FLIGHTDECK_TOOLS_ROOT:-$(cd "$ROOT/.." && pwd)}
exec bash "$TOOLS_ROOT/job-heartbeat/examples/demo.sh"
