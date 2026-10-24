# IDS Mock Exam

Practice quiz for the course *Introduction to Data Science* (Hertie School, Fall 2026), sessions 1–8.
Online at https://simonmunzert.com/ids-mock-exam/ (static site, no build step).

- `index.html` + `app.js` + `style.css` – the quiz app (random rounds, exam or practice mode, results with feedback, per-browser history)
- `print.html` – generates a printable paper version of a random set with an answer key (same question pool)
- `questions.csv` – **the question database**. Edit this file to add, change or remove questions; nothing else needs to be touched.
- `check.py` – optional sanity check for the CSV (`python3 check.py`)

## Question format (`questions.csv`)

One row per question. Multi-line cells (code) are quoted CSV cells; any spreadsheet program or `readr::read_csv()` handles them.

| column | content |
|---|---|
| `id` | unique ID, e.g. `s05-03`. Shown to students in the review so they can report errors. |
| `session` | 1–8, used for filtering and the per-session breakdown |
| `type` | `choice` (single choice incl. true/false) or `mark` (mark lines in a snippet) |
| `topic` | short label shown in the review |
| `lang` | label for the code block: `r`, `bash`, `html`, `sql`, `text` (empty if no code) |
| `question` | question text. Inline code in backticks, `**bold**` allowed. For `mark` questions say what to mark. |
| `code` | optional code/snippet for `choice`; the lines to mark for `mark`. One snippet line per text line. |
| `option_a` … `option_d` | answer options for `choice`. For true/false put `True` in `option_a`, `False` in `option_b`, leave c/d empty. Options are shuffled in the app (true/false is not). |
| `answer` | `choice`: letter of the correct option (`A`–`D`). `mark`: 1-based line number(s) of the code, comma-separated (`4` or `2,5`). A mark question counts as correct only if exactly these lines are marked. |
| `explanation` | 1–3 sentences shown as feedback |
| `source` | where the question comes from, e.g. `Quiz 5 · Lecture 5` or `Lecture 7, slide section 'Keys'` |

Reading it in R:

```r
library(tidyverse)
q <- read_csv("questions.csv")
q |> count(session, type)
```

## How rounds are drawn

A round draws `n` questions spread as evenly as possible over the selected sessions, then shuffles them. The draw is seeded, so the URL (`?seed=…&n=…&s=…&mode=…`) reproduces the same set; students can share a link or retake a set. Results are stored only in the browser (`localStorage`).
