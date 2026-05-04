# Stage 7 — Multi-Agent · Production

⏱ **Time estimate**: 2-4 weeks (~15-30 hours)

The final stage. You're moving from "I can build agents" to "I can run them in production with multiple agents coordinating, evaluation, observability, and deployment."

## 📌 Learning Goals

- Design multi-agent orchestration patterns (debate, planner-executor, peer review)
- Set up evaluation harness for agents
- Add observability (tracing, logging, cost tracking)
- Use Anthropic SDK / OpenAI SDK for production deployment (advanced features: streaming, prompt caching, batching)
- Deploy agents to production (Docker, serverless, monitoring)

## 📚 Required Reading

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — re-read with production lens
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% cost reduction technique
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — async batch jobs
4. **One eval framework's docs** — promptfoo OR LangSmith OR weave

## 🛠 Hello-X

- **Hello Multi-Agent** — 2 agents debating a topic, 3rd agent judging
- **Hello Eval** — write evals for an agent, measure success rate across N runs
- **Hello Observability** — connect LangSmith / Helicone / weave to an agent, view trace
- **Hello SDK Advanced** — use streaming + prompt caching + tool use in one call
- **Hello Deploy** — package an agent in Docker, deploy to cloud (any platform)

## 🎯 Curated Projects

### Multi-Agent Orchestration

#### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: 5 skills for multi-agent runs (task splitter, output reconciler, debate, shared memory, acceptance gate). Patterns for Claude Code multi-agent workflows.

**Best for**: Multi-agent in Claude Code context.

---

#### [microsoft/autogen](https://github.com/microsoft/autogen)

Already cited in Stage 4. In production context, AutoGen's GroupChat coordination pattern is a strong reference for multi-agent debate / brainstorming.

---

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Already cited in Stage 4. For role-based multi-agent (e.g., research → writer → reviewer pipelines), CrewAI is the simplest production pattern.

---

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

Already cited in Stage 4. For production with audit trails, checkpointing, and human-in-the-loop, LangGraph leads.

---

### Evaluation Frameworks

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)

| Stars | ★ 20k+ |
|---|---|
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: YAML-based eval harness for prompts and agents. Compare across models, run regression tests in CI.

**Best for**: Standardized eval pipeline. Replaces "I'll just eyeball it."

**Run it**:
```bash
npx promptfoo init
# Edit promptfooconfig.yaml
npx promptfoo eval
```

---

#### [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

| Stars | ★ 12k+ |
|---|---|
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Academic-grade eval framework with hundreds of standardized benchmarks (MMLU, HellaSwag, GSM8K).

**Best for**: When you need to claim "we got X% on benchmark Y." Research-flavored.

---

#### [openai/evals](https://github.com/openai/evals)

| Stars | ★ 18k+ |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: OpenAI's eval framework. Custom evals for specific use cases.

**Best for**: When you need OpenAI-specific evals or want to contribute back.

---

### Observability

#### [langfuse/langfuse](https://github.com/langfuse/langfuse)

| Stars | ★ 26k+ |
|---|---|
| License | MIT (open source) + paid cloud |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Open-source LLM observability — traces, sessions, evals, prompt management.

**Best for**: Self-hosted production observability. Strong open-source alternative to LangSmith.

---

#### [LangSmith](https://www.langchain.com/langsmith) (proprietary)

**What it teaches**: LangChain's observability platform. Traces, evals, prompt iteration.

**Best for**: If you're deep in LangChain/LangGraph stack. Hosted-only.

---

#### [Helicone](https://github.com/Helicone/helicone)

| Stars | ★ 5k+ |
|---|---|
| License | Apache 2.0 (open source) + paid cloud |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: LLM observability via proxy — drop-in replacement for OpenAI/Anthropic clients, gets you logging + caching.

**Best for**: Quick instrumentation without rewriting code.

---

#### [weave (by Weights & Biases)](https://github.com/wandb/weave)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Tracing + eval framework from W&B. Integrates with their ML platform.

**Best for**: Teams already on W&B for ML experiment tracking.

---

### Anthropic SDK Advanced

#### [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

| Recommendation | ⭐⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Official Python SDK. Streaming, async, tool use, prompt caching, batches, files API.

**Best for**: Building production apps directly on Claude API.

---

#### [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript)

**What it teaches**: TS equivalent of Python SDK.

**Best for**: TypeScript / Node / web apps.

---

#### [Anthropic Cookbook — Advanced patterns](https://github.com/anthropics/anthropic-cookbook)

Already cited. Specifically the `prompt_caching.ipynb`, `tool_use/`, and `multimodal/` notebooks teach production-grade SDK usage.

---

### Deployment

#### [BentoML/BentoML](https://github.com/bentoml/BentoML)

| Stars | ★ 8k+ |
|---|---|
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Serve any ML/LLM model as a production API. Docker + serving framework.

**Best for**: Wrapping your agent into a deployable service.

---

#### [LangServe](https://github.com/langchain-ai/langserve)

**What it teaches**: Deploy LangChain apps as REST APIs. FastAPI under the hood.

**Best for**: Quick deployment of LangChain-based agents.

---

#### [vLLM](https://github.com/vllm-project/vllm)

| Stars | ★ 79k+ |
|---|---|
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: High-throughput LLM serving. Run open-source models in production.

**Best for**: Self-hosting open-source LLMs (Llama, Qwen, etc.) instead of paying API.

---

### Production Case Studies

#### [WenyuChiou/WAGF](https://github.com/WenyuChiou/WAGF)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Production-grade governance layer for LLM-driven agent-based models. 6-stage validation pipeline catches hallucination, logical drift, unsafe state mutation. Multi-LLM ablation. 3 reference implementations.

**Best for**: Studying how production LLM-agent systems handle reliability concerns.

---

## ✅ Self-Check After Stage 7

Can you:
- [ ] Design a multi-agent system with explicit coordination protocol
- [ ] Set up automated eval pipeline running in CI
- [ ] Connect observability (tracing) to a production agent
- [ ] Use prompt caching to cut costs by 50%+ on a real workload
- [ ] Deploy an agent to a cloud service (any provider)

If yes → you've completed the main path. Choose a [specialized branch](../README.md#the-7-stage-learning-map) or contribute to this repo.

## 💡 What's Next

You now have foundational competence. The next 6-12 months should be about:
1. **Pick one production system** to take from prototype → production
2. **Contribute to upstream** (LangGraph, AutoGen, MCP servers, Anthropic cookbook)
3. **Read papers** — agent research is moving fast
4. **Build something visible** — open source a real tool, not another tutorial
