# Expected exact integer optimization under low-rank linear perturbations

Date: 2026-10-02. Status: complete proof with two fresh independent
reviews. No literature-priority claim.

Separable convex quartics minus a supplied low-rank concave quadratic
admit an expected exact algorithm on integer product boxes under an
explicit rational perturbation law. The number of integer variables is
unrestricted, interval endpoints are binary encoded, and no quadratic
growth or uniqueness assumption is required. The proof combines exact
separable integer recourse, the
[direct expected cell count](smoothed-semiconcave-cells.md), and a common
objective-value lattice.

The key precision distinction is that the original integer objective
has denominator proportional to `M-1` when the noise uses a common
`M`-point grid. Auxiliary quadratic values can have larger denominators,
but their lattice is not used for exact recovery. This permits one fixed
noise grid to support both the cell count and exact termination.

## 1. Model and result

Let

\[
 X=\prod_{j=1}^n\{L_j,L_j+1,\ldots,U_j\},
 \qquad L_j,U_j\in\mathbb Z,\quad L_j\le U_j,
\]

and let each rational polynomial `g_j` have degree at most four and be
convex on the real interval `[L_j,U_j]`. Define

\[
 G(x)=\sum_{j=1}^n g_j(x_j),\qquad
 F(x)=G(x)-\frac\alpha2\|Tx\|^2,
\tag{1}
\]

where rational `alpha>0` and `T in Q^(r x n)` are supplied. The rows
need not be linearly independent. In particular, the canonical convex
quartics `lambda_j x_j^4+mu_j x_j^2/2+b_j x_j+c_j`, with
`lambda_j,mu_j>=0`, are covered. On a nondegenerate interval, convexity
of a general quartic can be checked exactly by minimizing its quadratic
second derivative. A singleton integer interval is handled directly.

For each row choose a positive rational noise half-width `sigma_i`.
The perturbed objective is

\[
 F_d(x)=F(x)+d^TTx.
\tag{2}
\]

The `d_i` will be independent; the perturbation of the original `n`
linear coefficients is `T^T d`, which is generally correlated and
supported on a subspace of dimension at most `r`. This is not the law
of independent noise in all original coordinates.

If `r=0`, the objective separates and the direct integer recourse in
Section 2 solves it without perturbations or a mesh. Below assume `r>=1`.

Compute the exact row ranges

\[
 \ell_i=\min_{x\in X}(Tx)_i,\qquad
 u_i=\max_{x\in X}(Tx)_i.
\]

Each minimum and maximum is a sum of the appropriate endpoint choices,
requiring only `O(rn)` rational operations. Put

\[
 A=\prod_{i=1}^r
 [\ell_i-\sigma_i/\alpha,\ u_i+\sigma_i/\alpha],
 \qquad
 w_i=u_i-\ell_i+2\sigma_i/\alpha,
 \qquad s=\max_i w_i.
\tag{3}
\]

All `w_i` are positive. Constant or zero rows may be kept; they only
increase the auxiliary dimension and its displayed constants.

Let `Q` be the product of the positive denominators of all base rational
data: the coefficients of the `g_j`, `alpha`, the entries of `T`, and
the `sigma_i`. Define

\[
 D_0=2Q^3,
 \qquad
 M=\text{the least power of two at least }
       \max\{2,r\alpha s^2D_0\},
 \qquad J=\log_2 M.
\tag{4}
\]

Independently choose integers `K_i` uniformly in `{0,...,M-1}` and set

\[
 d_i=-\sigma_i+\frac{2\sigma_i K_i}{M-1}.
\tag{5}
\]

This law is fixed before optimization starts. It uses exactly `rJ`
unbiased random bits. All its parameters have polynomial bit length in
the base input, including the noise half-widths.

**Theorem.** For every draw (5), there is a deterministic algorithm
returning an exact integer optimizer and exact rational optimum of (2).
For a fixed polynomial `P` with absolute degree, its expected bit work is
at most

\[
 \boxed{
 8^r H_{\rm rat}P(I),\qquad
 H_{\rm rat}=
 \prod_{i=1}^r
 \left[3+\frac{(1+2r)\alpha w_i}{2\sigma_i}\right],}
\tag{6}
\]

where `I` is the base rational input length, including all integer
endpoints and the `sigma_i`. No objective growth modulus, separation
promise, or unique optimum is assumed.

Consequently, fixed `r` and numerically polynomial bounds on the ratios
`alpha w_i/sigma_i` give expected polynomial bit time. Binary encoding
alone does not bound these ratios. If the ratios have a common bound
independent of `I`, (6) instead has the form `f(r) P(I)`. These numerical
and parameter distinctions are part of the statement.

The algorithm solves the single perturbed objective (2), including all
draws with ties. It never resamples. It does not recover the exact
optimizer of the unperturbed objective.

## 2. Exact integer recourse in polynomial bit time

For a rational auxiliary vector `a in R^r`, define

\[
 W(a)=\frac\alpha2\|a\|^2+
       \min_{x\in X}[G(x)-\alpha a^TTx].
\tag{7}
\]

The inner problem separates into the integer minimizations of

\[
 \psi_j(z)=g_j(z)-\alpha(T^Ta)_j z,
 \qquad z\in\{L_j,\ldots,U_j\}.
\]

Each `psi_j` is convex on its real interval, so its forward differences

\[
 \Delta_j(z)=\psi_j(z+1)-\psi_j(z)
\tag{8}
\]

are nondecreasing. Binary search for the first `z` in
`{L_j,...,U_j-1}` with `Delta_j(z)>=0`. If it exists, choose it; if
none exists, choose `U_j`. A singleton interval needs no search.
This returns an exact integer minimizer using
`O(1+log(U_j-L_j+1))` rational comparisons. Ties cause no difficulty.

The coordinate's optimality can be certified by its two available
neighbor conditions:

\[
 \Delta_j(z-1)\le0\quad\text{if }z>L_j,
 \qquad
 \Delta_j(z)\ge0\quad\text{if }z<U_j.
\tag{9}
\]

The resulting vector `x(a)` is a feasible exact witness for (7).
Quartic evaluation at binary-encoded integers, rational difference
comparisons, and the sums in (7) have polynomial bit cost in the base
input and the encoding length of `a`. The number of integer coordinates
does not occur in an exponential factor, and their domains are not
enumerated. No general mixed-integer convex optimization oracle is
assumed.

## 3. A fixed auxiliary box and an exact transfer of the gap

Completing the square in (7) gives

\[
 W(a)=\min_{x\in X}
       \left[F(x)+\frac\alpha2\|a-Tx\|^2\right].
\tag{10}
\]

The finite minimum is continuous, and
`W(a)-alpha||a||^2/2` is the infimum of affine functions of `a`, hence
concave. In particular, `W` has upper coordinate curvature `alpha`
on the fixed box `A` in (3). The base function and box are independent
of the sampled noise.

For `Z_d(a)=W(a)+d^T a`,

\[
 Z_d(a)
 =\min_{x\in X}\left[
 F_d(x)+\frac\alpha2\|a-Tx+d/\alpha\|^2\right]
   -\frac{\|d\|^2}{2\alpha}.
\tag{11}
\]

Since `|d_i|<=sigma_i`, every point `Tx-d/alpha` lies in `A`.
Consequently, writing `C_d=||d||^2/(2alpha)`,

\[
 \min_{a\in A}Z_d(a)=F_d^*-C_d.
\tag{12}
\]

At any evaluated `a`, the exact recourse witness also satisfies

\[
 F_d(x(a))\le Z_d(a)+C_d.
\tag{13}
\]

Thus a certified auxiliary interval `[L,U]`, with `U=Z_d(a)` at an
evaluated point, gives

\[
 L+C_d\le F_d^*\le F_d(x(a))\le U+C_d.
\tag{14}
\]

The same witness is an original integer vector. Inner minimizers may
be nonunique; every attaining witness has property (13).

## 4. The cell algorithm and the expected count

Use the nested equal subdivisions from the
[semiconcave cell note](smoothed-semiconcave-cells.md). At level `j`, set

\[
 h_j=s2^{-j},\qquad
 m_{ij}=\text{the least power of two with }w_i/m_{ij}\le h_j,
 \qquad h_{ij}=w_i/m_{ij},
\]

and use the product partition with those coordinate subdivision counts.
Then `m_ij<=2^j`; each count stays unchanged or doubles at the next
level. For a refined coordinate, `h_j/2<h_ij<=h_j`.
Every level-`j` cell has the same curvature correction

\[
 B_j=\frac\alpha8\sum_{i=1}^r h_{ij}^2
       \le\frac{r\alpha s^2}{8}\,4^{-j}.
\tag{15}
\]

Start with the one level-zero cell. At each later level, process the
children of retained cells. Evaluate `Z_d(v)` and an exact integer
recourse witness at each processed cell's corners. Maintain the least
auxiliary value `U_j` evaluated so far and its witness. After finishing
all evaluations at the level, retain exactly those cells `C` satisfying

\[
 L(C)=\min_{v\text{ corner of }C}Z_d(v)-B_j\le U_j.
\tag{16}
\]

The coordinate-semiconcavity bound makes `L(C)` a valid lower bound
on `C`. A cell containing a global auxiliary minimizer always survives,
including equality cases. For
`L_j=min_(C retained)L(C)`, the exact inequalities are

\[
 L_j\le\min_A Z_d\le U_j,
 \qquad U_j-L_j\le B_j.
\tag{17}
\]

Every retained cell has a corner with auxiliary value at most
`min_A Z_d+2B_j`. The original witness stored with `U_j` has gap
at most `B_j` by (14). Discarded-cell lower bounds remain valid as the
incumbent improves; a certificate records them with the refinement tree.

For completeness, the finite-noise counting step uses no distributional
assumption about the adaptively selected cells. Fix a node of the
complete deterministic level grid. At every interior coordinate `i`,
being within `2B_j` of the global optimum requires beating both adjacent
grid nodes up to that tolerance. These two comparisons restrict `d_i`
to an interval of length at most

\[
 \alpha h_{ij}+4B_j/h_{ij}
 \le (1+2r)\alpha h_{ij}.
\tag{18}
\]

The intervals depend on `W` and the grid, not on the sampled noise.
An interval of length `ell` has probability at most
`ell/(2sigma_i)+1/M` on the grid (5). Independence multiplies these
probabilities across interior coordinates; a boundary coordinate costs
at most one. Summing over all grid nodes gives an expected number of
`2B_j`-near-optimal nodes at most

\[
 \prod_i\left[
 2+\frac{(1+2r)\alpha w_i}{2\sigma_i}
       +\frac{m_{ij}-1}{M}\right].
\tag{19}
\]

For every level `j<=J`, the fixed choice `M=2^J` guarantees
`m_ij<=M`. Hence (19) is at most `H_rat` in (6). A grid node belongs
to at most `2^r` cells. Every retained cell has a near-optimal corner,
so the expected number of retained cells is at most `2^r H_rat`.

Each retained parent has at most `2^r` children and each child has at
most `2^r` corners. The expected total number of exact recourse
evaluations through level `J`, even without caching shared corners, is
therefore at most

\[
 2^r+8^r H_{\rm rat}J.
\tag{20}
\]

This includes draws with many ties or poor conditioning. It does not
condition on successful optimization, require a growth bound, or
resample a difficult draw.

## 5. The original objective lattice gives exactness

Every base denominator divides `Q`. For integer `x`, the unary values
`G(x)` have denominator dividing `Q`, and the negative quadratic term
in (1) has denominator dividing `2Q^3`: one factor comes from `alpha`
and two from the entries of `T`. Also (5) implies

\[
 d^TTx
 =\sum_{i,j}
 \frac{\sigma_i(2K_i-(M-1))T_{ij}x_j}{M-1},
\]

whose denominator divides `Q^2(M-1)`. Thus every feasible original
objective value lies on the common lattice

\[
 \boxed{F_d(x)\in\frac{1}{D_0(M-1)}\mathbb Z
        \qquad(x\in X).}
\tag{21}
\]

This uses one common `M` across all noisy coordinates. Products of
unrelated sampling denominators are unnecessary.

At the predetermined terminal level `J=log_2 M`, (4) and (15) give

\[
 B_J\le\frac{r\alpha s^2}{8M^2}
       \le\frac{1}{8D_0M}
       <\frac{1}{D_0(M-1)}.
\tag{22}
\]

Let `x_inc` be the stored integer witness. Equations (14), (17), and
(22) give

\[
 0\le F_d(x_{\rm inc})-F_d^*\le B_J
       <\frac{1}{D_0(M-1)}.
\]

Both objective values belong to (21), so they must be equal. Return
`x_inc` and its exactly evaluated perturbed objective value.
The conclusion holds for every draw, and multiple original minimizers
are allowed.

The auxiliary function `Z_d`, its witnesses' joint values, and the
constant `C_d` may have denominators involving `(M-1)^2`. No lattice
claim about those values is used. Their only role is to certify the
original feasible gap in (14), where the same shift cancels. Imposing
an auxiliary-value lattice would create a false precision obstruction.

## 6. Bit complexity and the fixed noise law

The product defining `Q` has bit length at most the sum of the input
denominator bit lengths. Thus `log D_0=O(I)`. The row ranges and the
enlarged box have polynomial bit length. It follows that `J` itself is
bounded by a polynomial in `I`, and the binary encoding of `M=2^J`
has length `J+1=poly(I)`.

The sampled coefficients, all level-`j` grid points, and all arithmetic
used through `j=J` have polynomial bit length in `I+J`. Each original
integer witness has the input-bounded coordinate length. The exact
recourse method in Section 2 therefore has a uniform polynomial bit
bound per evaluation. Tree indices and grid addresses have length
`O(rJ)`; retaining an exceptionally large number of cells does not
increase the bit length of an individual arithmetic object beyond these
polynomial bounds. Multiplying (20) by the per-evaluation and bookkeeping
costs proves (6), after absorbing `J` and other polynomial factors into
`P(I)`.

There is no precision loop in this construction. Compute (3)--(4) from
the base input, sample (5) once, and run exactly through level `J`.
The same predetermined inequality `M>=r alpha s^2 D_0` makes the
finite-grid atom term bounded throughout the search and makes the final
original gap smaller than its lattice spacing.

The result does not claim the same expected count for arbitrary finer
search on an externally supplied fixed coarse noise grid. Nor does
it infer polynomial work merely from binary-encoded bounds: very large
row ranges relative to the noise appear explicitly in `H_rat`, since

\[
\frac{\alpha w_i}{\sigma_i}
=2+\frac{\alpha(u_i-\ell_i)}{\sigma_i}.
\tag{23}
\]

Long integer intervals do not always enlarge these numerical factors.
For a positive integer `N`, take `X_j={0,...,N}`, `g_j(x_j)=(x_j/N)^4`, and
`T=tildeT/N`, with rational `tildeT`, `alpha`, and the noise widths
fixed independently of `N`. The row ranges equal those of
`tildeT[0,1]^n`, so `H_rat` is independent of `N`. The additional input
length is only polynomial in `n`, `r`, and `log N`; the resulting
expected work has polynomial dependence on `log N` for fixed other
data. If `tildeT` is nonzero, the continuous polynomial extension has
negative curvature near zero, so this need not be a convex objective.
This illustrates the bound without claiming that this particular family
is otherwise hard.

## 7. Scope and easy special cases

The elementary recourse uses a product domain and separable convex
univariate terms. Coupled constraints on the integer coordinates are
outside this theorem. A small number of negative Hessian directions
alone does not supply the separable representation in (1).
Continuous coordinates also change exact recovery:
their quartic optima may be irrational and need not obey the lattice
(21). The
[certified approximate recourse note](approximate-convex-recourse.md)
handles such inner solves, but a mixed-domain exact theorem does not
follow from the present argument.

Binary problems already have a deterministic fixed-rank baseline.
On `{0,1}`, every unary quartic reduces to an affine coefficient, say
`c_j x_j` up to a constant. Project the cube to `(Tx,c^T x)` in
dimension at most `r+1`. This image is a zonotope, and the residual
objective is concave on it. An optimum therefore occurs at a zonotope
vertex, with a binary preimage. Fixed-dimensional enumeration has
`O(n^r)` such vertices. In rank one there is also a direct proof:
each inner binary decision changes at at most one rational threshold
in the auxiliary scalar. Sorting those thresholds leaves only
polynomially many explicit quadratic pieces to minimize.

More generally, explicitly listed integer labels give the lifted
polytopes

\[
 P_j=\operatorname{conv}\{(T_{\cdot j}t,g_j(t)):t\in X_j\}.
\]

Each summand is planar and has at most `|X_j|` vertices and edges.
The objective is a concave quadratic plus a linear term on their
Minkowski sum. Fixed-dimensional arrangement enumeration of the edge
directions is polynomial in the total explicit label count, and a
minimizing vertex supplies original labels. This bound may be
exponential in the binary encoding of long integer intervals.
These special cases must not be presented as new tractability
consequences. The theorem allows binary-encoded intervals without
enumerating their labels, with the numerical dependence in (6).

The proof gives an expected exact algorithm for the prescribed perturbed
objective. It does not assert an unconditioned worst-case polynomial
algorithm for low-rank integer nonlinear optimization, a method for
general MINLP, or publication priority.

## 8. Verification status

The objective lattice, the shared precision choice, the exact integer
recourse, the numerical parameter dependence, and the treatment of ties
were derived independently by two delegated reviewers. Both then checked
the completed text, including the normalized long-range family and the
deterministic baselines, and found no mathematical blocker. Their records
are the [independent review](../reviews/smoothed-integer-low-rank-review.md)
and the [adversarial review](../reviews/smoothed-integer-low-rank-adversary.md).
The parent researcher separately checked the full proof analytically;
that review did not run executable tests.

The targeted command actually run was

```text
python research-20261002/new-direction/check_smoothed_integer_low_rank.py
```

It passed 124 exact-rational discrete recourse comparisons against
exhaustive minimization and one search on `[-2^100,2^100]` with known
interior optimizer `2^80`. Another 756 rational-base objective values
satisfied the lattice bound. Seven cell-solver fixtures passed 73
prescribed draws, including 15 draws with multiple original minimizers.
They used 448 levels, 2,437 processed cells, and 8,434 corner calls;
the 246 original values enumerated for those draws also satisfied the
lattice.

Every processed-cell bound was checked against its exact minimum by
independently minimizing the finite quadratic wells on that cell.
Every terminal integer witness matched exhaustive original optimization.
The [checker](check_smoothed_integer_low_rank.py) includes signed
projection coefficients, unequal widths, fixed and zero rows, constant
projections, and the smallest allowed noise grid `M=2`. These deterministic
checks support the algebra and algorithm; they do not establish an
expected-runtime theorem by sampling. No project-wide checks, CI
inspection, or literature search were performed in this workstream.
