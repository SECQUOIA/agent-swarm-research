# Exact smoothed optimization through box-stable conditional recourse

Date: 2026-10-02. Status: independently reviewed; targeted exact checks
passed. This note gives an exact-completion
mechanism for a small continuous core with tractable conditional recourse.
It does not supply a general bounded-treewidth recourse algorithm.

The new step is an **excluded-region test**. Exact recourse on at most
`2n` additional coordinate restrictions certifies that every relevant
conditional optimizer lies in a small residual box. Original-bound
gradient tests and an exact Hessian test can then close the original
problem. The stopping depth depends only on base data, avoiding the
sampling-precision circle in rational reconstruction.

## 1. Model and conclusion

Let

\[
 F_\gamma(x)=\tfrac12x^TAx+b^Tx+c+\gamma^Tx,
 \qquad x\in[0,1]^n,\quad A=A^T\in\mathbb Q^{n\times n}.
 \tag{1}
\]

Supply a core `C` of `k` coordinates, with `R` its complement, and a
rational `L>0` such that `A_ii<=L` for `i in C`. All coordinates in this
main theorem are continuous. The following recourse assumption includes
its bit model: after fixing the core to any rational vector and restricting
each residual coordinate to any rational subinterval of `[0,1]`, an
algorithm computes an exact rational global minimizer and value in time
polynomial in the resulting input length. It also reports empty boxes.
The polynomial exponent is absolute, independent of `k`.

This assumption is called **box-stable recourse** here. It concerns global
optimization on every such restricted residual box, not merely a local
stationary point or one unrestricted conditional solve.

There is one base-computable integer `M`, a power of two with
`log M=poly(I)`, such that independent noise coordinates sampled uniformly
from

\[
 \{-\sigma+2\sigma j/(M-1):0\le j<M\},\qquad \sigma>0,
 \tag{2}
\]

give an algorithm that returns an exact rational global optimizer and
value on **every draw**. Its expected bit work is

\[
 8^k\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k
             \operatorname{poly}(I).
 \tag{3}
\]

The polynomial factor includes the polynomial recourse cost. No growth,
active-gradient, Hessian-conditioning, or uniqueness promise is supplied.
The exponential factor contains the core dimension, not the total number
of coordinates. The unit-box restriction makes the numerical width scale
explicit; arbitrary rational widths require the corresponding rescaled
curvature and noise parameters.

For `k=0`, solve recourse directly. If `R` is empty, omit all excluded-region
calls below. Empty or fixed coordinates can be removed before specifying
the core and recourse interface.

## 2. Exact conditional values and the core search

Condition on all residual noise and define

\[
 V(v)=\min_{z\in[0,1]^R}F_\gamma(v,z),\qquad v\in[0,1]^C.
 \tag{4}
\]

The function `V(v)-gamma_C^T v` is independent of all core noise. It has
upper coordinate curvature `L`, since an infimum over a fixed feasible
set preserves this property. This remains valid at nonsmooth points.
Each rational query supplies both its exact value and a feasible full
completion.

Use nested dyadic core cells of common side `h_j=2^-j`. At level zero
start with the full core box. At each next level generate only children
of retained cells, evaluate all distinct corners, and let `U_j` be the
smallest value queried at this level. Keep a cell if

\[
 \min_{v\text{ corner}}V(v)-e_j\le U_j,
 \qquad e_j=kLh_j^2/8.
 \tag{5}
\]

Coordinate interpolation proves that an optimizer cell survives. Its
corners give

\[
 U_j-f^*\le e_j.
 \tag{6}
\]

Every retained cell has a corner of value at most `f*+2e_j`. Let `D_j`
be the coordinate hull of the retained core cells. It contains the core
projection of every original optimizer. Choose a best queried corner
`c_j`, and its exact recourse completion `w_j=(c_j,z_j)`. This corner
belongs to a retained cell and hence to `D_j`.

The conditional-neighbor argument from
[local-error recourse](local-error-recourse-interface.md) now has no
outside rounding error. A near-optimal interior grid coordinate confines
its independent noise to an interval of length at most

\[
 Lh_j+4e_j/h_j=Lh_j(1+k/2).
 \tag{7}
\]

Boundary coordinates each contribute at most two choices. If `M>=2^J`,
then for every `j<=J` the expected number of `2e_j`-near-optimal full
core-grid tuples is at most

\[
 H=\left[3+\frac{(1+k/2)L}{2\sigma}\right]^k.
 \tag{8}
\]

Indeed, each interior tuple has coordinate probability at most the interval
length divided by `2sigma`, plus `1/M`; summing the `h_j^-1-1` interior
positions contributes at most one from atoms. The intervals depend on
the tuple and residual noise, not on other core noise, so their product
bound is valid. A near-optimal tuple touches at most `2^k` cells, a retained
cell generates at most `2^k` children, and a child has `2^k` corners.
Thus the expected number of queries through level `J` is at most
`2^k+8^k H J`. Storage and generation are charged to these actual lists;
there is no preliminary enumeration of the full fine grid.

## 3. A sound excluded-region certificate

Compute from base data

\[
 M_1=\max\{1,\max_i\sum_j|A_{ij}|\},\qquad
 G=\max\{1,\sum_{i\in C}(|b_i|+\sigma+\sum_j|A_{ij}|)\}.
 \tag{9}
\]

For every fixed residual feasible set, its conditional value is
`G`-Lipschitz in the core infinity norm. This follows by evaluating a
minimizer at the other core point and using the same uniform bound on
the core gradient; it needs no convexity of the residual problem.

Fix a positive rational radius `r`, a level, and abbreviate
`c=c_j`, `z=z_j`, `D=D_j`. Form

\[
 P=\prod_{i\in R}[\max(0,z_i-r),\min(1,z_i+r)].
 \tag{10}
\]

For each residual coordinate, solve conditional recourse at `c` on
`x_i<=z_i-r` if `0<z_i-r<1`, and on `x_i>=z_i+r` if
`0<z_i+r<1`, keeping all other residual bounds original. Omit a
restriction when its raw threshold is outside or at an original bound.
In particular, do **not** add a singleton at a clipped original endpoint:
it may contain an active global optimizer. Let `V_out(c)` be the minimum
of these at most `2|R|` values, or `+infinity` if there are no restrictions.

These closed restricted boxes cover the complement of `P` in the original
residual domain. Set `d=max_i width_i(D)`. If

\[
                    V_{\rm out}(c)-V(c)>2Gd,                 \tag{11}
\]

then **every conditional optimizer over every core point in `D` lies in
`P`**. To prove this, each restricted conditional value at any `v in D`
is at least its value at `c` minus `Gd`, whereas the unrestricted value
is at most `V(c)+Gd`. Inequality (11) strictly separates them.
Consequently every original global optimizer lies in `D times P`.

This certificate uses globally exact lower values from restricted recourse;
feasible witnesses alone would not justify it. All coordinate restrictions
keep the same supplied recourse class by assumption.

## 4. Exact convex closure and its base-only cutoff

On `D times P`, check affine gradient signs exactly. If the whole gradient
of a coordinate is strictly positive and its interval contains its
original lower bound, fix it at that bound; use the analogous rule for a
strictly negative gradient and an original upper bound. Each fixing is
sound because the product box contains every global optimizer. Let `J_f`
be the remaining coordinates, and check exactly

\[
                         A_{J_fJ_f}\succeq g_0 I              \tag{12}
\]

for a positive rational `g_0` chosen below. If (11) and (12) pass, an exact
convex-QP solve on the remaining box returns the original global optimizer.
If no coordinate remains, evaluate the single point. These are sound
deterministic checks on every draw; they do not assume that a probabilistic
event occurred. The convex-QP oracle has the standard exact rational
polynomial-bit guarantee.

For stopping analysis only, suppose the original sampled problem has
point growth at least `g_0` at its unique optimizer `a`, and each active
original-bound gradient has magnitude greater than `tau>0`. Put

\[
 r=\min\{1/8,\tau/(16M_1)\},\qquad
 A_0=2+kL/g_0.
 \tag{13}
\]

Growth and the retained-corner value bound show that every point of `D_j`
is within `A_0 h_j` of `a_C` in each coordinate. Equation (6) also gives
`||w_j-a||_2<=sqrt(e_j/g_0)<=A_0 h_j`. Therefore, if

\[
 h_j\le\min\left\{\frac r{4A_0},
                  \frac{g_0r^2}{16GA_0}\right\},             \tag{14}
\]

then `||w_j-a||<=r/4`, `e_j<=g_0r^2/16`, and `diam_inf D_j<=2A_0h_j`.
Any excluded residual point differs from `z_j` by at least `r` in one
coordinate, and thus differs from `a` by at least `3r/4`. This proves

\[
 V_{\rm out}(c_j)-V(c_j)
 \ge(9/16)g_0r^2-e_j\ge g_0r^2/2
 >2G\operatorname{diam}_\infty D_j.                          \tag{15}
\]

The containment certificate passes. Every point in `D_j times P` is
within `5r/4` of `a` in infinity norm, so each gradient differs from its
value at `a` by at most `5M_1r/4<tau/2`. The sign tests fix every original
active coordinate. They cannot fix an original free coordinate, whose
gradient is zero at `a` and whose interval contains `a`.

Two-sided free directions in the point-growth inequality imply
`A_{J_fJ_f}>=2g_0 I`. Since a quadratic Hessian is constant, (12) passes
on the entire remaining box. This proves exact closure by the first
level satisfying (14). No local eigenvalue approximation or algebraic
coordinate reconstruction is needed.

## 5. One finite law and exact fallback

Use the already reviewed quadratic special case of the
[finite-grid growth and active-gradient tails](sparse-bag-cell-smoothed-miqp.md).
For clarity, the following constants are deliberately conservative:

\[
 \begin{gathered}
 B=\max\{2,3^n\},\quad C_{\rm tail}=8(B+1)^2,\quad K=\max\{1,nB\},\\
 \rho=1/(4B),\qquad g_0=\rho\sigma/(2n),\qquad
 \tau=\rho\sigma/(2K).
 \end{gathered}                                                \tag{16}
\]

Choose the least `J>=0` satisfying (14), then the least power of two

\[
 M\ge\max\{2,2^J,4nC_{\rm tail}/\rho,2K/\rho\}.             \tag{17}
\]

These quantities depend only on the base input, and `J,log M=poly(I)`.
The tail bounds give failure probability at most `rho` for growth and
at most `rho` for active gradients on the positive-growth event. Thus
failure to close by level `J` has probability at most `1/(2B)`.

On any unresolved draw, use exact box-QP face enumeration on the **same**
draw. It has cost `B poly(I+log M)` and returns a rational optimum even
with a continuum of minimizers: choose an optimizer on a smallest face;
if its free PSD Hessian were singular, a nonzero flat stationary direction
could be followed to a smaller face. Thus either that free block is
nonsingular or no free variable remains, and face enumeration includes
an exact stationary solution with optimal value. Only feasibility and
objective comparison are needed to choose among the candidates.

Expected fallback cost is polynomial. At each searched level there are
at most `2n` extra restricted recourse calls, exact rational gradient and
PSD tests, and one optional convex-QP call. The input lengths of all
queries are polynomial: dyadic core coordinates use `O(J)` bits, recourse
returns polynomial-length rational coordinates, and patch endpoints add
only the base radius `r`. Combining these bounds with (8) proves (3).

The sampling precision is chosen once. In particular, there is no
requirement to refine to a rational separation bound that itself grows
with `log M`. Every-atom correctness follows from exact containment,
convex closure, or exact fallback, not from discarding a rare draw.

## 6. Forest deletion gives a concrete new scope

Suppose deleting the supplied core from the interaction graph of `A`
leaves a forest. Core fixing changes only residual linear and constant
terms. Restricting residual coordinate boxes, deleting fixed coordinates,
and affinely mapping their nondegenerate intervals to `[0,1]` preserves
the forest interaction graph. The exact rational forest algorithm of
Del Pia and Khajavirad therefore supplies every recourse call. Its
[local source record](../../literature/papers/pia2026-treewidth-and-the-complexity-of/paper.md)
states the Turing model explicitly; Theorem 1 and Lemmas 15--19 control
the sizes of piecewise-quadratic arc coefficients, breakpoint comparisons,
and returned rational coordinates.

Consequently (3) is an expected FPT bound in the size of a supplied
feedback vertex set and the core curvature/noise ratio. The residual
forest need not be convex, have bounded negative inertia, or be separable.
The forest oracle itself is an established result, not a contribution of
this note. The claimed contribution is its composition with a sound
excluded-region certificate and a single finite smoothed law.

This does not give expected FPT in treewidth alone: a graph of small
treewidth can require a large feedback vertex set. It also does not
extend the forest oracle to quartic residuals or arbitrarily many integer
coordinates. Any additional recourse class must independently satisfy the
stated exact, box-stable polynomial-bit interface.

## 7. Verification status

The [independent actual-file review](../reviews/smoothed-box-stable-recourse-review.md)
found no substantive gap in the containment certificate, quantitative
cutoff, fixed finite law, or expected bit bound. The coordinating
researcher separately read the complete proof and checked its constants.

The author-side targeted command
`python research-20261002/reviews/check_box_stable_recourse.py` passed four
noisy nonconvex-forest closure fixtures, 20 exact excluded-slab solves,
clipped-original-bound and tied-residual-mode guards, and three finite-law
budget cases with widely separated rational scales. The
[diagnostic](../reviews/check_box_stable_recourse.py) uses small face
enumeration as its oracle; it is not an implementation of the forest
algorithm. It checks the new localization/closure interface, not the
existing core-cell search.

The independent reviewer separately reported 600 random rational
two-variable QPs, 548 successful localization/convex closures, and
11,508 conditional-slice checks, including gradient-sign pitfalls. Those
are the reviewer's run, not a duplicate author run. No project-wide
checks, CI inspection, or index edits were performed.
