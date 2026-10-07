# Local interpolation budgets need conditional recourse

Date: 2026-10-02. Status: direct derivation, exact counterexample check,
and independent completed-text review finding no substantive gap.
This note investigates the dimension factor in the
[sparse polynomial cell theorem](smoothed-sparse-polynomial.md). It gives
an unsoundness example for a direct local-error substitution and a precise
sufficient interface for removing that factor. The interface is not an
implemented or proved efficient recourse algorithm.

## 1. A bag-local budget is unsound for current grid min-marginals

Let `m=32`, `epsilon=1/16`, and consider the star quadratic on
`[0,1]^{m+1}` with center `x` and leaves `y_1,...,y_m`:

\[
 F(x,y)=x^2-\frac{x}{2}\sum_{i=1}^m y_i+
          \sum_{i=1}^m y_i^2+
          \left(\frac m{16}-1-\varepsilon\right)x.
 \tag{1}
\]

Its interaction graph is a tree, with bags `{x,y_i}` of size two.
Every coordinate second derivative is exactly two, so `L=2`.
For fixed `x`, the unique continuous leaf minimizers are `y_i=x/4`.
The exact conditional value is

\[
 V(x)=\left(1-\frac m{16}\right)x^2+
       \left(\frac m{16}-1-\varepsilon\right)x.
 \tag{2}
\]

It is strictly concave, with `V(0)=0` and `V(1)=-epsilon`. Therefore
the original problem has the unique optimizer
`x=1, y_i=1/4`, with value `-1/16`.

At uniform mesh `h=1/2`, each grid coordinate is in `{0,1/2,1}`.
The conditional grid minima are

\[
 V_h(0)=0,\qquad V_h(1/2)=23/32,\qquad V_h(1)=31/16.
 \tag{3}
\]

Indeed, a leaf is minimized at zero when `x=0` or `x=1/2`, and at
either zero or one half when `x=1`. Thus the grid minimum and feasible
incumbent are both zero.

Consider the bag cell `x in [1/2,1], y_i in [0,1/2]`. It contains
the true optimizer's bag projection, but the minimum of its four exact
grid bag min-marginals is

\[
 q_C=23/32>\frac{|B|Lh^2}{8}=1/8.
 \tag{4}
\]

Replacing the current global correction by this bag-local correction
would remove a cell containing the unique global optimizer. The actual
global correction is `(m+1)Lh^2/8=33/16`, which is sufficient.
All level-zero cells are retained, so this is also an actual possible
first-refinement state of the current algorithm. Its whole-box gradient
tests do not fix coordinates, and its Hessian is indefinite.

The error is contributed by conditional outside minimization, rather
than by rounding the displayed bag alone. More explicitly,

\[
 V_h(x)-V(x)
   =m\operatorname{dist}\bigl(x/4,\{0,1/2,1\}\bigr)^2.
 \tag{5}
\]

It ranges from zero at `x=0` to `m/16` at `x=1`. Therefore the outside
discretization error is not a constant that automatically cancels when
messages or min-marginals are normalized. Its variation can be proportional
to the number of leaves even at treewidth one and fixed coordinate
curvature. This does not rule out exact recourse, conditional grids, or a
new certified relative-error construction.

## 2. An exact conditional-value interface removes the dimension factor

For a bag `B`, condition on all outside noise and define the true value
function over the original outside mixed domain:

\[
 V_B(v)=\min_{x_{-B}\in X_{-B}}
           \{F_0(v,x_{-B})+\gamma_{-B}^{\mathsf T}x_{-B}\},
 \qquad W_B(v)=V_B(v)+\gamma_B^{\mathsf T}v.
 \tag{6}
\]

The outside feasible set is independent of `v`. Infima preserve
coordinate semiconcavity, so `V_B` has upper coordinate curvature `L`
and is independent of the entire bag-noise vector. This is the same true
value function used in the existing expected-count proof.

If `W_B` were evaluated exactly at the bag grid corners, rounding only
the bag coordinates would give the valid cell lower bound

\[
 \min_{v\text{ a corner of }C}W_B(v)-e_B,
 \qquad e_B=|B|Lh^2/8.
 \tag{7}
\]

The bound concerns every original feasible point with bag projection in
`C`. It does not round the outside variables, so there is no outside
dimension in its error. For exact recourse, minimizing these bag-grid
values also gives a feasible upper bound at most `f^*+e_B`.

The following approximate interface suffices as well. At each requested
corner, suppose an oracle returns a certified lower bound `ell_B(v)`
and an original feasible completion with value `u_B(v)` such that

\[
 \ell_B(v)\le W_B(v)\le u_B(v),\qquad
              u_B(v)-\ell_B(v)\le\eta_B\le a e_B,
 \tag{8}
\]

where `a>=0` is a fixed error factor. The bounds include all outside
optimization error. They are not merely polynomial evaluation bounds
at one guessed outside completion.

First update `U` using the feasible completions from all current-level
oracle calls; then apply retention, or recheck it after that update.
Retain a cell when `min_corner ell_B-e_B<=U`. From a bag's current
grid containing a cell around an original optimizer, its feasible
completions give `U<=f^*+e_B+eta_B`. Each retained cell then has a corner
with

\[
                   W_B(v)\le f^*+2(e_B+\eta_B).
 \tag{9}
\]

For bags of different sizes, one can use the common upper budget
`e=pLh^2/8`, `eta<=ae` in both steps. This preserves every optimizer
and makes (9) hold with `e` in place of `e_B`. Incumbents returned by
recourse need only be feasible for the original domain; they need not
belong to every current whitelist.

## 3. The resulting conditional-noise count

Apply the existing coordinate-neighbor comparison to (9). For a bag
tuple, and comparison spacing `a_i=h` for continuous coordinates or
`a_i=max(1,h)` for integer coordinates, each regular coordinate confines
its noise to an interval of length at most

\[
 L a_i+\frac{4(e+\eta)}{a_i}
 \le L a_i\left(1+\frac{(1+a)p}{2}\right).
 \tag{10}
\]

The interval depends on the true `V_B`, the tuple, and outside noise,
not on other in-bag noise. Uniform error bounds (8) suffice even if
the oracle's choices depend on the sample. The expected tuple count
under the same finite-law condition `M>=2^J` is at most

\[
 \prod_{i\in B}
 \left[4+\frac{Lw_i}{2\sigma}
                  \left(1+\frac{(1+a)p}{2}\right)\right].
 \tag{11}
\]

Thus this interface replaces the global dimension inside the exponential
factor by the bag-size parameter. The numerical width/noise dependence
remains. If the oracle calls and their certificates had suitable polynomial
cost, the sparse nested-cell generation would inherit this improved
count, with a parameter-dependent factor and an ordinary polynomial in
the number of bags and levels.

Equation (11) is a sufficient conditional-recourse principle, not yet an
FPT algorithm. The outside subproblem can contain almost the entire
original instance. Existing grid messages do not satisfy (8) with a
bag-local budget; (1)--(5) demonstrate this directly. Dividing a uniform
error allowance among all outside variables can force a mesh smaller by
a square root of the dimension and reintroduce the same state-count
problem elsewhere.

The consequential algorithmic question is therefore how to compute
certified conditional message differences or recourse bounds with this
local accuracy, without globally refining all outside coordinates. A
proof must control their error variation over separator states, not
assume cancellation of a shared constant. Exact conditional solutions
on special recourse classes can meet the interface, but they do not
settle general sparse polynomial or indefinite quadratic boxes.

## 4. Verification and limits

The star calculation was independently checked by the coordinating
researcher and another agent. The latter also reviewed the complete
conditional-recourse interface, constants, and noise conditioning. Its
clarification of the incumbent-update order is included. An inline `python3` calculation using exact
`Fraction` arithmetic evaluated all nine bag rows and their outside-leaf
minima. It obtained the three values in (3), the optimizer-containing
cell value `23/32`, the invalid local budget `1/8`, and the valid global
budget `33/16`. The strict concavity of (2) proves the original optimum;
the diagnostic does not approximate it numerically.

No global hardness claim follows from this example. Its exact recourse
is an elementary quadratic, and the connected quartic state-count family
can also be easy by a different representation. These examples distinguish
limits of the current retention rule from limits of sparse optimization
itself. No external search, project-wide check, CI inspection, or index
edit was performed.

## 5. Positive definiteness alone does not repair grid-message error

There is a stronger deterministic version of the star warning. For an
integer `d>=8`, let `m=d^2`, and minimize on `[0,1]^(m+1)`

\[
 F_d(x,y)=(x-1/2)^2+
       \sum_{i=1}^{m}\left(y_i-1/8-(x-1/2)/d\right)^2.
 \tag{12}
\]

The unique optimizer is `(1/2,1/8,...,1/8)`. The Hessian has eigenvalues
`2` with multiplicity `m-1` and `3+-sqrt(5)`. Thus it is uniformly positive
definite, coordinate curvature `L=4` is valid, and point growth `g=3/8`
is valid. Its star graph is two-colorable. In particular, it satisfies
the dimension-independent spectral bound associated with a PSD Hessian
on a graph with bounded coloring number.

Nevertheless, on the uniform grid `h=1/4`, write `t=x-1/2`. The exact
conditional continuous value is `V(x)=t^2`, while the conditional grid
value is

\[
                  V_h(x)=d^2/64-d|t|/4+2t^2.
 \tag{13}
\]

Indeed, every ideal leaf coordinate lies between `1/16` and `3/16`,
so its nearest grid point is zero or `1/4`. Among the five core grid
points, the minimum occurs at `x=0` or `x=1`, with value
`U=d^2/64-d/8+1/2`. The optimizer-containing bag cell
`x in [1/2,3/4], y_i in [0,1/4]` has minimum corner min-marginal

\[
 q_C=d^2/64-d/16+1/8,
 \qquad q_C-U=d/16-3/8\ge1/8.
 \tag{14}
\]

The proposed bag-local correction is only
`|B|Lh^2/8=1/16`, so it again discards the optimizer-containing cell.
Subtracting a shared message constant does not fix this: the outside
error changes between `x=1/2` and `x=3/4` by

\[
 |(V_h-V)(3/4)-(V_h-V)(1/2)|=(d-1)h^2.
 \tag{15}
\]

Thus no deterministic bound on this error variation of the form
`C(p,L/g)h^2`, independent of the number of leaves, follows merely from
positive definiteness and bounded coloring. The coherent grid phases
produce variation of order `sqrt(m)h^2`.

This is not a smoothed lower bound: independent leaf noise can destroy
the phase alignment. It is also not a runtime obstruction to a solver
with a global convexity test, which solves (12) immediately. Its scope
is the proposed relative-error justification for fixed grid messages.
The [box-stable recourse theorem](smoothed-box-stable-recourse.md) gives
a positive alternative when globally exact conditional solves remain
tractable under coordinate-box restrictions.

The supplement's targeted inline `python` check used exact `Fraction`
arithmetic for `d in {8,9,16,64,1000}`. All 25 conditional grid values,
five local-budget failures, and five normalized-error variations matched
the displayed formulas. The eigenvalues follow by restricting the star
Hessian to its center and normalized all-leaves direction; the orthogonal
leaf subspace has eigenvalue two. No general optimization or project-wide
verification was run for this supplement.
