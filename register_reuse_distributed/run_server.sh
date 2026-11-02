#!/usr/bin/env bash
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
exec "${ANALYSIS_PYTHON:-python3}" "$script_dir/experiment.py" run "$@"
