#!/usr/bin/env bash
# Prefix-local compiler setup; no system package or sandbox changes.
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
toolchain_dir="${AGENTIC_TOOLCHAIN_DIR:-$repo_root/.agentic-toolchain}"
mkdir -p "$toolchain_dir/bin"
if [[ ! -f "$toolchain_dir/bin/micromamba" ]]; then
  curl -fLsS --connect-timeout 15 --max-time 120 \
    https://github.com/mamba-org/micromamba-releases/releases/download/2.9.0-0/micromamba-linux-64 \
    -o "$toolchain_dir/bin/micromamba"
fi
printf '%s  %s\n' 366cd9cd8be14df1ab8ed50352a82111082a36686b2d389fdb79a92c3fafb3e3 "$toolchain_dir/bin/micromamba" | sha256sum -c -
chmod +x "$toolchain_dir/bin/micromamba"
if [[ ! -x "$toolchain_dir/env/bin/clang" ]]; then
  "$toolchain_dir/bin/micromamba" create -y -p "$toolchain_dir/env" -f "$repo_root/ops/toolchain-linux-64.lock"
fi
AGENTIC_TOOLCHAIN_DIR="$toolchain_dir" bash "$repo_root/ops/with-toolchain.sh" bash "$repo_root/ops/setup-hosted.sh"
