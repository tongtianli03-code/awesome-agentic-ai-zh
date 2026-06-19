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


STAGE_CARDS = [
    ("0", "基础准备", "给电脑打地基", "你会打开终端、跑 Python、用 Git 存档、理解 API 和配置文件。", "做完 5 个小练习：公开 API、CLI、JSON/YAML、Git、API auth。"),
    ("1", "LLM 基础", "第一次用程序叫模型干活", "你会知道 token、上下文窗口、temperature 和计费为什么重要。", "跑 hello world、比较中英文 token、估算成本和延迟。"),
    ("2", "Prompt 设计", "给 AI 写清楚任务单", "你会把模糊需求写成角色、格式、例子和验收标准。", "练 system prompt、few-shot、CoT 和迭代优化。"),
    ("3", "工具与第一个 Agent", "让模型长出手脚", "你会理解模型如何选择工具、调用函数、观察结果再继续。", "练 function calling、ReAct、错误处理和 schema 设计。"),
    ("4", "Agent 框架", "给复杂任务搭脚手架", "你会知道什么时候用 LangGraph、AutoGen、CrewAI 这类框架。", "把同一个 agent 用不同框架实现，并比较取舍。"),
    ("5", "Claude Code 生态", "给 AI 助手配工具箱", "你会理解 MCP、Skills、Plugins、Subagents 分别解决什么问题。", "写 CLAUDE.md、slash command、skill、MCP 和 subagent 练习。"),
    ("6", "RAG 与 Memory", "给模型配图书馆和笔记本", "你会知道如何让模型查自己的资料、记住用户偏好和经验。", "练 embedding、vector DB、chunking、RAG pipeline 和 memory。"),
    ("7", "多 Agent 与生产化", "从演示变成能用的系统", "你会学评估、日志、成本、延迟、部署和失败恢复。", "练 multi-agent debate、eval、observability、deploy 和 cost control。"),
    ("7.5", "进阶概念地图", "学会判断边界和工程原则", "你会把前面技术连接成判断体系，不再只会照教程做。", "读 work boundary、system of record、progressive disclosure 等概念。"),
    ("8", "Agent 操作界面", "让 agent 操作真实世界", "你会理解 Computer Use、Browser Use、Code Sandbox 的边界和风险。", "练浏览器自动化、沙箱运行和安全护栏。"),
]


TRACKS = [
    ("Track A", "CLI Power User", "我想先会用，不急着自己造 agent", "Stage 0-2 → A1 → A2 → Stage 5 必修段 → A3 → Stage 8 使用视角 → Capstone"),
    ("Track B", "Agent Builder", "我想从零构建自己的 agent 系统", "Stage 0-2 → Stage 3 → Stage 4 → Stage 5 全量 → Stage 6 → Stage 7 → 7.5 → Stage 8 构建视角 → Capstone"),
    ("日常用户捷径", "Everyday User", "我主要想用 AI 改善日常工作生活", "README → setup-guide 网页/桌面/IDE 层 → everyday-users 分支 → 小流程实践"),
]


COURSE_STAGES = [
    {
        "number": "0",
        "title": "基础准备",
        "hook": "别急着学 Agent，先让电脑能听懂你的指令。",
        "pain": "零基础最容易卡在“我照着复制了，为什么终端说找不到文件”。这一关先解决环境、路径、命令、配置这些地基问题。",
        "analogy": "像开一家小店之前，先装好水电、收银台、货架和监控。AI 练习也一样，Python、终端、Git、API、JSON/YAML 就是这些基础设施。",
        "output": "你能打开终端，运行一个 Python 脚本，调用 GitHub 公开 API，把结果保存成文件，并知道 token 要放在环境变量里。",
        "concepts": [
            ("Python", "写给电脑看的步骤说明书。"),
            ("终端", "用文字命令直接操作电脑的窗口。"),
            ("Git", "给学习项目做版本存档。"),
            ("API", "软件之间按窗口规则办事。"),
            ("JSON/YAML", "机器能读懂的表格和配置。"),
        ],
        "steps": ["打开终端", "运行脚本", "请求 API", "读配置", "保存结果"],
        "exercise": "只做一件事：运行 GitHub followers 小脚本，看它能不能打印出某个用户的 follower 数量。",
        "success": "你能说清楚：脚本文件在哪里、终端当前在哪个文件夹、API 返回了什么、token 为什么不能写死在代码里。",
        "stuck": "先检查三件事：当前目录是不是项目根目录、文件名有没有打错、token 有没有真的 export 到当前终端。",
        "skip": "如果你已经能独立运行 Python、clone/push GitHub repo、读懂 JSON，可以快速扫一遍练习后进入 Stage 1。",
        "deep": ["stages/00-foundations.zh-Hans.md", "resources/setup-guide.zh-Hans.md"],
    },
    {
        "number": "1",
        "title": "LLM 基础",
        "hook": "让模型回你一句话，只是第一步；你要知道这句话是怎么被计费、被限制、被影响的。",
        "pain": "很多人会用 ChatGPT，但不知道 API 调用里有模型名、输入、输出、token、上下文窗口、temperature，所以一换成代码就迷路。",
        "analogy": "把 LLM API 想成一家云端问答店：你把问题递进去，店员按字数和难度计费，再把答案递回来。",
        "output": "你能用 DeepSeek、OpenAI 兼容 SDK 或本地 Ollama 跑一个 hello world，并知道回答为什么有时稳定、有时发散。",
        "concepts": [
            ("模型", "负责理解和生成文字的大脑。"),
            ("Token", "模型的计价单位，接近“字块”而不是完整汉字。"),
            ("上下文窗口", "模型一次能看到的材料上限。"),
            ("Temperature", "控制回答稳定还是发散的旋钮。"),
            ("延迟/成本", "每次调用都要付时间和费用。"),
        ],
        "steps": ["准备 API key", "发送问题", "模型生成", "拿到回答", "估算成本"],
        "exercise": "只做一件事：让模型回答“用一句话解释什么是 AI Agent”，再把 temperature 调高低各跑一次。",
        "success": "你能解释：为什么同一个问题会有不同回答，为什么长文档会更贵，为什么 API key 不能截图发给别人。",
        "stuck": "先看错误码：401 多半是 key 不对，429 多半是频率或额度问题，timeout 多半是网络或服务响应慢。",
        "skip": "如果你已经会用任意一家云模型 API，并能解释 token 和上下文窗口，可以进入 Stage 2。",
        "deep": ["stages/01-llm-basics.zh-Hans.md", "examples/stage-1/04-cross-provider/README.md"],
    },
    {
        "number": "2",
        "title": "Prompt 设计",
        "hook": "Prompt 不是玄学咒语，而是给 AI 写一张清楚的任务单。",
        "pain": "小白常见问题不是“不会写高级 prompt”，而是需求太含糊：没说角色、目标、格式、例子、验收标准。",
        "analogy": "你请助理做 PPT，不能只说“做得高级一点”。你要说给谁看、几页、风格、必须包含什么、什么算通过。",
        "output": "你能把一句模糊需求改成结构化 prompt，让模型按固定格式输出，并能通过迭代把结果改好。",
        "concepts": [
            ("角色", "让模型站在某种身份说话。"),
            ("格式", "提前规定输出长什么样。"),
            ("Few-shot", "给几个示范，让模型照样子做。"),
            ("Chain of Thought", "让模型先分步骤思考，再给结果。"),
            ("验收标准", "告诉模型什么叫完成。"),
        ],
        "steps": ["模糊需求", "补角色", "给格式", "加例子", "按标准修改"],
        "exercise": "只做一件事：把“帮我总结文章”改成一张任务单，要求模型输出 3 个要点、1 个风险、1 个行动建议。",
        "success": "你能说清楚：原始 prompt 哪里模糊，修改后新增了哪些限制，结果为什么更可控。",
        "stuck": "如果模型跑偏，不要骂模型；先补充输入材料、输出格式、反例和判断标准。",
        "skip": "如果你能稳定让模型按指定格式输出，并会用例子纠偏，可以进入 Stage 3。",
        "deep": ["stages/02-prompt-engineering.zh-Hans.md"],
    },
    {
        "number": "3",
        "title": "工具与第一个 Agent",
        "hook": "从这一关开始，AI 不只是回答，它开始会“办事”。",
        "pain": "聊天模型只能说；Agent 的关键是能选择工具、提交参数、读取结果、再决定下一步。",
        "analogy": "像前台接待员：它听懂你的需求后，不是自己瞎编，而是去查订单系统、日历、库存，再回来答复。",
        "output": "你能做一个最小 Agent：模型判断该用哪个工具，工具返回结果，模型根据结果继续回答。",
        "concepts": [
            ("工具调用", "AI 填一张工具申请单，让程序去执行。"),
            ("Schema", "工具申请单的字段说明。"),
            ("ReAct", "先想、再动手、看结果、决定继续。"),
            ("错误处理", "工具失败时，不让流程直接崩掉。"),
            ("多步推理", "一次任务拆成连续几步完成。"),
        ],
        "steps": ["听懂任务", "选择工具", "填写参数", "观察结果", "继续或停止"],
        "exercise": "只做一件事：做一个天气/计算/查询类小工具，让模型决定何时调用它。",
        "success": "你能指出一次运行里：模型想了什么、调用了哪个工具、工具返回什么、最后答案如何形成。",
        "stuck": "如果工具没被调用，先检查工具描述是不是太抽象；如果参数错，先检查 schema 是否写清楚字段含义。",
        "skip": "如果你还没搞懂 API 和 JSON，不建议跳过；这是从聊天走向 Agent 的分水岭。",
        "deep": ["stages/03-tool-use-and-hello-agent.zh-Hans.md", "examples/stage-3/03-react-from-scratch/README.zh-Hans.md"],
    },
    {
        "number": "4",
        "title": "Agent 框架",
        "hook": "当任务变长、工具变多、角色变多，就需要脚手架。",
        "pain": "手写一个小 Agent 可以，但复杂项目会变成一团流程线：谁先做、失败怎么办、状态放哪、下一步去哪。",
        "analogy": "像装修房子。你可以自己搬砖，但大工程需要施工图、工序表、监工和验收节点。",
        "output": "你能理解 LangGraph、AutoGen、CrewAI 这类框架为什么存在，并能把同一个小 Agent 用框架方式组织。",
        "concepts": [
            ("框架", "帮你组织步骤、状态和角色的脚手架。"),
            ("Graph", "把任务流程画成节点和连线。"),
            ("State", "流程进行到哪、已经知道什么。"),
            ("Typed Agent", "用更严格的输入输出减少混乱。"),
            ("多角色", "把任务拆给不同职责的助手。"),
        ],
        "steps": ["定义任务", "拆成节点", "保存状态", "连接流程", "比较框架"],
        "exercise": "只做一件事：把 Stage 3 的小 Agent 改成一个两步流程：先分析，再执行工具。",
        "success": "你能讲出：手写版和框架版分别适合什么场景，框架帮你省了哪些管理工作。",
        "stuck": "如果框架文档看不懂，先回到流程图：节点是什么、输入是什么、输出流向哪里。",
        "skip": "只想先会用 CLI Agent 的人，可以走 Track A，不必立刻深学 Stage 4。",
        "deep": ["stages/04-agent-frameworks.zh-Hans.md", "examples/stage-4/01-same-agent-two-frameworks/README.zh-Hans.md"],
    },
    {
        "number": "5",
        "title": "Claude Code 生态",
        "hook": "这里学的是：怎样给 AI 助手配工具箱、说明书和临时小组。",
        "pain": "真实项目里，Agent 不是只靠一个 prompt。它需要知道项目规则、调用外部工具、使用固定技能、必要时派子任务。",
        "analogy": "像一间办公室：CLAUDE.md 是公司制度，MCP 是外部系统接口，Skill 是标准作业流程，Subagent 是临时派出去的同事。",
        "output": "你能区分 MCP、Skills、Plugins、Subagents，并知道自己什么时候该用哪一个。",
        "concepts": [
            ("CLAUDE.md", "写给 AI 的项目规则。"),
            ("MCP", "连接外部工具的通用插头。"),
            ("Skill", "可重复使用的操作手册。"),
            ("Plugin", "打包好的工具能力。"),
            ("Subagent", "为某个子任务临时派出的助手。"),
        ],
        "steps": ["写项目规则", "接工具", "沉淀技能", "派子任务", "整合结果"],
        "exercise": "只做一件事：写一个最小 CLAUDE.md，规定学习项目里的文件位置、运行方式和不要泄露 API key。",
        "success": "你能解释：为什么同样是增强 Agent，MCP、Skill、Subagent 不是一回事。",
        "stuck": "如果概念混乱，就问自己：这是接工具、写流程，还是派人做事？答案通常能帮你分类。",
        "skip": "Track A 必看使用层；Track B 需要深读内部结构。",
        "deep": ["stages/05-claude-code-ecosystem.zh-Hans.md", "resources/mcp-skills-catalog.zh-Hans.md"],
    },
    {
        "number": "6",
        "title": "RAG 与 Memory",
        "hook": "让 AI 先查资料、再回答；让它该记住的东西别每次重来。",
        "pain": "模型不是万能数据库。它可能不知道你的私有文档，也可能忘记你前面说过的偏好。",
        "analogy": "RAG 像去图书馆查书后再写报告；Memory 像给助理一本长期笔记本。",
        "output": "你能理解 embedding、向量数据库、chunking、RAG pipeline 和长期记忆分别解决什么问题。",
        "concepts": [
            ("Embedding", "把文字变成可比较的坐标。"),
            ("向量数据库", "按语义相似度找资料的书架。"),
            ("Chunking", "把长资料切成合适的小段。"),
            ("RAG", "检索资料后再生成回答。"),
            ("Memory", "把重要经验留下来以后用。"),
        ],
        "steps": ["切资料", "变坐标", "存书架", "查相关段落", "带资料回答"],
        "exercise": "只做一件事：准备一段自己的学习笔记，让模型先检索笔记再回答问题。",
        "success": "你能说清楚：模型答案里哪些来自资料，资料为什么被找出来，切块大小会影响什么。",
        "stuck": "如果答案不准，先查检索结果，而不是只改 prompt。RAG 的问题常常出在资料没找对。",
        "skip": "如果你的 Agent 暂时只处理短任务，可以稍后学；只要涉及私有资料，就必须回来补上。",
        "deep": ["stages/06-memory-rag.zh-Hans.md", "examples/stage-6/04-full-rag-pipeline/README.zh-Hans.md"],
    },
    {
        "number": "7",
        "title": "多 Agent 与生产化",
        "hook": "从能演示，走向真的能在工作里用。",
        "pain": "Demo 能跑不等于系统能用。上线后会遇到成本、延迟、错误、日志、评测、权限、恢复等问题。",
        "analogy": "像开餐厅试营业：一道菜能做出来不够，还要稳定出餐、控制成本、处理投诉、记录问题。",
        "output": "你能判断什么时候需要多 Agent，怎样做评测、观察运行、控制成本，并把系统部署起来。",
        "concepts": [
            ("多 Agent", "多个角色分工协作，不是越多越好。"),
            ("Eval", "给 Agent 做考试，判断有没有变好。"),
            ("Observability", "看得见系统内部发生了什么。"),
            ("Deploy", "把本地练习放到可运行服务里。"),
            ("成本控制", "让效果、速度、费用达到平衡。"),
        ],
        "steps": ["拆角色", "设计考试", "记录运行", "控制成本", "部署服务"],
        "exercise": "只做一件事：做一个两角色小流程，一个负责提出答案，一个负责挑错并给修改建议。",
        "success": "你能回答：为什么需要两个角色，它们如何交接，怎么判断结果比单模型更好。",
        "stuck": "如果多 Agent 变乱，先减少角色。一个角色说不清楚职责，就不要增加它。",
        "skip": "个人学习可以晚点深入；只要要给别人长期使用，就不能跳过。",
        "deep": ["stages/07-multi-agent-production.zh-Hans.md", "examples/stage-7/02-eval/README.zh-Hans.md"],
    },
    {
        "number": "7.5",
        "title": "进阶概念地图",
        "hook": "这一关不是学更多名词，而是建立判断力。",
        "pain": "前面学完会有很多碎片：工具、记忆、框架、多 Agent、安全。Stage 7.5 帮你知道边界在哪里。",
        "analogy": "像学开车之后再学交通规则、事故责任和路线规划。不是为了炫技，是为了少犯大错。",
        "output": "你能用 work boundary、system of record、progressive disclosure 等概念判断 Agent 该做什么、不该做什么。",
        "concepts": [
            ("工作边界", "哪些事交给 Agent，哪些必须人确认。"),
            ("事实源", "系统到底以哪里为准。"),
            ("渐进披露", "不要一次把所有复杂度扔给用户。"),
            ("反思", "让系统复盘错误并改进。"),
            ("原则依赖", "工程原则之间互相支撑。"),
        ],
        "steps": ["定义边界", "确认事实源", "减少暴露", "复盘失败", "沉淀原则"],
        "exercise": "只做一件事：拿你自己的一个工作流，写出哪些步骤可自动化，哪些必须人工确认。",
        "success": "你能讲清楚：如果 Agent 做错，谁发现、谁负责、用什么事实源纠正。",
        "stuck": "如果概念太抽象，就绑定到真实流程：下单、发邮件、改代码、删文件，分别需要什么护栏？",
        "skip": "做学习 Demo 可以略读；做真实产品前必须回来读。",
        "deep": ["stages/07.5-advanced-agentic-concepts.zh-Hans.md"],
    },
    {
        "number": "8",
        "title": "Agent 操作界面",
        "hook": "最后一关：让 Agent 操作真实世界，但要先学会安全边界。",
        "pain": "让 AI 点网页、操作电脑、跑代码很强，但也危险。它可能点错、读错、执行不该执行的动作。",
        "analogy": "像让一个远程助理临时接管你的电脑。你会给它任务，也会限制它能进哪些房间、能不能付款、能不能删除文件。",
        "output": "你能区分 Computer Use、Browser Use、Code Sandbox 的适用场景，并知道基础安全护栏。",
        "concepts": [
            ("Computer Use", "像看屏幕和点鼠标。"),
            ("Browser Use", "像专门操作网页。"),
            ("Code Sandbox", "在隔离箱里运行代码。"),
            ("Guardrail", "防止越权或误操作的护栏。"),
            ("Human-in-the-loop", "关键动作前让人确认。"),
        ],
        "steps": ["读取界面", "决定动作", "执行操作", "检查结果", "触发护栏"],
        "exercise": "只做一件事：设计一个浏览器 Agent 的安全规则清单，规定哪些动作必须让人确认。",
        "success": "你能说明：什么时候用浏览器自动化，什么时候用沙箱，什么时候必须停下来问人。",
        "stuck": "如果你只觉得它“很酷”，先暂停。Stage 8 的核心不是炫技，而是可控地操作真实环境。",
        "skip": "日常用户可先理解风险；想做产品或自动化的人需要认真学。",
        "deep": ["stages/08-agent-interfaces.zh-Hans.md", "resources/agent-paradigms.zh-Hans.md"],
    },
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


def render_stage_cards() -> str:
    items = []
    for number, title, metaphor, learns, practice in STAGE_CARDS:
        items.append(
            f"""
            <article class="stage-card">
              <div class="stage-num">{html_escape(number)}</div>
              <div>
                <h3>{html_escape(title)}</h3>
                <p class="metaphor">{html_escape(metaphor)}</p>
                <p>{html_escape(learns)}</p>
                <p><strong>动手：</strong>{html_escape(practice)}</p>
              </div>
            </article>
            """
        )
    return "\n".join(items)


def render_track_selector() -> str:
    cards = []
    for label, title, intent, path in TRACKS:
        cards.append(
            f"""
            <section class="track-card">
              <span>{html_escape(label)}</span>
              <h3>{html_escape(title)}</h3>
              <p>{html_escape(intent)}</p>
              <div>{html_escape(path)}</div>
            </section>
            """
        )
    return "\n".join(cards)


def render_course_nav() -> str:
    items = [
        ("课程开场", "#story"),
        ("学习路线", "#course"),
        ("路径选择", "#tracks"),
        ("术语表", "#glossary"),
        ("图像导航", "#visuals"),
        ("完整资料库", "#source-library"),
    ]
    stage_items = [
        (f"{stage['number']} · {stage['title']}", f"#course-stage-{slug(stage['number'])}")
        for stage in COURSE_STAGES
    ]
    links = items + stage_items
    return "\n".join(
        f'<a href="{href}"><span>{idx:02d}</span><strong>{html_escape(label)}</strong></a>'
        for idx, (label, href) in enumerate(links, 1)
    )


def doc_id_for(idx: int, rel: str) -> str:
    return f"doc-{idx:03d}-{slug(rel)}"


def render_concept_list(concepts: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"<li><strong>{html_escape(term)}</strong><span>{html_escape(desc)}</span></li>"
        for term, desc in concepts
    )


def render_step_visual(steps: list[str]) -> str:
    return "\n".join(
        f"<li><span>{idx}</span><b>{html_escape(step)}</b></li>"
        for idx, step in enumerate(steps, 1)
    )


def render_deep_links(deep_links: list[str], doc_ids: dict[str, str]) -> str:
    links = []
    for rel in deep_links:
        target = f"#{doc_ids[rel]}" if rel in doc_ids else html_escape(rel)
        label = rel.replace(".zh-Hans.md", "").replace("README.md", "README")
        links.append(f'<a href="{target}">{html_escape(label)}</a>')
    return "\n".join(links)


def render_course_stages(doc_ids: dict[str, str]) -> str:
    cards = []
    for stage in COURSE_STAGES:
        anchor = f"course-stage-{slug(stage['number'])}"
        cards.append(
            f"""
            <article class="course-stage" id="{anchor}">
              <div class="course-stage-head">
                <span>第 {html_escape(stage['number'])} 关</span>
                <h3>{html_escape(stage['title'])}</h3>
                <p>{html_escape(stage['hook'])}</p>
              </div>
              <div class="course-stage-grid">
                <section class="course-story">
                  <h4>先解决什么问题</h4>
                  <p>{html_escape(stage['pain'])}</p>
                  <h4>生活类比</h4>
                  <p>{html_escape(stage['analogy'])}</p>
                  <h4>这一关做出什么</h4>
                  <p>{html_escape(stage['output'])}</p>
                </section>
                <section class="course-visual" aria-label="{html_escape(stage['title'])}流程图">
                  <ol>
                    {render_step_visual(stage['steps'])}
                  </ol>
                </section>
                <section class="concept-card">
                  <h4>核心词，用人话解释</h4>
                  <ul>
                    {render_concept_list(stage['concepts'])}
                  </ul>
                </section>
                <section class="mission-card">
                  <h4>30 分钟闯关任务</h4>
                  <p>{html_escape(stage['exercise'])}</p>
                  <div><strong>成功标志：</strong>{html_escape(stage['success'])}</div>
                  <div><strong>卡住先看：</strong>{html_escape(stage['stuck'])}</div>
                  <div><strong>能不能跳过：</strong>{html_escape(stage['skip'])}</div>
                </section>
              </div>
              <footer class="deep-links">
                <strong>原文深读：</strong>
                {render_deep_links(stage['deep'], doc_ids)}
              </footer>
            </article>
            """
        )
    return "\n".join(cards)


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
        doc_id = doc_id_for(idx, rel)
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
    doc_ids = {rel: doc_id_for(idx, rel) for idx, rel in enumerate(files, 1)}
    course_nav = render_course_nav()
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
    .side-label {{
      margin: 18px 0 8px;
      color: #83b7ff;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .course-nav {{
      display: grid;
      gap: 6px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(255,255,255,.18);
    }}
    .course-nav a {{
      display: grid;
      grid-template-columns: 34px 1fr;
      gap: 8px;
      padding: 9px;
      color: #eef2f4;
      text-decoration: none;
      border-radius: var(--radius);
      border: 1px solid transparent;
    }}
    .course-nav a:hover {{ background: rgba(255,255,255,.07); border-color: rgba(255,255,255,.14); }}
    .course-nav span {{
      color: #f4c166;
      font-variant-numeric: tabular-nums;
      font-weight: 800;
    }}
    .course-nav strong {{
      display: block;
      font-size: 13px;
      line-height: 1.35;
    }}
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
    .story-split {{
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(360px, .95fr);
      gap: 22px;
      align-items: stretch;
      margin-top: 24px;
    }}
    .story-copy {{
      border: 1px solid var(--line);
      background: var(--paper-2);
      border-radius: var(--radius);
      padding: 24px;
      font-size: 18px;
    }}
    .outcome-board {{
      display: grid;
      gap: 12px;
    }}
    .outcome-card {{
      border: 1px solid var(--line);
      border-left: 7px solid var(--green);
      background: rgba(255,255,255,.66);
      border-radius: var(--radius);
      padding: 15px 16px;
    }}
    .outcome-card:nth-child(2) {{ border-left-color: var(--blue); }}
    .outcome-card:nth-child(3) {{ border-left-color: var(--amber); }}
    .outcome-card b {{ display: block; font-size: 18px; margin-bottom: 4px; }}
    .course-wrap {{
      display: grid;
      gap: 22px;
      margin-top: 28px;
    }}
    .course-stage {{
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255,250,240,.93);
      box-shadow: 0 16px 44px rgba(25,32,38,.1);
      overflow: hidden;
    }}
    .course-stage-head {{
      padding: 24px 26px;
      background: #111a22;
      color: var(--paper);
    }}
    .course-stage-head span {{
      display: inline-block;
      color: #f4c166;
      font-weight: 900;
      margin-bottom: 8px;
    }}
    .course-stage-head h3 {{
      margin: 0;
      font-size: clamp(30px, 4vw, 52px);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .course-stage-head p {{
      max-width: 860px;
      margin: 12px 0 0;
      color: #d9e2e8;
      font-size: 19px;
    }}
    .course-stage-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(320px, .95fr);
      gap: 18px;
      padding: 20px;
    }}
    .course-story,
    .course-visual,
    .concept-card,
    .mission-card {{
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper-2);
      padding: 18px;
    }}
    .course-story h4,
    .concept-card h4,
    .mission-card h4 {{
      margin: 0 0 8px;
      font-size: 18px;
    }}
    .course-story p {{ margin: 0 0 14px; }}
    .course-story p:last-child {{ margin-bottom: 0; }}
    .course-visual {{
      display: grid;
      align-content: center;
      background:
        linear-gradient(90deg, rgba(29,99,216,.08) 1px, transparent 1px) 0 0 / 24px 24px,
        #f8fbff;
    }}
    .course-visual ol {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      gap: 10px;
    }}
    .course-visual li {{
      display: grid;
      grid-template-columns: 42px 1fr;
      align-items: center;
      gap: 10px;
      padding: 11px;
      background: #fffdf6;
      border: 1px solid #c8d7ef;
      border-radius: var(--radius);
      position: relative;
    }}
    .course-visual li:not(:last-child)::after {{
      content: "";
      position: absolute;
      left: 30px;
      bottom: -11px;
      width: 2px;
      height: 10px;
      background: var(--blue);
    }}
    .course-visual span {{
      display: grid;
      place-items: center;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: var(--blue);
      color: #fff;
      font-weight: 900;
    }}
    .concept-card ul {{
      list-style: none;
      display: grid;
      gap: 8px;
      padding: 0;
      margin: 0;
    }}
    .concept-card li {{
      display: grid;
      gap: 3px;
      padding: 10px;
      border-radius: var(--radius);
      background: #f0eadc;
    }}
    .concept-card li strong {{ color: var(--dark); }}
    .concept-card li span {{ color: var(--muted); }}
    .mission-card {{
      border-left: 7px solid var(--amber);
      display: grid;
      gap: 10px;
    }}
    .mission-card p,
    .mission-card div {{ margin: 0; }}
    .mission-card div {{
      padding: 10px;
      border-radius: var(--radius);
      background: rgba(20,122,92,.08);
    }}
    .deep-links {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      padding: 14px 20px 20px;
      border-top: 1px solid var(--line);
      background: #f0eadc;
    }}
    .deep-links a {{
      display: inline-flex;
      padding: 7px 10px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper-2);
      text-decoration: none;
      font-weight: 700;
    }}
    .term-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}
    .stage-map {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 24px;
    }}
    .stage-card {{
      display: grid;
      grid-template-columns: 70px 1fr;
      gap: 16px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper-2);
      padding: 16px;
      box-shadow: 0 10px 28px rgba(25,32,38,.07);
    }}
    .stage-num {{
      display: grid;
      place-items: center;
      aspect-ratio: 1;
      border-radius: var(--radius);
      background: var(--dark);
      color: var(--paper);
      font-weight: 900;
      font-size: 26px;
      font-variant-numeric: tabular-nums;
    }}
    .stage-card h3 {{ margin: 0 0 4px; font-size: 22px; }}
    .stage-card p {{ margin: 6px 0 0; }}
    .stage-card .metaphor {{
      color: var(--red);
      font-weight: 800;
    }}
    .track-selector {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 22px;
    }}
    .track-card {{
      border: 1px solid var(--line);
      border-top: 7px solid var(--blue);
      border-radius: var(--radius);
      background: var(--paper-2);
      padding: 18px;
    }}
    .track-card:nth-child(2) {{ border-top-color: var(--green); }}
    .track-card:nth-child(3) {{ border-top-color: var(--amber); }}
    .track-card span {{
      display: inline-block;
      color: var(--muted);
      font-weight: 800;
      margin-bottom: 8px;
    }}
    .track-card h3 {{ margin: 0 0 8px; font-size: 24px; }}
    .track-card div {{
      margin-top: 12px;
      padding: 12px;
      background: #f0eadc;
      border-radius: var(--radius);
      font-weight: 700;
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
    .source-library {{
      margin: clamp(32px, 5vw, 70px);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: rgba(255,250,240,.72);
      box-shadow: 0 18px 50px rgba(16, 24, 32, 0.12);
      overflow: hidden;
    }}
    .source-library > summary {{
      cursor: pointer;
      list-style: none;
      padding: 26px 30px;
      background: #111a22;
      color: var(--paper);
      font-size: 26px;
      font-weight: 900;
    }}
    .source-library > summary::-webkit-details-marker {{ display: none; }}
    .source-library > summary span {{
      display: block;
      color: #b9c5cd;
      font-size: 15px;
      font-weight: 600;
      margin-top: 6px;
    }}
    .source-library .coverage {{
      padding: 28px;
      border-bottom: 1px solid var(--line);
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
      .intro-grid, .term-grid, .visual-grid, .diagram-grid, .stage-map, .track-selector, .story-split, .course-stage-grid {{ grid-template-columns: 1fr; }}
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
        <span>零基础图文课程 · 后附 {len(files)} 份完整原文资料</span>
      </div>
      <div class="side-label">Course</div>
      <nav class="course-nav" aria-label="课程导航">
        {course_nav}
      </nav>
      <div class="side-label">Source Filters</div>
      <div class="filters" aria-label="内容筛选">
        <button class="active" data-filter="all">全部</button>
        <button data-filter="stage">主线</button>
        <button data-filter="track">Track A</button>
        <button data-filter="branch">分支</button>
        <button data-filter="resource">资源</button>
        <button data-filter="example">练习</button>
      </div>
      <div class="side-label">Source Library</div>
      <nav class="source-nav" aria-label="文档导航">
        {nav}
      </nav>
    </aside>
    <main>
      <section class="hero">
        <div>
          <h1>从会聊天，到会指挥 AI 做事。</h1>
          <p>你不是来背编程名词的。你要学会把 AI 从聊天窗口，升级成能查资料、调工具、写报告、操作网页、留下记忆的助手。</p>
        </div>
      </section>

      <section class="section-band" id="story">
        <h2>先想象一个真实任务</h2>
        <div class="story-split">
          <div class="story-copy">
            <p>你对 AI 说：“帮我看 10 篇资料，整理结论，做一份能给老板看的报告。”</p>
            <p>普通聊天模型会直接凭当前对话回答。真正的 Agent 会先拆任务：找资料、读资料、提取要点、调用工具、检查遗漏、生成报告，必要时再回头修正。</p>
            <p>这条路线的目标不是把你变成程序员，而是让你看懂并逐步掌握这套“指挥 AI 做事”的能力。</p>
          </div>
          <div class="outcome-board">
            <div class="outcome-card"><b>第一层：会问</b><span>写清楚任务，让模型稳定输出你要的格式。</span></div>
            <div class="outcome-card"><b>第二层：会查</b><span>让模型使用 API、文件、知识库，而不是凭空编。</span></div>
            <div class="outcome-card"><b>第三层：会做</b><span>让 Agent 分步骤调用工具、观察结果、继续推进。</span></div>
          </div>
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
        <h2>10 张路线卡，先建立方向感</h2>
        <p>下面是看地图，不是考试。每张卡只回答三个问题：这阶段像什么、学什么、动手做什么。</p>
        <div class="stage-map">
          {render_stage_cards()}
        </div>
      </section>

      <section class="section-band" id="course">
        <h2>主线课程：十关逐步走</h2>
        <p>这一部分是重新写给非程序员的主阅读区。每一关都先讲“为什么要学”，再给流程图、概念翻译、30 分钟任务和原文深读入口。</p>
        <div class="course-wrap">
          {render_course_stages(doc_ids)}
        </div>
      </section>

      <section class="section-band" id="tracks">
        <h2>我该走哪条路</h2>
        <p>这条路线不是所有人都必须完整走一遍。先按目标选路径，再回到完整原文查细节。</p>
        <div class="track-selector">
          {render_track_selector()}
        </div>
      </section>

      <section class="section-band" id="glossary">
        <h2>零基础术语表</h2>
        <p>下面这些解释故意不用工程师黑话。之后遇到同一个词，可以回到这里找直觉。</p>
        <dl class="term-grid">
          {render_glossary()}
        </dl>
      </section>

      <section class="section-band" id="visuals">
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

      <details class="source-library" id="source-library">
        <summary>完整原文资料库<span>主线课程读完后再展开。这里保留 {len(files)} 份源文件、练习、资源、分支和结业任务，确保内容没有遗漏。</span></summary>
        <section class="coverage">
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
      </details>
    </main>
  </div>
  <a class="top-link" href="#top" aria-label="回到顶部">↑ 顶部</a>
  <script>
    const buttons = document.querySelectorAll('.filters button');
    const navItems = document.querySelectorAll('.source-nav a');
    const docs = document.querySelectorAll('.source-doc');
    const sourceLibrary = document.querySelector('#source-library');
    const openSourceLibrary = () => {{
      if (sourceLibrary) sourceLibrary.open = true;
    }};
    document.querySelectorAll('.source-nav a, .deep-links a').forEach((link) => {{
      link.addEventListener('click', () => {{
        if (link.getAttribute('href')?.startsWith('#doc-')) openSourceLibrary();
      }});
    }});
    buttons.forEach((button) => {{
      button.addEventListener('click', () => {{
        const filter = button.dataset.filter;
        openSourceLibrary();
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
    content = "\n".join(line.rstrip() for line in build().splitlines()) + "\n"
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
