# One finite core-noise law gives a value oracle with convex recourse

Date: 2026-10-02. Status: complete proof with a
[fresh independent actual-file review](../reviews/core-only-noise-value-review.md).
The result concerns exact optimal-value Cauchy
output and certified objective approximation. It does not return an
optimizer-coordinate oracle. No publication-priority claim is made.

For one or two continuous core variables, arbitrary convex polynomial
recourse admits certified approximation at every requested precision
under a single finite core-noise law, with expected polynomial bit work
in the input length, requested accuracy bits, and `1+L/sigma`.
Residual strong convexity, a unique residual optimizer, and a growth
constant supplied to the algorithm are unnecessary. The key is to cap
the number of generated cells at each level and pay for exact fallback
with a truncated growth moment. The same noise sample works at all
precisions, including levels finer than its sampling grid.

## 1. Input and output

Fix the polynomial degree `d`. Let `F_0(v,z)` be an explicitly
represented rational polynomial on `[0,1]^k x [0,1]^m`, with
`k in {1,2}`. Supply verified bounds

\[
 F_{v_iv_i}\le L\quad(1\le i\le k),\qquad
 \nabla^2_{zz}F_0\succeq0
                 \quad\hbox{throughout the product box},    \tag{1}
\]

where `L>=0` is rational. Charge the polynomial, the rational noise
half-width `sigma>0`, and the encoded certificates to the base input
length `I`. For bound (4), certificate verification must be polynomial
in `I`; otherwise add the actual verification cost separately. Elementary
coefficient bounds supply a coordinate-curvature certificate, and a
supplied residual-convexity certificate must have the stated verifier.
Recognizing arbitrary polynomial convexity is not an uncharged step.
The residual may be empty. The case `k=0` is direct convex value
evaluation; fixed coordinates can be substituted in advance.

Only the core linear coefficients are randomized:

\[
 F_\gamma(v,z)=F_0(v,z)+\gamma^Tv,
 \qquad \gamma_i\text{ independent and uniform on an}
 \ M\text{-point grid in }[-\sigma,\sigma].                \tag{2}
\]

The endpoint-inclusive grid size `M`, a power of two, is chosen from
base data before sampling and has `log M=poly_d(I)`. It is not changed
when the requested accuracy changes.

**Theorem.** For this one sampled rational objective there is an exact
optimal-value Cauchy oracle. Given an integer `q>=0`, it returns a
feasible rational point `(v_q,z_q)` and rational bounds `a_q,U_q` with

\[
 a_q\le f_\gamma^*\le U_q=F_\gamma(v_q,z_q),
                       \qquad U_q-a_q\le2^{-q}.             \tag{3}
\]

Every draw and every query are correct. Expected bit work and expected
proof-record/output size for a query are at most

\[
                  (1+L/\sigma)\operatorname{poly}_d(I+q).
                                                               \tag{4}
\]

There is, more strongly, a single random work factor with expectation
at most `(1+L/sigma) poly_d(I)` that bounds the work divided by a fixed polynomial in
`I+q` simultaneously for all `q`. No resampling is used. Finite-accuracy
certificates on the ordinary branch are globally valid without trusting
a growth claim or a probabilistic event. A capped query invokes an
exact algebraic fallback on the same objective; its potentially large
cost and output have polynomial expected contribution.

The Cauchy descriptor consists of the sampled rational objective, the
base parameters, and the evaluator specified below. Efficient evaluation
is the content of the theorem. It is not a claim of polynomial-size
expanded algebraic output, convergence of `(v_q,z_q)` to a selected
optimizer, or a distance bound to the optimal set.

## 2. Two established bit interfaces

Write

\[
 V_\gamma(v)=\min_{z\in[0,1]^m}F_\gamma(v,z).
\]

This function is continuous. At a rational core point `v`, the
[certified convex recourse interface](smoothed-polynomial-box-recourse.md)
returns a rational feasible residual point and an interval

\[
 \ell_v\le V_\gamma(v)\le u_v=F_\gamma(v,z_v),
                            \qquad u_v-\ell_v\le\eta       \tag{5}
\]

in polynomial bit work in `I`, the core/noise coefficient lengths, and
`log(1/eta)`. No residual modulus is used. A tangent lower certificate
can be checked directly: convexity makes the minimum over the residual
box of the affine tangent at a rational feasible point a global lower
bound. The existing interface proves that a sufficiently accurate convex
value solve makes this tangent gap at most `eta`. Rational ellipsoid
weak optimization, with its feasible-output repair, supplies the solve.
The [convex epigraph evaluator](convex-patch-evaluation.md) obtains its
value interval and feasible point using only convexity. Its separate
strong-convexity assumption is used later to convert a value gap to
point distance; that conversion is not used here.
If `m=0`, evaluate the polynomial directly.

The [exact polynomial fallback](polynomial-exact-fallback.md) supplies
a base-computable integer `B_0=2^{poly_d(I)}>=2` and a fixed exponent
`c_d`. For sampled coefficients of at most `b` bits it returns an exact
global value representation, and also the feasible approximation and
global bounds in (3), in

\[
                      B_0(I+b+q+1)^{c_d}                  \tag{6}
\]

bit operations. Its exponential factor is independent of `b` and `q`.
This coefficient-height separation is needed before choosing `M`.
The fallback allows ties, flat fibers, and positive-dimensional optimal
sets. Its expanded output may be exponential; it is used only on the
capped branch.

## 3. Projected growth has a uniform finite-law tail

Let `g(gamma)` be the largest nonnegative point-growth constant of
`V_gamma` at a core optimizer, and set it to zero when optimal cores
are not unique. Distinct optimal residual points at the same core do
not force this constant to zero. For `t>0` its exact good-event formula
is

\[
 \exists(a,z_0)\ \forall(v,z):\quad
 F_\gamma(v,z)-F_\gamma(a,z_0)\ge t\|v-a\|^2,              \tag{7}
\]

where all variables lie in their product boxes. The inequality itself
enforces global optimality. There are two quantified blocks of `k+m`
variables; the growth norm uses only the core. Thus the same
[finite-section proof](polynomial-finite-noise-tails.md) supplies a
base-computable `C_0=2^{poly_d(I)}>=1`, uniform over every threshold,
such that

\[
 \Pr\{g<t\}\le kt/\sigma+C_0/M\qquad(t>0).                \tag{8}
\]

Indeed, apply the continuous proximal growth tail to the continuous
function `V_0` on `[0,1]^k`. Its total coordinate width is `k`.
For transfer to the finite law, quantifier elimination of (7), with one
noise coefficient free, bounds the number of scalar-section intervals
and points by `2^{poly_d(I)}` independently of all coefficient heights.
Replacing the `k` marginals one at a time yields (8), absorbing their
factors into `C_0`. Decreasing thresholds also covers `g=0` atoms.
Neither residual uniqueness nor residual noise enters this argument.

## 4. Certified core-cell refinement

Assume first `L>0`. At level `j`, let the core grid have side
`h_j=2^{-j}` and put

\[
                         e_j=kLh_j^2/8.                    \tag{9}
\]

Start with the whole core box at level zero. At each level use only the
dyadic children of cells retained at the preceding level. For every
generated cell, query (5) at its at most `2^k` corners with `eta=e_j`.
Repeated corner queries are permitted; their multiplicity is bounded
by a constant. Let `U` be the best feasible upper value found so far,
including earlier levels. Compute the cell bound

\[
                   \mathrm{LB}(C)=\min_{v\in\operatorname{corners}C}
                                                \ell_v-e_j.\tag{10}
\]

After all this level's corner queries, make a second linear pass and
retain exactly the cells with `LB(C)<=U`, using the **final** level
incumbent. Ties are retained. A first pass against an obsolete larger
incumbent would not justify the count below.

For every point of a cell, independently rounding core coordinates to
its corners preserves their means. Applying the coordinate upper
curvature bound successively gives expected cost increase at most
`L/2` times the total rounding variance, at most `e_j`. Fixing a residual
optimizer at the original core point shows that the same upper rounding
bound applies to `V_gamma`. Hence (10) is a valid lower bound throughout
the cell. All globally optimal cores survive every level.

An optimal core's cell has a true corner value at most `f*+e_j`, so

\[
                   U-f^*\le2e_j.                         \tag{11}
\]

For any queried corner, `ell_v>=u_v-e_j>=U-e_j`; consequently all
current cell bounds are at least `U-2e_j`. A previously pruned cell
had a certified bound above its then-current incumbent, which is at
least the current `U`. These facts give the sound global interval

\[
                           [U-2e_j,U].                   \tag{12}
\]

The retained cell that minimizes a corner lower bound has a true corner
value at most `U+2e_j<=f*+4e_j`. More precisely this holds separately
for **every** retained cell by choosing that cell's minimizing corner.
No growth constant is used to certify (10)--(12).

For query `q`, take the least `J>=0` with `2e_J<=2^{-q}`.
Then `J=O(I+q)`. In the absence of a cap, return (12) at that level and
the stored feasible incumbent. This terminates at the stated objective
accuracy even if the optimal core is not unique or has zero growth.

## 5. A per-level cap and one pre-draw noise budget

Suppose `g>0`, with unique optimal core `a`. The `4e_j` witness of a
retained cell is a grid corner within distance

\[
                       h_j\sqrt{kL/(2g)}                  \tag{13}
\]

of `a`. Each coordinate of such a corner has at most
`3+sqrt(2kL/g)` possible lattice values, and a corner belongs to at most
`2^k` cells. The number of retained cells is therefore at most
`2^k(3+sqrt(2kL/g))^k`. The number generated at the next level is at
most

\[
 4^k(3+\sqrt{2kL/g})^k
       \le512 Z^{k/2},\qquad Z=\max\{1,L/g\}.              \tag{14}
\]

The constant is valid for both `k=1` and `k=2`. It also bounds the
single initial cell. Set `Z=+infinity` when `g=0`.

Choose before sampling an integer `B>=B_0`, with `B>=2` and
`log B=poly_d(I)`. Use the generated-cell cap

\[
       T=512B,\qquad
       M=\text{the least power of two at least }\max\{2,C_0B\}.
                                                               \tag{15}
\]

Thus `log M=poly_d(I)` and
`beta:=C_0/M` satisfies `beta B<=1`. No query precision enters (15).

Before generating a new level, compare `2^k` times the retained parent
count with `T`. If it exceeds `T`, invoke (6) on the same sampled
objective. Do not construct or query the oversized level. The initial
cell is treated directly. Otherwise generate its cells, query corners,
and filter as in Section 4. A cap after pruning would be too late to
bound the work of the generated candidates.

All list operations are linear in the generated count: each parent has
exactly `2^k` children, every cell has at most `2^k` corners, and the
two passes maintain a scalar incumbent and filter a list. No quadratic
list comparison, Cartesian join, or duplicate-removal procedure is
needed. The dyadic cells are already distinct. Their shared corners may
be queried repeatedly within the constant bound above.

Let `W=Z^(k/2)`. If the cap is ever hit at **any** level or requested
precision, (14) implies `W>B`. This is one event about the fixed
objective, not a union over levels or queries. With `r=kL/sigma`, (8)
gives, for `s>=1`,

\[
                       \Pr\{W>s\}\le r s^{-2/k}+\beta.    \tag{16}
\]

Integrating this tail yields

\[
 \mathbb E\min(B,W)\le
 \begin{cases}
  1+r+\beta B,&k=1,\\
  1+r\log B+\beta B,&k=2.
 \end{cases}                                               \tag{17}
\]

Moreover,

\[
 B\Pr\{\text{a cap is ever hit}\}\le B\Pr\{W>B\}
       \le r B^{1-2/k}+\beta B\le r+1.                    \tag{18}
\]

The cap probability therefore pays for the exponential base factor of
the exact fallback. Equation (17) pays for the ordinary levels. The
finite-grid atom term is controlled by (15), without a condition
`M h_j>=1`. In particular the argument remains valid for arbitrarily
fine levels of the same sampled objective.

## 6. Bit work, certificates, and exact value output

Let `b` be the bit length of the sampled coefficients. Equation (15)
gives `b=poly_d(I)`. A level-`j` core coordinate has `O(j)` denominator
bits. The corner solver, tangent certificate, comparisons, and cell
records therefore use `poly_d(I+j)` bits and work per corner. Scalar
minima and dyadic subdivision do not multiply denominators along the
search tree. There is no numerical residual-conditioning parameter.

For every draw and every `q`, the number of completed ordinary levels
is at most `J+1=O(I+q)`. Their work is bounded by
`512 min(B,W) poly_d(I+q)`. Add (6) on the cap event. Enlarging a fixed
polynomial if necessary, the entire query and its recorded computations
are bounded by

\[
 \left[512\min(B,W)+B_0\,\mathbf1_{\{W>B\}}\right]
                                      \operatorname{poly}_d(I+q).
                                                               \tag{19}
\]

This inequality holds simultaneously for all query precisions. Taking
expectations in its single random factor, then using (17)--(18) and
`log B=poly_d(I)`, proves (4). The same argument bounds expected output
and proof-record length. It does not claim a deterministic polynomial
bound on exceptional draws.

On the ordinary branch, the record contains the dyadic refinement and
pruning decisions, rational corner upper points and tangent lower
certificates, and the final interval (12). A verifier checks coverage
and every bound under the verified premises (1). Its work is linear
in the number of recorded cells times a polynomial in their bit lengths.
The growth-tail argument proves only the expected cost; a verifier does
not need to believe it to accept the interval. The exact fallback has
the independent global correctness and bit bounds in its linked proof;
its potentially long computations are charged through (18).

The evaluator may start from scratch at each query. It may also cache
an exact fallback value representation after the first cap and reuse
its refinement algorithm. Neither choice changes the noise sample or
the uniform bound (19). The returned feasible primal sequence need not
converge to one optimizer. The intervals (3), however, evaluate exactly
one fixed number, the global optimum of the sampled rational instance.

## 7. Zero curvature and scope

If `L=0`, independent endpoint rounding never increases the expected
core objective. Thus the global value is the minimum of the `2^k`
residual values at the core vertices. Query each convex residual problem
to interval width `2^{-q}`, take the minimum lower bound and minimum
feasible upper bound, and return its feasible point. The interval width
is at most `2^{-q}`. This is deterministic polynomial work for `k<=2`,
with no growth or probabilistic argument. It also covers a core-linear
objective and arbitrary tied residual minima.

The restriction `k<=2` is substantive to this proof. For larger fixed
`k`, the integral in (17) grows like `B^(1-2/k)`, and the fallback term
in (18) has the same uncontrolled factor. No all-dimensional impossibility
is inferred from this failed moment bound.

The theorem avoids the point-extraction implication in the reviewed
[Square Root Sum](convex-point-radical-comparison.md) and
[PosSLP](posslp-convex-point-extraction.md) reductions: it never promises
constant-distance coordinates of a true residual optimizer. It instead
gives arbitrary certified objective precision and a feasible point with
that objective gap, on one fixed draw. This differs both from a bare
implicit `argmin` definition and from a per-accuracy theorem that changes
the perturbation law as the accuracy grows.

## Verification status

The [fresh actual-file review](../reviews/core-only-noise-value-review.md)
passed the rounding intervals, generated-count cap, all-precision tail
argument, convex value oracle, and fallback accounting. Its
[exact probability diagnostic](../reviews/check_core_value_cap_review.py)
passed 18 finite laws, 7,154 draws, and 108 threshold checks, including
genuine flat endpoint atoms. These are reviewer-owned runs; the author
did not duplicate them. The separate
[actual-file grid review](core-only-noise-value-grid-review.md) passed.
Its independently executed inline diagnostic checked 108 stages, 5,656
cell lower bounds, and 2,131 safe prunes. The persistent copy is
[check_core_value_grid.py](check_core_value_grid.py); it was saved after
the inline run and was not rerun separately. These checks cover the
actual lower bounds, feasible upper witnesses, and pruning.

The author ran a targeted inline Python check of local links, display
delimiters, fences, trailing whitespace, and control characters. It
passed. No index edits, project-wide tests, or CI checks were made.
