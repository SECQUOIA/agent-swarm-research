# Independent review: noncommutative rank and quadratic graph approximation

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.
Scope: the proposed law `p(ε)=(r/2)log2(1/ε)+O(1)`, where `r` is
the noncommutative rank of the real symmetric Hessian pencil.

The complete author draft survives this independent audit. This is a mathematical
review, not a publication-priority claim. The reviewed file is
`results/quadratic-system-noncommutative-rank-complexity.md`.
The audit covered the constants, graph containment, two-sided error, realification,
principal compression, all binary depth choices, and the formulation row count.
The only requested scope clarification was to state that the bounded input box
is closed, as assumed when using its compactness, or to use a closed interior
subbox for the lower bound. No substantive proof gap was found.

## An elementary alternative to the capacity import

The full-rank determinant-energy estimate needs no operator scaling theorem.
Here is an independently derived proof using the known no-shrunk-subspace
characterization of full noncommutative rank.

Let real symmetric `H_1,...,H_m` have full noncommutative rank in dimension `n`.
For a real orthogonal matrix `O`, set

```
K_j=O^T H_j O,
W_ab(O)=sum_j (K_j)_ab^2.
```

The bipartite support graph of `W(O)` has a perfect matching. Otherwise Hall's
theorem supplies a subset `J` of column indices whose row-neighborhood `I`
has `|I|<|J|`. Every `K_j` then maps `span{e_b:b in J}` into
`span{e_a:a in I}`, a shrunk subspace. Conjugation by `O` gives a real
shrunk subspace for the original tuple, contradicting full noncommutative
rank over the complex free skew field.

Consequently `per(W(O))>0` for every `O`. Since the orthogonal group is compact
and the permanent is continuous,

```
mu=min_(O in O(n)) per(W(O)) > 0.
```

For any positive definite real covariance matrix, choose
`Sigma=O diag(lambda_1,...,lambda_n) O^T`. Some permutation `pi` satisfies
`product_a W_(a,pi(a)) >= mu/n!`. Symmetry of the `H_j` gives

```
sum_j tr(H_j Sigma H_j Sigma)
 =sum_(a,b) W_ab lambda_a lambda_b
 >=sum_a W_(a,pi(a)) lambda_a lambda_(pi(a))
 >=n (mu/n!)^(1/n) (det Sigma)^(2/n).
```

The last step is the ordinary arithmetic-geometric mean inequality. All
selected weights are positive. The product of the selected eigenvalue factors
is `(product_a lambda_a)^2`, since `pi` is a permutation.

This provides the same exponent as the capacity proof, with
`gamma=n(mu/n!)^(1/n)>0`. Combining it with the independently checked
covariance identity and `|q_j(s-t)|<=4ε` gives

```
det Sigma <= (16m ε^2/gamma)^(n/2),
volume(S) <= omega_n (n+2)^(n/2) (16m/gamma)^(n/4) ε^(n/2).
```

The constant is nonconstructive and may be poor. No effective computation of
`mu` is asserted. Its positivity suffices for an asymptotic integer-dimension
law with a tuple-dependent additive constant. The argument does not assert
that the matrices can be simultaneously diagonalized.

## Principal compression over the free skew field

Use the complex free skew field with the involution conjugating scalar
coefficients and fixing the free generators. The pencil
`L=sum_j H_j t_j` is Hermitian for this involution.

Every Hermitian matrix `M` over a division ring with involution has an
invertible principal submatrix of size `rank(M)`. The following induction
checks the precise property needed here.

If a diagonal entry is nonzero, its one-by-one principal block is invertible.
If all diagonal entries vanish and `M` is nonzero, some `a=M_ij` is nonzero,
and the principal block

```
[0 a; a* 0]
```

is invertible, with inverse `[0 (a*)^(-1); a^(-1) 0]`.
Call this pivot block `P` and write the remaining blocks as
`M=[P B; B* D]`. Multiplication by invertible block triangular matrices
reduces it to `diag(P,D-B*P^(-1)B)`. The Schur complement is Hermitian and
has rank `rank(M)-size(P)`. Apply induction to this Schur complement.
If `J` is the resulting principal index set, the original principal matrix
on the pivot indices together with `J` is invertible by the same Schur
factorization. The empty matrix covers rank zero.

Therefore a real symmetric Hessian pencil of noncommutative rank `r` has
a principal `r`-coordinate restriction with full noncommutative rank. This is
a coordinate restriction of the ORIGINAL pencil, even though the induction
uses rational Schur complements. Fix all other input coordinates at interior
box values; the resulting graph has exactly these principal Hessians and
still has a full-dimensional `r`-dimensional box as its domain.

The needed involution is explicitly defined in Section 2.1 of
[Volčič, *Hilbert's 17th problem in free skew fields*](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1).
The principal-submatrix induction above is included as a direct proof;
it should not be presented as a new general algebra theorem.

## Real maximal shrinking and the upper bound

Let `A(U)=sum_j H_j U` and `d=max_U(dim U-dim A(U))` over complex
subspaces. The known min-max theorem gives `r=n-d`.
The deficiency function is supermodular: `A(U+V)=A(U)+A(V)` and
`A(U intersect V) subset A(U) intersect A(V)`, together with the dimension
identity for sums and intersections, show

```
f(U)+f(V) <= f(U+V)+f(U intersect V).
```

Because the Hessians are real, conjugate subspaces have equal deficiency.
If `U` attains `d`, supermodularity forces `U+conj(U)` to attain `d`
as well: each term on the right is at most `d`. This sum is invariant under
conjugation and is the complexification of a real subspace. Thus a real
maximizer exists with the same deficiency. This avoids any implicit appeal
to field-extension invariance.

For such real `U`, put `V=A(U)`, `Z=U intersect V^perp`, and
`W=V intersect U^perp`. Then `Z` and `W` are orthogonal, and

```
H_j Z subset W,
dim Z-dim W=dim U-dim V=d.
```

The first identity follows because `H_j z` lies in `V`, and for all `u in U`,
`<H_j z,u>=<z,H_j u>=0`. For the second, the restriction of orthogonal
projection from `U` to `V` and the restriction from `V` to `U` are adjoints,
so their ranks agree. Rank-nullity yields the identity.

In an orthonormal decomposition `Z direct-sum W direct-sum R`, the allowed
quadratic monomials have types `ZW`, `WW`, `WR`, and `RR`. There are no
`ZZ` or `ZR` terms. If `z,w,t` are these dimensions, then
`r=n-d=2w+t`.

An enclosing box in these transformed coordinates suffices: retain the
original box inequalities as additional linear constraints. Normalize the
enclosing coordinate intervals to unit length; this changes only fixed
coefficients and adds affine terms. Use no bits on `Z`, depth `2L` on `W`,
and depth `L` on `R`. Every allowed pair has residual width product at most
`2^(-2L)`, and every allowed square has residual width squared at most this
quantity. Exact binary-continuous product encodings plus the residual
McCormick/square inequalities therefore give `O(2^(-2L))` output error.
The binary count is `(2w+t)L=rL`, and fixed-system formulation size is
`O(L+1)`.

## Scope and details that must remain explicit

- The error requirement is two-sided and applies to every admitted output
  over the box. Exact graph containment is separately required.
- Parity classes need not be measurable; taking their closures inside the
  compact input box preserves all pair inequalities and produces a finite
  measurable cover.
- The proof gives a lower bound for arbitrary finite-dimensional convex
  lifts with unrestricted integer coordinates. The upper construction uses
  binary linear lifts; hence it applies to both minimum dimensions.
- Rank zero means every Hessian is zero, so the graph is affine and admits
  an exact continuous linear description. It should be treated separately.
- The theorem is asymptotic for each fixed system and box. Constants are
  not uniform over Hessian tuples approaching a rank-deficient tuple.
- This audit checks correctness, not novelty or practical solver performance.

The standard noncommutative-rank/shrunk-subspace correspondence is stated
in Theorem 1.4 and discussed with rank in Section 1.3 of
[Garg, Gurvits, Oliveira, and Wigderson, *Operator Scaling: Theory and Applications*](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
Its capacity machinery remains a valid alternative lower-bound route,
but the elementary support-matching argument above makes it unnecessary
for this proof.
