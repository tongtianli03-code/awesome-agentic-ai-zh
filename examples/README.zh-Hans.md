> [繁體中文](./README.md) | **简体中文** | [English](./README.en.md)

# `examples/` — 动手练习可跑范例

> [← 回主路线 README](../README.zh-Hans.md)

学习地图每个 stage 都有「动手练习」section、讲「该做什么」。这个资料夹补上**真的可以跑的范例 code**——复制 → 装依赖 → `python starter.py` 看到预期输出。

## 目录结构

```
examples/
├── stage-3/                     # Tool Use & Agent 入门
│   ├── 03-react-from-scratch/   # 练习 3：从零实现 ReAct
│   │   ├── starter.py           # 主程式（~70 行可跑）
│   │   ├── test.py              # 自我验证（pure assert、无 pytest）
│   │   ├── README.md            # 200-400 字走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 依赖钉版本
│   └── ...
├── stage-1/
└── ...
```

短的练习（≤30 LOC）直接以 `<details>` 收摺塞在 stage 档内、不开资料夹。长的（>30 LOC）才开资料夹——避免 stage 档被 code block 撑爆。

## 怎么跑任一个范例

```bash
cd examples/stage-3/03-react-from-scratch
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # 各范例顶端会说它要哪个 key
python starter.py                     # 跑真的 API 看输出（会花一点点钱、约 $0.001）
python test.py                        # 跑验证（用 mock、不花钱）
```

## 设计原则

| 维度 | 规则 |
|---|---|
| 程式长度 | starter ≤80 LOC、超过拆档 |
| 依赖 | stdlib + 最多 2 个 pip 套件、钉版本 |
| 测试 | 纯 `assert`、不用 pytest、reader 跑 `python test.py` 看 ✅ |
| 注解 | 中文（zh-Hans 为主）、变数 / 函式名英文 |
| 自我验证 | 每个 starter.py 结尾必有 `# === 自我验证 ===` 区块 |
| 环境变数 | 顶端注解写清楚需要哪些 key |
| Free-tier 友善 | 用最便宜 model（claude-haiku / Ollama）、注解写怎么换 Sonnet |
| **Windows 编码** | **每个 .py 顶端必须有 UTF-8 reconfigure**（见下） |

### Windows cp950 编码 fix（每个 starter.py / test.py 必加）

Windows 预设 console 是 cp950（Big5）、印不出 emoji 跟非 Big5 中文。每个 `.py` 档顶端 import 区后立刻加：

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

否则 Windows reader 在 PowerShell / cmd 跑会炸 `UnicodeEncodeError: 'cp950' codec can't encode character '✅'`。

## 没 API key 也能练习吗？

可以的两条路：
1. **Ollama 本机跑**：每个有 Ollama 替代版本的 starter 会有 `starter_ollama.py` 对照
2. **Mock 模式**：所有 `test.py` 都用 `unittest.mock` 不打 API、reader 可以先看程式逻辑通过再决定要不要花钱跑真实 API

## 对应 stage 索引

| Stage | 练习 | 范例位置 |
|---|---|---|
| 1 LLM 基础 | 6 个 | inline 4 + folder 2（`examples/stage-1/`） |
| 2 Prompt eng | 4 个 | 全 inline |
| **3 Tool use** | **6 个** | inline 1 + folder 5（`examples/stage-3/`） |
| 4 Frameworks | 5 个 | 全 folder（`examples/stage-4/`） |
| 5 Claude Code 生态 | 11 个 | inline 6 + folder 5（`examples/stage-5/`） |
| 6 Memory/RAG | 5 个 | 全 folder（`examples/stage-6/`） |
| 7 Multi-agent | 5 个 | inline 1 + folder 4（`examples/stage-7/`） |
| Track A1-A3 | 12 个 | 全 inline、外加 2 个小 folder（CLI-9 / CLI-10） |

→ T1 完成范围：**只有 Stage 3 全部 6 个**（剩余 stage 按 plan 分批推进）。

## 贡献 / 报错

跑不过、结果跟预期输出对不上、或想补一个新练习：
- 开 issue 标 `examples` label
- 或直接 PR、follow 本资料夹「设计原则」表格的规则

## 为什么这样分（不直接全塞 stage 档）

1. **Stage 档保持 readable**：学习地图读者不一定要看 code、只想理解 concept；长 code block 干扰阅读流
2. **范例可独立演进**：API SDK 升版、model name 改、范例需要单独 commit、不污染学习地图 git log
3. **Reader 可以 clone 单一 example**：`svn export` 或 `git clone --filter=tree:0` 只抓一个资料夹
4. **未来 CI**：example 失败不应 block mdbook deploy；分开可让 CI 有条件性检查
