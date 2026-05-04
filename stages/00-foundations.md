# Stage 0 — Foundations

⏱ **Time estimate**: 1-2 weeks (~5-15 hours, can skip if you have these)

## When to skip this stage

If you can:
- Write a Python function that calls a public API and parses JSON response
- Use git to clone, commit, push, and resolve a basic merge
- Use the command line on your OS (cd, ls, mkdir, run a script)
- Read a YAML / JSON file without confusion

→ **Skip directly to [Stage 1](01-llm-basics.md)**.

If you can't, work through this stage. Don't skip — every later stage assumes these.

## 📌 Learning Goals

- Write Python: functions, classes, async/await basics
- Use git: clone, branch, commit, push, basic conflict resolution
- Use REST APIs: send GET/POST, parse JSON, handle auth headers
- Read & write YAML and JSON

## 🛠 Hello-X

- **Hello Python** — write a Python script that calls https://api.github.com/users/torvalds and prints follower count
- **Hello git** — clone any public repo, make a commit, push to your fork
- **Hello YAML** — read a `.yaml` config file in Python, modify a value, write it back

## 🎯 Curated Resources (not full projects, just learning material)

### Python
- [**Python Crash Course**](https://github.com/ehmatthes/pcc_3e) — book + exercises (paid book, free exercises)
- [**Real Python tutorials**](https://realpython.com/) — high-quality free articles
- **datawhalechina/learn-python (zh-CN)** — Chinese-language Python intro

### Git
- [**Pro Git book**](https://git-scm.com/book/en/v2) — free, full-length reference
- [**Atlassian Git Tutorials**](https://www.atlassian.com/git/tutorials) — workflow-focused
- [**Oh Shit, Git!?!**](https://ohshitgit.com/) — when things go wrong

### REST APIs
- [**MDN — HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP) — protocol fundamentals
- [**Postman Learning Center**](https://learning.postman.com/) — API exploration tool

### YAML / JSON
- [**YAML official site**](https://yaml.org/) — spec
- [**JSON crash course**](https://www.json.org/json-en.html) — official quick guide

## Why this stage exists

Most "AI agent" tutorials assume you already have these. If you don't, you'll get blocked at random places (tools requires async; configs are YAML; SDK setup needs git). One week investing here saves 10+ weeks of frustration later.
