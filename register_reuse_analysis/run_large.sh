#!/usr/bin/env bash
set -euo pipefail
analysis_dir=$(cd -- "$(dirname -- "$0")" && pwd)
analysis_python=${ANALYSIS_PYTHON:-python3}
exec "$analysis_python" "$analysis_dir/large_run.py" "$@"
