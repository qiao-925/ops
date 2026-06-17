
# ops

任务聚合平台 — 一个命令执行所有子任务，纯透传。

## 安装 / 重装

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/install.py | python3
```

已有旧版本会自动卸载后重装。

## 用法

```bash
ops sync     # 执行所有子任务的同步命令
ops status   # 执行所有子任务的状态命令
```

`ops sync` 等于你手动依次执行每个子任务的同步命令，输出完全一致。

## 新增任务

在 `bin/ops` 中加两个函数 + 注册到数组：

```bash
mytask_sync()   { some-cli sync; }
mytask_status() { some-cli status; }

SYNC_TASKS=(repo_sync session_sync mytask_status)
STATUS_TASKS=(repo_status session_status mytask_status)
```

## 目录

```
~/.local/share/ops/          ops 安装
~/.local/share/repos/        数据仓库 (齐平，互不影响)
~/.local/bin/ops             全局命令
```
