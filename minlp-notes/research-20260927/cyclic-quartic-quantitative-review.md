# Quantitative audit of the cyclic quartic construction

Date: 2026-09-28. Scope: the full construction in
[Strongly convex integer quartics with exponentially large zero degree](cyclic-quartic-exponential-degree.md).
The argument was rederived independently before comparison with the draft.
The reviewer subsequently supplied bounds and interpretation suggestions,
so this is a contributor audit, not a review by a noncontributing reader.
A separate [fresh review](cyclic-quartic-fresh-review.md) has now completed
and found no blocking defect.

**Finding.** No gap was found in the cyclic identities, degree claim,
quantitative convexification, rational certificate construction, or bit
bounds. The construction attains degree asymptotic to \((2/3)2^n\)
with polynomial encoding size. Its output consequences depend on the
specified representation: algebraic degree alone does not exclude short
rational-power or arithmetic-circuit descriptions.

## 1. Exact arithmetic and the exposing identity

Write \(m=n+1\), \(\sigma=(-1)^m\),
\(d=(2^m-\sigma)/3\), and \(s_i=((-2)^i-1)/3\).
The numerator in the definition of \(d\) is an odd positive multiple
of three, so \(d\) is an odd positive integer. For nonwrapping indices,
the sequence \(s_i\) satisfies
\(2s_i-s_{i+1}-s_{i+2}=0\). The last two cyclic differences are
\(\sigma d\) and \(-\sigma d\). This verifies the signs of the
two exceptional rational coefficients in the quadratic system.

The inequalities \(|s_i|<d\) imply the strict bounds
\(1/2<p_i<2\) and \(1/4<p_i^{-2}<4\). With
\(X_i=x_i/p_i\) and \(X_0=1\), weighted summation gives

\[
 \sum_i p_i^{-2}q_i(x)
 =\sum_i X_i^2-\sum_i X_{i+1}X_{i+2}
 =\frac12\sum_i(X_i-X_{i+1})^2.
\]

The second equality is a cyclic reindexing, including \(m=3\).
Every common real zero of the rational quadratics therefore has all
\(X_i=1\). This proves uniqueness without invoking a toric-root count
or a convexity theorem. The factor \(x_0=1\) is essential.

Eisenstein's criterion gives degree \(d\) for the positive root
\(a\) of \(T^d-2\). The coordinate \(p_1=a^{-1}\) alone
generates its field, while every other coordinate is an integer power
of \(a\). Thus the joint degree is exactly \(d\), not merely a
lower bound inferred from the determinant of a quadratic system.

## 2. Independent norm estimates

Let \(h_0=0\) and \(h_i=u_i/p_i\). A slightly stronger form of
the draft's anchored estimate follows directly from Cauchy--Schwarz:

\[
 \sum_{j=1}^{n}h_j^2
 \le\frac{n(n+1)}2\sum_{i=0}^{m-1}(h_i-h_{i+1})^2
 \le n^2\sum_{i=0}^{m-1}(h_i-h_{i+1})^2.
\]

The last inequality uses \(n\ge1\). Since
\(\|h\|\ge\|u\|/2\) and \(\|h\|\le2\|u\|\),
the exposing quadratic's matrix satisfies

\[
                 \frac1{8n^2}I\preceq H_*\preceq8I.
\]

For the residual Jacobian, the exact scaling is

\[
 J=\operatorname{diag}(p_i^2)(2I-S-S^2)E D_p^{-1}.
\]

The factorization \((2I+S)(I-S)\) is in the stated order, and
\(S\) is an isometry. Therefore
\(\|(2I+S)v\|\ge\|v\|\). Combining this with the anchored
estimate and the diagonal lower bounds \(p_i^2>1/4\) gives
\(\|Ju\|\ge\|u\|/(8n)\). No lower bound on separation among
the complex conjugates is used.

The residual Hessian matrices also admit the claimed uniform bound.
Because the three cyclic indices are distinct, each homogeneous
quadratic part has a diagonal block \(1\), an off-diagonal block
with entries of magnitude at most \(1\), or a subset of those blocks.
Thus \(\|T_i\|\le1\). Every residual gradient has at most three
entries of magnitude below four, giving \(\|b_i\|<7<8\).

## 3. Rounding, regularization, and the two dimension counts

The chosen values

\[
 M=10^6n^5,\quad \varepsilon=M^{-2},\quad
 Q=32mM^2,\quad \mu=1/(16n^2),\quad L=9
\]

give \(\|\ell\|\le\varepsilon/4\),
\(\|H-H_*\|\le\varepsilon/32\), and
\(\mu I\preceq H\preceq LI\). Rounding remains in the rational
linear span of quadratics vanishing at the exact point, so it never
perturbs the prescribed zero.

There are \(m=n+1\) residuals but only \(n\) variables. Their roles
in the imported SOS argument differ:

- The quartic Gram block loses at most \(4\varepsilon m I\),
  since there are \(m\) possibly indefinite \(T_i\).
- The cubic block's Frobenius estimate has the dimension factor
  \(6\sqrt n\), and its coefficient sum is bounded by
  \(D=L+8m=8n+17\le17n\).

The draft correctly uses these separate counts. In particular,

\[
 \varepsilon\le\frac{\mu^2}{2m},\qquad
 \frac{\nu^2\mu^2}{36nD^2}
 \ge\frac1{170459136n^9}
 \ge\frac1{10^{12}n^{10}}=\varepsilon.
\]

The first inequality is immediate after multiplying positive denominators;
the last holds for every \(n\ge2\), with considerable slack. These
bounds establish both ordinary strong convexity and a positive definite
Hessian Gram matrix. The proof retains the negative contribution of
\((u^{\mathsf T}T_i u)^2\) when \(T_i\) is indefinite.

The integer scaling is exact:

\[
 4Q^2\left(G^2+M^{-2}\sum_iq_i^2\right)
   =\left(2\sum_i z_iq_i\right)^2
      +\sum_i\left((2Q/M)q_i\right)^2.
\]

Both square factors are integral because \(2q_i\) is integral and
\(2Q/M=64mM\) is even. Multiplying the continuous curvature bound
by \(4Q^2\) gives
\(96m^2M^2/n^2\ge1\), as asserted.

The rational Hessian certificate uses the existing proved affine
coefficient projection. Its positive gap has an inverse-polynomial
lower bound, the translation point has norm at most \(2\sqrt n\),
and all translated Gram entries are bounded-degree polynomial expressions
in bounded coordinates and polynomial-sized rational data. Therefore
inverse-polynomial coordinate accuracy suffices. The coefficient projection
is onto rational equations and preserves the positive gap. This does not
assume an exact semidefinite-feasibility algorithm.

## 4. The construction really avoids exponential-degree root algorithms

Using a generic dense algebraic-number routine on \(T^d-2\) would not
justify polynomial time in \(n\). The draft instead computes
\(p_i\) and \(w_i\) through logarithm and exponential series on
bounded intervals. Its displayed logarithm tail estimate follows from
the geometric tail of the \(\operatorname{arctanh}(1/3)\) series.
For the exponential series and \(K\ge2\), the ratio of successive
tail terms is at most \(2/(K+2)\le1/2\), so the claimed
\(2^{K+2}/(K+1)!\) bound is valid.

The input rational multiplier \(s_i/d\) has \(O(n)\) bits, and
only \(O(\log Q)\) precision and series terms are needed. Exact
rational evaluation therefore has polynomial bit cost. Rounding an
approximation within \(1/(4Q)\), rather than deciding exact nearest
integer comparisons for \(Qw_i\), avoids a hidden root-separation
requirement at rounding boundaries.

The numerators \(z_i\) have magnitude at most \(4Q+1\), and
\(M,Q\) are fixed powers of \(n\) times constants. Hence the
integer square factors have \(O(\log(n+1))\)-bit coefficients.
The first factor has \(O(n)\) monomials, and the remaining factors
have two each. Squaring and adding yields \(O(n^2)\) monomials with
polynomially bounded coefficients. Expansion into the specified explicit
input format remains polynomial time.

## 5. Output interpretation and prior boundaries

The initial first-coordinate polynomial \(2T^d-1\) is sparse.
After rational translation, its primitive irreducible polynomial becomes
\(2(T-1)^d-1\). Irreducibility is preserved by translation; its
constant term is \(-3\) and every positive-degree coefficient is a
nonzero signed binomial coefficient times two. Ordinary minimal-polynomial
monomial lists therefore require \(d+1\) terms for that coordinate.
Translation expands each degree-four input monomial into at most five
terms, so it does not spoil the short input bound.

This conclusion concerns minimal-polynomial coefficient lists. A shifted
basis, a circuit, a rational-power expression, or a suitable other exact
format can remain short. No lower bound for exact decision follows.

The Jacobsthal determinant and the grounded cycle energy are established
prior ingredients. Their sources and exact conventions are examined in
[the grounded-energy prior audit](cyclic-grounded-energy-prior.md).
The potential contribution is the rational arithmetic construction and its
quantitative convexification, not a new spanning-tree enumeration formula.
Publication priority for that combination remains unestablished.

The separate rational-SOS upper-bound study shows why the construction's
exponential base is significant, but is not required by this lower-bound
proof. Neither that upper bound nor the construction automatically extends
to arbitrary nonnegative quartics without their respective assumptions.

## 6. Added conditioning and ellipsoid corollaries

The later local conditioning statement follows from the exact Hessian
\(2\ell\ell^{\mathsf T}+2\varepsilon J^{\mathsf T}J\) at the
zero. The lower bound \(2\varepsilon\nu^2\), the gradient bound,
and \(m\) residual rows give condition number
\((1+64m)/\nu^2=O(n^3)\). This is a bound at the minimizer;
it is not a uniform condition-number bound over all points.

The added ellipsoid construction was checked independently as well.
For \(R_i=G+\tau q_i\), \(\tau=\mu/2\), the quadratic matrix
is at least \((\mu/2)I\). With \(c_i=z_i/Q\),
\(C=\sum_i c_i\), and \(W=\sum_iw_i\), the proposed weights

\[
 \lambda_i=\tau^{-1}\left(w_i-\frac{Wc_i}{\tau+C}\right)
\]

satisfy \(\sum_i\lambda_i=W/(\tau+C)\) and
\(\sum_i\lambda_iR_i=G_*\). Their positivity follows from
\(\tau(\tau+C)\lambda_i\ge\tau/4-8m/Q>0\).
Consequently the common weak sublevel is exactly the prescribed point.
Each individual positive definite rational quadratic has a rational
minimizer; that minimizer differs from the irrational point at value zero,
so its minimum is strictly negative. Thus every individual sublevel is a
full-dimensional bounded ellipsoid, despite the singleton intersection.
The common denominator \(64n^2Q\) has polynomial magnitude and makes
all ellipsoid rows integral without changing their sublevels.

## 7. Verification scope

This audit is based on exact derivations of the identities and estimates,
and direct reading of the complete draft and imported Gram proof. It does
not treat numerical Hessian sampling as a proof. The author and root have
separate exact checks; their commands are recorded in their own notes.
A fresh noncontributing reviewer checked the complete assembly, including
the later conditioning and ellipsoid corollaries, and found no defect.
That review records a distinct exact rational Hessian Gram construction in
dimension two. The subsequent reduction in square count is audited in
[a separate refinement note](cyclic-sos-compression-review.md).
No project-wide build, CI inspection, or new Lean verification was run for
this construction.
