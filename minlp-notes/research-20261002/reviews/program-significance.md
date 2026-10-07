# Program significance and strongest next opportunity

Date: 2026-10-02. This is a fresh significance assessment of the October 2
program. It is not another full proof audit or an external priority search.
The local theorem drafts, independent reviews, and current prior-art audits
were read. A delegated reviewer independently challenged the stable-control
applications and their simpler dynamic-programming baselines. No knowledge
base files were read or changed by this assessment.

## Assessment

The program now has a plausible main theoretical contribution: a certified
global algorithm whose dependence on numerical accuracy is polynomial in
the number of requested bits, while structural parameters enter separately.
The strongest proposed formulation is the forthcoming exact rational
continuous box-QP theorem with running time

    f(p,k,kappa) poly(I),       kappa=max(1,M/g),

where the polynomial exponent is independent of bag size p, variable
occurrence k, and conditioning kappa. The proposed approximate version has
poly(I+q), for error 2^(-q). This would improve the earlier shared-grid
result's width-dependent polynomial exponent, rather than just restate
polynomial solvability at fixed width. The new
[bit-complexity draft](../geometric-dp/regridded-qp-bit.md) was written
during this assessment and its statement, Taylor model, denominator
invariant, operation count, and bit-budget schedule were then read. Its
final proof review remains authoritative. This significance assessment does
not replace that separate adversarial review.

If that theorem survives its current audit and the focused prior-art
comparison, it is the best candidate for a coherent main result. It concerns
a recognizable exact optimization class beyond the forest-QP boundary
reported in the literature audit, removes the generic exact-convex-oracle
qualification, and changes the parameterized complexity statement. The
nonlinear feasible-repair theorem is the most promising application-facing
extension, but its current exact-real formulation has a substantial
implementation gap. The finite-optimum and screening results are useful
supporting material, not competing headlines.

There is still insufficient evidence for a major practical MINLP advance.
No end-to-end implementation demonstrates competitive certificates on a
nontrivial family, and several constants can be huge even in the displayed
examples. A correct conditioned FPT theorem can be worth publishing without
that empirical claim. Its contribution should be stated at that level.

## What is substantive and what is established machinery

The current [literature audits](../prior-art/geometric-grid-prior.md) already
identify continuous graphical-model DP, certified interval DP, geometric
refinement, trajectory recentering, exact sparse-QP algorithms, and rational
QP height bounds. The [optimum-set audit](../prior-art/optimum-set-grid-audit.md)
also identifies adaptive refinement around several minima and classical
quadratic-growth theory. These mechanisms individually are not defensible
novelty claims.

The candidate distinction is the entire algorithmic guarantee: full-domain
lower certificates remain valid at every stage; minimizing configurations
generate new centers; aggregate quadratic-growth contraction gives the
rate; and sparse decomposition allows the rate to depend on bag dimension
instead of ambient dimension. The announced quadratic specialization makes
the local lower model affine, so minimizing it over a leaf/separator box
intersection requires only corners. Rational coordinate and message
denominators then stay polynomial in bit length across stages. The standard
height theorem finally turns certified approximation into exact recovery.

The exact rational recovery step is a valuable consequence, but its
originality rests on the preceding runtime, not on continued fractions or
Cramer's rule. Likewise, globally valid regridding is more than a local
trajectory-refinement heuristic, but the present audits establish only a
scoped negative literature finding. They do not establish priority.

## Ranking the current results

| Rank | Result | Why it matters | Material limit |
| --- | --- | --- | --- |
| 1 | Announced rational continuous box-QP FPT theorem | Separates parameter dependence from input and accuracy-bit exponents; removes nonlinear local oracles; yields exact rational output | Requires unique optimum, useful global growth, supplied decomposition, and bounded occurrence; final proof review is ongoing |
| 2 | Rebuilt continuous certificates, including nonlinear stable dynamics | Finds centers and feasible incumbents with global certificates; nonlinear outer strips plus adjoints preserve second-order error after repair | Generic oracle counts are not Turing time; invariant boxes and stable repair exclude important coupled constraints |
| 3 | Shared coordinate grids and exact mixed-integer box-QP corollaries | Covers large integer intervals and explicit finite modes; requires only upper coordinate curvature; exact rational arithmetic is already developed | At present the exponent on input/accuracy bits grows with width; continuous-indicator constraints are not automatic product boxes |
| 4 | Coordinate-anchor optimum-set theorem | Measures projected optimal values instead of the number of full optima; removes an artificial uniqueness restriction | Work contains powers of anchor count and accuracy bits depending on width; positive-dimensional optimal sets can still force fine grids |
| 5 | Random screening and component enumeration | Gives a clean exact expected-polynomial regime on unbounded-treewidth graphs | Sparse potentially active sets are the key restriction; proof is a modest combination of safe screening and percolation |

The first two rows have different strengths. The box-QP result is the more
precise complexity contribution. The nonlinear repair result reaches a
more recognizable constrained-control setting. Adding many nearby
corollaries will not by itself make either result more important.

## Assumptions that can carry the difficulty

**Global growth is a global separation parameter.** A feasible point at
distance D from the unique optimizer and objective gap delta forces
g<=delta/D^2. The existence of some positive g for a unique compact box-QP
does not supply a useful bound. The current proofs correctly use g only
for complexity, with certificates valid independently of it. That is a
real advantage: the method does not ask the user to prove a difficult
global condition before trusting an answer. It does not make the
condition harmless in a runtime claim.

Growth is not equivalent to convexity, a Polyak--Lojasiewicz inequality, or
easy local optimization. Even separable smooth functions can have a uniform
quadratic lower bound around a unique optimizer and exponentially many
strict local minima across coordinates. Thus the hypothesis does not make
the theorem vacuous. Conversely, a nonconvex Hessian somewhere is too weak
a demonstration of useful scope. The current affine and nonlinear quartic
examples expose their zero optimizer immediately through a sum of
nonnegative terms. They verify assumptions and cancellation, but do not
show a difficult optimization problem becoming tractable.

**Occurrence is not treewidth.** A width-one edge-bag decomposition of a
star repeats the center in order n bags. The proposed FPT statement must
retain k explicitly. A supplied decomposition is part of the input;
neither finding a suitable decomposition nor replacing it with one of
simultaneously small width and occurrence is free. The full bag-Hessian
constant M also depends on the supplied factor allocation, and can be
larger than a global Hessian bound when factors cancel. The announced
theorem is consequently not FPT in treewidth and spectral conditioning
alone.

**The finite-optimum parameter is not automatically small.** The anchor
theorem's A=sum_i |pi_i(S)| can be exponentially smaller than |S|, which
is useful. It can also be exponentially large in input length. Even when
A is polynomial, the present total work contains (T+1)^(p+1), where T
counts failed anchor solves. Thus this extension does not inherit the
announced FPT statement merely because the unique-optimum theorem does.
The separable double-well example illustrates the parameter distinction;
ordinary separability already solves that example. The diagonal-ridge
example is correctly labeled a limitation of the particular certificate,
not an optimization-hardness statement.

**Feasibility repair is strong structure.** An affine retraction mapping
the whole box into a constrained feasible set is much more than an
ordinary Hoffman error bound. In the nonlinear theorem, forward simulation
is feasible for every initial state and control sequence because the
boxes are invariant. There are no extra terminal targets, coupled budgets,
or path restrictions that the repair can violate. These omissions are
material in control and MINLP applications. The cancellation using
adjoints is substantive within that class; the theorem is not a generic
nonlinear-constraint extension.

**Stability and arithmetic remain visible parameters.** Constants grow
with 1/(1-a), derivative bounds, and the curvature of the nonlinear
dynamics multiplied by an adjoint bound. Scalar state is fixed dimension;
vector states would put their dimension in the geometric exponent. The
current nonlinear example's displayed sufficient mesh constants already
give an enormous worst-case count, despite benign data. Its stable map
s->s^2/4 also demonstrates exponential exact rational output length. A
polynomial count of exact simulation oracles does not bypass that issue.
The Turing extension must specify its output, such as exact controls plus
a recurrence representation of states and certified numerical enclosures.

## A tempting extension that should not be a headline

One proposed next step was to derive useful mixed growth from random mode
charges in stable finite-control nonlinear dynamics, rather than assume
it. The isolation argument is sound: with T binary decisions and independent
uniform charges of width delta, the optimal-sequence gap is at least eta
except with probability at most 2T eta/delta. Bounded trajectory diameter
then gives g of order eta/T. This produces a non-planted example with
competing mode-dependent trajectory costs.

However, this polynomial-time capability already follows from an elementary
uniform-state Bellman baseline. For a scalar contractive state map, rounding
each successor to a mesh of spacing h gives

    |s_t - s_hat_t| <= h/[2(1-a)].

With uniformly Lipschitz stage costs, every sequence's total cost changes
by at most E=O(T h/(1-a)). Quantized DP costs O(q T/h) for q actions.
Taking E<eta/4 identifies the exact winning sequence when its gap is at
least eta. Substituting the isolation scale eta=Theta(delta rho/T) gives
polynomial work of order q T^3/[(1-a) delta rho], suppressing fixed domain
and Lipschitz constants. Keeping the two best distinct sequences provides
a deterministic certificate once their rounded gap exceeds 2E. Both
approaches have the same exact trajectory-evaluation caveat.

The parent agent identified a related baseline when the initial state is
continuous but the controls come from a separated finite alphabet. Full
mixed quadratic growth implies a positive objective gap to every different
control sequence. A coarse state DP can find the winning sequence; a
second DP can exclude it by carrying one binary flag recording whether a
control has ever differed, thereby lower-bounding every competing
sequence. Once that lower bound exceeds the incumbent, only the fixed
sequence's continuous initial-state problem remains. Under suitable
fixed-dimensional curvature and growth bounds, ordinary global refinement
can handle that final problem with accuracy-bit dependence. This is a
baseline mechanism rather than a newly completed theorem here, but it
further limits claims for finite-control extensions. Fully continuous
control trajectories have no corresponding discrete-sequence gap shortcut.

The new regridding bound can be worse after substituting its growth
constant. Therefore a smoothed finite-mode corollary is a useful conditioning
example or baseline, but not a new solver capability by itself. The
literature agent was alerted to this comparison. It should not divert work
from the stronger structural question below.

## Strongest next theoretical opportunity

After completing the current FPT proof and Turing extension, prioritize the
following precise question:

> Can rational continuous box-QP under unique global growth be solved in
> f(p,H/g) poly(I) time from a width-p decomposition and a global Hessian
> norm bound H, without a separate occurrence parameter k?

An intermediate theorem with a computable weighted copy-drift parameter
would also be useful if it covers graph families for which k grows with n.
This target improves the main structural scope instead of adding another
special example. It reconciles the strongest existing virtues: shared
coordinate grids need no occurrence bound, while rebuilt certificates avoid
the width-dependent accuracy-bit exponent. A positive theorem would give a
cleaner complexity frontier; a genuine obstruction would identify the
missing parameter rather than merely show that one proof estimate is loose.

There is a concrete algebraic starting point for quadratics. Allocate each
entry of the global Hessian once to a bag, and denote the resulting
symmetric local Hessians by H_t. For any vector v, rowwise
Cauchy--Schwarz gives

    sum_t ||H_t v_Vt||^2
      <= p sum_(i,j) H_ij^2 v_j^2
      <= p ||H||_2^2 ||v||^2.                              (1)

Each row inside a bag has at most p terms, and every coefficient is
allocated once, which proves the first inequality. Thus the linear Taylor
copy-error term can be bounded by

    sqrt(p) ||H||_2 ||x-c|| sqrt(E),

instead of using M sqrt(k)||x-c|| sqrt(E). This removes one source of
occurrence dependence without assuming positivity or ignoring cancellation.
It does not prove the target theorem: unweighted copy drift and the sum
of graded cell widths still contain multiplicity. The next proof task is
to choose weighted local error budgets, representative copies, and cell
grading that control those two quantities in a norm compatible with (1).

Use a star and a fan (a path with one common hub) as the first stress
families. Their decompositions can have many copies of one variable while
the global quadratic norm stays bounded by distributing its couplings.
Any claimed replacement should display constants on these families,
including nonconvex box-QP examples. A result that only renames the old
k-dependent bound does not advance this question. No such replacement has
been proved in this assessment.

For application scope, the next most valuable target is exact-feasibility
certification for nonlinear stable dynamics with continuous controls, a
precise finite-bit output contract, and private finite modes handled by
local enumeration. This should follow the current Turing work, not precede
it. An extension to additional terminal or path constraints needs a new
repair mechanism and is a distinct harder topic. It should not be claimed
from the present invariant-box theorem.

## Recommended presentation and validation

Lead with one uniform complexity theorem, its actual parameters, and the
certificate that a separate checker can validate without knowing g. Present
the mixed grid and nonunique-optimum results as complementary extensions,
with their different parameter exponents explicit. Keep the nonlinear
repair theorem separate until its arithmetic contract is complete.

Before claiming solver significance, exhibit a family with interacting
continuous decisions, cycles in the interaction graph, a non-obvious
optimizer, certified growth constants, and no reduction to separable or
endpoint-only DP. Compare actual state or certificate counts with a uniform
grid and the simpler relevant baseline. This is a targeted demonstration,
not a request for a large benchmark campaign. Its purpose is to show that
the theorem's new scope is populated by more than planted examples.

No project-wide checks, CI inspection, or external search was performed
for this assessment. The mathematical claims in (1) and the uniform-grid
baseline were checked directly; they are supporting deductions, not newly
audited algorithms. External novelty questions were sent to the existing
literature agents, with missing sources routed only through the sole
ingest agent.
