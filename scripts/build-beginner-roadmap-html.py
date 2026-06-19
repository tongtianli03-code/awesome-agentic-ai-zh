#!/usr/bin/env python3
"""Build a beginner-friendly single-file HTML guide for the Chinese roadmap."""

from __future__ import annotations

import html
import posixpath
import re
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "beginner-agentic-ai-roadmap.html"


CORE_FILES = [
    "README.zh-Hans.md",
    "PROGRESS.zh-Hans.md",
    "docs/HOW_TO_USE.md",
    "resources/setup-guide.zh-Hans.md",
    "stages/00-foundations.zh-Hans.md",
    "stages/01-llm-basics.zh-Hans.md",
    "stages/02-prompt-engineering.zh-Hans.md",
    "stages/03-tool-use-and-hello-agent.zh-Hans.md",
    "stages/04-agent-frameworks.zh-Hans.md",
    "stages/05-claude-code-ecosystem.zh-Hans.md",
    "stages/06-memory-rag.zh-Hans.md",
    "stages/07-multi-agent-production.zh-Hans.md",
    "stages/07.5-advanced-agentic-concepts.zh-Hans.md",
    "stages/08-agent-interfaces.zh-Hans.md",
    "tracks/cli/A1-cli-intro.zh-Hans.md",
    "tracks/cli/A2-cli-workflow.zh-Hans.md",
    "tracks/cli/A3-cli-production.zh-Hans.md",
    "branches/for-everyday-users.zh-Hans.md",
    "branches/for-developer.zh-Hans.md",
    "branches/for-knowledge-worker.zh-Hans.md",
    "branches/for-researcher.zh-Hans.md",
    "branches/for-teacher.zh-Hans.md",
    "walkthroughs/build-first-agent-in-7-steps.zh-Hans.md",
    "examples/README.zh-Hans.md",
    "examples/stage-1/04-cross-provider/README.md",
    "resources/README.zh-Hans.md",
    "resources/glossary.zh-Hans.md",
    "resources/agent-paradigms.zh-Hans.md",
    "resources/cli-agents-guide.zh-Hans.md",
    "resources/cookbook.zh-Hans.md",
    "resources/courses.zh-Hans.md",
    "resources/mcp-skills-catalog.zh-Hans.md",
    "resources/schema-design-cheatsheet.zh-Hans.md",
    "resources/subagent-advanced.zh-Hans.md",
    "resources/subagent-cookbook.zh-Hans.md",
    "CAPSTONE.zh-Hans.md",
    "ROADMAP.zh-Hans.md",
    "RESOURCES.zh-Hans.md",
    "CONTRIBUTING.zh-Hans.md",
    "CODE_OF_CONDUCT.zh-Hans.md",
    "SECURITY.zh-Hans.md",
]


VISUALS = [
    ("resources/diagrams/banner.zh-Hans.png", "总览横幅", "这张图适合作为路线入口，让你先知道主题不是单点工具，而是一整条学习地图。"),
    ("resources/diagrams/learning-map.zh-Hans.png", "学习地图", "先走 Stage 0-2，再分 Track A 使用 CLI agent 或 Track B 构建 agent。"),
    ("resources/diagrams/branch-decision-tree.zh-Hans.png", "分支选择", "按你的身份选择后续路径：开发者、研究员、教师、知识工作者、日常用户。"),
    ("resources/diagrams/ai-ml-llm-agent-hierarchy.zh-Hans.png", "AI / LLM / Agent 层级", "把 AI、模型、智能体放在同一张层级图里，避免概念混淆。"),
    ("resources/diagrams/prompt-context-harness-stack.zh-Hans.png", "Prompt / Context / Harness", "理解智能体工程不是只写 prompt，还要管理上下文和执行外壳。"),
    ("resources/diagrams/stage5-stack.zh-Hans.png", "Claude Code 生态栈", "Stage 5 的 MCP、Skills、Plugins、Subagents 在这里形成一套工具生态。"),
    ("resources/diagrams/claude-architecture-map.zh-Hans.png", "Claude Code 架构图", "把 CLI agent、MCP、Skills、Subagents、SDK 放到同一套架构里看。"),
    ("resources/diagrams/subagent-4-stage-flow.zh-Hans.png", "Subagent 生命周期", "展示子代理从分派、执行、回报到整合的流程。"),
    ("resources/diagrams/subagent-vs-skill.zh-Hans.png", "Subagent vs Skill", "区分“派一个助手做事”和“加载一份做事流程”。"),
    ("resources/diagrams/rag-pipeline-overview.jpg", "RAG 基础流水线", "把“查资料再回答”的过程画成流水线。"),
    ("resources/diagrams/chunking-strategies.jpg", "Chunking 切分策略", "资料切太小没语境，切太大噪音多；这张图帮你理解切资料的取舍。"),
    ("resources/diagrams/reflexion-persistent-memory-loop.zh-Hans.png", "持久记忆循环", "展示 agent 如何把经验写入记忆，再在下一轮任务中使用。"),
    ("resources/diagrams/multi-agent-debate-flow.zh-Hans.png", "多 Agent 辩论流程", "Stage 7 的多角色协作适合用流程图理解。"),
    ("resources/diagrams/stack-4layer.zh-Hans.png", "四层工作边界", "Stage 7.5 用它解释 agent 的任务边界、上下文和执行层。"),
    ("resources/diagrams/failure-lifecycle.zh-Hans.png", "失败生命周期", "生产化不是只让 agent 跑起来，还要知道它怎么失败、怎么恢复。"),
    ("resources/diagrams/concept-cluster.zh-Hans.png", "进阶概念群", "把 12 个进阶概念按关联聚成一张地图。"),
    ("resources/diagrams/principle-dependency.zh-Hans.png", "原则依赖图", "展示哪些工程原则互相支撑，适合复盘时看。"),
    ("resources/diagrams/agent-guardrail-patterns.zh-Hans.png", "安全护栏模式", "Stage 8 的 Computer Use / Browser Use / Sandbox 都需要这类护栏。"),
    ("resources/diagrams/power-user-multi-type-workflow.zh-Hans.png", "高级用户工作流", "给 Track A 使用者看：多个 CLI / 浏览器 / 桌面工具如何协作。"),
    ("resources/diagrams/agent-paradigm-decision-tree.zh-Hans.png", "Agent 型态选择树", "在 CLI、浏览器、工作流、嵌入式 agent 之间做选择。"),
    ("resources/diagrams/subagent-composition-patterns.zh-Hans.png", "Subagent 组合模式", "适合作为 Stage 5/7 之后的进阶图。"),
]


BEGINNER_NOTES = {
    "README.zh-Hans.md": (
        "你可以把这个仓库理解成一份“AI agent 学习导航地图”。它不是一本从头到尾读完的课本，"
        "而是告诉你先学什么、什么时候动手、之后按你的目标走哪条路。"
    ),
    "resources/setup-guide.zh-Hans.md": (
        "这一章是给完全没写过代码的人准备的开机指南。目标不是成为程序员，而是让你的电脑具备“能运行练习”的基本环境。"
    ),
    "stages/00-foundations.zh-Hans.md": (
        "Stage 0 是地基。Python 像说明书语言，CLI 像和电脑直接对话，Git 像历史记录，API 像服务窗口，JSON/YAML 像表格配置。"
    ),
    "stages/01-llm-basics.zh-Hans.md": (
        "Stage 1 开始真正碰 LLM。你会学会把一句话发给模型、拿回回答，并理解 token、上下文窗口、temperature 为什么影响费用和结果。"
    ),
    "stages/02-prompt-engineering.zh-Hans.md": (
        "Prompt 不是“魔法咒语”，更像给助理写清楚任务说明。你会练习角色设定、例子、逐步思考和反复修改。"
    ),
    "stages/03-tool-use-and-hello-agent.zh-Hans.md": (
        "从这里开始，模型不只是聊天，而是会选择工具。Agent 可以理解为“会思考下一步、会调用工具、会观察结果再继续”的助理。"
    ),
    "stages/04-agent-frameworks.zh-Hans.md": (
        "Framework 像脚手架。它帮你组织多个步骤、多个角色和工具调用，避免每次都从零手写。"
    ),
    "stages/05-claude-code-ecosystem.zh-Hans.md": (
        "这一章讲工具生态。MCP 像统一插头，Skills 像操作手册，Plugins 像工具包，Subagents 像临时派出去的小助手。"
    ),
    "stages/06-memory-rag.zh-Hans.md": (
        "RAG 和 Memory 解决的是“模型不知道或记不住”的问题。可以把 RAG 想成先去资料库查书，再带着书里的内容回答。"
    ),
    "stages/07-multi-agent-production.zh-Hans.md": (
        "多 agent 不是越多越好。这里学的是什么时候需要多角色协作，以及上线后怎么观察、评估、控制成本和处理失败。"
    ),
    "stages/07.5-advanced-agentic-concepts.zh-Hans.md": (
        "这是概念加深层。它帮你把前面零散技术连接成一套工程判断：边界、反思、评估、工作流、动态生成。"
    ),
    "stages/08-agent-interfaces.zh-Hans.md": (
        "最后一章是 agent 怎么操作世界：看屏幕、用浏览器、在沙箱里跑代码。这里开始接近真实产品。"
    ),
    "tracks/cli/A1-cli-intro.zh-Hans.md": (
        "Track A 是“先会用”。如果你的目标是让 CLI agent 帮你做事，不急着自己造 agent，就从这里进入。"
    ),
    "tracks/cli/A2-cli-workflow.zh-Hans.md": (
        "这一段教你把临时聊天变成可重复流程：固定说明、固定命令、固定验收标准。"
    ),
    "tracks/cli/A3-cli-production.zh-Hans.md": (
        "这里把个人使用升级到真实工作流：权限、成本、自动化、CI、可观察性都开始重要。"
    ),
}


GLOSSARY = [
    ("Python", "一种让电脑照步骤做事的语言。你写的是说明书，电脑逐行执行。"),
    ("CLI / Terminal", "不用鼠标点，而是用文字命令和电脑对话。适合自动化和让 agent 操作项目。"),
    ("Git", "项目的时间机器。每次 commit 都像存档，可以知道改了什么，也能回退。"),
    ("API", "软件之间的服务窗口。你按规定格式提交请求，对方返回结果。"),
    ("Token", "模型计算文字长度的单位。它决定模型能看多少内容，也影响费用。"),
    ("Prompt", "你给模型的任务说明。写得越清楚，模型越不容易猜错。"),
    ("Tool use", "让模型不只回答，还能调用计算器、搜索、文件系统、数据库等工具。"),
    ("Agent", "会规划下一步、会用工具、会根据结果继续行动的 AI 助理。"),
    ("RAG", "先查资料再回答。适合让模型使用你自己的文档、知识库或数据库。"),
    ("MCP", "让 AI 工具接入外部系统的统一协议，可以理解成一套通用插头。"),
    ("Sandbox", "隔离试验箱。让 agent 跑代码或操作文件时，不直接碰坏真实环境。"),
]


def all_source_files() -> list[str]:
    files = []
    seen = set()
    for item in CORE_FILES:
        path = ROOT / item
        if path.is_file() and item not in seen:
            files.append(item)
            seen.add(item)

    for path in sorted(ROOT.glob("examples/**/README.zh-Hans.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel not in seen:
            files.append(rel)
            seen.add(rel)

    for path in sorted(ROOT.glob("**/*.zh-Hans.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("_build/"):
            continue
        if rel not in seen:
            files.append(rel)
            seen.add(rel)
    return files


def slug(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value).strip("-").lower()
    return clean or "section"


def title_for(markdown_text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return fallback


def strip_github_switcher(markdown_text: str) -> str:
    return re.sub(r'^<div align="right">.*?</div>\s*', "", markdown_text, count=1, flags=re.DOTALL)


def convert_markdown(markdown_text: str) -> str:
    cleaned = strip_github_switcher(markdown_text)
    return markdown.markdown(
        cleaned,
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )


def rewrite_local_paths(converted_html: str, source_rel: str) -> str:
    source_dir = posixpath.dirname(source_rel)

    def repl(match: re.Match[str]) -> str:
        attr = match.group(1)
        url = html.unescape(match.group(2))
        if (
            url.startswith("#")
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url)
            or url.startswith("//")
        ):
            return match.group(0)

        suffix = ""
        main = url
        for marker in ("#", "?"):
            if marker in main:
                main, tail = main.split(marker, 1)
                suffix = marker + tail
                break

        if not main:
            return match.group(0)

        normalized = posixpath.normpath(posixpath.join(source_dir, main))
        if normalized.startswith("../"):
            normalized = normalized.lstrip("./")
        return f'{attr}="{html_escape(normalized + suffix)}"'

    return re.sub(r'(src|href)="([^"]+)"', repl, converted_html)


def html_escape(value: str) -> str:
    return html.escape(value, quote=True)


def source_meta(rel: str) -> tuple[str, str]:
    if rel.startswith("stages/"):
        return "主线阶段", "stage"
    if rel.startswith("tracks/"):
        return "Track A", "track"
    if rel.startswith("branches/"):
        return "身份分支", "branch"
    if rel.startswith("resources/"):
        return "参考资源", "resource"
    if rel.startswith("examples/"):
        return "练习代码", "example"
    if rel.startswith("walkthroughs/"):
        return "走查教程", "walkthrough"
    return "总览/附录", "appendix"


def render_visuals() -> str:
    cards = []
    for src, title, caption in VISUALS:
        if not (ROOT / src).is_file():
            continue
        cards.append(
            f"""
            <figure class="visual-card">
              <img src="{html_escape(src)}" alt="{html_escape(title)}" loading="lazy">
              <figcaption><strong>{html_escape(title)}</strong><span>{html_escape(caption)}</span></figcaption>
            </figure>
            """
        )
    return "\n".join(cards)


def render_glossary() -> str:
    return "\n".join(
        f"<div class=\"term\"><dt>{html_escape(term)}</dt><dd>{html_escape(desc)}</dd></div>"
        for term, desc in GLOSSARY
    )


def render_css_diagrams() -> str:
    return """
    <div class="diagram-grid">
      <section class="diagram-panel">
        <h3>Stage 0 地基顺序</h3>
        <ol class="flow">
          <li><b>Python</b><span>让电脑照步骤办事</span></li>
          <li><b>CLI</b><span>用命令直接操作电脑</span></li>
          <li><b>Git</b><span>给项目做历史存档</span></li>
          <li><b>API</b><span>按窗口规则请求服务</span></li>
          <li><b>JSON/YAML</b><span>机器能读懂的配置表</span></li>
        </ol>
      </section>
      <section class="diagram-panel">
        <h3>Stage 2 Prompt 进阶梯</h3>
        <ol class="ladder">
          <li>随口问</li>
          <li>写清角色和目标</li>
          <li>给 2-5 个例子</li>
          <li>让它逐步推理</li>
          <li>按验收标准反复改</li>
        </ol>
      </section>
      <section class="diagram-panel">
        <h3>Stage 3 ReAct 循环</h3>
        <div class="loop">
          <span>Thought<br><small>先想</small></span>
          <span>Action<br><small>调用工具</small></span>
          <span>Observation<br><small>看结果</small></span>
          <span>Stop / Continue<br><small>停或再来</small></span>
        </div>
      </section>
      <section class="diagram-panel">
        <h3>Stage 8 三种操作界面</h3>
        <div class="compare">
          <div><b>Computer Use</b><span>看屏幕、点鼠标，像远程控制电脑。</span></div>
          <div><b>Browser Use</b><span>读网页结构，适合自动化网站任务。</span></div>
          <div><b>Code Sandbox</b><span>隔离运行代码，避免弄坏真实环境。</span></div>
        </div>
      </section>
    </div>
    """


def render_documents(files: list[str]) -> tuple[str, str]:
    nav_items = []
    articles = []
    for idx, rel in enumerate(files, 1):
        path = ROOT / rel
        markdown_text = path.read_text(encoding="utf-8")
        title = title_for(markdown_text, rel)
        doc_id = f"doc-{idx:03d}-{slug(rel)}"
        group, group_slug = source_meta(rel)
        note = BEGINNER_NOTES.get(rel)
        note_html = ""
        if note:
            note_html = f"""
            <aside class="beginner-note">
              <span>给零基础读者的翻译</span>
              <p>{html_escape(note)}</p>
            </aside>
            """
        articles.append(
            f"""
            <article id="{doc_id}" class="source-doc" data-group="{html_escape(group_slug)}">
              <div class="doc-kicker">{idx:02d} · {html_escape(group)} · <code>{html_escape(rel)}</code></div>
              <h2>{html_escape(title)}</h2>
              {note_html}
              <div class="markdown-body">
                {rewrite_local_paths(convert_markdown(markdown_text), rel)}
              </div>
            </article>
            """
        )
        nav_items.append(
            f"""
            <a href="#{doc_id}" data-group="{html_escape(group_slug)}">
              <span>{idx:02d}</span>
              <strong>{html_escape(title)}</strong>
              <small>{html_escape(group)}</small>
            </a>
            """
        )
    return "\n".join(nav_items), "\n".join(articles)


def render_coverage(files: list[str]) -> str:
    rows = []
    for idx, rel in enumerate(files, 1):
        group, _ = source_meta(rel)
        rows.append(
            f"<tr><td>{idx}</td><td>{html_escape(group)}</td><td><code>{html_escape(rel)}</code></td></tr>"
        )
    return "\n".join(rows)


def build() -> str:
    files = all_source_files()
    nav, articles = render_documents(files)
    coverage = render_coverage(files)
    return f"""<!doctype html>
<html lang="zh-Hans">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Agent 学习路线 · 零基础图文版</title>
  <style>
    :root {{
      --paper: #f8f4e8;
      --paper-2: #fffaf0;
      --ink: #192026;
      --muted: #66727f;
      --line: #d6cdbb;
      --blue: #1d63d8;
      --green: #147a5c;
      --red: #b73a30;
      --amber: #ba7a16;
      --dark: #101820;
      --radius: 8px;
      --shadow: 0 18px 50px rgba(16, 24, 32, 0.14);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(16,24,32,.04) 1px, transparent 1px) 0 0 / 32px 32px,
        linear-gradient(0deg, rgba(16,24,32,.035) 1px, transparent 1px) 0 0 / 32px 32px,
        var(--paper);
      font: 16px/1.75 "Avenir Next", "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", sans-serif;
      letter-spacing: 0;
      overflow-x: hidden;
    }}
    a {{ color: var(--blue); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    img {{ max-width: 100%; height: auto; }}
    code, pre {{
      font-family: "SFMono-Regular", "Menlo", "Consolas", monospace;
      font-size: .92em;
    }}
    .app-shell {{
      display: grid;
      grid-template-columns: minmax(240px, 320px) minmax(0, 1fr);
      min-height: 100vh;
    }}
    .sidebar {{
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      padding: 22px 18px;
      background: #111a22;
      color: #f8f4e8;
      border-right: 1px solid rgba(255,255,255,.12);
    }}
    .brand {{
      display: grid;
      gap: 8px;
      padding-bottom: 18px;
      border-bottom: 1px solid rgba(255,255,255,.18);
    }}
    .brand b {{
      font-size: clamp(24px, 3vw, 38px);
      line-height: 1.05;
      letter-spacing: 0;
      font-weight: 800;
    }}
    .brand span {{ color: #b9c5cd; font-size: 13px; }}
    .filters {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin: 18px 0;
    }}
    .filters button {{
      border: 1px solid rgba(255,255,255,.2);
      background: rgba(255,255,255,.06);
      color: #f8f4e8;
      padding: 8px 9px;
      border-radius: var(--radius);
      cursor: pointer;
      font-size: 13px;
      text-align: left;
    }}
    .filters button.active {{ background: #f8f4e8; color: #111a22; }}
    .source-nav {{ display: grid; gap: 6px; padding-bottom: 24px; }}
    .source-nav a {{
      display: grid;
      grid-template-columns: 34px 1fr;
      gap: 8px;
      padding: 9px;
      color: #eef2f4;
      text-decoration: none;
      border-radius: var(--radius);
      border: 1px solid transparent;
    }}
    .source-nav a:hover {{ background: rgba(255,255,255,.07); border-color: rgba(255,255,255,.14); }}
    .source-nav span {{
      color: #83b7ff;
      font-variant-numeric: tabular-nums;
      font-weight: 700;
    }}
    .source-nav strong {{
      display: block;
      font-size: 13px;
      line-height: 1.35;
      overflow-wrap: anywhere;
      min-width: 0;
    }}
    .source-nav small {{ display: block; color: #9daab3; font-size: 12px; }}
    main {{ min-width: 0; }}
    .hero {{
      min-height: 92vh;
      display: grid;
      align-items: end;
      padding: clamp(28px, 6vw, 78px);
      background:
        linear-gradient(180deg, rgba(16,24,32,.05), rgba(16,24,32,.18)),
        url("resources/diagrams/banner.zh-Hans.png") center / cover no-repeat;
      border-bottom: 1px solid var(--line);
    }}
    .hero h1 {{
      max-width: 980px;
      margin: 0;
      color: #fffaf0;
      text-shadow: 0 3px 18px rgba(0,0,0,.45);
      font-size: clamp(40px, 8vw, 96px);
      line-height: .95;
      font-weight: 900;
      letter-spacing: 0;
    }}
    .hero p {{
      max-width: 820px;
      margin: 22px 0 0;
      color: #fffaf0;
      font-size: clamp(18px, 2.2vw, 27px);
      text-shadow: 0 2px 12px rgba(0,0,0,.38);
    }}
    .section-band {{
      padding: clamp(32px, 5vw, 70px);
      border-bottom: 1px solid var(--line);
    }}
    .section-band h2 {{
      margin: 0 0 16px;
      font-size: clamp(28px, 4vw, 52px);
      line-height: 1.08;
      letter-spacing: 0;
    }}
    .intro-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 26px;
    }}
    .milestone {{
      border: 1px solid var(--line);
      border-left: 6px solid var(--blue);
      background: rgba(255,255,255,.58);
      padding: 16px;
      border-radius: var(--radius);
      min-height: 156px;
    }}
    .milestone:nth-child(2) {{ border-left-color: var(--green); }}
    .milestone:nth-child(3) {{ border-left-color: var(--amber); }}
    .milestone:nth-child(4) {{ border-left-color: var(--red); }}
    .milestone b {{ display: block; font-size: 18px; margin-bottom: 8px; }}
    .term-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .term {{
      border: 1px solid var(--line);
      background: var(--paper-2);
      border-radius: var(--radius);
      padding: 14px;
    }}
    .term dt {{ font-weight: 800; color: var(--dark); }}
    .term dd {{ margin: 4px 0 0; color: var(--muted); }}
    .visual-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      margin-top: 22px;
    }}
    .diagram-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      margin-top: 22px;
    }}
    .diagram-panel {{
      border: 1px solid var(--line);
      background: var(--paper-2);
      border-radius: var(--radius);
      padding: 18px;
      min-height: 260px;
    }}
    .diagram-panel h3 {{ margin: 0 0 14px; font-size: 20px; }}
    .flow, .ladder {{
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 10px;
    }}
    .flow li {{
      display: grid;
      grid-template-columns: 92px 1fr;
      align-items: center;
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-left: 5px solid var(--blue);
      border-radius: var(--radius);
      background: rgba(255,255,255,.62);
    }}
    .flow li:nth-child(2) {{ border-left-color: var(--green); }}
    .flow li:nth-child(3) {{ border-left-color: var(--amber); }}
    .flow li:nth-child(4) {{ border-left-color: var(--red); }}
    .flow li:nth-child(5) {{ border-left-color: #6b5d9a; }}
    .flow span, .compare span {{ color: var(--muted); }}
    .ladder li {{
      padding: 10px 12px;
      margin-left: calc(var(--i, 0) * 12px);
      border-radius: var(--radius);
      background: #ecf3ff;
      border: 1px solid #b8cdeb;
    }}
    .ladder li:nth-child(1) {{ --i: 0; }}
    .ladder li:nth-child(2) {{ --i: 1; }}
    .ladder li:nth-child(3) {{ --i: 2; }}
    .ladder li:nth-child(4) {{ --i: 3; }}
    .ladder li:nth-child(5) {{ --i: 4; }}
    .loop {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}
    .loop span {{
      display: grid;
      place-items: center;
      min-height: 86px;
      text-align: center;
      border-radius: 50%;
      border: 2px solid var(--green);
      background: #edf7f0;
      font-weight: 800;
    }}
    .loop small {{ color: var(--muted); font-weight: 600; }}
    .compare {{ display: grid; gap: 10px; }}
    .compare div {{
      display: grid;
      gap: 4px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255,255,255,.62);
    }}
    .visual-card {{
      margin: 0;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper-2);
      overflow: hidden;
      box-shadow: var(--shadow);
    }}
    .visual-card img {{
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: contain;
      background: #202831;
    }}
    .visual-card figcaption {{
      display: grid;
      gap: 4px;
      padding: 13px 15px 15px;
    }}
    .visual-card figcaption span {{ color: var(--muted); }}
    .source-doc {{
      margin: clamp(22px, 4vw, 46px) clamp(18px, 5vw, 70px);
      padding: clamp(22px, 4vw, 46px);
      border: 1px solid var(--line);
      background: rgba(255,250,240,.88);
      border-radius: var(--radius);
      box-shadow: 0 12px 38px rgba(25,32,38,.09);
    }}
    .doc-kicker {{
      color: var(--muted);
      font-size: 13px;
      text-transform: none;
      margin-bottom: 12px;
    }}
    .source-doc h2 {{
      margin: 0 0 18px;
      font-size: clamp(25px, 3vw, 42px);
      line-height: 1.15;
      letter-spacing: 0;
    }}
    .beginner-note {{
      border: 1px solid #98c3ad;
      border-left: 7px solid var(--green);
      background: #eef8f0;
      border-radius: var(--radius);
      padding: 14px 16px;
      margin: 18px 0 28px;
    }}
    .beginner-note span {{
      display: block;
      font-weight: 800;
      color: var(--green);
      margin-bottom: 6px;
    }}
    .beginner-note p {{ margin: 0; }}
    .markdown-body h1 {{ font-size: 30px; margin-top: 28px; }}
    .markdown-body h2 {{ font-size: 25px; border-top: 1px solid var(--line); padding-top: 24px; margin-top: 30px; }}
    .markdown-body h3 {{ font-size: 21px; margin-top: 24px; }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      display: block;
      overflow-x: auto;
      border: 1px solid var(--line);
      background: #fffdf6;
    }}
    .markdown-body th, .markdown-body td {{
      border: 1px solid var(--line);
      padding: 9px 10px;
      vertical-align: top;
    }}
    .markdown-body th {{ background: #efe5d0; text-align: left; }}
    .markdown-body pre {{
      overflow-x: auto;
      max-width: 100%;
      padding: 14px;
      background: #111a22;
      color: #eef2f4;
      border-radius: var(--radius);
      border: 1px solid rgba(0,0,0,.2);
    }}
    .markdown-body code {{
      background: rgba(29,99,216,.09);
      color: #0c458f;
      padding: 2px 5px;
      border-radius: 5px;
      max-width: 100%;
      overflow-wrap: anywhere;
      word-break: break-word;
    }}
    .markdown-body pre code {{
      display: block;
      background: transparent;
      color: inherit;
      padding: 0;
      max-width: 100%;
    }}
    .coverage table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--paper-2);
      border: 1px solid var(--line);
    }}
    .coverage td, .coverage th {{
      border: 1px solid var(--line);
      padding: 8px 10px;
      text-align: left;
    }}
    .top-link {{
      position: fixed;
      right: 18px;
      bottom: 18px;
      background: var(--dark);
      color: var(--paper);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}
    @media (max-width: 980px) {{
      .app-shell {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: relative; height: auto; }}
      .source-nav {{ max-height: 380px; overflow: auto; }}
      .source-nav a {{ grid-template-columns: 40px minmax(0, 1fr); }}
      .intro-grid, .term-grid, .visual-grid, .diagram-grid {{ grid-template-columns: 1fr; }}
      .hero {{ min-height: 78vh; padding: 28px 18px; }}
      .section-band {{ padding: 30px 18px; }}
      .source-doc {{
        margin: 20px 12px;
        padding: 18px;
        max-width: calc(100vw - 24px);
      }}
      .source-doc h2, .markdown-body h1, .markdown-body h2, .markdown-body h3 {{
        overflow-wrap: anywhere;
      }}
      .markdown-body pre, .markdown-body pre code {{
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: break-all;
      }}
      .markdown-body :not(pre) > code {{
        white-space: normal;
        overflow-wrap: anywhere;
        word-break: break-all;
      }}
      .markdown-body table {{
        display: table;
        table-layout: fixed;
        width: 100%;
        max-width: 100%;
        overflow: visible;
      }}
      .markdown-body th, .markdown-body td {{
        overflow-wrap: anywhere;
        word-break: break-word;
      }}
    }}
  </style>
</head>
<body>
  <div class="app-shell" id="top">
    <aside class="sidebar">
      <div class="brand">
        <b>AI Agent 学习路线</b>
        <span>零基础图文版 · 覆盖 {len(files)} 份中文路线文件</span>
      </div>
      <div class="filters" aria-label="内容筛选">
        <button class="active" data-filter="all">全部</button>
        <button data-filter="stage">主线</button>
        <button data-filter="track">Track A</button>
        <button data-filter="branch">分支</button>
        <button data-filter="resource">资源</button>
        <button data-filter="example">练习</button>
      </div>
      <nav class="source-nav" aria-label="文档导航">
        {nav}
      </nav>
    </aside>
    <main>
      <section class="hero">
        <div>
          <h1>从零开始学 AI Agent，不把你当程序员。</h1>
          <p>这是一份把原仓库路线完整打包的单页 HTML：先用生活类比建立直觉，再保留全部中文原文、练习、资源、分支和结业任务。</p>
        </div>
      </section>

      <section class="section-band">
        <h2>先看这 4 个判断</h2>
        <p>如果你完全没有代码基础，不要从工具名开始背。先看你在每一阶段要获得哪种能力。</p>
        <div class="intro-grid">
          <div class="milestone"><b>1. 电脑地基</b><span>会打开终端、运行脚本、读写配置、用 Git 存档。不会这些，后面会在小错误上反复卡住。</span></div>
          <div class="milestone"><b>2. 模型对话</b><span>理解 token、上下文、temperature，知道一次 API 调用到底发生了什么。</span></div>
          <div class="milestone"><b>3. 会用工具的 Agent</b><span>让模型选择工具、执行动作、读结果，再决定下一步。</span></div>
          <div class="milestone"><b>4. 上线与界面</b><span>多 agent、记忆、评估、浏览器、沙箱、安全和成本，决定它能不能用于真实工作。</span></div>
        </div>
      </section>

      <section class="section-band">
        <h2>零基础术语表</h2>
        <p>下面这些解释故意不用工程师黑话。之后遇到同一个词，可以回到这里找直觉。</p>
        <dl class="term-grid">
          {render_glossary()}
        </dl>
      </section>

      <section class="section-band">
        <h2>图像导航</h2>
        <p>这些是仓库里最适合先看的图。它们负责建立方向感，后面完整原文会展开细节。</p>
        <div class="visual-grid">
          {render_visuals()}
        </div>
      </section>

      <section class="section-band">
        <h2>流程图式理解</h2>
        <p>有些概念原仓库用文字讲得很完整，这里额外用 HTML/CSS 做成小图，帮助零基础读者先建立直觉。</p>
        {render_css_diagrams()}
      </section>

      <section class="section-band coverage">
        <h2>覆盖清单</h2>
        <p>为避免遗漏，下面列出本 HTML 已纳入的本地中文路线文件。生成时会跳过 <code>_build/</code> 里的重复副本。</p>
        <table>
          <thead><tr><th>#</th><th>分类</th><th>源文件</th></tr></thead>
          <tbody>
            {coverage}
          </tbody>
        </table>
      </section>

      {articles}
    </main>
  </div>
  <a class="top-link" href="#top" aria-label="回到顶部">↑ 顶部</a>
  <script>
    const buttons = document.querySelectorAll('.filters button');
    const navItems = document.querySelectorAll('.source-nav a');
    const docs = document.querySelectorAll('.source-doc');
    buttons.forEach((button) => {{
      button.addEventListener('click', () => {{
        const filter = button.dataset.filter;
        buttons.forEach((b) => b.classList.toggle('active', b === button));
        navItems.forEach((item) => {{
          item.style.display = filter === 'all' || item.dataset.group === filter ? '' : 'none';
        }});
        docs.forEach((doc) => {{
          doc.style.display = filter === 'all' || doc.dataset.group === filter ? '' : 'none';
        }});
      }});
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
