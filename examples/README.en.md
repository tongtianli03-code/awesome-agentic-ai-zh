> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# `examples/` — Runnable hands-on exercises

> [← Back to main path README](../README.en.md)

Every stage in the learning roadmap has a "Hands-on Exercises" section that tells you *what* to do. This folder adds the **actual runnable starter code** — copy → install deps → `python starter.py` → see expected output.

## Directory layout

```
examples/
├── stage-3/                     # Tool Use & Agent intro
│   ├── 03-react-from-scratch/   # Exercise 3: ReAct from scratch
│   │   ├── starter.py           # Main program (~70 LOC runnable)
│   │   ├── test.py              # Self-check (pure assert, no pytest)
│   │   ├── README.md            # 200-400-word walkthrough (+.zh-Hans.md +.en.md)
│   │   └── requirements.txt     # Pinned deps
│   └── ...
├── stage-1/
└── ...
```

Short exercises (≤30 LOC) stay inline as `<details>` blocks in the stage doc — no folder. Longer ones (>30 LOC) get their own folder so stage docs don't get bloated by code blocks.

## How to run any example

```bash
cd examples/stage-3/03-react-from-scratch
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # Each example header lists the key it needs
python starter.py                     # Hits the real API to see output (~$0.001 in credits)
python test.py                        # Runs validation (mock-based, free)
```

## Design rules

| Dimension | Rule |
|---|---|
| Program length | starter ≤80 LOC, split if longer |
| Dependencies | stdlib + ≤2 pip packages, pinned versions |
| Tests | Plain `assert`, no pytest; reader runs `python test.py` to see ✅ |
| Comments | Chinese (zh-TW primary), English variable / function names |
| Self-check | Every starter.py ends with a `# === Self-check ===` block |
| Environment vars | Header comment must list required keys |
| Free-tier friendly | Use the cheapest model (claude-haiku / Ollama); note how to switch to Sonnet |
| **Windows encoding** | **Every .py must reconfigure stdout to UTF-8** (see below) |

### Windows cp950 encoding fix (mandatory in every starter.py / test.py)

Windows consoles default to cp950 (Big5) and can't print emoji or non-Big5 Chinese. Add this right after imports in every `.py`:

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

Without it, Windows readers running in PowerShell / cmd hit `UnicodeEncodeError: 'cp950' codec can't encode character '✅'`.

## Practicing without an API key — three paths

Every exercise ships in three forms:

### Path A (default) — Anthropic API
- Default `starter.py` / inline `<details>` uses Claude (`claude-haiku-4-5`, the cheapest tier)
- Requires `ANTHROPIC_API_KEY`; ~$0.001 per run
- Switch to Sonnet via `MODEL` env var or by editing one line
- Best for: Claude subscribers who want to follow the mainstream agent stack

### Path B (no API, local Ollama)
- Companion `starter_ollama.py` (folder) or a second inline `<details>` block (short exercises)
- Requires [Ollama](https://ollama.com); pull a model based on the stage:
  - **Stage 1 + 2** (plain chat / prompt eng): `ollama pull gemma3:4b` (3.3 GB; CPU-friendly)
  - **Stage 3+** (tool use / agent): `ollama pull qwen2.5:3b` (1.9 GB; reliable tool-use support)
- $0, offline, fine for privacy-sensitive data
- Best for: no Anthropic account, China mainland users, offline practice, exploring local-LLM limits

### Path C (verify logic, no API call)
- Every `test.py` uses `unittest.mock`; reader runs `python test.py` to validate logic
- Complements A / B — mock first, then real call

### Trade-offs

| Dimension | A Anthropic | B Ollama | C Mock |
|---|---|---|---|
| Cost per call | ~$0.001 | $0 | $0 |
| Requires | API key | Ollama install + ideally GPU | nothing |
| Answer quality | High | Medium (4B model) | canned, not representative |
| Speed | ~1-3 s/call | 5-30 s/call (no GPU) | <0.1 s |
| Offline | ❌ | ✅ | ✅ |
| Stage 3+ tool use | ✅ | ✅ (qwen2.5 / llama3.2) | ✅ |
| Best for | mainstream full path | privacy / China / no key | logic verification |

→ **Recommended combo**: C first (validate logic, no cost), then B (see real model behaviour locally), then A (high-quality answer if budget allows).

## Index by stage

| Stage | Exercises | Example location |
|---|---|---|
| 1 LLM basics | 6 | inline 4 + folder 2 (`examples/stage-1/`) |
| 2 Prompt engineering | 4 | all inline |
| **3 Tool use** | **6** | inline 1 + folder 5 (`examples/stage-3/`) |
| 4 Frameworks | 5 | all folder (`examples/stage-4/`) |
| 5 Claude Code ecosystem | 11 | inline 6 + folder 5 (`examples/stage-5/`) |
| 6 Memory/RAG | 5 | all folder (`examples/stage-6/`) |
| 7 Multi-agent | 5 | inline 1 + folder 4 (`examples/stage-7/`) |
| Track A1-A3 | 12 | all inline + 2 small folders (CLI-9 / CLI-10) |

→ T1 scope: **Stage 3 全 6 exercises only** (remaining stages roll out per plan tiers).

## Contributing / reporting issues

If something doesn't run, output doesn't match expectations, or you want to add a new example:
- File an issue tagged `examples`
- Or open a PR following the "Design rules" table above

## Why this split (instead of stuffing everything into stage docs)

1. **Stage docs stay readable** — roadmap readers don't always want code, they want concepts; long code blocks break that
2. **Examples evolve independently** — SDK bumps, model rename, example needs its own commit without polluting the roadmap's git log
3. **Readers can clone one example** — `svn export` or `git clone --filter=tree:0` grabs a single folder
4. **Future CI** — example failures shouldn't block mdbook deploy; this split lets CI run examples conditionally
