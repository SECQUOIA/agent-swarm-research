# Independent review of the quadratic-denominator construction

Date: 2026-09-28. The
[author's note](rational-tower-quadratic-denominator.md) was read in
full at SHA256
`70f82791edec87b1f9091b0d9ec804bd9b213c6c5449e283500c0b68c794a0c6`.
This review independently checks the new algebra, quantitative bounds,
rational construction, and its use of the existing tower theorem.
It does not establish publication priority or repeat a full review
of that earlier theorem.

The construction is correct for the refined tower family, using
the enlarged scale in (12). Its quadratic common denominator is
everywhere positive and has minimum possible degree over
\(\mathbb Q\). The general multiplier lemma also follows from the
stated span assumptions. No assumption of linear independence for
the polynomial lists is missing.

The one wording correction requested in Section 5 is resolved: sufficiency of
the coefficient-field characterization uses a rational positive
Hessian Gram, so the scaling should be said to meet the original
Hessian-Gram threshold. Strong convexity alone is not the hypothesis
used by that proof. The scale actually chosen in (12) meets the
required threshold, so this does not affect the construction. The
corrected paragraph was reread at file SHA256
`1a8d8750080f5c6c8c58ae3e8ee97a456dcf0b25b7c3c5e76a1a45371016723c`.

## Identity and strict positivity

With the author's notation,
\(a^{\mathsf T}w=R\), \(U^{\mathsf T}w=XG\), and \(b=XR\).
Consequently the quadratic form of the proposed zero matrix is

\[
cR^2+R\ell^{\mathsf T}XR-(XG)^{\mathsf T}T(XR)
                    +R^2X^{\mathsf T}HX
=R^2G-GR(X^{\mathsf T}TX)=0.
\]

This verifies both the minus sign in \(C\) and its factor
\(1/2\). Homogeneity of \(R=X^{\mathsf T}TX\) is used here;
an arbitrary inhomogeneous relation would need a different identity.
The tower supplies the exact required relation
\(R=xr_{k,2}-yr_{k,1}\).

Set \(A=I+\varepsilon caa^{\mathsf T}\). The prescribed bound
on \(\varepsilon\) gives

\[
A\succeq
\left(1-\frac{|c|\|a\|^2}{2(1+|c|\|a\|^2)}\right)I
\succeq\tfrac12 I.
\]

Hence \(\|A^{-1}\|\leq2\). With
\(\eta=\det H/(\operatorname{tr}H)^{n-1}\), the remaining
epsilon bound gives

\[
\varepsilon H-\varepsilon^2C^{\mathsf T}A^{-1}C
\succeq
\varepsilon\eta\left(1-
 \frac{\|C\|_F^2}{2(1+\|C\|_F^2)}\right)I
\succeq\tfrac12\varepsilon\eta I.
\]

Thus \(Q_\varepsilon\) is positive definite, including when
\(c<0\), \(\ell\ne0\), or some span coordinates are redundant.
No estimate of its smallest eigenvalue is inferred directly from
the separate Schur blocks. The subsequent determinant bound
\(\delta\) supplies that estimate correctly.

The subtraction matrix is exactly
\(D_R=\operatorname{diag}(aa^{\mathsf T},I_n)\), because its
quadratic form is \(R^2+\|X\|^2R^2=hR^2\). Its actual norm is
\(\max\{\|a\|^2,1\}\), bounded by the author's
\(1+\|a\|^2\). Therefore

\[
\widehat\lambda Q_\varepsilon-D_R
\succeq
\bigl(2+\|a\|^2-\max\{\|a\|^2,1\}\bigr)I
\succeq I.
\]

The two numerical margins, the SOS identity (14), and its degree
bound are valid. Each entry of \((w,b)\) has degree at most three.

## Rational size and the field claims

The general lemma needs only rational linear algebra to find the
span coordinates: compare coefficients through degree three.
The number of equations is polynomial in the explicit input, and
minor bounds give polynomial bit length for a rational solution.

For the tower, the constant matrices have dimension \(O(n^2)\).
Determinants of rational matrices of polynomial dimension and entry
bit length, powers with polynomial exponents, exact comparisons,
and ceilings all retain polynomial bit length and admit polynomial
time algorithms. This applies to \(\eta,\varepsilon,\delta\),
the enlarged integer scale, and the final Gram. The determinant
bound can make the scale numerically large without making its
binary representation exponentially long.

Rational LDL decomposition of the positive definite final Gram has
positive rational diagonal entries and polynomial bit length.
For a weight \(u/v>0\), the binary expansion of \(uv\) gives
at most twice its bit length in integer squares. Division by
\(v^2\) then gives rational squares. Thus the conversion to actual
unweighted square factors is deterministic and polynomial in size;
it does not silently require square roots or an integer-factorization
algorithm.

The curvature threshold also remains sufficient. For the last-gate
matrix \(T\), \(\|T\|=1\) and \(\|T\|_F^2=3/2\).
The Hessian Gram of \(R^2\) therefore has norm at most
\(8(3/2)+4=16\). The first threshold in (12) leaves a rational
Hessian Gram at least the identity. Since value and gradient still
vanish at the same tower point, its unique zero is unchanged.

The earlier obstruction to polynomial SOS over a real field
omitting the final root is independent of the positive scale.
For a field containing the root, the rational positive Hessian
Gram supplies the existing Taylor SOS argument over that field.
Both directions therefore survive this particular rescaling.
The individual-coefficient conclusion uses the previously proved
individual-coefficient lemma as stated by the author.

## Common denominator and its minimum degree

If \(hF=\sum f_i^2\), multiplication by
\(h=1+\sum X_j^2\) gives exactly

\[
F=\sum_i(f_i/h)^2+\sum_{j,i}(X_jf_i/h)^2.
\]

The numerator degree is at most four, the number of factors remains
polynomial, and \(h\geq1\) on all real points. A multiplier
identity has thus been converted to a genuine squared-common-
denominator identity.

For completeness, suppose a rational-function SOS had a common
nonconstant rational affine denominator \(l\). Clearing it gives
\(l^2F=\sum u_i^2\) with \(u_i\in\mathbb Q[X]\). Each
\(u_i\) vanishes at every real point of \(l=0\). A rational
affine change of coordinates makes that hyperplane a coordinate
hyperplane, proving \(l\mid u_i\) over \(\mathbb Q\).
Canceling \(l^2\) would make \(F\) rational polynomial SOS,
contrary to the retained field obstruction. A nonzero constant
denominator gives the same contradiction directly.

The minimum common-denominator degree is therefore exactly two
over \(\mathbb Q\). This assertion concerns common polynomial
denominators for rational functions with rational coefficients;
over the tower coefficient field the polynomial SOS already has
denominator degree zero.

## Targeted verification

The separate retained checker
[check_tower_quadratic_denominator_review.py](check_tower_quadratic_denominator_review.py)
uses a three-variable quadratic \(G\) with positive quadratic
part, nonzero linear part, and negative constant. Exact arithmetic
checks the span identities, zero Gram relation, multiplier identity,
positive definiteness of \(Q_\varepsilon\), and the claimed final
matrix margin. This example tests signs and indexing; the universal
result rests on the inequalities above.

Command run successfully:

```text
python research-20260927/check_tower_quadratic_denominator_review.py
```

It printed:

```text
PASS: syzygy, zero Gram relation, multiplier identity, and exact PSD margins
```

No project-wide verification or CI inspection was performed. The
author's file was not edited by this reviewer.

The commands `git diff --no-index --check /dev/null` followed by
each of the review and checker paths emitted no whitespace warnings;
both returned the expected difference status for a new file.
