# Mirror Sync TODO — 2026-05 Session Drift

**Date**: 2026-05-13
**Trigger session**: Stage 6 refactor + Stage 7 audit + **Stage 8 creation** + 2026 freshness sweep + GitHub Actions setup
**Strategy**: Path B (zh-TW canonical, mirrors trail). 本 session strategic minimum sync 完成、剩下 deferred 給後續 session（建議用 Gemini delegation per global `CLAUDE.md`、CJK 翻譯主場）。

---

## ✅ Done in this session

| Sync item | en | zh-Hans | Notes |
|---|---|---|---|
| **Anchor cleanup ⭐ + strict mode** | ✅ 37 broken anchors fixed (Codex delegation, commit 706d257) | ✅ same | `python scripts/check-anchors.py --strict` now exits 0. `anchor-validator.yml` flipped from warn-only to `--strict` mode |
| **Stage 6 FULL catch-up** ⭐ | ✅ 318→576 lines (Gemini, commit 06181b6) | ✅ 321→576 lines | All new positioning + Memory/Reasoning/RAG advanced sections + 2024-2026 entries translated |
| **Stage 7 FULL restructure** ⭐ | ✅ 363→298 lines (Gemini, commit 75df682) | ✅ 364→298 lines | 22 H4 blocks consolidated, 8-component harness, Benchmark Landscape, multi-agent skepticism — all synced |
| **Stage 8 FULL translation** ⭐ | ✅ 55→545 lines (Gemini, commit 3f4ea8f) | ✅ same | Replaced stubs with full translations, H2 parity 16/16 |
| **Stage 1 pricing sync** ⭐ | ✅ Claude pricing 4.5 → 4.6/4.7 trio (Codex, commit fe989bd) | ✅ same | Pricing dict + Q1→Q2 comment + expected output + print line + URL all updated |
| README structural | ✅ Stage 8 row + 8-stages + time + Part 5 + dual hub callout (commits d3c0119 / cbf4d12 / 21d9c28) | ✅ same | |
| Glossary 8 Agent Interfaces | ✅ 6 new entries (commits cbf4d12 / 21d9c28) | ✅ same | Renumbered from 7→8 to avoid duplicate H2 anchor |

---

## 🚧 Deferred — future session priorities

### ~~🔴 HIGH — Stage 8 full translation~~ ✅ COMPLETED (commit 3f4ea8f, Gemini)
### ~~🔴 HIGH — Stage 7 refactor sync~~ ✅ COMPLETED (commit 75df682, Gemini)
### ~~🔴 HIGH — Stage 6 catch-up~~ ✅ COMPLETED (commit 06181b6, Gemini)
### ~~🔴 HIGH — Stage 5 catch-up~~ ✅ COMPLETED (commit 8b39c75, Gemini)
### ~~🟡 MEDIUM — Stage 4 restructure sync~~ ✅ COMPLETED (commit 488526a, Gemini)
### ~~🟡 MEDIUM — Stage 3 restructure sync~~ ✅ COMPLETED (commit 8ae18e6, Gemini)
### ~~🟢 LOW — Anchor cleanup + strict mode~~ ✅ COMPLETED (commit 706d257, Codex)
### ~~🟡 MEDIUM — Stage 1 pricing sync~~ ✅ COMPLETED (commit fe989bd, Codex)

### ~~🟢 LOW — Stage 1 / Stage 2 mirror "extra content" trim~~ ✅ RESOLVED 2026-05-25

**Root cause (re-investigated 2026-05-25)**: drift was concentrated entirely in `## 🎯 Curated Projects` H2 — Stage 1 mirrors had +265 lines, Stage 2 mirrors had +93 lines, but **all other H2 sections matched canonical**. Not "extra content" — **stale schema**. Mirrors held the OLD H3-card-per-project format (one ### per project, sub-table for Stars/License, bullet lists), canonical migrated to the new compact-table format during the 2026-05-13 Stage 3-8 restructure but Stage 1/2 missed the pass.

Same project list (17 in Stage 1, 9 in Stage 2) verified by link-diff. Only difference: one stale `anthropic-cookbook` URL (renamed to `claude-cookbooks`) + outdated star counts (★ 60k+ instead of ★ 74k+ for dair-ai).

**Fix applied**: regenerated the 4 mirrors' 🎯 Projects sections from canonical (en hand-translated, zh-Hans via `opencc tw2s` + `zh-hans-localize` vocab + 影片→视频 / 搜寻→搜索 verified against repo convention). Also normalized Stage 1 .zh-Hans H2 titles (📌 / 🚪 / 📚 / 🛠 / ✅ + canonical wording) which had drifted to non-emoji forms.

### 🟢 LOW — Stage 1/2 mirror reverse drift (mirrors SMALLER than canonical, deferred)

After the 🎯 Projects fix, Stage 1/2 mirrors are now **slightly smaller** than canonical:

| Stage | zh-TW | en | zh-Hans | net drift (after 2026-05-25 fix) |
|---|---|---|---|---|
| 01 | 533 | 477 (-56) | 476 (-57) | mirrors lost ~5 lines 必修閱讀 + ~49 lines 動手練習 expansion that canonical gained later |
| 02 | 475 | 455 (-20) | 468 (-7) | small expansions in canonical 動手練習 not yet mirrored |

This drift is in the *reverse* direction from the 2026-05-13 finding — canonical has slightly more exercise / required-reading content than mirrors. Not blocking; gates green; deferred to a separate session.

### Final mirror parity status (2026-05-25 end of session)

| Stage | zh-TW | en | zh-Hans | Status |
|---|---|---|---|---|
| 01 | 533 | 477 (-56) | 476 (-57) | ⚠ reverse drift (canonical +content in 必修閱讀 / 動手練習) |
| 02 | 475 | 455 (-20) | 468 (-7) | ⚠ reverse drift (small canonical expansions in 動手練習) |
| 03 | 500 | 499 (-1) | 500 (0) | ✅ parity |
| 04 | 227 | 227 (0) | 227 (0) | ✅ parity |
| 05 | 570 | 570 (0) | 570 (0) | ✅ parity |
| 06 | 576 | 576 (0) | 576 (0) | ✅ parity |
| 07 | 298 | 298 (0) | 298 (0) | ✅ parity |
| 08 | 546 | 545 (-1) | 545 (-1) | ✅ parity |

**Forward-schema drift eliminated across all 8 stages.** Remaining drift is reverse-direction in Stage 1/2 only (-7 to -57 lines per file).

### 🔴 HIGH — Stage 6 catch-up

zh-TW grew from ~320 lines to **576 lines** this session. Mirror still at 318/321 lines. Major net new content not in mirrors:

- Context Engineering 是什麼（先定位）+ 3-row lineage table + 4-row 概念對照表 (Memory / Embedding / Vector DB / RAG)
- RAG vs Long Context vs Fine-tuning trade-off table
- 進階 Memory — CoALA framework + Generative Agents 三分數 + 2024-2026 縱覽（including A-MEM / HippoRAG 2 / ScrapMem / Memory Security survey）
- 進階 Reasoning — Path 1 prompt-based table + Path 2 trained-in table (含 R2 / V4 / GPT-5.5 / Opus 4.7 / Gemini 3.1)
- 進階 RAG 技巧 — GraphRAG / Contextual Retrieval / Hybrid Search & Reranking deep dives + 縱覽 (17 techniques)
- 常用 Memory / RAG 工具推薦 + 精選 Projects 單一表

**Estimated translation**: ~260 lines of new content × 2 locales.

### 🔴 HIGH — Stage 7 refactor sync

zh-TW REFACTORED from 462 → 274 lines (net) but the structure is completely different:
- 22 H4 detail blocks consolidated → single Projects table with 適合誰 column
- New Multi-Agent · Production 是什麼（先定位）opening with discipline lineage
- New 但你真的需要 multi-agent 嗎? (Anthropic + Cognition essays)
- Harness 7→**8** components (added Cost/Latency Optimization)
- New Agent Benchmark Landscape + ⚠ Berkeley reward-hacking warning
- New 常用工具推薦
- Title softened: "Multi-Agent · Production" → "Multi-Agent · 進階應用"

Mirror still has the OLD structure (22 H4 detail blocks, 7 components, "Production" title).

**Estimated translation**: full restructure ~300 lines × 2 locales.

### 🟡 MEDIUM — Stage 5 forward ref + Stage 4 enhancement + Stage 8 mention

- Stage 4 什麼時候真的需要 multi-agent gained Anthropic + Cognition essays table
- Stage 5 自我檢查 gained Stage 8 forward ref
- Stage 5.6 H2/H3 sub-stage updates for 6→8 harness components

**Estimated translation**: ~30 lines diff × 2 locales.

### 🟡 MEDIUM — Stage 1 + Stage 2 small updates

- ~~Stage 1: Claude pricing exercise updated to 4.5/4.6/4.7 trio + 必修閱讀 URL updated~~ ✅ COMPLETED (commit fe989bd, Codex delegation)
- Stage 2 / Stage 3: small wording updates for 2026 freshness (still deferred — minor)

**Remaining estimated translation**: ~5 lines diff × 2 locales (Stage 2/3 only).

### 🟢 LOW — tracks/cli/A3-cli-production.md anchor fixes

3 dead-anchor link target updates after Stage 7 Observability + Evaluation Frameworks sections were consolidated into 常用工具推薦 + Benchmark Landscape.

**Estimated translation**: 3 line diffs × 2 locales.

### 🟢 LOW — Anchor cleanup + enable `--strict` in anchor-validator

`anchor-validator.yml` currently runs in **warn-only** mode. Local run found ~38 legacy broken anchors (Stage 5 sub-headings gained ⭐ extras during this session's template refactor, but cross-references in glossary / cookbook / examples / tracks didn't all sync to the new slugs).

**Action**: one-time anchor cleanup PR to fix the legacy ~38 broken anchors, then flip workflow line from `python scripts/check-anchors.py` to `python scripts/check-anchors.py --strict` to enforce on future PRs. Without this tracker entry the upgrade would silently linger in the workflow YAML's TODO comment.

**Estimated effort**: ~30-50 line diffs across ~10 files, mostly one-line anchor URL fixes.

---

## 📋 Suggested delegation prompt template

When using Gemini (per CJK translation routing in global `CLAUDE.md`):

```
Task: translate Stage 8 (and/or other mirror sync) from zh-TW canonical to en + zh-Hans.

Source files (zh-TW canonical):
- stages/08-agent-interfaces.md (~547 lines)
- stages/06-memory-rag.md (the new 進階 sections)
- stages/07-multi-agent-production.md (full restructure)
- README.md (already structurally synced this session — diff against current mirrors)
- resources/glossary.md 7 Agent Interfaces (already synced this session)

Style:
- Match existing mirror style (see stages/01-llm-basics.en.md / stages/03-tool-use-and-hello-agent.en.md for tone)
- zh-Hans uses 简体中文 (用户 not 使用者; 软件 not 軟體; 网络 not 網路)
- zh-TW canonical uses 繁體中文 (使用者; 軟體; 網路)
- en mirror: technical but casual, matches Anthropic / OpenAI docs tone
- KEEP all cross-stage anchor links valid (use anchor-validator.yml CI to verify)

Constraints:
- Don't translate model names (Opus 4.7 stays Opus 4.7 in all locales)
- Don't translate framework names (browser-use stays browser-use)
- 2026 dates stay literal (2026-05, April 2026)
- Code blocks stay as-is

Output: split into separate commits per file/section for reviewability.
```

---

## 🔁 Automation status

`mirror-sync-reminder.yml` workflow (shipped this session, commit `5cd2dec`)
will now flag any PR that modifies zh-TW canonical without syncing mirrors —
preventing future drift accumulation. The existing drift documented here
is the **legacy** to clear; new drift should be caught at PR time.

---

## 📍 References

- Mirror sync workflow: [`.github/workflows/mirror-sync-reminder.yml`](.github/workflows/mirror-sync-reminder.yml)
- Mirror sync script: [`scripts/check-mirror-sync.py`](scripts/check-mirror-sync.py)
- Anchor validator (helps after translation): [`scripts/check-anchors.py`](scripts/check-anchors.py)
- Freshness check (helps verify 2026 model refs): [`scripts/check-2026-freshness.py`](scripts/check-2026-freshness.py)
- This session's commit range: `dc8b5be..b515e3f` (zh-TW work) + `a3c7406..d8d299d` (freshness + CI)
