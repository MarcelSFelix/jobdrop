# Learning Log

One entry per stage, written by me in my own words after the stage is done. No copying from docs or Claude.

## Template

### Stage N: Title (date)
**What I built:**

**How it works and why it's built this way:**

**What broke and how I fixed it:**

**Still unclear:**

**Interview version (2 to 3 sentences, the way I'd say it):**

---

### Stage 0: Setup and keyword baseline
**What I built:**

**How it works and why it's built this way:**

**What broke and how I fixed it:**

Meaning cannot be read by the keyword baseline. It decides remote by which word appears in the text and by order of the checks

Cases it will get wrong:

- "Hybrid" and "100% Remote" in the same ad. The check order decides.
- "Once a month we meet in the office". It still counts as remote but could be decided as onsite
- "Homeoffice möglich" in a header from the job portal that conflicts with what the job ad says

Added a FULL_REMOTE_KEYWORDS list and check that before hybrid to have a workaround.

**Still unclear:**

**Interview version:**
