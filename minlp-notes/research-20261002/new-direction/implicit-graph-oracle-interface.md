# Rational oracles and exact closure for implicit polynomial graphs

Date: 2026-10-02. Status: complete interface proof; passed
[fresh actual-file review](../reviews/implicit-graph-oracle-review.md).
No literature-priority claim.

This note supplies the evaluation, approximate-DP, and convex-patch
interfaces for a sparse optimization theorem on implicit polynomial graphs.
It does not prove the required finite-noise tail bounds or choose their
common sampling law. Its exact output uses implicit graph points;
rational numerical approximations to physical coordinates need not satisfy
the graph equations exactly.

## 1. Global graph premises and their verification scope

Let `t` range over a bounded mixed product box `T`, and let `T_hat` be
its full real hull. Round integer bounds inward, reject empty domains,
and substitute fixed anchor coordinates. Dependent continuous coordinates
satisfy

\[
 q_j(t_{S_j},y_j)=0,\qquad y_j\in V_j=[a_j,b_j],
 \tag{1}
\]

where each `q_j` is an explicit rational polynomial of fixed degree.
It depends on anchor coordinates and its own dependent coordinate only.
The intervals are closed and rational. Assume valid supplied rational
bounds `mu_j>0` and the global properties

\[
 \partial_yq_j(t,y)\ge\mu_j
 \quad(t\in\widehat T,\ y\in V_j),
 \qquad
 q_j(t,a_j)\le0\le q_j(t,b_j)
 \quad(t\in\widehat T).
 \tag{2}
\]

These give one root `y_j=psi_j(t)` throughout the real anchor hull.
If `a_j=b_j`, the bracket premise forces `q_j(t,a_j)=0` on the entire
anchor hull. This fixed dependent coordinate can therefore be substituted
without leaving a residual constraint on the anchors.
The implicit function theorem applies at each graph point, including
points on the displayed box boundaries. Thus the chart has smooth local
extensions there and well-defined derivatives on the entire hull.

If no anchor coordinate remains, return this one implicit graph point
and use the scalar evaluation procedure below. The DP discussion assumes
at least one anchor coordinate.

Let the objective on the graph be

\[
 G(t)=F_0(t,\psi(t))+\gamma^Tt+\eta^T\psi(t),
 \tag{3}
\]

where `F_0` is an explicit fixed-degree rational polynomial. The actual
sampled coefficients are rational, with `|gamma_i|,|eta_j|<=sigma` for
a base rational `sigma`. Let `I` include the base formulas, boxes and
supplied bounds, and let `b` bound sampled coefficient lengths. A valid
rational upper coordinate-curvature bound `L>0` for (3) on `T_hat`
is also supplied or derived. Linear anchor noise does not alter curvature.

The global conditions (2) and the curvature bound are mathematical
premises. A certificate claiming independent verification must supply
checkable proofs of them or account for their verification cost. This
note does not infer a polynomial-time algorithm for arbitrary polynomial
positivity from their being stated. Root brackets at individual queried
rows do not replace these global premises: they do not establish global
uniqueness, smoothness, or validity of rounding between grid points.

Assume that the reduced factor scopes have already been assigned once
each to a valid anchor tree decomposition. The scope-expansion and
running-intersection argument are separate structural obligations.

## 2. Polynomial-bit values and derivative intervals

At a rational anchor tuple, scalar bisection uses exact rational signs
of `q_j(t,midpoint)` and maintains a bracket inside `V_j`. A zero sign
identifies an exact rational root; otherwise monotonicity chooses the
correct half. To obtain width `epsilon` takes
`O(1+log_+((b_j-a_j)/epsilon))` steps. Fixed-degree rational evaluation
has polynomial bit cost in the query length and requested accuracy bits.

A row certificate can retain rational endpoints `l_j,u_j` with

\[
 q_j(t,l_j)\le0\le q_j(t,u_j),\qquad[l_j,u_j]\subseteq V_j.
 \tag{4}
\]

The global monotonicity premise proves that these intervals contain the
actual graph values. Rational interval evaluation of the assigned
objective factors then gives certified lower and upper costs. Absolute
monomial sensitivity bounds determine enough root precision for any
desired absolute factor error; cancellations or negative factor values
cause no difficulty. Such sensitivity bounds have polynomial encoding
length. One does not use a possibly negative objective maximum as an
error bound.

For explicit derivative bounds, let `A_j>=1` bound the absolute values
of all partial derivatives of `q_j` through order three on
`T_hat x V_j`. Rational monomial bounds suffice. For individual anchor
derivative entries, valid bounds are

\[
 P_{1,j}=A_j/\mu_j,\qquad
 P_{2,j}=\frac{A_j(1+P_{1,j})^2}{\mu_j},\qquad
 P_{3,j}=\frac{A_j[(1+P_{1,j})^3+
                    3(1+P_{1,j})P_{2,j}]}{\mu_j}.
 \tag{5}
\]

For example, `psi_i=-q_i/q_y`, and

\[
 \psi_{ik}=-\frac{
 q_{ik}+q_{iy}\psi_k+q_{ky}\psi_i+q_{yy}\psi_i\psi_k}{q_y}.
 \tag{6}
\]

Differentiating once more gives the bound in (5). These are entry bounds;
sum the relevant entries when obtaining matrix norms or row sums.
Their encoding lengths are polynomial because the derivative order is
fixed and each positive rational `mu_j` is part of the input.

Use root brackets and (6) to enclose the gradient and Hessian at rational
anchor queries. Before interval division, intersect the denominator
enclosure with the known positive range `q_y>=mu_j`. Refining the scalar
brackets then obtains any specified absolute error in polynomial bit
work. The required reciprocal powers of `mu_j` have fixed exponents,
so their logarithms, rather than their numerical magnitudes, determine
precision. The chain rule and (5) give uniform rational bounds such as

\[
 M_1\ge\max\{1,\max_i\sum_k\sup|\partial_{ik}G|\},
 \qquad
 T_3\ge\max\{1,\max_i\sum_{k,l}\sup|\partial_{ikl}G|\}.
 \tag{7}
\]

They can be chosen uniformly for `|eta_j|<=sigma`; anchor linear terms
do not affect (7). Values, gradients, Hessians, and their rational
enclosures therefore have polynomial precision cost. No exact ordering
oracle for algebraic objective values is being assumed.

## 3. Approximate bag costs preserve rounding and pruning

Let `n` be the number of anchor coordinates and `N` the number of bags.
At a grid level of spacing `h`, put

\[
 E=\frac{nLh^2}{8}.
 \tag{8}
\]

Use the shared mixed partitions and fixed-cell rounding invariant of the
[sparse polynomial box algorithm](smoothed-sparse-polynomial.md). Upper
coordinate curvature gives expected rounded cost at most `G(t)+E`.
The rounding remains in the current bag whitelists, also when one bag
cell is specified. This is rounding in the anchor box, followed by the
exact chart; physical coordinates are not independently rounded.

For every row of bag `B`, compute rational costs with

\[
 \ell_B\le f_B\le\ell_B+\delta_B,
 \qquad D=\sum_B\delta_B\le E.
 \tag{9}
\]

For example, use `delta_B=E/N`. Each assigned factor contributes exactly
once. Reused rows must be refined when the level's error budget decreases.
Let `H^-` be the sum of lower row costs, so `G-D<=H^-<=G` on the grid.
Run exact rational DP on these lower costs. Write `m^-` for its global
minimum and `q_C^-` for the least complete lower cost over corners of
a specified bag cell `C`, obtained from its min-marginals.

Rounding an optimizer gives

\[
 m^-\le f^*+E,
 \qquad
 U\le m^-+D\le f^*+E+D,
 \tag{10}
\]

where the incumbent `U` is updated with `m^-+D`. This is a certified
upper bound attached to the actual implicit graph point of a DP witness.
It may be improved by previous certified incumbents; always `U>=f*`.
The rational approximants used inside bisection are not claimed feasible.

For a cell define `LB_C=q_C^- - E` and retain it when `LB_C<=U`.
Fixed-cell rounding proves `LB_C<=G(t)` for every feasible point in
the corresponding current cell domain. Thus all original optimizers
remain covered. Equality cases must be retained. A retained cell has a
globally consistent anchor-grid witness `v` satisfying

\[
 G(v)\le q_C^-+D\le U+E+D
       \le f^*+2E+2D\le f^*+4E.
 \tag{11}
\]

Negative costs and rational DP ties do not change this reasoning. Sums
contain at most one assigned cost per bag, so rational encoding lengths
grow polynomially with `N` and row precision, rather than with the total
number of table rows.

The conditional semiconcavity counting argument consequently uses near
optimality tolerance `4E`. At a regular node with neighbors at distance
`a`, the admissible anchor coefficient interval has length at most

\[
 La+\frac{8E}{a}=La+\frac{nLh^2}{a}.
 \tag{12}
\]

Hence the box theorem's factor `1+n/2` becomes `1+n`. No conditioning
on successful pruning or positive growth is needed for this deterministic
near-optimality implication.

## 4. Rational derivative certificates close a convex patch

The coordinate projection hulls of the retained cells contain every
optimizer. Intersect hulls from all bags containing each coordinate.
Fix integer anchors only when their resulting hull is a singleton.
The midpoint of a nonsingleton hull may have noninteger coordinates;
the full-real-hull graph premises make derivative evaluation there valid.

For a rational midpoint `c`, let `r` be the largest half-width of the
current hull. Compute a rational vector `g_hat` with coordinate error
at most `epsilon_g`. The intervals

\[
 [\widehat g_i-M_1r-\epsilon_g,
   \widehat g_i+M_1r+\epsilon_g]
 \tag{13}
\]

enclose each gradient component throughout the hull. A strictly positive
interval forces the original lower bound at every optimizer; a strictly
negative one forces the original upper bound. Apply this only to continuous
anchor coordinates, using their original-box first-order condition in
each fixed integer slice.

After all integer anchors have been fixed, substitute them and every
forced continuous original bound. On the remaining rational continuous
box `C`, remove singleton coordinates. Reset `c` and `r` to its midpoint
and largest half-width. Compute a symmetric rational
matrix `H_hat` with

\[
 \|\widehat H-\nabla^2G(c)\|_2\le\epsilon_H.
\]

For example, enclose upper-triangular entries to error at most
`epsilon_H/dim(C)` and copy them symmetrically. Given a rational trial
modulus `g_0>0`, the exact rational test

\[
 \widehat H-(T_3r+\epsilon_H+g_0)I\succ0
 \tag{14}
\]

certifies `Hessian(G)>=g_0 I` on `C`. Indeed, (7) gives operator
variation at most `T_3r`. The patch contains all original optimizers,
so its unique constrained minimizer is an original global optimizer.
No growth or active-margin promise is needed for this certificate's
soundness.

For the stopping argument only, suppose point growth is at least `g_0`
and all active continuous anchor gradients have magnitude greater than
`tau>0`. Equation (11) gives witness radius
`h sqrt(nL/(2g_0))`. The same cell-hull geometry is therefore bounded by
`A h`, with the coarse choice `A=2+nL/g_0`. If

\[
 h\le\min\{1/(4A),\tau/(4M_1A),g_0/(4T_3A)\},
 \quad
 \epsilon_g\le\tau/8,\quad\epsilon_H\le g_0/8,
 \tag{15}
\]

integer hulls are the correct singleton labels. Since `r<=A h`, the
gradient enclosure differs from the optimizer's gradient by at most
`2M_1r+2epsilon_g<=3tau/4`; all active continuous coordinates are
therefore fixed. The remaining original coordinates are interior at
the optimizer, so their Hessian there is at least `2g_0 I` by two-sided
Taylor expansion. The matrix in (14) is at least
`(g_0-2T_3r-2epsilon_H)I >= (g_0/4)I`. Closure succeeds with strict
slack. Exact rational midpoint Hessians must not be substituted for the
certified algebraic derivative approximations used here.

If no anchor coordinate remains, the graph point is fixed implicitly;
its dependent coordinates and objective value can still be irrational.
Return its unique scalar-root descriptions and evaluation oracle rather
than claiming a rational physical point or an exact rational value.

## 5. A rational weak separator for the algebraic convex epigraph

Fix an accepted positive-dimensional patch `C`. Its reduced function `G`
is convex there and supports the value and gradient interval oracles above.
Compute rational bounds `W>=max{1,sup_C |G|}` and
`G_1>=max{1,sup_C ||grad G||_2}` from the original bounded chart and
the derivative bounds. Define

\[
 K=\{(x,s):x\in C,\ G(x)\le s\le W+2\},
 \qquad D_1=\sum_i\operatorname{width}(C_i).
 \tag{16}
\]

Queries outside `C` or above `W+2` have exact rational box or cap
separators. For a query `(x,s)` passing those tests and a requested weak
tolerance `epsilon>0`, compute

\[
 \ell\le G(x)\le u,\quad u-\ell\le\epsilon/2,
 \qquad
 \|\widehat g-\nabla G(x)\|_\infty\le
 \beta=\frac{\epsilon}{2\max\{1,D_1\}}.
 \tag{17}
\]

Convexity gives the valid affine lower bound, for all `z in C`,

\[
 G(z)\ge\ell+\widehat g^T(z-x)-\beta D_1.
 \tag{18}
\]

If `s<ell-beta D_1`, the rational normal `(g_hat,-1)` strictly separates
the query from `K`. Its infinity norm is at least one; dividing by this
norm gives the exact rational normalization required by the GLS weak
separation definition. Otherwise
`G(x)-s<=u-ell+beta D_1<=epsilon`. If the query is below the epigraph,
moving it vertically to `(x,G(x))` reaches `K` within Euclidean distance
`epsilon`; if it is already above `G(x)`, it belongs to `K`.
Thus either answer is a valid weak-separation answer. There is no exact
comparison with the algebraic value or gradient.

Every query and output is rational. Bisection, derivative approximation,
the rational comparison and infinity-norm normalization have polynomial
bit complexity in the patch encoding, query encoding and tolerance bits.
The oracle needs convexity only on `C`; it never evaluates the chart at
an outside-box query.

## 6. GLS evaluation with an approximate feasible value

The rational body bounds and GLS Turing-model reduction from
[convex-patch evaluation](convex-patch-evaluation.md) apply unchanged to
(16). In particular, with midpoint `c`, set

\[
 r_K=\min\{\tfrac12\min_i\operatorname{width}(C_i),1/2\},
 \qquad R_K=D_1+2W+2.
\]

The radius-`r_K` ball about `(c,W+1)` lies in `K`, and `R_K` bounds
its outer radius about the same center. Remove fixed coordinates before
using these positive radii. Their encoding lengths are polynomial even
for very thin patches.

For a desired objective gap `eta>0`, put

\[
 A_0=1+(2W+1)/r_K,\qquad
 C_0=G_1+2+(2W+1)/r_K,\qquad
 \varepsilon=\min\{r_K/2,\eta/(2C_0)\}.
 \tag{19}
\]

Apply GLS weak optimization to `-s` on `K` with tolerance `epsilon`.
The inner-ball homothety and rational box-projection argument in the
linked proof give a rational output `(x,s)`, and its clipped anchor
`v=proj_C(x)`, with

\[
 s\le G^*+A_0\varepsilon,
 \qquad G(v)\le s+(G_1+1)\varepsilon.
 \tag{20}
\]

The source allows approximate feasibility and comparison against an
eroded body; (20) already accounts for both. The homothety also ensures
the eroded body is nonempty for (19).

Unlike polynomial rational evaluation, `G(v)` need not be rational.
Compute a rational upper bound `U` with
`0<=U-G(v)<=eta/2`, using the scalar-root oracles. Return

\[
 [a,U]=[s-A_0\varepsilon,U].
 \tag{21}
\]

Then `a<=G*<=G(v)<=U` and
`U-a<=C_0 epsilon+eta/2<=eta`. The feasible witness is the implicit
graph point `(v,psi(v))`, with the already fixed integer anchors. This
extra upper-value error is necessary; using `U=G(v)` as an exactly
rational value would be incorrect.

All constants and tolerances have polynomial encoding length. The cited
GLS reduction with the polynomial-bit weak separator above consequently
gives polynomial bit work in the patch encoding and `log(1/eta)`.
This is not a claim about an unrounded exact-real ellipsoid algorithm.

## 7. Meaningful exact output and physical-coordinate precision

The exact usual output consists of the rational anchor patch, all fixed
rational anchor coordinates (including integer labels, singleton hulls and
forced original bounds), the scalar equations and branch intervals
(1), and its unique reduced constrained minimizer. It can be written as
`argmin_C G` or by polynomial graph equations and box KKT conditions.
For the latter, graph multipliers satisfy
`lambda_j=-(partial_yj F_0+eta_j)/partial_y q_j`; substitution gives
the reduced anchor gradient. Include anchor-box multipliers and branch
intervals `V_j`. The displayed dependent intervals select the globally
valid chart; no claim about positive ambient Hessians is needed.

The rational lower-cost rows, root brackets, DP trace, derivative enclosures
and matrix test provide the soundness evidence. Global graph premises
remain separate as stated in Section 1. A trace's length is charged to
the work that generated it; this argument does not assert a uniformly
polynomial pruning trace on every draw. The final local patch description
can be compact independently of that trace.

A rational bound on the chart Lipschitz constant is, for example,

\[
 K_\Phi=1+\sum_j |S_j|P_{1,j},\qquad
 \|\Phi(t)-\Phi(t')\|_2\le K_\Phi\|t-t'\|_2,
 \quad \Phi(t)=(t,\psi(t)).
 \tag{22}
\]

It has polynomial encoding length. Strong convexity and constrained
first-order optimality on the accepted patch give
`G(v)-G*>=g_0 ||v-t*||_2^2/2`, including boundary minimizers.
For physical accuracy `2^(-q)`, apply Section 6 with

\[
 \eta\le\min\{2^{-q},(g_0/2)(2^{-q}/(2K_\Phi))^2\}.
 \tag{23}
\]

Then the exact feasible implicit point `Phi(v)` is within `2^(-q)/2`
of the exact optimizer. Refine its dependent scalar roots to total
Euclidean error at most `2^(-q)/2`, obtaining a rational approximation
within `2^(-q)` of the physical optimizer. The approximation itself is
not asserted graph-feasible. The rational value interval (21) has the
requested accuracy. All extra precision is polynomial in input lengths
and `q`, since `log K_Phi` and `log(1/g_0)` are counted in the encoding.

## 8. Apply the exact fallback to the original polynomial graph

The reduced `G` is generally not an explicitly encoded polynomial. The
[exact fallback](polynomial-exact-fallback.md) must instead use the
original bounded semialgebraic domain

\[
 t\in T,\qquad y_j\in V_j,\qquad q_j(t_{S_j},y_j)=0.
 \tag{24}
\]

In the fallback's lexicographic singleton formulas, replace box membership
by (24). Add the dependent variables to each of the two quantified blocks.
The objective remains the explicit polynomial
`F_0(t,y)+gamma't+eta'y`. Degrees stay fixed, the new variable and atom
counts are polynomial in the base input, and integer-label expansion has
logarithmic size polynomial in that input. Compactness follows from the
closed bounded domain; (2) ensures nonemptiness over every anchor.

The same primary fixed-block elimination bound and univariate root
refinement therefore give exact selection and evaluation on every draw in
`B poly(I+b+q)`, with a base-only `B=2^{poly(I)}`. This includes ties
and positive-dimensional optimizer sets. It does not substitute algebraic
charts into a theorem requiring an explicit polynomial objective.

For a feasible approximate point after fallback, recover integer anchor
labels exactly, approximate and clip continuous anchors to their original
box, then attach the unique scalar graph roots. A reduced-gradient bound
controls objective error, just as in Section 6 of the fallback note.
Refine the exact value for a global lower endpoint. This yields an exact
implicit feasible point and rational objective-gap bounds. Clipping all
physical coordinates independently would not preserve (24) and is not
part of this contract.

## 9. Review and check scope

The approximate-DP constants, scalar derivative bounds and corrected patch
tests were independently checked before this draft. The weak-separation
definition and cleanup were checked against the reviewed GLS interface.
The [completed-text review](../reviews/implicit-graph-oracle-review.md)
approved the full argument. Its zero-anchor, singleton-dependent,
restricted-midpoint and fixed-coordinate clarifications are included.
Scoped inline Python checks passed whitespace, paired math delimiters,
local links and all 24 sequential equation tags in this note and its
review. No general optimizer is implemented by this note, and no
project-wide verification, CI inspection or external search was performed.
