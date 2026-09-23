# Stage 6, round 1 — independent review 1

**Verdict: no major issues; accept after two minor documentation corrections.**

Reviewed the frozen `stage06-round01` manuscript, its tables/main/bibliography
and README, the author record and validation manifest, and the changed flat
oracle and strong-baseline source/tests. I did not consult other current-round
reviews, edit manuscript or production code, or reuse the author's verification
helpers in my independent tests.

## Enumerated findings

1. **S06R01-R1-F01 — minor: the printed reproduction command has two trailing
   backslashes instead of one.**

   Location: `sections/08-computation.tex`, line 328, inside `verbatim`.

   LaTeX verbatim prints both characters literally. In a shell the first
   backslash escapes the second; neither continues the newline. The first
   command therefore lacks its required `--output` option and receives a
   literal backslash argument, while the next line is interpreted as a new
   shell command. Replace the two trailing backslashes with one. The README's
   command already uses the correct form. This is a local reproducibility
   documentation defect, not a defect in the benchmark results.

2. **S06R01-R1-F02 — minor: specify that three-label recovery also uses inverse
   bases.**

   Location: `sections/08-computation.tex`, lines 40–42; corresponding prose
   in `process/stage06-author.md`, implementation paragraph.

   The text says three labels use sixteen circuits and repairs, followed by
   “larger label sets use finite inverse bases.” This suggests that inverse
   bases start above three labels. In fact `flat_chain.py`, lines 338–348,
   enumerates `_reduced_bases(a)` for every `a>=3` successful decomposition
   query. Clarify the distinction: three labels use the sixteen feasibility
   circuits and coefficient repairs; recovery at **three or more** labels
   uses inverse bases. `FLAT_CHAIN.md` states this correctly already. No code
   or theorem change is needed.

## Implementation correctness audit

The production flat oracle correctly restricts profile construction to labels
observed anywhere, while retaining every original simplex weight. Its merged
weight is exactly one minus the observed-label sum. Label slots, observation
classification, and separate bypass observations are consistent with the
manuscript's indexing conversion. Deduplication occurs before classifying a
state as doubly observed.

The reduced endpoint rows are faithful to the proof. Zero-normal rows are
checked; same-normal right-hand sides are minimized with their original affine
expressions retained. Explicit/residual bounds provide all required interval
groups for the direct one/two-label recovery. The larger-dimensional inverse
bases include all full-rank bases and do not impose an obsolete profile-sum
equality. At three labels, the code's cut sign and selected gadget coefficient
agree with both proved bypass repairs. The repairs preserve exact violation
after the aggregate flow checks.

For decomposition, observed-label groups use their own state weights, and the
default stores one weighted group profile/flow. `flow(j)` returns the same
normalized default for each positive unobserved original label. Multiplying it
by each original weight gives the required proportional refinement; a positive
original weight cannot lie in a zero-weight default group. Zero observed
weights force their entries to zero. The `a=0` path returns the aggregate flow
as the normalized common default. Dense compatibility accessors are optional
and are not used during compact construction.

The new baseline systems are mathematically appropriate. Full/global
optimization retains all original `y` coordinates, objectives and additional
row coefficients; state merging affects only flows and their weight equations.
The block/Kronecker signs agree with the outgoing-minus-incoming convention.
For point membership, exact zero-weight detection and observed-state bound
checks precede deletion. With two positive states, the lower/upper bounds
correctly combine the first state with `x-f`, including observations in either
state and conflicting fixed values. With one positive group, the direct check
is sufficient after the aggregate domain check.

I found no conflation of these numerical baseline answers with exact membership
certificates. The aggregate balance tolerance is disclosed, and solver statuses
other than zero/two raise failures. Fixed-weight independent optimization
preserves unobserved-label objective contributions and is only used without
coupling rows. Adding the budget is correctly described as intersecting the
component hull with a row, not as convexifying the additionally constrained
graph exactly.

## Independent checks

All **82** manifest dependency hashes matched before testing, including the
changed code and raw measurement data. My evidence is confined to
`verification/reviewer1/stage06-round01/`.

The independently written `check.py` generated exact mixtures with arbitrary
gadget/bypass observations, nonconsecutive observed labels, zero weights,
zero observed labels, and up to 53 original labels. It checked compact group
sizes, exact normalized state feasibility, aggregate reconstruction, every
observed product, and shared normalized defaults. Perturbed points were
handled by either another exactly checked decomposition or a cut optimized
exactly over all path/simplex vertices using the chain's separable path
objective. Results:

- 71 exact decompositions;
- 29 strictly violated, exactly globally valid cuts;
- 288 numerical membership comparisons covering full/global merging and
  enabled/disabled two-state reduction;
- 32 independent optimization comparisons with a directly assembled convex
  combination of actual path/simplex vertices, checking free and fixed `y`,
  nonzero costs on unused labels, and two coupled `x/y/z` rows.

All passed. The last two counts are explicitly numerical comparisons, not
exact optimality certificates. The exact checks do not call the author's
decomposition or cut-audit helpers.

## Computational claims and presentation

I inspected benchmark construction, timing, status checks and out-of-timing
audits. The full/global objectives and additional rows are shared correctly.
Membership-only and recovery-inclusive calls are timed as distinct workloads.
Raw observations/weights and the targeted controls match the section's
description. The independent-network baseline is excluded from the budget
control. All numerical optimization methods are compared to the same objective
and fixed weights.

I independently recomputed **483** stored timing summaries from the raw
five-run records; every minimum, median and maximum matched. The highlighted
size counts follow directly from the formulations: 5,675/644 variables for
full/global sparse optimization, 7,279 for both all-labels-observed baselines,
and 2,050/1,025 variables for the two positive-state/one-flow 512-gadget
membership systems. The table interpretations preserve the negative results
about global merging and stronger boundary-face LPs. They do not overstate
five runs on a shared host as a universal speed ordering or industrial result.

The two-supplier interpretation fits the arbitrary-orientation parallel-path
theorem: each supplier-to-demand pair forms one undirected length-two path,
with the second arc traversed in reverse. Its warning about additional budgets
is appropriate.

A private snapshot copy compiled to 45 pages, with no final LaTeX warnings or
overfull/underfull boxes. Existing mathematical sections remain unchanged and
their interfaces fit the implementation discussion.

## Limitations

I did not rerun the full timing study: timings are host-dependent, and the
independent raw-summary and hash checks address the reported arithmetic
without modifying the frozen experiment. I did not re-audit every unchanged
general compressed solver routine or every bibliographic metadata field in
this round. No implementation correctness defect was identified in the changed
paths; the two findings concern accurate instructions and algorithm description.
