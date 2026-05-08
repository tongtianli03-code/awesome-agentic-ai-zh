# Cookbook — 把概念变成可执行的 recipe

> [繁體中文](./cookbook.md) | **简体中文** | [English](./cookbook.en.md)

> Stage 5（Claude Code 生态）跟 [`mcp-skills-catalog.md`](mcp-skills-catalog.zh-CN.md) 讲“概念”跟“有哪些工具”。这份 cookbook 补中间缺的：“**怎么动手做出来**”。每个 recipe 是一份 step-by-step + sample code + 常见 pitfall，~30-50 分钟做完一个。
>
> 不是 reference 也不是 tutorial——是 recipe，挑你需要的那道煮就好。

---

## 📋 目录

1. [写你的第一个 Skill（SKILL.md anatomy）](#1-写你的第一个-skill)
2. [写你的第一个 MCP server（Python SDK）](#2-写你的第一个-mcp-server)
3. [Word / Excel / PowerPoint workflow](#3-office-docs-workflow)
4. [NotebookLM workflow](#4-notebooklm-workflow)
5. [Zotero workflow](#5-zotero-workflow)

---

## 1. 写你的第一个 Skill

> Skill = 一个文件夹含 `SKILL.md`，Claude Code 启动时自动 discover、按情境自动加载。最小 viable 版本 50 行就能跑。
>
> 📚 **这份是“30 分钟跑出第一个”实作版。想看“Skill 怎么写得好”深度讨论** → [Hello-Agents Extra08：如何写出好的 Skill](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md)（中文最完整的 Skill 最佳实践，讨论 description 写法、references / scripts 设计等）。两份互补：先用本 recipe 跑出第一个，再读那份 polish 写法。

### 为什么

写 Skill 跟“在 prompt 里加几段 instruction”差别在于：
- Skill 是 **per-domain** 的，不会污染所有 conversation
- 可以打包跨 project / team 共用
- Claude 自己决定何时加载（看 description match 不 match）

### 步骤

#### Step 1：创建 skill 文件夹

两个位置可以放（看你要 user 级还是 project 级）：

```bash
# user 级（所有 project 共用）
mkdir -p ~/.claude/skills/my-first-skill
cd ~/.claude/skills/my-first-skill

# 或 project 级（只在这个 repo 触发）
mkdir -p .claude/skills/my-first-skill
cd .claude/skills/my-first-skill
```

#### Step 2：写 `SKILL.md`

最小可 work 的模板：

```markdown
---
name: my-first-skill
description: When the user asks for [SPECIFIC SITUATION], use this skill to [WHAT IT DOES]. Examples include [2-3 trigger phrases]. Do NOT use for [WHAT IT'S NOT FOR].
---

# My First Skill

You are now in the [domain] context.

## When the user asks X, do these steps:

1. First, [action A]
2. Then, [action B]
3. Verify with [check]

## Don't do:

- [anti-pattern 1]
- [anti-pattern 2]

## Reference

- (optional) link to a doc / paper / API spec
```

具体例子：“整理 Python 代码的 import 顺序”

```markdown
---
name: python-import-organizer
description: When the user pastes Python code or asks to clean up imports / format code / sort imports, organize the imports following PEP 8 + isort order: stdlib first, then third-party, then local. Do NOT use for non-Python code.
---

# Python Import Organizer

When the user wants Python imports cleaned up:

1. Group imports into 3 sections: stdlib / third-party / local
2. Within each group, sort alphabetically
3. Add a blank line between groups
4. Remove unused imports (only if user explicitly asks; otherwise just sort)

## Don't:
- Don't change function code, only the import block
- Don't auto-remove imports without asking
```

#### Step 3：测试

```bash
# 重启 Claude Code（让它重新 discover skills）
# 在 conversation 里丢一个触发句
# e.g.「帮我整理一下这段 Python 的 imports」
# 观察 Claude 有没有按照 SKILL.md 的步骤做
```

#### Step 4（进阶）：加 evals

在 skill folder 内加 `evals/evals.json`：

```json
{
  "evals": [
    {
      "input": "整理一下这段 Python 的 imports: import os
import requests
from mypackage import foo",
      "expected_behavior": ["按 stdlib / third-party / local 分组", "alphabetical 排序"]
    }
  ]
}
```

之后可以用 promptfoo 之类工具 batch 跑。

### 常见 pitfall

| 症状 | 原因 | 解法 |
|---|---|---|
| Claude 从不触发我的 skill | description 写得太笼统，匹配不到 user query | description 加 2-3 个具体 trigger phrase（"when the user asks X / Y / Z"） |
| 触发了但行为不对 | SKILL.md 步骤太抽象 | 改成 numbered list、每步明确动作 |
| 触发了不该触发 | description 太宽，匹配到不相关 query | 加 "Do NOT use for X" 收敛 |

### 进一步

- 看 [Stage 5.3](../stages/05-claude-code-ecosystem.zh-CN.md#53--skillsclaude-code-的行为层) 的 Skill anatomy 详解
- 看 [`anthropics/skills`](https://github.com/anthropics/skills) 官方 skill 模板（docx / xlsx / pptx 等）的写法
- 多个 skill 打包成 plugin → [Stage 5.4](../stages/05-claude-code-ecosystem.zh-CN.md#54--plugins-与-marketplaces)

---

## 2. 写你的第一个 MCP server

> MCP server = 一个独立 process，跑起来提供 tool / resource / prompt 给 LLM host（Claude Desktop / Claude Code）。最小可 run 版 < 50 行 Python。

### 为什么

- Skill 是给 Claude 的“角色 + 规则”；MCP 是给 Claude 的“**外部 function**”
- Skill 不能读档、不能呼叫 API；MCP 可以（任何 tool 你写得出来）
- Skill 只在 Claude Code 跑；MCP 任何 LLM host（包括 Cursor、自写 agent）都能接

### 步骤

#### Step 1：安装官方 SDK

```bash
pip install mcp
```

#### Step 2：写 `server.py`

最小模板——一个会回 echo 的 tool：

```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("hello-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="echo",
            description="Echo the input text back to the user.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back",
                    }
                },
                "required": ["text"],
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "echo":
        return [TextContent(type="text", text=f"Echo: {arguments['text']}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

#### Step 3：在 Claude Desktop / Code 设置

**Claude Desktop**：编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "python",
      "args": ["/绝对路径/到/server.py"]
    }
  }
}
```

**Claude Code**：用 `claude mcp add` 指令：

```bash
claude mcp add hello-mcp python /绝对路径/到/server.py
```

#### Step 4：重启 Claude Desktop / Code、测试

```
你问：echo "hello world" 给我
Claude 回（会显示 tool call icon）：Echo: hello world
```

### 常见 pitfall

| 症状 | 原因 | 解法 |
|---|---|---|
| Claude Desktop 没看到 tool | server.py 启动失败 | 终端直接 `python server.py` 跑、看 stderr 哪里爆 |
| tool 列出但 call 失败 | inputSchema 格式错（required 漏写、type 写错） | 看 [`schema-design-cheatsheet.md`](schema-design-cheatsheet.zh-CN.md) |
| Claude 不主动叫 tool | description 太笼统 | description 改成“When the user asks X, use this tool”式的具体 trigger |
| stdio 跟 SSE 哪个用？ | local desktop integration 用 stdio；remote / web 用 SSE | 第一个 server 一律用 stdio |

### 进一步

- 看 [Stage 5.2](../stages/05-claude-code-ecosystem.zh-CN.md#52--mcpmodel-context-protocol-基础) 的 MCP 完整介绍
- 看 [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) 官方示例（filesystem、github、sqlite、time 等）
- 写 production server 看 [Stage 5.2“练习：MCP in production”](../stages/05-claude-code-ecosystem.zh-CN.md#52--mcpmodel-context-protocol-基础) 跟 [`anthropics/claude-code`](https://github.com/anthropics/claude-code) 的 `~/.claude/skills/`

---

## 3. Office Docs Workflow

> 用 Claude 读写 Word / Excel / PowerPoint / PDF 不用装额外 tool——[`anthropics/skills`](https://github.com/anthropics/skills) 官方 repo 已经内建好。

### 为什么

最常见场景：
- 把 Markdown / 大纲 → 自动生成 Word / PPT
- 读一堆 PDF / Excel → 整理摘要 / 提取数字
- 改别人传来的 docx → 加 track changes、或重排格式
- 把表格 cross-reference 写成报告

不需要自己 parse XML、不需要找 python-docx / openpyxl 教学——anthropics/skills 已经包好。

### 步骤

#### Step 1：安装 skills

最简单：clone Anthropic 官方 skills repo 到 user-level skill 目录：

```bash
# user 级（所有 project 用）
git clone https://github.com/anthropics/skills.git ~/.claude/skills/anthropic-skills
```

或者用 `claude plugin install`（如果有打包成 plugin）。

#### Step 2：重启 Claude Code

- skills/docx/ → docx 读写
- skills/xlsx/ → Excel 读写
- skills/pptx/ → PowerPoint 读写
- skills/pdf/ → PDF 读

Claude 会根据 user query 自动加载合适的 skill。

#### Step 3：实用 prompt 模板

**从大纲生 PPT**：
```
读我写的 outline.md，照这个结构生一份 PPT：
- 封面 1 页
- 每个 H2 一页，bullet points 从 H3 内容浓縮
- 结语 1 页

存成 ./output/presentation.pptx
```

**读 Excel 整理数字**：
```
读 ./data/sales-2023.xlsx 第一张 sheet，把每个 region 的 Q4 总额算出来，
写进 ./output/q4-summary.md（用 markdown table 格式）。
```

**改 docx**：
```
读 ./doc/draft.docx，把繁中词汇转成简中（譬如“软体”→“软件”），
存成 ./doc/draft.zh-CN.docx，保留原本的 track changes。
```

**读 PDF 提取信息**：
```
读 ./papers/research.pdf，把 abstract、main contributions、limitations
分别写进三个 markdown section，存到 ./notes/research-summary.md。
```

### 常见 pitfall

| 症状 | 原因 | 解法 |
|---|---|---|
| skill 没被触发 | repo 路径放错 | 确认 SKILL.md 在 `~/.claude/skills/anthropic-skills/skills/docx/SKILL.md` 这种层级 |
| pptx 生出来样式丑 | 没给设计参考 | prompt 加“参考 ./template.pptx 的样式” |
| 大 PDF 读不完 | context 爆 | 改用 [`SylphxAI/pdf-reader-mcp`](https://github.com/SylphxAI/pdf-reader-mcp)（5-10× 快） |
| Excel 公式被吃掉 | docx skill 不处理 formulas | 开档前 prompt 明说“保留 formula 不要 hard-code” |

### 进一步

- catalog §2 [`mcp-skills-catalog.md` §2 办公文件](mcp-skills-catalog.zh-CN.md#2-办公文件word--excel--powerpoint--pdf)：补强版 office skill / Excel / PPT 专用 MCP
- 中文圈 office workflow：[`leemysw/feishu-docx`](https://github.com/leemysw/feishu-docx) 飞书 / Lark docs ↔ Markdown

---

## 4. NotebookLM Workflow

> NotebookLM 是 Google 的 RAG-on-your-docs 工具。**Claude Code 没有官方 NotebookLM 集成**，但社群有 2 个成熟方案。

### 为什么

NotebookLM 强的地方：
- 上传 50 份 PDF 自动建索引
- Q&A 带 citation（每个答案都标出来自哪份文件第几页）
- 生成 summary / mind map / podcast-style audio overview

弱点：要在 NotebookLM 网页里用，跟你的其他 workflow（Claude Code、Obsidian、Zotero）断开。

两个方案桥接：
1. **PleasePrompto/notebooklm-skill**（Skill，browser automation）
2. **teng-lin/notebooklm-py**（Python API + CLI）

### 两个方案怎么选

| 场景 | 选哪个 | 为什么 |
|---|---|---|
| 偶尔从 Claude Code 查一下 NotebookLM | `PleasePrompto/notebooklm-skill` | Claude Code 内 prompt 一句话就跑、setup 简单 |
| 批次操作（建 100 个 notebook、批次导入文件） | `teng-lin/notebooklm-py` | Python API，可程式化跑 |
| 不想 Google 政策变动就坏 | （等 Google 出官方 API） | 两个都是 unofficial、会有风险 |

### 方案 A：PleasePrompto/notebooklm-skill

#### Step 1：clone 到 skills 目录

```bash
git clone https://github.com/PleasePrompto/notebooklm-skill ~/.claude/skills/notebooklm
```

#### Step 2：第一次跑会要 Google login（浏览器自动化）

照 repo README 设置 OAuth / 登录 cookie。

#### Step 3：实用 prompt

```
查我 NotebookLM 内“LLM Agents 2024”这个 notebook，
找出所有提到 "tool use" 的段落，整理成一份比较表，
带上每个来源文件名跟页数。
```

### 方案 B：teng-lin/notebooklm-py

```bash
pip install notebooklm-py
```

示例：

```python
from notebooklm import NotebookLM
nlm = NotebookLM()  # OAuth 流程

# 建一个 notebook
nb = nlm.create_notebook("My Research")

# 批次导入 PDF
for pdf in glob.glob("papers/*.pdf"):
    nb.add_source(pdf)

# Q&A
answer = nb.query("What are the main contributions?")
print(answer.text)
print(answer.citations)
```

### 常见 pitfall

| 症状 | 原因 | 解法 |
|---|---|---|
| 突然不能用 | Google 改了内部 API | 检查 issue tracker、等社群更新 |
| Q&A 答案模糊 | 上传文件太多、retrieve 失准 | 拆成几个 notebook（每个 < 50 source）|
| 中文支持不好 | 预设 UI 设成英文 | NotebookLM 设置改 zh-Hant |

### 进一步

- catalog §1 [`mcp-skills-catalog.md` §1 笔记 / 知识库](mcp-skills-catalog.zh-CN.md#1-笔记--知识库)
- 完整 research workspace：用 [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) 集成 NotebookLM + Zotero + Obsidian

---

## 5. Zotero Workflow

> Zotero 管文献，加上 [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) 后 Claude Code 能直接搜 / 加 / 分类 / 标 references。

### 为什么

研究流程经典痛点：
- “我那篇 paper 在哪？”——Zotero 有，但要切换窗口
- “给我所有讲 transformer 的 paper 摘要”——要自己 select、export、丢给 LLM
- “这篇 paper 该打什么 tag？”——人工

zotero-skills 把这些变成 Claude Code 内一句 prompt 就跑。

### 跟 zotero-gpt 差别

| 工具 | 角色 | 适合 |
|---|---|---|
| [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) | Zotero plugin（在 Zotero **内部** chat） | 边读 paper 边问 LLM、不切换窗口 |
| [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | Claude Code skill（从 **外部** 操作 Zotero） | 写 paper / 整理文献时，Claude Code 为主 |

互补不冲突，可以两个都装。

### 步骤

#### Step 1：开启 Zotero local API

Zotero 桌面版默认不开 API。打开：
- **Edit → Preferences → Advanced → Config Editor**
- 找 `extensions.zotero.httpServer.enabled`，设 `true`
- 找 `extensions.zotero.httpServer.port`，默认 `23119`

#### Step 2：clone zotero-skills

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

照 repo README 设置（包含 API key 给 Web API 写操作用）。

#### Step 3：实用 prompt

**搜文献**：
```
搜我 Zotero library 内所有 2023 年之后、跟 multi-agent 相关的 paper，
按 cited count 排序、输出成 markdown table。
```

**自动分类**：
```
看我 collection "Inbox" 里的 50 篇 paper，按主题自动建 sub-collection
（譬如 "RAG"、"Tool Use"、"Multi-Agent"），把 paper 移进去。
```

**标 tag**：
```
读我 Zotero 内这篇 paper（attached PDF 看完），
从 abstract 提取 5 个 keyword 当 tag 加上去。
```

**写 paper 引用整理**：
```
我的 paper draft 在 ./paper/v3.tex，
找出所有 \cite{} 对应的 BibTeX entry，跟 Zotero library 对比，
把缺的 export 出 .bib 给我。
```

### 常见 pitfall

| 症状 | 原因 | 解法 |
|---|---|---|
| skill 触发但 query 失败 | Zotero 没在跑 / API 没开 | 开 Zotero 桌面版 + 确认 port 23119 listening |
| 写操作（add / move）失败 | local API 是 read-only，要用 Web API | 设置 Web API key（[zotero.org/settings/keys](https://www.zotero.org/settings/keys)） |
| collection 结构乱 | 自动分类 prompt 没给目录结构 | prompt 给 Claude 看现有 collection tree、再决定怎么分 |

### 进一步

- 完整 research workspace：[`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) 集成 Zotero + Obsidian + NotebookLM
- 学术论文写作：[`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills)
- 14 个研究流程 skill 集：[`WenyuChiou/ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)

---

## 找不到你要的 recipe？

- 看 [Stage 5](../stages/05-claude-code-ecosystem.zh-CN.md) 完整概念
- 看 [`mcp-skills-catalog.md`](mcp-skills-catalog.zh-CN.md) 完整工具清单
- 看 [`schema-design-cheatsheet.md`](schema-design-cheatsheet.zh-CN.md) 写 tool schema 的细节
- 看 [`cli-agents-guide.md`](cli-agents-guide.zh-CN.md) 6 个主流 CLI agent 比较

要新 recipe → 开 issue 或直接 PR 一份。recipe 格式：**为什么 + 步骤 + 范本 prompt + 常见 pitfall + 进一步**。
