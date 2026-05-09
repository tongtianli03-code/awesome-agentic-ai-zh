# Outreach: wong2/awesome-mcp-servers + punkpeye/awesome-mcp-servers

> **Status**: not contacted · **Channel**: GitHub PR
> **Primary lang**: en
> **Last updated**: 2026-05-09
> **Repos**:
> - https://github.com/wong2/awesome-mcp-servers
> - https://github.com/punkpeye/awesome-mcp-servers (alternative — pick whichever has more activity)

**Why this target**: We already cite both in our README's "Related projects" section (mutual benefit baked in). They're the canonical MCP server catalogs. Our angle: we're the **how-to-learn-MCP** complement.

**Pitch angle**: Their readers want to use MCP servers; we teach them how MCP works first (Stage 5.2 of our roadmap). Our §5.2 walkthrough → their flat catalog is a natural funnel.

**Their counter-value**: Reciprocal cross-link; better onboarding for their readers.

---

## Variant 1 — Social post (X, ~280 chars)

```
Browsing the awesome-mcp-servers catalog and unsure where to start? Stage 5.2
of awesome-agentic-ai-zh walks through MCP from concept to first install in
~2 hours, then hands you off to wong2/awesome-mcp-servers for the actual
catalog browsing.

★525 week 1 · MIT
🔗 github.com/WenyuChiou/awesome-agentic-ai-zh
```

## Variant 2 — GitHub PR (200-300 words)

**PR title**: Add awesome-agentic-ai-zh to Learning Resources / Tutorials section

**Diff** (location depends on which list you target — assume a tutorials section):

```diff
+ - [`WenyuChiou/awesome-agentic-ai-zh`](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
+   — Trilingual (zh-TW · zh-CN · en) 7-stage learning roadmap. Stage 5.2 is a
+   dedicated walkthrough of MCP (concept → first install → writing your own
+   server), with prerequisites and time estimates. Catalog includes 62
+   integrations grouped by use case.
```

**PR description**:

```markdown
Hi @wong2 (or @punkpeye),

awesome-mcp-servers is already in our `Related projects` section
([README.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/README.md))
— we cite you as a primary catalog for MCP server discovery.

Our repo is the **structured learning complement**:

- Stage 5.2 of our roadmap is a **dedicated MCP walkthrough**: concept →
  first install → writing your own server, with hands-on exercises and time
  estimates
- After Stage 5.2, readers are sent to your catalog to find specific servers
  for their stack
- Trilingual (zh-TW / zh-CN / en), MIT, ★525 week 1

If you have a tutorials / learning-resources section, this fits there. If
your list is server-only by policy, totally understand — just close the PR.

Reciprocal cross-link is the goal: your readers get a learning order; ours
get the canonical server catalog.

Stats: 6,800 views / 3,200 unique / 408 unique cloners in week 1. CI runs
banned-word audit + link rot check on every PR.

— Wenyu (PhD candidate, individual maintainer)
```

## Variant 3 — DM / Twitter (150 words)

```
@wong2 — your awesome-mcp-servers list is already in our README's "Related
projects". I run awesome-agentic-ai-zh: a trilingual 7-stage learning roadmap
with Stage 5.2 dedicated to MCP (walkthrough → install → writing your own
server, with cost/time estimates).

After Stage 5.2 our readers are sent to your catalog. Reciprocal link in your
Learning Resources / Tutorials section would be natural — opened a PR
(<link>). Close it if it doesn't fit your list's policy.

— Wenyu
```

---

## Notes

- **Pick one fork** — both are popular. Check recent commit activity and pick
  whichever maintainer is more active (gh api repos/<owner>/<repo>)
- If the list is policy-strict (servers only, no tutorials), don't push —
  thank, close, move on
- If they accept, mirror cross-cite by ensuring our README still references
  them (already done as of 2026-05-09)
