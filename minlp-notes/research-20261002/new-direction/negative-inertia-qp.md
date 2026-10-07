# Exact quadratic optimization with few negative directions and quadratic growth

Date: 2026-10-02. Status: a theorem and complete reduction that passed a
[fresh independent review](../reviews/negative-inertia-qp-review.md).
The proof combines rational spectral normalization,
convex quadratic optimization, and growth-controlled branch and bound.
These ingredients have substantial prior art; publication priority is not
established.
The reviewed [mixed-integer theorem](negative-inertia-miqp.md) adds integer
dimension as a parameter. This note develops its continuous special case
separately, where every inner solve is a continuous convex QP.

## Main result

Let

\[
 F(x)=\tfrac12x^TAx+b^Tx+c,\qquad X=\{x:Mx\le d\},
\]

where the data are rational, \(A\) is symmetric, and \(X\) is a
nonempty bounded polytope. Lower-dimensional polytopes are allowed. Let
\(k=n_-(A)\) be the negative inertia, counting multiplicities. Suppose
the global optimizer \(x^*\) is unique and

\[
 F(x)-F^*\ge g\|x-x^*\|^2\quad(x\in X),\qquad g>0.       \tag{1}
\]

Write \(\nu=\max\{0,-\lambda_{\min}(A)\}\) for the magnitude of
the negative curvature. There is an algorithm returning an exact rational
optimizer and optimum value in

\[
 f\bigl(k,\max\{1,\nu/g\}\bigr)(I+1)^K                 \tag{2}
\]

bit operations, where \(K\) is an absolute constant and \(I\) is the
rational input length. A feasible rational point and a
certified additive objective gap at most \(2^{-q}\) require

\[
 f_1\bigl(k,\max\{1,\nu/g\}\bigr)(I+q+1)^{K_1}.       \tag{3}
\]

The polynomial exponents do not depend on \(k\) or \(\nu/g\). The
algorithm does not need \(g\), \(\nu\), or a spectral bound as input.
Positive curvature affects the rational input and preprocessing precision,
but is not a separate numerical parameter in (2)--(3). Since
\(\nu\le H\) whenever \(H\ge\|A\|_2\), the earlier bounds in
\(k,\max\{1,H/g\}\) follow as weaker corollaries. No sparsity, treewidth,
variable-occurrence, strict-complementarity, or interior-minimum assumption
is made. For \(k=0\), one exact convex-QP solve suffices.

The theorem is conditional on the quantitative global growth in (1).
Qualitative uniqueness alone need not give a useful numerical parameter.
The mixed extension uses an existing exact convex-MIQP oracle with an
additional parameter for the number of integer variables; that parameter
cannot be dropped from the present argument.

The proof also gives a stronger projected version. Suppose a rational
decomposition

\[
 A=P-\alpha T^TT,\qquad P\succeq0,\qquad \alpha>0          \tag{4}
\]

is supplied, with \(T\) having \(r\) rows. It suffices that every
optimizer has the same image \(t^*\), and

\[
 F(x)-F^*\ge g_T\|Tx-t^*\|^2\quad(x\in X).             \tag{5}
\]

Then (2)--(3) hold with parameters \(r,\max\{1,\alpha/g_T\}\)
and the encoding length of (4). The original optimizer set can contain a
continuum. The algorithm returns one exact rational optimizer, and does
not need \(g_T\).

## Fixed-domain convex recourse

For a rational auxiliary vector \(a\in\mathbb R^r\), define

\[
 W(a)=\frac\alpha2\|a\|^2+
 \min_{x\in X}\left[\frac12x^TPx+b^Tx+c-\alpha a^TTx\right]. \tag{6}
\]

The inner feasible set is always \(X\); it does not depend on \(a\).
Its objective is convex. The exact rational convex-QP theorem therefore
returns both \(W(a)\) and an attaining rational point \(x_a\) in
polynomial bit time. This includes singular Hessians and lower-dimensional
feasible sets. The oracle premise and primary source are documented in
[the independent convex-modulator derivation](convex-modulator-qp.md).
An exact certificate can consist of the feasible point and nonnegative
polyhedral KKT multipliers satisfying stationarity and complementarity;
these rational conditions are directly checkable. Such multipliers can
also be recovered by rational linear programming after the primal solve.

Completing the square gives the central identity

\[
 W(a)=\min_{x\in X}\left[F(x)+\frac\alpha2\|a-Tx\|^2\right]. \tag{7}
\]

Consequently

\[
 W(a)\ge F^*,\qquad
 F(x_a)\le W(a),\qquad
 \min_a W(a)=F^*.                                      \tag{8}
\]

Every joint minimizer satisfies \(a=Tx\) and \(F(x)=F^*\).
Conversely, every original optimizer supplies such a joint minimizer.
In particular, the auxiliary optimum is unique whenever all original
optimizers have the same image under \(T\).

Compute each coordinate range of \(Tx\) over \(X\) by exact rational
linear programming, and let \(B_0\) be the product of those intervals.
It contains every minimizer of \(W\). Coordinates with constant range
can be fixed and removed. If all ranges are constant, one convex inner
solve at that common image gives an exact original optimizer by (7), and
no subdivision is needed. Evaluations elsewhere in this bounding box are
still well-defined: no membership test in the potentially non-box image
\(TX\) is needed.

Finally, \(W(a)-\alpha\|a\|^2/2\) is an infimum of affine
functions of \(a\), hence concave. Thus \(W\) has upper coordinate
curvature \(\alpha\), even when it is nonsmooth. This is why corner
rounding is valid here. Directly minimizing \(F\) on the changing
slices \(Tx=a\) need not have this upper-curvature property; the
convex-modulator note gives an explicit upward-kink counterexample.

## Exact transfer of quadratic growth

Under the projected assumption (5), the triangle inequality gives, for
every \(x\in X\),

\[
 \|a-t^*\|\le\|a-Tx\|+\|Tx-t^*\|.
\]

Minimizing the sum of the two squared terms in (7), or completing a
scalar square, gives

\[
 W(a)-F^*\ge g_W\|a-t^*\|^2,\qquad
 g_W=\frac{g_T\alpha}{2g_T+\alpha}.                     \tag{9}
\]

Under the full-vector assumption (1), put \(\beta=\|T\|_2\).
Now \(\|a-Tx^*\|\le\|a-Tx\|+\beta\|x-x^*\|\), so

\[
 g_W=\frac{g\alpha}{2g+\alpha\beta^2},\qquad
 \frac\alpha{g_W}=2+\frac{\alpha\beta^2}{g}.             \tag{10}
\]

These estimates hold on all of \(\mathbb R^r\), not only on \(TX\).
No differentiability of \(W\), smooth dependence of \(x_a\), or
uniqueness of the inner optimizer is required.

For the intrinsic theorem with \(k>0\), use the one-sided refinement of
[rational spectral normalization](spectral-normalization.md). It constructs
in polynomial bit time a positive rational \(\bar\nu\) and a rational
\(n\)-by-\(k\) matrix \(U\) with

\[
 \nu\le\bar\nu<2\nu,\qquad
 \|U\|_2\le1,\qquad A+2\bar\nu UU^T\succeq0.
\]

Set \(T=U^T\), \(\alpha=2\bar\nu\), and
\(P=A+2\bar\nu UU^T\). Then \(r=k\) and
\(\alpha/g_W<2+4\nu/g\).

The rational bound \(\bar\nu\) is found by starting from a rational
row-sum bound \(H\ge\|A\|_2\) and halving while
\(A+(\bar\nu/2)I\succeq0\). Exact rational PSD tests give the
factor-two guarantee. A polynomial-bit lower bound on nonzero eigenvalue
magnitudes bounds the number of halvings. The full bound \(H\) remains
in the Jacobi rotation precision, while the correction and its subspace
accuracy use \(\bar\nu\). The convex case \(k=0\) is handled before
halving. All preprocessing and the convex oracle operate on
polynomial-length rational data. The
normalization treats singular \(A\) by exactly removing its kernel;
an approximate negative eigenspace without this step is insufficient.

## The auxiliary branch-and-bound algorithm

Let \(s\) be the largest side length of the nondegenerate auxiliary
box. At level \(j\), use the nested isotropic lattice with spacing
\(h_j=s2^{-j}\), clipping its terminal intervals to \(B_0\).
At level zero there is one cell. Refine surviving cells along this lattice;
each has at most \(2^r\) children.

For a cell \(B\) with side lengths \(w_i\), evaluate (6) exactly at
its at most \(2^r\) corners and retain the corresponding witnesses.
Set

\[
 m_B=\min_{v\text{ corner of }B}W(v),\qquad
 L_B=m_B-\delta_B,\qquad
 \delta_B=\frac\alpha8\sum_i w_i^2.                    \tag{11}
\]

Independent unbiased corner rounding and the upper curvature prove
\(L_B\le\min_B W\). The original-feasible witness at the minimizing
corner has value at most \(m_B=L_B+\delta_B\).

Maintain the smallest original objective \(U\) among all witnesses.
Discard every cell with \(L_B\ge U\). If none remain, return the
incumbent as exact. Otherwise their least lower bound \(L\) and the
incumbent give

\[
 L\le F^*\le U,\qquad
 U-L\le\delta_j:=r\alpha h_j^2/8.                      \tag{12}
\]

The second inequality follows even when the best original witness has a
smaller value than its auxiliary evaluation: for the cell attaining \(L\),
\(U\le F(x_v)\le W(v)=L+\delta_B\). Discarded cells remain
irrelevant because the incumbent only decreases.

For completeness, if \(U>F^*\), a cell containing the auxiliary
optimizer survives and supplies \(U\le F^*+\delta_j\). If instead
\(U=F^*\), that bound already holds. Therefore every surviving cell
has a minimizing corner satisfying

\[
 W(v)=L_B+\delta_B<U+\delta_j\le F^*+2\delta_j.
\]

By growth, this corner lies within
\(h_j\sqrt{r\alpha/(4g_W)}\) of the unique auxiliary optimizer.
There are at most

\[
 2^r\bigl(\sqrt{r\kappa}+4\bigr)^r,\qquad
 \kappa=\alpha/g_W,                                    \tag{13}
\]

such cells. The extra factor covers cells sharing a corner; the constant
also covers clipped terminal intervals. This bound depends on the actual
growth constant, but pruning and stopping do not use it.

Through level \(J\), the number of convex-QP calls is at most
\(f_2(r,\kappa)(J+1)\), including child generation and all corner
evaluations. Corner coordinates have bit length polynomial in \(I+J\).
Since \(J=\operatorname{poly}(I)+O(q+\log(r+1))\) makes
\(\delta_J\le2^{-q}\),
the oracle's uniform polynomial bit bound proves (3) and its projected
version. This is ordinary growth-based pruning and lattice packing, not
a new branch-and-bound mechanism.

## Exact rational recovery without a supplied growth constant

A rational quadratic on a nonempty bounded rational polytope has a
polynomial-height rational optimizer. One proof chooses an optimizer in
a face of smallest dimension. At a relative-interior optimum the
restricted Hessian is PSD. If it had a null tangent direction, first-order
stationarity would make the quadratic constant along that direction until
a smaller face was reached. Hence its tangent Hessian is positive definite,
or the face is a vertex. Rational linear algebra and determinant bounds
then give the claimed height. The face need not be found or enumerated by
the algorithm. The detailed argument is in the convex-modulator note.
Concretely, take independent active input rows \(Ex=e\) defining its
affine hull. Positive definiteness on \(\ker E\) makes the KKT matrix
\(\left(\begin{smallmatrix}A&E^T\\E&0\end{smallmatrix}\right)\)
nonsingular. Cramer's rule applied to this matrix gives a uniform,
computable denominator bound over all choices of those input rows.

Thus the input determines polynomial-bit denominator bounds \(V\) for
\(F^*\) and \(R\) for every coordinate of the common optimal image
\(a^*=Tx^*\). A universal determinant bound suffices; these bounds do
not use \(g\). Once the certified interval (12) has width less than
\(1/(2V^2)\), bounded-denominator rational reconstruction isolates
\(F^*\) uniquely.

If the current incumbent has that exact value, return it. Otherwise
\(U>F^*\), so an optimal cell survives at every subsequent level.
The least auxiliary value among the corners evaluated so far, attained
at \(v_j\), therefore satisfies

\[
 W(v_j)-F^*\le\delta_j,\qquad
 \|v_j-a^*\|^2\le\delta_j/g_W.                         \tag{14}
\]

At every level try to reconstruct each coordinate of \(a^*\) as the
unique denominator-at-most-\(R\) rational in the radius
\(1/(4R^2)\) interval around the corresponding coordinate of \(v_j\).
There is at most one, since distinct such rationals differ by at least
\(1/R^2\). If a coordinate has no candidate, continue refining.

For a candidate \(a\), solve the convex inner problem (6) and accept
its rational witness only if its original objective equals the already
isolated \(F^*\). This test makes premature reconstruction harmless.
When \(a=a^*\), every inner optimizer is acceptable: (7) gives

\[
 F(x_a)+\frac\alpha2\|a^*-Tx_a\|^2=F^*,
\]

and both terms are bounded below by \(F^*\) and zero, respectively.
No further equality constraint \(Tx=a^*\) is needed.

After \(O(\operatorname{poly}(I)+\log\kappa)\) levels, (14) makes
the reconstruction succeed. The algorithm simply continues certified
refinement and these exact acceptance tests; it never guesses \(g\).
This proves the exact bounds (2). It returns an expanded rational vector
of polynomial bit length, not merely an optimum-value certificate.

## What is added, and what is already known

The Fenchel square completion and fixed-domain convex recourse are standard
identities. Spectral subdivision, convex underestimation, and spatial
branch and bound are also established tools. The independently derived
[convex-slab proof](convex-modulator-qp.md) reaches the same conditioned
conclusion with chord minorants on \(Tx\)-slabs. It is a useful separate
check on the mechanism, rather than a competing novelty claim.

Two close comparisons require different accuracy conventions:

- Del Pia's 2026 theorem covers rational mixed-integer QP with an
  objective bounded below over a rational linear polyhedron, for fixed
  integer dimension and negative inertia. On bounded polytopes its
  approximation is relative to the finite objective range, and its Turing
  bound is polynomial in \(1/\varepsilon\). On an unbounded polyhedron
  with infinite objective supremum that relative guarantee is vacuous,
  as the paper explicitly notes.
  Its rational Jacobi construction is directly relevant to preprocessing.
  [Primary preprint](https://arxiv.org/abs/2607.29386).
- Luo and coauthors' 2019 spectral branch-and-bound method gives an absolute
  additive \(\varepsilon\) guarantee for bounded QCQP with convex
  constraints. Its displayed subdivision bound scales as a product of
  \(1/\sqrt\varepsilon\) factors over the negative directions.
  It already uses a PSD-minus-low-rank decomposition and convex subproblems.
  [Author full text](https://peng.ie.uh.edu/wp-content/uploads/2018/01/QP2NE_Ver3-4.pdf).

The claim assessed here is the additional global-growth assumption's
explicit consequence: an input exponent independent of negative inertia,
logarithmic accuracy dependence, and exact rational recovery, with
conditioning measured against negative-curvature magnitude. These comparisons
do not establish that this combination is unpublished. The source audit is
separate from the mathematical review.

The result does not contradict one-negative-eigenvalue hardness. A global
growth constant can be extremely small, and its reciprocal enters the
parameter dependence. Nor does the theorem establish competitive runtime
for a practical QP solver. Its local solver is an exact polynomial-time
convex-QP algorithm; ordinary floating-point solver output alone is not the
oracle specified here.

## Verification

The fresh Astra review checked the lift, both exact growth-transfer
constants, independent original and auxiliary incumbents, pruning,
packing, rational heights, convex-oracle certificates, and exact recovery.
It found no blocker after the zero-dimensional and bit-length clarifications
recorded in the linked review. The slab and spectral notes record separate
reviews of those derivations.
The spectral review includes a fresh addendum approving the one-sided
\(\nu\) refinement: exact PSD halving, the revised subspace accuracy,
kernel handling, and polynomial bit bounds. Its additional eight rational
checks include a tiny negative eigenvalue beside a large positive one.

The reviewer's targeted command `python - <<'PY'` used exact fractions
on a lower-dimensional polytope with an indefinite original Hessian,
singular convex residual, and a continuum of original optimizers sharing
one nondyadic projection. It passed 38 corner evaluations and 12
retained-cell checks, rejected two premature reconstructed images, and
recovered the exact image at level four. A second case verified immediate
exact pruning when an original-feasible witness is already optimal although
its queried auxiliary point is not. Full formulas and check scope are in
the review record.

The reusable [targeted checker](check_negative_inertia_qp.py) was run with

```text
python research-20261002/new-direction/check_negative_inertia_qp.py
```

It passed five fixtures and ten actual auxiliary branch-and-bound runs,
including nonsmooth recourse, inner ties, auxiliary points outside \(TX\),
clipped lattice cells, and the singular and nonunique cases above. It made
416 distinct auxiliary evaluations, generated 428 cells, rejected four
premature image reconstructions, and attained all requested approximation
gaps of \(1/4096\). Its independent closed-form checks agree with the
small active-face enumeration oracle. The checker uses an exponential
diagnostic oracle and fixture-supplied denominator bounds; it does not
implement spectral preprocessing or the production polynomial convex
solver and universal height-bound routines.

These checks are not a full implementation or performance benchmark of
the general algorithm. No project-wide verification or CI inspection was
performed. Mathematical review and the source comparison remain separate.
