#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
toolchain_dir="${AGENTIC_TOOLCHAIN_DIR:-$repo_root/.agentic-toolchain}"
[[ $# -gt 0 ]] || { echo 'Usage: bash ops/with-toolchain.sh COMMAND [ARG...]' >&2; exit 2; }
exec "$toolchain_dir/bin/micromamba" run -p "$toolchain_dir/env" env \
  CPATH="$toolchain_dir/env/include" \
  LIBRARY_PATH="$toolchain_dir/env/lib" \
  LD_LIBRARY_PATH="$toolchain_dir/env/lib" "$@"
