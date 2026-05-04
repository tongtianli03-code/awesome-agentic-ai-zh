# awesome-agentic-ai-zh

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Status](https://img.shields.io/badge/status-WIP%20%C2%B7%20Phase%201-orange)](#roadmap)

> A learning roadmap for agentic AI — from your first LLM API call to shipping multi-agent production systems. **Structured as a 7-stage path, not a flat list**, with curated projects, hello-world demos, and required reading at every stage.
>
> Written in English with curated Chinese-language entry points where they exist. A full Traditional Chinese (繁體中文) companion is Phase 2 work — see [ROADMAP](#roadmap).

---

## Why this exists

Most "awesome" lists for AI agents are flat catalogs — useful when you already know what you're looking for, useless when you're trying to figure out **what to learn next**.

This repo is a **structured learning roadmap**:

- 7 stages from prerequisites to production
- Hello-X projects you must run (not just read)
- Curated projects categorized by stage and audience
- Bilingual: English canonical + Traditional Chinese companion (繁中、非簡中)
- Honest time estimates (約 14-19 週走完主幹)

If you're a **Chinese-speaking learner** trying to break into agentic AI without getting lost in the noise — this is for you.

---

## The 7-Stage Learning Map

```
Stage 0  Foundations           (Python · CLI · git · API · JSON)         1-2 週
Stage 1  LLM Fundamentals      (tokens · API · model comparison)         1 週
Stage 2  Prompt Engineering    (system prompts · few-shot · CoT)         1-2 週
Stage 3  Tool Use & Hello Agent⭐  (function calling · ReAct · 5 hello-X) 2-3 週
Stage 4  Agent Frameworks      (LangGraph · AutoGen · CrewAI · ...)      2-3 週
Stage 5  Claude Code Ecosystem⭐⭐  (MCP · Skills · Plugins)              3-4 週
Stage 6  Memory · RAG · Advanced (vector DBs · long-term memory)         2 週
Stage 7  Multi-Agent · Production (orchestration · eval · deploy · SDK)  2-4 週
```

**Total main path: 14-19 weeks minimum, ~5-6 months realistic** at 5-8 hr/week part-time. The lower bound assumes you skip Stage 0 and don't get stuck on framework installs.

After main path, choose a specialized branch:
- 🔬 [For Researchers](branches/for-researcher.md)
- 💻 [For Developers](branches/for-developer.md)
- 🎓 [For Teachers](branches/for-teacher.md)
- 📊 [For Knowledge Workers](branches/for-knowledge-worker.md)

---

## Quick Reference: Stages At A Glance

| Stage | Title | Key Question | Detailed page |
|---|---|---|---|
| 0 | Foundations | Do I have the basics? | [stages/00-foundations.md](stages/00-foundations.md) |
| 1 | LLM Fundamentals | What is an LLM, really? | [stages/01-llm-basics.md](stages/01-llm-basics.md) |
| 2 | Prompt Engineering | How do I make LLMs behave? | [stages/02-prompt-engineering.md](stages/02-prompt-engineering.md) |
| 3 | Tool Use & Hello Agent ⭐ | How do I build my first agent? | [stages/03-tool-use-and-hello-agent.md](stages/03-tool-use-and-hello-agent.md) |
| 4 | Agent Frameworks | Which framework should I learn? | [stages/04-agent-frameworks.md](stages/04-agent-frameworks.md) |
| 5 | Claude Code Ecosystem ⭐⭐ | How do I extend Claude Code? | [stages/05-claude-code-ecosystem.md](stages/05-claude-code-ecosystem.md) |
| 6 | Memory · RAG · Advanced | How do agents remember? | [stages/06-memory-rag.md](stages/06-memory-rag.md) |
| 7 | Multi-Agent · Production | How do I ship to production? | [stages/07-multi-agent-production.md](stages/07-multi-agent-production.md) |

---

## How to Use This Repo

1. **Skim the 7 stages above** to find where you are.
2. **Click into the matching stage page** (links above). Each page has:
   - Learning goals (what you'll be able to do after)
   - Entry conditions (prerequisites)
   - Required reading (3-5 links)
   - Hello-X projects you must run
   - Curated case-study projects (with my notes on each)
   - Self-check questions before moving on
3. **Don't skip Stage 3 Hello Agent.** Reading without doing the 5 hello-X projects = wasted time.
4. **Stage 5 is where most readers spend the most time.** That's expected.

---

## Curation Criteria

Every project listed has been evaluated on:

- **Active maintenance** (commits within last 6 months)
- **Quality of documentation** (README clarity, hello-world reproducibility)
- **Educational value** (does it teach a generalizable lesson?)
- **License clarity** (avoid no-license repos)
- **Trustworthiness** (well-known maintainer or org)

Recommendation stars (⭐ to ⭐⭐⭐⭐⭐):
- ⭐⭐⭐⭐⭐ — Must-read for the stage
- ⭐⭐⭐⭐ — Highly recommended, study this
- ⭐⭐⭐ — Solid example, worth running
- ⭐⭐ — Useful reference, browse if interested
- ⭐ — Niche / advanced / for completeness

---

## Related Awesome Lists

This repo doesn't try to replace flat awesome lists. Use them when you already know what to look for:

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — broad Claude Code resources catalog (currently restructuring)
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — flat MCP server catalog
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — alternative MCP list
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills catalog
- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — official MCP reference servers
- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale Chinese tutorial (zh-CN)

---

## Note on self-citation

About a sixth of the curated projects (~12 entries) are repos maintained by this catalog's author (`WenyuChiou/...`). They're included as concrete pattern examples (e.g., multi-plugin marketplace pattern, single-skill pattern, multi-agent orchestration). Each one's notes section explains what *pattern* it teaches. If a non-self repo teaches the same pattern more cleanly, please open a PR — see CONTRIBUTING.md.

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Highest-value contributions:

- Add a project to a stage with explanation of why it teaches that stage
- Translate a stage page to 繁中
- Flag a project that's gone stale or unmaintained

---

## License

MIT. Maintained by [@WenyuChiou](https://github.com/WenyuChiou).
