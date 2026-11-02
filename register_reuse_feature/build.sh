#!/usr/bin/env bash
set -euo pipefail
feature_dir=$(cd -- "$(dirname -- "$0")" && pwd)
workspace_dir=$(dirname -- "$feature_dir")
cd -- "$workspace_dir/GEM5"
exec scons "$feature_dir/build/RISCV/gem5.opt" --gold-linker -j"${JOBS:-32}"
