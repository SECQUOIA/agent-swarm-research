# Stage 5, round 1 — independent review 2

**Verdict: no major issues; accept after one minor terminology correction.**

I reviewed all of `05-universality.tex`, `06-series-parallel.tex`, and
`07-fixed-state-chains.tex` in the frozen `process/snapshots/stage05-round01`
snapshot, with their dependencies. I did not read another current-round report,
coordinate judgments, edit manuscript sources, or spawn agents.

## Enumerated findings

1. **R2-S5-01 — minor: “coordinate plane” has an incompatible existing definition.**
   `sections/04-bounded-rank.tex:376–378` explicitly defines a coordinate plane
   as fixing every coordinate except **two**. The general transfer theorem at
   `sections/05-universality.tex:19–24` calls a section with **p** free observed
   coordinates a coordinate plane, with no restriction to `p=2`. Use “coordinate
   affine subspace” (or “coordinate subspace obtained by fixing the other
   coordinates”) in the general transfer statement. Retain “coordinate plane”
   in the two-coordinate applications. This is a terminology conflict, not a
   mathematical defect: the construction plainly produces the asserted
   p-coordinate affine section. No new mathematical review round is needed
   for this local correction alone.
2. **No major findings.** I found the imported universality map, explicit
   Fibonacci constructions, new reduced-profile formulation, unit-coefficient
   results, and sharp four-state obstruction mathematically sound under their
   stated assumptions.

## Universality and original-coordinate transfer

At `05-universality.tex:6–16,29–44`, I independently checked the primary source
in `literature/papers/loera2006-all-linear-and-integer-programs/fulltext.md`.
Theorem 1.1 uses coordinate-erasing representation; Section 3.1 preserves
original variables as coefficient-reduction coordinates, Section 3.2 explicitly
embeds those coordinates into table entries, and Section 3.3, printed p. 816,
uses exactly the stated final injection into layer 1. The source construction
uses integer margins after integer equation data and an integer upper bound
are supplied. Clearing the rational equation denominators therefore does not
rescale the designated original variables. The added nonnegative slack
coordinates are unique affine functions of the bounded original variables,
so the standard-form extension remains bounded.

The padding at lines 46–52 is valid: zero old–new two-margins force all cross
entries to zero, and unit row/column layer margins force each new corner
entry to one. It preserves every old designated coordinate while making all
three layer totals positive.

In the graph transfer at lines 54–91, all aggregate and boundary coordinates
are genuinely fixed; the only free original coordinates are the designated
interior products. The two observed boundary layers and the aggregate determine
the third layer's margins. Conversely every table yields a feasible state
flow, since its nonnegative interior and boundary entries cannot exceed the
layer total. That total equals its state weight times the common capacity.
Thus the proof establishes a section in the sparse original model, not a
projection claim about facets of a larger observed hull.

Uniform scaling of every flow and product by B preserves all coefficient
ratios between products. The original normalized nonlinear model has only unit
data; the rational section constants are not asserted to be constraints of
that model. The polynomial-in-log-M construction and the superpolynomial
*magnitude* consequence follow. The two-coordinate triangle application has
a genuine local half-plane with interior, so the earlier facet-transfer lemma
and its affine-equation invariance apply.

## Balanced incidence and Fibonacci families

At `06-series-parallel.tex:23–90`, the inequality from unobserved row entries
bounded by their common state profile has the stated sign. Multiplication by
the strictly positive balancing vector eliminates the profile deviation because
its sum is zero. For the converse, the vector `-delta+tau` has only the two
stated nonzero entries. The given neighborhood controls both the inverse-matrix
perturbation and the nonnegative correction tau. All observed entries remain
strictly below their profile values, and subtracting tau from one allowed
entry preserves nonnegativity. Completing the other parallel arc and bypass
therefore gives actual graph state flows, including on the boundary line.
No independent profile is silently chosen for each gadget.

The small four-state example and the more general linear-ratio family have the
reported graph, observation, and ratio counts. The separate-scalar failure
uses distinct feasible gadget profiles and correctly shows why those scalar
conditions cannot be composed.

At lines 135–211, I checked the Fibonacci column recurrence, invertibility,
positive balancing weights, their sum, and complement invertibility. Every
row of D has two or three ones for q at least three, so both D and its
complement have nonempty proper rows. The sparse observation count is exactly
`5q-4`; the dense variant has the complementary count. The selected free cells
in the sparse version really are observations. The ratio is `F_q/F_1=F_q`,
with every other original coordinate fixed.

For the simple maximum-degree-three lift at lines 213–240, splitting joins and
subdividing b arcs gives exactly `3N` vertices and `4N` arcs. The endpoints have
degree three; each split join has degree three and each subdivision vertex
has degree two. In the applicable family N is at least five, so the untouched
bypass does not create a parallel pair with an a arc. New connector flows are
uniquely the chain flow, and the subdivided b arcs copy the old b flow. This
extension works state by state with redundant unit capacities. Fixing their
aggregate coordinates leaves precisely the same two-coordinate section.
The count, treewidth/planarity, unit-data, and encoding conclusions are correct.

## New reduced profile and small-state theorems

At `07-fixed-state-chains.tex:25–87`, the four observation classes give exactly
the available a-arc interval in each gadget. Nonnegativity of observed products
is explicitly checked, which is necessary when a doubly observed cell is
recovered from its sum. Eliminating the residual coordinate transforms the
second endpoint using `0 in U_i`; this is why all endpoint normals become
*positive* subsets, while only negative singletons and the negative full vector
remain. Empty subset rows are not discarded without their scalar checks.

The general determinant/circuit argument, fixed-size inverse-basis recovery,
greedy filling, and rational encoding analysis at lines 91–201 are valid.
A grouped minimum retains an actual affine row choice, so selected circuit
branches are globally valid. The statement does not assume that every normal
in the universe occurs in a given instance.

For two explicit states, the five tests are exactly interval/sum-strip
feasibility. The displayed recovery attains an allowed sum and splits it
between the two intervals. The product occurrence argument establishes unit
original coefficients, rather than merely unit cancellation weights. The
shared bypass coefficient is correctly offset by the compulsory negative
full row when two upper singleton endpoints are selected.

For three explicit states, I checked both the completeness proof and an
independent exact enumeration of the sixteen circuits. The four families
contain 7, 5, 3, and 1 circuits, with weight two only on the negative full
normal in the last family. The stated exclusion properties of singleton and
subset normals hold in every family and control repeated product occurrences.
Only the bypass flow can acquire coefficient magnitude two.

Both bypass repairs at lines 389–416 are valid. A coefficient of -2 comes
only from three upper singleton endpoints in distinct gadgets; a coefficient
of +2 comes only from three lower pair endpoints in distinct gadgets. Thus the
chosen gadget's a-flow coefficient has exactly the required sign and no other
contribution. Adding or subtracting its valid flow equation reduces the bypass
coefficient and preserves all other unit bounds. The violation is unchanged
for queries passing the flow precheck. Both supplied query examples satisfy
their stated McCormick checks and have the stated negative circuit value.
The four-explicit-state balanced-incidence example then supplies the sharp
failure of a unit description, through actual free product coefficients whose
ratio cannot be altered by affine equations.

The observed-label merger at lines 453–475 preserves the original full simplex
while using only the observed-label profile coordinates. A shared normalized
merged flow gives compact recovery for all unused labels with O(m) additional
weight bookkeeping. The stated `(a+1)L` term covers the original graph even
when a is zero; the no-observation hull is correctly identified as the
Cartesian product of flow domain and simplex.

## Independent executable evidence

I wrote two standalone exact checks without importing repository hull code:

- `verification/reviewer2/stage05-round01/check_circuits.py` enumerates the
  reduced circuits independently for m=1,2,3, obtaining 1,5,16 circuits on
  2,6,11 normals. It checks 3,096 affine row-selection combinations over
  **all** gadget observation-class patterns for m=2,3. Product and individual
  gadget-flow coefficients always have magnitude at most one. Independently
  enumerating bypass coefficient choices yields exactly the two exceptional
  m=3 patterns repaired in the proof. Result: `circuit-result.json`, PASS.
- `verification/reviewer2/stage05-round01/check_fibonacci.py` constructs both
  dense and sparse-complement incidence families for q=3 through 9. It verifies
  matrix identities, invertibility, counts, and ratios, then checks 184 exact
  feasible section witnesses and 166 exact infeasible-side certificates. It
  explicitly builds the simple split/subdivided graph and checks 2,012 state
  flows for balance, capacity, aggregates, simplicity, degree, and counts.
  Result: `fibonacci-result.json`, PASS.

Commands actually run:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage05-round01/check_circuits.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage05-round01/check_fibonacci.py
```

The occurrence enumeration isolates each gadget because an observed product is
unique to its gadget and label; all other selected rows contribute zero to that
product. The bypass enumeration is separate because its coordinate is shared.
The exact finite experiments support, rather than replace, the general proofs.

## Limitations

I verified the imported first-layer injection and construction scope from the
local primary-source full text, but did not reimplement the entire De Loera–Onn
universality algorithm. I did not independently certify priority of the new
small-state results, inspect a private PDF build, or review later unwritten
stages. The only required change identified here is R2-S5-01.
