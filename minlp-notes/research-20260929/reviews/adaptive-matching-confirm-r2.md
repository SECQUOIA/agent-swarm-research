# Confirmation review, round 2: `theory-decomposition/adaptive-matching.md`

Date: 2026-09-30. Independent referee. I did not write the note or any of
its earlier reviews
([`adaptive-matching-review.md`](adaptive-matching-review.md),
[`adaptive-matching-confirm-r1.md`](adaptive-matching-confirm-r1.md)). I
checked whether the revision fixes the three problems raised in
`adaptive-matching-confirm-r1.md`, judged the reviser's refusals, and
looked for claims that the revision made stronger. My scripts and logs are
in
[`adaptive-matching-confirm-r2-checks/`](adaptive-matching-confirm-r2-checks/).
Only targeted checks were run. No project-wide verification was run and no
CI results were consulted.

Labels. **By hand**: I redid the argument. **Float**: double-precision
computation, not certified. **Reproduced**: I reran the authors' script and
got output identical to the logged output. Nothing was checked in exact
arithmetic or in Lean.

## 1. Verdict

All three problems are fixed. The fixes narrow claims or add hypotheses;
none makes a claim stronger. The three refusals are justified. I found no
remaining problem that needs a change. Verdict: **verified**.

## 2. The three problems

| # | Problem | What the note says now | My check | Status |
|---|---|---|---|---|
| 1 | Shin–Anitescu–Zavala: wrong pages 1110–1136 | Section 9 (line 1389): "SIAM J. Optim. 32(2) (2022) 1156–1183, doi:10.1137/21M1391079, arXiv:2101.03067", with a note that the pages and DOI were checked against Crossref in round 2 and that the first revision gave wrong pages. Revision item 4 (lines 1623–1631) gives the same data, keeps 1110–1136 marked as corrected, and says the round-1 check missed the pages. Revision item 10 records the change. | Crossref for DOI `10.1137/21M1391079` (`crossref_shin.log`): title "Exponential Decay of Sensitivity in Graph-Structured Nonlinear Programs", authors Sungho Shin, Mihai Anitescu, Victor M. Zavala, SIAM Journal on Optimization, volume 32, issue 2, pages 1156–1183, issued 2022-05-31. The arXiv abstract page of 2101.03067 (`arxiv_2101.03067.log`) has the same title and authors and `citation_doi` 10.1137/21M1391079. `grep` over all `.md` files of the repository: "1110–1136" now appears only in the two places that mark it as corrected (lines 1626 and 1712) and in the round-2 review. No other note in the repository gives pages for this paper (`../literature/decomposition-bb-prior.md` gives none). | fixed |
| 2 | Proposition 6 stated "per separator dimension" | Summary item 4 (lines 144–149): "costs `sqrt(n)` cells per edge per halving (proved for one-dimensional separators)", followed by "*Conjecture, not proved:* for separators of dimension `w >= 2` the cost is `sqrt(n)` per separator dimension, that is `n^{w/2}` cells per edge per halving". Section 5 opening (lines 791–793) and item 2 (lines 806–811) say the same; item 2 names "rule `bd` on a quadratic path with one-dimensional separators". The *Scope* paragraph (lines 829–837) says the proof covers the quadratic path (any `n >= 25`, `0 < \|b\| < 1`), whose separators are single variables and whose cells are intervals, and that it does not cover `w >= 2`. Status row: "proved (one-dimensional separators only)". | By hand, I reread the proof. Each separator is the scalar `s_t`; cells are intervals `[d - r, d + r]`. The bracket bound `g(D) >= \|p_t\| r^2 - (q_t/(2n))(2d^2 + r^2)` follows from averaging `A` over the two endpoints and evaluating `B` at `d` (the affine parts cancel). A final cell then has `K_t r^2 <= d^2 + eps/q_t` with `K_t >= n theta_t - 1/2 >= (n-1)/2` for `t <= (n+1)/2`. The counting step gives `r <= 3 rho/sqrt(K_t - 2)` on `[rho, 2 rho]`, so at least `sqrt(K_t - 2)/6` cells per range and `I sqrt(K_t - 2)/12` in total, with `K_t - 2 >= (n-5)/2`. That is `sqrt(n)` cells per covered edge per halving, for one-dimensional separators only. Nothing in the proof counts boxes in two or more coordinates, so the `w >= 2` statement is correctly labelled a conjecture. `grep`: "per separator dimension" now appears only inside the conjecture labels (lines 148 and 836–837, and item 2 at line 809) and in the revision record. Reproduced: `check_bd_qg.py 1e-6` gives output byte-identical to `logs/check_bd_qg.log` (`rerun_check_bd_qg.log`), so the numbers in Section 8.5 and Summary item 4 are unchanged. | fixed |
| 3 | Two restatements of Theorem 2 omit (S) | Summary item 5 (lines 158–159): "algorithmic for path decompositions with (S) (`∇F(x*) = 0`)". Status row (line 226): "proved (path decompositions, with (S) `∇F(x*) = 0`)". Also Summary item 3 (line 100), which the review did not raise: "For a tree decomposition (still with (S))". | By hand against the statement of Theorem 2 (line 541: "Assume the setting of Section 1.1 with (QG), (L^{1,1}), (U^q) and (S)") and Remark 3.3 (line 707: "For any tree decomposition with (QG), (L^{1,1}), (U^q) and (S)"). The added text matches both. I read all 40 mentions of "Theorem 2" (`grep -n`). Every statement of its scope now names (S) and the path restriction: Summary items 1, 3 and 5, the Significance paragraph, the status table, Section 3.2 (line 633), Remark 3.3 and Section 7. The remaining mentions are proof steps, numerical comparisons on families where (S) holds (`x* = 0` or interior), the novelty assessment of Section 9, and the round-1 revision record. | fixed |

## 3. The refusals

1. **The case `w >= 2` of Proposition 6 was not proved.** Justified. The
   round-2 review asked for a conjecture label, not a proof. The label is
   present in the Summary, Section 5 item 2 and the *Scope* paragraph, and
   the status table says "one-dimensional separators only".
2. **The round-1 line "Not changed: Lemma 1, Theorem 2 for paths, ..." was
   left as written.** Justified. It records what the round-1 revision left
   unchanged. It does not state the scope of Theorem 2, and the round-2
   entry 12 explains why it was kept.
3. **No edits to the files the root maintains, to
   `../literature/decomposition-bb-prior.md`, or to review files.**
   Justified. The task forbids editing the root files. My `grep` found no
   other file in the repository with the wrong pages. The literature audit
   cites the paper without pages (line 841), so it needs no change.

## 4. Checked for statements made stronger

None found. The round-2 changes are:

- the corrected pages and the added DOI;
- the Proposition 6 claim narrowed to one-dimensional separators, with the
  `w >= 2` statement moved to a labelled conjecture (Summary item 4,
  Section 5 opening and item 2, *Scope*, status table);
- (S) added to Summary items 3 and 5 and to the Theorem 2 status row;
- bookkeeping: the header status line, the cited-notes list, the "Round 1"
  and "Round 2" subsections of the revision record, and the new table in
  Section 11.

Proposition 6, its proof and all numbers are unchanged. File timestamps
agree with this: `check_bd_qg.py` (21:10) and `logs/check_bd_qg.log` (21:17)
are older than the round-2 review (23:19). The reviser's rerun output is
in `/tmp/check_bd_qg_rerun_r2.log` (23:26), as Section 11 says.

## 5. Remarks that need no change

- **"Per edge" in Summary item 4 and Section 5 item 2.** The proof covers
  the edges `t <= (n+1)/2`, where `theta_t >= 1/2`. Float
  (`per_edge_bd.log`, `b = 0.8`, `eps = 1e-6`, the note's own functions):
  the last edge `t = n` uses one cell (`u_n = 0`, so `K_n = 0`), while
  edges `n - 2` and `n - 1` still use 5.4–6.4 `sqrt(n)` cells. Edges
  1, `n/4`, `n/2` and `3n/4` use 8.1–12.0 `sqrt(n)`. So "per edge" holds on
  all edges except the last in these runs. It is proved for the covered half
  of the edges, and on average. The statement of Proposition 6 is precise
  ("every edge `t <= (n+1)/2`"), and the Summary wording is an order
  statement that the round-2 review suggested. I do not ask for a change.
- **Section 9 assessment (line 1427)** lists "a certificate-producing
  algorithm with the instance-dependent count ... (Theorem 2)" among
  things not found in the literature, without repeating (S) and the path
  restriction. It reports a search result and does not restate the
  theorem's scope. The Significance paragraph, which makes the same point,
  names both. No change needed.
- The Crossref and arXiv outputs of the reviser's round-2 commands were not
  kept (Section 11 says so). My copies are in the checks folder.

## 6. Commands run

From `research-20260929/reviews/adaptive-matching-confirm-r2-checks/`
unless stated, with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1` and Python 3.13. The machine
is shared (load about 25 on 36 cores).

| Command | Log | Result |
|---|---|---|
| `curl -s https://api.crossref.org/works/10.1137/21M1391079` with a short Python filter | `crossref_shin.log` | SIAM J. Optim. 32(2), pages 1156–1183, issued 2022-05-31; title and authors as cited |
| `curl -sL https://export.arxiv.org/abs/2101.03067` with `grep` for the `citation_*` meta tags | `arxiv_2101.03067.log` | same title and authors; `citation_doi` 10.1137/21M1391079 |
| `timeout 1500 python3 check_bd_qg.py 1e-6` (run in `theory-decomposition/adaptive2/`, 466 s), then `diff` with `logs/check_bd_qg.log` | `rerun_check_bd_qg.log` | byte-identical |
| `timeout 900 python3 per_edge_bd.py` (imports `check_bd_qg.py` unchanged) | `per_edge_bd.log` | per-edge `bd` cell counts for `n = 64, 256` on selected edges (Section 5 above) |
| `grep -rn "1110"`, `grep -rn "2101.03067\|21M1391079"` over the repository's `.md` files; `grep -n` for "Theorem 2", "per separator dimension" and "one-dimensional" in the note | – | as described in Sections 2 and 3 |

I also reread the proof of Proposition 6 (lines 813–872), the statements of
Theorem 2 and Remark 3.3, and the full revision record (lines 1540–1753).
The reruns created no `__pycache__`.
