#!/usr/bin/env bash
set -euo pipefail
analysis_dir=$(cd -- "$(dirname -- "$0")" && pwd)
workspace_dir=$(dirname -- "$analysis_dir")
repo_dir="$workspace_dir/GEM5"
if [[ ! -e "$repo_dir/ext/dramsim3/DRAMsim3" ]]; then
    if [[ -f /nfs/home/share/gem5_ci/DRAMsim3/libdramsim3.so ]]; then
        ln -s /nfs/home/share/gem5_ci/DRAMsim3 "$repo_dir/ext/dramsim3/DRAMsim3"
    else
        printf '%s\n' 'DRAMsim3 is missing; follow GEM5/ext/dramsim3/README.' >&2
        exit 1
    fi
fi
cd -- "$repo_dir"
exec scons "$workspace_dir/build/RISCV/gem5.opt" --gold-linker -j"${JOBS:-32}"
