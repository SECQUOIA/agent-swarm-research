# A two-marginal cubic family with limiting ratio 243/115

Date: 2026-09-04. Status: full family, exact finite witness, and unit-coefficient corollary independently audited; see `notes/review-positive-cubic-two-level.md`.

The [finite-witness Lean package](../formal/topics/04-cubic-gaps/COVERAGE.md) proves the scalar minorant and attaining atoms, the exact cases m=4,8,12,16, and the explicit 52-variable homogeneous example below. Its [verification record](../formal/topics/04-cubic-gaps/VERIFICATION.md) records the completed checks. The bounds for every m and the limit 243/115 remain written results outside that formal scope; the [focused cubic completion](../formal/topics/11-cubic-completion/COVERAGE.md) also excludes the general two-level family.

Positive cubic polynomials can have a term-by-term/convex-hull gap ratio above two even when every coordinate marginal is at least 1/2 and there are only two distinct marginal values. The family below uses only two types of monomials and has an exact limiting ratio 243/115. This is a structural simplification of the cubic counterexample, not an improvement of the strongest lower bound for R(3).

## Finite family

Let m be a positive multiple of four. Take two disjoint groups U,W of m variables, and write A and C for the coordinate sums of U and W, respectively, and E₂ for the elementary symmetric multilinear polynomial of degree two on the indicated group. Set

\[
f_m=A E_2(W)+\frac{5m}{4}E_2(U).
\]

Every coefficient is a positive integer and every monomial has degree two or three. Evaluate each coordinate of U at 1/2 and each coordinate of W at 3/4. Then

\[
\frac{243}{115}\left(1-\frac1m\right)
\le\frac{\operatorname{tbtgap}f_m}{\operatorname{chgap}f_m}
\le\frac{243}{115}.
\tag{1}
\]

In particular, the ratio exceeds two for m≥20 and converges to 243/115 as m tends to infinity through multiples of four. At m=20, the polynomial is simply A E₂(W)+25E₂(U), in 40 variables, and its ratio is at least 4617/2300>2. No general exact finite hull-gap formula is asserted.

## An exact 32-variable witness

The member m=16 has an even smaller exact certificate. It is

\[
f=A E_2(W)+20E_2(U),
\]

with 16 variables in each group and the same marginals 1/2 and 3/4. At every binary vertex, whose success counts satisfy A,C∈{0,...,16}, the following affine minorant holds:

\[
A\binom C2+20\binom A2
\ge214A+\frac{177}{2}C-1686.
\tag{8}
\]

The exact verifier checks all 289 integer count pairs. Equality holds at (A,C)=(8,12). Uniformly choosing an eight-element subset of U and a twelve-element subset of W therefore gives the prescribed individual marginals and attains the minorant. Consequently

\[
\operatorname{vex}f=1088,\qquad
\operatorname{cav}f=\operatorname{tbtgap}f=2160,\qquad
\frac{\operatorname{tbtgap}f}{\operatorname{chgap}f}
=\frac{135}{67}>2.
\]

This finite equality uses an exact integer-grid certificate; the continuous-square certificate below supplies the general family bound and limiting ratio.

## An explicit unit-coefficient homogeneous cubic

The 32-variable witness also gives a small explicit example with every coefficient equal to one and every monomial of degree exactly three. Introduce 20 additional variables z₁,...,z₂₀ and define

\[
g=A E_2(W)+\left(\sum_{k=1}^{20}z_k\right)E_2(U).
\]

There are 52 variables and 4,320 distinct cubic monomials, all with coefficient one. Set the U marginals to 1/2, the W marginals to 3/4, and every z marginal to 999/1000. All coordinates are strictly inside the cube. Then

\[
\frac{\operatorname{tbtgap}g}{\operatorname{chgap}g}
\ge\frac{2700}{1343}>2.
\tag{9}
\]

To prove it, first set every z to one. The polynomial reduces to the exact 32-variable witness, so its two gaps agree with those computed above. With the stated perturbed marginals, every monomial still has concave value 1/2 and convex value zero. Thus cav g=tbtgap g=2160.

For any binary coupling with these new marginals,

\[
g=f-\left(20-\sum_{k=1}^{20}z_k\right)E_2(U),
\qquad 0\le E_2(U)\le120.
\]

Its projection onto U,W has the original marginals, so E f≥1088. Also E[20−Σz_k]=20/1000. Therefore

\[
\operatorname{vex}g\ge1088-\frac{12}{5},\qquad
\operatorname{chgap}g\le1072+\frac{12}{5}=\frac{5372}{5}.
\]

The hull gap is positive, as is seen by comparing independent rounding with common-threshold rounding. This proves (9). The construction is explicit; it uses no probabilistic existence argument or coefficient approximation.

## A globally valid scalar minorant

For real a,c∈[0,1], set

\[
F(a,c)=ac^2+\frac54a^2,\qquad
\ell(a,c)=\frac{11}{6}a+\frac{20}{27}c-\frac{95}{108}.
\]

The following identity proves F≥ℓ over the full square:

\[
F-\ell
=\frac54\left(a-\frac{11-6c^2}{15}\right)^2
+\frac{(1-c)(3c-2)^2(3c+7)}{135}.
\tag{2}
\]

Both terms are nonnegative. Equality holds at (a,c)=(1/3,1) and (5/9,2/3). Their mixture with weights 1/4 and 3/4, respectively, has mean (1/2,3/4), and

\[
\ell(1/2,3/4)=\frac{16}{27}.
\]

Thus the minimum expected value of F over arbitrary distributions on the square with this mean is exactly 16/27. This statement concerns the auxiliary scalar polynomial F; it does not treat repeated powers as independent multilinear coordinates.

## Lower bound on the finite ratio

At a binary vertex, let a=A/m and c=C/m be the two normalized success counts. Direct expansion of the elementary symmetric polynomials gives

\[
\frac2{m^3}f_m
=F(a,c)-\frac{ac+(5/4)a}{m}.
\tag{3}
\]

Since ac≤a on the square, (2) and (3) imply, for every binary coupling with the prescribed marginals,

\[
\frac2{m^3}\mathbb E f_m
\ge\frac{16}{27}-\frac9{8m}.
\tag{4}
\]

The concave envelope has the exact scaled value

\[
\frac2{m^3}\operatorname{cav}f_m
=\frac98\left(1-\frac1m\right).
\tag{5}
\]

Indeed, each cubic term has concave value 1/2, each quadratic term also has concave value 1/2, and one common-threshold distribution attains all these values together. Subtracting (4) from (5) yields

\[
\frac2{m^3}\operatorname{chgap}f_m\le\frac{115}{216}.
\tag{6}
\]

Each cubic term has convex value max(0,1/2+3/4+3/4−2)=0 and gap 1/2. Each quadratic term has convex value zero and gap 1/2. Therefore

\[
\frac2{m^3}\operatorname{tbtgap}f_m
=\left(\frac12+\frac54\frac12\right)\left(1-\frac1m\right)
=\frac98\left(1-\frac1m\right).
\tag{7}
\]

Equations (6) and (7) prove the lower inequality in (1).

## Matching limit

Use the two-atom distribution with weights 1/4 and 3/4 attaining equality in (2). Conditional on its sampled pair (a,c), independently sample every coordinate of U as Bernoulli(a) and every coordinate of W as Bernoulli(c). This preserves the individual marginals 1/2 and 3/4. Distinct variables within each monomial are conditionally independent, so

\[
\frac2{m^3}\mathbb E[f_m\mid a,c]
=\left(1-\frac1m\right)F(a,c).
\]

Averaging gives a feasible convex-envelope value of (1−1/m)16/27. Together with (5), this proves

\[
\frac2{m^3}\operatorname{chgap}f_m
\ge\frac{115}{216}\left(1-\frac1m\right)>0.
\]

Combining this inequality with (7) proves the upper inequality in (1), and the two bounds establish the claimed limit.

## Scope

Every displayed marginal is strictly inside the unit cube, and the smallest marginal is exactly 1/2. Since all finite gap functions are continuous and the m=20 ratio is strictly above two, sufficiently small upward perturbations of the U marginals give examples with every marginal strictly greater than 1/2 as well. No explicit perturbation radius is needed for that existence statement.

The coefficient-removal theorem in `positive-multilinear-coefficient-removal.md` separately allows the same degree-based supremum to be approached using unit coefficients and homogeneous polynomials, with increased dimension. It is not needed for this two-type family.

The exact symbolic replay `code/multilinear_ratio/verify_cubic_two_level.py` checks the factor identity, equality atoms, weighted means and objective, finite count expansion, and rational gap constants. Its `.log` records a complete pass.

The independently audited [equal-marginal companion](positive-multilinear-equal-marginals.md), a consequence of classical symmetric-envelope machinery, shows that equal normalized marginals always give ratio at most two. Thus two distinct marginal values are the minimum needed for a ratio above two on the unit cube; the 32-variable example has exactly two.
