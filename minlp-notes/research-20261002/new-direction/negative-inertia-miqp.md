# Exact mixed-integer QP with few integer and negative directions

Date: 2026-10-02. Status: a mixed-domain extension of the
[continuous Fenchel theorem](negative-inertia-qp.md) that passed a
[fresh independent review](../reviews/negative-inertia-miqp-review.md).
The exact convex mixed-integer oracle is an existing theorem.
No publication-priority or practical-performance claim is made.

## Result

Let \(\mathcal P=\{x:Mx\le d\}\) be a nonempty bounded rational
polytope, possibly lower-dimensional, and let

\[
 X=\mathcal P\cap(\mathbb Z^m\times\mathbb R^{n-m}),
 \qquad F(x)=\tfrac12x^TAx+b^Tx+c,
\]

with rational data and symmetric \(A\). Mixed feasibility can be checked
as part of the algorithm. Suppose \(X\ne\varnothing\), its global
optimizer \(x^*\) is unique, and

\[
 F(x)-F^*\ge g\|x-x^*\|^2\quad(x\in X),\qquad g>0.    \tag{1}
\]

Write \(k=n_-(A)\) and
\(\nu=\max\{0,-\lambda_{\min}(A)\}\). There are deterministic
algorithms with the following bounds:

- An exact rational optimizer and optimum value require
  \(f(m,k,\max\{1,\nu/g\})(I+1)^C\) bit operations.
- An original mixed-feasible rational point and certified additive gap at
  most \(2^{-q}\) require
  \(f_1(m,k,\max\{1,\nu/g\})(I+q+1)^{C_1}\) bit operations.

Here \(I\) is the input length, and the polynomial exponents are absolute.
The algorithm needs neither \(g\) nor a spectral bound as input. Integer
interval cardinalities are not enumerated. For \(k=0\), the existing
exact convex-MIQP oracle alone solves the problem, without growth. For
\(m=0\), this is the continuous theorem.

A projected version allows nonunique original optima. Given a rational
decomposition

\[
 A=P-\alpha T^TT,\quad P\succeq0,\quad\alpha>0,
 \qquad T\in\mathbb Q^{r\times n},
\]

suppose every original optimizer has the same image \(t^*\), and

\[
 F(x)-F^*\ge g_T\|Tx-t^*\|^2\quad(x\in X).             \tag{2}
\]

Then the parameters are \(m,r,\max\{1,\alpha/g_T\}\), with the
decomposition included in the input. The original optimal set may contain a
continuum. The conclusion returns one exact rational optimizer, not all of
them. The useful growth constant remains a quantitative assumption.

## The exact mixed convex oracle

Del Pia's Theorem 3 accurately solves rational mixed-integer convex
quadratic programming in fixed-parameter time with the number of integer
variables as parameter. The paper defines accurate solution to include
feasibility, boundedness, and the exact optimum together with an attaining
point. The number of continuous variables is unrestricted, and its
dimension-reduction results cover lower-dimensional feasible regions.
[Primary paper](https://arxiv.org/abs/2311.00099),
[local source record](../../literature/papers/pia2025-convex-quadratic-sets-and-the/paper.md).

In particular, for rational \(a\), the oracle computes

\[
 W(a)=\frac\alpha2\|a\|^2+
 \min_{x\in X}\left[\frac12x^TPx+b^Tx+c-\alpha a^TTx\right] \tag{3}
\]

and an attaining mixed-feasible rational point \(x_a\), in
\(f_0(m)\operatorname{poly}(I+\operatorname{size}(a))\) time.
The Hessian is \(P\succeq0\), and the integer count stays \(m\):
the rational parameter \(a\) is fixed in this call. The feasible set
never changes with \(a\), and integrality is retained exactly.

For a uniformly short witness, fix the returned optimal integer tuple and
solve the remaining continuous convex QP exactly. Bounds from the original
bounded polytope make this tuple polynomial in encoding length; the
continuous solve then supplies a polynomial-height rational witness. This
optional step preserves the mixed optimum of the inner problem.

Continuous KKT conditions alone do **not** certify this oracle's global
mixed optimum. They certify only an appropriate continuous subproblem.
The lower-bound contract here relies on the exact mixed-integer algorithm;
its arithmetic computation can be recorded or rerun within the same FPT
bound. No ordinary polynomial-size KKT certificate for arbitrary mixed
optimization is asserted.

## Why the auxiliary proof survives integrality

Square completion still gives

\[
 W(a)=\min_{x\in X}\left[F(x)+\frac\alpha2\|a-Tx\|^2\right]. \tag{4}
\]

This identity, and every following geometric step, does not require a
convex feasible set. Boundedness makes \(X\) a finite union of compact
continuous slices, so the displayed minima are attained. Moreover,
\(W(a)-\alpha\|a\|^2/2\) is still an infimum of affine functions.
It is concave, giving upper coordinate curvature \(\alpha\).

Every oracle witness obeys \(F(x_a)\le W(a)\), and auxiliary
minimizers are exactly the images of original global optimizers. The
growth constants from the continuous theorem are unchanged:

\[
 g_W=\frac{g\alpha}{2g+\alpha\|T\|_2^2}
 \quad\hbox{under (1)},\qquad
 g_W=\frac{g_T\alpha}{2g_T+\alpha}
 \quad\hbox{under (2)}.                                 \tag{5}
\]

Use linear programming over the continuous polytope \(\mathcal P\)
to bound each coordinate of \(Tx\). These ranges may be larger than
the mixed image, but their product contains every auxiliary optimizer.
Evaluating (3) outside the image is harmless. If every range is constant,
one inner solve at that image is exact. Mixed feasibility is first checked
by the convex oracle with constant objective.

Now apply exactly the auxiliary corner branch and bound of the continuous
theorem. A cell with widths \(w_i\) has valid lower bound

\[
 L_B=\min_{v\text{ corner}}W(v)
           -\frac\alpha8\sum_iw_i^2.
\]

The best original mixed-feasible value supplies the upper bound. At mesh
\(h_j\), their certified gap is at most
\(\delta_j=r\alpha h_j^2/8\). Growth confines a minimizing corner
of every retained cell to a ball of radius
\(h_j\sqrt{r\alpha/(4g_W)}\) around the common auxiliary optimum.
Thus the number of retained cells per level remains a function only of
\(r,\alpha/g_W\); it does not depend on the number of integer slices.
The total work is the continuous theorem's number of calls multiplied by
the oracle factor \(f_0(m)\), with an absolute polynomial bit exponent.

For the intrinsic bound, rational spectral normalization computes
\(\nu\le\bar\nu<2\nu\), \(\|T\|_2\le1\), and
\(A=P-2\bar\nu T^TT\), using \(k\) rows. Hence
\(\alpha/g_W<2+4\nu/g\). This preprocessing is a matrix operation
and is unaffected by which coordinates are integer. The case \(k=0\)
is handled separately.

## Uniform rational heights and exact recovery

Boundedness of \(\mathcal P\) is used substantively. Linear-programming
height bounds give a uniform polynomial bound on the encoding length of
every integer coordinate appearing in any mixed-feasible point. There may
be exponentially many integer tuples; their numerical count is neither
bounded polynomially nor enumerated.

Choose an original global optimizer and fix its integer tuple. Its
continuous slice is a compact rational polytope with uniformly
polynomial-length data. The quadratic restricted to this slice need not
be convex. Nevertheless, choose an optimal point in a face of smallest
dimension. Relative-interior local optimality makes its tangent Hessian
positive semidefinite. It is then positive definite, unless the face is a
vertex: a null tangent direction would preserve the objective until a
smaller face was reached. The corresponding rational nonsingular KKT
system gives a polynomial-height rational optimizer for this slice.

This proves that the original mixed QP has some polynomial-height
rational global optimizer and optimum value. Under common-image uniqueness,
its image is the required \(t^*\). Uniform determinant bounds therefore
give known polynomial-bit denominator bounds \(V\) for \(F^*\) and
\(R\) for every coordinate of \(t^*\), without identifying or
enumerating the optimal integer tuple.

The exact stopping rule is now identical to the continuous theorem.
Isolate \(F^*\) from the certified interval; return an incumbent already
attaining it. Otherwise maintain the least auxiliary corner value
separately from the best original objective. Try bounded-denominator
reconstruction of its auxiliary coordinates. Accept a candidate only if
an attaining **mixed-feasible** oracle witness has original objective
equal to the isolated \(F^*\). At the true image every inner minimizer
works, because (4) is the sum of two nonnegative optimality gaps.
Quantitative growth guarantees successful reconstruction after
\(\operatorname{poly}(I)+O(\log(\alpha/g_W))\) levels; the algorithm
does not need that constant to recognize success.

No argument here infers a uniform useful growth constant from common-image
uniqueness. Boundedness gives finitely many integer slices, which is enough
for the height argument. Nearly tied distant integer assignments can still
make a global or projected growth constant extremely small. An unbounded
integer domain is outside this theorem and cannot be substituted silently.

## Comparison and verification

This result combines the exact convex-MIQP FPT oracle with the conditioned
auxiliary search. It does not replace that oracle or make arbitrary
integer dimension tractable. The
[mode-wise growth barrier](modewise-growth-barrier.md) explains why good
conditioning inside each integer assignment alone is insufficient: (1) or
(2) must compare against the common global optimum across assignments.

Del Pia's 2026 negative-inertia approximation theorem is a direct comparator,
but uses objective-range-relative error and polynomial dependence on
\(1/\varepsilon\). The proposed additional conclusion is the explicit
growth-conditioned FPT dependence, logarithmic additive accuracy, and exact
rational recovery. The [source comparison](../prior-art/convex-recourse-prior.md)
separates these guarantees from the established spectral and convex-oracle
tools. No checked-source comparison establishes publication priority.

A fresh Astra review checked the primary theorem's exact FPT oracle
contract, the finite-slice height argument, short-witness polishing, exact
recovery, and the distinction between mixed-oracle traces and continuous
KKT certificates. It found no remaining mathematical blocker.

Its targeted `python - <<'PY'` check used exact fractions on a mixed fixture
whose optimal inner integer assignment changes with the auxiliary query.
It passed 242 original growth checks, 399 rounding and lift-growth checks,
11 distinct corner evaluations, and 12 retained-cell checks. Two premature
image reconstructions were rejected before exact recovery at level four.
The fixture includes a lower-dimensional version with a continuum of
original optimizers sharing one image. At one query, replacing the mixed
oracle by its continuous relaxation would give a lower bound below the true
mixed optimum; the check explicitly verifies this distinction.

The review records the full formulas and commands. Its small mixed oracle
enumerates the two allowed integer assignments; this tests the mechanism,
not the cited FPT oracle's implementation. The continuous auxiliary checker
separately tests the unchanged outer algorithm. No project-wide verification
or CI inspection was performed, and no performance benchmark is claimed.
