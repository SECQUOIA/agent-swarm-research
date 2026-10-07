# Expected cell counts under independent linear perturbations

Date: 2026-10-02. Status: the direct argument passed
[independent review](../reviews/smoothed-semiconcave-cells-review.md).
No priority claim is made. This note proves an expected approximate-solver
bound directly from local grid comparisons. It does not integrate a
worst-case bound involving a global quadratic-growth constant.

## 1. Setting and the local counting lemma

Let

\[
 X=\prod_{i=1}^k[a_i,b_i],\qquad w_i=b_i-a_i>0,
\]

and let \(f:X\to\mathbb R\) be continuous. Assume upper coordinate
curvature at most \(\alpha>0\): with other coordinates fixed,
\(t\mapsto f(x_1,\ldots,t,\ldots,x_k)-\alpha t^2/2\) is concave.
The coordinates here are continuous. Remove fixed coordinates first;
if none remain, one evaluation solves the problem.

Independently sample coefficients \(c_i\), each with density at most
\(\rho_i\), and minimize

\[
 F_c(x)=f(x)+c^Tx.
\]

The base function and domain must be fixed independently of these
coefficients. Convexity, differentiability, uniqueness, and quadratic
growth are not assumed.

Choose positive integers \(m_i\), set \(h_i=w_i/m_i\), and use the
complete tensor grid with nodes \(a_i+\ell h_i\),
\(\ell=0,\ldots,m_i\). For \(\delta\ge0\), let \(N_\delta(c)\)
count grid nodes satisfying

\[
 F_c(v)\le\min_X F_c+\delta.
\]

**Counting lemma.**

\[
 \mathbb E N_\delta\le
 \prod_{i=1}^k\left[
 2+(m_i-1)\min\left\{1,
 \rho_i\left(\alpha h_i+\frac{2\delta}{h_i}\right)
 \right\}\right].                                      \tag{1}
\]

The same estimate holds if the minimum defining near-optimality is
the minimum over the complete grid instead of the whole box.

**Proof.** Fix a deterministic grid node \(v\). If coordinate \(i\)
is interior, near-optimality implies both neighboring comparisons

\[
 F_c(v)\le F_c(v+h_i e_i)+\delta,\qquad
 F_c(v)\le F_c(v-h_i e_i)+\delta.
\]

Consequently \(c_i\) belongs to the deterministic interval

\[
 \left[
 \frac{f(v)-f(v+h_i e_i)-\delta}{h_i},
 \frac{f(v-h_i e_i)-f(v)+\delta}{h_i}
 \right].                                               \tag{2}
\]

If the upper endpoint is below the lower endpoint, the event is empty.
Otherwise the interval length is

\[
 \frac{f(v+h_i e_i)+f(v-h_i e_i)-2f(v)}{h_i}
       +\frac{2\delta}{h_i}
 \le \alpha h_i+\frac{2\delta}{h_i}.                     \tag{3}
\]

The other random coefficients cancel in these comparisons. Thus the
intervals in (2) are fixed before any noise is sampled. Independence
multiplies their probability bounds over the interior coordinates.
An endpoint coordinate contributes the bound one. Sum these bounds over
the complete tensor grid: each coordinate has two endpoints and
\(m_i-1\) interior nodes. The sum factors, proving (1). QED.

The lemma uses only the displayed upper second-difference inequality.
Downward corners or arbitrarily large negative curvature do not obstruct
the proof. An upper curvature bound is essential to this argument.

## 2. Nested meshes without an aspect-ratio penalty

Put \(s=\max_i w_i\), \(h_j=s2^{-j}\). At level \(j\), let
\(m_{ij}\) be the smallest power of two such that

\[
 h_{ij}=w_i/m_{ij}\le h_j.
\]

Each \(m_{ij}\) stays unchanged or doubles from one level to the next,
so the grids and cell partitions are nested. At level zero there is
just one cell. For every refined coordinate, meaning \(m_{ij}\ge2\),

\[
 h_j/2<h_{ij}\le h_j.                                   \tag{4}
\]

An unrefined coordinate has no interior grid node, so a very short
original width incurs no inverse-width factor in the count.
This construction uses equal subdivisions of the whole coordinate
interval. It does not clip a uniform step and create a tiny final gap.

Define the common curvature correction for every level-\(j\) cell by

\[
 B_j=\frac{\alpha}{8}\sum_i h_{ij}^2
       \le\frac{k\alpha}{8}h_j^2.                       \tag{5}
\]

For \(\delta=2B_j\), equations (3)--(5) give, in every refined
coordinate,

\[
 \alpha h_{ij}+2\delta/h_{ij}
 \le (1+2k)\alpha h_{ij}.
\]

Therefore the following constant is independent of the level:

\[
 \boxed{\mathbb E N_{2B_j}\le H,\qquad
 H=\prod_{i=1}^k[2+(1+2k)\alpha\rho_i w_i].}             \tag{6}
\]

For fixed \(k\), this is polynomial in the numerical curvature, widths,
and density bounds. The dependence on \(k\) is not polynomial.

## 3. A cell algorithm that realizes the count

This section assumes exact feasible-point evaluations and exact
arithmetic/comparisons. It gives an actual search procedure; it does
not enumerate the complete fine grid to discover its good nodes.

At level zero process the original box. At later levels, subdivide
every retained cell according to the next nested partition. Each parent
has at most \(2^k\) children. For every processed cell \(C\), evaluate
its corners and form

\[
 L(C)=\min_{v\text{ corner of }C} F_c(v)-B_j.             \tag{7}
\]

Maintain the least value \(U_j\) of any feasible point evaluated so
far, with a point attaining it. After processing all cells at that level,
retain exactly those satisfying \(L(C)\le U_j\). Update the incumbent
before applying this test at the level.

Independent mean-preserving rounding within a cell, followed by the
coordinate-semiconcavity inequalities, gives

\[
 L(C)\le\min_C F_c.                                    \tag{8}
\]

Thus a cell containing a global minimizer always survives and all its
children are processed at the next level. Its corner evaluations give

\[
 U_j-\min_X F_c\le B_j.                                \tag{9}
\]

If \(C\) survives, one of its corners satisfies

\[
 F_c(v)=L(C)+B_j\le U_j+B_j\le\min_X F_c+2B_j.           \tag{10}
\]

A grid node belongs to at most \(2^k\) cells. If \(A_j\) is the
number retained at level \(j\), then deterministically

\[
 A_j\le2^kN_{2B_j},\qquad \mathbb E A_j\le2^kH.          \tag{11}
\]

Adaptivity causes no independence issue: (1) counts the entire
deterministic level grid, and the adaptively retained cells are a subset
covered by (10).

The level's certificate can use
\(L_j=\min_{C\text{ retained}}L(C)\). It satisfies

\[
 L_j\le\min_XF_c\le U_j,
 \qquad U_j-L_j\le B_j.                                \tag{12}
\]

For the last inequality, every evaluated corner has value at least
\(U_j\), so every level lower bound is at least \(U_j-B_j\).
Previously discarded cells have certified minimum above the incumbent
at discard time, hence above the current incumbent. A verification
record retains these discarded-cell bounds and the refinement tree.

Choose

\[
 J=\max\left\{0,\left\lceil\frac12
 \log_2\frac{k\alpha s^2}{8\varepsilon}\right\rceil\right\}.
                                                               \tag{13}
\]

Then level \(J\) gives a certified \(\varepsilon\)-solution for
every noise realization. There are at most \(2^kA_{j-1}\) processed
cells at any subsequent level and at most \(2^k\) evaluations per
processed cell. Hence the expected total number of point evaluations
through level \(J\), even without caching shared corners, is at most

\[
 2^k+8^k HJ.                                           \tag{14}
\]

Cell bookkeeping and certificate size obey comparable bounds, with
dimension-dependent factors. This establishes expected logarithmic
accuracy dependence for every fixed dimension in the exact-oracle
arithmetic model. Any point-evaluation and bit-arithmetic costs still
have to be included. The conclusion concerns the sampled objective.

If upper coordinate curvature is zero, separate concavity makes an
endpoint solve exact; the positive-\(\alpha\) mesh schedule is then
unnecessary.

## 4. Rational noise for a prescribed accuracy

The local counting argument also has a direct finite-bit version.
Suppose \(c_i\) is uniform on \(M_i\) equally spaced rational points
of \([-\sigma_i,\sigma_i]\), where \(M_i\ge2\). An interval of
length \(\ell\) has probability at most

\[
 \ell/(2\sigma_i)+1/M_i.                               \tag{15}
\]

Use the same proof of (1), replacing its interval probability bound by
the minimum of one and (15). For a prescribed terminal level \(J\),
choose \(M_i\ge m_{iJ}\). Then every level through \(J\) satisfies

\[
 \mathbb E N_{2B_j}\le
 H_{\rm rat}:=
 \prod_i\left[3+\frac{(1+2k)\alpha w_i}{2\sigma_i}\right].
                                                               \tag{16}
\]

The choice \(M_i=\max\{2,m_{iJ}\}\) is a power of two and is at most
\(\max\{2,2^J\}\). Sampling needs \(O(k(J+1))\) random bits.
For rational data and point oracles whose certification cost is
polynomial in input and coordinate bit lengths, the expected
approximation cost is polynomial in the accuracy bits and the numerical
parameters displayed in (16), at fixed \(k\).

This perturbation grid is chosen for the requested accuracy. A fixed
finite grid does not justify (16) at arbitrarily fine subsequent levels:
the atomic term \((m_{ij}-1)/M_i\) then grows. No exact-optimization
or fixed-distribution arbitrary-accuracy corollary is asserted here.

## 5. Application to a convex quadratic recourse oracle

Let \(X\subseteq\mathbb R^n\) be a nonempty compact rational
polytope, and let \(F\) be a rational quadratic with Hessian \(Q\).
Suppose rational \(\alpha>0\) and
\(T\in\mathbb Q^{r\times n}\) are supplied such that

\[
 Q+\alpha T^TT\succeq0.
\]

For \(a\in\mathbb R^r\), define the base value function

\[
 W(a)=\min_{x\in X}
       \left[F(x)+\frac\alpha2\|a-Tx\|^2\right].        \tag{17}
\]

Every fixed-\(a\) problem is a convex quadratic program. Compactness
gives an attained minimum, and \(W\) is continuous. Each fixed-\(x\)
function of \(a\) has coordinate curvature exactly \(\alpha\);
taking its infimum preserves coordinate semiconcavity. Thus \(W\)
satisfies the preceding theorem without any smoothness assumption on
the value function.

Independently sample \(d_i\in[-\sigma_i,\sigma_i]\), with bounded
densities or the rational grids of section 4, and perturb the original
objective to

\[
 F_d(x)=F(x)+d^TTx.
\]

This law perturbs coefficients independently in the supplied
\(T\)-coordinates. Its original-coordinate coefficient perturbation
is \(T^Td\), which is generally correlated and has lower-dimensional
support. It is a different law from independent noise in all original
linear coefficients.

Compute coordinate bounds
\(\ell_i=\min_{x\in X}(Tx)_i\),
\(u_i=\max_{x\in X}(Tx)_i\) by linear programming, and use the
fixed auxiliary box

\[
 A=\prod_{i=1}^r
 [\ell_i-\sigma_i/\alpha,\ u_i+\sigma_i/\alpha].         \tag{18}
\]

This box is independent of the sampled \(d\). The identity

\[
 W(a)+d^Ta
 =\min_{x\in X}\left[
 F_d(x)+\frac\alpha2\|a-Tx+d/\alpha\|^2\right]
       -\frac{\|d\|^2}{2\alpha}                        \tag{19}
\]

shows that

\[
 \min_{a\in A}[W(a)+d^Ta]
 =\min_{x\in X}F_d(x)-\frac{\|d\|^2}{2\alpha}.         \tag{20}
\]

Indeed, \(a=Tx- d/\alpha\) belongs to \(A\) for every
\(x\in X\). Apply the cell algorithm to the fixed base function
\(W\) with independent linear tilt \(d\).

At an evaluated \(a\), retain an exact minimizing witness \(x(a)\)
from the convex recourse solve. Equation (19) gives

\[
 F_d(x(a))\le W(a)+d^Ta+\frac{\|d\|^2}{2\alpha}.       \tag{21}
\]

Thus an auxiliary certificate \([L,U]\), with its incumbent's
recourse witness, gives the original feasible certificate

\[
 L+\frac{\|d\|^2}{2\alpha}
 \le\min_XF_d\le F_d(x(a))
 \le U+\frac{\|d\|^2}{2\alpha}.                        \tag{22}
\]

The gap does not increase. No projected growth, unique recourse witness,
or enumeration of the original feasible region is needed.
The expected auxiliary cell bound depends on dimension \(r\),
curvature \(\alpha\), auxiliary widths
\(u_i-\ell_i+2\sigma_i/\alpha\), and the noise densities.
Convex-QP evaluation, witness, and certificate costs must be added to
the cell count. The [convex residual note](convex-modulator-qp.md)
records the exact polynomial-bit convex-QP theorem and certificate
premise used here. For the rational version, these are exact rational
convex-QP solves at rational grid points; the grid-coordinate bit lengths
grow only linearly with the level, in addition to the input bit lengths.

The guarantee is for an epsilon-optimum of the perturbed problem.
Exact recovery under a fixed finite perturbation distribution needs a
separate argument and is outside this note.

## 6. Verification record and remaining limits

Independent mathematical review found no substantive gap in the local
interval calculation, levelwise incumbent invariant, anisotropic meshes,
finite-noise atoms, or the fixed auxiliary domain in (18).

The targeted command actually run was

```sh
python research-20261002/new-direction/check_smoothed_cells.py
```

It passed 30 exact-rational instances, 120 levels, 928 processed cells,
13,056 corner calls, and 17,630 complete-grid nodes used for independent
count checks. The fixtures are nonconvex lower envelopes of quadratic
wells in dimensions one through four, including anisotropic boxes.
Each cell's true minimum is computed independently by minimizing each
well on that cell. Checks cover local bounds, global certificates,
incumbent accuracy, near-optimal survivor corners, and the incidence
bound (11). They do not establish the probabilistic theorem by sampling.
No project-wide checks or CI inspection have been run for this note.

The direct theorem does not cover arbitrary coupled feasible sets in
its gridded variables. The recourse application handles its original
polytope constraints inside the supplied convex-QP oracle. Arbitrary
inexact evaluation requires explicit certified lower and feasible-upper
error budgets; the exact-oracle argument above must not be applied to
uncertified numerical values.
