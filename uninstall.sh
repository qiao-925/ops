#!/usr/bin/env bash
# ops 一键卸载 — curl -fsSL <url>/uninstall.sh | bash
set -euo pipefail

OPS_DIR="$HOME/.local/share/ops"
BIN_LINK="$HOME/.local/bin/ops"

echo "=== ops 一键卸载 ==="
echo ""

# 1. 移除全局命令链接
if [ -L "$BIN_LINK" ]; then
    rm -f "$BIN_LINK"
    echo "[ok] 移除链接 $BIN_LINK"
else
    echo "[ok] 链接不存在，无需移除"
fi

# 2. 删除 ops 仓库目录
if [ -d "$OPS_DIR" ]; then
    rm -rf "$OPS_DIR"
    echo "[ok] 删除 $OPS_DIR"
fi

echo ""
echo "=== 卸载完成 ==="
