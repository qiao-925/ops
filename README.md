
# ops

个人运维集成面板 — 一个命令调度所有运维任务。

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/install.py | python3
```

## 用法

```bash
ops sync     # 同步所有仓库 + Claude 会话
ops status   # 查看同步状态
ops log      # 查看完整同步日志
```

## 架构

```
ops sync
 ├── 1. 仓库同步 (clone-faster)
 │    └── 完成后才能执行后续任务
 └── 2. Claude 会话同步 (claude-session-sync)
```

所有任务通过 subprocess 调用外部 CLI，零代码依赖。

## 目录

```
~/.local/share/ops/               ops 安装
~/.local/share/ops/repos/         数据仓库
~/.local/bin/ops                  全局命令
```

## 卸载

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/uninstall.py | python3
```
