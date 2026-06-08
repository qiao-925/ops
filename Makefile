# ops — 多仓库调度入口（薄封装层，逻辑在 bin/ops）
OPS_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BIN_LINK := $(HOME)/.local/bin/ops
SESSION_SYNC := $(OPS_ROOT)/../claude-session-sync
SESSION_REPO := git@github.com:qiao-925/claude-session-sync.git

.PHONY: sync status log help install

install:
	@echo "=== ops 全局环境安装 ==="
	@echo ""
	@# 确保 ~/.local/bin 存在
	@mkdir -p "$(HOME)/.local/bin"
	@# 全局命令链接
	@if [ -L "$(BIN_LINK)" ]; then \
		echo "[ok] ops 链接已存在"; \
	else \
		ln -sf "$(OPS_ROOT)/bin/ops" "$(BIN_LINK)"; \
		echo "[ok] 创建链接 $(BIN_LINK) -> $(OPS_ROOT)/bin/ops"; \
	fi
	@echo ""
	@# 确保 ~/.local/bin 在 PATH
	@if echo "$$PATH" | tr ':' '\n' | grep -qF "$(HOME)/.local/bin"; then \
		echo "[ok] ~/.local/bin 已在 PATH"; \
	else \
		echo '[!!] 请将 export PATH="$$HOME/.local/bin:$$PATH" 加入 ~/.bashrc'; \
	fi
	@echo ""
	@# Claude 会话同步仓库
	@if [ -d "$(SESSION_SYNC)" ]; then \
		echo "[ok] claude-session-sync 已存在"; \
	else \
		git clone "$(SESSION_REPO)" "$(SESSION_SYNC)"; \
		echo "[ok] 克隆 claude-session-sync"; \
	fi
	@echo ""
	@# 会话同步 cron
	@$(MAKE) -C "$(SESSION_SYNC)" cron-install
	@echo ""
	@echo "=== 安装完成 ==="
	@echo "现在可以从任意目录执行: ops sync / ops status"

sync:
	@$(OPS_ROOT)bin/ops sync

status:
	@$(OPS_ROOT)bin/ops status

log:
	@$(OPS_ROOT)bin/ops log

help:
	@$(OPS_ROOT)bin/ops help
