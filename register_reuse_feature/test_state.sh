#!/usr/bin/env bash
set -euo pipefail
feature_dir=$(cd -- "$(dirname -- "$0")" && pwd)
workspace_dir=$(dirname -- "$feature_dir")
cd -- "$workspace_dir/GEM5"
reuse_cxx=${CXX:-g++}
"$reuse_cxx" -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
  -Isrc -Iext/googletest/googletest/include -Iext/googletest/googletest \
  src/cpu/o3/register_reuse_state.test.cc \
  ext/googletest/googletest/src/gtest-all.cc \
  ext/googletest/googletest/src/gtest_main.cc -pthread \
  -o "$feature_dir/reuse-state-tests"
exec "$feature_dir/reuse-state-tests"
