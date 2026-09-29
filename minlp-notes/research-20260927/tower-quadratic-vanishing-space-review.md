# Independent review of the tower's quadratic space and rational SOS recognition

Date: 2026-09-28. Status: passed; no mathematical defect found.
Reviewer: `one_parameter_spectrahedral_fields`, who did not develop
the uniform vanishing-space or product-independence lemmas.

I independently reconstructed the claims before reading the complete
[author note](tower-quadratic-vanishing-space.md), then read its proof,
algorithm, literature qualifications, and retained checker. The
five-relations-per-gate basis, injectivity of the quadratic-product map,
and rational SOS recognition consequence all hold with the stated
input and field restrictions. No substantive correction was needed.

## Exponent collisions and the complete quadratic space

Let `a=2^(1/5^k)`. Each coordinate of gate `i` is a power of `a`
with exponent `e*5^(k-i)`, for `e=1,2,3`. The five proposed
relations eliminate distinct local pivot monomials, and no pivot
occurs on a right-hand side. The remaining monomials have exactly
the following distinct base-five exponent patterns:

- zero, for the constant;
- one digit from `1,2,3,4`, for the retained local monomials;
- two digits from `1,2,3`, for monomials involving different gates.

Every retained exponent is strictly smaller than `5^k`. Eisenstein
irreducibility of `T^(5^k)-2` therefore proves independence of all
retained evaluations. This proves completeness of the basis, not just
independence of the displayed relations. It gives the claimed nullity
`5k` without building an exponentially large field-coordinate matrix.

The wrap factors are correct: the first gate gives `y1*z1=2` and
`z1^2=2*x1`. Evaluation classes can have more than two members;
for example, `x1`, `y2*z2`, and `z1^2` are in the same class with
the stated rational factors. I explicitly challenged this possibility.
The final proof uses retained monomials and records this example, so
it does not incorrectly count all collisions as isolated pairs.

The affine ideal-membership identities are polynomial identities,
including when the gate's radicand is a predecessor variable. They
therefore give affine multipliers for every rational quadratic in the
vanishing space. Cubic terms cancel. Neither the note nor this review
asserts an affine-multiplier bound for arbitrary higher-degree members
of the full ideal.

## Independence of all products

I checked all fifteen local quartic monomials reconstructed in the
author's equations (6)--(7). The corresponding integer matrix has
determinant of absolute value one. Thus the fifteen products of
`(x^2,xy,y^2-xz,yz,z^2)` are independent, and the five quadratics
themselves are independent as well.

The global induction has the needed triangular dependence. Earlier
gate relations contain none of the last gate's variables. In the last
gate, the radicand is constant with respect to those variables;
consequently `-b_k*x_k` has local degree one and `-b_k` has local
degree zero. In a relation among pair-products, local degree four
therefore isolates exactly the products of two last-gate relations.
Their scalar coefficients vanish by the local fifteen-product result.

After those terms are removed, local degree two isolates the products
of one last-gate relation and one earlier relation. Independence of
the five leading quadratics remains valid over the polynomial ring
in all earlier variables, so the five earlier coefficient polynomials
vanish separately. Independence of the earlier basis then removes
all cross-gate coefficients. Induction removes the remaining products.

This proves independence over the rationals and reals for every `k`.
It does not rely on an unproved absence of degree-four exponent
collisions. It uses polynomial coefficient identities in independent
variables, not merely evaluations at the tower point. It also uses
the chain's direction of dependence; arbitrary cyclic or root-circuit
systems are not covered by this induction.

## The recognition algorithm and the full rational Gram

For a rational quartic `F` with the supplied zero `p`, any rational
SOS factor has degree at most two and vanishes at `p`. Thus all
factors belong to the established `5k`-dimensional rational space.
The product injectivity gives at most one Gram matrix on this basis.
Membership in its product span is still a necessary separate test;
the note does not assume that every quartic vanishing at `p` belongs
to that span.

A positive semidefinite rational Gram gives a rational SOS by exact
rational symmetric elimination followed by the binary decomposition
of its nonnegative rational weights. The latter produces polynomially
many rational squares of polynomial bit length and needs no integer
factorization. This proves both recognition and certificate output.

I also checked the stronger uniqueness assertion on the full monomial
basis. If `Q` is such a rational positive semidefinite Gram, zero
value at `p` implies `Q*m(p)=0`. Each row is consequently the
coefficient vector of a **rational** vanishing quadratic. With
`q=B^T*m`, its range lies in `range(B)`. For a rational left
inverse `C` of `B`,

```text
Q = B (C Q C^T) B^T.
```

Indeed `B C` is the identity on the range of `Q`, and symmetry
supplies the corresponding identity on the other side. The middle
matrix is positive semidefinite, and product injectivity uniquely
determines it. Thus the full rational positive semidefinite Gram is
unique whenever one exists.

This argument fails for arbitrary real rows: the real space of all
quadratics vanishing at `p` is much larger than the real scalar
extension of its rational vanishing space. The note explicitly
preserves this distinction. The algorithm does not recognize real SOS
or nonnegativity, find a zero, or search for a suitable root-circuit
encoding.

The runtime statement is polynomial in `k` and the explicit rational
input length, as written. It is not a bound polynomial only in the
bit length of a succinct binary `k`. The supplied zero can also be
validated efficiently: a quartic monomial has raw exponent at most
`12*5^(k-1)`, so reduction modulo `5^k` has quotient at most two.
There are only polynomially many printed monomials and their exponent
integers have `O(k)` bits. Grouping their reduced residues proves
`F(p)=0` without enumerating a degree-`5^k` field basis.

## Significance and prior boundary

The result supplies an explicit family whose rational SOS cone has
an injective positive-semidefinite parametrization. A polynomial-time
test follows from linear algebra once that parametrization and the
supplied zero are available. This is a useful structural consequence,
not a new general SOS algorithm or an established MINLP speedup.
The note appropriately leaves detection and useful occurrence of
these particular subproblems to future work.

I directly checked Laplagne's
[paper](https://arxiv.org/pdf/2312.16801), Proposition 3.1 and
Section 3.2. They support the attribution of rational kernel
restrictions and uniqueness mechanisms to earlier SOS work. They
do not establish priority for this specific uniform tower calculation.
The local fifteen-product calculation was already present in the
repository's least-field argument. The additional claims reviewed
here are the full base-five normal form, the cross-gate induction,
and their exact rational recognition consequence. No absence of an
equivalent prior theorem has been proved.

## Targeted verification

I created and ran a distinct checker:

```text
python research-20260927/check_tower_quadratic_space_review.py
```

It passed the complete degree-two evaluation-class counts for
`k=1,...,12`, full pair-product ranks for `k=1,2,3` over the exact
finite field of prime order 1009, and the exact local determinant of
absolute value one. Full rank of an integer matrix modulo a prime
certifies full rank over the rationals in each tested case. The
checks supplement the all-`k` proof; they do not prove it by finite
enumeration.

I read the author's retained checker and its reported larger finite
checks, but did not rerun those overlapping cases. No numerical root
approximations, Lean proof, project-wide checks, or CI inspection were
used for this review.
