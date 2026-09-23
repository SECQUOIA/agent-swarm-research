# A linear lower bound in positive-box aspect ratio

Date: 2026-09-04. Status: full proof independently audited; no unresolved mathematical issue identified. Novelty is provisional.

Let C_box(ρ) be the worst positive multilinear termwise-to-hull gap ratio on
boxes `[1,ρ]^n`, over arbitrary dimensions, degrees, positive coefficients,
and evaluation points with positive hull gap. For every fixed ρ>1,

```
C_box(ρ) >= max{2,ρ}.                                    (1)
```

Combined with the independently reviewed [matching upper bound](positive-multilinear-positive-box-sharp.md),
this gives the sharp asymptotic `C_box(ρ)~ρ`, with leading constant one.
The construction below has actual
gap ratio tending to ρ while ρ stays fixed and its dimension grows. It gives
more than a lower bound based on perturbing zero box endpoints.

## Construction and exact termwise gap

Fix ε=1/ρ in (0,1). For integers L>=2, set b=L² and m=b^L. Use the variable-radix
support family with L anchor variables and m leaf variables:

```
p(a,z)=Σ_(j=1)^L Σ_(B in P_j) a_j product_(i in B) z_i,
```

where P_j partitions the m leaves into b^j nested equal blocks. Every variable
now ranges over `[ε,1]`. Its normalized endpoint-success mean is

```
Pr(A_j=1)=u_j=b^-j,
Pr(Z_i=1)=1-1/m,
```

so the physical means are `ε+(1-ε)u_j` and
`ε+(1-ε)(1-1/m)`. Every mean is strictly inside its interval. At a binary
endpoint assignment a physical anchor is ε+(1-ε)A_j, and each physical leaf
is ε+(1-ε)Z_i.

A level-j block contains k=m/b^j leaves. The sum of the endpoint-failure
probabilities across its anchor and leaves is

```
(1-u_j)+k/m = 1.
```

Its vertex product is ε^R, where R is the number of failed coordinates in
that term. Jensen's inequality gives E ε^R>=ε whenever E R=1. This value is
attainable by selecting exactly one failed coordinate, using the prescribed
failure probabilities as the categorical law. Therefore every term's exact
convex-envelope value is ε.

The common-threshold success coupling attains every positive term's concave
envelope. Since u_j<=1-1/m, its value for this term is

```
C_(j,B) = u_j + (1-1/m-u_j)ε + ε^(k+1)/m
        = ε+(1-ε)u_j - (ε/m)(1-ε^k).
```

Summing the gaps of the b^j terms at each level gives the exact total

```
T_L = (1-ε)L - D_L,
D_L = ε Σ_(t=0)^(L-1) (1-ε^(b^t))/b^t.                  (2)
```

Here t=L-j. The correction is uniformly bounded:

```
0 <= D_L <= ε Σ_(t=0)^(L-1)b^-t <= ε b/(b-1).             (3)
```

Consequently T_L/L→1-ε for each fixed ε.

## The hull gap as softened coverage

For any admissible binary coupling let R_B count failed leaves in block B,
and let R be the total number of failed leaves. Then E R=1. At that endpoint
assignment the physical term equals

```
[ε+(1-ε)A_j] ε^(R_B).
```

Subtracting its expectation from the concave-envelope value above and summing
shows that the exact hull gap is

```
H_L = max E [(1-ε) Σ_j A_j Σ_(B in P_j)(1-ε^(R_B))
                   + ε Σ_j Σ_(B in P_j)(1-ε^(R_B))] - D_L,  (4)
```

where the maximum ranges over all binary laws with the stated marginals.

Let N_j be the number of level-j blocks containing at least one failed leaf.
For every endpoint assignment,

```
1-ε^(R_B) <= 1[R_B>0].
```

Therefore the first, anchor-weighted part in (4) is at most (1-ε) times
`max E Σ_j A_j N_j`. This is exactly the hull gap of the reviewed unit-box
variable-radix family with the same normalized marginals. Since b>=L, its
value is `1+(L-1)/b`; see
[the incidence-growth result](positive-multilinear-incidence-sharp-growth.md).

For the second part, the finite geometric sum gives

```
1-ε^r <= (1-ε)r,       r=0,1,2,... .
```

The blocks at each level partition the leaves, so `Σ_B R_B=R` and E R=1.
Applying these two bounds to (4) yields

```
H_L <= ε(1-ε)L + (1-ε)[1+(L-1)/b] - D_L.                (5)
```

## An attaining-order lower bound on the hull gap

Choose exactly one uniformly random failed leaf. This gives every leaf its
required failure marginal. Choose anchors with their required means, for
example independently of that leaf and of each other.

For every level there is exactly one block with one failed leaf, so

```
Σ_(B in P_j)(1-ε^(R_B)) = 1-ε
```

deterministically. The expectation of the anchor-weighted contribution is
therefore `(1-ε)² Σ_j b^-j`. Substitution into (4) gives

```
H_L >= ε(1-ε)L + (1-ε)² Σ_(j=1)^L b^-j - D_L.           (6)
```

Equations (3), (5), and (6), with b=L², imply

```
H_L/L -> ε(1-ε),
T_L/H_L -> 1/ε = ρ.                                    (7)
```

The denominator is positive already for every finite L: the geometric-sum
inequality gives D_L<=ε(1-ε)L, so (6) is at least the strictly positive term
`(1-ε)² Σ_j b^-j`.

All these are statements for each fixed ε in (0,1). They do not require any
interchange of the limits in L and ρ.

## Scaling and the other lower bound

The family above has unit coefficients on `[1/ρ,1]`. Scaling all physical
variables by ρ maps its domain to `[1,ρ]`. A degree-d term then has coefficient
ρ^-d, which remains positive. This affine change preserves both gaps exactly
for the correspondingly transformed polynomial. For rational ρ, all example
data are rational. Equation (7) proves the lower bound ρ in (1).

The lower bound two is already the classical positive complete-bilinear-graph
example at normalized means 1/2. For even n its ratio is `2(n-1)/n`, tending
to two. The substitution `z_i=1+(ρ-1)x_i` maps the cube to the common box
`[1,ρ]^n`. Every quadratic term acquires the same factor `(ρ-1)^2` plus
affine terms, so both gaps scale by that factor and the ratio is unchanged.
This gives C_box(ρ)>=2 for every ρ>1. For unequal coordinate widths the
quadratic factors differ, so the unchanged-ratio argument does not apply.

This proof does not determine the exact function C_box(ρ) at each fixed ρ.
It supplies the lower side of the sharp leading-order characterization; the
upper side is proved separately.

## Review and novelty status

The [topic-18 Lean package](../formal/topics/18-positive-box/README.md)
contains the radix lower construction, its finite gap estimates and fixed-ρ
limit, and the common-box bilinear witnesses. Its
[coverage map](../formal/topics/18-positive-box/COVERAGE.md) identifies the
declarations and the common-box qualification corrected above. The
[verification record](../formal/topics/18-positive-box/VERIFICATION.md)
distinguishes the recorded builds and kernel replays from later additions;
in particular, those checks predate the odd-dimensional bilinear formulas.

The [independent audit](../notes/review-positive-multilinear-positive-box-lower.md)
checks the original termwise envelopes, softened coverage, both hull-gap
bounds, finite positivity, scaling, and fixed-ρ limit. It also includes exact
rational primal and dual LP checks on small instances. The construction adapts
the reviewed variable-radix support family. Novelty should be assessed together
with the positive-box upper theorem; mathematical verification does not establish
priority.
