#!/usr/bin/env bash
# ops 一键安装 — curl -fsSL <url>/install.sh | bash
set -euo pipefail

REPO="qiao-925/ops"
OPS_DIR="$HOME/.local/share/ops"
BIN_LINK="$HOME/.local/bin/ops"

echo "=== ops 一键安装 ==="
echo ""

# 1. 克隆 ops 仓库
if [ -d "$OPS_DIR" ]; then
    echo "[ok] ops 仓库已存在"
else
    mkdir -p "$(dirname "$OPS_DIR")"
    gh repo clone "$REPO" "$OPS_DIR"
    echo "[ok] 克隆 ops 仓库"
fi

# 2. 创建全局命令链接
mkdir -p "$HOME/.local/bin"
if [ -L "$BIN_LINK" ]; then
    echo "[ok] ops 链接已存在"
else
    ln -sf "$OPS_DIR/bin/ops" "$BIN_LINK"
    echo "[ok] 创建链接 $BIN_LINK"
fi

# 3. 检查 PATH
if echo "$PATH" | tr ':' '\n' | grep -qF "$HOME/.local/bin"; then
    echo "[ok] ~/.local/bin 已在 PATH"
else
    echo '[!!] 请将 export PATH="$HOME/.local/bin:$PATH" 加入 ~/.bashrc'
fi

# 4. 创建同步目录
mkdir -p "$HOME/.local/share/ops/repos"
echo "[ok] 同步目录 ~/.local/share/ops/repos"

echo ""
echo "=== 安装完成 ==="
echo "现在可以从任意目录执行: ops sync / ops status"
