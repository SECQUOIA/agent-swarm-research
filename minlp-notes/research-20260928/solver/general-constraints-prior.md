# Prior audit: sparse kernels with general local constraints

Date: 2026-09-28. This is an independent literature and significance audit
of the support-repair extension. It does not certify that
extension's proof.

The strongest comparison is not the 2025 effective Putinar bound. A May
2026 lift-and-project theorem, combined with the May 2026 nearly quadratic
box theorem, already gives the older **dense ordinary-module** rate
`O((log^(3/2)(R)/R)^alpha)`. The same lifting argument preserves a bag tree
and transfers that rate from a sparse box theorem. A July 2025 preprint by
Tran and Toh already proves the dense preordering rate `O(R^-alpha)` by
moment approximation and feasible projection. Neither the algebraic
exponent nor projection onto the feasible set is an independent discovery
of this extension.

The accompanying theorem note proves a direct-transport refinement to
`O((log(R)/R)^alpha)`, improving the logarithmic factor over that stated
ordinary-module composition. Its independent proof review and targeted
checks are recorded separately. The sparse construction also rounds
compatible overlapping bags without an attained polynomial separator
dual. These are the specific additions to assess. The improvement over
the inspected combination is not an originality claim: an equivalent
direct result may exist, and this source audit does not certify the
transport proof or settle priority.

## Candidate and exponent convention

Let a running-intersection bag tree support an objective
`f=sum_b f_b(x_Bb)` and polynomial inequalities `g_j(x_Bj)>=0`. Include
the coordinate inequalities `1-x_i^2>=0` in every owning bag's ordinary
quadratic module. Let `K` be their common nonempty feasible set in the
cube. The assumption is the **global** error bound

\[
 \operatorname{dist}(x,K)\le H V(x)^{\alpha/2},
 \qquad V(x)=\sum_j(-g_j(x))_+^2,
 \quad x\in[-1,1]^n,
 \tag{1}
\]

with `0<alpha<=1`, matching the kernel note's squared-violation convention.
If `v_j=(-g_j)_+` and there are `m` constraints, then
`max_j v_j <= sqrt(V) <= sum_j v_j <= sqrt(m V)`. Thus replacing
`sqrt(V)` by the maximum or the sum changes constants only for fixed
`m`. Sources using `dist(x,K)^L<=c max_j v_j` use `L=1/alpha`;
sources using `dist(x,K)<=c(max_j v_j)^L` use `L=alpha`. Confusing
these conventions would invert the rate.

The baseline ordinary-module objective rate obtained by lifting is

\[
 O\!\left(\left(\frac{\log^{3/2}R}{R}\right)^\alpha\right),
 \tag{2}
\]

with local degree cutoff `2R`. The theorem note's direct-transport refinement is
`O((log(R)/R)^alpha)`, discussed separately below. The logarithm-free
preordering version needs more than the ordinary local module:
box-preordering positivity, including
the products `g_j` times every box-generator product used by the kernel.
It must identify that strengthened cone exactly.

## Primary comparisons

**Heijmans-Kuryatnikova, Vera, Zuluaga, “Degree Bounds for
Positivstellensätze of general semialgebraic sets,” arXiv:2605.15821v2,
20 May 2026.** Theorem 4 gives ordinary-module degree
`O(epsilon^(-2L))`, and Theorem 6 gives full-preordering degree
`O(epsilon^(-L))`, for fixed data. Their global distance convention is
equation (9). The key reusable result is Theorem 2: a fixed-degree
polynomial lift on a higher-dimensional box preserves the polynomial
after substitution and has condition number `O(kappa^(2L))`. The
ordinary-module projection uses fixed certificates for bounding
generators. The authors explicitly discuss applying their transfer to
other coefficient norms. This source is more directly relevant than
earlier effective-positivity estimates.
[Primary text, Theorems 2, 4, 6 and final remarks](https://arxiv.org/html/2605.15821v2).

**Gribling, de Klerk, Vera, “Squared polynomial approximation kernels for
the hypercube: improved error bounds and implications for Lasserre
hierarchies,” arXiv:2605.31496v1, 29 May 2026.** Theorem 7 gives the
dense ordinary-box-module bound `C(n,d)||f||_(1,cheb) log^3(R)/R^2`.
For fixed dimension and degree, equation (3) controls the coefficient
norm by the uniform norm. Thus it applies uniformly to the fixed-degree
lift as its penalty coefficient changes. The exact composition is
derived below. Neither dense box convergence nor its dense constrained
consequence can be claimed as a new rate here.
[Primary text, Theorem 7 and equation (3)](https://arxiv.org/html/2605.31496v1).

**Tran and Toh, "On the convergence rates of moment-SOS hierarchies
approximation of truncated moment sequences," arXiv:2507.00572v1,
1 July 2025; published 7 July 2026.** Theorem 4.7 and Corollary 4.8
give dense fixed-degree moment approximation and objective error
`O(R^-alpha)` under a global Hölder distance bound. Their exponent `L`
equals `alpha`, unlike the reciprocal convention above. They lift
constraint values to a ball-simplex product, approximate moments there,
and project the resulting support onto the feasible set. The formulation
includes an explicit redundant ball inequality. Their reduced cone
`R(X)` still contains every subset product of inequality generators;
it weakens equality handling, not those inequality products. These
theorems therefore do not supply the ordinary-module conclusion or
consistent sparse bag laws. They are nevertheless direct antecedents for
both support repair and the dense preordering exponent. This audit read
the preprint's definitions (2.8), Section 4.2, Theorem 4.7, and Corollary
4.8, and checked the published abstract; it does not attribute uninspected
final theorem numbering to the published version.
[Primary preprint](https://arxiv.org/pdf/2507.00572v1),
[published abstract](https://link.springer.com/article/10.1007/s10107-026-02394-6).

**Korda, Magron, Ríos-Zertuche, “Convergence rates for sums-of-squares
hierarchies with correlative sparsity,” Mathematical Programming 209
(2025), 435–473; online 25 March 2024.** Theorem 8 treats sparse ordinary
modules under running intersection, normalized local Archimedean
certificates, and **local** distance exponents `L_b`. For fixed data its
explicit equations (5)–(6) require `R^2` of order
`epsilon^(-max_b max(A_b,B_b))`, where

\[
 A_b=1+L_b+\frac{4L_b+1}{3}(2L_b+|B_b|+2)
                          \left(1+\frac{8L_b}{3}\right),
 \qquad B_b=\frac{2(12L_b+1)}3.
 \tag{3}
\]

For `L_b=1`, `A_b=(238+55|B_b|)/9`, giving the rate
`R^(-18/(238+55w))`. The source uses coordinatewise degrees; fixed width
converts them to total degrees without changing the exponent. Global and
local error bounds are not interchangeable, as shown below.
[Published primary article, Theorem 8](https://link.springer.com/article/10.1007/s10107-024-02071-6).

**Baldi, Mourrain, Parusiński, “On Łojasiewicz inequalities and the
effective Putinar's Positivstellensatz,” Journal of Algebra 662 (2025),
741–767.** Theorem 3.1 bounds degree using an objective-dependent
Łojasiewicz exponent. Corollary 3.3 substitutes the global distance
exponent and gives degree `O(epsilon^(-(7L+3)))`; this translates to
objective error `O(R^(-alpha/(7+3alpha)))`. Corollary 3.4 gives degree
`O(epsilon^-10)` under constraint qualification. These are important
antecedents, but are superseded as general dense benchmarks by the
May 2026 lift theorem.
[Primary author-hosted published PDF](https://math.univ-cotedazur.fr/u/parus/publis/BMP2025.pdf).

**Baldi and Mourrain, “On the effective Putinar's Positivstellensatz and
moment approximation,” Mathematical Programming 200 (2023), 71–103.**
Theorem 1.8 and Section 5 already bound the Hausdorff distance between
fixed-degree normalized pseudomoments and moments of measures supported
on the feasible set. Hence existence of a nearby supported measure is
not itself new. These bounds follow by convex separation from effective
positivity; the older degree exponent is dimension dependent. They do
not construct compatible bag laws from a sparse pseudomoment point.
[Primary article](https://doi.org/10.1007/s10107-022-01877-6),
[local primary text](../../literature/papers/baldi2023-on-the-effective-putinars-positivstellensatz/fulltext.md).

**Schlosser, “Convergence rate for linear minimizer-estimators in the
moment-sum-of-squares hierarchy,” SIAM Journal on Optimization 35(4)
(2025), 2599–2622.** The accessible arXiv text transfers effective
positivity estimates to convergence toward measures supported on global
minimizers, and hence to linear minimizer estimates. This is a stronger
target support than feasibility for near-optimal pseudomoments, with
additional objective geometry. It must be distinguished from a
constructive sparse rounding theorem for every feasible pseudomoment
point. This audit examined the arXiv version; its numbering and bounds
should not be silently attributed to an uninspected final version.
[Primary preprint](https://arxiv.org/html/2502.18370),
[published article](https://doi.org/10.1137/25M1739716).

**Henrion and Safey El Din, “Convergence rate of the moment-SOS hierarchy
for univariate polynomial optimization,” arXiv:2609.20544, 17 September
2026.** Theorem 1 gives `O(R^-2)` for every fixed polynomial problem on
a nonempty bounded subset of the line, with arbitrary polynomial
inequality generators. Theorem 2 gives a matching quartic example with
gap `1/[2R(R-1)]`. Degenerate generators affect its constants rather
than the exponent. Section 5.3 also reduces a bivariate cusp to a
univariate problem. Consequently a global Hölder exponent is an upper
bound mechanism, not evidence that the resulting hierarchy exponent is
intrinsic. This audit checked the theorem statements and supporting
reductions, not every proof in this recent preprint.
[Primary PDF, Theorems 1–2](https://arxiv.org/pdf/2609.20544).

## Why the dense exponent is already a composition of prior results

Here is an explicit inference from the two May 2026 sources. Normalize
the fixed constraints so `|g_j|<=1/2` on the ambient cube. For
`p_epsilon=f-f*+epsilon`, the lift has the form

\[
 F_\varepsilon(x,u)=p_\varepsilon(x)
             +M_\varepsilon\sum_j(u_j-g_j(x))^2,
 \qquad u\in[0,1]^m,
 \tag{4}
\]

where `M_epsilon=O(epsilon^(1-2/alpha))` suffices. To see the scaling
directly, Lipschitz continuity and (1) bound the possible loss below
`f*` by a constant times
`[sum_j(-g_j(x))_+^2]^(alpha/2)`. Young's inequality absorbs this term
into a multiple of the squared residual plus `epsilon/2`.
Thus `F_epsilon>=epsilon/2` and its coefficient norm is
`O(epsilon^(1-2/alpha))`. Its degree is independent of `epsilon`.

Applying a `log^3(R)/R^2` box certificate needs

\[
 \frac{\log^3 R}{R^2}=O(\varepsilon^{2/\alpha}),
\]

which gives (2). Substitute `u_j=g_j(x)` to recover
`p_epsilon`. Endpoint and quadratic box generators are interconvertible
at a fixed degree cost, for example
`u(1-u)=u(1-u)^2+(1-u)u^2`. After substitution the generator `1-g_j`
has a fixed ordinary box-module certificate because it is strictly
positive on the cube. Multiplication by squares preserves the module.
All degree costs depend on fixed data, not `epsilon`.

This derivation was checked independently by the audit's child reviewer.
It is a mathematical implication of primary results, not a claim that
the two papers explicitly state their combined corollary.

## The same lift preserves sparse structure

There is a simple sparse version of (4). Keep the original bag tree. For
each constraint, add **one leaf bag** `B_j union {u_j}` attached to an
original bag containing `B_j`. Assign its squared penalty to that leaf,
and keep each `f_b` on its original bag. The new variable occurs only in
its leaf; every original coordinate still has a connected set of bags.
The maximum width increases from `w` to at most `w+1`, not to `w+m`.

An ordinary sparse box certificate for (4), followed by substitution,
therefore yields a certificate in the original sparse ordinary module.
The fixed certificates for `1-g_j` use only its original owner bag.
No polynomial separator-dual attainment assumption is introduced by
this construction.

Accordingly, a reviewed sparse box theorem plus the established lift
already supplies the baseline constrained rate (2), at an order changed
by fixed factors and offsets. It also supplies certificates with any
strictly positive excess margin, without needing strict feasibility of
the original constrained moment SDP. It does not establish certificate
attainment at an exact finite error value.

A direct support-repair theorem can provide a law tied to the supplied
sparse pseudomoments, explicit constraint-residual control, and more
transparent constants. Existence of a nearby supported measure alone is
already prior, both by effective-positivity separation and by Tran--Toh's
projection argument. The additions should be stated as finite quantitative
and sparse consistency results.

## What the sharper transport rate adds

The theorem note's direct estimate controls expected squared constraint
violation by `O(1/s^2)`, while the SOS kernel degree is
`O(s log s)`. Global Hölder repair then costs
`O(s^-alpha)=O((log(R)/R)^alpha)`. The objective smoothing term remains
`O(log^3(R)/R^2)`, which is lower order for every `0<alpha<=1`.

Relative to (2), this removes a factor `log^(alpha/2)(R)` from the
upper bound. It preserves the algebraic exponent `alpha` and the same
global geometric assumption. The black-box lift followed by the stated
Gribling--de Klerk--Vera theorem does not give that improvement: its
penalty coefficient and theorem error lead exactly to (2). A sharper
analysis of the prior kernel is a plausible source of a new refinement,
not a reason to claim a new kernel or a new dense algebraic exponent.

For `alpha=1`, the existing sparse affine-recourse example has an
`Omega(1/R)` gap. It makes the inverse-order power sharp for the full
class with a global linear error bound. It does not prove that a
logarithm is necessary for the ordinary module, or establish sharpness
for every `alpha<1`. Faster dense or univariate results are compatible
with that sparse lower bound.

## Global geometry can be much worse than local geometry

This independent example explains a limitation of comparing (2) with
(3). On `[0,1]^T`, impose

\[
 x_{i+1}=x_i^2\quad(1\le i<T),\qquad x_T=0,
 \tag{5}
\]

using paired polynomial inequalities. The bags `{x_i,x_(i+1)}` form a
path, and the last constraint has a singleton bag. Each graph constraint
has a linear local distance bound: changing only `x_(i+1)` to `x_i^2`
repairs it within distance `|x_(i+1)-x_i^2|`. The terminal equality also
has a linear bound. Nevertheless the full feasible set is `{0}`.
At the point `x_i=t^(2^(i-1))`, all graph equations hold and the only
positive violation is `t^(2^(T-1))`, so `sqrt(V)` has this value,
whereas its distance to `{0}` is at least `t`. Thus (1) cannot hold
with `alpha>2^(-(T-1))`.

Local exponent one under running intersection therefore does not imply
global exponent one. The candidate improves a rate under controlled
global geometry; it does not uniformly dominate the published local-
geometry sparse theorem. This example concerns repair geometry, not a
lower bound on the sparse hierarchy itself.

## Remaining claims to avoid

- A global semialgebraic error bound exists for fixed nonempty `K`, but
  its exponent and constant may deteriorate with the whole constraint
  system. Fixed bag width alone does not control them.
- A nearest-feasible-point operation can be a global nonconvex
  optimization problem. Existence of a rounded supported law does not
  by itself give a fast feasible-point algorithm.
- Primal strict feasibility of the unconstrained box moment SDP need
  not survive added constraints, especially when `K` has empty
  interior. Certificate attainment at the exact displayed error needs
  a separate argument; an arbitrarily small extra positive slack is a
  different statement.
- A prior full-preordering rate alone does not give a rate for the weaker
  cone containing only box products and single `g_j` multipliers. The
  kernel note proves the result for that explicitly specified cone.
- The July 2025 and February 2026 Magron slides already assert the sparse
  box-preordering `R^-2` rate. The existing
  [ordinary-module source audit](sparse-putinar-prior.md) records the
  discrepancy with the published theorem. A constrained consequence
  cannot reset priority for that prerequisite.

## Search and verification record

The audit read the published Korda–Magron–Ríos-Zertuche theorem,
the author-hosted published Baldi–Mourrain–Parusiński PDF, the local
Baldi–Mourrain primary text, and the primary arXiv versions linked above.
Searches included the terms “sparse Putinar quantitative Łojasiewicz,”
“moment approximation concentration,” “polynomial kernel constraints,”
and “Putinar lift-and-project,” followed by bibliography tracing from
the September 2026 univariate paper. Secondary search summaries were
used only to locate primary texts.

The closing audit independently reopened the primary lift theorem and
its proof, the dense kernel theorem and its kernel identities, and the
published sparse theorem's equations (5)--(6). It additionally read
Tran--Toh's primary preprint Section 4.2 and definitions (2.8), rather
than treating its abstract's reference to moment-SOS hierarchies as a
claim about ordinary modules. Follow-up searches used the exact dense
kernel identifier with "constraint", and Putinar, logarithms, and
Łojasiewicz terms. No matching logarithm-refined constrained theorem was
located in those inspected sources; this bounded search does not prove
that none exists.

An independent child audit checked the strongest dense comparison and
the composition of the two May 2026 theorems. No computational test or
Lean proof was needed for this literature audit. It is not exhaustive,
and it does not establish novelty by failure to locate an equivalent
statement. It establishes a concrete prior implication that materially
narrows the candidate contribution.

The closing pass ran
`git diff --no-index --check /dev/null research-20260928/solver/general-constraints-prior.md`;
it reported no whitespace errors. This checks file formatting only.
No project-wide verification or CI inspection was performed.
