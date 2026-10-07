# Certified convex values and exact fallback on rational polytopes

Date: 2026-10-02. Status: fresh actual-file
[review passed](../reviews/convex-polytope-value-interface-review.md).
These are standard convex and real-algebraic tools
adapted to the coupled-polytope cell algorithm. No new solver or
publication-priority claim is made.

Let `Q={x:Ax<=b}` be a nonempty bounded rational polytope, with a
supplied rational bounding box, and let `phi` be an explicit rational
polynomial of fixed degree. All variables here are continuous. Denote
the input length by `S`. Rational linear programming checks emptiness
and supplies a Farkas certificate if the domain is empty.

## 1. Convex value interface

Suppose `phi` is convex on `Q`, with this premise verified or supported
by a supplied certificate whose verification is charged. For every
rational `eta>0`, there is an algorithm of bit cost polynomial in
`S` and the encoding length of `eta` returning a rational `y in Q`
and rational bounds

\[
             \ell\le\min_Q\phi\le u=\phi(y),\qquad
                              u-\ell\le\eta.                \tag{1}
\]

No full-dimensionality, strict complementarity, strong convexity or
numerical regularity bound is assumed. The lower bound has a compact
tangent/linear-program dual certificate described below.

### Relative coordinates and a rational inner ball

For each row of `Ax<=b`, maximize its slack over `Q` by exact rational
linear programming. Rows with maximum slack zero are universally
tight. For every other row retain a rational feasible positive-slack
witness. Their average `x_0` is feasible and has positive slack in
every non-universal row. If no such row exists, choose any feasible
rational point.

The universally tight equations define precisely the affine hull of
`Q`. To see this, every other row is strict at the average point, so
a sufficiently small neighborhood of that point in the equation
space satisfies all remaining inequalities. Solve the equations by
rational Gaussian elimination and write

\[
                       x=x_0+B w.                           \tag{2}
\]

The full-column-rank matrix `B` can be chosen so the free coordinates
of `x-x_0` are exactly the coordinates of `w`. If its column count is
zero, `Q` is a rational singleton and direct evaluation proves (1).
Otherwise the reduced domain is a full-dimensional bounded polytope

\[
                         R=\{w:A' w\le b'\}.                \tag{3}
\]

Remove zero coefficient rows. Every remaining row has strictly positive
right-hand side because `w=0` corresponds to the average point.
There is at least one such row when the dimension is positive, since
the domain is bounded. Thus

\[
            r_R=\min_i b'_i/\|A'_i\|_1>0                    \tag{4}
\]

is a rational Euclidean inner-ball radius about zero. A rational outer
radius `R_R` follows from the original bounding-box widths of the
selected free coordinates: their sum bounds `||w||_2` on `R`.

Exact rational LP solutions, their average, Gaussian elimination and
the ratios in (4) all have polynomial encoding length. In particular,
`log(1/r_R)` when positive is polynomial in `S`. Tiny relative slacks
are handled through their binary lengths; no numerical inverse slack
is charged to the number of cells. Substitution into the fixed-degree
polynomial gives `psi(w)=phi(x_0+B w)` of polynomial encoding length.

### Weak optimization and feasible-output repair

Compute rational coefficient bounds `W>=max(1,sup_R |psi|)` and
`G>=max(1,sup_R ||grad psi||_1)`, using a rational coordinate box
containing `R`. They have polynomial bit length. Consider

\[
 K=\{(w,t):w\in R,\ \psi(w)\le t\le W+2\}.                \tag{5}
\]

This body contains the Euclidean ball about `(0,W+1)` of radius
`r_K=min(r_R,1/2)` and lies in a ball about that point of radius
`R_K=R_R+2W+2`. A violated row of (3), the epigraph cap, or the tangent
inequality to `psi` supplies a rational strong separator. Check the
linear constraints before using a tangent, so convexity is needed only
on `R`. Normalize separators as in the reviewed
[GLS bit interface](convex-patch-evaluation.md).

That interface applies after translating the known center to the
origin. For tolerance `epsilon<=r_K/2`, it returns rational `(w,t)`
within Euclidean distance `epsilon` of `K`, with objective compared
against the eroded body. Homothety toward the inner-ball center gives

\[
 t\le\psi^*+A_0\varepsilon,\qquad
                   A_0=1+(2W+1)/r_K.                       \tag{6}
\]

Restore exact feasibility by solving the rational linear feasibility
problem

\[
             y\in R,\qquad
                 -\varepsilon\le y_i-w_i\le\varepsilon.     \tag{7}
\]

A nearby point `(bar w,bar t) in K` satisfies
`||w-bar w||_infinity<=epsilon` and `|t-bar t|<=epsilon`.
It witnesses feasibility of (7). The returned rational `y` satisfies
`||y-bar w||_infinity<=2epsilon`. Both points lie in `R`, so

\[
                \psi(y)\le t+(1+2G)\varepsilon.             \tag{8}
\]

Consequently `[t-A_0 epsilon,psi(y)]` encloses `psi*` with width at
most `(A_0+1+2G)epsilon`. Choose
`epsilon=min(r_K/2,eta/(A_0+1+2G))` and map `y` back by (2).
Every operation has polynomial bit cost in the query data. In
particular the repair uses an exact LP, not a Hoffman error bound
or clipping that could violate a coupled constraint.

The direct Turing source and the precise weak-optimization guarantee
are already checked in the linked GLS interface. The argument here
changes the relative domain and feasible-output repair, not the
source theorem or its precision model.

### A short independently checkable lower bound

For a feasible rational point `y` in the original coordinates, let
`g=grad phi(y)`. Solve the rational tangent LP

\[
                  m=\min_{x\in Q}g^T x.                    \tag{9}
\]

Then `ell=phi(y)-g^T y+m` is a global lower bound by convexity.
For the representation `Ax<=b`, an exact minimization dual is

\[
       \lambda\ge0,\qquad A^T\lambda=-g,
                    m=-b^T\lambda.                         \tag{10}
\]

A feasible rational point attaining the same linear value and a dual
vector prove the LP optimum. These certificates have polynomial bit
length, including for lower-dimensional domains.

To make the tangent gap at most `eta`, compute a rational `K_0>=1`
bounding `sup ||H_phi||_2` on the original bounding box times
`max(1,diam(Q))^2`. Such a bound has polynomial bit length. First
use the value solve above to obtain a feasible point of objective gap
at most `delta=min(eta/2,eta²/(8K_0))`. The segment from that point
to a tangent-LP minimizer stays in `Q`. Taylor's bound on the segment
gives, with `gap=phi(y)-ell`,

\[
                 gap\le\delta/t+K_0t/2\quad(0<t\le1).       \tag{11}
\]

Taking `t=min(1,eta/(2K_0))` proves `gap<=eta`. The additional
accuracy has only polynomial encoding length. A final verifier
checks feasibility, objective and gradient evaluation, (10), and
the actual rational gap. It need not reproduce the relative-coordinate
GLS computation.

## 2. General exact fallback on the same rational polytope

Convexity is not needed for this second interface. Let
`F_c(x)=F_0(x)-c^T v`, where the selected core coordinates `v` are
part of `x`. Let `I` be the binary length of the base polytope,
bounding box, `F_0` and selected core indices, excluding sampled
coefficients and requested precision. Let `b_c` bound the bit length
of the rational sampled coefficients. There is a base-computable
`B_0=2^{poly_d(I)}` and fixed exponent `c_d` such that exact global
optimization and a feasible rational approximation of gap `2^-q`
cost at most

\[
                         B_0(I+b_c+q+1)^{c_d}.              \tag{12}
\]

This follows from the reviewed
[scalar lexicographic fallback](polynomial-exact-fallback.md) with
one explicit domain change. Replace its mixed-box predicate by
`D(x): Ax<=b`. The compact nonempty polytope has a unique
lexicographically first global optimizer. The scalar formulas for
each coordinate and the value still have one existential block and
one universal block, fixed degree, and a base-only number of atoms.
The verified Renegar bound and univariate root extraction therefore
give exactly the same separation between a base-only exponential
factor and a polynomial in sampled height and requested precision.
Lower-dimensional domains and positive-dimensional optimal sets do
not change the argument.

The coordinate representations need not themselves be feasible when
rounded. Refine the selected exact optimizer `x*` to a rational
vector `w` of infinity error at most `epsilon`. Apply (7) in the
original polytope to obtain rational feasible `y`; the exact optimizer
witnesses that `Q` intersects this rational error box, so
`||y-x*||_infinity<=2epsilon`. Let `G_0>=max(1,sup ||grad F_c||_1)`
be a polynomial-bit coefficient bound on the supplied bounding box.
Then `F_c(y)-F_c(x*)<=2G_0 epsilon`. Choose
`epsilon=2^-q/(4G_0)` and separately refine the algebraic optimal-value
interval to width `2^-q/2`. Its lower endpoint and `F_c(y)` prove
the desired feasible approximation contract.

LP computations polynomial in the possibly exponentially sized
algebraic-query records remain within (12) after enlarging the same
base-only exponential factor and fixed exponent. No sampled height
or accuracy parameter enters the exponent. This is the all-draw
fallback used by the coupled-polytope theorem, not a claim that the
expanded algebraic representation is always short.

## Verification status

The relative geometry, LP repair, tangent dual and fallback formula
change passed the saved fresh actual-file review. The separate
[exact coupled-cell diagnostic](check_coupled_polytope_cells.py) and
[results](coupled-polytope-cell-results.json) check relative dimensions
zero, one and two, a 101-bit thin bound, 337 tangent LP duals and
81 feasible error-box repairs through 200-bit requested precision.
The fixtures use complete rational face enumeration; they are not
an implementation of the general GLS or algebraic fallback algorithms.
No index edits, project-wide checks or CI inspection were used.
