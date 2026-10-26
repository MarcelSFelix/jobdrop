# Job Ad Analyzer: Learning Plan

## Goal
A tool for my own job search. It reads job ads, extracts the requirements into structured data, matches them against my CV with vector search, and drafts talking points after I approve them. It also tracks my applications, updates their status from the mails in my GMX folder "Bewerbungen", and exports everything to Excel.

Built in stages so I learn every part properly on current versions, and every stage leaves a working version.

## How I work
- Each stage: work through the source first, then build. I write the "I write" parts myself, Claude reviews (rules in `.claude/CLAUDE.md`).
- Claude Code runs with the Learning output style: in VS Code type `/` in the prompt box → Output styles → Learning. It applies from the next message.
- Claude Code runs in Manual permission mode, so I see every edit as a diff before it's applied.
- Each stage gets its own branch, e.g. `feat/stage-0-python-refresh`; larger stages get one branch per task. Other prefixes: `fix/`, `docs/`, `refactor/`, `test/`, `chore/`. Commit freely on the branch.
- A stage is done when its "Done when" list is met. Then: entry in `docs/LEARNING.md`, pull request into `main` (squash merge), `git tag stage-N` on `main`.
- Only the current stage is planned in detail. The next one gets detailed when I get there.

## Stack
- Python with uv
- Anthropic API (Claude Haiku 5.5)
- LangChain 1.x and LangGraph 1.x
- PostgreSQL with pgvector, in Docker
- Ollama for embeddings (multilingual model, since ads are German and English), optionally for classifying mails locally
- LangSmith for tracing and evaluation
- `imaplib` (Python standard library) for reading GMX, `openpyxl` for the Excel export

## Private data
Never in the repo: `.env` (API key, GMX credentials), `data/ads/` (real job ads), `data/profile/` (my CV), `data/private/` (my real application spreadsheet, mail exports). The public repo only gets made-up examples in `data/samples/`.

---

## Stage 0: Setup and keyword baseline (current)

**Learn:** project setup with uv, typed Python, file handling with `pathlib` and `json`, Pydantic models and validation errors.

**Sources:**
- Python tutorial at docs.python.org/3/tutorial, as needed
- uv docs, "Getting started"
- Pydantic docs, "Models"

**Tasks:**
1. Done: `uv init`, `uv add pydantic`, Python pinned to 3.14. Run the hello function with `uv run job-ad-analyzer`.
2. Add to `.gitignore` (uv already added `.venv`): `.env`, `data/ads/`, `data/profile/`, `data/private/`, `.claude/settings.local.json`.
3. Paste 5 real job ads into `data/ads/*.txt`, German and English mixed. Write 2 short made-up ads into `data/samples/` for the public repo.
4. Write a `JobAd` Pydantic model: title, languages, frameworks, remote, seniority. Pass it a wrong type on purpose and read the error.
5. Write `baseline.py`: reads all ads, finds known languages and frameworks from a keyword list (case-insensitive, whole words only), guesses remote from keywords, writes `data/baseline.json`.

**I write:** everything in this stage.

**Done when:**
- `uv run` on the baseline turns 5 ads into valid JSON
- I can explain what Pydantic does with a wrong type, and why that matters for LLM output
- The baseline stays in the repo: in stage 6 it's what the LLM version has to beat

---

## Stage 1: Plain SDK
Send one ad to Claude with the Anthropic SDK. Then build a tool loop by hand with one tool, `normalize_skill(name)`, that maps different spellings to canonical names from my keyword list.

- **I write:** the API call and the tool loop
- **Source:** Anthropic Academy "Building with the Claude API" (API basics and tool use sections)
- **Done when:** the loop works and I can explain every message in it (tool request, my tool result, final answer)

## Stage 2: LangChain
The same extraction with `create_agent`, the `JobAd` model as structured output, and `normalize_skill` as a tool. Results for all ads go to `data/llm.json`.

- **I write:** the model, the tool, the agent call
- **Source:** LangChain Academy "LangChain Essentials"
- **Done when:** all ads come back as validated `JobAd` objects

## Stage 3: PostgreSQL
Postgres in Docker, using the pgvector image but as plain Postgres for now. Tables for ads, skills, and the link between them. Connect from Python with psycopg.

- **I write:** all SQL (schema, inserts, queries)
- **Source:** PostgreSQL docs, Tutorial part; psycopg docs
- **Done when:** SQL answers "top 10 frameworks across all ads" and "remote ads that mention LangGraph"

## Stage 3b: Application tracking
An `applications` table (company, role, date applied, link, status, last update), linked to the job ad where one exists. Status limited to fixed values (applied, receipt confirmed, interview, rejected, offer, withdrawn). One-time import of my existing `Bewerbungen.xlsx` from `data/private/`; the original file stays untouched. Export generates a new formatted Excel file from the database. No AI in this stage.

- **I write:** the table SQL, the column mapping for the import, the status queries
- **AI may write:** Excel formatting for the export (colors, column widths)
- **Source:** PostgreSQL docs (constraints, dates); openpyxl docs
- **Done when:** all existing applications are imported, the export opens correctly in Excel, and SQL answers "applications with no reply for more than 4 weeks"

## Stage 4: pgvector and RAG
Split my CV and project descriptions into chunks, embed them with Ollama, store them in a vector column, find the best matching chunks for each requirement. Optional: hybrid search with Postgres full-text search.

- **I write:** chunking, embedding calls, the similarity query
- **Source:** pgvector README on GitHub
- **Done when:** for one ad I get a match/gap list per requirement

## Stage 5: LangGraph
Turn the steps into a graph: extract, store, match, draft talking points, pause for my approval, save. State is persisted with a Postgres checkpointer. When I decide to apply, the graph creates the entry in `applications`.

- **I write:** state, nodes, edges, the approval interrupt
- **Source:** LangChain Academy "Introduction to LangGraph"
- **Done when:** the run pauses for approval, can be resumed with approve, edit or reject, and an approved application shows up in the table

## Stage 5b: Inbox
Read only my GMX folder "Bewerbungen" and turn new mails into status updates.

1. **Read:** IMAP, read-only (nothing marked as read, moved or deleted). Headers first, full text only for candidates. Remember processed mails so none is handled twice.
2. **Pre-filter with rules, no AI:** sender domains of companies I applied to, known applicant-tracking systems (Personio, Softgarden, Workday and similar), keywords (Bewerbung, Absage, leider, Vorstellungsgespräch, interview).
3. **Classify:** rejection, interview invitation, receipt confirmation, question, irrelevant. Structured output, optionally with a local model via Ollama so mail content stays on my machine.
4. **Match** the mail to an application (company and role from sender and body). If unsure, ask me.
5. **Approve:** proposed status change → approval interrupt → database update → fresh Excel export.

Setup: enable "POP3 und IMAP Zugriff erlauben" in the GMX settings; app-specific password if two-factor login is on; credentials only in `.env`.

- **I write:** the IMAP read loop, the filter rules, the classification schema, the matching logic, the graph wiring
- **Source:** Python docs for `imaplib`; LangGraph interrupts from stage 5
- **Done when:** a run over the folder proposes correct status updates for new mails, no mail is changed in GMX, and approved changes appear in the Excel export

## Stage 6: Evaluation and LangSmith
Label 20 ads and about 30 real mails by hand. Measure precision and recall per field for the ads, compare the stage 0 baseline with the stage 2 LLM version. For mails, measure classification accuracy and how many relevant mails the rule filter catches. Trace runs in LangSmith.

- **I write:** the labels and the metric code
- **Source:** LangSmith docs (tracing, evaluation)
- **Done when:** a results table for ads and mails is in the README

## Stage 7: Deployment
Small web UI or API, Docker Compose on the Oracle server, rate limit per IP, max input length, spending limit at the API provider. Optional: scheduled inbox check. The public demo uses a sample CV and made-up mails, never my real data.

- **I write:** the rate limit logic
- **Source:** as needed
- **Done when:** the public URL works, the rate limit is tested, and the README explains architecture and results

## Optional: Qdrant comparison
Run the stage 4 search against Qdrant and compare results and setup effort.