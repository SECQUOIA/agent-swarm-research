# Integer dimension for quadratic graph approximation is half the Hessian rank

Date: 2026-09-05. Status: independently reviewed; see
`notes/review-quadratic-rank-integer-complexity.md`. Publication priority is unestablished. The lower
proof combines the published integer-parity midpoint mechanism with an
elementary maximal-simplex estimate. Related approximation geometry is
classical; the scope beyond piecewise affine approximants is material.

## Statement and scope

Let `B=product_i [l_i,u_i]` be a bounded box with `l_i<u_i`, and let

```
f(x) = (1/2) x^T H x + a^T x + b,
H=H^T,   r=rank(H).
```

Fix `ε>0`. A relaxation `R` must contain the entire graph of `f` over `B` and obey

```
|w-f(x)| <= ε  for every (x,w) in R with x in B.
```

Let `p_conv(ε)` be the minimum number of integer coordinates in any
finite-dimensional convex lifted formulation of such a relaxation:

```
R = {(x,w): exists y in R^q, z in Z^p with (x,w,y,z) in K},
K convex.
```

Integer coordinates can be unbounded. Neither closedness nor
polyhedrality of `K` is required for the lower bound. Let `p_bin(ε)` be
the minimum number of binaries when `K` is a polyhedron. All coefficients
may be real, and continuous variables and inequalities are unrestricted.

**Theorem.** If `r=0`, both minima are zero, even at zero error. If `r>=1`,
then, as `ε` tends to zero,

```
p_conv(ε) = (r/2) log2(1/ε) + O_(H,B)(1),
p_bin(ε)  = (r/2) log2(1/ε) + O_(H,B)(1).
```

The coefficient depends on rank and is independent of the numbers of
positive and negative eigenvalues. A compact binary linear upper
formulation uses `O_(H,B,n)(log(1/ε))` variables and constraints.

For an explicit lower constant, choose any index set `I` of size `r`
with `H_I=H[I,I]` nonsingular, and write
`V_I=product_(i in I)(u_i-l_i)`. Then every admissible convex integer
lift with `p` integer coordinates satisfies

```
ε >= c_I 2^(-2p/r),
c_I = |det(H_I)|^(1/r) V_I^(2/r) / (48 sqrt(r)).
```

This constant is not claimed sharp. In particular, it is weaker than
the exact univariate square constant in
`results/mip-relaxation-binary-lower-bounds.md`.

## Geometric lemma for indefinite forms

Let `M` be a nonsingular symmetric `d by d` matrix with `d>0`, let
`q(v)=(1/2)v^T M v`, and fix `δ>=0`. Let compact `S subset R^d` satisfy

```
|q(s-t)| <= δ   for every s,t in S.
```

Then

```
volume_d(S) <= 2^d (3 sqrt(d) δ)^(d/2) / sqrt(|det M|).
```

Proof. If the affine hull of `S` has dimension below `d`, its volume is
zero. Otherwise choose `s_0,...,s_d` in `S` maximizing

```
|det A|,   A=[s_1-s_0,...,s_d-s_0].
```

The maximum exists by compactness and is positive. Every `s in S` has
coordinates `c=A^(-1)(s-s_0)`. Replacing column `i` of `A` by `s-s_0`
yields another simplex with vertices in `S`, and its determinant equals
`c_i det A`. Maximality gives `|c_i|<=1` for every `i`. Therefore

```
S subset s_0+A[-1,1]^d,
volume_d(S) <= 2^d |det A|.
```

Put `v_i=s_i-s_0` and `G=A^T M A`. The pairwise bounds imply

```
|G_ii|=2|q(v_i)| <= 2δ,
|G_ij|=|q(v_i)+q(v_j)-q(v_i-v_j)| <= 3δ.
```

Each row of `G` has Euclidean norm at most `3 sqrt(d) δ`. Hadamard's
determinant inequality and the identity
`det G=(det A)^2 det M` give

```
|det A| <= (3 sqrt(d) δ)^(d/2) / sqrt(|det M|).
```

Combining the two estimates proves the lemma. This proof uses the
absolute determinant, and never positive definiteness. If `δ=0`, the
positive-volume case would make `G` both nonsingular and zero, a
contradiction; the same conclusion remains valid.

## Integer-parity lower bound

First suppose `H` is nonsingular and the domain has dimension `r=n`.
For each parity vector `alpha in {0,1}^p`, let `S_alpha` be the set of graph inputs
having a feasible lift whose integer vector has that parity. These sets
cover `B`. For `s,t` in the same class, choose corresponding lifts.
Their midpoint belongs to `K` by convexity, and its integer coordinates
are integer. Its output deviation is

```
[f(s)+f(t)]/2 - f((s+t)/2) = (1/8)(s-t)^T H(s-t).
```

Thus `|q(s-t)|<=4ε` for `q(v)=(1/2)v^T H v`. Taking the closure of each
`S_alpha` in `B` preserves the inequality by continuity. The resulting
at most `2^p` compact sets still cover `B`; no measurability assumption
on the original parity classes is needed.

The geometric lemma with `δ=4ε` gives volume at most

```
2^r (12 sqrt(r) ε)^(r/2) / sqrt(|det H|)
```

for each class. Summing volumes and rearranging proves

```
ε >= |det H|^(1/r) volume(B)^(2/r)
      / (48 sqrt(r)) * 2^(-2p/r).
```

If `rank(H)=r<n`, choose a nonsingular principal `r by r` submatrix
`H_I`. Such a submatrix exists: the sum of all principal minors of order
`r` is the product of the nonzero eigenvalues, which is nonzero. Fix all
coordinates outside `I` at any values in their box intervals. Intersecting
the lifted formulation with these affine equations preserves convexity
and does not add integer variables. The resulting graph problem is a
quadratic on the `r`-dimensional box `B_I`, with Hessian `H_I` and an
irrelevant affine term. Applying the preceding argument gives `c_I`.

The integer-parity step is the mechanism of Lubin, Vielma, and Zadik's
published Midpoint Lemma; see
[[lubin2022-mixed-integer-convex-representability]] p.11-12.
The new quantitative work in this proof is the volume estimate.

## Compact binary upper bound

A real symmetric matrix of rank `r` has a decomposition

```
(1/2)x^T H x = sum_(j=1,...,r) d_j ell_j(x)^2,
```

where each `d_j` is nonzero and the linear functions `ell_j` are
nonzero. For example, use its nonzero eigenvectors. One normalization uses the bounds
`L_j=min_B ell_j(x)` and `U_j=max_B ell_j(x)`; every width
`D_j=U_j-L_j` is positive because the box has interior. Normalize

```
y_j=(ell_j(x)-L_j)/D_j in [0,1].
```

Expanding the squares gives

```
f(x)=affine(x)+sum_j c_j y_j^2,
c_j=d_j D_j^2,   A=sum_j |c_j|>0.
```

Let

```
L=max{0,ceil[(1/2)log2(A/(4ε))]}.
```

For each `j`, independently apply the depth-`L` binary sawtooth
relaxation of `t_j=y_j²`. It contains that graph and satisfies
`|t_j-y_j²|<=2^(-2L-2)`. Set

```
w=affine(x)+sum_j c_j t_j.
```

Every exact graph point has a lift. For every point admitted with
integral binaries,

```
|w-f(x)| <= sum_j |c_j| |t_j-y_j²|
          <= A 2^(-2L-2) <= ε.
```

This uses `rL` binaries and `O(r(L+1))` sawtooth variables and rows,
plus the linear normalization equations and box bounds. Thus

```
p_conv(ε) <= p_bin(ε) <= rL
          = (r/2)log2(1/ε)+O_(H,B)(1).
```

Together with the integer-dimension lower bound this proves the theorem.
Affine terms do not affect the error or the integer count. The sawtooth
construction and its square error bound are established results of
Beach and collaborators; their use here is an upper-bound ingredient,
not a new formulation technique.

## Interpretation, limitations, and source comparison

This result concerns a scalar quadratic graph, so algebraic cancellations
are already reflected in `rank(H)`. For example, `(x_1+...+x_n)^2` has
rank one and leading integer count `(1/2)log2(1/ε)`, despite involving
all quadratic monomials. The simultaneous graph of all individual
products has a different complexity. Conversely, every nonsingular
indefinite Hessian requires the same leading count as a positive definite
Hessian of the same dimension, even with arbitrary convex lifts and
unbounded integer ranges.

For an epigraph or hypograph alone, rank is not the correct universal
parameter: a convex epigraph can have a direct zero-integer convex
representation. Domain constraints that remove every full-dimensional
transverse slice can also invalidate the stated lower bound.

Pottmann, Krasauskas, Hamann, Joy, and Seibold (2000) study optimal
piecewise affine quadratic approximation, including indefinite forms,
midpoint errors, and dimension reduction. Their objects are different
from arbitrary graph-containing mixed-integer convex lifts. The
investigation note records the precise source comparison and remaining
novelty limits. No prior statement of this general integer-dimension
rank law was found in the initial targeted searches, which does not
establish novelty.

Sources:

- Lubin, Vielma, Zadik, *Mixed-integer convex representability*,
  Mathematics of Operations Research 47 (2022), Lemma 4.1.
- Beach et al., *Enhancements of discretization approaches for non-convex
  mixed-integer quadratically constrained quadratic programming: Part I*,
  Computational Optimization and Applications 87 (2024), sawtooth
  relaxation and error formula; see the scalar result's source details.
- Pottmann et al., *On Piecewise Linear Approximation of Quadratic
  Functions*, Journal for Geometry and Graphics 4 (2000), 31–53,
  [open publisher PDF](https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0403.pdf).

## Verification record

`code/quadratic_rank/check_simplex.py` performs exact rational checks of
maximal-simplex enclosure, Gram polarization, determinant identities,
and Hadamard bounds for 42 examples covering every signature in
dimensions one through four. It also checks 15 rank-deficient matrices
for a nonsingular principal minor and the associated rank factorization.
Both groups passed on 2026-09-05. These checks exercise the proof's
algebraic steps and do not replace its general argument.


## Lean verification: topic 20

The [topic 20 coverage map](../formal/topics/20-scalar-quadratic/COVERAGE.md)
links the statements here to their Lean declarations. The
[verification record](../formal/topics/20-scalar-quadratic/VERIFICATION.md)
records the final targeted build, axiom audit, kernel checks and source
fingerprints; those checks are separate from the historical numerical checks
above. The formal scope is scalar quadratics, not the vector quadratic systems
reserved for topic 26 or the entire integer-dimension paper.

The lower proof starts with actual convex integer lifts and their compact
parity covers. It proves the contact-volume constant, constructs a nonsingular
principal submatrix of order `rank(H)`, and restricts the original box without
adding integer coordinates. The contact-volume lemma requires `δ >= 0`,
including for an empty contact. The zero-rank and zero-error affine cases are
included.

The upper proof constructs finite families of real affine inequalities. For a
linear coordinate `v_j · x`, it uses the positive enclosing radius

```
R_j = 1 + sum_i |v_ji| max(|l_i|, |u_i|),
y_j = (v_j · x + R_j)/(2 R_j).
```

This replaces exact coordinate extrema by a proved enclosure; it changes the
constant `A`, not the precision coefficient. The normalized coefficients are
`c_j = (lambda_j/2)(2 R_j)^2` for nonzero eigenvalues. At depth `L`, the actual
graph system has `r L` binaries, `r(3+2L)` real auxiliary coordinates, and
`2n + r(11+10L) + 2` inequality rows. Original inputs and the output are not
counted as auxiliary coordinates. The error is at most
`A 4^(-L)/4`, with `A=sum_j |c_j|`; affine substitution adds no rows.
The proof establishes the minima and the uniform bounded additive remainder,
not just a conditional count for a supplied decomposition.
