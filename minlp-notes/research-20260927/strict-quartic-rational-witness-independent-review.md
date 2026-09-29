# Fresh review of the rational witness lower bound

Date: 2026-09-28. Reviewer: `/root/unconstrained_posslp_adversary`.
Status: the complete proof in
[the standalone witness note](strict-convex-quartic-rational-witness-lower-bound.md)
passes this independent review. The reviewed version had SHA256
`c6928d09538c2c729f7a4fe3e15348d392a69274c95ee5c23d6896419d9d8a63`.

I did not develop this construction. I previously reviewed the
different cubic perturbation used for PosSLP hardness. Before reading
this note, I independently reconstructed the quadratic perturbation,
its localization bound, and the denominator argument from the task
description. I then read the complete frozen note and checked its
literal constants and quantified claims. The substantially deeper
[signed-root realization](signed-odd-root-circuit-quartic.md) is used
as a previously reviewed theorem, with its input promises checked here.

No correctness issue was found. The output-size obstruction is
unconditional for ordinary binary rational coordinates. Publication
priority, and superiority over all prior restricted convex examples,
remain unestablished.

## The root circuit and normalization

The definitions \(M=1000^{k+3}\), \(\delta_0=M^{-1}\), and
\(\delta_i=(1+3\delta_{i-1}^2)^{1/3}-1\) give
\(0<\delta_k\le M^{-2^k}\). This upper bound follows from
monotonicity of cubing and \((1+t)^3\ge1+3t\) for \(t\ge0\);
it does not require approximation of \(\delta_k\).

Every output root \(\xi_i=1+\delta_i\) stays near one.
The radicands are a rational constant for the first gate and
\(3\xi_{i-1}^2-6\xi_{i-1}+4\) thereafter. Thus they use
only the earlier root and its permitted retained square. The direct
signed interval width bound \(12w+3w^2\le13w\) and the
factor-1000 increase between successive box widths prove the required
interval inclusion. No cancellation between dependent interval terms
is assumed. The first constant radicand also lies in its box by the
same elementary cubic endpoint estimates.

There are exactly \(k\) boxes, with
\(w_k=1000^{-3}=10^{-9}\). The normalization is therefore the
fixed rational

\[
                 \kappa=\frac{10^9}{10^9-1}<2.
\]

The signed-root theorem uses two coordinates per cubic-root gate, so
the resulting dimension is exactly \(n=2k\). Its polynomial-time
and polynomial-size guarantees apply because the coefficient and box
encodings have polynomial total size. There is no hidden request to
print a rational approximation of exponentially small width.

## The perturbation and the entire sublevel set

Let \(F\) and its full rational positive definite Hessian Gram
\(M_0\) be the baseline. The note's determinant bound

\[
 \mu=\frac{\det M_0}{(\operatorname{tr}M_0)^{h-1}}
 \le\lambda_{\min}(M_0)
\]

is valid because every eigenvalue is at most the trace. The negative
quadratic \(-u^2\), where \(u=X_{k,1}-\kappa\), has
Hessian Gram \(-2ee^{\mathsf T}\) in the constant-direction
block. Thus \(\lambda=\lceil3/\mu\rceil\) gives a full
rational Hessian Gram at least the identity for \(G=\lambda F-u^2\).
All matrix dimensions and rational bit lengths remain polynomial in
\(k\). Subtracting the quadratic does not change the quartic leading
part.

At the baseline zero \(p\), let \(u_*=\kappa\delta_k>0\).
Then \(G(p)=-u_*^2\) and \(\|\nabla G(p)\|=2u_*\).
The first formula proves strict feasibility, hence a nonempty open
subset of the feasible set and existence of rational feasible points.
Strong convexity proves coercivity and compactness of the closed zero
sublevel set. For two distinct feasible points, its strong-convexity
inequality makes every interior segment point strictly feasible,
which also proves the stated strict convexity of the body.

For every feasible \(X\), including boundary points, write
\(r=\|X-p\|\). The exact quadratic lower bound gives

\[
 0\ge G(X)\ge-u_*^2-2u_*r+\tfrac12r^2,
 \qquad
 r\le(2+\sqrt6)u_*<5\kappa M^{-2^k}.
\]

This argument does not assume that \(p\) remains the minimizer of
\(G\). The normalized baseline coordinates are bounded by constants,
and the displayed radius is below one. The note's coordinate bounds
\((-1,5)\), and absolute value below three for the first feasible
coordinate, are consequently valid for every \(k\ge1\).

## The denominator bound

The first normalized coordinate is \(\alpha=\kappa\xi_1\),
with

\[
 \alpha^3=\frac{A}{B},\qquad
 A=M(M^2+3),\quad B=(M-1000^k)^3<M^3.
\]

The irrationality proof is correct. Since \(M=10^{3(k+3)}\),
the number \(M^{2/3}\) is an integer. The integer \(M^2+3\)
lies strictly between \((M^{2/3})^3\) and
\((M^{2/3}+1)^3\). A rational cube root of an integer is an
integer, so \(\xi_1\) is irrational. Multiplication by the
nonzero rational \(\kappa\) preserves irrationality. Its cubic
equation then also establishes degree exactly three.

For a rational feasible first coordinate \(a/b\), with \(b>0\),
the integer \(Ba^3-Ab^3\) is nonzero. Hence

\[
 \frac1{b^3}
 \le\left|B(a/b)^3-A\right|
 \le27B\,|a/b-\alpha|
 <135B\kappa M^{-2^k}
 <270M^{3-2^k}.
\]

The factor 27 follows by factoring the difference of cubes and using
the absolute-value bound three for both arguments. Neither coprimality
of \(A,B\) nor irreducibility of \(BT^3-A\) as a primitive
integer polynomial is needed for the integer numerator bound. The
strict inequality follows from \(2+\sqrt6<5\).
Taking logarithms gives exactly the author's lower bound

\[
 \log_2b>
 \frac{(2^k-3)(k+3)\log_2 1000-\log_2 270}{3}.
\]

This is \(\Omega(k2^k)=\Omega(n2^{n/2})\) asymptotically.
The theorem is stated for all \(k\ge1\); a weak or negative lower
bound at small \(k\) does not affect its validity. Since the entire
dense quartic and certificate have size bounded by a polynomial in
\(k\), this witness size is superpolynomial in their input size.
The note correctly avoids claiming exponential size in the total
dense input length.

## Source comparison and verification scope

I examined the local primary text of Khachiyan and Porkolab,
[Integer Optimization on Convex Semialgebraic Sets](../literature/papers/khachiyan2000-integer-optimization-on-convex-semialgebraic/fulltext.md),
Section 2.3, Proposition 2.5 and Corollary 2.6. Proposition 2.5,
restating Basu--Pollack--Roy results, bounds the logarithm of an
inscribed box's inverse radius by \(LD^{O(n)}\) for a nonempty
strict polynomial system of degree \(D\) and coefficient length
\(L\). Rounding inside that box gives rational points of
corresponding exponential size. The new lower bound is compatible
with this general upper bound and shows that the listed strong
curvature restrictions do not imply polynomial rational witnesses.

Laurent and Rendl's author-hosted
[Semidefinite Programming and Integer Programming](https://optimization-online.org/wp-content/uploads/2002/12/585.pdf),
Section 2.3, records an SDP chain forcing
\(x_i\ge2^{2^{i-1}}\) and therefore exponential rational
witness length. That example uses large coordinates. It establishes
clear prior for the general phenomenon and does not by itself give
the compact single-quartic construction reviewed here. This limited
comparison does not establish priority for the present restrictions.

This review is a proof reconstruction. I did not run the author's
finite-example checker, did not implement the full signed-root
construction, and did not formalize this argument in Lean. The scalar
inequalities above were checked exactly as mathematical identities
and inequalities, not inferred from numerical experiments. No
project-wide verification or CI inspection was performed.

The consequence concerns explicit rational coordinate witnesses only.
It neither rules out small certificates in other representations nor
proves nonmembership in NP. Strict feasibility supplies no quantitative
Slater radius; the small radius is exactly what forces the precision
lower bound. The statement also gives no obstruction to approximation
with a separately specified error tolerance.
