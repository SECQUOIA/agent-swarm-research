# Targeted verification

Date: 2026-10-03. Checks cover this continuation only. No project-wide
verification was run and no CI status or logs were inspected. The reviews
record additional checks performed by the independent agents.

## Mathematics and exact reference implementations

These commands were actually run from the repository root and passed:

```sh
python3 research-20261003-adaptive-obbt/theory/check_effort_allocation.py
python3 research-20261003-adaptive-obbt/theory/check_constrained_obbt.py
code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/theory/check_remaining_benefit.py --with-lp-proposals
code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/theory/check_certified_driver.py
python3 research-20261003-adaptive-obbt/reviews/check_theory_review.py
```

| Check | Result and meaning |
|---|---|
| Effort allocation | 19,683 ledger traces and 8,000 scheduling/rescue traces passed. These check accounting, not solver speed. |
| Constrained theory | Exact examples for C1–C5 passed, including 141 nonlinear graph-repair cases and floating-input rejection. |
| Remaining benefit | Twelve groups passed. Six of eight automatic-discovery fixtures produced exactly verified certificates; two contracting fixtures correctly remained inconclusive. |
| Certified driver | Ten workflow cases and five invalid-proof cases passed. Contracting examples retained positive residuals instead of claiming finite closure. |
| Independent theory diagnostic | Scope counterexamples, 3,360 nested McCormick points, 65 cutoff LPs, 1,089 cross-region pairs, and 50 matrix partial sums passed. The final independent review also records arithmetic rejection and three separate driver cases. |

The checked finite examples supplement the proofs. They do not establish
unstated uniform sensitivity or feasible-repair assumptions. Numerical proposal
failure is not a mathematical certificate of infeasibility or no future benefit.

## Solver and experiment regressions

After the final added regressions, this command passed **31 tests**:

```sh
code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261003-adaptive-obbt/solver/test_adaptive_obbt.py \
  research-20261003-adaptive-obbt/reviews/test_solver_review.py \
  research-20261003-adaptive-obbt/experiments/test_models.py \
  research-20261003-adaptive-obbt/experiments/test_analyze.py \
  research-20261003-adaptive-obbt/experiments/test_run.py
```

The thirteen author tests and nine independent solver tests cover conservative
dual bounds, graph containment, local and integer bound application, witness
validation, objective cancellation, trigger state, failure handling, actual SCIP
operation, and model-construction time exhausting the solve budget. Nine
experiment tests cover model interpretation, original-model validation, scoring
all outcomes, and preserving incomplete attempts during resume.

The independent public-model check was also run before outcomes existed:

```sh
python3 research-20261003-adaptive-obbt/reviews/check_source_models.py
```

It matched all twelve archived original OSiL models to the normalized inputs,
including bounds, variable types, objective, and rows at five diagnostic points
per model. At that stage it checked no returned incumbents. The completed
campaign audit and document checks are recorded below and in the owning reports.

## Completed campaign audit

The independent reviewer ran:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/check_source_models.py --campaign campaign-01
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python research-20261003-adaptive-obbt/reviews/check_campaign.py campaign-01
```

Both passed. The direct XML evaluator checked all 69 returned public-model
incumbents against the twelve original OSiL models. The separate campaign
checker confirmed all 120 planned model/seed/policy combinations, source and
input hashes, configuration, full logs, solved counts, penalized times, and
actual process totals without importing the experiment analyzer.

All three arms solved 14 of 40 cases. No invalid incumbents, process failures,
objective mismatches, inconsistent primal/dual bounds, or plugin exceptions
were found. Four added-policy runs encountered unsupported unbounded boxes
and retained native search. Seventy-eight solver calls exceeded the nominal
ten-second budget; the maximum excess was 0.0930 seconds, and actual elapsed
costs remain in the results. Process startup and validation are also retained.

The [independent review](reviews/solver-review.md) gives a scoped pass for the
implementation and evidence. The experiment supplies no demonstrated net
runtime benefit for the additional policies.

## Integrated report

The document owner ran the following from `document/` after integrating the
final outcomes:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n 'Warning|Overfull|Underfull' main.log
pdfinfo main.pdf
pdftotext -layout main.pdf main.txt
pdftoppm -f 1 -l 1 -r 110 -png -singlefile main.pdf /tmp/adaptive-obbt-report-title
pdftoppm -f 19 -l 19 -r 110 -png -singlefile main.pdf /tmp/adaptive-obbt-report-results
```

The final 24-page PDF builds successfully, has an empty author field, and
contains no undefined references, undefined citations, or overfull boxes.
One bibliography entry produces two harmless underfull-box warnings. The
extracted text contains the final outcome values without unresolved-reference
markers. Visual inspection of the title/abstract and results pages found no
clipping or overlapping text. The temporary extracted text was removed.
The PDF's primary table uses full process times, matching the experiment report.

The root review also checked PDF metadata, the final build log, the absence of
unfinished placeholders in the current reports, and local document links.
All 75 checked local links across 27 authored Markdown and LaTeX files resolve.
The [document record](document/README.md) lists the resolved transcription
findings and the separate constrained-theory author's check.

## Interpretation

The exact checker validates rational objects and its stated LP proof contracts.
The SCIP implementation uses numerical original-model feasibility and SCIP's
numerical solution contract. Its conservative bound arithmetic does not turn
the complete native search into an independently certified solve.

The [theory review](reviews/theory-review.md) and
[solver review](reviews/solver-review.md) record resolved defects and remaining
scope limits. Source fixes made before the comparative snapshot are part of
that snapshot. A later change to the live experiment runner preserves partial
attempts on resume; it changes neither the frozen measured policy nor the
uninterrupted campaign's outcomes.
