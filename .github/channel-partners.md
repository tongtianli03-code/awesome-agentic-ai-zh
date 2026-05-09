# Channel Partners — Outreach Tracking

> Single source of truth for **awesome-agentic-ai-zh** channel-partner outreach.
> Per-target pitch templates live in `.github/outreach/<slug>.md`.
> Maintainer: @WenyuChiou (个人 maintainer; rule: 1-2 sends/day max).

---

## Status enum

| Status | Meaning |
|---|---|
| `not contacted` | Pitch drafted in `outreach/<slug>.md`, nothing sent yet |
| `contacted` | Outbound sent (issue/PR/email) — awaiting response |
| `replied-positive` | Partner replied; discussion in progress; no commit yet |
| `replied-negative` | Partner declined or asked to redirect |
| `merged-or-listed` | Cross-link landed (PR merged / featured / listed) |
| `ghosted` | No reply in ≥ 2 weeks; one ping sent then dropped |
| `cooldown` | Don't contact for ≥ 30 days (over-asked, restructuring, etc.) |

## Outreach matrix

| # | Target | Channel | Status | Date contacted | Outcome | Date confirmed | Notes |
|---|---|---|---|---|---|---|---|
| 1 | [Datawhale](outreach/datawhale.md) | GitHub issue | not contacted | — | — | — | Already cite Hello-Agents Extra05/08 in our cookbook |
| 2 | [liyupi/ai-guide](outreach/liyupi.md) | GitHub PR | not contacted | — | — | — | ★13k mainland resource hub |
| 3 | [HuggingFace 中文社群](outreach/huggingface-zh.md) | HF community/discuss | not contacted | — | — | — | English ecosystem hub w/ growing zh segment |
| 4 | [LangChain (kyrolabs/awesome-langchain)](outreach/langchain-ai.md) | GitHub PR | not contacted | — | — | — | Stage 4 covers LangChain; §11 lists Langchain-Chatchat |
| 5 | [hesreallyhim/awesome-claude-code](outreach/awesome-claude-code.md) | GitHub PR | not contacted | — | — | — | Already cited reciprocally in our README |
| 6 | [wong2/awesome-mcp-servers](outreach/awesome-mcp-servers.md) | GitHub PR | not contacted | — | — | — | Already cited in our README |
| 7 | [Zhipu BigModel community](outreach/zhipu.md) | dev community / 知乎 | not contacted | — | — | — | Inviting them to PR a Zhipu agent entry to §11 |
| 8 | [Moonshot Kimi](outreach/moonshot.md) | dev community / 知乎 | not contacted | — | — | — | Inviting them to PR a Kimi agent entry to §11 |

## Sequencing rule

**Pace: 1-2 outbound sends per day.** Reasoning:

- Replies need to be handled. If we batch-send all 8 in one day, we can't respond
  to early-positive replies before they cool.
- Multiple open conversations dilute attention; one-at-a-time keeps quality.
- If 5 replies land in week 1, that's a good problem; if 0 land, we don't burn
  all our cards before learning what's not working.

Suggested first-week order (low-risk → high-risk):

1. Day 1: [#5 awesome-claude-code](outreach/awesome-claude-code.md) — already
   reciprocally cited, lowest risk
2. Day 2: [#6 awesome-mcp-servers](outreach/awesome-mcp-servers.md) — same
3. Day 3: [#1 Datawhale](outreach/datawhale.md) — most strategic for zh-CN reach
4. Day 4: [#2 liyupi](outreach/liyupi.md) — high reach if accepted
5. Day 5: [#4 LangChain (kyrolabs)](outreach/langchain-ai.md)
6. Day 6: pause — review responses to date
7. Day 7+: [#3 HuggingFace](outreach/huggingface-zh.md), then [#7 Zhipu](outreach/zhipu.md), [#8 Moonshot](outreach/moonshot.md) only after digesting earlier feedback

## Update protocol

- Always update this matrix when contacted / received reply / closed.
- Use `git commit -m "outreach: status update for <target> (<status>)"` so the
  log is greppable.
- Dates: ISO format `YYYY-MM-DD`.
- Notes: 1-2 lines max — full context lives in the per-target `outreach/<slug>.md`.

## What NOT to do

- ❌ Bulk-send same template to all 8 in one day — looks like spam
- ❌ Lead with star count (★525) — small to ★1k+ partners; lead with scope
- ❌ Promise things we won't ship (e.g., "we'll add X if you cross-link")
- ❌ Ping after one reply — give 5+ business days
- ❌ Pitch via Discord DM unless explicitly invited (follow each project's
  preferred contact channel; Discord DM cold = annoying)
- ❌ Edit pitch templates without recording the change in the file's git history

## Success indicators

Order by signal strength (top = stronger):

1. **Cross-link landed** in their canonical README / docs / awesome-list
2. **Public mention** (their tweet / post / blog cites us)
3. **Reciprocal listing** in their tutorials/learning section
4. **Soft acknowledgment** — they replied positively but no concrete action

If by **2026-06-01** no signal #1-3 has landed across all 8: pause outreach,
audit the pitch tone (likely too founder-y, not enough technical specifics).
