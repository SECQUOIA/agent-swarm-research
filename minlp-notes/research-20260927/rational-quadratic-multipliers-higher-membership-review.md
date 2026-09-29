# Fresh review of multiplier order from quadratic ideal membership

Date: 2026-09-28. Status: the mathematical proof passes after a
clarification of the scale's input length. Publication priority was
not established or certified by this review.

Reviewer: `tower_quadratic_space_fresh`. I did not develop the
higher-membership construction. I read its complete frozen proof,
independently checked the matrix identities and all level exponents,
challenged its complexity quantifiers, and wrote a distinct exact
stress checker. The reviewed source is
[the higher-membership note](rational-quadratic-multipliers-higher-membership.md).

## The hierarchy has the needed coordinates and signs

The initial list contains every \(X^\alpha q_i\) through coefficient
degree \(d\). A target \(R_a\) therefore has its supplied coordinate
vector entirely at level zero, even when that vector uses degree-\(d\)
membership coefficients. Level is an assigned Gram-coordinate level,
not the polynomial degree of that entry.

For \(|\alpha|=e>0\), choosing an index with \(\alpha_j>0\)
represents \(X^\alpha R_a\) by one coordinate in the existing block
\(X^{\alpha-e_j}XR_a\), at level \(e\). Each new block
\(X^\alpha XR_a\) is placed at level \(e+1\). Repeated polynomial
entries do not cause a problem: each designated coordinate is separate,
and the argument never assumes independence of the polynomial list.

The polynomial lists \(X^\alpha G\) and \(X^\alpha X_jG\) are
indeed available at level zero for \(|\alpha|\le d-1\). Their
coordinates follow from the supplied constant-span representation of
\(G\). Thus no hidden multiplication step requires degree \(d+1\)
membership coefficients.

Writing \(u=X^\alpha\), \(p=uR_a\), \(g=uG\),
\(z=uXR_a\), and \(V=uXG\), the identity
\[
 z^{\mathsf T}Hz+p\ell^{\mathsf T}z+cp^2
       -V^{\mathsf T}T_a z-g r_a^{\mathsf T}z-s_agp=0
\]
is correct for inhomogeneous targets. The first three terms are
\(u^2G R_a^2\). The subtracted expression is
\(u^2G R_a(X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a)\), the same
polynomial. Negative constants, nonzero linear terms, and off-diagonal
entries of \(H\) or \(T_a\) do not change the identity.

## One rational scaling controls all errors

After removing the new positive \(H\) block, the residual terms join
levels \((e,e)\), \((0,e)\), \((e,e+1)\), or \((0,e+1)\).
Multiplication by \(\rho^{2(e+1)}\), followed by congruence with
the diagonal entries \(\rho^{-l}\), gives powers
\(2,e+2,1,e+1\), respectively. Every exponent is positive.
This includes \(e=0\), where the parent may have many nonzero
coordinates in the initial block.

The designated positive blocks occupy disjoint coordinate blocks:
the initial multinomial-weight diagonal and one copy of \(H\) per
new block. They are at least \(\eta_0 I\). Other occurrences of
the same polynomial in the redundant list do not identify these
matrix coordinates or destroy this estimate.

The sum of absolute values of all entries bounds the operator norm
of each symmetric error matrix and their sum. With the stated
\(K\) and \(\rho=\eta_0/[2(1+K)]\), the scaled error has norm
at most \(K\rho<\eta_0/2\). Hence the scaled matrix is positive
definite. Undoing the congruence gives precisely
\[
                  Q\succeq\eta_0\rho^{2d}I/2.
\]
No determinant of an intermediate growing Gram matrix is needed.

Every \(X^\beta R_a\) with \(|\beta|\le d\) also has a
designated coordinate: the input membership vector if \(\beta=0\),
and a selected entry of the level-\(|\beta|\) block otherwise.
The stated target matrix therefore represents
\(h^d R^{\mathsf T}JR\), including cross-target terms for arbitrary
symmetric \(J\). Its maximum absolute row sum bounds its operator
norm. The scale then gives \(\lambda Q-D_J\succeq I\), as claimed.

The zero-set conclusion also follows. Positive definiteness makes
zero value equivalent to every entry of the polynomial list vanishing.
The list includes every baseline factor, and the membership identities
make every other entry zero when those factors vanish. Since \(h>0\),
the multiplier does not add real zeros.

## Complexity, denominator degree, and the corrected quantifier

The claimed size is polynomial in the explicitly expanded monomial
budget \(\binom{n+d}{d}\), the displayed dimensions, and the rational
coefficient lengths. It is not a bound polynomial only in binary-encoded
\(d\). The coefficient-matching system through degree \(d+2\)
has polynomially many rows relative to that budget, as shown in the
author's binomial-coefficient comparison.

All zero-matrix entries use rational coefficient operations on supplied
representations. Their sum \(K\), the determinant bound for the fixed
\(n\)-by-\(n\) matrix \(H\), and \(\rho\) have polynomial bit
length. Raising \(\rho\) to powers at most \(2d\) keeps this
property in the stated model. Rational elimination and binary expansion
of positive weights yield actual rational squares of polynomial length;
no square-root field extensions or factorization algorithm are assumed.

I requested one clarification: a polynomial output bound cannot be
independent of the bit length of an arbitrarily large externally chosen
\(\lambda\). The author added that the bound uses the constructed
\(\lambda_*\); for a larger prescribed scale, its bit length is
included in the input. I reread the amended theorem statement and
verified that it resolves this quantifier issue. The original reviewed
hash was `1b3f52f1d0beeb3be13158735a390a32f3880213a4d484028e6e8001ae6b7c22`;
the corrected source hash at this recheck was
`5aa787fa207b34b6a99259f4676763e4c23c8ccc9d2b84196dc896cd6a2528a9`.

For even \(d\), division of the multiplier SOS by \((h^{d/2})^2\)
gives a common denominator \(h^{d/2}\). For odd \(d\), multiply
the SOS once by \(h=1+\sum X_j^2\) before division. The stated
denominator degree \(2\lceil d/2\rceil\) and numerator bound two
higher are therefore correct. They are upper bounds, not optimality
claims. The separate degree-zero membership case is direct rational
Gram domination and needs no multiplier.

## Distinct exact stress checks

I created and ran:

```text
python3 research-20260927/check_higher_membership_multiplier_review.py
```

The final retained version passed for \(n=2\), three baseline factors,
two targets, and membership degrees \(d=2,3\). The Gram dimensions
are thirty and fifty-four. It uses
\[
 G=2x^2+2xy+3y^2+x-2y-3,\qquad q=(G,x-1,y),
\]
so \(H=\left(\begin{smallmatrix}2&1\\1&3\end{smallmatrix}\right)\succ0\),
the linear term is nonzero, and the constant is negative. Both
nonhomogeneous quadratic targets vanish at \((1,0)\). The target
matrix \(J=\left(\begin{smallmatrix}1&2\\2&-3\end{smallmatrix}\right)\)
is indefinite and has a nonzero cross term.

The checker adds higher-degree zero syzygies to the target membership
identities. This makes their supplied coefficient degree exactly two or
three and exercises every level of the construction. These degrees are
not claimed to be minimal for these examples; the checks test the
construction for valid supplied representations, not sharpness of the
degree theorem.

Using exact symbolic and rational arithmetic, the checker verifies every
zero identity, the assembled scaled error bound, positive definiteness
of both the baseline and final Gram by separate exact LDL decompositions,
and the complete final polynomial identity. An earlier version with
\(H=I\) also passed; the retained version adds an off-diagonal positive
matrix to challenge the block assembly.

The finite checks do not prove the general theorem, its bit bounds, or
publication priority. Those mathematical conclusions rely on the audited
proof and its stated input model. No Lean verification, numerical roots,
project-wide checks, or CI inspection was used.

## Significance assessment

The theorem gives an explicit denominator-order upper bound from a
supplied ideal-membership degree while keeping the perturbed polynomial
quartic. Its assumptions are material: targets remain quadratic, a
positive definite leading quadratic is supplied in the constant factor
span, and the degree budget is explicitly expanded. It does not solve
unrestricted ideal membership, discover that positive definite quadratic,
or provide a practical estimate for the possibly very large scale.

This is a useful constructive structural theorem. A comparison with
effective ideal certificates, order-unit arguments, and rational SOS
denominator bounds remains necessary before claiming a new publishable
result. A positive mathematical review does not supply that comparison.

## Additional independent check: degree two can be necessary for membership

After the main review, the author supplied a small example separating
affine membership from degree-two membership under the theorem's
positive-leading-quadratic hypothesis. I independently checked it.
In \(\mathbb Q[x,y,z]\), let
\[
 q=(G,x^2,xy-z,yz-1),\qquad G=x^2+y^2+z^2-1,
 \qquad R=1.
\]
The identity
\[
\begin{aligned}
1={}&xG+(-x+y^2-1)x^2\\
   &+(-xy+xz-y)(xy-z)+(-x^2-x-1)(yz-1)
\end{aligned}
\]
gives coefficient degree at most two. Define the rational functional
on polynomials of degree at most three by
\[
 \mathcal L=[1]+[x]+[yz]+[z^2]+[xy^2]+[xyz],
\]
where brackets extract monomial coefficients. It annihilates every
\(q_i,xq_i,yq_i,zq_i\), while \(\mathcal L(1)=1\).
Therefore no affine coefficient representation of the target exists;
the minimum membership-coefficient degree is exactly two.

I checked the identity by hand cancellation, checked all sixteen
functional values, and ran a separate inline `python3` calculation
using exact SymPy expansion and coefficient extraction. It returned
zero on all sixteen affine multiples and one on the target, and the
displayed identity expanded exactly to one. This calculation is
distinct from the author's original coefficient-matching search.

Here \(H_G=I\) is positive definite. The baseline factors have no
common zero even over the complex numbers: \(x^2=0\) forces \(x=0\),
then \(xy-z=0\) forces \(z=0\), contradicting \(yz-1=0\).
An empty common zero set is allowed by the multiplier theorem. The
example proves that its degree-two membership hypothesis is strictly
more general than affine membership. It does **not** prove any lower
bound on the required SOS multiplier or rational-function denominator
degree; other certificate constructions are not excluded.
