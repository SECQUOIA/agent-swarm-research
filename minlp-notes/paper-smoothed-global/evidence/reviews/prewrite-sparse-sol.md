# Sparse polynomial and constraint audit by Sol

Date: 2026-10-05. Scope: the 17 assigned sparse, polynomial, graph, simplex,
order, and actuator notes, their relevant completed-text reviews, and the
local-error counterexample referenced by the global-error review. This is an
independent mathematical reconstruction. No source note was edited, experiment
rerun, literature searched, CI inspected, or commit made.

The final proofs support all the stated extensions under their stated
premises. I found no unresolved mathematical blocker. Several qualifications
are essential to their correctness and should remain explicit in the paper.
The strongest coherent presentation uses one mixed polynomial box theorem,
a rational quadratic specialization, two graph reductions, a product-simplex
theorem, and one continuous/binary order theorem. The binary order transport
proof also improves the continuous specialization; its sharper count should
supersede the earlier continuous count. The actuator reduction is a separate
corollary because it permits arbitrary forward depth while preserving unary
reduced terms under affine state costs.

This conclusion concerns the reviewed proof interfaces, not novelty,
practical performance, or an executable implementation of the complete
sampler, quantifier elimination, and ellipsoid routines. The classical
quantifier-elimination and convex-optimization source statements are used as
transcribed in the assigned notes and previously audited reviews. I checked
their applications and complexity composition; I did not conduct a new
literature audit.

**Coverage and precise source locators.** Paths below are relative to the
repository root. The line locators identify the version read in this audit.

| Source | Mathematical disposition | Main locators |
| --- | --- | --- |
| `research-20261002/new-direction/sparse-bag-cell-smoothed-qp.md` | Complete continuous quadratic theorem; retain its rational exact-output specialization. | §§2–3, lines 68–168; §4, lines 170–239; §§5–7, lines 241–410. |
| `research-20261002/new-direction/sparse-bag-cell-smoothed-miqp.md` | Complete native-integer quadratic extension; supersedes the continuous theorem's domain, with the same rational output. | §§2–3, lines 57–192; §§4–6, lines 194–340. |
| `research-20261002/new-direction/smoothed-sparse-polynomial.md` | Complete fixed-degree mixed polynomial box theorem with exact implicit output. | Statement, lines 12–80; rounding/count, lines 84–198; closure, lines 200–289; schedule/evaluation, §§5–6. |
| `research-20261002/new-direction/polynomial-finite-noise-tails.md` | Complete uniform scalar-section and active-gradient interfaces. It is a lemma, not an optimization theorem on its own. | Growth formula, lines 31–45; section bound, lines 79–163; hybrid transfer, lines 180–215; root count, lines 217–258. |
| `research-20261002/new-direction/polynomial-exact-fallback.md` | Complete canonical all-draw fallback with separated coefficient-height and precision costs. Its formula proof extends directly to the constrained domains. | Canonical selection/formulas, lines 77–156; complexity and root recovery, lines 158–237; feasible gaps, lines 239–270. |
| `research-20261002/new-direction/polynomial-exact-fallback-construction.md` | Complete independent constructive fallback for mixed boxes. Keep as alternative proof or appendix; it does not itself give the constrained fallback. | Finite quotient, lines 106–173; optimizer completeness, lines 175–206; heights/counts, lines 208–254; exact ties and precision, lines 256–368. |
| `research-20261002/new-direction/convex-patch-evaluation.md` | Complete bit-model evaluator after the GLS feasibility/erosion correction. | Contract, lines 15–45; epigraph/oracle, lines 47–118; GLS and repair, lines 120–215; distance accuracy, lines 217–245. |
| `research-20261002/new-direction/global-error-cell-barrier.md` | Complete limitation of the specified retention and hull-closure rules. It is neither hardness nor a lower bound for all algorithms. | Actual graph/curvature, lines 18–64; survivor count, lines 66–131; closure obstruction, lines 133–174; scope, lines 176–202. |
| `research-20261002/new-direction/smoothed-polynomial-graph-constraints.md` | Complete bounded-depth explicit graph substitution corollary. | Model/curvature, lines 22–104; expanded decomposition, lines 106–131; common law, lines 133–212; feasible output, lines 214–241. |
| `research-20261002/new-direction/smoothed-implicit-graph-constraints.md` | Complete scalar monotone implicit graph extension, including approximate DP and original-domain algebraic fallback. | Global premises, lines 11–63; approximate DP/count, lines 128–181; closure, lines 183–223; KKT/tails/fallback, lines 225–318; output, lines 320–360. |
| `research-20261002/new-direction/implicit-graph-oracle-interface.md` | Complete rational oracle and exact implicit-output interface. It does not independently choose the noise law. | Root/derivative oracles, lines 78–147; DP, lines 149–223; closure, lines 225–300; separation/evaluation, lines 302–456; original-graph fallback, lines 458–490. |
| `research-20261002/new-direction/simplex-block-smoothed-extension.md` | Complete disjoint inequality/equality simplex extension with native integers and whole-block bags. | Curvature/model, lines 15–64; rounding/count, lines 66–174; forcing/closure, lines 176–241; margin tail, lines 243–290; relative evaluator, lines 340–446; equality blocks, lines 448–482. |
| `research-20261002/new-direction/smoothed-sparse-order-polynomial.md` | Complete continuous order theorem. Its count can be replaced by the sharper transport specialization below. | Rounding/pruning, lines 70–129; old count, lines 131–172; LP closure, lines 174–236; finite schedule, lines 238–346; feasible evaluation, lines 348–396. |
| `research-20261002/new-direction/smoothed-mixed-order-polynomial.md` | Complete continuous/binary order theorem; use its stronger count for both domains. | Model, lines 17–65; rounding, lines 67–109; transport, lines 111–164; sharper count, lines 166–228; binary-before-exposure rule, lines 230–285; schedule/evaluation, lines 287–409. |
| `research-20261002/new-direction/order-polytope-cell-count.md` | Complete continuous chamber-count lemma. The affine-fiber representation is valid but unnecessary for the strongest unified theorem. | Projection/closed-fiber proof, lines 76–146; face grid count and independent tests, lines 148–227. |
| `research-20261002/new-direction/order-polytope-face-closure.md` | Complete all-draw LP forcing and finite-law exposure-gap lemma; its weighted Hessian test is sharper than the composition's unweighted version. | LP soundness/Lipschitz gap, lines 43–133; stationary roots and sum fibers, lines 175–271; weighted closure, lines 276–365; feasible evaluation, lines 367–506. |
| `research-20261002/new-direction/smoothed-polynomial-actuator-dynamics.md` | Complete arbitrary-horizon affine-state/affine-state-cost reduction with polynomial actuators and native integer controls. | Invariance/scope, lines 24–99; adjoint identity, lines 107–177; uniform schedule, lines 179–257; exact trajectory evaluation, lines 284–316. |

**The shared pruning proof.** Let the current physical domain be the original
feasible domain intersected with the unions of the candidate bag cells. Each
bag uses the same deterministic partition for every coordinate it shares
with another bag. A coordinate strictly between grid nodes has one containing
interval; a coordinate on a grid boundary is fixed by the rounding. Thus one
rounding distribution preserves every chosen incident bag cell at once. It
also preserves one specified bag cell, which is needed for the conditional
lower bound. Choosing independent cells or independent witnesses per bag
would not establish this invariant.

For a mixed box, replace coarse integer intervals by singleton labels once
the mesh is below one. This preserves their physical integer sets. Refine
clipped continuous intervals using the next common grid, rather than their
individual midpoints. Sequential mean-preserving rounding applies
`f'' <= L` to each intermediate coordinate segment. The bound must hold on
the full continuous hull, including between integer labels. It yields

```
E[F(Y)] <= F(x)+E_h,                 E_h=n L h^2/8.
```

For a quadratic this reduces to cancellation of off-diagonal errors and a
sum of diagonal variances. The sequential proof is needed for higher-degree
terms such as `x^2 y^2`; quadratic cancellation is insufficient there.

The row lists are the union of candidate-cell corners, with duplicate rows
removed. Exact separator consistency and the running-intersection property
give one global assignment. Every assigned factor is counted once. Directed
messages take minima keyed by separator tuples. A bag row looks up incoming
minima and updates an outgoing key, so adjacent random table sizes are never
multiplied. Copy bags to make the decomposition degree at most three before
counting work, and include those copies in the bag total. Missing keys have
infinite cost; an implementation must recompute bounded-degree sums or track
infinity counts rather than subtracting infinity from infinity.

With exact row costs, let `m_h` be the allowed-grid minimum and `U` the best
original-feasible incumbent after the current DP pass. For a cell `C`, let
`q_C` be its smallest finite bag min-marginal over its corners. Fixed-cell
rounding proves

```
q_C-E_h <= F(x)  on the current physical domain with x_B in C.
f* <= U <= m_h <= f*+E_h.
```

Retaining exactly `q_C-E_h <= U` therefore preserves every original
optimizer, including all tied optima and all incident cells at a boundary.
Every retained cell has a single complete feasible grid witness `y` with
`F(y)=q_C <= f*+2E_h`. An old incumbent may leave the retained domain; it
continues to be feasible for the original domain and remains a valid upper
bound. A final whitelist alone is insufficient for global certification;
retain the pruning/DP trace or permit its recomputation.

The current statements supply all these ingredients. In particular, none
assumes independent adaptively retained cells. Sources: the quadratic and
mixed notes, §§2–3; polynomial note, §2; original deterministic review,
`sparse-bag-cell-review.md`, §§1–4.

**The box count and expected work.** Condition only on noise outside a fixed
bag. Form `V_B` by minimizing over the original outside mixed product domain,
not a sample-dependent retained domain. For a fixed outside point,
`F_0(v,x_out)-L v_i^2/2` is concave in `v_i`; its infimum is concave too.
The entire bag-noise vector is absent from `V_B`. A witness of gap at most
`2E_h` implies necessary comparisons at `v +/- a_i e_i`, with
`a_i=h` for continuous coordinates and `a_i=max(1,h)` for integers.
They restrict each regular `gamma_i` to an interval of length at most

```
L a_i + 4E_h/a_i.
```

For a fixed full-grid tuple the interval endpoints are independent of all
other bag coefficients. The coefficient tests therefore multiply. There
are at most three exceptional coordinate nodes, at most `w_i/a_i` regular
nodes, and finite-grid interval mass at most `length/(2 sigma)+1/M`.
Summing the resulting deterministic tuple probabilities gives

```
E[number of qualifying bag tuples]
 <= product_(i in B)
    [3+Lw_i/(2 sigma)(1+n h^2/(2 a_i^2))+w_i/(M a_i)].
```

Choosing `M >= 2^J` with `h_j=s 2^-j` and `w_i <= s` makes every atomic
correction at most one through the cap `J`. Each retained cell is incident
to a qualifying corner. Corner incidence, children, and child corners each
contribute at most `2^p`; generating level `j` is charged to retained
parents at level `j-1`. Initial lists have at most a constant to the `p`
rows. Sorting costs at most `R log R`; even the full deterministic grid has
polynomial logarithmic size for `j <= J`, so this remains polynomial
overhead times `R`. DP values sum only polynomially many assigned factor
costs, which keeps their bit length polynomial independently of the number
of table rows. These points justify a first-moment bound on total work
without any product of expectations or higher-moment assumption.

**Finite sampling, ties, and the fallback budget.** The point-growth modulus
is zero on nonunique draws. For every positive threshold `epsilon`, the good
event is exactly

```
exists a in X, for all x in X:
F_gamma(x)-F_gamma(a) >= epsilon ||x-a||^2.
```

It uses two quantified blocks, one scalar free coefficient, and fixed
degree. Native integer label disjunctions can be exponential in the base
encoding, but their logarithmic length is polynomial and they add no blocks.
Renegar's block-sensitive format bound gives at most
`C_tail=2^poly_d(I)` interval/point pieces in every scalar section, uniformly
over the threshold and all fixed real coefficients. Remove identically
zero output polynomials before counting roots. The real-coefficient
uniformity is needed during replacement of continuous marginals by discrete
ones. The endpoint-inclusive uniform `M`-grid has CDF discrepancy at most
`1/M`; each interval or point contributes at most `2/M`. Replacing marginals
one at a time gives

```
Pr[g_* < epsilon] <= W epsilon/sigma + 2n C_tail/M.
```

For the active continuous gradient, condition away its own noise and fix an
integer assignment and original continuous face. The free stationary
equations omit that coefficient. Positive point growth makes the relevant
free Hessian nonsingular; only those roots need be counted. Their isolated
complex-root count is at most `max(1,d-1)^k`, even if other stationary
components are singular or have positive dimension. At each counted root
the active gradient is `gamma_i+b`, producing an interval of length
`2 tau`. The bound is an unconditional intersection with positive growth;
it is not a conditional probability after conditioning on a good event.

The general fallback selects the same lexicographically least optimizer in
every coordinate formula. Compactness justifies successive coordinate
minimization even for a continuum of optima. Separate scalar formulas use
`exists candidate, for all competitor` and one free scalar for a coordinate
or value. Their format factor is base-only exponential. Coefficient height
enters a fixed polynomial factor, rather than an exponent depending on
dimension. A singleton must be a root of a nonconstant output atom: away
from all atom roots the formula has locally constant truth value. Taking
the squarefree product, isolating all roots, and evaluating atom signs
therefore selects its unique value. Refining stored roots adds requested
precision polynomially. The same enlarged base budget must dominate both
construction/output and later refinement/feasible-gap work.

The constructive box fallback independently passes this audit. The symbolic
even-degree perturbation has pairwise coprime leading powers and a finite
monomial quotient for every nonzero parameter. Normalize each multiplication
characteristic polynomial at its lowest Laurent power before specializing
to zero. A convergent sequence of perturbed minimizers on one fixed face
then yields roots containing an original optimizer. Spurious coordinate-root
tuples are harmless because they are filtered for original feasibility.
For exact comparisons, multiplying each algebraic coordinate by its integer
defining polynomial's leading coefficient makes it integral; a nonzero
integer field norm gives the stated separation from zero. This handles
exact ties, inclusive endpoints, and reducible defining polynomials without
a common primitive element. Its degree, height, and comparison precision
are base-exponential times polynomial in new coefficient bits.

Choose a base-only budget `B`, then
`rho=1/(4B)`, `g_0=rho sigma/(2W)`, and `tau=rho sigma/(2K)`. Compute the
level cap from these quantities and uniform derivative bounds. Only then
choose `M` to cover the cap and atomic corrections. In the box variants,
`M >= max(2,2^J,4n C_tail/rho,2K/rho)` makes each bad event at most `rho`.
For order exposure gaps the correction is `2/M`, requiring `4K/rho`.
Failure of closure is contained in the union, of probability at most
`1/(2B)`. Invoke the all-draw fallback on that same objective. Its cost
`B poly_d(I+log M+q)` and possible exponential output/refinement size then
have polynomial expectations. This is a specified base-chosen fine finite
law, not a theorem for every atomic law. Tied atoms are covered and must
not be discarded or resampled. Sources: tail note, §§2–5; both fallback
notes; polynomial main note, §5; their independent completed-text reviews.

For quadratics, the specialized rational fallback is smaller: enumerate
integer labels and original continuous faces, solve stationary systems
only on positive-definite free Hessians, and include vertices. On an
optimal integer slice choose a minimizer with a smallest-dimensional
containing face. Its free Hessian is PSD. A nonzero kernel direction would
leave the quadratic value unchanged until reaching a smaller optimal face,
a contradiction. Thus this list contains a rational global optimizer even
on flat or tied draws. Do not transfer this finite stationary-face argument
to general polynomials. Sources: quadratic note, §6; mixed quadratic note,
§5, lines 307–316.

**Closure and meaningful exact output.** Intersection of incident bag
projection hulls contains every original optimizer. Fix an integer only
from a singleton hull. A strictly positive gradient enclosure forces an
original continuous lower endpoint; a strictly negative one forces an
original upper endpoint. This uses first-order optimality in the original
box within an optimizer's integer slice. An artificial hull endpoint and
an integer derivative sign do not support the same argument.

After all integers and certified continuous bounds are substituted, let
`C` be the remaining continuous hull box. With midpoint `c`, largest
half-width `r`, and a bound on the absolute third-derivative row sums,
symmetry gives `||H(x)-H(c)||_2 <= T r`. The rational test

```
H(c)-(Tr+g_0)I positive definite
```

certifies a strongly convex patch containing every global optimizer. Its
unique constrained minimizer is an exact global optimizer. Remove and
record singleton continuous coordinates before evaluation. With no free
coordinates, return the fixed feasible point. The certificate does not
trust growth or active margins. Those conditions prove stopping only:
the `2E_h` witnesses lie within `h sqrt(nL/g_0)/2` of the unique optimizer;
adding cell width bounds the hull by `A h`, `A=2+nL/g_0`. The three cap
inequalities in the polynomial note fix integers, detect active continuous
bounds, and leave positive matrix slack. Two-sided Taylor expansion in
the remaining original-interior directions gives `H(a) >= 2g_0 I`.
It needs no quantitative lower bound on inactive primal slacks.

The exact successful output is the objective and verified patch whose
unique constrained minimizer denotes the point, or an equivalent KKT
description. Its compact descriptor has polynomial encoding length. The
global pruning proof trace has the expected work/size bound, not a
polynomial bound on every successful draw. Exact algebraic coordinates or
the expanded optimal value are not required on successful draws. An
arbitrary-precision evaluator does not imply exact comparison with an
arbitrary rational threshold or discovery of the exact active set.

The revised evaluator accounts for both parts of the GLS weak-optimization
contract. For `|f| <= V`, the capped epigraph
`K={(x,t):x in C, f(x)<=t<=V+2}` contains a known ball centered at
`(midpoint(C),V+1)`, of radius the smaller of `1/2` and the least positive
box half-width. Translate by this rational center for the circumscribed
body convention. Rational tangent planes and box/cap inequalities give
polynomial-bit separation. Weak optimization returns an approximately
feasible point and compares against the eroded body. Homothety toward the
known center gives

```
t <= f* + [1+(2V+1)/r_K] epsilon.
```

Projection onto the box is nonexpansive; with a valid gradient norm bound
`G`, the feasible upper value satisfies `U <= t+(G+1)epsilon`. Hence

```
[t-[1+(2V+1)/r_K]epsilon, U]
```

is a certified objective interval of width at most
`[G+2+(2V+1)/r_K]epsilon`. Its required tolerance has polynomial bit
length even for thin boxes or exponentially small `g_0`. Strong convexity
turns an objective gap at most `min(2^-q,(g_0/2)2^-2q)` into point error
at most `2^-q`, including a boundary minimizer. The earlier claim that GLS
directly returns exact epigraph feasibility is superseded by this proof.

**Explicit polynomial graphs.** The global free coordinates remain
ambient coordinates and range over a mixed product box. An acyclic
dependent graph has fixed polynomial degree and fixed dependency depth;
all additional output bounds must be redundant. Expanding each original
bag by all free ancestors of its variables contains every reduced factor.
The bags containing one free coordinate are a union of original occurrence
subtrees connected through parent-child constraint bags. This establishes
running intersection, not just scope containment. The equality scopes
must therefore be covered by the supplied decomposition. With at most
`k` parents and depth `D`, a safe size bound is `p' <= p max(1,k^D)`.
Composed degree is fixed, so explicit substitution and its coefficient
arithmetic have polynomial base size.

Conditioning on all dependent-coordinate noise leaves exactly the original
independent free linear coefficients. Choose curvature, derivative,
scalar-section, active-root, and fallback bounds uniformly over the entire
dependent-noise box before sampling either group. Their format and degree
are base-fixed; sampled coefficient heights enter only polynomial factors.
Apply the box theorem conditionally and then average. The curvature in
the count is that of the pulled-back objective, including dependent
linear-noise terms. A bounded inverse alone does not preserve conditional
noise, and an ambient diagonal bound alone does not bound pulled-back
curvature. The two counterexamples in the graph note, §5, demonstrate
both failures exactly.

At evaluation, map a feasible rational free point through the explicit
polynomials. This gives rational ambient coordinates satisfying every
graph equation exactly. Derivative bounds of polynomial encoding length
supply the extra free precision needed for ambient Euclidean accuracy.
Independent rounding of dependent outputs would lose equality feasibility.
This corollary is complete; it does not imply arbitrary coupled
inequality constraints or arbitrary-depth polynomial composition.

**Monotone implicit graphs.** Each dependent coordinate solves one
fixed-degree polynomial equation involving its own dependent coordinate
and a retained support. A positive rational derivative floor and endpoint
brackets hold on the entire real retained hull times the dependent interval.
These are global premises, including between integer labels. Individual
queried brackets do not prove them. They give one smooth scalar-root chart
everywhere; roots at output interval endpoints still have smooth local
extensions. Dependent bounds are branch selectors and redundant feasible
restrictions, which is why no dependent-bound KKT multipliers are needed.
A singleton dependent interval can be substituted because its equation
then vanishes throughout the retained hull.

Rational sign bisection gives root brackets, and implicit differentiation
through order three gives polynomial-bit value, gradient, and Hessian
enclosures. Intersect denominator intervals with the known positive floor
before division. The derivative order and reciprocal powers are fixed;
the cost depends polynomially on encoded conditioning and precision, not
its numerical reciprocal. Expand scopes as in the one-layer graph proof,
and condition on all dependent noise before the retained bag count.

Because grid costs are usually algebraic, use certified rational lower
row costs, each assigned once, with total error `D_h <= E_h`. The lower-cost
DP is exact rational arithmetic. Update the incumbent with `m_h^-+D_h`,
attached to its actual implicit feasible witness. The same cell test
`q_C^- - E_h <= U` preserves every optimizer and gives

```
G(witness_C) <= q_C^-+D_h <= f*+2E_h+2D_h <= f*+4E_h.
```

Refine reused rows whenever the level error budget decreases. The widened
witness tolerance changes the count's curvature/noise factor from `1+n/2`
to `1+n`. Different bag evaluations may use different root brackets; each
contains the same exact root, so global consistency is unaffected.

The closure test includes certified derivative errors:

```
g_hat +/- (M_1 r+epsilon_g),
H_hat-(Tr+epsilon_H+g_0)I positive definite.
```

With `epsilon_g <= tau/8`, `epsilon_H <= g_0/8`, and the stated mesh cap,
the gradient enclosure has error at most `3tau/4` from an active optimal
derivative, and the tested Hessian has slack at least `g_0/4`. All tests
remain sound on bad draws.

The active-gradient tail is proved by a polynomial KKT system with
`k+2m` unknowns: `q=0`, `L_y=0`, and `L_u=0`. Here `q_y` is diagonal
invertible. Its nullspace basis is `Z=[I;-q_y^-1 q_u]`. A kernel of the
bordered Jacobian reduces to a kernel of `Z' H_L Z=H_reduced`; positive
growth eliminates it. The remaining multiplier kernel is eliminated by
`q_y'`. Thus the relevant roots are nonsingular, and the fixed-degree
isolated-root bound applies even with other singular components. The own
coefficient of a fixed active retained coordinate is absent from this
system and enters its active reduced derivative with coefficient one.
The graph-assisted growth formula still has two blocks; only retained
noise marginals are replaced, giving atomic correction `2n C_tail/M` even
though the quantified dimension is `n+m`.

The exceptional fallback must use the original explicit polynomial graph
domain. The reduced algebraic objective is not an explicit polynomial and
cannot be fed to the box fallback as if it were one. Adding graph variables
to the candidate/competitor blocks preserves the format/height separation.
For successful evaluation, a value enclosure and an approximate gradient
give the valid rational lower plane
`ell+g_hat'(z-x)-beta diam_1(C)`. Failure to separate bounds vertical
epigraph error; the ordinary GLS homothety and clipping repair then applies.
Allocate additional error for a rational upper enclosure of the feasible
algebraic objective value. An exactly feasible output point consists of
rational retained coordinates and their unique scalar-root equations;
rational ambient enclosures need not satisfy the equations. These are
fully developed contracts, with no hidden exact ordering of algebraic sums.

**Product simplices.** Blocks are disjoint unit resource simplices or unit
probability simplices, and each bag contains a whole block whenever it
contains any coordinate from that block. Native integer coordinates may
also occur. Correlated feasible block rounding requires the block matrix
bound `H_BB <= L I`; diagonal bounds alone are insufficient. Bounds for
midpoint gradients and Hessian variation must hold on the enclosing
coordinate box because a coordinate-hull midpoint can lie outside a simplex.
Both distinctions are explicit in the final note.

A cube intersected with a simplex at mesh `h=1/m` scales to
`[0,1]^b` intersected with an integer sum inequality or equality. Its
vertices are cube corners: two fractional coordinates admit an exchange,
and one fractional coordinate is either movable or forced integral by
the active integer budget. Every point therefore has mean-preserving
rounding to feasible corners with trace covariance at most `b h^2/4`.
On shared supporting faces the expected nonnegative slack is zero, so
rounding stays on that face almost surely. This proves preservation of
every incident bag cell, including boundary-only cells. Before unit
resolution use the original simplex vertices; their variances obey the
same coarser bound. No triangulation or factorial incidence is needed.

The outside domain is fixed because bags contain whole disjoint blocks.
Conditional minimization preserves block semiconcavity. Stratify a node
by its original simplex face. On a slack face compare in directions `e_i`;
on a tight face compare in directions `e_i-e_anchor`. Condition on each
fixed anchor coefficient. The remaining tests use independent original
coefficients, with interval length at most `Lh(2+n/2)`. A face of dimension
`r` has `binom(m-1,r)` relative-interior grid points, canceling the `h^r`
probability factor. Sum faces and then multiply joint bag probabilities;
do not multiply expectations of separately filtered blocks.

For inequality-simplex blocks the three sound forcing rules are positive
partial implies a zero coordinate, negative partial implies tight budget,
and positive derivative difference implies the first coordinate is zero.
These use descent in the original simplex. For original equality-simplex
blocks omit both absolute-gradient tests and use only transfers. The
equality multiplier has no sign or positive-margin requirement. Active
zero-coordinate multipliers are derivative differences from any positive
support anchor. No lower bound on that anchor's value is needed.

For multiplier tails, transform tight-face coefficients into tangent
differences and unchanged normal coefficients. The transform is unimodular
but its output law is dependent. Count transformed tuples instead of
assuming conditional independence: tangent differences have at most
`2M-1` labels, unchanged coefficients have `M`, and a normal multiplier
slab permits at most `tau(M-1)/sigma+1` labels. The resulting per-face
factor `2^k max(1,d-1)^k (tau/sigma+1/M)` is sound.

After face fixing, tangent bases have `I <= Z'Z <= nI`. The generalized
matrix test subtracts `(Tr+g_0)Z'Z`, which preserves the physical metric.
The relative evaluator is complete: substitute singleton blocks; strict
rational centers exist in every remaining box-and-budget block; drop an
anchor in equality blocks; and compute a polynomial-bit interior ball.
Projection onto each reduced box/sum slab is rational via a common clipping
threshold and sorted rational breakpoints. Its nonexpansiveness supports
the GLS repair. The original-coordinate error tolerance must retain the
copy-basis norm factor, as in the final note. Arbitrary affine simplex
images and overlapping budgets are outside this theorem.

**Order constraints: unified statement and stronger count.** Use the mixed
order theorem as the manuscript's main order result. Let `N` be the number
of continuous coordinates, `p` the maximum scalar bag size, and `q` the
maximum continuous bag size. With binary remaining coordinates, a fixed
degree explicit objective, full ambient Hessian upper bound `H I` on
`[0,1]^n`, and decomposition bags covering all factor scopes and order
edges, the supported bound is

```
C_0^p q! (q+1) [2+3NH/(4 sigma)]^q poly_d(I).
```

The all-binary case is ordinary exact finite-state DP. The all-continuous
case specializes to

```
C_0^p p! (p+1) [2+3nH/(4 sigma)]^p poly_d(I).
```

This improves the earlier continuous bracket
`[2+nH(p+1)/(2 sigma)]^p`. The proof uses existing transport in the
mixed note, §§3–4, rather than a new assumption. The older continuous
affine-fiber/chamber lemma remains correct and may be omitted or moved to
an appendix. It should not be used to force the weaker bracket into the
unified theorem.

Here is a self-contained reconstruction of the improvement. Fix a bag's
binary row and condition on all coefficients except its continuous noises.
The conditional value includes the fixed bag-binary noise constant. Take
a deterministic feasible continuous bag tuple `v`, its smallest standard
order-simplex face, and one conditional minimizing full point. List the
distinct interior bag knots with endpoints zero and one. For a target `w`
in the closed same face, apply to every full coordinate the nondecreasing
piecewise-affine map carrying those source knots to the corresponding
target knots while fixing zero and one. It preserves order and every
binary label. For this fixed source, the full vector is affine in `w`,
with nonnegative row coefficients of sum at most one and zero derivative
on binary rows.

The transported objective is a feasible upper support for the conditional
value and agrees at `v`. Whole target fibers need not agree, especially
at endpoints where new binary labels become feasible. Upper support is
the direction the comparison proof needs. For a successive face-vertex
difference `a`, its entries are zero or one on disjoint supports. Every
transported derivative entry along `a` lies in `[0,1]`, and only `N` rows
move. Thus `||J a||^2 <= N`, and its directional second derivative is at
most `NH`, without a factor for the support size. A point of true gap at
most `eta h^2` must therefore satisfy a noise interval of length at most
`(NH+2eta)h` in each such direction.

Select one original continuous noise coefficient from each disjoint support
and condition on the others. The remaining tests are independent. A
`k`-dimensional face has at most `h^-k/k!` relative-interior grid points.
Sum its scalar interval probabilities, all faces of the `c!` simplices,
and the at most `2^z` binary rows of a bag. This yields

```
2^z c! sum_(k=0)^c binom(c+1,k+1) A_h^k/k!
 <= 2^z c! (c+1)(1+A_h)^c,
A_h=(NH+2eta)/(2 sigma)+1/(Mh).
```

The common-threshold feasible rounding has `E_h=NHh^2/8`, since binary
coordinates are fixed. Retained witnesses have gap at most `2E_h`, so
`eta=NH/4`. With `Mh >= 1`, the asserted stronger bracket follows.
The construction also covers tied coordinates, endpoint faces, cyclic
orders, and nonconvex projected mixed fibers. Sources: mixed note,
lines 111–228; its independent review, §§1–2. This strengthening is
proved here as a specialization, not claimed as a new contribution.

For rounding, use one common threshold for all ordered coordinates.
Its scalar map is monotone, mean preserving, and fixes grid nodes and
binary endpoints. A full Hessian upper bound is needed for this correlated
rounding; the box diagonal parameter cannot replace it.

For closure, first fix every binary coordinate from its singleton hull.
Continuous exposure tests on the unfixed mixed relaxation are unsound.
The explicit counterexample in the mixed note, lines 264–270, has mixed
optimum `(1/2,1)`, growth one, and a false relaxed exposure gap nine for
`x=z`. Once the binary labels are fixed, the continuous slice has zero-one
vertices. At every optimizer its true slice gradient exposes a linear
optimal face. If an equality were absent, a vertex in that face would
lie in the opposite endpoint face. Hence an LP gap greater than
`N delta`, where `delta` bounds gradient error in infinity norm, soundly
forces the equality at every optimizer. The gap is `N`-Lipschitz, not
`2N`-Lipschitz: compare opposite and unrestricted minimizing vertices,
whose difference has one-norm at most `N`.

For an active continuous order edge, fix the sum of its two coefficients
and vary their difference. The restricted stationary roots on the minimal
face remain fixed; at each root that is actually optimal the opposite-face
gap changes with slope of absolute value one. Its small nonnegative gap
event lies in an interval of length `tau`. Count at most `2M-1` sum fibers
and divide by `M^2` to obtain `tau/sigma+2/M` per counted root. This avoids
the false assumption of a uniformly bounded conditional density on short
sum fibers. Bound constraints use a single coefficient. Union over minimal
faces, nonsingular roots, and fixed binary assignments is analysis only;
the solver never enumerates them.

After certifying all active equalities, substitute block copies and retain
every remaining order inequality. Either use the weighted test in the
face-closure note, subtracting `(Tr+g_0)D'D`, or the conservative unweighted
test in the composition, subtracting `(NT r+g_0)I`. Do not omit metric
factors by mixing these two versions. Bound propagation, singleton removal,
cycle contraction, and removal of tautological rows give the relative
affine hull. LP supplies a rational strict center and polynomial-bit
inradius. The feasible repair clips to propagated intervals and takes
predecessor maxima. It preserves the same infinity error from any feasible
comparison point; with the gradient one-norm bound it supplies the GLS
objective repair. Binary endpoint bounds must be propagated before repairing
fallback approximants so that a small positive continuous approximation
cannot move a binary zero. Original-coordinate Euclidean accuracy retains
the block-copy norm factor. These closure/evaluation proofs are complete.

**Actuator dynamics.** The reduction assumes rational affine state
dependence `s_(t+1)=a_t s_t+g_t(u_t)`, a fixed-degree polynomial in each
own control, strict contraction `|a_t| <= a < 1`, and affine costs in the
dependent states. Additional free-variable polynomial factors may be
nonconvex and coupled, provided their entire scopes fit the supplied
free-variable decomposition. Full-control-hull interval invariance makes
state bounds redundant; there are no extra terminal, path, or control
constraints. Inward integer rounding and empty-domain detection occur
first. At fixed degree invariance is decidable in polynomial bit time by
univariate derivative-root comparisons.

Condition on dependent-state noise. The backward recurrence
`lambda_H=c_H+eta_H`, `lambda_t=c_t+eta_t+a_t lambda_(t+1)` gives

```
sum_(t=1)^H (c_t+eta_t)s_t
 = a_0 lambda_1 s_0 + sum_(t=0)^(H-1) lambda_(t+1)g_t(u_t).
```

Only unary factors are added to the free cost, so degree and bag size
remain fixed regardless of horizon. The remaining initial-state/control
noises remain independent. Uniform adjoint bounds yield uniform curvature
and higher derivative bounds before sampling. The same format/height
separation then supplies one common finite law and fallback budget.
Noise on fixed free variables contributes a sampled additive constant
that must be restored to all reported values.

An exact free optimizer plus the recurrence specifies one common exact
trajectory. Rational free approximants produce exactly feasible rational
trajectories. The control polynomial is evaluated at its own control;
the state update is affine in the previous state. Denominator bit lengths
therefore add over the horizon rather than being repeatedly powered.
Geometric convolution bounds the Euclidean trajectory map by a rational
constant with polynomial logarithmic size, for example
`1+(1+G_1)/(1-a)`. Extra free precision gives full-trajectory accuracy,
and the adjoint identity transfers objective gaps exactly. This result
is complementary to bounded-depth explicit graph substitution and the
local monotone inverse chart. Arbitrary nonlinear state recurrence,
nonlinear dependent-state cost, or extra constraints are not covered.

**The dimension barrier must remain.** In the connected clique-plus-path
quartic example, diagonal curvature is `L=2`, widths and noise scale are
fixed, and every global optimizer is a vertex. Completing any bag corner
by an optimal vertex outside it changes the objective by at most `3p/40`.
The global allowance `E_h=nh^2/4` consequently retains all cells whenever
`h^2 >= 3p/(10n)`. The last such dyadic clique bag has at least
`(5n/(6p))^(p/2)` cells on every noise draw. During those levels the hull
is the original box, its gradient takes both signs, and its midpoint
Hessian is negative definite. The stated whole-hull tests and scheduled
fallback cannot bypass the count. The interaction graph has actual
treewidth `p-1`.

This excludes `f(p) poly(I)` retained-state work for these specified rules
under fixed numerical scales; it does not exclude FPT for another method.
The example itself is easy by binary endpoint DP. A direct replacement of
the global error by a bag-local error is also unsound: the referenced star
quadratic's optimizer-containing cell has `q_C=23/32`, incumbent zero, and
invalid local correction `1/8`. Its outside-grid error varies with the
separator value and does not cancel under message normalization. The
local-error note's conditional recourse interface is sufficient if supplied,
but it is not a developed efficient oracle or an FPT theorem. Sources:
global-error barrier, §§2–4; its review, final two paragraphs;
`local-error-recourse-interface.md`, §§1–3.

**Preliminary TU and general-polytope scope.** The supplementary
`research-20261002/new-direction/tu-feasible-rounding.md` proves a rounding
lemma, not an expected exact optimization theorem. Its precise model is
continuous `P={x in [0,1]^n:Ax<=b}`, with integral totally unimodular `A`,
integral `b`, and dyadic coordinate cells. In scaled cell coordinates,
`Az <= b/h-Ak`, `0<=z<=1` has integral right-hand side and integral vertices.
Thus every feasible cell point admits a mean-preserving distribution on
feasible corners with mean-square error at most `nh^2/4`. Fixing original
grid-boundary coordinates gives the same simultaneous whitelist and
specified-cell preservation used above. A full Hessian upper bound on the
original coordinate box gives objective error `nLh^2/8`. Integer coordinates
already fixed in a slice cause no difficulty; this is not a theorem for
rounding arbitrary unfixed integer ranges or arbitrary mixed TU systems.

Rational right-hand sides require `b/h` integral on the initial and all
later grids, or another proved compatible alignment. Starting at a fine
alignment may have a large numerical state cost; denominator clearing
does not erase that cost. Under equality `x_1=x_2` and objective
`2x_1x_2`, feasible mean-preserving corner rounding incurs positive error
despite zero pure coordinate second derivatives, so even TU constraints
do not permit the box diagonal-curvature proof. Sources: TU note, lines
14–55, 57–94.

The lemma supplies feasible rounding and hence conditional cell lower
bounds if a correct sparse DP enforces every constraint in a containing
bag. It supplies neither an input-controlled expected count nor an exact
closure/evaluation theorem. General TU feasible fibers vary with bag
values, so the box proof's global coordinate semiconcavity may fail.
The supplementary `polyhedral-chamber-count.md` proves that, for a fixed
compact continuous polytope and fixed smooth objective, the expected
number of truly `O(h^2)`-near-optimal bag tuples remains bounded as
`h -> 0`. Its constant depends on the recourse chambers, their geometry,
and affine-pullback curvature, with no favorable input-complexity bound.
Its finite-law version also requires `Mh>=1`. This is a complete
qualitative counting result, not a fixed-width expected bit-work result
or a complete algorithm. Sources: that note, lines 3–18, 20–67, 69–141.
The order theorem is the developed constrained specialization that
controls these counts and supplies exact closure. The paper may include
the TU lemma and fixed-polytope result as supporting results or scope
boundaries, but must not state an unrestricted TU optimization theorem.

**Manuscript conditions that cannot be compressed away.** Use fixed explicit
degree and factor scopes inside primal decomposition bags; carry the
post-rounding nonempty, closed, bounded domain premise. State numerical
width/curvature/noise dependence and fixed-width expected polynomial work,
with no FPT claim or polynomial dependence on binary integer-width encoding
alone. Distinguish a valid curvature/global-chart input premise from an
independently verified certificate: use concrete monomial bounds or count
a supplied polynomial-time proof verifier. Keep the point-growth convention
at a single optimizer, global optimizer preservation, one feasible witness
per retained cell, one pre-draw law, and same-draw fallback. Distinguish
compact descriptors from expected-size global traces and exact implicit
feasibility from rational numerical enclosures. State reduced curvature
for graphs, block curvature for simplices, and full ambient curvature for
orders. Preserve equality-simplex rule changes, binary-before-exposure
ordering, and all GLS feasibility/erosion corrections.

**Original reviews used.** The mathematical reconstruction was compared with
the complete-file records in `new-direction/sparse-bag-cell-review.md`,
`sparse-bag-cell-noise-review.md`, `sparse-mixed-bag-cell-review.md`,
`sparse-mixed-bag-noise-review.md`,
`smoothed-sparse-polynomial-independent-review.md`,
`simplex-block-noise-review.md`, and `order-polytope-independent-review.md`;
and in `reviews/smoothed-sparse-polynomial-review.md`,
`polynomial-finite-noise-tails-review.md`,
`polynomial-exact-fallback-review.md`, `global-error-cell-barrier-review.md`,
`smoothed-polynomial-graph-review.md`, `implicit-graph-oracle-review.md`,
`implicit-graph-tail-kkt-review.md`, `implicit-graph-composition-review.md`,
`smoothed-implicit-graph-composition-review.md`,
`simplex-block-closure-review.md`, `smoothed-mixed-order-review.md`, and
`smoothed-polynomial-actuator-dynamics-review.md`. Their previous checks are
reported evidence and were not rerun. Their main resolved corrections—GLS
repair, trace size, full-hull graph premises, simplex ambient-box derivative
bounds, and binary-before-exposure order—are present in the final source
versions. Use the final notes rather than earlier proposed interfaces.

**Verification performed in this audit.** Read-only targeted commands were
`cat AGENTS.md`, `cat paper-smoothed-global/evidence/BRIEF.md`, `rg --files`
and scoped `rg -n` for the assigned notes and reviews, `wc -l` on those
files, and `nl -ba ... | sed -n ...p`/`cat` for their mathematical text.
The proof inequalities, dimensions, interval counts, and complexity
separation were rederived analytically above. The targeted document check
actually run was:

```sh
python3 - <<'PY'
from pathlib import Path
import re
root = Path('/workspace/minlp-notes')
p = root / 'paper-smoothed-global/evidence/reviews/prewrite-sparse-sol.md'
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
assert len(re.findall(r'^```', s, re.M)) % 2 == 0
refs = sorted(set(re.findall(r'`(research-20261002/[^`]+\.md)`', s)))
assert all((root / r).is_file() for r in refs)
print(f'PASS: scoped report format and {len(refs)} explicit source paths; {len(s.splitlines())} lines')
PY
```

Result: passed final-newline, trailing-whitespace, fenced-block parity, and
existence checks for all 18 fully spelled-out source paths. These are local
targeted document checks. No optimizer experiment, project-wide verification,
or CI result is asserted.
