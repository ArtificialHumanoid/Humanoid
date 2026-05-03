#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

python3 "$script_dir/install_act.py"

act_bin_dir="${HUMANOID_ACT_BIN_DIR:-$HOME/.local/bin}"
act_args=()
has_platform=false
for arg in "$@"; do
    case "$arg" in
        -P|--platform|--platform=*)
            has_platform=true
            ;;
    esac
done

if [ "$has_platform" = false ]; then
    act_args=(-P ubuntu-latest=-self-hosted --pull=false)
fi

exec "${HUMANOID_ACT_BIN:-$act_bin_dir/act}" "${act_args[@]}" "$@"
