# Smoothed polynomial optimization with certified approximate recourse

Date: 2026-10-02. Status: independently reviewed; targeted exact checks
passed. This extends the
[excluded-region recourse mechanism](smoothed-box-stable-recourse.md)
to nonlinear recourse whose values need not be rational. It uses certified
objective intervals and feasible rational completions, never exact
comparisons between algebraic recourse values.

## 1. Interface, concrete class, and output

Let `F_0` be an explicitly encoded rational polynomial of fixed degree `d`
on `[0,1]^n`. Supply a core `C` with `k` continuous coordinates and residual
coordinates `R`. Supply rational `L>0` with

\[
                \partial_{ii}F_0(x)\le L\quad(i\in C,
                                      \ x\in[0,1]^n).          \tag{1}
\]

Assume a **box-stable approximate recourse algorithm**: for any rational
core point, any rational residual subbox, any rational added linear term,
and any rational `eta>0`, it returns a rational lower value `ell` and a
feasible rational completion of value `u` satisfying

\[
                  \ell\le V\le u,\qquad u-\ell\le\eta,       \tag{2}
\]

where `V` is the global conditional optimum on that subbox. Its bit work,
output length, and verification cost are polynomial in query length and
`log(1/eta)` when `eta<1`; equivalently, polynomial in the binary encoding
of `eta`. The exponent is independent of `k`. Empty boxes are reported.
The restriction is to continuous variables throughout this note.

A concrete sufficient class is a polynomial with a verified residual
convexity certificate

\[
                  \nabla^2_{RR}F_0(x)\succeq0
                        \quad(x\in[0,1]^n).                 \tag{3}
\]

Core fixing, linear noise, and residual box restriction preserve (3).
The residual objective may be nonlinear, nonseparable, and not strongly
convex. Section 2 derives (2) from classical rational convex optimization.
Neither (1) nor (3) is assumed to be polynomial-time decidable from an
arbitrary polynomial. For a verifiable global proof record, use direct
coefficient bounds for (1), or supply a sharper checkable proof; supply
a polynomial-time-verifiable proof of (3) or another established oracle
interface. Include their sizes and verification costs in input length `I`.

For rational `sigma>0`, there is a base-computed power of two `M` with
`log M=poly_d(I)` such that independent noise in **all** coordinates,

\[
 \gamma_i\ \text{uniform on}\
 \{-\sigma+2\sigma j/(M-1):0\le j<M\},                       \tag{4}
\]

admits exact global optimization of `F_gamma=F_0+gamma^T x` on every
draw, with expected bit work and expected output/proof-record size

\[
 8^k\left[3+\frac{(1+k)L}{2\sigma}\right]^k
                    \operatorname{poly}_d(I).                \tag{5}
\]

The usual output is a rational restricted box and fixed original-bound
coordinates with a verified positive Hessian modulus. Its unique
constrained minimizer, expressed as `argmin` or by its polynomial KKT
system, specifies an exact global optimizer and value. This compact
descriptor has polynomial length and admits `q`-bit point/value evaluation
in `poly_d(I+q)` time. The exceptional output is an exact real-algebraic
optimizer and value obtained by general fallback on the same draw. That
representation, its evaluation, and the full global proof trace may be
large. Initial work, output size, and proof-record costs obey (5).
Subsequent `q`-bit evaluation has expected cost `poly_d(I+q)` once the
descriptor's global validity has been established. No expanded algebraic
output bound is asserted on every draw, and the usual branch's entire pruning record has
only an expected size bound.

The parameter is the supplied continuous core dimension and its numerical
curvature/noise ratio. This is not a treewidth-only or binary-encoding-only
numerical bound. It requires no growth or local-Hessian promise and does
not assert exact optimization of the unperturbed objective.

Remove fixed coordinates first and handle empty or singleton domains
directly. For `k=0`, keep a single empty core query; all counting factors
are constants and the same residual localization/closure proof applies.

## 2. Convex recourse needs no strong-convexity modulus

Fix the core, noise, and a rational residual box, substitute zero-width
coordinates, and call the restricted polynomial `f`. Under (3) it is
convex. The objective-interval part of the
[convex-patch evaluation lemma](convex-patch-evaluation.md) uses convexity
alone; its positive modulus is needed only for converting value accuracy
to distance accuracy.

More explicitly, choose polynomial-bit rational bounds `|f|<=W` and
`G_f>=max(1,sup ||grad f||_2)` on the query box `B`. The capped epigraph
`K={(z,t):z in B, f(z)<=t<=W+2}` has a known rational center, inner radius
`r_K=min(1/2,min positive half-width)`, and outer radius of polynomial
encoding length. Box inequalities, the epigraph cap, and the rational
tangent inequality at a queried rational point give strong separation;
normalize each nonzero separator by its infinity norm.

Use the precise GLS weak-optimization guarantee documented in the linked
lemma: the returned `(z,t)` is within `epsilon` of `K`, and its height is
compared with the `epsilon`-eroded body. Homothety toward the known inner
ball gives

\[
 t\le f^*+A_f\varepsilon,\qquad
 A_f=1+(2W+1)/r_K.
\]

Clip `z` to the rational box, obtaining an exactly feasible point `y`.
Nonexpansiveness and the gradient bound give
`f(y)<=t+(G_f+1)epsilon`. Thus

\[
 [\ell,u]=[t-A_f\varepsilon,f(y)],\qquad
 \varepsilon=\min\{r_K/2,\eta/(A_f+G_f+1)\}                 \tag{6}
\]

satisfies (2). All quantities have polynomial bit length, including for
thin query boxes. If no coordinate remains, direct evaluation suffices.
The linked lemma gives the direct GLS Turing-model source and the
near-feasibility repair; no exact-real optimization oracle or unproved
exact epigraph feasibility is being used. Exact algebraic minimizers are
unnecessary for these calls.

For the concrete convex class, a classical tangent bound makes each
returned certificate directly checkable without retaining the convex
solver's execution. Compute `K_f>=1` bounding
`sup_B ||H_f||_2 max(1,diam B)^2`, and first obtain a feasible `y` with
objective error at most

\[
             \delta=\min\{\eta/2,\eta^2/(8K_f)\}.
\]

Return `u=f(y)` and

\[
 \ell=f(y)+\min_{z\in B}\nabla f(y)^T(z-y).
 \tag{6a}
\]

The linear minimum is an explicit rational endpoint choice in each
coordinate, and convexity proves `ell<=f*`. To bound the certificate gap,
let `z` be such a minimizing endpoint vector and let `gap=u-ell`.
The smoothness bound along the feasible segment gives, for `0<t<=1`,
`f*<=f(y)-t gap+K_f t^2/2`, hence
`gap<=delta/t+K_f t/2`. Take `t=min(1,eta/(2K_f))`. If `eta<=2K_f`,
the last bound is at most `eta/2`; otherwise it is less than `3eta/4`.
Thus (2) holds. All extra precision lengths remain polynomial. A verifier
checks the feasible rational point, its value and gradient, the endpoint
linear minimum, and `u-ell<=eta`, using the supplied convexity proof;
it does not need to trust the convex solver's internal stopping decision.
No strong-convexity modulus is used in this certificate.

## 3. Core cells with inexact conditional values

Let `V(v)=min_z F_gamma(v,z)` on the original residual box. For fixed
residual noise, `V(v)-gamma_C^T v` is independent of the entire core-noise
vector and has upper coordinate curvature `L`. Use nested dyadic core
cells of side `h_j=2^-j`; query only corners of children of retained cells.
At a corner use (2) with

\[
                    \eta_j=e_j=kLh_j^2/8.                    \tag{7}
\]

Set `U_j=min u(v)` over the current queries and retain a cell when
`min_corner ell(v)-e_j<=U_j`. Interpolation preserves every optimizer
cell. Its corners and the oracle error give

\[
 U_j-f^*\le2e_j,
 \qquad \text{each retained cell has a corner }v
                   \text{ with }V(v)\le f^*+4e_j.             \tag{8}
\]

Choose a corner `c_j` attaining `U_j` and its rational completion `w_j`.
It survives and belongs to the retained core hull `D_j`. The hull contains
the core projection of every original optimizer.

For a `4e_j`-near-optimal core tuple, the two neighboring inequalities at
an interior coordinate confine its independent noise to an interval of
length at most `Lh_j+8e_j/h_j=Lh_j(1+k)`. Hence, for `M>=2^J`, the same
conditional finite-grid calculation as the exact-recourse theorem gives

\[
 \mathbb E[\text{near-optimal tuples at level }j]
 \le H=\left[3+\frac{(1+k)L}{2\sigma}\right]^k,
                         \qquad j\le J.                     \tag{9}
\]

Adaptive oracle choices may depend on all noise; (2) still implies the
necessary event in terms of the true value function, so they do not spoil
noise conditioning. Cell incidence, child generation, and corner queries
cost at most `2^k+8^k HJ` in expectation. No full fine grid is generated.

For `k=0`, replace (7) by `eta_j=2^-2j`, set `e_j=eta_j`, and use one
empty core cell and query. Then `U_j-f*<=e_j`; the weaker bound (8) still
holds. Set `D_j` to the empty-coordinate singleton with diameter zero.
This convention permits residual localization even without a core.

## 4. Certified exclusion and nonlinear convex closure

Compute rational coefficient bounds on the original unit box:

\[
 \begin{split}
 M_1&\ge\max\{1,\max_i\sum_j\sup|\partial_{ij}F_0|\},\\
 T&\ge\max\{1,\max_i\sum_{j,l}\sup|\partial_{ijl}F_0|\},\\
 G&\ge\max\{1,\sum_{i\in C}(\sup|\partial_iF_0|+\sigma)\}.
 \end{split}                                                   \tag{10}
\]

These have polynomial bit length for fixed explicit degree. They bound
gradient variation, Hessian operator-norm variation, and core Lipschitz
variation, respectively. The same `G` applies to conditional values over
every fixed residual subbox.

Choose positive base constants `g_0,tau` below, and set

\[
 r=\min\{1/8,\tau/(16M_1),g_0/(4T)\},\quad
 A_0=2+(kL+8)/g_0,\quad \eta_{\rm out}=g_0r^2/16.             \tag{11}
\]

The harmless `8/g_0` term accommodates the empty-core convention and
does not enter (9). At a level, center the residual patch `P` of radius
`r` at the residual part of `w_j`, clipped to original bounds. Query (2)
at `c_j` with accuracy `eta_out` on each closed slab
`z_i<=w_{j,i}-r` or `z_i>=w_{j,i}+r` whose raw threshold lies strictly
between zero and one. Omit a side at or beyond an original bound. These
at most `2|R|` subboxes cover the complement of `P`. Let `ell_out` be
the minimum returned lower value, or `+infinity` when there is no slab.

If

\[
          \ell_{\rm out}-U_j>2G\operatorname{diam}_\infty D_j, \tag{12}
\]

then every conditional optimizer over every core point of `D_j` lies in
`P`. Indeed, a restricted value at another core point is at least its
value at `c_j` minus `G diam_inf D_j`, while the unrestricted value is
at most `V(c_j)+G diam_inf D_j<=U_j+G diam_inf D_j`. Using a certified
lower excluded value, rather than an excluded feasible value, is essential.
Thus every original global optimizer lies in `D_j times P`.

Use rational derivative bounds to fix original-bound coordinates with a
uniform strict gradient sign on this box. A sufficient test evaluates the
gradient at the box midpoint and uses `M_1` times its infinity radius for
each error bound. Only fix a bound contained in the coordinate interval.
After these sound fixings, call the remaining rational box `Q`, its
midpoint `m`, and its infinity radius `r_Q`. Check exactly

\[
          \nabla^2 F_\gamma|_Q(m)-(Tr_Q+g_0)I\succeq0.       \tag{13}
\]

Hessian variation then proves uniform strong convexity of modulus `g_0`
on `Q`. Together with global containment, this is the exact implicit
output certificate. If no variable remains, direct evaluation supplies
the exact point and value. All accepted certificates are sound without
probabilistic assumptions.

Until closure succeeds, these are temporary patch tests: later core
queries still optimize over the original residual box defining `V`.

For termination analysis, suppose the draw has point growth at least
`g_0` at its unique optimizer `a`, with every active original-bound
gradient of magnitude greater than `tau`. Equation (8) implies that `D_j`
lies within `A_0h_j` of `a_C` coordinatewise and
`||w_j-a||<=A_0h_j`. These estimates also hold for the stated `k=0`
convention. If

\[
 h_j\le\min\{r/(4A_0),\ g_0r^2/(16GA_0)\},                \tag{14}
\]

then `||w_j-a||<=r/4` and `2e_j<=g_0r^2/16`. Each closed excluded slab
lies at distance at least `3r/4` from `a`. Its approximate lower value
therefore gives

\[
 \ell_{\rm out}-U_j
 \ge (9/16)g_0r^2-\eta_{\rm out}-2e_j
 \ge (7/16)g_0r^2
 > 2G\operatorname{diam}_\infty D_j.                         \tag{15}
\]

Here (14) bounds the last comparison term by `g_0r^2/4`. Every point of
`D_j times P` is within `5r/4` of `a`. A midpoint gradient test differs
from the true optimizer gradient by at most `5M_1r/4`, and its extra
midpoint-radius error is at most `M_1r`; their sum is less than `tau/2`
by (11). Thus all original active coordinates are fixed, while an
original free coordinate cannot pass a strict sign test because its
gradient at `a` is zero.

On the remaining free coordinates, two-sided Taylor expansion of growth
gives `H(a)>=2g_0 I`. Because `a in Q` and `r_Q<=r`,
`H(m)>=2g_0 I-Tr_Q I`. Consequently (13) holds with slack at least
`g_0-2Tr>=g_0/2`. This proves exact closure by the base-only cutoff (14),
including arbitrary original-bound contacts.

## 5. Fixed finite sampling, fallback, and evaluation

Use the [polynomial finite-noise tails](polynomial-finite-noise-tails.md).
They provide a base-computable `C_tail=2^{poly_d(I)}` such that

\[
 \Pr\{g_*<\epsilon\}\le n\epsilon/\sigma+2nC_{\rm tail}/M,
\]

and an active-gradient bound `K(tau/sigma+1/M)` on positive-growth draws,
where `K=max(1,n3^n max(1,d-1)^n)`. The section-count bound is independent
of thresholds and sampled coefficient height; the finite law includes
all exceptional atoms.

The [exact polynomial fallback](polynomial-exact-fallback.md) supplies
a base-computable `B=2^{poly_d(I)}>=2` dominating its bit work, output
size, and subsequent coordinate/value refinement, apart from fixed-degree
polynomial factors in additional sampling and requested precision bits.
Set

\[
 \rho=1/(4B),\qquad g_0=\rho\sigma/(2n),\qquad
 \tau=\rho\sigma/(2K).                                      \tag{16}
\]

First compute (10)--(11) and the least `J>=0` satisfying (14). Then choose
the least power of two

\[
 M\ge\max\{2,2^J,4nC_{\rm tail}/\rho,2K/\rho\}.             \tag{17}
\]

Every quantity preceding `M` is base-only; `J,log M=poly_d(I)`. The two
failure events each have probability at most `rho`, so unresolved draws
have probability at most `1/(2B)`. Invoke the general exact fallback on
that same draw. No draw is rejected or resampled. Expected fallback work,
output size, and evaluation work are polynomial.

For each level, oracle accuracies (7) and (11), query coordinates, and
returned rational witnesses have polynomial encoding length. Each core
query and each of the at most `2n` additional slab calls therefore costs
`poly_d(I)`. Derivative bounds, rational PSD tests, and list management
also have polynomial bit cost. Combining this with (9) proves (5).

The usual output's polynomial has fixed degree and explicit rational
coefficients, and its patch endpoints and modulus `g_0` have polynomial
bit length. The convex-patch evaluation lemma gives a feasible rational
point and value interval of width `2^-q` in `poly_d(I+q)` time. Using
objective accuracy at most `min(2^-q,(g_0/2)2^-2q)` also gives Euclidean
point error at most `2^-q`. This evaluation statement needs neither an
exact active-set decision nor expanded algebraic coordinates.

## 6. Scope of the new mechanism

The concrete residual-convex class permits dense nonlinear coupling among
arbitrarily many residual variables. Only the supplied core contributes
to the exponential state-count factor. In particular, it need not be a
quadratic negative-inertia decomposition, a low-rank concave penalty, or
separable scalar recourse. For illustration,

\[
 F_0(v,z)=\psi(v)+\sum_i z_i^4+\|Dz-Ev\|_2^2
\]

has jointly convex residual recourse for any rational matrices `D,E`
and fixed-degree rational `psi`; the residual Hessian is a sum of PSD
terms. More general couplings can satisfy (3) as well. This example
illustrates the interface, not a hardness or prior-priority claim.

A [separate dense nonlinear family](polynomial-recourse-rank-separation.md)
has one core coordinate with curvature independent of an arbitrarily large
core-residual coupling scale. Every fixed PSD quadratic correction making
that family jointly convex has rank at least the residual dimension.
This shows that a small coordinate core need not arise from a small-rank
fixed quadratic concave penalty. The lemma concerns that particular
representation; it does not exclude more general difference-of-convex
methods or imply hardness.

The theorem combines established convex optimization, finite-noise tails,
and real-algebraic fallback with the excluded-region certificate. Its
additional content over the quadratic recourse result is that certified
approximate solves suffice throughout, while a base-only nonlinear
Hessian test still yields finite exact implicit output. No general
efficient recourse construction for sparse nonconvex residuals is claimed.

## 7. Verification status

The targeted command
`python research-20261002/reviews/check_polynomial_box_recourse.py`
passed a genuinely nonlinear recourse fixture at the base cutoff stage 42.
Its full quartic objective is nonconvex, its residual restriction is
jointly convex, and its stationary cubic is irreducible modulo three, so
the optimizer is provably irrational. A rational bisection oracle with
convex tangent lower bounds made 109 bisections and certified five excluded
slabs. The resulting patch passed the uniform active-bound gradient test
and exact rational midpoint-Hessian test. The
[diagnostic](../reviews/check_polynomial_box_recourse.py) also checks the
four directly checkable full-box tangent certificates in (6a) and the
empty-core budget, and demonstrates why an excluded feasible upper value
cannot replace its certified lower value. It is a fixture oracle, not a
GLS implementation or a duplicate of the existing core-cell algorithm.

The [independent completed-text review](../reviews/smoothed-polynomial-box-recourse-review.md)
found no substantive gap, including in the compact tangent certificates,
the empty-core convention, the nonlinear cutoff, and the fixed finite law.
It requested only that the initial construction bound be distinguished
from the precision-dependent evaluation bound; that clarification is
included in Section 1. The coordinating researcher separately read the
complete proof and checked the new constants. An
[independent significance assessment](polynomial-box-recourse-significance.md)
records its structural scope and limitations.

Scoped local links, math delimiters, and whitespace checks passed. No
index edits, project-wide tests, or CI inspection were performed.
