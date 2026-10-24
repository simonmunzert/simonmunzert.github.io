#!/usr/bin/env python3
"""Sanity check for questions.csv: run `python3 check.py` after editing the database."""
import csv, sys, collections, os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.csv")
rows = list(csv.DictReader(open(path, encoding="utf-8")))
ids = collections.Counter(r["id"] for r in rows)
problems = []
for r in rows:
    qid = r["id"] or "<no id>"
    if ids[r["id"]] > 1:
        problems.append(f"{qid}: duplicate id")
    if not r["session"].isdigit():
        problems.append(f"{qid}: session must be a number")
    if r["type"] == "choice":
        opts = [r[k] for k in ("option_a", "option_b", "option_c", "option_d") if r[k].strip()]
        if len(opts) < 2:
            problems.append(f"{qid}: needs at least two options")
        a = r["answer"].strip().upper()
        if a not in "ABCD"[:len(opts)] or len(a) != 1:
            problems.append(f"{qid}: answer '{r['answer']}' is not one of the options")
    elif r["type"] == "mark":
        n = len(r["code"].split("\n")) if r["code"] else 0
        try:
            lines = [int(x) for x in r["answer"].replace(";", ",").split(",")]
        except ValueError:
            problems.append(f"{qid}: answer must be line numbers like 3 or 2,5"); continue
        if not n:
            problems.append(f"{qid}: mark question without code")
        bad = [l for l in lines if l < 1 or l > n]
        if bad:
            problems.append(f"{qid}: line numbers {bad} outside 1..{n}")
    else:
        problems.append(f"{qid}: unknown type '{r['type']}'")
    if not r["question"].strip():
        problems.append(f"{qid}: empty question")
    if "%>%" in r["code"] or "%>%" in r["question"]:
        problems.append(f"{qid}: uses %>% (use |>)")

per = collections.Counter((r["session"], r["type"]) for r in rows)
print(f"{len(rows)} questions")
for s in sorted({r["session"] for r in rows}, key=int):
    print(f"  session {s}: {per[(s,'choice')]} choice, {per[(s,'mark')]} mark")
if problems:
    print("\nProblems:"); print("\n".join("  " + p for p in problems)); sys.exit(1)
print("No problems found.")
