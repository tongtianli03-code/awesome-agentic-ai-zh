# Outreach draft — Threads（共同維護者徵求）

> **Status**: draft, not submitted. Maintainer reviews + posts manually.
> Identity-bound channel — do not delegate posting to an agent.
> **Last updated**: 2026-05-29

## Why Threads

As of 2026-05-26, Threads (`l.threads.com`) was the **#2 external referrer** for this repo (1,138 views / 608 uniques over a 14-day window — second only to github.com; check current standing via GitHub Insights → Traffic). The zh-TW + zh-Hans developer audience is heavily on Threads, and the recommendation algorithm rewards substantive longer-form posts (vs X's 280-char broadcast model).

Audience: Chinese-speaking developers / researchers who already follow Wenyu's posts and would recognize the repo. Recruitment-shaped post fits the platform's "personal-update-from-someone-doing-real-work" tone better than X or LinkedIn.

## What we're recruiting for

Per `CONTRIBUTORS.md` § Stage maintainers + § Branch maintainers:

> 每個 stage 都歡迎社群志願者掛名長期維護者——有空時 review 一輪、處理該 stage 的 issue、把關 PR。沒有強制節奏。

**Lowest-friction model**:
- Open an Issue, say which stage/branch you want, mention what you can spare (no commitment to weekly/monthly cadence)
- No fixed review schedule
- Just review the PRs that come in for that stage and flag stale entries when you spot them
- Maintainer status is public credit (CONTRIBUTORS.md), useful for AI-domain CV building

**Specific gaps to call out** (per ROADMAP.md + CONTRIBUTORS.md notes):
- 📊 `for-knowledge-worker` branch — 目前最薄
- 🎓 `for-teacher` branch — 學術引用待深化
- Stage 0-2 共用基礎 — 沒有指定 maintainer
- Track A (A1-A3) — 沒有指定 maintainer
- Stage 6 (Memory · RAG) — 內容多、需要 RAG 領域人盯

---

## Post variants (pick one — Threads supports threading if you want longer)

### A — Honest "one-person-can't-do-this-forever" framing (Recommended)

```
repo 三個月跑到 ★1.7k+，但內容維護一個人扛——8 stages × 3 locale 翻譯、245 個 project 追星數、5 個 audience branch 深化、每月 frontier model 換名...

想找社群長期 stage / branch maintainer。**沒有固定 review 節奏**、能做幾次算幾次、有空時 review 一輪那個區塊的 PR / 處理該段 issue 就好。

最需要的兩個：
📊 for-knowledge-worker（目前最薄）
🎓 for-teacher（學術引用待深化）

自薦方式：開個 issue 寫你想 maintain 哪一塊就好。

github.com/WenyuChiou/awesome-agentic-ai-zh
```

### B — Identity-led（matches existing X / LinkedIn outreach tone）

```
我是 Lehigh PhD 學生，業餘維護 awesome-agentic-ai-zh——一份從 LLM 基礎走到 multi-agent 的三語（繁中 · 简中 · EN）學習地圖。三個月 ★1.7k+，社群動能起來了，但「翻譯 + catalog 維護 + 新內容 + 把關 PR」一個人扛不久。

想找長期 stage 或 branch maintainer。沒有固定節奏、有空 review 一輪、處理該區塊的 issue / PR 就好。

最缺：📊 for-knowledge-worker、🎓 for-teacher。

開 issue 自薦：
github.com/WenyuChiou/awesome-agentic-ai-zh
```

### C — Value-prop（for those who need to know "what's in it for me"）

```
找 awesome-agentic-ai-zh 共同維護者。

對你：
✓ CONTRIBUTORS.md 公開掛名（中文 AI 圈履歷加分）
✓ 接觸第一手 frontier model / agent 工具
✓ 沒有固定值班、沒有 review 期程要求

對 repo：
✓ 不用我一個人追 catalog 過時 entry
✓ 多一層 review 把關品質

工具都做好了（link rot + star refresh 每週 CI 自動跑）、你做 judgement call 就行。

最缺：📊 for-knowledge-worker、🎓 for-teacher、Stage 6 RAG。

開 issue 自薦：
github.com/WenyuChiou/awesome-agentic-ai-zh
```

---

## Optional second post (thread — for context after the recruitment post)

If post A or B generates interest, post this as a reply for those clicking through:

```
補細節給有興趣的人：

維護者做什麼：
- review 該 stage / branch 的 PR
- 處理對應 issue
- 看到 catalog entry 過時就開 issue 標出來
- 月度 / 季度節奏：不限，能做就做

不做什麼：
- 沒有固定 review 期程
- 不必每天值班
- 不要求最低 commit 量

機制都做好了：
- scripts/refresh-stars.py 每週 CI 自動刷新星數、揪過時 entry
- 4 個 CI gate 把關 PR 格式（anchor / mirror sync / lint / stage template）

完整 stage / branch list + 自薦範本：CONTRIBUTORS.md
```

---

## What NOT to say (per resources/style-guide.md §3)

- ❌ 「全世界最好的 / 業界最強」型 overclaim
- ❌ 「首選 / 唯一選擇」
- ❌ production-grade / world-class / cutting-edge 等
- ❌ 「找不到人幫忙」型負面 framing（reads desperate；用 A 的「一個人扛不久」中性 framing 替代）
- ❌ 比較對抗：「比 X repo 好」這類

## Pre-flight checks

- [ ] 確認 banner.zh-Hans.png 或 banner.png 已上傳到 Threads（圖片附加 > 純連結 card）
- [ ] 重新 verify ★1.7k 數字當下還對（`gh repo view WenyuChiou/awesome-agentic-ai-zh --json stargazerCount`）
- [ ] 用 GitHub Insights → Traffic 確認 Threads 仍是主要 referrer（萬一變動，調整「Why Threads」rationale）

## Tracking

Once posted:
- Add to `channel-partners.md`? (No — Threads isn't a 1-on-1 channel partner outreach; it's broadcast, different category)
- Watch for Issue self-nominations over next 7-14 days
- If 0 responses by 2026-06-15, audit post tone (likely needs to be MORE concrete on time investment) and try variant B
