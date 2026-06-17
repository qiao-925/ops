
# ops

任务聚合平台 — 三个字母，执行所有子任务。

## 安装 / 重装

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/install.py | python3
```

已有旧版本会自动卸载后重装。

## 用法

```bash
ops
```

## 新增任务

在 `bin/ops` 的 `COMMANDS` 数组中加一行：

```bash
COMMANDS=(
    "curl .../clone_faster.py | python3 - --output $SYNC_DIR"
    "make -C .../claude-session-sync sync"
    "curl .../new_task.py | python3 -"     # ← 加这里
)
```

## 目录

```
~/.local/share/ops/          ops 安装
~/.local/share/repos/        数据仓库 (齐平，互不影响)
~/.local/bin/ops             全局命令
```
