# Stage 5 — Claude Code Ecosystem ⭐⭐

⏱ **Time estimate**: 3-4 weeks (~15-25 hours)

This stage has 4 sub-sections. **Do them in order** — each builds on the previous.

```
5.1  Claude Code Basics       3-5 days   (install, slash commands, CLAUDE.md)
5.2  MCP — Protocol Layer     5-7 days   (write your first MCP server)
5.3  Skills — Behavior Layer  5-7 days   (write your first SKILL.md)
5.4  Plugins & Marketplaces   5-7 days   (package and ship)
```

After this stage you will be able to extend Claude Code, write your own MCP server, ship a plugin marketplace, and contribute to the ecosystem.

---

## 5.1 — Claude Code Basics

### Learning Goals
- Install Claude Code on your OS
- Use slash commands (`/help`, `/compact`, `/clear`, `/plan`)
- Understand the `~/.claude/` directory structure
- Write a project-level `CLAUDE.md` that customizes behavior

### Required Reading
1. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — official install guide
2. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) — how to write project memory
3. [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-CN beginner guide

### Hello-X
- **Hello Claude Code** — install, run first session, ask Claude to read a file and summarize
- **Hello CLAUDE.md** — write a project CLAUDE.md, observe behavior change

### Curated Projects
- [**anthropics/claude-code**](https://github.com/anthropics/claude-code) — official repo (issues, releases)
- [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-CN walkthrough
- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — broader resource list (currently restructuring)

---

## 5.2 — MCP (Model Context Protocol) ⭐ Foundation

### Learning Goals
- Explain MCP's three abstractions (Tools, Resources, Prompts)
- Connect an existing MCP server to Claude Desktop or Claude Code
- Write a minimal MCP server in Python that exposes 1-2 tools
- Distinguish MCP server vs Tool Use vs Skills vs Plugins

### Required Reading
1. [**Anthropic — Introducing MCP**](https://www.anthropic.com/news/model-context-protocol) — original announcement, conceptual overview
2. [**MCP Specification**](https://spec.modelcontextprotocol.io/) — the actual protocol spec
3. [**Complete Guide to MCP in 2026**](https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11) — implementation walkthrough

### Hello-X
- **Hello MCP client** — install `modelcontextprotocol/servers/filesystem` and connect via Claude Desktop. Watch Claude read your files.
- **Hello MCP server** — write a Python MCP server that exposes one tool (e.g., "convert temperature"). Connect from Claude Code.
- **Hello MCP in production** — connect 2-3 MCP servers in one Claude session and watch them coordinate.

### Curated Projects

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐ Official

| Field | Value |
|---|---|
| Maintainer | Anthropic (official) |
| Language | TypeScript / Python |
| Stars | ★ 85k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: 20+ reference MCP servers (filesystem, git, github, sqlite, time, fetch, memory, sequential thinking). The canonical examples for writing your own.

**Best for**: Hello-1 and as reference. Read the source of `everything` server and `filesystem` server to understand the protocol.

**Run it**:
```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
# Or use Python servers:
pip install mcp-server-fetch
```

---

#### [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

| Field | Value |
|---|---|
| Maintainer | Anthropic (official) |
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Official Python SDK for writing MCP servers. Use this for Hello-2.

**Run it**:
```bash
pip install mcp
# Then follow https://github.com/modelcontextprotocol/python-sdk#quickstart
```

---

#### [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

| Field | Value |
|---|---|
| Maintainer | Anthropic (official) |
| Language | TypeScript |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: TypeScript equivalent of the Python SDK. Pick this if you prefer TS.

---

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) ⭐ Catalog

| Field | Value |
|---|---|
| Maintainer | wong2 |
| Format | Curated list |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Catalog of 150+ community MCP servers organized by category — search, code, cloud, communication, finance.

**Best for**: Discovering existing servers before writing your own. Browse this when you have a specific tool need.

**Notes**: Submission goes through their website (mcpservers.org).

---

#### [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

| Maintainer | punkpeye |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Alternative MCP server catalog with different organization (often more current).

**Best for**: Cross-reference with wong2's list. Different curators surface different projects.

---

#### [github/github-mcp-server](https://github.com/github/github-mcp-server)

| Field | Value |
|---|---|
| Maintainer | GitHub |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: How a real production MCP server is structured. Official GitHub-maintained.

**Best for**: Reading the source as a reference implementation for production-grade MCP server.

---

#### [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: A non-trivial MCP server that creates UI components. Shows how MCP can extend beyond simple data fetching.

**Best for**: Inspiration after Hello-2 — what creative MCP servers can do.

---

## 5.3 — Skills (Claude Code Behavior Layer)

### Learning Goals
- Anatomy of `SKILL.md` (YAML frontmatter + body)
- When skills auto-load (description matching)
- How to write a SKILL.md that solves your daily task
- Use of `references/`, `scripts/`, `evals/` subdirectories

### Required Reading
1. [**Anthropic — Claude Skills documentation**](https://docs.anthropic.com/en/docs/claude-code/skills)
2. **A few example SKILL.md files** from `anthropics/claude-code` or community marketplaces

### Hello-X
- **Hello SKILL.md** — write a 200-word skill solving one of your daily tasks
- **Hello SKILL with references** — add a `references/` markdown the skill can pull from
- **Hello SKILL eval** — add `evals/evals.json` with 3-5 self-tests

### Curated Projects

#### [anthropics/claude-code (official skills examples)](https://github.com/anthropics/claude-code)

| Recommendation | ⭐⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Official skill examples maintained by Anthropic. Reference for SKILL.md structure.

---

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)

| Field | Value |
|---|---|
| Maintainer | Wenyu Chiou |
| Stars | ★ 41+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 5-plugin marketplace, 14 research skills covering literature triage, paper memory building, NotebookLM verification, Zotero curation. **Multi-plugin marketplace pattern.**

**Best for**: Studying how a marketplace catalogs multiple plugins from different source repos.

**Run it**:
```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install research-workspace@ai-research-skills
```

---

#### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills)

| Field | Value |
|---|---|
| Maintainer | Wenyu Chiou |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 5 skills for multi-agent orchestration (task splitter, output reconciler, debate, shared memory, acceptance gate). **Single-plugin bundle pattern.**

**Best for**: Studying how a single-plugin marketplace bundles related skills.

---

#### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate)

| Field | Value |
|---|---|
| Stars | ★ 57+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Single-skill repo for delegating from Claude Code to Codex CLI. Wrapper script + result.json contract pattern.

**Best for**: Single-skill plugin pattern + sub-CLI delegation pattern.

---

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Curated catalog of Claude Skills across the community.

**Best for**: Discovering existing skills before writing your own.

---

#### [obra/superpowers](https://github.com/obra/superpowers)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: 20+ battle-tested skills (TDD, debugging, collaboration patterns) with `/brainstorm`, `/write-plan`, `/execute-plan` commands and skills-search tool.

**Best for**: Power-user setup. Read SKILL.md sources to learn advanced patterns.

---

#### [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: 1000+ agent skills compatible with Claude Code, Codex, Gemini CLI, Cursor. Cross-tool perspective.

**Best for**: After you understand SKILL.md, browse for ideas.

---

#### [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: 232+ Claude Code skills across engineering, marketing, product, compliance.

**Best for**: Domain-specific skill examples.

---

## 5.4 — Plugins & Marketplaces

### Learning Goals
- `plugin.json` schema (name, version, skills array, configuration)
- `marketplace.json` schema (plugins array, source, metadata)
- `claude plugin marketplace add` workflow
- Distinguish single-plugin bundle vs multi-plugin marketplace
- Publish your own marketplace

### Required Reading
1. [**Anthropic — Plugins documentation**](https://docs.anthropic.com/en/docs/claude-code/plugins)
2. **Read the `plugin.json` and `marketplace.json` of 2-3 marketplaces below**

### Hello-X
- **Hello plugin install** — install one of the marketplaces below, see it load
- **Hello plugin.json** — package the SKILL.md you wrote in 5.3 into a plugin
- **Hello marketplace publish** — push to GitHub, install via `claude plugin marketplace add`

### Curated Projects

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) (multi-plugin marketplace pattern)

Already cited in 5.3. Read its `.claude-plugin/marketplace.json` to study the multi-plugin pattern (5 plugins across 5 source repos).

---

#### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) (single-plugin bundle pattern)

Read its `.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` to study the single-plugin bundle pattern.

---

#### [obra/superpowers](https://github.com/obra/superpowers) (production marketplace)

A larger, battle-tested marketplace. Read its packaging structure.

---

#### [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: One of the largest community catalogs of Claude Code agents, skills, hooks, and templates. Wide breadth across many use cases.

**Best for**: After Hello-3, browse for ecosystem awareness.

---

## ✅ Self-Check Before Stage 6

Can you:
- [ ] Install Claude Code and use 5 different slash commands
- [ ] Connect 2 MCP servers in one Claude session
- [ ] Write your own MCP server in Python that exposes 1 working tool
- [ ] Write a `SKILL.md` that auto-loads on a specific trigger phrase
- [ ] Package skills into a plugin and publish via `marketplace.json`
- [ ] Distinguish MCP / Skills / Plugins / SDK by their roles

If yes → proceed to [Stage 6 — Memory & RAG](06-memory-rag.md).

## 💡 Bonus: After this Stage

- Submit a PR to `anthropics/claude-code` cookbook (small fix, doc update)
- Submit your own plugin to a community marketplace
- Write a blog post comparing your hello-MCP server with one from the official `modelcontextprotocol/servers` collection
