# Core-only noise with strongly convex recourse and changing residual faces

Date: 2026-10-02. Status: independently reviewed; targeted checks passed. This extends the
[interior-recourse theorem](core-only-noise-strong-recourse.md) by removing
its conditional-interiority assumption. Uniform residual strong convexity
remains a supplied, verified premise. Arbitrary convex residual fibers
are outside this result.

## 1. Statement and inherited algorithmic interfaces

Let `F_0` be a rational polynomial of fixed degree `d` on `[0,1]^n`.
Supply a core of size `k`, rational `L,mu>0`, and checkable certificates

\[
 F_{ii}\le L\quad(i\text{ in the core}),\qquad
 H_{RR}\succeq\mu I\quad\text{throughout the box}.             \tag{1}
\]

Charge these certificates and their verification in the base input
length `I`. No active pattern, residual multiplier margin, interior
selector, or explicit selector formula is supplied. Remove fixed
coordinates first. The cases `k=0` and `R` empty use direct convex output
and the direct core-corner algorithm, respectively; henceforth both sets
are nonempty.

Perturb only the core by independent coefficients uniform on the same
endpoint-inclusive `M`-point rational grid in `[-sigma,sigma]`. A power of
two `M` is fixed from the base data before sampling, with
`log M=poly_d(I)`. Exact implicit optimization on every sampled instance
has expected initial bit work and expected output/proof-record size

\[
 8^k\left[3+\frac{(1+k)L}{2\sigma}\right]^k
                   \operatorname{poly}_d(I).                 \tag{2}
\]

The ordinary output is a globally certified strongly convex polynomial
on a rational product patch, with some original core or residual bounds
fixed. Its unique constrained minimizer and value are an exact implicit
answer. Coordinate/value refinement to `q` bits is polynomial in `I+q`.
An unresolved draw uses the same-draw
[exact algebraic fallback](polynomial-exact-fallback.md); its representation
and refinement may be large, but have polynomial expected contribution.
The full global pruning trace has an expected-size bound, not a uniformly
small per-draw bound. Subsequent expected evaluation has a polynomial
bound in `I+q` after the global proof is established.

The numerical factor in (2) uses the original core curvature `L`.
Residual conditioning and mixed derivatives enter the polynomial bit
precision, through logarithms of bounds derived below. They are not
additional numerical parameters in that factor.

Certified approximate convex recourse, the corrected-corner search,
excluded-slab containment, compact tangent lower certificates, and exact
patch evaluation are the interfaces proved in
[polynomial box recourse](smoothed-polynomial-box-recourse.md). The new
point is why a strongly convex patch exists with high enough probability
under core noise, despite changing and weakly active residual bounds.

## 2. Sensitivity, projected growth, and core active gradients

Choose rational coefficient bounds

\[
 M_1\ge\max\{1,\max_i\sum_j\sup|F_{ij}|\},\qquad
 T\ge\max\{1,\max_i\sum_{j,l}\sup|F_{ijl}|\},\qquad H=M_1/\mu.
 \tag{3}
\]

The selector `s(v)` is unique and `H`-Lipschitz by strong monotonicity
and the fixed-box variational inequalities. The value
`V(v)=F_0(v,s(v))` is continuously differentiable, with
`grad V=F_C(v,s(v))`, including its derivatives along original core
faces. Its gradient is Lipschitz with bound
`H_V=M_1(1+H)`. Partial minimization preserves the coordinate upper
curvature `L`.

Projected point growth `g_V` at a core optimizer lifts to full point growth

\[
 g_F=\min\{g_V/(1+2H^2),\mu/4\}.                            \tag{4}
\]

Neither sensitivity nor (4) assumes interiority. The proof and the exact
two-block projected-growth formula are in the restricted theorem. For
one finite product law the latter gives a base-computable
`C_tail=2^{poly_d(I)}` such that

\[
 \Pr\{g_V<g\}\le kg/\sigma+2kC_{\rm tail}/M.                \tag{5}
\]

An active core-gradient tail now counts **all** original full-coordinate
faces. Conditional on other core coefficients, the stationarity system
on a face is independent of the coefficient of a fixed core coordinate.
Positive projected growth implies (4); two-sided directions along the
actual face then give a positive definite free Hessian. The relevant
stationary root is nonsingular, even if other stationary components are
singular. The isolated-root bound therefore gives

\[
 \Pr\{g_V>0,\ \text{some active core gradient has magnitude}\le\tau\}
 \le K_C(\tau/\sigma+1/M),\quad
 K_C=\max\{1,k3^n\max(1,d-1)^n\}.                           \tag{6}
\]

Residual gradient coefficients are never randomized in this argument.
The extra residual faces only enlarge the base-only counting constant.

## 3. A stable residual branch with a base-only noise tail

For each closed original core face `K` with `q>=1` free coordinates, let
`S_K` be its affine boundary together with the relative boundaries of
the residual active sets `{s_i=0}` and `{s_i=1}`. These are compact
semialgebraic sets of dimension at most `q-1`. Put
`E_K=-grad_K V(S_K)`.

The [active-stratum tube lemma](core-noise-active-stratum-tube.md) gives
a coefficient-height-independent degree bound `D_*=2^{poly_d(I)}` for
a nonzero polynomial whose zero set contains each `E_K`. It follows from
three-block elimination of the residual box KKT graph. The algorithm
needs the degree bound, not the eliminated polynomials or the active sets.

The same lemma, using the primary algebraic tube estimate and an exact
grid-jitter argument, supplies

\[
 \Pr\{\operatorname{dist}(\gamma_K,E_K)\le\delta\}
 \le C(q,D_*)\left(\delta/\sigma+\sqrt q/M\right),
 \quad C(q,D)=16q^{q+1}D(4D+2)^{q-1}.                       \tag{7}
\]

Truncate the right side at one if needed. This includes atoms exactly
on the exceptional set. Choose
`C_S=3^k max_{1<=q<=k} C(q,D_*)`. At a face-stationary optimum,
`gamma_K=-grad_K V(a)`. Gradient Lipschitz continuity therefore implies

\[
 \Pr\{\text{the optimal core lies within }2\eta
          \text{ of its face's }S_K\}
 \le C_S(2H_V\eta/\sigma+k/M).                              \tag{8}
\]

This is a union over faces fixed before sampling, not conditioning on an
adaptively chosen face. Faces of dimension zero are omitted: they have
no core tangent direction and no branch transition to avoid.

Outside the event in (8), a Euclidean core ball of radius `eta` on the
optimal face has constant residual bound status. The free residual
coordinates form a smooth implicit stationary branch there, since their
Hessian is at least `mu I`. Active residual multipliers are nonnegative
throughout that ball; they need not be bounded away from zero.

## 4. Small residual multipliers may remain free

Set `m=|R|` and

\[
 K_3=\max\{1,nT(1+H)^3\}.
\]

On any stable branch, `K_3` bounds each active residual multiplier's core
Hessian. Differentiating free stationarity gives this bound without
requiring a residual distance to its endpoints. The detailed calculation
and the following simultaneous-release estimate are proved in the
[small-multiplier lemma](small-residual-multiplier-curvature.md).

Suppose projected growth is at least `g` and the stable core ball has
radius `eta`. Set

\[
 \theta=\min\{K_3\eta^2/2,\mu g/(4mK_3)\},\qquad
 \nu=\min\left\{\mu/2,
       \frac{\min\{g,\mu/2\}}{1+2H^2}\right\}.             \tag{9}
\]

Fix active residual bounds with multiplier greater than `theta`, but
leave every other residual coordinate free. The full Hessian on the
remaining coordinates, after the active core coordinates have been fixed,
is at least `nu I` at the optimizer.

Indeed, eliminate the already free residual coordinates. The reduced
core Hessian is at least `2g I`, and the reduced residual Hessian is at
least `mu I`. For each released multiplier, nonnegativity on a two-sided
ball and its Hessian bound imply
`||grad lambda_i||^2<=2K_3 lambda_i`. Their combined squared cross norm
is at most `2mK_3 theta<=mu g/2`. Thus the reduced Hessian is at least
`diag(g I,mu I/2)`. Completing the square when restoring the eliminated
coordinates gives (9). Further sound fixings leave a principal matrix
and preserve the same lower bound.

If the optimal core face has dimension zero, residual strong convexity
directly gives a modulus at least `mu`, so (9) is a valid weaker bound
without any branch ball. This treats the boundary case without applying
a two-sided multiplier estimate in nonexistent core directions.

## 5. One pre-draw budget and a sound closure test

Take a base-only fallback factor `B=2^{poly_d(I)}>=2`, large enough for
initial exact output and subsequent refinement. Define

\[
 \rho=1/(6B),\quad
 g=\rho\sigma/(2k),\quad \tau=\rho\sigma/(2K_C),\quad
 \eta=\min\{1/4,\rho\sigma/(4C_SH_V)\}.                    \tag{10}
\]

Compute `theta,nu` by (9), and use the conservative common margin

\[
 g_* =\min\{g/(1+2H^2),\mu/4,\nu/4\}.                    \tag{11}
\]

Choose a rational bound `G>=1` on the core gradient one-norm for all
allowed noise, and put

\[
 r=\min\{1/8,\tau/(16M_1),\theta/(16M_1),g_* /(4T)\},
 \qquad A_0=2+(kL+8)/g_* .                                 \tag{12}
\]

Let `J` be the least nonnegative integer for which `h_J=2^-J` satisfies

\[
 h_J\le\min\{r/(4A_0),g_*r^2/(16GA_0)\}.                  \tag{13}
\]

Finally choose the least power of two

\[
 M\ge\max\{2,2^J,4kC_{\rm tail}/\rho,
                   2K_C/\rho,2C_Sk/\rho\}.                \tag{14}
\]

Every quantity before (14) depends only on base data. All have polynomial
binary length, so `J,log M=poly_d(I)`. No sampled optimum height or
noise-dependent reconstruction cutoff enters this order of choices.
Equations (5), (6), and (8) each give failure probability at most `rho`.
Their union has probability at most `1/(2B)`.

Run the predecessor's approximate-recourse search through level `J`.
At level `j`, use corner accuracy `e_j=kLh_j^2/8`, incumbent upper value
`U`, and the rule `min_corner lower-e_j<=U`. All global optima remain in
the retained core hull; `U-f*<=2e_j`, and every retained cell has a true
`4e_j`-near-optimal corner. Only core noise is needed for the expected
count in (2), including its finite-grid correction because `M>=2^J`.

Center the residual patch at the incumbent feasible completion, with
radius `r`, clipped by the original box. Query its at most `2m` closed
excluded slabs to accuracy `g_*r^2/16`. Omit a slab when its raw threshold
is at or beyond an original endpoint. Accept containment only if the
minimum certified excluded lower value minus `U` exceeds
`2G diam_inf D`, where `D` is the retained core hull. This is an exact
sound certificate that every conditional optimizer on `D` lies in the
patch, independent of any growth promise.

On that product patch, test uniform strict derivative signs at eligible
original bounds of **all** coordinates. Fix every bound certified this
way. For example, a midpoint derivative and the rational row-sum variation
bound `M_1 r_Q` give a sufficient uniform sign test. On the remaining
box with midpoint `c` and infinity radius `r_Q`, test exactly

\[
                 H_F(c)-(Tr_Q+g_*)I\succeq0.               \tag{15}
\]

These tests are sound on every draw and yield the exact implicit convex
patch when they pass. If every coordinate is fixed, evaluate that feasible
point exactly instead of applying an empty Hessian test. The algorithm does not construct or identify the
stable branch or classify a multiplier as small.

On the complement of the three bad events, the inherited localization
proof applies with full growth `g_*`: the excluded lower gap is at least
`7g_*r^2/16`, whereas `2G diam_inf D<=g_*r^2/4`. Every patch point is
within `5r/4` of the optimum in infinity norm. Equations (12) ensure the
uniform sign tests fix all active core gradients greater than `tau` and
all active residual multipliers greater than `theta`. Additional sound
fixings are harmless. Section 4 leaves a free Hessian at least
`nu I>=4g_* I` at the optimum. Since the optimum belongs to the remaining
box, the midpoint variation and `r_Q<=r` make (15) pass; indeed its slack
is at least `3g_*-2Tr>=5g_*/2`.

Consequently closure succeeds by `J` outside a set of probability at
most `1/(2B)`. Exact fallback on the remaining samples contributes only
polynomial expected cost. All per-call derivative bounds, recourse
accuracies, convex evaluation, and rational arithmetic have polynomial
bit cost. This proves (2) with the stated all-draw output semantics.

## 6. Scope and verification status

The result removes both residual noise and a global conditional-
interiority assumption. It permits residual active-pattern changes and
identically zero residual multipliers. Uniform residual strong convexity
is still essential to this proof: it supplies a unique Lipschitz selector,
bounded implicit derivatives, and a positive residual Schur block.
The [rotating-fiber examples](core-only-noise-rotating-fiber.md) show why
mere residual convexity or strict convexity does not justify this closure.

This class does admit a fixed rank-`k` concave-quadratic decomposition.
Indeed, the Schur complement and (3) give
`H_F + alpha diag(I_C,0) >= 0` for `alpha=M_1+M_1^2/mu`.
Thus adding that core quadratic makes the full objective convex. The
resulting curvature parameter can be much larger than the original `L`.
The contribution here is preserving `L/sigma` in the numerical search
factor, together with exact core-only-noise closure despite changing and
weakly active residual faces. It is not a claim that the objective lacks
a fixed low-rank quadratic decomposition.

This is not an efficient recognition theorem for the certificates in
(1), nor a claim that the eliminated value function has small explicit
degree or representation. The algebraic sets in the probability proof
are never computed by the optimization algorithm. The coefficient-height-
independent tube theorem supplies an input-precision bound, not an
extra enumeration step.

The [fresh independent composition review](core-only-noise-boundary-recourse-independent-review.md)
passed without a substantive correction. A
[separate supporting-lemma review](core-noise-boundary-lemmas-independent-review.md)
checked the tube and quantitative multiplier arguments. The primary tube
contract was independently read and verified by the literature reviewer;
its source is recorded in the linked tube note.

The author ran
`python research-20261002/reviews/check_core_only_boundary_recourse.py`.
The [exact rational diagnostic](../reviews/check_core_only_boundary_recourse.py)
passed two weak-multiplier releases, three sound residual fixings, seven
changing-active-pattern/KKT cases, one core-vertex closure with an
indefinite original full Hessian, and nine three-event finite-law budgets.
The nonlinear release fixture has a zero residual multiplier at a genuine
endpoint noise atom and an indefinite Hessian elsewhere in the original
box. These tests exercise the new closure and budget interfaces; they are
not an implementation of the entire general algorithm.

The restricted antecedent has its own independent review and nonlinear
recourse diagnostic. No project-wide checks, CI inspection, or index
edits were performed.
