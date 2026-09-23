# Investigation: integer precision for systems of quadratic outputs

Date: 2026-09-05. Parent task: test whether half the maximum rank in the
span of the output Hessians determines simultaneous approximation
complexity. The answer is negative. The candidate results and full
proof are in `results/quadratic-system-covariance-lower-bounds.md`.
Independent mathematical review was requested immediately.

## Counterexample and proof mechanism

The three coordinates of `x cross y`, with `x,y in [0,1]^3`, have
Hessians whose every nonzero scalar combination has rank four.
Nevertheless, simultaneous graph approximation needs
`3log2(1/ε)+O(1)` integer coordinates in every convex lift, and that
coefficient is achieved by compact binary linear lifts. The strongest
scalar Hessian-rank lower coefficient is only two.

The proof uses more information than a scalar combination. The three
Hessians satisfy `sum_j H_j²=2I_6`. For a same-parity graph-contact set
with covariance `Sigma`, midpoint errors give

```
sum_j tr(H_j Sigma H_j Sigma)<=48ε².
```

The squared Hessian entries in an eigenbasis of `Sigma` have row and
column sums two. Weighted AM–GM yields the lower bound
`12(det Sigma)^(1/3)` on the same quantity. Hence
`det Sigma<=64ε^6`. The volume-covariance bound gives contact-set volume
`O(ε³)`, and a cover by at most `2^p` parity classes proves the result.

This also proves a general sufficient criterion: if symmetric Hessians
obey `sum_j H_j²=cI_n`, `c>0`, the precision coefficient is `n/2`.
The upper uses shared coordinate expansions and residual McCormick or
square triangle relaxations. No additional structural hypothesis on
the convex lifted cells or integer ranges is needed.

For `k` independent cross-product blocks, the coefficient is `3k`
while every scalar combination has rank at most `4k`, giving an
arbitrarily large additive gap between the true and scalarized leading
coefficients. The matrix-space rank phenomenon itself is classical.

## A false weakening of the certificate

Positive definiteness of `sum_j H_j²` alone does not imply coefficient
`n/2`. For outputs `(x_1x_2,x_2x_3)` on `[0,1]^3`, the squared Hessian
sum is `diag(1,2,1)`, which is positive definite. Yet this star has
coefficient one by the independently reviewed graph theorem, below
`3/2`. The exact constant row/column sum in the AM–GM proof, or a
stronger suitable scaling/capacity hypothesis, matters.

Likewise, a vanishing common Hessian kernel is not sufficient. The
same star has zero common kernel. These examples prevent promoting
an incorrect universal characterization from nonsingularity alone.

## Primary bounded-rank matrix sources

Huang and Landsberg, *On linear spaces of matrices of bounded rank*,
[open author manuscript](https://people.tamu.edu/~jml/HLLbnddrk5-22-25.pdf),
Section 2.1, reviews compression spaces, odd-dimensional alternating
matrices, and exterior-product constructions. It identifies the
three-by-three alternating space among the classical primitive
bounded-rank examples. The cross-product matrix used here is precisely
that classical space, embedded as a symmetric off-diagonal block.
Our proposed contribution is its implication for approximation
formulation dimension, not a new bounded-rank matrix construction.

A publisher search result reports a 2026 version with DOI
10.1007/s00029-026-01137-x. Direct DOI opening failed in this run; the
open author manuscript above was readable. It lists Hang Huang and
J. M. Landsberg, and those are the names used in the result.

## Operator-capacity extension

The following derivation extends the isotropic certificate. It is
recorded with proof, but its source identification and independent
review should be completed before it becomes the central statement.
For real symmetric Hessians define

```
T(P)=sum_j H_j P H_j,
kappa=inf_(P positive definite) det(T(P))/det(P).
```

If `kappa>0`, then the full coefficient `n/2` follows. Indeed, for any
positive definite covariance `Sigma`, the matrix
`Sigma^(1/2) T(Sigma) Sigma^(1/2)` is positive definite. Its eigenvalue
AM–GM inequality gives

```
tr(Sigma T(Sigma))
 >=n[det(Sigma)det(T(Sigma))]^(1/n)
 >=n kappa^(1/n)(det Sigma)^(2/n).
```

The same fourth-moment bound gives `tr(Sigma T(Sigma))<=16mε²`, hence

```
volume(S)<=omega_n(n+2)^(n/2)
            [16m/(n kappa^(1/n))]^(n/4) ε^(n/2).
```

Thus the finite lower constant is

```
sqrt(n kappa^(1/n)/m) V^(2/n)
 / [4(n+2)omega_n^(2/n)].
```

This argument uses only positive capacity and does not assume that
operator scaling preserves symmetry or acts by a single congruence.
That avoids an unnecessary and potentially false inference about the
form of available scalings.

Garg, Gurvits, Oliveira, and Wigderson,
[Operator Scaling: Theory and Applications](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf),
Foundations of Computational Mathematics 20 (2020), Sections 1.3 and
2.1, give the established relationship between positive operator
capacity, rank nondecrease, and full noncommutative rank. Their standard
capacity is defined on Hermitian positive definite matrices; positivity
there implies positivity when restricted to real symmetric matrices,
which is sufficient for the argument above. The paper and its tutorial
also discuss the classical alternating three-by-three commutative versus
noncommutative rank gap. None of those algebraic facts is a novelty claim.

## Continuation: full noncommutative-rank candidate

The counterexample rules out maximum scalar rank as a complete invariant.
The investigation subsequently produced a full candidate characterization:
integer precision coefficient equals half the noncommutative rank.
The complete proof is in
`results/quadratic-system-noncommutative-rank-complexity.md`, under fresh
independent review. The two missing rank-deficient steps are now supplied:

- A Hermitian pencil over the free skew field has an invertible principal
  submatrix of order equal to its noncommutative rank. This follows by
  one-by-one or two-by-two Hermitian pivots and Schur complements.
- A maximum real shrunk pair `H_j U subset V` can be symmetrized to
  `Z=U intersect V^perp`, `W=V intersect U^perp`, with
  `dim Z-dim W=n-r` and `H_j Z subset W`. Orthogonal coordinates on
  `Z,W,(Z+W)^perp` admit precision exponents `0,1,1/2`, totaling `r/2`.

Complex-to-real descent is handled explicitly using supermodularity of
shrunk-space deficiency and conjugation. The primary involution reference
is Volčič's 2021 paper *Hilbert's 17th problem in free skew fields*,
Section 2.1. No independent left/right scaling is treated as an input
congruence.

The independent reviewer also supplied a full-rank energy argument
requiring no operator-capacity import: in every orthogonal basis, the
squared-entry sum of the Hessians has bipartite support with a perfect
matching, otherwise there is a shrunk space. Its permanent has a positive
minimum on the orthogonal group. A matching and arithmetic-geometric
mean then give the same determinant-energy exponent. This is included
as an alternative in the candidate theorem.

Another useful general viewpoint is volume of ellipsoids under bounds
on all quadratic forms. A maximal-simplex argument converts arbitrary
contact sets to comparable-volume affine balls with uniformly bounded
transformed Hessians. This suggests flags of subspaces and anisotropic
precision as an optimization problem, but no complete flag formula is
yet proved.

## Verification and search limits

`code/quadratic_rank/check_vector.py` verifies exact symbolic Hessians,
the sum-of-squares identity, the skew rank formula, the fourth-moment
expansion, and determinant energy inequalities on rational positive
definite matrices. All checks passed.

Targeted searches included quadratic systems integer dimension,
cross-product mixed-integer approximation, symmetric primitive
bounded-rank matrix spaces, and operator capacity/noncommutative rank.
No matching approximation-dimension result appeared. This is limited
negative evidence, not proof of novelty. The strong established
algebraic precedents must remain visible in any future presentation.
