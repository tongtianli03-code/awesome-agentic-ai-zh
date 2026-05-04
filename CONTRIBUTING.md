# Contributing

Thanks for considering a contribution. This is a curated learning roadmap, not an exhaustive catalog. Quality > quantity.

## What We Accept

### High-value PRs
- **Adding a project** to a stage with reasoning for why it teaches that stage
- **Translating** a stage page to 繁中 (Traditional Chinese only — we are NOT zh-CN)
- **Flagging stale / unmaintained projects** (open an issue first)
- **Improving curation notes** on existing projects (clearer "what it teaches" explanations)
- **Reorganizing** within a stage if the current ordering doesn't match learning progression

### Lower priority (still welcome)
- Typo fixes
- Link fixes (verify with `curl -I` first)
- Stage description polish

### Not accepted
- Bulk additions of repos without curation reasoning
- Self-promotion without educational value
- Projects with no documentation
- Projects without clear license

## How to Add a Project

Each project in a stage page should follow this format:

```markdown
### [Project Name](url)

| Field | Value |
|---|---|
| Maintainer | who runs it |
| Language | Python / TS / etc. |
| Stars | ★ k |
| License | MIT / Apache 2 / ... |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 1-sentence summary of the core learning.

**Best for**: who should study this and why.

**Notes**: 1-3 sentence personal evaluation. What's strong, what's weak, what to skip.

**Run it**:
\`\`\`bash
# minimal install / first-run command
\`\`\`
```

## Curation Criteria

A project worth listing must have:

1. **Active maintenance**: commits within last 6 months OR explicit "stable, no longer maintained" notice
2. **Documented hello-world**: a reader should be able to run something within 30 minutes
3. **Clear license**: MIT, Apache 2, BSD, or comparable. Avoid no-license repos.
4. **Trustworthy maintainer**: well-known org, company, or individual with track record

## Bilingual Style

- **English is canonical**. Translation goes EN → 繁中.
- **繁中 (Traditional Chinese), not 簡中**. If you submit zh-CN we'll ask you to convert.
- **Natural translation**, not word-for-word. Technical terms can stay in English where natural ("使用 LangGraph 建 multi-agent 系統").
- Terminology consistency rules will live in `resources/style-guide.md` (Phase 2 work).

## Process

1. Open an issue first for new projects or bigger restructuring
2. PR with focused scope (one stage at a time)
3. Wait for review (typically 7 days)
4. Reviewer may ask for clarification on "why this teaches that stage"

## Anti-patterns to Avoid

- ❌ "leverage", "delve", "comprehensive", "robust" (LLM-tells)
- ❌ Hype framing ("revolutionary", "game-changing")
- ❌ Listing a project just because it's popular
- ❌ Long quotes from the project's own marketing copy

## License

By contributing, you agree your work is licensed under MIT.
