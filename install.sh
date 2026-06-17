#!/usr/bin/env bash
# ops 一键安装 — 兼容 curl | bash 分发方式，委托给 Python 实现
set -euo pipefail
exec python3 -c "
import urllib.request, sys, tempfile, os
url = 'https://raw.githubusercontent.com/qiao-925/ops/main/install.py'
with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='wb') as f:
    urllib.request.urlretrieve(url, f.name)
    os.execvp(sys.executable, [sys.executable, f.name])
"
