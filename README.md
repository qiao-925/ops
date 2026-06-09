
# ops

所有仓库 + Claude 会话的统一调度入口。

## 安装

首次使用需在项目目录执行一次安装：

```bash
make install
```

这会完成：
- 创建 `~/.local/bin/ops` 全局命令链接
- 确保 `~/.local/bin` 在 PATH 中

## 用法

`ops` 已链接到 `~/.local/bin/ops`（全局可用），从任意目录执行：

```bash
ops sync     # 仓库更新 + Claude 会话同步
ops status   # 查看同步状态、记录、统计
ops log      # 查看完整同步日志
ops help     # 查看帮助
```

所有 `ops` 命令也可在项目目录通过 Makefile 调用：

```bash
make sync    # 等同于 ops sync
make status  # 等同于 ops status
make log     # 等同于 ops log
make help    # 等同于 ops help
```

### 架构

```
ops sync
 ├── 1/2 仓库同步
 │    └── curl clone_faster.py | python3 - --output ~/.local/share/ops/repos
 │        ├── git clone --depth 1 (首次)
 │        └── git fetch --depth 1   (后续增量)
 └── 2/2 Claude 会话同步
      └── make -C ~/.local/share/ops/repos/qiao-925/claude-session-sync sync
           ├── git pull --rebase
           ├── cp -ru 双向同步 ~/.claude/projects/
           └── git commit + push (有变化时)
```

仓库数据统一存放在 `~/.local/share/ops/repos/`，可通过 `OPS_SYNC_DIR` 环境变量自定义。

同步日志记录在 `.sync.log`，包含每次的开始/结束时间和各步骤退出码。
