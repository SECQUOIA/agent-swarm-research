# Independent review of the analytic positive cubic family

Date: 2026-09-04. Target:
[`results/positive-cubic-analytic-family.md`](../results/positive-cubic-analytic-family.md).
This is an independent agent review, not external peer review.

**Verdict:** The global polynomial minorant, its domain partition, all Bernstein
certificates, and the finite-family scaling argument are correct. They prove
`R(3)≥483/223`. The certificates actually give a uniform positive residual of
`901/120000`, which strengthens the same proof to
`R(3)≥1610000/743033`. This improvement was communicated to the author and parent.
Neither bound is claimed to be the exact value of `R(3)`.

## Convex elimination and the two regions

Define

```
F(a,b,c)=6c³+27bc²+18b²+30ac+20ab+9a²,
ℓ(a,b,c)=37a+(79/2)b+38c−103/3,
h=F−ℓ.
```

For fixed `c`, the Hessian of `h` in `(a,b)` is
`[[18,20],[20,36]]`, with positive first principal minor and determinant 248.
Thus the quadratic is strictly convex.

On `0≤c≤3/10`, set `a=1` and `b*=13/24−3c²/4`. The latter lies in
`[569/1200,13/24]`, strictly inside `[0,1]`.
Direct differentiation gives `∂_b h=0` at that point and

```
∂_a h = −49/6+30c−15c² ≤ −31/60 < 0.
```

The derivative increases on the interval, since its derivative in `c` is `30−30c`.
For any `a≤1`, the first-order convexity bound contributes
`∂_a h·(a−1)≥0`, and the `b` term vanishes. This directly proves that the point is
a global minimizer over the square, with no unverified active-set assumption.
Its value is

```
p(c) = 101/96−8c+(117/8)c²+6c³−(81/8)c⁴.
```

On `3/10≤c≤1`, minimizing over all real `a,b` is a valid lower bound on the
minimum over the square. Write

```
v=30c−37,  w=27c²−79/2,  q=6c³−38c+103/3.
```

Completing the square gives the unrestricted minimum

```
r(c)=q−[18v²−20vw+9w²]/248
    =−11275/2976+(1709/62)c−(16983/248)c²
      +(2211/31)c³−(6561/248)c⁴.
```

This is exactly the author's quartic. The stationary point need not lie in the cube;
using the unrestricted minimum is conservative and valid regardless of its location.
The two regions cover the full cube and overlap only at their common boundary.

## Independent rational Bernstein verification

I recomputed `p` by substituting the boundary minimizer and `r` by the Schur-complement
formula above, using polynomial arrays with exact rational coefficients. This was
independent of the author's SymPy script. For each subinterval, I then transformed
`c=lo+(hi−lo)t`, computed its degree-four Bernstein coefficients, and expanded the
Bernstein polynomial back to its power coefficients. Every reconstructed polynomial
agreed exactly with the transformed original.

The resulting coefficients, in ascending Bernstein index, are:

| Polynomial and interval | Exact Bernstein coefficients |
|---|---|
| `p`, `[0,1/5]` | `101/96, 313/480, 839/2400, 1879/12000, 4133/60000` |
| `p`, `[1/5,3/10]` | `4133/60000, 751/30000, 901/120000, 947/60000, 11597/240000` |
| `r`, `[3/10,1/2]` | `6947/240000, 8293/48000, 11473/59520, 10003/59520, 1613/11904` |
| `r`, `[1/2,3/4]` | `1613/11904, 2257/23808, 1991/47616, 4615/95232, 15869/190464` |
| `r`, `[3/4,1]` | `15869/190464, 5627/47616, 4315/23808, 1435/5952, 485/2976` |

These fractions agree with every numerator and denominator in the result's table.
The five subintervals cover the relevant domains of `p` and `r`. All 25 coefficients
are strictly positive. The Bernstein basis functions are nonnegative and sum to one,
so every polynomial value is at least its row's smallest coefficient. Taking the
minimum across all rows gives the stronger uniform statement

```
h(a,b,c) ≥ δ := 901/120000   on [0,1]³.               (A)
```

In particular the requested nonnegative residual certificate is valid over every
real cube point, not only integer normalized counts or a numerical sample.

## Finite multilinear family and scaling

For three groups of `m` variables, where `m≥9` is a multiple of nine, the six family
coefficients are `(2,3,2m,5m/3,10m/9,m)`. They are positive integers. Their supports
are distinct squarefree monomials of degree two or three. The evaluation point has
respective group marginals `1/4,1/2,3/4`, all interior.

At binary counts `A=ma,B=mb,C=mc`, expanding the binomial count polynomials gives

```
18 f_m/m³ = F(a,b,c)
            −[18c²+27bc+18b+9a]/m+12c/m².            (B)
```

Each term in the negative correction is nonnegative on the cube, and their sum is
at most `18+27+18+9=72`; the last term is nonnegative. Thus the lower bound
`18 f_m/m³≥F−72/m` is valid. No assumption that the continuous count formula equals
the original multilinear polynomial away from vertices is used.

Every binary coupling with the prescribed individual marginals has mean normalized
counts `(1/4,1/2,3/4)`. The affine value at that mean is

```
37/4+79/4+57/2−103/3 = 139/6.
```

Combining the affine minorant and (B), and minimizing over binary couplings, gives
`18 vex(f_m)/m³≥139/6−72/m`. Using (A) improves this to
`18 vex(f_m)/m³≥139/6+δ−72/m`. This argument is valid for arbitrary dependence
between coordinates and groups; no primal attainability of the bound is asserted.

## Exact termwise and concave-envelope values

The normalized contributions `18/m³` times each family's concave-envelope value are
as follows, in the same family order as the result:

| Family | Normalized contribution |
|---|---|
| `2E_3(W)` | `9/2−27/(2m)+9/m²` |
| `3B E_2(W)` | `27/2−27/(2m)` |
| `2m E_2(V)` | `9−9/m` |
| `(5m/3)AC` | `15/2` |
| `(10m/9)AB` | `5` |
| `m E_2(U)` | `9/4−9/(4m)` |

Their sum is `167/4−153/(4m)+9/m²`. Positivity of coefficients makes this sum
exactly the full concave envelope: a common threshold coupling attains every
monomial's minimum marginal simultaneously.

Only the first family has a positive termwise convex-envelope value. Its normalized
contribution is `3/2−9/(2m)+3/m²`. Subtraction gives the exact normalized termwise gap

```
18 tbtgap/m³ = 161/4−135/(4m)+6/m².                  (C)
```

Subtracting the verified convex-envelope lower bound from the concave-envelope
value gives

```
18 chgap/m³ ≤ 223/12+135/(4m)+9/m².                 (D)
```

The improvement (A) subtracts an additional `δ` from the right-hand side of (D).
All of these arithmetic identities were checked independently of the supplied log.

## Passage to the supremum

For each finite family member, the hull gap is positive: independent binary rounding
at the interior point gives a strictly smaller expected value for each nonlinear
monomial than the common-threshold upper coupling. The coefficients are positive,
so these two feasible expected values are distinct.

The numerator in (C) and upper denominator in (D) are positive for `m≥9`. Dividing
therefore gives the claimed lower bound on each actual ratio. Taking arbitrarily
large multiples of nine yields

```
R(3) ≥ (161/4)/(223/12) = 483/223.
```

This only needs a convergent sequence of certified lower bounds. It does not assume
that the convex-envelope lower bound is exact, that the finite-member ratios equal
their displayed certificates, or that their actual ratios have a proved limit.

Using the uniform positive Bernstein margin instead gives

```
R(3) ≥ (161/4)/(223/12−901/120000)
     = 1610000/743033.
```

The new denominator is positive. The strengthened number is an immediate consequence
of the same independently checked certificates, rather than a new unverified
optimization result. The result's finite bound at `m=36`, `16985/8436>2`, was also
confirmed from (C) and (D).
