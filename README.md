# JobDrop

A job ad analyzer and application tracker for my own job search, built with Python, LangChain, LangGraph and PostgreSQL.

> **Work in progress.** Built in stages; currently at stage 0. The plan is in [`docs/PLAN.md`](docs/PLAN.md), what I learned along the way in [`docs/LEARNING.md`](docs/LEARNING.md).

## What it will do

- **Extract** the requirements of a job ad into structured data: role, languages, frameworks, cloud, seniority, remote share
- **Store** every ad in PostgreSQL and answer questions across all of them, such as "which frameworks show up most in my target ads?"
- **Match** each requirement against my CV and projects with vector search, showing either the evidence or the gap
- **Draft** talking points for an application and wait for my approval before saving them
- **Track** applications, with an import of my existing spreadsheet and an Excel export
- **Read** a mail folder (read-only) and suggest status updates like "rejected" or "interview", applied only after my approval

## Why

- **A real problem:** deciding what to learn next and tailoring each application takes time. This tool answers both from the ads I actually apply to.
- **A learning project:** I'm building my LLM development skills properly on the current versions of the tools job ads ask for. Each stage introduces one new topic and ends in a working version.

## Status

- [ ] 0. Python refresh, keyword baseline
- [ ] 1. Plain Anthropic SDK, tool calling by hand
- [ ] 2. LangChain, structured output
- [ ] 3. PostgreSQL
- [ ] 3b. Application tracking, Excel import and export
- [ ] 4. pgvector and RAG
- [ ] 5. LangGraph with an approval step
- [ ] 5b. Mail folder, classification, status updates
- [ ] 6. Evaluation and LangSmith
- [ ] 7. Deployment

## Tech stack

- Python 3.14, managed with [uv](https://docs.astral.sh/uv/)
- Anthropic API (Claude Haiku 5.5)
- LangChain 1.x, LangGraph 1.x
- PostgreSQL with pgvector, in Docker
- Ollama for embeddings
- LangSmith for tracing and evaluation

## Getting started

Requires [uv](https://docs.astral.sh/uv/). uv installs the right Python version itself.

```bash
git clone https://github.com/MarcelSFelix/JobDrop.git
cd JobDrop
uv sync
uv run jobdrop
```

Further setup (API key, database) will be added with the stages that need it.

## Project structure

```
.claude/CLAUDE.md     rules for the AI tutor in this project
docs/PLAN.md          staged learning plan
docs/LEARNING.md      what I learned per stage
src/jobdrop/          source code
data/samples/         made-up example data
```

## Data and privacy

Real job ads, my CV, my application spreadsheet and mails stay on my machine and are excluded via `.gitignore`. This repo only contains made-up examples. Mail access is read-only: nothing is marked, moved or deleted.

## How it's built

I use Claude Code as a tutor and reviewer. The core part of each stage, listed under "I write" in the plan, I write myself; Claude explains, reviews and writes setup code. Each finished stage gets an entry in the learning log and a git tag.

## Results

Evaluation results (LLM extraction vs. keyword baseline, mail classification accuracy) will be added in stage 6.