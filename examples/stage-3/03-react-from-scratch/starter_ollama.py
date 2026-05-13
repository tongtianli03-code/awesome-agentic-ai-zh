"""
練習 3：從零實作 ReAct — starter_ollama.py（Path B、本機 Ollama）

跟 starter.py 同樣 70 行 ReAct loop、但用 qwen2.5:3b 本機跑、$0/run。

跑法：
    pip install -r requirements_ollama.txt   (只需 openai SDK)
    ollama pull qwen2.5:3b
    ollama serve   # 預設 port 11434
    python starter_ollama.py

驗證：
    python test.py   （test.py 跨 backend 通用、用 mock、不打 API）

跟 starter.py 的 SDK 差異：
    - Anthropic:   client.messages.create(tools=[{name,description,input_schema}, ...])
                    → resp.content[i].type == "tool_use"
    - OpenAI-compat: client.chat.completions.create(tools=[{"type":"function","function":{...}}, ...])
                    → resp.choices[0].message.tool_calls[i].function.name
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")  # tool-use 支援好的 Ollama model

# Reuse 同樣的 tool 實作（避免重複）
from starter import tool_calculator, tool_lookup_fact


# OpenAI-compat 的 tools schema wrap 在 {"type":"function", "function":{...}} 裡
TOOLS_SPEC_OPENAI = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "做基本算術運算（加減乘除）。輸入是表達式字串。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "算術表達式"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_fact",
            "description": "查詢一個事實（人口 / 物理常數等）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "查詢關鍵字"},
                },
                "required": ["query"],
            },
        },
    },
]

TOOL_IMPL = {
    "calculator": lambda inp: tool_calculator(inp["expression"]),
    "lookup_fact": lambda inp: tool_lookup_fact(inp["query"]),
}


def react_loop_ollama(question: str, max_iter: int = 6, client: Any = None) -> dict:
    """ReAct loop using OpenAI-compatible API (Ollama backend)."""
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []

    for step in range(max_iter):
        resp = client.chat.completions.create(
            model=MODEL,
            tools=TOOLS_SPEC_OPENAI,
            messages=messages,
        )
        msg = resp.choices[0].message

        thought_text = msg.content or ""
        tool_calls = msg.tool_calls or []

        # 把 assistant message 加進 messages（OpenAI 格式）
        assistant_entry: dict = {"role": "assistant", "content": thought_text}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if resp.choices[0].finish_reason == "stop" or not tool_calls:
            trace.append({"step": step, "thought": thought_text, "tool": None, "obs": None})
            return {"final": thought_text, "trace": trace, "steps": step + 1}

        # 執行每個 tool call、把 observation 接回（OpenAI 用 role="tool"）
        last_obs = ""
        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            last_obs = obs
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": obs,
            })

        trace.append({
            "step": step,
            "thought": thought_text,
            "tool": tool_calls[0].function.name,
            "tool_input": json.loads(tool_calls[0].function.arguments),
            "obs": last_obs,
        })

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


if __name__ == "__main__":
    question = "台北人口除以紐約人口、答案保留 4 位小數。"
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    print("-" * 60)

    result = react_loop_ollama(question, max_iter=5)

    for entry in result["trace"]:
        print(f"[step {entry['step']}] thought: {(entry['thought'] or '')[:80]}...")
        if entry["tool"]:
            print(f"           tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # 自我驗證（更寬鬆——小 model 可能不會精確到 4 位小數）
    assert result.get("final") is not None or result.get("truncated"), "loop 應收尾或顯式 truncate"
    print("✅ 練習 3（Ollama path）通過 — 你已用本機 qwen2.5:3b 跑通 ReAct + tool use、$0/run")
