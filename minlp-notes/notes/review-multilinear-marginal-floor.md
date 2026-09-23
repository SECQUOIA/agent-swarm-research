# Independent audit of the marginal-floor gap theorem

Date: 2026-09-04. Reviewer: common-factor audit agent, independent of the root author's proof.

Scope: [Sharp multilinear gap growth as the smallest mean approaches zero](../results/positive-multilinear-marginal-floor-gap.md), including the finite bound, exact marginal construction, asymptotic constant, lower examples, and normalized-mean extension to nonnegative boxes. The complete written proof passes this audit. Novelty is being screened separately.

## 1. Clipping and marginal completion

The density normalization is exact:

```
integral_0^1 1/[L(t+tau)] dt = 1.
```

For a high variable, its failure mean satisfies `0<=p<1/2`. Pointwise clipping therefore gives `0<=m_p<=p<1/2`; the completion denominator is positive, and its multiplier `(p-m_p)/(1-m_p)` lies in `[0,1]`. Integrating the completed probability gives

```
m_p + [(p-m_p)/(1-m_p)](1-m_p) = p.
```

The completion only increases each conditional failure probability. It includes zero failure means without exception. Conditional independence of the high-variable coins and the common uniform variable for all low means together define one globally consistent law; the construction does not require separate incompatible couplings for different terms.

The exponential union bound handles clipping correctly. If any untruncated conditional probability reaches one, its completed failure probability equals one, making the union certain. If none reaches one, the product of conditional nonfailure probabilities is at most the exponential of minus their sum, and that sum is at least `S h(t)`. It would be incorrect to substitute the sum of clipped probabilities for `S h(t)` without the saturated-coordinate case, but the draft explicitly separates that case.

## 2. Uniform hard-term bound

For a hard term, the anchor succeeds exactly on the interval `[0,u]`. Since `u>=delta`, the shifted cutoff after scaling time by `u` satisfies

```
tau/u <= B^(-2).
```

Writing `y=S/u`, concavity of `1-exp(-a y)` for `0<y<=1` and monotonicity for `y>=1` give the displayed normalized inequality. It is valid pointwise for every `a>=0`. Increasing the denominator shift decreases the integrand, so replacing `tau/u` by `B^(-2)` has the stated lower-bound direction.

This proves the same integral guarantee for every positive-gap hard term, irrespective of its degree, its failure means, or its anchor mean above the floor. Terms with `S=0` have zero gap and are correctly treated separately. No limit is taken over terms; the uniformity is established before the asymptotic argument.

The easy-term independent-rounding bounds are correct. In the final mixture, weighting the hard-term law by `1/I` and independence by `kappa` gives each class at least its full individual gap before division by the total mixture weight. Every omitted term contribution is nonnegative. This justifies summing arbitrary positive objective coefficients.

## 3. Integral asymptotics and leading constant

As the floor tends to zero, `B=ln(1/delta)` and

```
L = B+2 ln B+ln(1+tau) = B+2 ln B+o(1).
```

The upper integral estimate follows from removing the positive shift and using `1-exp(-a)<=min(1,a)`. For the lower estimate on `[1/L,1]`, the two bounds on `z+B^(-2)` are used in the correct directions: the first-order term is bounded below by `1/[L z(1+L/B^2)]`, while the negative second-order term is bounded below by `-1/(2L^2 z^2)`. Integrating gives exactly

```
I >= ln L/[L(1+L/B^2)] - (L-1)/(2L^2).
```

Since `L/B^2` tends to zero and the second term is lower order than `ln L/L`, the two bounds squeeze `I` to `(1+o(1)) ln L/L`. Taking the reciprocal and adding the fixed `kappa` therefore preserves leading constant one in the claimed upper bound.

For the lower construction, choose `ell=floor(log_2(1/delta))`. Then `2^(-ell)>=delta`, all anchor and leaf means meet the floor, and `ell` differs from `ln(1/delta)/ln 2` by less than one. The previously verified dyadic ratio `ell/log_2 ell` consequently has the required leading constant one. The passage from the dyadic sequence to every sufficiently small floor is valid.

## 4. Two-sided interiority and nonnegative boxes

The same asymptotic also holds if all unit-box means are required to belong to `[delta,1-delta]`. In the dyadic example, every anchor is at most `1/2`, while every leaf mean is `1-2^(-ell)<=1-delta`. For small `delta`, all anchors also satisfy the upper restriction and all leaves satisfy the lower restriction. Thus the existing lower example already lies in that strip; the floor-only upper bound applies to its smaller class.

The nonnegative-box extension is sound with the stated normalized means. After fixed coordinates are substituted, positive affine rescaling preserves their normalized floor and expands each original term into nonnegative unit-cube monomials. The full-function hull gap is unchanged under this coordinate bijection. The exact hull gap of a sum of subterms is at most the sum of their exact hull gaps, by the standard concave-majorant and convex-minorant inequalities. Therefore the expanded termwise gap bounds the original termwise gap from above. Unlike variable frequency, the marginal-floor parameter survives the expansion.

The statement must refer to normalized positions in the original box; a fixed positive numerical lower endpoint alone supplies no such condition. The draft makes this distinction explicitly.

## 5. Supplemental numerical checks

[The independent verifier](../code/audit-marginal-floor-coupling.py) passed 30 marginal-completion quadrature checks and 120 hard-term conditional-union checks, using floors from `1/2` through `1e-80`. It includes clipped and unclipped probabilities, zero failure probabilities, varying term degrees, and failure means on both sides of the anchor scale. It also checks the displayed finite integral estimates.

The completion integrals are evaluated after a logarithmic change of variable to resolve the narrow density near zero; hard-term integrals use time scaled by the anchor mean. These floating-point quadrature tests exercise the construction and complement the analytic proof. They are not exact-arithmetic certificates of the theorem or of its asymptotic limit.

No mathematical correction was needed. One minor definition clarification was sent to the author: define the positive-gap supremum for `0<delta<1`, and restrict the monotonicity sentence to `1/2<delta<1`, avoiding an empty positive-gap class at `delta=1`.
