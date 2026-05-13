# Stage 2 — Prompt Engineering

> [繁體中文](./02-prompt-engineering.md) | **简体中文** | [English](./02-prompt-engineering.en.md)

⏱ **时间估算**：1-2 周（约 5-12 小时）

> 👋 **从 [Stage 1](01-llm-basics.zh-Hans.md) 来的**：好，你会调用 API 了——这 5-12 小时：写出可重用的结构化 prompt、用 few-shot 跟 chain-of-thought 解难题、用 eval 量化 prompt 改善幅度。**直接从这里开始的**：先确认你会调用 LLM API、会用 token 算成本——做不到请先回 [Stage 1](01-llm-basics.zh-Hans.md)。

> 💡 用语不熟（prompt / few-shot / CoT / system prompt⋯）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)。

## 📌 学习目标

走完这个阶段后你会：
- 写出结构化 prompt（角色 + 任务 + 格式 + 示例）
- 应用 few-shot prompting，并知道什么时候有用
- 在推理任务上使用 chain-of-thought（CoT）
- 反复迭代修改一个 prompt 并衡量改善
- 看出什么时候 prompt 已经到极限了（这时你需要 tool / agent）

## 🚪 进入条件

你应该已经：
- 会调用 LLM API（Stage 1）
- 会解析 / 遍历 API 响应

## 📚 必修阅读

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 官方，整理得不错
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI 观点
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — 学术风，深入
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — 直接清楚

## 🛠 动手练习

### 练习 1：System Prompt
同样的 user message，三个不同的 system prompt。观察人格 / 输出格式怎么变。

<details>
<summary>📋 <b>起手码</b>（复制到 <code>practice_1.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "请帮我解释什么是租赁合约。"

for label, system in SYSTEM_PROMPTS.items():
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system=system,
        messages=[{"role": "user", "content": USER_MSG}],
    )
    print(f"\n--- [{label}] ---")
    print(msg.content[0].text)

# === 自我验证 ===
print(f"\n✅ 练习 1 通过 — 同一个问题、3 种人格 / 格式 / 语气")
```

> 🦙 **Ollama 对照**：Anthropic 用 `system=` 参数；OpenAI 兼容 SDK（含 Ollama）把 system 放在 messages 第一笔：`messages=[{"role": "system", "content": ...}, {"role": "user", "content": ...}]`。其余相同。

</details>

### 练习 2：Few-Shot
挑一个分类任务。先用 0-shot 跑，再用 3-shot 跑。量一下准确率差多少。

<details>
<summary>📋 <b>起手码</b>（复制到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

TEST_SET = [
    ("这部电影超赞、看完想再看一次！", "正面"),
    ("剧情无聊、演员演技尴尬。", "负面"),
    ("这是一部 2019 年的电影。", "中立"),
    ("我不确定喜不喜欢、可能再想想。", "中立"),
    ("第一集很不错但第二集就崩了。", "负面"),
    ("看完心情很好、推荐！", "正面"),
]

FEW_SHOT_EXAMPLES = """范例：
input: 这家餐厅的牛排好吃到让我哭出来。
output: 正面

input: 服务生态度很差、我再也不会来了。
output: 负面

input: 这家店位于新北市三重区。
output: 中立
"""


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{prefix}input: {text}\noutput:"
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip().splitlines()[0]


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正确 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正确 {c3}/{n} = {c3/n:.0%}")

# === 自我验证 ===
print(f"\n✅ 练习 2 通过 — 0-shot {c0}/{n}、3-shot {c3}/{n}")
assert c3 >= c0, f"预期 3-shot 不比 0-shot 差、实际 {c3} < {c0}"
```

> 🦙 **Ollama 对照**：Few-shot 对小 model（gemma3:4b）改善幅度通常**更大**——小 model 更需要 example 来校准。改 SDK 跟练习 1 Path B 一样。

</details>

### 练习 3：CoT
挑一个数学文字题，比较：
- 纯 prompt
- 纯 prompt + "Let's think step by step"
- 纯 prompt + 一个展示 CoT 的范例

<details>
<summary>📋 <b>起手码</b>（复制到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

QUESTION = "小明有 3 颗苹果。他给了小华 1 颗、又从妈妈那边拿到 5 颗、然后吃了 2 颗。请问现在剩几颗？"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """范例：
Q: 一只鸡有 2 只脚。3 只鸡跟 1 个人共有几只脚？
A: 让我一步一步算。3 只鸡 × 2 只脚 = 6 只脚。1 个人有 2 只脚。总共 6 + 2 = 8 只脚。答案是 8。
"""


def ask(prompt: str) -> str:
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def extract_number(text: str) -> int | None:
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


out_a = ask(QUESTION)
ans_a = extract_number(out_a)

out_b = ask(QUESTION + "\nLet's think step by step.")
ans_b = extract_number(out_b)

out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:")
ans_c = extract_number(out_c)

for label, out, ans in [("A 纯 prompt", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] 答案={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === 自我验证 ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
print(f"\n✅ 练习 3 通过 — {correct}/3 答对")
```

> 🦙 **Ollama 对照**：CoT 对 gemma3:4b 等小 model **必要**——没 step-by-step 几乎答不对。可以拿这题实验大 model 跟小 model 对 CoT 的依赖程度。

</details>

### 练习 4：Iterative Refinement
拿一个模糊的 prompt，refine 5 次。把每一轮记下来。观察哪些改动会提升质量。

<details>
<summary>📋 <b>起手码</b>（复制到 <code>practice_4.py</code>）— 这题没有「对错」、重点是观察过程</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

PROMPTS = {
    "v1 模糊": "写一段介绍 ReAct 的文字。",
    "v2 加目标读者": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。",
    "v3 加格式": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落。",
    "v4 加 example 要求": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落、结尾举一个具体例子（譬如查天气）。",
    "v5 加禁忌": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落、结尾举一个具体例子（譬如查天气）。不要用「赋能」「驱动」「智能」这类空泛词汇。",
}

for label, prompt in PROMPTS.items():
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === 自我验证 ===
print(f"\n✅ 练习 4 通过 — 你已实际感受 prompt 5 个维度的影响")
print("💡 5 个 refine 维度：(1) 目标读者 (2) 格式 (3) 长度 (4) 范例要求 (5) 禁忌词")
```

> 🦙 **Ollama 对照**：用 gemma3:4b 跑 5 轮 refine 特别有教学价值——你会看到「v1 模糊」几乎答不出有用内容、「v5 加禁忌」品质跳幅最大。小 model 对 prompt 质量 sensitivity 高，是练 prompt engineering 的好沙包。

</details>

## 🎯 精选项目

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| 字段 | 内容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：从基础到进阶（CoT、ToT、ReAct、RAG）的端到端 prompt engineering。学术风但实用。

**适合谁**：当参考用。先大致扫过一次，需要某个技巧时再回来查。

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| 字段 | 内容 |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：上百个角色型 prompt。"Act as a [角色]..."的模式。

**适合谁**：卡关时找灵感。不要照抄——把模式拿出来改写。

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**教什么**：跟 dair-ai GitHub 同样的内容，但做成网站、有可以跑的示例。

**适合谁**：手机阅读。

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐ |

**教什么**：管理大量 prompt 的 TypeScript library（模板、对话历史）。

**适合谁**：开始要在 production 管很多 prompt 时。

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| 字段 | 内容 |
|---|---|
| Stars | ★ 10k+ |
| 推荐度 | ⭐⭐⭐ |

**教什么**：可视化 prompt 设计 + 评估工具。

**适合谁**：以 prompt 为主、需要 eval 的团队型应用。

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐ |

**教什么**：Google Cloud 的 prompting cookbook（notebook，PaLM/Gemini 为主）。

**适合谁**：用 Google 技术栈时的跨厂商观点。

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Stage 1 已经提过。这里特别推 `misc/prompt_caching.ipynb` 跟 `multimodal/` 系列 notebook，会教进阶 prompting 模式。

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 34k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：把 prompt 当 code 写——定义 signature 跟 module、用 compiler / teleprompter 自动优化 prompt，不用手刻 f-string。Stanford NLP 出品，是 Stage 2 → Stage 3 的桥。

**适合谁**：跑完 dair-ai 的指南、开始问“我要怎么把 prompt 规模化（不是再多 hard-code）”的人。

**备注**：是 framework 不是 tutorial，学习门槛比 prompt-engineering-guide 高。建议搭配官方 tutorial 网站 dspy.ai 一起读。

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| 字段 | 内容 |
|---|---|
| 语言 | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION（自定义条款，研究 / 非商用为主，使用前读条款） |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：22 种 prompt engineering 技巧的可执行 Jupyter notebook（zero-shot → CoT → ReAct → constitutional），2025 年的更新内容，比 dair-ai 更动手。

**适合谁**：偏好“边跑边学”的人。每个技巧都有独立 notebook，挑感兴趣的看。

---

## 🔭 进阶：context engineering（不是 prompt engineering 了）

当你发现“**单一 prompt 已经 cover 不了**”——要动态组 system prompt + 拉 memory + 塞 retrieved chunks + 接多个 tool definitions——这已经不叫 prompt engineering，叫 **context engineering**。是 prompt engineering 的下一层。

**这个 stage 不用学完它**，只是给个方向性提示：

- 在 [Stage 6（Memory · RAG）](./06-memory-rag.zh-Hans.md) 会碰到（什么数据塞进 prompt）
- 在 [Stage 7（Multi-Agent · Production）](./07-multi-agent-production.zh-Hans.md) 完整面对（context window 预算、memory 阶层、observability）

延伸阅读（不必修、未来想深挖时看）：

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)（★ 3k+）——从 prompt engineering 一路推到 production agent 的 survey
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works)（★ 2k+）——Claude Code 内部解析，含 context engineering 章节

## ✅ 进 Stage 3 前的自我检查

你能不能：
- [ ] 写一个有 system message + user message + 3 个示例 message 的 prompt（few-shot）
- [ ] 示范 CoT 在某个推理任务上提升准确率
- [ ] 反复 refine 一个 prompt 5 次，每一版都留下記录
- [ ] 看出 prompt 不是对的工具的时候（这时要用 tool use）

如果可以 → 进 [Stage 3 — Tool Use & Agent 入门](./03-tool-use-and-hello-agent.zh-Hans.md)。这是最重要的一个阶段——prompt 不要急着跳过去，但也不要卡在这里。
