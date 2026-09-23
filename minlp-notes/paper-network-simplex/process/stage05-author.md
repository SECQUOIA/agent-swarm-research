# Stage 5 author record

Date: 2026-09-07. Sole author/developer agent: `paper_author`.
Status: author development and checks complete; five independent stage
reviews are still required before acceptance.

## Files and source coverage

Added three manuscript sections and their inputs in `main.tex`:

- `sections/05-universality.tex`: the complete transfer from slim
  transportation tables to a sparse original-coordinate section, positive
  layer padding, unit normalization, fixed-two-variable coefficient growth,
  encoding qualifications, and the 0/1-hull interpretation.
- `sections/06-series-parallel.tex`: the common branch profile, full
  balanced-incidence lemma with an explicit valid neighborhood and exact
  disaggregation, the five-vertex/nine-arc example, the earlier general-M
  family, an actual infeasible witness for scalar-only composition, dense
  and sparse Fibonacci constructions, and the simple degree-three lift.
- `sections/07-fixed-state-chains.tex`: the full arbitrary-observation profile
  formulation, original-domain checks, zero states, circuit elimination,
  determinant and encoding bounds, finite inverse-basis recovery, and the
  new reduced-profile and sharp few-state conclusions described below.

Canonical sources read and covered are `results/network-simplex-universality.md`,
`results/network-simplex-series-parallel-coefficient-growth.md`, and
`results/network-simplex-flat-chain-fixed-states.md`, together with
`notes/network-simplex-reopened-series-parallel.md` and their independent
review records. The earlier dense Fibonacci construction follows directly
from the proved balanced-incidence lemma and is retained explicitly as a
comparison; the sparse complement is the primary result. The scalar failure
now has a precise negative witness, not only an explanation of missing state
information. The root independently suggested and checked that witness.

The four accepted earlier section files and the bibliography remain
byte-identical to the Stage 4 accepted snapshot. No earlier theorem was
changed. README now describes the added material and runnable checks.
The introduction and abstract retain their accepted provisional scope;
their final synthesis belongs to the planned later exposition stage.

## New developments completed while writing

### Residual-coordinate elimination

The root noticed that the residual state is unobserved in every gadget.
I independently rederived the substitution `w0=t-sum(w_explicit)`. It turns
the upper aggregate endpoint into a positive subset inequality, leaving
only positive subset normals, negative singletons, and the negative full
normal in dimension `m`, rather than arbitrary signed subsets in dimension
`d=m+1`. Every individual original flow/product coefficient remains unit.

This improves the general description bound from `(d+1) Delta_d` to
`(m+1) Delta_m`. The manuscript calls the determinant constant `Delta_m^{01}`
to distinguish it from the already established simplex notation `Delta_m`.
For dimensions 1, 2, 3 the reduced library has 1, 5, 16 circuits, versus
1, 5, 41 in the complete signed-subset universe. Both counts and their
different meanings are retained. The parameter work is `2^{O(m^2)}`.

### Finite-basis profile recovery

The existing theorem left recovery as a grouped LP followed by interval
filling. The manuscript gives a full finite inverse-basis construction:
enumerate all bases of the fixed reduced normal universe, solve each
selected active system, and retain a feasible candidate. Every bounded
nonempty profile domain has a vertex with full ambient-rank active normals,
including points and lower-dimensional domains. This proves termination
without an online LP. One inverse application and greedy interval filling
preserve polynomial rational encoding length. Preindexed subset masks and
cached singleton indices justify the stated row-grouping operation count.

### Two-state five-test oracle

The root proposed the reduced hexagon interpretation; I independently
verified all five conditions and the explicit sum-and-interval recovery
formula. This gives linear-time grouping, five tests, and direct recovery
with no library enumeration. Unit circuit multipliers alone do not prove
unit original coefficients. The manuscript includes the complete occurrence
argument for a-only, b-only, doubly observed, and bypass products, plus the
separate shared `x_h` coefficient check.

### Sharp unit-coefficient threshold at three explicit states

The root then proposed extending the unit guarantee to `m=3`. I rederived
the full 7+5+3+1 positive-circuit classification and all coefficient cases.
Every product and gadget-first-arc coefficient is already unit. Only two
types of affine branches have a bypass coefficient of magnitude two:

- three upper singleton endpoints plus the negative full row give `x_h=-2`;
- three lower pair endpoints plus twice the negative full row give `x_h=+2`.

Each extreme case uses three distinct gadgets. Adding, respectively
subtracting, one selected gadget equation `x_a+x_b+x_h=1` repairs the
bypass coefficient, cancels its nonunit-risk partner `x_a`, and introduces
only a unit `x_b` coefficient. This produces an exact unit description
modulo the already required flow equations. The old four-explicit-state
seven-product example has a necessary ratio two invariant under all affine
equations. It therefore makes the state cutoff sharp on this flat topology.

Both repair types have explicit McCormick-feasible but jointly infeasible
queries in the paper. Their exact circuit values are `-1/5` and `-1/20`.
Root development and independent checks remain separately recorded in
`process/stage05-residual-profile-development.md` and `verification/stage05-root/`.
No arbitrary nested series-parallel or fixed-state general-treewidth theorem
is asserted.

### Observed-label parameter

The root noted that the accepted exact state merger applies to the whole
flat chain. The concluding corollary explicitly replaces the total explicit
state count by the number `a` of observed labels: the unit guarantee holds
for `a<=3`, and the five-test oracle for `a<=2`, even with many unused
simplex coordinates. Unused labels share one normalized recovered flow.
The added `O(m)` bookkeeping and possible dense global-flow output cost
are distinguished from profile work. This is a direct application of the
accepted merger, with a short proof and no new gluing assumption.
The bound uses `(a+1)L`, including the original-flow scan and default
flow when no label is observed; the root caught and corrected the initially
omitted `L` term at `a=0` before the stage was frozen.

## Literature and attribution

Checked the open author-hosted De Loera--Onn primary PDF at
<https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf>.
Theorem 1.1 supplies universality; Section 3.3, printed page 816, supplies
the injection `((i,j),(1,k),1)` needed to put all retained coordinates in
one layer. Theorem 1.2 and pages 807--808 already provide bitransportation
universality and the two-commodity network interpretation. The manuscript
credits these explicitly, rather than presenting universal network flows
as a new result. The added statement is the sparse bilinear coordinate
section and its coefficient consequence. No implementation of the entire
imported universality construction is claimed.

Read the primary Alon--Vu PDF
<https://web.math.princeton.edu/~nalon/PDFS/av1.pdf>, including its 0/1
geometry discussion. The paper credits the established general large-weight
and ill-conditioned-matrix phenomenon without suggesting that large 0/1
facet coefficients were first found here.

Checked Almoghrabi--Skutella--Warode (2026), Remark 1, at
<https://link.springer.com/article/10.1007/s10107-026-02392-8>.
It explicitly distinguishes aggregate flow integrality from full commodity
vectors; that distinction is attributed precisely. The existing
Khademnia--Davarnia comparison remains in the accepted earlier sections.
The bibliography already contained all three relevant verified entries;
no padding references or unsupported priority claims were added.

## Verification executed

All commands used `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`.
The new scripts import no existing repository oracle implementation.

1. `python paper-network-simplex/verification/stage05-padding.py`:
   60 exact positive-padding, full state-flow, residual subtraction, and
   unit-normalization checks; 45 inputs had a zero layer before padding.
   This checks the added transfer algebra, not De Loera--Onn's full reduction.
2. `python paper-network-simplex/verification/stage05-profile.py`:
   exact reduced and unreduced circuit enumeration; 42 and 1,715 full affine
   branch checks for `m=1,2`; 4,160 per-coordinate branch-extremum checks
   and all 539 exceptional repaired branches for `m=3`; 216 membership
   cases with 116 exact full-flow recoveries and 100 exact rejections;
   122 cases had a zero state weight. An independently assembled state-arc
   LP agreed in all 216 cases, with only statuses 0 and 2 accepted. The
   two explicit repair queries also passed exact coefficient/value checks,
   separate McCormick checks, and numerical LP infeasibility checks.
   Twelve additional exact checks recovered six-explicit-state instances
   through only one, two, or three observed labels and verified every
   proportionally refined global state flow.
3. `python code/network_simplex_review/fibonacci_vertex_audit.py`:
   120 exact full-flow witnesses across the dense and sparse families,
   through `q=30` and ratio `F_30=832040`, plus 32 numerical path-vertex
   mixture LP checks. Both families passed.
4. `python code/common-factor-network-simplex-verify.py`:
   300 numerical projected support comparisons on 150 table instances,
   comparing table LPs with explicitly enumerated normalized sparse hull
   vertices. This does not prove universality computationally.
5. `python code/network_simplex_review/flat_chain_profile_audit.py`:
   320 numerical independent path-vertex/profile comparisons (171 feasible,
   149 infeasible), 684 exact simple-graph path lifts, and independent
   signed-subset counts 1, 5, 41. Includes zero residual and explicit states.

Exact certificates and witnesses are distinguished from numerical LP checks
in this record and `verification/stage05-validation.json`. Existing audit
scripts were rerun unchanged; new reports are retained alongside their scripts.
The full paper is rebuilt with `latexmk -gg -pdf -interaction=nonstopmode
-halt-on-error main.tex`; the final log has no undefined citations/references,
overfull boxes, or other warnings. The resulting manuscript has 38 pages.

## Remaining scope and review status

No proof gap remains identified in the stated results. The new unit threshold
has root/author mathematical checks and exact branch verification but still
requires the user's five independent stage reviews. The theorem is restricted
to the specified flat topology; arbitrary nested series-parallel networks
are outside its claim. Coefficient magnitudes are distinguished throughout
from their encoding lengths, and no separation-hardness or extension-size
lower bound is inferred. Literature comparison is a documented search, not
an unconditional first-publication claim. Stage 6 implementation and empirical
evaluation have not been started by this author.
