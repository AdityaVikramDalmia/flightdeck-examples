#!/usr/bin/env bash
# Deprecated reference example for new Claude Code integrations (2026-09-22).
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
TOOLS_ROOT=${FLIGHTDECK_TOOLS_ROOT:-$(cd "$ROOT/.." && pwd)}
exec bash "$TOOLS_ROOT/config-baseline/examples/demo.sh"
