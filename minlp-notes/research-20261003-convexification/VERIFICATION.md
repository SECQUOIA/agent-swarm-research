# Targeted verification

Only this topic's implementation, reviews, experiment harness, and document
were checked locally. No project-wide verification or CI inspection was run.
Internal independent review is distinct from external peer review and formal
verification.

The primary agent ran this combined targeted command:

```sh
PYTHONPATH=research-20261003-convexification:research-20261003-convexification/solver \
  code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261003-convexification/solver/test_*.py \
  research-20261003-convexification/theory/test_*.py \
  research-20261003-convexification/reviews/test_*.py \
  research-20261003-convexification/experiments/test_*.py
```

Result on 2026-10-03: **250 tests and 8 subtests passed**, in 5.34 seconds.
An earlier attempt with only the topic on `PYTHONPATH` stopped during collection
because one test still used a bare module import. Its owner corrected the
package import concurrently; no implementation failure was reported by that
attempt. The completed run above includes the correction.

The component reviews record additional exact analytic diagnostics, source
hashes, findings, and their resolutions:

- [Model and domain review](reviews/model-review.md).
- [General polytope support review](theory/polytope-review.md).
- [Original-row integration and replay review](reviews/integration-review.md).
- [Separation review](reviews/separation-review.md).
- [Experiment review](reviews/experiment-review.md).
- [Row theorem and rounding proof review](literature/row-proof-review.md).

These counts overlap with the combined test suite and must not be added to it
as though they were disjoint tests.

The 282-run campaign uses its archived source snapshot. Its final independent
replay checked all 123 recorded cuts and bound 278 complete model records to
their original inputs. Four worker failures have unknown cut logs and remain
explicit. The metric audit checked 156 archived source hashes and 271 returned
incumbents, with no original-model check failure or reference-bound conflict.

The current integration also has defensive infinity-sentinel and heuristic
evaluation checks made during freeze coordination. The campaign then exposed
large-model recursion failures and discovery continuing past its intended
budget. The repair uses sparse polynomial generators, retains unsupported
nonrational or oversized terms in the nonlinear remainder, and checks the
existing deadline between discovery steps. No partial discovery is presented
as a completed structural analysis. The original records remain unchanged;
a separately frozen, matched 75-job supplement validates the affected cases.
All 75 jobs completed with no worker errors or unknown cut logs. Its final
independent replay passed all 42 recorded cuts, and its metric audit verified
103 frozen source files and all 67 returned incumbents without a reference
conflict. These are a separate correction cohort, not replacement primary
outcomes. See the [replay](experiments/repair-discovery-v1/replay.json) and
[metric audit](reviews/experiment-repair-audit.json).

After these repairs, the primary agent ran the focused regression command:

```sh
PYTHONPATH=research-20261003-convexification \
  code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261003-convexification/solver/test_integration.py \
  research-20261003-convexification/solver/test_row_certificate.py \
  research-20261003-convexification/reviews/test_replay_review.py
```

Result: **81 tests and 3 subtests passed**, in 2.75 seconds. This is a focused
post-repair run, not a second disjoint suite. The independent reviewer approved
integration source SHA256
`128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210`
before the supplement. Single symbolic calls can still overshoot the soft
deadline; the repair prevents continuing sequential discovery after expiration.

The independent reviewer subsequently ran:

```sh
code/minlp_solver_lab/.venv/bin/python \
  research-20261003-convexification/reviews/test_replay_review.py
```

All seven tests passed in 1.882 seconds, including the final regression for
tamper controls on a valid cut with no nonzero columns. This later checker-only
fix does not change either solver snapshot. Its final bytes and SHA256 are
archived in [replay-final.py](reviews/replay-final.py) and the
[provenance record](reviews/replay-final-provenance.json).

The primary agent also ran the scoped whitespace check below; it passed:

```sh
git diff --check -- README.md research-20261003-convexification
```

The report's build, evidence links, and final source hashes are recorded in
[document/VERIFICATION.md](document/VERIFICATION.md) and the independent
[document review](reviews/document-review.md).

The primary agent built the final report with:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  research-20261003-convexification/document/main.tex
```

The command exited successfully. The final PDF has 25 pages; its log has no
undefined references or citations, warnings, or overfull/underfull boxes.
The primary agent also rendered and visually checked the title/abstract page
and the repair-results page (pages 1 and 20). Both were legible and unclipped.
