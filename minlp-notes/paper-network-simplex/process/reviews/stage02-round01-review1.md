# Stage 2, round 1 — independent review 1

**Verdict: accept this stage. No major or minor defects found.**

I reviewed the frozen `stage02-round01` snapshot, all of
`sections/02-compression.tex`, and the integration changes against Stage 1.
I used the accepted foundations as dependencies, while independently checking
the new proofs. I did not consult other current-round reviews or edit the
manuscript.

## Enumerated findings

1. **S02R01-R1-F00 — no actionable finding.** The new statements, exactness
   arguments, size bounds, and stated limits of the minimality claim are sound.

## Detailed checks

### Fixed-arc preprocessing and affine dimension

The lemma at lines 12–42 is correct. Nonemptiness ensures every supplied fixed
value satisfies its original bounds; reattaching these values to a reduced
feasible vector is therefore a two-sided bijection, not merely a projection
relaxation. Reattaching `z_ej=c_e y_j` is affine in the retained coordinates,
so the same assertion holds after convexification.

I specifically checked the new full-affine-dimension assertion. If a remaining
coordinate is nonconstant, two feasible values are distinct in `[0,u_e]`, so
their midpoint is strictly between both endpoints. Averaging one such midpoint
for every remaining coordinate keeps all bounds feasible and makes every bound
strict: for each coordinate at least one summand is strict. Consequently a
relative open neighborhood in the balance affine space is feasible. This
excludes additional affine equations beyond balances. Fixed coordinates at
interior capacity values cause no problem, since they too are deleted. The
empty remaining-edge set is correctly handled. Conditional state slices can
still be lower-dimensional, as the text explicitly cautions.

### Core reduction and initial formulation

- Lines 51–105: signed path constancy follows from zero divergence of block
  deviations, even when the reference flow itself violates capacities or
  original arc orientations oppose the path traversal. The two interval
  formulas have the correct signs. Suppressing degree-two vertices preserves
  cycle rank; a nonsingle-cycle cyclic block leaves minimum core degree three,
  giving the stated `2r-2` and `3r-3` bounds. The special loop/cycle convention
  correctly covers rank one and parallel pairs.
- Lines 107–154: eliminating the merged state retains both its capacity bounds
  and its circulation equations implicitly, because both the aggregate core
  deviation and every explicit-state deviation are circulations. Zero weight
  forces every path value and hence every cycle coordinate to zero. There is
  no lost condition at the simplex boundary. Counts include all original
  domains and observations; representative original arcs avoid increasing
  flow coefficients in residual rows.

### Unit minors and observed-direction elimination

- Lines 169–204: the network-matrix total-unimodularity proof is correct.
  Replacing tree columns proves the minor formula after expansion against
  unchanged identity columns. Cramer's rule for row replacement and the bordered
  determinant formula then give both `W` and the Schur remainder entries in
  `{0,+1,-1}`. Singular/repeated-row borders give zero. Empty pivot and free
  sets are harmless.
- Lines 206–260: the selected independent observation rows use distinct
  actual product coordinates. The pivot substitution is reversible for
  arbitrary retained values, and keeping every nonselected observation
  preserves consistency along a suppressed path. A selected product appears
  at most once in a reconstructed path. Different labels have disjoint columns;
  thus collection of terms in a residual inequality cannot create a product
  coefficient of magnitude two. The restriction kernel is exactly the
  circulation space supported on the unobserved subgraph, including loops and
  isolated vertices, proving `r-d=rho`.
- Lines 278–292: the explicit nonzero bound counts the potential dense
  reconstructed rows, not only the number of inequalities. For bounded block
  rank it is linear in the declared sparse input. The warning about rational
  row normalization correctly prevents an unsupported primitive-integer
  coefficient claim.

### Forest complements, completion, and reconstruction

The no-auxiliary corollary (lines 294–312) follows immediately from zero
restriction nullity. It appropriately imposes no conditions on labels already
merged locally and does not claim necessity of the forest criterion for all
possible unit-coefficient descriptions.

The completion proposition (lines 314–341) has the correct scope. Every added
individual coordinate reduces nullity by at most one. Choosing all nonforest
unobserved edges kills the circulation kernel with exactly `rho` additions.
Completing the graph's product set and then projecting its hull gives exactly
the original hull because linear projection commutes with convexification.
The extra equations are absorbed by the stated row bound, and no new label is
introduced. This is not an extension-complexity lower bound. The explicit
warnings about capacity-degenerate and zero-weight slices are necessary and
present.

Cut-based reconstruction (lines 343–350) is valid even when the unobserved
forest is disconnected: only its remaining tree edge is unknown across the
chosen component cut, while component balance imposes consistency. The
recovery paragraph retains the distinction between exact rational recovery
from a feasible extension and numerical LP feasibility.

Finally, I verified the K4 example (lines 377–401) directly from all four
balance equations. The reconstructed deviation on edge `23` yields exactly
the displayed cut. The four-path average and all three McCormick checks are
correct, and `3/5>1/2` gives a strict gap.

## Independent executable evidence and integration

`verification/reviewer1/stage02-round01/check.py` is a small independent exact
SymPy check, written for this review rather than reusing the author's code.
It constructs a K4 cycle matrix from incidence equations and checks:

- 300 exact Schur-row calculations over every independent observed-row subset
  and admissible pivot-column choice;
- all 64 K4 observation subsets against the incidence nullity formula;
- the stated K4 McCormick-feasible separating example using rational arithmetic.

All checks passed; `check-output.json` records the counts. These finite checks
supplement the general proof audit, rather than replacing it.

A private copy of the snapshot compiled with the documented `latexmk` command
to 13 pages. The final log contains no LaTeX warnings or overfull/underfull
boxes. The new `main.tex` input and accepted foundation clarifications introduce
no notation or logical inconsistency.

## Literature and review limits

I compared the manuscript to the repository's observed-rank development note
after performing the proof audit. The new fixed-arc lemma strengthens its
handling of degeneracy without overstating the conditional-slice conclusion.
The paper credits reduced RLT for product reconstruction and confines the
additional contribution to the graph criterion and sparse simplex-hull
consequence.

The repository contains metadata but no primary full text for
Liberti–Pantelides. I attempted to open the linked author-manuscript copy at
CiteseerX; it timed out. Thus I did not independently verify the exact
Theorem 3.1/Section 2 locator in this round. The fully supplied algebraic proof
does not depend on that unverified locator. This review does not establish
literature priority or audit later experimental claims.
