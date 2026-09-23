# Independent audit of multilinear coefficient removal

Date: 2026-09-04. Reviewer: common-factor audit agent, independent of the coefficient-removal author and root derivation.

Scope: [Removing positive coefficients from worst-case multilinear gap ratios](../results/positive-multilinear-coefficient-removal.md), including the homogeneous blow-up lemma, homogenization/interior reduction, and the finite 25,000-coordinate cubic existence bound. The written argument passes this audit. This is a correctness review, not a novelty certification.

## 1. Homogenization and continuity

Removing affine terms preserves both gaps. Once all remaining monomials have degrees between two and `d`, `d-2` new padding variables suffice: append the first `d-k` to a degree-`k` monomial. New variables are distinct from the original ones, so the resulting monomials remain squarefree. Distinct original supports remain distinct after padding, including when their original degrees differ.

At padding marginals equal to one, every representing binary distribution fixes these variables at one almost surely. The full envelopes therefore reduce exactly to the original envelopes. The single-monomial upper bound and Fréchet lower bound reduce in the same way, so the termwise gap is also unchanged.

The convex and concave envelopes of a fixed multilinear polynomial are the lower and upper boundaries of the convex hull of its finitely many binary-vertex graph points. On the cube these are continuous piecewise affine functions. Thus both gaps are continuous, and their ratio is continuous wherever its denominator is positive. Perturbing all coordinates into the interior preserves any strict target-ratio inequality when the perturbation is small enough. This proves equality of suprema; it does not assert exact preservation of a boundary ratio at a particular interior point.

Scaling by the largest positive coefficient does not change the ratio and places all included coefficients in `(0,1]`. No zero-probability terms need be treated as included monomials.

## 2. Cloning preserves the two envelopes exactly

For a homogeneous degree-`d` multilinear polynomial, substituting averages of `m` clones and multiplying by `m^d` produces exactly `m^d` clone monomials per original monomial, each retaining the original coefficient. Clone groups correspond to distinct original variables. Therefore each expanded term is squarefree, different clone choices give different supports, and terms from different original supports cannot collide. The original polynomial must be understood with equal supports already collected, as the draft explicitly requires.

The envelope argument proves equality of the entire feasible expectation intervals. An arbitrary binary clone distribution yields random group averages in `[0,1]^n` with the prescribed original means. Conditional independent Bernoulli rounding of those averages preserves the expected original polynomial by multilinearity. Conversely, setting all clones in a group equal to the original binary variable embeds every original distribution in the clone model. Neither direction assumes that clones from the same group are independent.

Every cloned monomial has the same list of marginal values as its source monomial. Its exact termwise gap is consequently identical, and summing over the `m^d` copies proves the stated scaling. Homogeneity is required for this common scale; the earlier padding step correctly supplies it.

## 3. Random thinning and simultaneous errors

After normalization, independent Bernoulli retention with each source coefficient as its probability has the required expected polynomial. There are `s m^d` distinct random indicators. At any fixed binary vertex, the summand range lengths are at most one. Hoeffding therefore gives the stated exponent `-2t^2/(s m^d)`.

The termwise gap at the repeated evaluation point is a separate weighted sum of the same indicators. Each fixed single-monomial gap lies in `[0,1]`, so the same concentration bound applies. These two events need not be independent; their probabilities are combined by a union bound. Reusing the indicators in both sums causes no problem.

The union covers exactly `2^(nm)` binary vertices plus one termwise-gap event. With `t_m=K m^((d+1)/2)`, its failure bound is

```
2(2^(nm)+1) exp(-2K^2 m/s).
```

The condition `K^2>s n ln(2)/2` makes this tend to zero. Here `n,s,d` and the original polynomial are fixed before `m` grows, as needed by the proof. Since `d>=2`, the normalized error `t_m/m^d` tends to zero. There is no corresponding argument for affine degree one, whose gap ratio is not the object being studied.

Uniform error on the binary vertices bounds each full envelope error by `t_m`, because all feasible expectations are probability-weighted vertex sums. The hull-gap error is at most `2t_m`. No claim about preserving an optimal representing distribution is needed.

The original hull gap is explicitly assumed positive. Hence sufficiently large successful samples also have positive hull gap, and their ratios converge. This establishes equality of the dimension-free suprema. It does not establish equality at fixed dimension, preservation of a maximum, a small construction, or an efficient certification algorithm for a sampled polynomial. The draft correctly distinguishes these claims.

## 4. Exact checks of the finite cubic bound

The source homogeneous example has 25 coordinates, 464 monomials, coefficients at most 13, termwise gap `943`, and hull gap at most `80947/175`. Consequently

```
T_0-2H_0 >= 3131/175.
```

With `m=1000` and `t=m^3/10`, Hoeffding gives

```
2t^2/(464m^3) = m^3/23200.
```

The displayed union bound is less than one. Even replacing `ln(2)` by one gives the exact upper bound

```
(25m+2)-m^3/23200 = -524942/29 < 0
```

on its logarithm. The error allowance in the strict inequality is `5t`: one `t` from the termwise-gap estimate and twice `2t` from the hull-gap estimate. Its remaining normalized margin is exactly

```
3131/2275 - 1/2 = 3987/4550 > 0.
```

These rational identities were independently checked with exact arithmetic.

The resulting strict inequality ensures that the polynomial is nonempty. For a nonempty positive homogeneous polynomial of degree at least two at an interior point, the hull gap is positive: the common-threshold coupling attains the concave envelope `sum_e a_e min_{i in e} x_i`, while the actual graph value is `sum_e a_e product_{i in e} x_i`, strictly smaller term by term. Therefore the strict inequality does imply a well-defined ratio above two.

The 25,000-coordinate conclusion is a finite probabilistic existence certificate. The proof neither generates a retained support nor verifies a particular sample. The potentially enormous candidate monomial set is stated explicitly, and the note correctly retains the smaller weighted examples as the explicitly listed certificates.

## 5. Scope

The proof uses positive coefficients, squarefree monomials, degree at least two, and freedom to increase dimension. The nonnegative-box extension invokes the earlier positive-expansion comparison, rather than claiming cloning directly preserves an original nonunit-box relaxation. Arbitrary signed boxes, fixed-size formulations, and deterministic polynomial-time support construction are not covered.

No mathematical correction was needed. Minor prose spacing and an optional explicit positive-denominator justification were sent to the author.
