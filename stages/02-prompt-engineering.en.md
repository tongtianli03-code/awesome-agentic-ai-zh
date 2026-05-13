# Stage 2 — Prompt Engineering

> [繁體中文](./02-prompt-engineering.md) | [简体中文](./02-prompt-engineering.zh-Hans.md) | **English**


⏱ **Time estimate**: 1-2 weeks (~5-12 hours)

> 👋 **Coming from [Stage 1](01-llm-basics.en.md)?** Good — you can call an API. The next 5-12 hours: write reusable structured prompts, use few-shot and chain-of-thought for hard reasoning tasks, and quantify prompt improvement with evals. **Jumped straight here?** Make sure you can call an LLM API and estimate cost in tokens — if not, head back to [Stage 1](01-llm-basics.en.md).

> 💡 Term-unfamiliar? (prompt / few-shot / CoT / system prompt / …) → see [`resources/glossary.en.md`](../resources/glossary.en.md).

## 📌 Learning Goals

After this stage you will be able to:
- Write structured prompts (role + task + format + examples)
- Apply few-shot prompting and know when it helps
- Use chain-of-thought (CoT) for reasoning tasks
- Iteratively refine a prompt and measure improvement
- Recognize when prompting hits its limit (and you need tools / agents)

## 🚪 Entry Conditions

You should already:
- Be able to call an LLM API (Stage 1)
- Be able to parse / iterate over API responses

## 📚 Required Reading

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — official, well-organized
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI's perspective
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — academic-flavored, in-depth
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — be clear and direct

## 🛠 Hands-on Exercises

### Exercise 1: System Prompt
Same user message, three different system prompts. Watch the personality / output format change.

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_1.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPTS = {
    "Strict lawyer": "You are a precise contract lawyer. Cite statute numbers, avoid subjective adjectives.",
    "Kindergarten teacher": "You are a kind kindergarten teacher speaking to a 5-year-old. Use analogies, colloquial language, under 80 words.",
    "JSON machine": "Reply only in JSON. schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "Explain what a lease agreement is."

for label, system in SYSTEM_PROMPTS.items():
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system=system,
        messages=[{"role": "user", "content": USER_MSG}],
    )
    print(f"\n--- [{label}] ---")
    print(msg.content[0].text)

# === Self-check ===
print(f"\n✅ Exercise 1 passed — same question, three different personas / formats / tones")
```

> 🦙 **Ollama equivalent**: Anthropic uses a `system=` parameter; OpenAI-compatible SDKs (including Ollama) put system in the first message: `messages=[{"role": "system", "content": ...}, {"role": "user", "content": ...}]`. Everything else is identical.

</details>

### Exercise 2: Few-Shot
Pick a classification task. Run it 0-shot, then 3-shot. Measure accuracy difference.

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_2.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

# Sentiment classifier: positive / negative / neutral
TEST_SET = [
    ("This movie was amazing — I want to watch it again!", "positive"),
    ("Boring plot, awkward acting.", "negative"),
    ("This is a 2019 film.", "neutral"),
    ("Not sure how I feel about it, might think more.", "neutral"),
    ("Season 1 was great but season 2 fell apart.", "negative"),
    ("Left in a great mood — recommended!", "positive"),
]

FEW_SHOT_EXAMPLES = """Examples:
input: The steak at this place made me cry tears of joy.
output: positive

input: The waiter was rude. Never coming back.
output: negative

input: This shop is in New Taipei City.
output: neutral
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
print(f"correct {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"correct {c3}/{n} = {c3/n:.0%}")

# === Self-check ===
print(f"\n✅ Exercise 2 passed — 0-shot {c0}/{n}, 3-shot {c3}/{n}")
assert c3 >= c0, f"expected 3-shot ≥ 0-shot, got {c3} < {c0}"
```

> 🦙 **Ollama equivalent**: few-shot prompts typically lift small models (gemma3:4b) by an even **larger** margin — smaller models depend more on examples for calibration. SDK swap matches Exercise 1 Path B.

</details>

### Exercise 3: CoT
Pick a math word problem. Compare:
- Plain prompt
- Plain prompt + "Let's think step by step"
- Plain prompt + worked example showing CoT

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_3.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

QUESTION = "Tom has 3 apples. He gives Sarah 1, then mom gives him 5 more, then he eats 2. How many does he have now?"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """Example:
Q: A chicken has 2 legs. 3 chickens and 1 person — how many legs total?
A: Let me work through this step by step. 3 chickens × 2 legs = 6 legs. 1 person has 2 legs. Total 6 + 2 = 8 legs. The answer is 8.
"""


def ask(prompt: str) -> str:
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def extract_number(text: str) -> int | None:
    """Pull the last number from the response as the answer."""
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


out_a = ask(QUESTION)
ans_a = extract_number(out_a)

out_b = ask(QUESTION + "\nLet's think step by step.")
ans_b = extract_number(out_b)

out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:")
ans_c = extract_number(out_c)

for label, out, ans in [("A plain", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] answer={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === Self-check ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
print(f"\n✅ Exercise 3 passed — {correct}/3 correct")
```

> 🦙 **Ollama equivalent**: CoT is **essential** for small models like gemma3:4b — without step-by-step they fail this almost completely. Use this exercise to measure how strongly each model depends on CoT.

</details>

### Exercise 4: Iterative Refinement
Take a vague prompt, refine it 5 times. Track the iterations. Notice what changes improve quality.

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_4.py</code>) — this exercise has no "right answer"; the point is observing the process</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()

# 5 iterations, each adds one constraint
PROMPTS = {
    "v1 vague": "Write a paragraph about ReAct.",
    "v2 +audience": "Write a paragraph about ReAct for software engineers who know Python.",
    "v3 +format": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph.",
    "v4 +example": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph, ending with a concrete example (e.g. weather lookup).",
    "v5 +bans": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph, ending with a concrete example (e.g. weather lookup). Avoid words like 'empower', 'leverage', 'intelligent'.",
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

# === Self-check ===
print(f"\n✅ Exercise 4 passed — you've experienced 5 prompt refinement dimensions in action")
print("💡 The 5 dimensions: (1) target audience (2) format (3) length (4) example demand (5) banned words")
```

> 🦙 **Ollama equivalent**: running 5 refine iterations on gemma3:4b is especially instructive — you'll watch "v1 vague" struggle to produce anything useful and "v5 +bans" show the biggest jump. Small models are highly sensitive to prompt quality, which makes them an excellent sparring partner for prompt engineering.

</details>

## 🎯 Curated Projects

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| Field | Value |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: End-to-end prompt engineering from basics to advanced (CoT, ToT, ReAct, RAG). Academic-flavored but practical.

**Best for**: Reference. Skim once, return when you need a specific technique.

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| Field | Value |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Hundreds of role-based prompts. "Act as a [role]..." patterns.

**Best for**: Inspiration when stuck. Don't copy verbatim — adapt the patterns.

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**What it teaches**: Same content as dair-ai's GitHub but in website format with live examples.

**Best for**: Mobile reading.

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: TypeScript library for managing prompts at scale (templating, conversation history).

**Best for**: When you start managing many prompts in production.

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| Field | Value |
|---|---|
| Stars | ★ 10k+ |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Visual prompt design + evaluation tooling.

**Best for**: Teams building prompt-heavy apps with eval needs.

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: Google Cloud's prompting cookbook (notebooks, PaLM/Gemini focus).

**Best for**: Cross-vendor perspective if you use Google's stack.

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Already cited in Stage 1. Specifically the `misc/prompt_caching.ipynb` and `multimodal/` notebooks teach advanced prompting patterns.

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 34k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Prompt-as-code — define signatures + modules, optimize prompts via compilers / teleprompters instead of hand-tuning f-strings. The natural Stage 2 → Stage 3 bridge. From Stanford NLP.

**Best for**: Readers who finished dair-ai's guide and ask "how do I scale prompts beyond hard-coded strings?"

**Notes**: It's a framework, not a tutorial — higher learning bar than prompt-engineering-guide. Pair with the official tutorial site dspy.ai.

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION (custom terms, research/non-commercial — read before use) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 22 prompt-engineering techniques as runnable Jupyter notebooks (zero-shot → CoT → ReAct → constitutional). 2025 vintage, more hands-on than dair-ai.

**Best for**: Learners who prefer "run-and-learn." Each technique is a standalone notebook — pick whatever interests you.

---

## 🔭 Beyond prompts: context engineering

When you find that **a single prompt can no longer cover the problem** — and you need to dynamically assemble system prompt + retrieved chunks + memory + tool definitions + multi-turn history — you've graduated from prompt engineering to **context engineering**. It's the next layer up.

**Don't try to learn it now**, just know the direction:

- You'll first hit it in [Stage 6 (Memory · RAG)](06-memory-rag.en.md) (what data goes into the prompt)
- You'll fully face it in [Stage 7 (Multi-Agent · Production)](07-multi-agent-production.en.md) (context window budget, memory layering, observability)

Further reading (optional, for when you want to dig deeper):

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering) (★ 3k+) — comprehensive survey from prompt engineering to production agents
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works) (★ 2k+) — Claude Code internals, includes a context-engineering chapter

## ✅ Self-Check Before Stage 3

Can you:
- [ ] Write a prompt with system message + user message + 3 example messages (few-shot)
- [ ] Demonstrate CoT improving accuracy on a reasoning task
- [ ] Iteratively refine a prompt 5 times tracking each version
- [ ] Identify when prompting is the wrong tool (and tool use is needed)

If yes → proceed to [Stage 3 — Tool Use & Agent Intro](03-tool-use-and-hello-agent.en.md). This is the most important stage — don't rush past prompts but also don't get stuck here.
