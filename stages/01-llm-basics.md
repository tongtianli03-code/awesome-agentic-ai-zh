# Stage 1 — LLM Fundamentals

⏱ **Time estimate**: 1 week (~5-8 hours)

## 📌 Learning Goals

After this stage you will be able to:
- Explain what an LLM is, what tokens are, and what context window means
- Make your first API call to Claude / GPT / Gemini and parse the response
- Compare the four major LLM families (Claude / GPT / Gemini / Llama) on strengths
- Estimate cost per task using per-token pricing

## 🚪 Entry Conditions

You should already:
- Be able to run a Python script
- Know what HTTP / REST is conceptually
- Have an API key from at least one provider (Anthropic / OpenAI / Google)

If not — go back to Stage 0 first.

## 📚 Required Reading

1. [**Anthropic — What is Claude?**](https://www.anthropic.com/news/claude-3-family) — official model overview
2. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — first API call walkthrough
3. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face's intro
4. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — read the pricing table, calculate cost for 1k input + 1k output

## 🛠 Hello-X Projects (must run, not just read)

### Hello, LLM API
Five-line Python script that calls Claude API and prints the response.

```python
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}]
)
print(msg.content[0].text)
```

### Hello, Tokens
Run the same prompt 100 times and watch token counts vary.
- Notice: temperature ≠ 0 produces variation
- Notice: token count for the SAME English vs Chinese sentence

### Hello, Pricing
Calculate the actual dollar cost of running 1000 inferences for your hello-world prompt. Use Anthropic's pricing page + count tokens via the SDK's `usage` field.

## 🎯 Curated Projects

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

| Field | Value |
|---|---|
| Maintainer | Anthropic (official) |
| Language | Python |
| Stars | ★ 42k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: How to call Claude API for every common pattern — chat, tools, citations, multi-modal, prompt caching.

**Best for**: Anyone starting with Claude. The notebooks walk you through every API feature with runnable examples.

**Notes**: Treat this as your reference manual. Don't try to read it cover-to-cover; use as needed when you hit a specific question.

**Run it**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| Field | Value |
|---|---|
| Maintainer | OpenAI (official) |
| Language | Python / Jupyter |
| Stars | ★ 73k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Same as Anthropic Cookbook but for GPT family. Massive collection of recipes, structured outputs, tool use, embeddings.

**Best for**: Anyone using OpenAI API. The structured outputs and function calling examples are particularly strong.

**Notes**: Larger than Anthropic's cookbook. Use the search heavily — don't browse linearly.

---

### [LangChain Academy](https://academy.langchain.com/)

| Field | Value |
|---|---|
| Maintainer | LangChain Inc. |
| Format | Free online courses |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: LLM fundamentals, embeddings, RAG, agents — taught through LangChain. Good even if you don't end up using LangChain.

**Best for**: Visual learners who want video walkthroughs.

**Notes**: Some lessons are LangChain-marketing-heavy. Skip those, take the conceptual lessons.

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| Field | Value |
|---|---|
| Maintainer | datawhalechina (Chinese ML community) |
| Language | 中文 (zh-CN) |
| Stars | ★ 23k+ |
| Last update | ⚠️ Borderline (Jun 2025) |
| License | Custom (CC BY-NC-SA) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Andrew Ng's prompt engineering / building systems / fine-tuning courses translated and adapted for Chinese learners. Hands-on notebooks.

**Best for**: Chinese-speaking beginners who want a guided LLM curriculum.

**Notes**: zh-CN content (Datawhale uses simplified Chinese) — but technical content transfers fine. Excellent free Chinese-language entry point.

---

### [Hugging Face — Large Language Model Course](https://huggingface.co/learn/llm-course)

| Field | Value |
|---|---|
| Maintainer | Hugging Face |
| Format | Free online course + notebooks |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: How LLMs actually work (tokenization, transformers, fine-tuning) with Hugging Face ecosystem.

**Best for**: Readers who want to understand what's happening inside, not just the API surface.

**Notes**: More academic than cookbooks. Covers training, not just inference.

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| Field | Value |
|---|---|
| Maintainer | Andrej Karpathy |
| Status | ⚠️ Archived (last update Aug 2024); outline only — never built out |
| Recommendation | ⭐⭐ |

**What it teaches**: Build a "Storyteller AI LLM" from scratch. Karpathy's signature pedagogical depth.

**Best for**: Readers who want to truly understand LLMs (not just call API).

**Notes**: Course is being built — currently has outline + some videos on YouTube. Watch Karpathy's "Let's build GPT from scratch" first.

---

### [Anthropic — Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| Field | Value |
|---|---|
| Maintainer | Anthropic (official) |
| Format | Documentation |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Authoritative documentation for the Claude API.

**Best for**: Direct reference. Bookmark this.

---

### [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| Field | Value |
|---|---|
| Maintainer | Andrej Karpathy |
| Format | YouTube video (2 hours) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build a transformer-based GPT from scratch in PyTorch. Foundational understanding of how LLMs work internally.

**Best for**: Anyone who wants to understand WHY LLMs behave the way they do, not just HOW to call them.

**Notes**: 2 hours of dense content. Pause and code along — don't passively watch.

---

## ✅ Self-Check Before Stage 2

Can you:
- [ ] Make a Claude API call from Python in 5 lines
- [ ] Explain why "你好" might use 2 tokens but "Hello" uses 1
- [ ] Quote roughly the per-token price for Claude Sonnet vs Opus
- [ ] Name one strength of Claude vs GPT vs Gemini vs Llama

If yes → proceed to [Stage 2 — Prompt Engineering](02-prompt-engineering.md).

If no → re-read the Anthropic Quickstart + run all 3 hello-X projects above.
