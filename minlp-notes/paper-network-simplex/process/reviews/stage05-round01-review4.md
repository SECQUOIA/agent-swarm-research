# Stage 5, round 1 — independent reviewer 4

Snapshot: `process/snapshots/stage05-round01`.

## Verdict

**No major issues. One minor terminology inconsistency should be corrected.**
The universality transfer, balanced-incidence construction, sparse Fibonacci
family, reduced profile formulation, five-test oracle, and new sharp
three-versus-four-state coefficient threshold pass the proof audit and the
independent checks below.

## Enumerated findings

1. **R4-S05-01 — Minor: “coordinate plane” has conflicting dimensions.**
   Location: `sections/05-universality.tex`, Theorem `thm:universality`,
   lines 21–24. This theorem calls the affine space leaving `p` products free
   a “coordinate plane,” whereas `sections/04-bounded-rank.tex`, lines 376–377,
   explicitly defines a coordinate plane to leave exactly two coordinates free.
   The transfer theorem allows arbitrary `p`. Use “coordinate affine subspace”
   or “coordinate section fixing ...” here, reserving “coordinate plane” for
   the two-coordinate applications. The construction and proof are correct;
   this requires no mathematical change.

## Universality and sparse series–parallel audit

I independently read the relevant primary-source statements in
[De Loera–Onn](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf).
Theorem 1.1 defines representation by a coordinate-erasing bijection, and
Section 3.3, printed page 816, explicitly injects the retained variables into
layer one. The manuscript correctly distinguishes the new sparse bilinear
section transfer from their already established bitransportation and
two-commodity flow interpretation.

Adding nonnegative slack variables to a bounded inequality-described polytope
gives a bounded standard-form extension: each slack is determined by the bounded
original vector. Clearing equation denominators preserves these coordinates.
The padding sets old–new cross cells to zero by their nonnegative zero-total
constraints; the new row and column layer margins then force exactly one in
each corner layer. Thus it supplies strictly positive layer totals without
altering the retained coordinates.

In the four-layer network, aggregate interior flows fix the cell totals,
observed boundary products fix the first two layers' row and column margins,
and subtraction fixes the third layer. Every resulting state flow is a
nonnegative acyclic source–sink flow of value `D_k`, so every arc is bounded
by `D_k`, exactly its scaled uniform capacity. Conversely every table supplies
the full disaggregation. Scaling both flows and products by the same `B`
preserves the bilinear equations and coefficient ratios. The original model
has only unit numerical data after this normalization; rational constants
used to define the section are correctly distinguished from its input data.
The coefficient lower bound and its interpretation concern magnitudes, not
bit-length or separation hardness.

For the balanced-incidence lemma, multiplication by the positive balancing
vector proves necessity with the correct sign. The proposed correction
`tau_s=(alpha_r/alpha_s) delta_r+delta_s` satisfies
`alpha^T(-delta+tau)=0`; hence the recovered profile has the fixed total.
The stated epsilon bounds both `K^{-1}(-delta+tau)` and `tau_s`, since that
right-hand side has only the entries `-delta_r` and
`(alpha_r/alpha_s) delta_r`. Observed entries stay below each profile,
and reducing one allowed cell in row `s` by `tau_s` leaves it nonnegative.
This gives all gadget and bypass state flows, including the zero residual
state. The witness proves a locally full half-plane rather than only one
support inequality, which is what the coefficient-transfer lemma needs.

I checked the four-state, seven-observation small example and its generalized
linear-ratio counts. The separate-scalar-composition counterexample also works:
each gadget can move profile mass independently, while the positive balance
certificate forbids a single common profile for the proposed joint point.

For the Fibonacci family, the paired column equations force the recurrence
in every kernel vector, and the final column forces it to zero. The positive
balancing weights sum to `(q-1)F_{q+1}+1`; the complement consequently retains
positive constant column balance and is invertible. Its observed entries are
exactly the `5q-4` ones of the sparse original incidence matrix. All row
properness, graph counts, cycle rank, and the stated width-two decomposition
are correct. The fixed section's coordinates have logarithmic bit length;
the large Fibonacci ratio is not inserted into the original network data.

The simple lift adds `N-1` connectors and `N` subdivision vertices, yielding
`3N` vertices and `4N` arcs. It removes parallel pairs and makes every join
degree three. Connector state flows equal the common profile; both subdivided
segments carry the old `b_i` state flow. These are uniquely determined, respect
unit scaled capacities, and preserve all observed `a_i` coordinates. Fixing
their aggregates therefore preserves precisely the two-coordinate section.

## Shared-profile and new threshold audit

The four-way observation partition gives the stated exact range of aggregate
`a_i` flow. Product nonnegativity is essential for doubly observed cells and
is included among the prechecks. The bypass equations, profile bounds, and
aggregate profile sum supply every state balance and capacity. No argument
requires positive state weights.

Eliminating the residual coordinate changes both gadget endpoint inequalities
to positive subset normals and leaves only negative singleton and negative
full normals. The signs of `t-R_i` and `lambda_0-t` are correct. Zero normals
are separately checked. Grouping by a minimum right-hand side is exact, and
positive Farkas circuits justify independent branch expansion. Cofactor bounds
apply because each normal is a signed whole-row `0/1` vector. The count,
arithmetic complexity, and general coefficient bound follow.

The inverse-basis recovery is complete even on a lower-dimensional feasible
profile region, because a vertex's tight rows span the ambient profile space.
There is only one basis solution followed by greedy filling, so polynomial
rational encoding follows directly from the input-derived right-hand sides and
bounded determinants. The fill preserves prescribed observations and realizes
each aggregate. The observed-label merger changes no flow or product
coefficient, and its compact recovery requires only one default flow plus
the unused global weights. Dense output is separately accounted for.

For two explicit states, the five conditions are precisely interval
nonemptiness and intersection of the attainable sum interval with its imposed
interval. The displayed recovery choices satisfy all endpoints. Product
coefficient control requires more than unit circuit weights, and the manuscript
correctly checks repeated occurrences: two same-sign appearances cannot enter
the same minimal circuit. The full negative row offsets the only possible
double bypass contribution. Thus all five tests have unit representatives.

For three explicit states, I independently enumerated the complete positive
circuit list and obtained the stated `7+5+3+1=16` circuits. The direct
case classification is also complete: with the negative full row, zero,
one, or two negative singleton rows give exactly the stated possibilities;
minimality excludes opposite pairs inside a larger support. All positive
subset weights are one, and the sole doubled weight is on the negative full
normal, whose right-hand side has no product coordinate. The same occurrence
argument therefore still controls every product coefficient.

The two bypass repairs are valid. In the singleton-partition exception, all
three selected positive rows are upper gadget endpoints from distinct gadgets,
so adding one gadget's flow equation changes coefficients `(-2,-1,0)` on
`(x_h,x_{a_i},x_{b_i})` to `(-1,0,1)`. In the pair-triangle exception,
all three selected positive rows are lower endpoints from distinct gadgets;
subtracting one gadget balance changes `(2,1,0)` to `(1,0,-1)`. No other
selected row from that gadget contributes a flow coefficient. Both repairs
preserve candidate violation after the original flow precheck. I recalculated
both explicit repair examples and their separate McCormick feasibility.
The four-state balanced example has a locally full ratio-two section, so its
obstruction cannot be removed by these or any other valid affine equations.
This establishes the claimed sharp threshold on this topology.

## Independent executable checks

Evidence uses fresh scripts under `verification/reviewer4/stage05-round01`,
without importing repository result implementations.

`check_new_chain.py` independently enumerates circuits and inverse bases,
constructs symbolic reduced-profile rows, expands circuit branches, and
compares exact circuit decisions against an independently assembled LP over
complete directed-path/simplex-vertex mixtures. Final results:

- reduced circuit counts `1,5,16` for one, two, and three explicit states;
- 10,668 symbolic circuit branches checked for original flow/product
  coefficients, including both bypass repairs;
- 300 path-mixture LP comparisons, all agreeing, with only HiGHS statuses
  optimal or infeasible accepted;
- 100 exact rational inverse-basis/greedy disaggregations checked against
  state capacities, aggregates, and all observations.

The generated weights include zero explicit and residual states, and observation
patterns include both arcs and the bypass. Two observation patterns were
explicitly included to exercise both bypass repairs; an initial random-only
run did not exercise those repairs and was replaced by the final run.

`check_balanced.py` verifies exact balancing, matrix invertibility, the local
construction, and state extensions through the simple lift. Results:

- seven Fibonacci families, `q=3,...,9`;
- 92 exact feasible witnesses and 83 exact exclusions by positive balancing;
- 1,006 simple-lift state-extension checks;
- 14 additional exact witnesses for the four-explicit-state threshold example.

Both scripts passed; their JSON summaries are retained alongside them.
The LP comparisons are numerical corroboration, whereas the coefficient,
recovery, and balanced-incidence witness checks use exact arithmetic.

The complete private snapshot compiled successfully with `latexmk` in the
reviewer's `build` directory; its final log has no warning, undefined-reference,
overfull, or underfull matches.

## Coverage and limitations

I compared the current-stage claims with the repository universality and
fixed-state-chain result files and with the earlier series–parallel source
development supplied in the task. The manuscript retains the relevant
obstructions and improves the previously unreduced 41-circuit result with a
proved residual elimination and sharp unit-coefficient threshold. Historical
computational counts need not be copied into this theoretical stage.

I did not reimplement the entire De Loera–Onn universal encoding; that part is
an explicitly cited primary-source theorem, whose required first-layer property
I inspected directly. Tests do not prove arbitrary-size claims or establish
literature priority. I read no other current-round reports, edited no
manuscript sources, and spawned no agents.
