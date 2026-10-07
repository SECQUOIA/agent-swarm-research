# Exact conditional cuts remove outside grid error for a concrete nonconvex class

Date: 2026-10-02. Status: complete arguments and a rational reference
implementation, with targeted checks recorded below. The
[independent review](reviews/independent-review.md) passed after three
implementation repairs. This note supplies a usable conditional oracle for
the earlier local-error interface. It does not prove a treewidth-only FPT
algorithm for general sparse polynomials or indefinite quadratics.

The positive result is a small supplied continuous core with an arbitrarily
large, possibly dense nonconvex residual problem. Residual coordinates are
concave separately, and their pairwise couplings become nonpositive after
fixed coordinate reversals. Each requested conditional value is one exact
minimum cut with a flow certificate. Only the core is discretized. Neither
outside discretization error nor complete parametric Bellman messages are
constructed.

The underlying endpoint reduction and graph cuts are classical. The
contribution here is an explicit box-stable oracle and certificate, its
composition with the existing adaptive conditional search, the resulting
cost and mixed-domain statements, and a checked implementation. Publication
priority for that composition is not established.

## 1. Quadratic class and conditional oracle

Write a rational quadratic on a product box as

\[
 F(x)=c+\sum_i(a_i x_i^2+b_i x_i)
                  +\sum_{i<j}c_{ij}x_i x_j.                 \tag{1}
\]

Supply a core `C` of `k` coordinates and let `R` be its complement.
Assume

\[
 a_i\le0\quad(i\in R),\qquad
 c_{ij}s_i s_j\le0\quad(i,j\in R),\quad s_i\in\{-1,1\}.     \tag{2}
\]

There is no condition on core-core or core-residual edges. Missing edges
have coefficient zero. The residual graph can have arbitrary width and
degree. The signs are supplied; for a fixed quadratic they can also be
found or disproved by propagating the required relative sign across each
nonzero edge, in linear graph time. A contradiction on a cycle rejects this
class. Selecting a smallest useful core is not solved here.
The implemented `detect_flips` checks residual coordinate concavity and
performs that graph traversal for a supplied core. Positive residual
curvature or a contradictory signed cycle gives a precise class-rejection
reason. It does not classify the rejected optimization problem as hard.

Fix any rational core assignment `v`. Restrict every residual coordinate
to an arbitrary rational subinterval `[l_i,u_i]` of its original domain,
and add arbitrary rational linear coefficients if desired. Empty boxes
are detected. For native-integer residual coordinates replace the lower
bound by its ceiling and upper bound by its floor before proceeding.

**Endpoint lemma.** There is a conditional global optimizer at a residual
endpoint in every coordinate. Starting from any feasible point, fix all
but one residual coordinate. Its univariate objective is concave, so one
endpoint has value no greater. Repeat for all residual coordinates. This
gives an endpoint vector without increasing the objective. Compactness
gives an initial optimizer. The same endpoints belong to an integer domain
after inward bound rounding, so the minimum over the continuous box and
over any designated native-integer residual coordinates is the same.

Choose the endpoint origin and signed interval length

\[
 \alpha_i=\begin{cases}l_i&s_i=1,\\u_i&s_i=-1,\end{cases}
 \qquad d_i=s_i(u_i-l_i),\qquad x_i=\alpha_i+d_i y_i,
 \quad y_i\in\{0,1\}.                                    \tag{3}
\]

Substituting the core point and the endpoint expressions gives

\[
 F(v,x_R)=K+\sum_{i\in R}h_i y_i+
                       \sum_{i<j\in R}q_{ij}y_i y_j,
 \qquad q_{ij}=c_{ij}d_i d_j\le0.                          \tag{4}
\]

All coefficients are obtained by rational evaluation and expansion; the
diagonal identity `y_i^2=y_i` is used. Put

\[
 p_i=h_i+\tfrac12\sum_{j\ne i}q_{ij},\qquad
 r_{ij}=-q_{ij}/2\ge0.
\]

The elementary identity

\[
 q_{ij}y_i y_j=\tfrac{q_{ij}}2(y_i+y_j)
                         -\tfrac{q_{ij}}2|y_i-y_j|
\]

rewrites the energy as `K + sum_i p_i y_i + sum_ij r_ij |y_i-y_j|`.
Use one graph vertex per residual coordinate and label `y_i=1` on the
source side of a cut. Add arcs

- `i -> sink` with capacity `max(p_i,0)`;
- `source -> i` with capacity `max(-p_i,0)`;
- both `i -> j` and `j -> i`, each with capacity `r_ij`.

Then for every endpoint assignment,

\[
             F(v,x_R)=K+\sum_i\min(0,p_i)+\operatorname{cut}(y).
                                                               \tag{5}
\]

Only one of the two opposite pair arcs crosses a cut. The construction
also covers singleton residual intervals and an empty residual set.

**Oracle theorem.** Under (2), an exact rational conditional value and
attaining residual endpoint vector are computable in polynomial bit time,
uniformly over rational core points, rational residual box restrictions,
and rational added linear terms. The polynomial exponent is independent
of `k`. A feasible flow whose value equals the returned cut is a
polynomial-size certificate of the conditional value.

**Proof and cost.** The graph has `r+2` vertices and `O(r+m_R)` arcs,
where `r=|R|` and `m_R` counts nonzero residual edges. The implemented
Edmonds--Karp algorithm uses `O((r+2)(r+m_R)^2)` rational operations.
Scale all capacities by the product of their denominators if necessary:
that product has polynomial encoding length in the explicit query, and
all residual capacities and flows are then integers bounded in bit length
by the scaled total capacity. Scaling need not actually be performed.
Thus intermediate rational lengths and total bit work are polynomial.
The verifier reconstructs (5), checks endpoint feasibility, flow capacity
constraints and conservation, and equality of flow and cut values. These
are `O(r+m_R)` rational checks, plus reading and compiling the input.
The endpoint lemma and weak max-flow/min-cut duality prove the result.

The class is substantially different from convex or forest recourse. For
example, the residual Hessian `-I-(1/r)11^T` is negative definite, has `r`
negative eigenvalues, and has a clique interaction graph. It satisfies
(2). Dense concave residuals of this form can couple to a core arbitrarily.
Their tractability here comes from the cut structure, not from bounded
feedback vertex number, bounded negative inertia, or convexity.

## 2. Adaptive core cells and an independently checkable bound

For this section, core coordinates are continuous on `[0,1]^k`; residual
boxes may be rational or native integer. Coordinate rescaling gives a
version on other core boxes but changes curvature and noise scales.
Supply `L>=0` with `2a_i<=L` on core coordinates and let

\[
 V(v)=\min_{z\in X_R} F(v,z),\qquad
 h_j=2^{-j},\qquad e_j=kLh_j^2/8.                          \tag{6}
\]

For fixed residual `z`, subtracting `(L/2)v_i^2` gives a concave function
of any one core coordinate. An infimum of concave functions is concave
(its hypograph is an intersection of convex hypographs). Thus `V` has
upper coordinate curvature `L` even where it is nonsmooth. Equivalently,
one may fix a minimizer at the interior query and use it at both endpoints.
Mean-preserving endpoint rounding one core coordinate at a time proves

\[
 \min_{v\text{ a corner of }D}V(v)-e_j
               \le \min_{v\in D}V(v)                     \tag{7}
\]

for every side-`h_j` core cell `D`. No residual coordinate is rounded.

Start with the single unit core box. At each level query the exact
conditional values of all distinct candidate corners and update a global
feasible incumbent `U`. Keep exactly the cells satisfying

\[
             \min_{v\text{ corner of }D}V(v)-e_j\le U.     \tag{8}
\]

At the next level generate only dyadic children of kept cells. Cache
previous queries; no preliminary fine-grid enumeration is needed. Every
optimizer-containing cell survives by (7). Such a cell also gives a
corner of value at most `f*+e_j`, so

\[
       U-f^*\le e_j,
 \qquad V(v)\le f^*+2e_j
 \quad\text{for some corner of every kept cell}.           \tag{9}
\]

The minimum candidate cell bound at a level is a global lower bound,
since the candidate union contains an optimizer. Taking the maximum of
these lower bounds over completed levels remains valid. Call it `LB`.
The incumbent `U` is no greater than any current queried value, so
`LB>=U-e_j`. Stop when `U-LB<=epsilon`.
It suffices to reach a base-computable level

\[
 J=\max\{0,\lceil\tfrac12\log_2(kL/(8\epsilon))\rceil\}.  \tag{10}
\]

For `kL=0`, level zero is exact. Without noise or growth this is a
globally correct additive algorithm; the worst-case number of cells can
still be exponential in `k` and in accuracy bits.

The reference implementation returns all queried cut certificates and a
level trace containing retained cells and bound values.
`verify_search` reconstructs every candidate list from retained parents,
checks every corner certificate without optimizing, and recomputes all
retention and bound decisions. The final incumbent is one of the
certified feasible completions. Verification takes polynomial work per
listed cell and cut certificate, with the same core-dimension factors
needed to enumerate each cell's corners. A caller-imposed level limit can
return an unfinished run with a valid enclosure; it never labels that
run complete unless its requested gap has been achieved.

## 3. Expected cost has no residual dimension in the exponential factor

Condition on arbitrary fixed residual linear coefficients. Independently
perturb each core linear coefficient uniformly on the finite grid of `M`
equally spaced points in `[-sigma,sigma]`. Write

\[
 W(v)=V_0(v)+\gamma_C^Tv,
\]

where `V_0` is independent of all core noise. Choose `M>=2^J` before
sampling, with `M>=2` and `J` from (10). The algorithm is correct on every
draw, and its expected number of conditional queries through level `J`
is at most

\[
 2^k+8^k J H,\qquad
 H=\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k.              \tag{11}
\]

**Proof.** For any fixed full level-`j` grid tuple `v` with
`W(v)<=f*+2e_j`, compare with `v+h_j e_i` and `v-h_j e_i` whenever
coordinate `i` is interior. These two inequalities confine `gamma_i` to
an interval of length at most

\[
 Lh_j+4e_j/h_j=Lh_j(1+k/2).                               \tag{12}
\]

The interval endpoints depend on `v`, `V_0`, and residual coefficients,
not on any other core noise. A uniform finite-grid interval has
probability at most its length divided by `2sigma`, plus `1/M`.
Independence permits a product bound for the interior coordinates.
Sum over the full grid: each coordinate has two boundary choices and
`2^j-1` interior choices, giving a factor at most

\[
 2+(2^j-1)\left[\frac{Lh_j(1+k/2)}{2\sigma}+\frac1M\right]
 \le 3+\frac{L(1+k/2)}{2\sigma}.
\]

Thus the expected number of such near-optimal tuples is at most `H`.
By (9), each kept cell touches one; a tuple touches at most `2^k`
cells. Each kept cell has `2^k` children, each with `2^k` corners.
Charge all generation, storage, and querying to these actual lists.
Level zero costs at most `2^k` queries, proving (11).

Each query has polynomial encoding length in the input and `J+log M`.
Multiplying (11) by the oracle and verification cost from Section 1 gives
an expected bit bound of

\[
 8^k\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k
       \operatorname{poly}(I+\log(1/\epsilon)+\log M).       \tag{13}
\]

The polynomial exponent is absolute. Residual dimension and graph size
enter that polynomial, not `H`. The numerical curvature/noise ratio
remains a parameter. This proves a particular implemented instance of
the earlier [conditional-value interface](../../research-20261002/new-direction/local-error-recourse-interface.md).
It does not replace its bag parameter by `k` on arbitrary sparse models;
a suitable supplied core and residual signs are essential assumptions.

## 4. Exact finite-noise and polynomial extensions

### Deterministic exact output implemented by rational separation

For rational quadratic data the reference code also has a complete
deterministic exact-output algorithm, subject to its explicit execution
level limit. Let `S` be the product of the denominators of all objective
coefficients and original box endpoints, and let `T=S^3`. After any
residual endpoint assignment, `T F` is an integer-coefficient quadratic
in the unit-box core variables. A quadratic monomial contains at most
two residual endpoints, which explains the power three.

Let `H_A>=1` be the largest absolute entry of the scaled core Hessian
`T Hess_CC(F)`, or one if all its entries vanish. Put

\[
               D=T\bigl(k!H_A^k\bigr)^2.                  \tag{13a}
\]

Every residual-label core optimum, and hence the original global optimum,
has reduced rational denominator at most `D`. To prove this, choose an
optimizer of its core box QP on a smallest face. Its free Hessian is PSD
by local optimality. If singular, a null stationary direction can be
followed to a smaller face with unchanged objective, a contradiction.
Thus either no coordinate is free or the free Hessian is nonsingular.
Its scaled integer determinant has absolute value at most `t!H_A^t`
for `t<=k`, by the determinant expansion. Cramer's rule shows that all
free core coordinates have denominators dividing this determinant.
Evaluating the scaled quadratic then gives a denominator at most its
square. Division by `T` proves (13a). The bound holds uniformly over
all endpoint labels without enumerating them; `log D` is polynomial in
input length.

Run the additive core search with tolerance `1/(2D^2)`. Its incumbent
fixes one residual endpoint label. Minimize the core quadratic for that
label exactly by enumerating its `3^k` faces, solving every nonsingular
free stationary system, and comparing feasible candidate values. The
smallest-face argument proves that this list includes an optimizer,
including when the full core Hessian is singular or indefinite. Let
its point and value be `x_hat` and `v_hat`. Then

\[
 f^*\le v_{\rm hat}\le U,
 \qquad U-LB\le 1/(2D^2),
 \qquad \operatorname{den}(v_{\rm hat}),
           \operatorname{den}(f^*)\le D.
\]

Distinct rationals with denominators at most `D` differ by at least
`1/D^2`, so `v_hat=f*`. This proves exact output on every rational input
in the class once enough levels are allowed. Equation (10) gives a
polynomial number of levels in input length, but the deterministic state
count can still be exponentially large. Face enumeration adds
`3^k poly(I)` work.

`verify_exact` needs neither face enumeration nor a new optimization
oracle. It checks the additive trace, recomputes `D`, checks exact
feasibility and objective evaluation of `x_hat`, verifies that its value
has denominator at most `D`, and checks that it lies in the certified
interval of length less than `1/D^2`. The same rational-separation
argument proves equality. `exact_core` returns an unfinished certified
enclosure when its explicit level budget is inadequate; the verifier
does not certify that response as an exact optimum.

This deterministic output mode does **not** inherit (14) by substituting
its stopping depth into (11). If coefficients contain sampled noise,
`D` and this depth depend on sampling precision, and requiring
`M>=2^J(D(M))` can be circular. The following smoothed exact result uses
the distinct, already proved base-selected closure and fallback theorem.

### Exact smoothed corollaries and broader residual objectives

**Continuous quadratic corollary.** On the unit box, with independent
finite linear noise in every coordinate, the existing
[box-stable recourse theorem](../../research-20261002/new-direction/smoothed-box-stable-recourse.md)
applies verbatim to Section 1's oracle. Consequently one base-computed
finite law gives an exact rational optimum on every draw, with expected
bit work

\[
 8^k\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k\operatorname{poly}(I).
                                                               \tag{14}
\]

That theorem's excluded-coordinate boxes, linear coefficient changes,
and rational restrictions preserve (2), so every required extra oracle
call remains a certified cut. Its exact convex closure and same-draw
fallback supply termination, rather than an assumption that sampled
cells eventually identify a rational optimum. When `L=0`, direct endpoint
evaluation of the core is already exact; otherwise use a positive valid
`L` in the imported theorem. The prototype implements the additive search
and deterministic rational-separation exact mode above, not that full
smoothed closure/fallback algorithm.

**Integer residual distinction.** Sections 1--3 directly permit arbitrary
native-integer residual intervals, with no enumeration of their labels.
At any original rational core point, the corresponding inward-rounded
continuous residual box has the same optimum. Hence an exact quadratic
optimizer of that relaxation can be converted to an original integer
residual optimizer by sequential concave endpoint choices. Each choice
does not increase the objective and so preserves an already global
optimum. This is a rational operation on quadratic exact output.
For nonunit integer intervals, a smoothed exact bound must use the
width-rescaled noise and curvature parameters of the imported theorem;
(14) is not claimed unchanged for arbitrarily wide binary-encoded boxes.
On binary residual unit intervals, (14) transfers directly. No continuous
integer core search is asserted.

**Polynomial oracle extension.** The exact-cut oracle also applies to

\[
 F(v,z)=P(v)+\sum_i\phi_i(v,z_i)
                   +\sum_{i<j}c_{ij}(v)z_i z_j,            \tag{15}
\]

where all functions are explicitly represented rational polynomials of
fixed degree, and the input supplies checkable uniform certificates

\[
 \partial^2_{z_i z_i}\phi_i(v,z_i)\le0,
 \qquad s_i s_j c_{ij}(v)\le0                               \tag{16}
\]

on the relevant original boxes. For fixed rational `v`, all unaries at
both endpoints are rational and the residual endpoint energy is still
(4). Bounds, added linear noise, and any subbox preserve (16). Thus the
exact polynomial-bit and flow-certificate oracle is unchanged; it is not
necessary to enumerate stationary algebraic roots of the concave unaries.
Supply a verified core coordinate-curvature bound `L` as before.
Sections 2--3 then hold with polynomial evaluation cost, whose exponent
may depend on fixed degree. A general sign or concavity recognition
algorithm for polynomial input is not assumed: include certificate size
and verification work in `I`.

For all-continuous unit-box variables, this exact oracle also meets the
approximate interface (with zero error) in the existing
[polynomial recourse theorem](../../research-20261002/new-direction/smoothed-polynomial-box-recourse.md).
Its exact implicit-output finite-noise theorem therefore has the concrete
nonconvex residual class (15)--(16), in addition to its previously stated
convex residual example. The conservative bound from that theorem is
`8^k[3+(1+k)L/(2sigma)]^k poly_d(I)`. Its assumptions on representation,
same-draw fallback, certificates, and exact output remain in force.
The current code implements quadratic coefficients only.

**Mixed concave and convex residual blocks.** The
[supplement](mixed-submodular-recourse.md) proves a broader quadratic
oracle: after sign reversals all residual off-diagonal coefficients are
nonpositive; a designated block has nonpositive diagonals, and the
remaining principal Hessian is PSD. Round only the first block to
endpoints. The exact convex-QP value after each binary label is a
submodular set function, since minimization over the remaining product
lattice preserves the submodular inequality. Exact rational submodular
minimization gives polynomial-time recourse on every subbox. The supplement
constructs a polynomial certificate from a convex combination of greedy
base vectors, with rational convex-QP KKT witnesses for its values. This
allows arbitrarily many coupled convex and concave residual coordinates.
The general submodular minimization algorithm is a proved construction,
not an implemented part of the cut prototype.

## 5. What the construction resolves and what remains open

The earlier star examples show that normalizing fixed-grid messages does
not give a dimension-free local error allowance: even a positive-definite
star can have varying outside rounding error of order `sqrt(n) h^2`.
The [global-error cell barrier](../../research-20261002/new-direction/global-error-cell-barrier.md)
shows an actual `n^{p/2}` retained-state obstruction for the old rule.
The [scalar-message example](../../research-20261002/new-direction/scalar-message-growth-obstruction.md)
rules out assuming few complete Bellman pieces at fixed width and growth.
None of those arguments is contradicted here. Each requested outside
value is instead globally solved and certified exactly by a polynomial
algorithm on the stated class.

The construction gives a solver component that can recognize a tractable
residual after a proposed core assignment and remove its entire grid
dimension. The residual may be large, dense, and highly nonconvex. It is
not merely a separable collection of leaves. However, a general sparse
polynomial graph need not admit any small core satisfying (2) or (16).
The general width-only state-count question remains unresolved. General
continuous submodularity, without separate concavity or an additional
tractability argument, is not assumed to be an exact rational cut oracle.

## 6. Implementation and targeted evidence

Files:

- [mincut_recourse.py](mincut_recourse.py): automatic residual recognition,
  exact rational endpoint compiler, Edmonds--Karp oracle, independent flow
  checker, adaptive core search, complete trace checker, and rational
  separation exact-output mode with its verifier.
- [check_recourse.py](check_recourse.py): exact exhaustive comparisons,
  invalid-premise guards, certificate tampering checks, and bounded examples.
- [check-results.json](check-results.json): recorded counts, enclosures,
  search time, and independent trace-verification time.

The targeted command actually run was

```text
python research-20261002-decomposition/conditional-messages/check_recourse.py --examples --output research-20261002-decomposition/conditional-messages/check-results.json
```

It passed 100 exact conditional comparisons against endpoint enumeration,
including 84 sign-reversed cases, 100 restricted boxes, and native-integer
residuals; 100 automatic sign-recognition comparisons; contradictory-cycle
and three invalid-premise guards; 20 exact global comparisons;
105 levels preserving every exhaustively known optimizer projection;
508 flow-certificate checks; 20 complete trace checks and 20 altered-bound
rejections. Zero curvature, ties, no core, no residual, and an unfinished
level-limited search are covered. Enumeration is confined to the small
independent test oracle; it is not used by the reference search.
Four exact-output fixtures also pass, including a non-dyadic core optimum,
a residual-label change, zero core coordinate curvature, and a singular
core Hessian. Their exact mode terminates in 1--7 levels. The diagnostic
also rejects altered exact values and insufficient-level exact claims.
The separate exact-output reconstruction deliberately enumerates core
faces; it never enumerates residual labels.

Independent review identified and corrected three input-boundary problems:
one-pass integer-index iterables were consumed before use; floating point
flows could bypass exact conservation arithmetic; and floating point
endpoint signs could contaminate the exact energy transformation.
The final code normalizes the iterable once and rejects inexact
certificate arithmetic. Exact adversarial regressions cover all three.

Six bounded illustrative random searches had one or two core coordinates
and 8--64 residual coordinates, with 12--528 edges. Each reached a certified
gap at most `1/1024` in five or six levels, using 6--53 conditional queries.
The dense 32-residual case had 528 edges and used nine queries. Exact
search times in the recorded run were approximately 0.003--0.63 seconds;
trace verification was separately timed. These fixtures are small and
chosen to satisfy the class. They establish operation and certificate
agreement, not competitive commercial-solver performance, smoothed
empirical scaling, or practicality of the exact finite-law fallback.

Two additional dense examples have a residual mode switch and two distinct
interior optimal core values. They use

\[
 F(x,z)=(x-3/4)^2+(x-1/2)\frac1r\sum_i z_i
                +\sum_{i<j}(z_i+z_j-2z_i z_j).             \tag{17}
\]

The residual diagonals vanish and all residual edges are negative. For
binary residuals any mixed assignment incurs at least one unit of cut
cost, while its core-dependent unary part varies by at most one half.
Thus an exact recourse optimizer is uniformly zero or uniformly one, and
`V(x)=(x-3/4)^2+min(0,x-1/2)`. Its two minima are zero at `x=1/4,3/4`.
For `r=8` and `r=32`, the actual search used five queries and three levels,
retained both optimal modes, and certified the exact gap zero. This
family gives a transparent example of a query count unchanged when
residual size grows, while cut solve and certificate costs still grow.
No project-wide verification or CI inspection was performed.

## 7. Source comparison

The pairwise binary submodularity condition and exact cut representation
are established by Kolmogorov and Zabih, Theorem 4.1 and Lemma 3.2;
the explicit construction is discussed in Section 4. Their result supplies
the classical cut ingredient in (4)--(5), rather than a new continuous
optimization theorem. The local source package and primary PDF were
checked. [Primary paper](https://www.cs.cornell.edu/~rdz/Papers/KZ-PAMI04.pdf)

Del Pia and Khajavirad explicitly use endpoint reduction for nonpositive
diagonal box-QP variables, and prove exact forest algorithms and other
structural results. Theorem 4 of their paper treats binary residual
structure through treewidth and attachment size. Our residual oracle
instead uses binary submodularity, allowing arbitrary residual graph
width. These are different sufficient sources of tractability.
[Primary paper](https://arxiv.org/html/2609.35595v1)

Burer, Natarajan, and Willemsen's current revision explicitly distinguishes
the classical coordinatewise-concave submodular endpoint case from general
continuous submodular QP. Its SDP is guaranteed tight only through
dimension three, with a four-variable counterexample and an open general
complexity question. Consequently the diagonal-concavity premise in the
cut oracle, or the convex-block premise in the supplement, must not be
dropped based on a general continuous-submodularity claim.
[Revision v3, introduction and Example 4](https://arxiv.org/html/2504.03996v3)

The local interpolation, conditional-noise count, and exact finite-law
closure are established project results cited above. The present note
instantiates their previously abstract oracle on an explicit nonconvex
class and supplies a small exact implementation. No claim is made that
endpoint reductions, graph cuts, tree decompositions, or submodular
optimization are novel.
