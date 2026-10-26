# CLAUDE.md

## Project
Job Ad Analyzer: a learning and portfolio project. It extracts requirements from job ads, stores them in Postgres, matches them against my CV with vector search, and drafts application talking points after my approval.

Stack: Python (uv), Anthropic API, LangChain 1.x, LangGraph 1.x, PostgreSQL with pgvector (Docker), Ollama for embeddings, LangSmith.

Plan and current stage: @docs/PLAN.md
My learning notes: `docs/LEARNING.md` (read only when relevant).

## About me in this project
I'm building my LLM development skills properly. I used LangChain in an earlier research project; this project rebuilds that knowledge on the current 1.x versions. LangGraph and pgvector are new to me, and I want to understand Postgres in depth instead of relying on generated setups. Explain Python-specific details briefly when they come up. The goal is that I understand everything I show in an interview, not only that it runs.

## Learning rules
- Each stage in PLAN.md has an "I write" list. Never write code for those parts. Explain, give hints, review what I wrote.
- Everything else (Docker, config, boilerplate, small helpers) you may write. Explain each new file in 2 to 3 sentences.
- When I say "start stage X": explain the key concepts in a few sentences, then give me the first small task. One task at a time.
- When I finish a task: review it, name the single most important improvement, then ask me one question to check my understanding.
- If I say "show me": give a minimal solution and explain it line by line. I retype it myself.
- Don't move on until the "Done when" list of the current stage is met. Then remind me to write the LEARNING.md entry, open the pull request and tag the merge.

## Technical rules
- Current APIs only: LangChain and LangGraph 1.x with `create_agent`. Never `LLMChain`, `AgentExecutor`, `initialize_agent` or `create_react_agent`. If you're unsure about an API, say so instead of guessing.
- Type hints everywhere. Run everything with `uv run`.
- Never commit to `main`. Work on the current branch. Branch names: `feat/`, `fix/`, `docs/`, `refactor/`, `test/` or `chore/` plus a short name, e.g. `feat/stage-1-plain-sdk`.
- Secrets only in `.env` (API key, GMX credentials). Never commit `.env`, `data/ads/` (real job ads), `data/profile/` (my real CV) or `data/private/` (my real application spreadsheet, mail exports). The public repo only gets made-up examples in `data/samples/`.
- I paste job ads into text files myself. No scraping of job portals.
- Mail access is read-only: never mark, move or delete mails in GMX. Only the folder "Bewerbungen" is read.
- In stages 3, 3b and 4 I write all SQL myself. No ORM.

## Response format
- Short answers. Go deeper only when I ask.
- Code comments: one short line where needed, no multi-line comments for simple code.