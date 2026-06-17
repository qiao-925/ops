
# ops

个人运维集成面板 — 批量调度独立运维任务，全部并行执行。

## 设计原则

- **ops = 调度层** — 只负责发现任务、并行执行、聚合展示。不包含任何领域逻辑。
- **子任务完全独立** — 每个任务通过 CLI (subprocess) 调用，零代码依赖，可单独使用。
- **插件化** — 新增任务 = 往 `ops/tasks/` 丢一个文件，自动发现、自动并行。

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/install.sh | bash
```

或直接用 Python：

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/install.py | python3
```

## 用法

```bash
ops sync       # 并行执行所有同步任务
ops status     # 查看同步状态和各任务状态
ops log        # 查看完整同步日志
ops tasks      # 列出所有已注册任务
```

## 架构

```
ops (Python, 集成面板)
├── 调度: 并行执行 N 个独立任务
├── 聚合: 统一的日志、状态展示
└── 入口: ops sync / ops status / ops tasks

  ↓ subprocess 调用 (零代码依赖)

tasks/
  repo-sync      → curl clone_faster.py | python3 (独立 CLI)
  session-sync   → make -C claude-session-sync sync (独立 CLI)
  ...            → 更多独立任务
```

## 新增任务

在 `ops/tasks/` 下新建一个 `.py` 文件：

```python
from ops.task import Task, TaskContext, TaskResult

class MyTask(Task):
    name = "my-task"
    description = "我的自定义任务"

    def run(self, ctx: TaskContext) -> TaskResult:
        # 执行逻辑，通过 subprocess 调用外部 CLI
        return TaskResult(success=True, summary="完成")

    def status(self, ctx: TaskContext) -> str:
        return "状态信息"
```

自动发现，无需修改任何其他文件。

## 卸载

```bash
curl -fsSL https://raw.githubusercontent.com/qiao-925/ops/main/uninstall.sh | bash
```
