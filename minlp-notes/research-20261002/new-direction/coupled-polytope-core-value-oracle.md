# Finite core-noise value evaluation with coupled polytope feasibility

Date: 2026-10-02. Status: complete and independently reviewed; the
[fresh composition review](../reviews/coupled-polytope-core-value-review.md)
and [separate oracle review](../reviews/convex-polytope-value-interface-review.md)
both passed. This extends the
[all-scale finite-law value theorem](all-scale-core-value-oracle.md)
from a product feasible domain to a rational polytope, under a supplied
joint convexification condition. No publication-priority claim is made.

The algorithm solves a convex relaxation on each core cell. Feasible
points inside retained cells replace the predecessor's feasible grid
corners. This permits coupled linear equalities and inequalities,
including lower-dimensional feasible sets and core projections.

## 1. Model and theorem

Let `P` be a nonempty bounded rational polytope in variables
`x=(v,z)`, with `v in [0,1]^k` and a supplied rational bounding box
for the remaining continuous coordinates `z`. The polytope may have
arbitrary linear coupling between these variables. Fix the polynomial
degree `d` and let `F_0` be an explicit rational polynomial. Supply
`alpha>=0` such that

\[
                F_0(v,z)+\frac\alpha2\|v\|^2
                    \quad\hbox{is convex on }P.             \tag{1}
\]

This is a valid verified premise, or has a supplied certificate.
The polynomial work claim assumes polynomial-time verification of
that certificate; any different verification cost is charged separately.
Include the certificate's encoding, the polytope,
bounding box, polynomial, core indices, `alpha`, and a rational noise
half-width `sigma>0` in base length `I`. Arbitrary polynomial convexity
recognition is not an uncharged step. All variables are continuous;
arbitrary integer feasibility is not covered by the convex cell oracle.

Perturb only the core by

\[
                         F_c(v,z)=F_0(v,z)-c^Tv.             \tag{2}
\]

The sign convention is immaterial for symmetric uniform noise.
For `k>=1` and `alpha>0`, there is one base-computable power-of-two
`M`, with `log M=poly_d(I)`, such that independent endpoint-inclusive
uniform `M`-point coefficients in `[-sigma,sigma]` admit the following
oracle for the same sampled rational objective.

For every integer `q>=0`, return a rational feasible point `x_q in P`
and rational bounds

\[
 a_q\le\min_P F_c\le U_q=F_c(x_q),\qquad
                              U_q-a_q\le2^{-q}.             \tag{3}
\]

Every draw and query are correct. Expected bit work and expected
proof/output size are at most

\[
       f(k)(1+\alpha/\sigma)^k\operatorname{poly}_d(I+q),    \tag{4}
\]

with `f(k)=k^{O(k)}` up to absolute constants and polynomial exponent
independent of `k` and the residual dimension. The dependence on
`alpha/sigma` is numerical. One random work factor of this expected
size bounds every requested precision simultaneously. No growth
constant, strict complementarity, residual strong convexity, or
interiority premise is supplied to the algorithm.

The output is an exact optimal-value Cauchy oracle and a feasible
objective approximation. It does not promise distance to an optimizer
or a polynomial-size expanded algebraic optimizer. Rare capped draws
use an exact algebraic fallback on the same sampled instance.

If `P` is empty, exact rational LP supplies an infeasibility certificate.
If `k=0` or `alpha=0`, the whole objective is convex on `P` and the
convex value interface below gives deterministic polynomial work.

## 2. Certified convex problems on coupled cells

For a dyadic core cell `C=prod_i[l_i,u_i]` of common side `h`, put

\[
 \begin{aligned}
 Q_C&=P\cap\{v\in C\},\qquad e_h=\alpha k h^2/8,\\
 \phi_{C,c}(v,z)
   &=F_c(v,z)+\frac\alpha2
                   \sum_i(v_i-l_i)(v_i-u_i).                 \tag{5}
 \end{aligned}
\]

The function `phi` is the convex function in (1) plus an affine
function and a constant, so it is convex on `Q_C`. Furthermore

\[
              0\le F_c(x)-\phi_{C,c}(x)\le e_h
                                      \quad(x\in Q_C).       \tag{6}
\]

The [polytope value interface](convex-polytope-value-interface.md)
checks whether `Q_C` is empty by exact LP. Otherwise it returns a
rational feasible `w_C in Q_C` and a certified lower bound `ell_C`
such that

\[
 \ell_C\le\min_{Q_C}\phi_{C,c}\le\phi_{C,c}(w_C),\qquad
                    \phi_{C,c}(w_C)-\ell_C\le e_h.          \tag{7}
\]

This costs polynomial bit work in `I`, sampled coefficient length,
and the dyadic level. The interface handles a lower-dimensional `Q_C`
by exact LP affine-hull reduction and relative epigraph optimization.
It repairs weak output by rational feasibility in a small coordinate
box, not by clipping coordinates and potentially violating constraints.
Its final lower certificate is a tangent bound with an exact rational
LP dual. No numerical regularity parameter is required.

Define the cell's feasible original upper value
`U_C=F_c(w_C)`, and retain the best incumbent `U` over all queried
cells and earlier levels. At a level, first compute all nonempty cell
answers, then retain precisely the cells with `ell_C<=U` against
the final incumbent. Empty cells are discarded with their LP
infeasibility certificates.

Every cell lower bound is globally valid on that cell because
`F_c>=phi`. A cell containing a global optimizer has `ell_C<=f*<=U`
and therefore survives. From that cell's upper answer and (6)--(7),

\[
                         U-f^*\le2e_h.                     \tag{8}
\]

Conversely, for every current nonempty cell,

\[
 \ell_C\ge\phi_{C,c}(w_C)-e_h
             \ge F_c(w_C)-2e_h\ge U-2e_h.                  \tag{9}
\]

Previously pruned cells have lower bounds above their then-current
incumbents, which are at least the new `U`. The current cells together
with those previously discarded cover `P`. Hence

\[
                            [U-2e_h,U]                      \tag{10}
\]

is a certified global value interval. No growth or probability claim
is used for its validity. Every retained cell has its own feasible
point satisfying

\[
                    F_c(w_C)\le U+2e_h\le f^*+4e_h.         \tag{11}
\]

This point can be anywhere in the cell. No coordinate rounding is
applied to a feasible point of `P`.

The algorithm begins with the whole core box and generates only
dyadic children of retained cells. A query stops when
`2e_h<=2^-q`, after `J=O(I+q)` levels unless the cap below is reached.
At each level the number of prospective children is checked before
their construction or oracle calls. The list operations are linear in
the generated count; there is one convex cell solve per nonempty cell.

## 3. Whole-cell packing on a possibly proper core projection

Define the true projected near-optimal set at scale `h` by

\[
 S_h(c)=\{v:\exists z\ (v,z)\in P,
                F_c(v,z)\le f_c^*+\alpha k h^2/2\}.         \tag{12}
\]

It is nonempty and compact as a projection of a compact joint
sublevel set. No continuity of a projected value function is assumed.
Set

\[
 \begin{split}
 K_h(c)&=\operatorname{conv}(S_h(c))+[-h,h]^k,\\
 D_h(c)&=\max_{y_0,\ldots,y_k\in K_h(c)}
                   |\det(y_1-y_0,\ldots,y_k-y_0)|,\\
 A(c)&=\sup_{0<h\le1}D_h(c)/h^k,\qquad W(c)=\max\{1,A(c)\}.
                                                               \tag{13}
 \end{split}
\]

The padding makes `K_h` full-dimensional even if the feasible core
projection is a point or a lower-dimensional polytope. Allow `W` to
be infinite on exceptional draws.

Each retained cell contains the core component of its near-optimal
point in (11), hence is contained in `K_h`. Distinct full dyadic
cells have disjoint interiors. The elementary maximum-simplex
comparisons from the predecessor give

\[
       D_h/k!\le\operatorname{Vol}(K_h)\le2^kD_h.
\]

Consequently

\[
  \#\text{retained cells}\le2^k A(c),\qquad
  \#\text{generated cells at the next level}\le4^k W(c).     \tag{14}
\]

The initial single cell is covered by this bound. Full cell volumes
are used for counting; they need not be feasible subsets of `P`.
Their inclusion in the padded body is all that is required. This
avoids grid-node incidence or assumptions that core corners are feasible.

## 4. The same all-scale weak first-moment tail

The conjugate construction from the
[all-scale theorem](all-scale-core-value-oracle.md) applies directly
to compact `P`. Define on all coefficient space

\[
 b(c)=\max_{(v,z)\in P}\{c^Tv-F_0(v,z)\},\qquad
 H(c)=b(c)+\|c\|^2/(2\alpha).                               \tag{15}
\]

The function `b` is finite convex, with every subgradient in
`conv(proj_v P)`, a subset of `[0,1]^k`. Thus `H` is
`1/alpha`-strongly convex and `grad H*` is alpha-Lipschitz.
The locally finite measure

\[
                 \mu(E)=\operatorname{Leb}
                          \{y:\nabla H^*(y)\in E\}          \tag{16}
\]

has the same bounding-box mass estimate as in the predecessor.

For `v in S_h(c)`, near-optimality gives the Fenchel residual bound
at `y_0=v+c/alpha` of `epsilon_h=alpha k h²/2`. Its gradient norm
there is at most `sqrt(2alpha epsilon_h)=sqrt(k)alpha h`.
The larger padding in (13) has `||u||<=sqrt(k)h`, so smoothness gives

\[
 H(c)+H^*(y_0+u)-c^T(y_0+u)
 \le\epsilon_h+\sqrt{k}\alpha h\|u\|
                         +(\alpha/2)\|u\|^2
 \le2k\alpha h^2.                                          \tag{17}
\]

Convexity of the residual extends this bound over `K_h+c/alpha`.
It follows that this translated body is mapped by `grad H*` into
the open ball `B(c,4k alpha h)`, since
`2sqrt(k)alpha h<4k alpha h`. Therefore

\[
                  \operatorname{Vol}(K_h(c))
                     \le\mu(B(c,4k\alpha h)).               \tag{18}
\]

The same `5r` covering argument and local mass estimate now give,
for continuous uniform core noise and every `T>0`,

\[
 \Pr\{A(c)>T\}\le a_k/T,\qquad
 a_k=(180k^3)^k(1+\alpha/\sigma)^k.                          \tag{19}
\]

Only compact joint attainment and the bounded core projection were
used. There is no smooth projected-value or full-dimensionality
assumption hidden in this transfer.

For the finite law, the strict event `A(c)>T` has the same finite
two-block formula. Existentially choose `0<h<=1`, the `k+1` points
of a witnessing simplex, and Caratheodory representations using
points `v_ij in S_h(c)` plus padding `|u_i,l|<=h`. For each such
point choose a feasible residual witness `z_ij` and require

\[
 F_c(v_{ij},z_{ij})\le F_c(v,z)+\alpha k h^2/2
                      \quad\text{for every }(v,z)\in P.     \tag{20}
\]

All comparisons use one universal competitor block. The original
linear inequalities describe membership in `P`. The determinant
threshold `|det|>T h^k` uses the predecessor's polynomial-size
quadratic QR and scalar product-chain encoding; no factorial-sized
symbolic determinant is expanded. All witnesses remain in the
existential block. The total variable, atom and monomial counts are
polynomial in base size, and degree is bounded by `max(d,2)`.

The verified fixed-block quantifier-elimination bound gives a
base-computable scalar-section component bound independent of
coefficient heights and `T`. Marginal finite-grid transfer therefore
supplies a base-computable `C_0=2^{poly_d(I)}` with

\[
 \Pr\{W>s\}\le a_k/s+\beta\quad(s\ge1),\qquad
                                      \beta=C_0/M.          \tag{21}
\]

This bound holds at every threshold for one fixed law, including
singular and tied atoms. It describes a finite determinant event;
no quantifier over a volume or an integral is invoked.

## 5. One cap, one rational law, every accuracy

The [polytope fallback interface](convex-polytope-value-interface.md)
supplies a base-only budget `B_0=2^{poly_d(I)}` for arbitrary sampled
rational coefficients. It replaces the box membership predicate in
the lexicographic two-block fallback by membership in `P`. Feasible
rational approximation is repaired inside `P` intersected with a
rational coordinate-error box around the approximate exact optimizer;
coordinate clipping is not used.

Choose before sampling `B>=max(2,B_0)` with `log B=poly_d(I)`, and
let `M` be the least power of two at least `max(2,C_0B)`. Use the
per-level generated-cell cap

\[
                            T_{\mathrm{cells}}=4^k B.       \tag{22}
\]

If `2^k` times the retained parent count would exceed this cap,
invoke exact fallback before generating that level, on the same
sampled objective. By (14), any cap at any level or query implies
`W>B`. There is no union bound over scales or requested precisions.

The tail (21) gives

\[
 \mathbb E\min(B,W)\le1+a_k\log B+\beta B,\qquad
             B\Pr\{W>B\}\le a_k+\beta B.                    \tag{23}
\]

Here `beta B<=1`. The ordinary branch uses at most `O(I+q)` levels,
each with polynomial bit work per generated cell. The lower-dimensional
LP geometry has input length polynomial in `I+j`, so its conditioning
enters only through that bit length. The fallback has cost
`B_0 poly_d(I+b_c+q)`, with exponential factor independent of sampled
height `b_c` and accuracy. Since `b_c=poly_d(I)`, the entire query
work and trace length satisfy the common pathwise bound

\[
       [4^k\min(B,W)+B_0\mathbf1_{\{W>B\}}]
                              \operatorname{poly}_d(I+q).   \tag{24}
\]

Taking expectations proves (4). Neither the cap nor the law depends
on `q`, and there is no condition relating the core mesh to the noise
grid. Ordinary certificates use only (1), exact feasibility,
convex tangent/LP-dual lower bounds, the correction (6), and the
pruning trace. Their validity is independent of the probabilistic
analysis. The fallback remains correct on every exceptional draw.

## 6. Interpretation and scope

The restriction (1) is stronger than convexity in residual coordinates
at each fixed core point. It supplies a joint convex problem on every
coupled cell. For example, a bilinear core/residual term with no
residual curvature need not admit any such core-only convexifier.
The theorem does not remove this restriction by assuming a repair
or sensitivity bound implicitly.

A concrete nonlinear family is
`F_0(x)=sum_j lambda_j(a_j'x+b_j)^4+q(x)-(alpha/2)||v||²`,
where all data are rational, `lambda_j>=0`, and `q` is a convex
quadratic with a supplied positive-semidefinite matrix certificate.
Each fourth power of an affine function is convex, so (1) has a
direct polynomial-time-verifiable decomposition. Arbitrary rational
linear balances, resource constraints and bounds can be placed in `P`.
Fixed degree keeps explicit expansion polynomial in the input size.

The standard relaxation (5) is the secant underestimate of the
concave quadratic in a difference-of-convex decomposition. The
addition here is the all-scale finite-noise count and bit-model
completion on a coupled feasible polytope, including lower-dimensional
cells. The underlying convexification is not presented as new.

An equality lifting also covers a supplied rational linear factor
`v=Cx`: if `F_0(x)+(alpha/2)||Cx||²` is convex on a bounded rational
polytope, retain the equality `v=Cx` in a lifted polytope. Known
coordinate bounds can normalize `v` to the unit box. For positive
coordinate widths `w_i`, a sufficient new scalar is
`alpha_bar=alpha max_i w_i²`; the remaining diagonal correction is
convex, and the translation contributes only an affine term.
Fixed factor coordinates can be removed. The scaling
changes the necessary convexification parameter and the physical
noise directions; widths and coupling constants are charged, not
claimed to disappear. This gives a supplied rank-`k` convexification
interpretation, with correlated noise in the original `x` coordinates.

For quadratic objectives, related low-rank and aligned-noise exact
QP results already exist locally, including
[the exact cell-closure theorem](smoothed-exact-cell-closure.md).
The present value result should not be described as the first
arbitrary-rank exact QP theorem. Its nonlinear objective class,
coupled-cell oracle, and value-only output are the relevant distinctions.
The [focused source comparison](../prior-art/coupled-polytope-core-value-oracle-prior.md)
places the correction alongside alphaBB and low-negative-inertia QP
branching. Those are precedents for the underestimator and partitioning;
the stated addition is the finite-law, all-precision expected bit
composition on coupled polynomial cells. The comparison makes no
publication-priority claim.

## Verification status

The [fresh actual-file composition review](../reviews/coupled-polytope-core-value-review.md)
passed the full proof and oracle composition, including the changed
padding constants, finite-law transfer, and base-only fallback budget.
The [separate interface review](../reviews/convex-polytope-value-interface-review.md)
also passed. The parent independently read both complete notes and
reported no gap; that was a separate analytic check.

The distinct exact diagnostic
[check_coupled_polytope_cells.py](check_coupled_polytope_cells.py)
uses `z=v_1+v_2`, the coupled bound `z<=1`, optional equality `z=1`
or a 101-bit thin bound, and the objective
`(z-1/3)^2-(v_1²+v_2²)/2-c'v`. Its supplied convexifier is one.
Rational face enumeration solves these small fixtures exactly and
produces deliberately inexact convex-cell answers with tangent LP
dual certificates. This tests feasible witnesses inside cells, not
an assumption that grid corners are feasible.

The [saved results](coupled-polytope-cell-results.json) report 108 levels,
391 generated cells, 54 empty cells, 246 positive relative-ball checks,
91 singleton cells, 337 tangent dual certificates, 123 retained
witnesses, 246 noncorner oracle points and 108 global value intervals.
Another 81 error-box repairs check simultaneous core and objective
accuracy through 200-bit requests. A separate example confirms that
ambient coordinate clipping does not restore the coupled equality.

The command actually run was:

```
python research-20261002/new-direction/check_coupled_polytope_cells.py
```

These are arithmetic and algorithm-interface checks, not a stochastic
performance estimate or an implementation of the general GLS and
algebraic fallback algorithms. No index edits, project-wide tests
or CI inspection were used.
