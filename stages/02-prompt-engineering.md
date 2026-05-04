# Stage 2 — Prompt Engineering

⏱ **Time estimate**: 1-2 weeks (~5-12 hours)

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

## 🛠 Hello-X

### Hello System Prompt
Same user message, three different system prompts. Watch the personality / output format change.

### Hello Few-Shot
Pick a classification task. Run it 0-shot, then 3-shot. Measure accuracy difference.

### Hello CoT
Pick a math word problem. Compare:
- Plain prompt
- Plain prompt + "Let's think step by step"
- Plain prompt + worked example showing CoT

### Hello Iterative Refinement
Take a vague prompt, refine it 5 times. Track the iterations. Notice what changes improve quality.

## 🎯 Curated Projects

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| Field | Value |
|---|---|
| Maintainer | DAIR.AI |
| Stars | ★ 60k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: End-to-end prompt engineering from basics to advanced (CoT, ToT, ReAct, RAG). Academic-flavored but practical.

**Best for**: Reference. Skim once, return when you need a specific technique.

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| Stars | ★ 130k+ |
|---|---|
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

| Stars | ★ 10k+ |
|---|---|
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

## ✅ Self-Check Before Stage 3

Can you:
- [ ] Write a prompt with system message + user message + 3 example messages (few-shot)
- [ ] Demonstrate CoT improving accuracy on a reasoning task
- [ ] Iteratively refine a prompt 5 times tracking each version
- [ ] Identify when prompting is the wrong tool (and tool use is needed)

If yes → proceed to [Stage 3 — Tool Use & Hello Agent](03-tool-use-and-hello-agent.md). This is the most important stage — don't rush past prompts but also don't get stuck here.
