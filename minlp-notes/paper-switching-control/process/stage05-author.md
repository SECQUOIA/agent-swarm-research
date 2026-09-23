# Stage 5 author handoff

Stage 5 is complete for independent review. The author has stopped manuscript
and verification changes after this handoff; no stage acceptance is asserted.

## Manuscript

New `sections/10-instance-algorithms.tex` and
`sections/11-transfer-and-coarsening.tex` are included by `main.tex`.
They appear as Sections 13–14, beginning on p.40 of the 48-page draft.
Three primary-source bibliography entries were added. All accepted
Sections 01–09 and `macros.tex` are byte-for-byte identical to
`stage04-accepted`; no accepted mathematics, original research source, or
frozen snapshot was changed.

The instance section covers the repository's one-switch algorithm, crossing
queries, arbitrary-prefix residual completion, subset assignment, fixed-budget
enumeration, all complexity and bit-complexity claims, minimum dwell on
maximal runs, unary-restriction scope, and the role candidate-label lemma.
It further develops a complete exact continuous solver through word/time-cell
LP enumeration and bounded-polytope rational vertex enumeration. The latter
is a small-instance verification method with explicit combinatorial cost,
not a claim to a fast practical continuous solver.

The transfer section proves supported integral-prefix rounding, chronological
switch preservation, strict instance transfer, binary nonuniform transfer,
and sharpness of the universal coefficient. It resolves the old minimax
comparison limitation using accepted exact cell averaging and an attained
grid maximizer; the strict minimax inequality is not obtained by taking an
arbitrary supremum of pointwise strict inequalities.

The new certified-coarsening development produces actual schedules and
rigorous additive intervals using exact nonaligned integration. It explicitly
distinguishes piecewise-constant input inference from a general measurable
control's actual coarse integral oracle, continuous feasibility from nested
fine-grid feasibility, exact quantized-data optimization from an original
input perturbation certificate, and strict from clipped lower endpoints.
The root's useful half-width special cases are included. The root also
suggested the binary odd-grid dwell obstruction; it is proved and checked,
showing persistent constrained discretization gaps even under refinement.

## Verification

`verification/stage05/run_checks.py` passes using only Python's standard
library. All 30 bundled original hashes match. Newly bundled unchanged files
are `rounding.py`, `check_rounding.py`, `check_rounding_review.py`,
`check_fixed_budget_review.py`, and `check_grid_transfer_review.py`; their
source paths and hashes were appended to the existing provenance manifest.

Historical verification freshly reproduced:

- 530 exact one-switch comparisons, 44 dwell comparisons, 90 arbitrary-prefix
  checks, and 110 block/budget comparisons in the original check script.
- 3776 independent enumeration/crossing checks, 194 partitions, 156 budget
  checks, and 2097 arbitrary-prefix completions in the separate review checker.
- 729 exhaustive microcontrols and 40 nonuniform controls, 3836 budget
  comparisons, 3139 partitions, 100 candidate-set cases, and 608 dwell cases
  including 52 infeasible cases in the fixed-budget reviewer checker.
- 8819 exhaustive original controls, 22065 supported prefix witnesses,
  500 rational randomized controls, 56 sharpness-family cases, and 200 binary
  nonuniform cases in the transfer reviewer checker.

The new checker evaluates every coarse word against the original fine input
on a common refinement in 48 nonuniform input/budget cases. Independent
nested-grid enumeration checks the certificate bounds. It also checks exact
nonaligned masses, both clipping conventions including equality at zero,
epsilon rounding and invalid input rejection, four quantization bounds, and
four dwell-refinement examples.

Nine continuous instances are solved by complete rational enumeration and
their schedules checked through separate direct integration. Cases include
full and one-sided objectives, switches at input boundaries, repeated modes,
zero-length blocks, and a zero-switch case. For uniform three-mode one-cell
input with two switches, the exact full optimum is 1/6 and the exact
one-sided optimum is 8/57; this detects objective confusion and exercises
k>N. The three-cell pure word 010 is reproduced exactly with a disconnected
repeated mode. A lower-dimensional rational polytope is also tested.

The entire suite was rerun from `/tmp/cia-stage05-relocated`, with process
history and build artifacts omitted. Its exact JSON summary agrees with the
workspace summary. `README.md` documents every API convention, command,
complexity limitation, and log/snapshot distinction. Source PDFs and external
Python packages are not required.

## Sources and presentation

The source record verifies Bestehorn–Kirches Corollary 2.7 on p.2,
Bestehorn et al.'s established exact graph algorithm and bibliographic
metadata, Zeile Section 6.4.3 pp.78–80, and the source's half-mesh arguments
on Sager–Zeile p.615 and thesis p.139. Download hashes are recorded; original
PDFs were kept in a temporary directory and are not redistributed. The
manuscript credits the matching and enumeration ingredients and does not
claim publication priority for standard dynamic programming.

The final 48-page manuscript builds with `latexmk` without unresolved
references, undefined citations, or overfull/underfull warnings. A relocated
clean build also passes. The author rendered and visually inspected pp.40–48;
new displays, theorem blocks, proof breaks, and bibliography are legible and
inside the margins. Page images and contact sheets are verification artifacts.

## Review scope and remaining stage allocation

Review all mathematical quantifiers, exact arithmetic, repeated labels,
zero-length continuous blocks, active-constraint completeness, clipping and
quantization contracts, dwell counterexample, and source interpretation.
The comprehensive claim coverage list has been appended to
`process/claim-coverage.md`. Application-data benchmarks, comparative
computations, the full introduction/abstract, and overall synthesis remain
assigned to stage 6. No stage 5 theorem depends on an unresolved conjecture.
