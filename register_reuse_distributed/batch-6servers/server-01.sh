#!/usr/bin/env bash
set -euo pipefail
plan_dir=$(cd -- "$(dirname -- "$0")" && pwd)
workspace=${REGISTER_REUSE_WORKSPACE:-/nfs/home/liuchanghe/register_reuse}
exec "${ANALYSIS_PYTHON:-python3}" "$workspace/register_reuse_distributed/experiment.py" run --plan "$plan_dir/plan.json" --shard-id 1 --workspace "$workspace" "$@"
