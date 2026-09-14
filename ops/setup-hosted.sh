#!/usr/bin/env bash
# Prepared setup for an isolated Codex environment; not executed by preflight.
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
if ! command -v clang >/dev/null || ! command -v bison >/dev/null || ! command -v flex >/dev/null || ! command -v rsync >/dev/null; then
  if [[ "${AGENTIC_INSTALL_DEPS:-0}" != 1 ]]; then
    echo 'Compiler dependencies missing. In hosted setup, set AGENTIC_INSTALL_DEPS=1 to install through apt.' >&2
    exit 2
  fi
  command -v apt-get >/dev/null || { echo 'This setup recipe requires an apt-based image.' >&2; exit 2; }
  if [[ "$(id -u)" == 0 ]]; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clang make bison flex rsync libncurses-dev ca-certificates curl
  else
    sudo -n apt-get update
    sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clang make bison flex rsync libncurses-dev ca-certificates curl
  fi
fi
node -e 'if(Number(process.versions.node.split(".")[0])<22)process.exit(2)'
git submodule update --init nethack-c/upstream
# Record installed versions and source pins; pin a successfully calibrated compiler
# version before reusing C recordings as ground truth. Do not infer equivalence.
clang --version
node --version
git -C nethack-c/upstream rev-parse HEAD
bash nethack-c/build-recorder.sh

# Linux minimal hints may omit the required runtime sysconf.
python3 ops/prepare-recorder-config.py
