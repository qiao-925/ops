#!/usr/bin/env python3
"""ops 安装/重装 — curl -fsSL <url>/install.py | python3"""

import os
import shutil
import subprocess
from pathlib import Path

REPO = "qiao-925/ops"
OPS_DIR = Path.home() / ".local" / "share" / "ops"
BIN_LINK = Path.home() / ".local" / "bin" / "ops"
DATA_DIR = Path.home() / ".local" / "share" / "repos"

print("=== ops 安装 ===\n")

# 已有则先卸载
if BIN_LINK.is_symlink() or BIN_LINK.exists():
    BIN_LINK.unlink()
    print("[ok] 移除旧链接")
if OPS_DIR.exists():
    shutil.rmtree(OPS_DIR)
    print("[ok] 删除旧安装")

# 克隆
OPS_DIR.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(["gh", "repo", "clone", REPO, str(OPS_DIR)], check=True)
print(f"[ok] 克隆 → {OPS_DIR}")

# 链接
BIN_LINK.parent.mkdir(parents=True, exist_ok=True)
BIN_LINK.symlink_to(OPS_DIR / "bin" / "ops")
print(f"[ok] 链接 → {BIN_LINK}")

# PATH
local_bin = str(Path.home() / ".local" / "bin")
if local_bin in os.environ.get("PATH", "").split(":"):
    print("[ok] ~/.local/bin 已在 PATH")
else:
    print('[!!] 请将 export PATH="$HOME/.local/bin:$PATH" 加入 ~/.bashrc')

# 数据目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
print(f"[ok] 数据目录 → {DATA_DIR}")

print("\n=== 安装完成 ===")
