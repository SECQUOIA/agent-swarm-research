# Independent check: positive generalized powers can have an unbounded gap ratio

Date: 2026-09-04. This is an independent mathematical check of the proposed
two-term example. It is a scope obstruction, with no claim of novelty or external
peer review. The intended companion is
[generalized-monomial-gap-obstruction.md](generalized-monomial-gap-obstruction.md).

**Verdict:** the formulas and divergence are correct. Two positive power terms in
one original variable suffice, even with both exponents in `[0.5,1.5]` and the
fixed box `[1,3]`. Thus the positive multilinear degree theorem cannot simply be
extended to positive generalized monomials by replacing multilinear degree with
the largest exponent or the sum of exponents.

## Envelope calculation

Fix `0<ε<1` and define on `[1,3]`

```
g_−(x)=x^(1−ε),       g_+(x)=x^(1+ε),
f_ε(x)=g_−(x)+g_+(x).
```

The first term is strictly concave and the second strictly convex. For a continuous
convex univariate function on an interval, its convex envelope is the function
itself and its concave envelope is the endpoint chord. For a concave function,
the roles reverse. At the midpoint `x=2`, the width of the exact term-by-term
relaxation is therefore

```
T_ε = [2^(1−ε) − (1+3^(1−ε))/2]
    + [(1+3^(1+ε))/2 − 2^(1+ε)]
    = 3 sinh(ε ln3) − 4 sinh(ε ln2).
```

Both bracketed quantities are strictly positive, so `T_ε>0`.

Differentiation gives

```
f_ε''(x)
 = ε x^(−1−ε) [(1+ε)x^(2ε) − (1−ε)].
```

For `x≥1`, the expression in square brackets is at least `2ε>0`.
Consequently `f_ε` is strictly convex throughout the box. Its true graph-hull
width at the midpoint is precisely its chord error, not merely an upper bound:

```
H_ε = [f_ε(1)+f_ε(3)]/2 − f_ε(2)
    = 1 + 3 cosh(ε ln3) − 4 cosh(ε ln2) > 0.
```

The exact term-by-term formulation here retains the same original `x` in the two
term envelopes but imposes no coupling between their separate convex-combination
representations. Summing their interval widths is therefore the correct width
for that formulation. No recursive McCormick approximation is involved.

## Asymptotic constant

Write

```
A = 3 ln3 − 4 ln2 = ln(27/16) > 0,
B = 3(ln3)^2 − 4(ln2)^2 > 0.
```

For example, `ln3 > (3/2)ln2` follows from `9>8` and implies `B>0`.
The Taylor series of the hyperbolic functions yield

```
T_ε = A ε + O(ε^3),
H_ε = (B/2) ε^2 + O(ε^4),
T_ε/H_ε = (2A/B)/ε + O(ε).
```

The leading constant is

```
2A/B = 0.6159357483693755… .
```

Restricting the sequence to `0<ε≤1/2` keeps both exponents in `[0.5,1.5]` while
the ratio still diverges. The number of terms is exactly two, their coefficients
are exactly one, and their exponents are distinct for every member of the
sequence. At `ε=0`, the function is affine and both widths vanish, so that limit
point itself is not used to define a ratio.

## Numerical cross-check

The displayed asymptotic was checked directly at four values. To avoid subtracting
nearly equal constants in the denominator, the equivalent expression

```
H_ε = 6 sinh²((ε ln3)/2) − 8 sinh²((ε ln2)/2)
```

was used for the floating-point check.

| ε | T_ε/H_ε | ε T_ε/H_ε |
|---:|---:|---:|
| 0.5 | 1.435184292 | 0.717592146 |
| 0.1 | 6.200818465 | 0.620081846 |
| 0.01 | 61.597724317 | 0.615977243 |
| 0.001 | 615.936163321 | 0.615936163 |

These values corroborate the expansion; the derivative and Taylor arguments
above prove the result without numerical assumptions.

## Interpretation and limits

The mechanism is cancellation of opposite first-order curvature. Uniformly on
the fixed box,

```
x^(1±ε) = x ± ε x ln x + (ε²/2)x(ln x)² + O(ε³),
f_ε(x) = 2x + ε² x(ln x)² + O(ε⁴).
```

The separate envelopes charge the first-order concave and convex deviations;
those first-order deviations cancel in the summed function. This explanation is
an elementary expansion, not a novelty claim about curvature cancellation.

The example concerns convexification in the original variable `x`. Under the
change of variable `x=exp(y)`, both terms become convex exponentials on
`[0,ln3]`. Their separate chord errors then sum to the chord error of their sum,
so that particular transformed one-variable formulation has term-by-term ratio
one. The obstruction therefore does not assert weakness of every formulation
of a positive generalized-power model, or of its logarithmic formulation.
