# Independent audit: contracted pooling with a common capacity interval

Date: 2026-09-05. Reviewer: `close_pooling/interval_proof`.

**Verdict: PASS.** I independently checked Sections 3–4 of the
[completed path-cut investigation](parametric-path-cut-clamp-investigation.md),
the signed-flow mapping in the
[contracted pooling theorem](../results/pooling-quality-scaled-path-flow.md),
and the polynomial symbolic path argument in Section 1. The extension
correctly permits any rational common pool interval `0<=L_P<=U_P`,
including a positive lower bound, for the scalar exactly contracted
one-pool class with bypass maximum degree two. Exact feasibility and
construction of a witness in a single real algebraic field of polynomial
degree and encoding length are polynomial bit-time tasks.

No mathematical defect was found. The previous degree-at-most-two witness
bound is correctly withdrawn for this extension. General source/product
contract intervals and arbitrary arc-profit optimization are not proved.

## Bounded-divergence base polyhedron

With outgoing-minus-incoming divergence, the cut function
`f(S)=u(delta+ S)-ell(delta- S)` is submodular even when arc bounds have
either sign. Indeed it is the nonnegative-capacity cut function for
`u-ell`, plus the modular function `div(ell)(S)`. The prescribed-divergence
circulation criterion gives precisely `B(f)` as the image of the bounded
arc-flow box.

For nonempty `D=B(f) intersect [alpha,beta]`, define

```
g(S)=min_T [f(T)+beta(S\T)-alpha(T\S)].
```

The two-label contribution at each node is jointly submodular because
its cross coefficient is `alpha_v-beta_v<=0`. Adding `f(T)` and partially
minimizing over `T` preserves submodularity, by applying the lattice
inequality to minimizing pairs and testing their union and intersection.

For every `d in D`, decomposition into `S intersect T`, `S\T`, and
`T\S` gives `d(S)<=g(S)`. At the empty and full sets, nonemptiness of
`D`, together with the specified choices of `T`, forces
`g(empty)=g(V)=0`. Conversely, `g(S)<=f(S)` follows from `T=S`. The
choices `T=empty` for singletons and `T=V` for their complements give
the respective upper and lower node bounds for any point of `B(g)`.
Therefore `D=B(g)`. Nonemptiness is needed here and is checked separately
by the retained circulation conditions in the application.

For costs in decreasing order, the differences
`g(S_k)-g(S_(k-1))` give a feasible greedy divergence vector. The standard
diminishing-increments argument proves all its subset inequalities.
Summation by parts then gives the stated maximum support formula because
`g(V)=0`. Negative costs are valid, ties can be broken arbitrarily, and
the minimum is the negative of maximum support with costs `-c`.

I also opened the cited
[primary manuscript](https://eprints.whiterose.ac.uk/id/eprint/78189/10/shakhlevich1.pdf).
Shioura, Shakhlevich, and Strusevich state the box-truncation rank formula
and greedy rule in Theorems 1–2, printed page 192. The direct proof in the
note checks the particular base-polyhedron normalization needed here.
Neither formula should receive a new general priority claim.

## Parameter partition and symbolic support

On each initial nonsingular quality interval, every `C_i-q` has a fixed
nonzero sign. The reviewed physical transformation gives affine node
bounds and constantly many quadratic capacity candidates per arc.
Partitioning at candidate-comparison roots makes the effective lower and
upper bounds explicit quadratic polynomials. All equality cells must be
retained; the construction does so. The original local parameter rows,
arc consistency rows, and connected circulation cuts establish exactly
whether the bounded signed-flow system is nonempty.

For every input node, its divergence divided by `C_i-q` equals its total
original bypass flow. Therefore, with zero costs on product nodes,

```
Z=c(q).div(w),             T_pool=A-Z.
```

Cost order is fixed between input qualities. For two input costs, the
difference has numerator `C_j-C_i` and denominator
`(C_i-q)*(C_j-q)`. Repeated source qualities produce ties. Input costs
cannot cross the zero output costs inside such an interval.

For a fixed greedy prefix `S`, the rank minimization over `T` is a cut
energy with nonnegative directed capacities `u-ell` and signed unary
terms. All coefficients are quadratic on the coarse parameter cell.
The underlying degree-two components are paths, cycles, or isolated
vertices. Section 1's translated clamp recurrence gives polynomially
many quadratic comparison polynomials for a path. Conditioning a cycle
label reduces it to two such path problems; comparing their piecewise
quadratic values adds only polynomially many breakpoints. Component
minima add, with no coupling between their labels.

The common refinement for both cost orders, all prefixes, and all
components remains polynomial: it is a union of polynomially many
univariate algebraic breakpoint sets. It is not a Cartesian enumeration
of independent component regions. On every resulting cell, including
singletons, each required rank value has one selected quadratic
expression. Tied expressions agree at the tie, so a consistent selected
expression evaluates the rank correctly there.

The support functions are sums of these expressions times reciprocal
linear factors. A product over distinct nonzero `C_i-q` factors clears
denominators. This produces degree and coefficient bit length polynomial
in input length. The sign of the denominator is known throughout each
cell. Nothing in this step requires a fixed number of source qualities.

## Exact common-interval decision

At fixed nonsingular `q`, the feasible signed-flow polytope is nonempty
and compact. Its total-bypass image is exactly the closed interval
`[Z_min(q),Z_max(q)]`. Thus intersecting with
`[A-U_P,A-L_P]` is equivalent to the two inequalities stated in the note.
Both the lower and upper common pool bounds are thereby enforced.

After denominator clearing, the local conditions and these two support
inequalities form a univariate polynomial sign problem of polynomial
degree, count, and coefficient length. Exact root isolation and sign
testing handle open cells and isolated feasible roots in polynomial bit
time. All original singular quality values and initial search endpoints
are handled by the complete original fixed-quality LP with the common
interval retained. They are not evaluated through singular reciprocals.

The existing degenerate physical preprocessing must retain the new common
interval as well: if pool flow is forced to zero because no usable intake
or outlet exists, a positive `L_P` makes that branch infeasible. This is
already required by applying the extension to the complete physical
model; spelling it out would make the inherited preprocessing clearer.

## Algebraic witness and bit complexity

A feasible open sign interval has a rational sample of polynomial
encoding length by the root separation bounds for the defining
polynomials. Otherwise choose an isolated feasible represented algebraic
root. Its degree and encoding length are polynomial. At this single
parameter `q`, select the rank-value expressions valid on its cell and
form both greedy divergence vectors. They lie in `Q(q)` with polynomial
representations and satisfy every node and base inequality.

For either divergence vector `d`, shift the arc flow by `ell`. The
remaining capacities are `u-ell>=0`, and the required residual divergence
is `d-div(ell)`. The usual source/sink construction reduces realization
to maximum flow. Edmonds–Karp has polynomially many augmentations over
an ordered field: its combinatorial termination proof depends on shortest
augmenting paths, not integral capacities. Exact field sign comparisons
decide bottlenecks and zero residual capacities.

This use of field arithmetic has a bit bound, not merely an operation
bound. Initial capacities and imbalances are polynomially represented
elements of the same `Q(q)`. All augmentation updates use additions and
subtractions and select bottlenecks from existing residual values. After
polynomially many updates, coefficient growth is at most exponential in
that operation count, hence has polynomial bit length; common rational
coefficient denominators can be retained. Ordered-field comparisons in
one represented real algebraic extension of polynomial degree and height
are polynomial-time operations.

Choose the desired bypass value as
`max(Z_min,A-U_P)`, which lies below both upper endpoints by the feasibility
test. If the extreme values differ, the required interpolation coefficient
is a single quotient in `Q(q)`; if they agree, no division is needed.
Field inversion and the resulting products have polynomial bit cost and
encoding length. Convex interpolation preserves all bounded-flow and
node rows. Dividing each recovered `w_ij` by nonzero `C_i-q` stays in
the same field. The reviewed conservation identities recover the actual
feeds, outlets, and both pool balances, and the interpolated total enforces
the common interval. Thus the witness claim is constructive and covers
irrational isolated feasible qualities without a numerical margin.

## Independent exact checks

The retained checker
[check_box_divergence_support_review.py](../code/pooling_bypass_paths/check_box_divergence_support_review.py)
passed 128 signed path/cycle systems, including disconnected and isolated
vertices. It enumerated 5,549 integer arc assignments, checked all 3,076
rank values against the actual bounded-divergence support, verified 256
greedy maximum/minimum vectors with reciprocal-quality costs, and checked
512 interpolated realizing flows exactly using rational arithmetic.
The systems have integral incidence data, so their bounded-flow polytopes
are integral and enumeration supplies the full support extrema, not only
sampled feasible points.

These checks independently exercise the new rank/support/interpolation
step. Section 1's separate recurrence checker and the earlier physical
mapping checks cover different dependencies. The mathematical argument
above establishes the entire parameter and algebraic-witness result.

The investigation's title and opening “not established” status are now
stale relative to the completed Sections 3–4. Its author should reconcile
that presentation and link this audit when closing the direction.

## Promotion confirmation

I checked the reorganized
[promoted theorem](../results/pooling-contracted-common-capacity-algorithm.md).
It preserves the audited argument and scope. The unusable-pool branch now
explicitly rejects `L_P>0`, resolving the exposition point above. The
affine-input-rank-at-most-one corollary uses the already reviewed rational
scalar compression from Section 11 of the earlier contracted theorem;
it preserves every physical flow and the common throughput interval.
Rank zero remains the original rational LP case. No new quality-rank
claim is introduced.

Section and equation references resolve to the intended arguments. The
displayed equation labels retain a harmless gap between (1) and (3),
but no reference points to a missing equation. The promoted statement
correctly retains polynomial-degree algebraic witnesses rather than the
earlier quadratic-field guarantee. **Promotion confirmation: PASS.**
No additional tests were needed for this reorganization.
