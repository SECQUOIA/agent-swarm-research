# Independent review of the two-marginal cubic family

Date: 2026-09-04. Target:
[`results/positive-cubic-two-level-family.md`](../results/positive-cubic-two-level-family.md).
This is an independent agent review, not external peer review.

**Verdict:** The final family with limiting ratio `243/115` is correct. The scalar
minorant holds on the entire square, its two equality atoms give the exact scalar
convex envelope at the claimed mean, and both finite-family gap bounds hold for
every positive multiple of four. The conditional Bernoulli construction proves the
actual finite ratios converge to `243/115`; it does not merely give a sequence of
lower bounds with that limit. No mathematical issue remains in the reviewed proof.
The reviewer also obtained the exact `m=16` certificate below, reducing the simple
finite witness to 32 variables.

## Scalar identity and exact attainment

Independent symbolic expansion verifies

\[
ac^2+\frac54a^2-\frac{11}{6}a-\frac{20}{27}c+\frac{95}{108}
=\frac54\left(a-\frac{11-6c^2}{15}\right)^2
+\frac{(1-c)(3c-2)^2(3c+7)}{135}.
\]

Both terms are nonnegative for every real `a,c∈[0,1]`. The second term vanishes
only at `c=1` or `c=2/3`; the square then forces `a=1/3` or `a=5/9`, respectively.
Thus these are exactly the two equality points on the square. Assigning them
probabilities `1/4,3/4` gives mean `(1/2,3/4)` and expected value `16/27`.
The affine minorant has the same value at this mean. This proves the exact convex
envelope of the auxiliary scalar polynomial at the prescribed point.

The auxiliary polynomial contains repeated powers. Its scalar envelope is used
only to bound the normalized count polynomial. It is not being identified with a
termwise multilinear relaxation. The final proof preserves this distinction.

## Finite-family transfer

For two groups of `m` binary variables with counts `A,C`, the identity

\[
\frac{2}{m^3}\left[A\binom C2+\frac{5m}{4}\binom A2\right]
=F(A/m,C/m)-\frac{(A/m)(C/m)+(5/4)(A/m)}m
\]

was independently expanded exactly. Every binary coupling with the required
individual marginals has `E[A/m]=1/2` and `E[C/m]=3/4`. Since `ac≤a`, the expected
correction is at most `9/(8m)`, giving the stated lower bound on the convex envelope.
For a multilinear polynomial on a cube, vertex distributions suffice for both hull
envelopes: conditionally independent Bernoulli rounding at any fractional point
preserves every multilinear monomial and each coordinate mean. Thus restricting
this argument to binary couplings loses nothing.

All cubic terms have marginals `(1/2,3/4,3/4)` and all quadratic terms have marginals
`(1/2,1/2)`. Their individual lower envelopes are zero. Their individual upper
envelopes are `1/2`, attained simultaneously by a common threshold coupling.
Consequently both the scaled concave envelope and scaled termwise gap equal
`(9/8)(1−1/m)`. Subtracting the convex-envelope lower bound gives scaled hull gap
at most `115/216`.

For the reverse estimate, choose one of the scalar equality atoms, then sample all
coordinates conditionally independently with the atom's two probabilities. Every
monomial uses distinct coordinates, including within the quadratic term. Therefore
its expected product is exactly the corresponding conditional monomial, and the
scaled conditional polynomial expectation is `(1−1/m)F(a,c)`. This valid binary
coupling gives scaled convex envelope at most `(1−1/m)16/27`, hence scaled hull gap
at least `(1−1/m)115/216>0`. Divisions by the hull gap are therefore justified.

These two estimates prove the claimed ratio interval and convergence. The arithmetic
`(243/115)(19/20)=4617/2300>2` checks exactly. The requirement `4|m` ensures integral
coefficients; it is not needed by the envelope argument itself.

## Exact 32-variable witness found during review

Set `m=16`, so

\[
f=A E_2(W)+20 E_2(U),\qquad E A=8,\quad E C=12.
\]

Independent rational reconstruction followed by exact integer enumeration of all
`17²=289` count states verifies

\[
2f(A,C)-428A-177C+3372\ge0
\qquad(0\le A,C\le16,\ A,C\text{ integers}).
\]

For transparency, minimizing this integer residual over `C=0,…,16` for successive
`A=0,…,16` gives

```
540, 352, 204, 96, 28, 0, 9, 7, 0, 0, 19, 63, 132, 235, 369, 540, 742.
```

This is a finite exact certificate, not a floating-point feasibility check.
Its expectation gives `vex f≥214·8+(177/2)·12−1686=1088`.
Choose exactly eight coordinates in `U` and twelve in `W`, uniformly within each
group. This binary distribution has every required individual marginal and
constant objective
`8·binom(12,2)+20·binom(8,2)=1088`, proving equality.
The exact concave envelope and termwise gap are both `2160`, so

\[
\operatorname{chgap}f=1072,\qquad
\frac{\operatorname{tbtgap}f}{\operatorname{chgap}f}=\frac{135}{67}>2.
\]

The same exact count-envelope procedure gives ratios `27/16,21/11,99/50` at
`m=4,8,12`, respectively. Thus `m=16` is the first positive multiple of four in this
family whose exact ratio exceeds two. This is not a global minimal-dimension claim.

## Scope and earlier verified variant

Both distinct marginal values lie strictly inside `[0,1]`. Continuity of the finite
polyhedral envelopes and the strict gap ratio imply that sufficiently small upward
perturbations of the `1/2` marginals preserve a ratio above two. Thus examples also
exist with every coordinate marginal strictly above one-half. This argument gives
existence, not a quantitative perturbation radius.

The earlier parameter choice is also valid and is retained here as a checked
alternative: `F=ac²+(24/25)a²`, marginals `(1/2,4/5)`, and

\[
F-\left(\frac{41}{25}a+\frac45c-\frac{68}{75}\right)
=\frac{24}{25}\left(a-\frac{41-25c^2}{48}\right)^2
+\frac{(1-c)(5c-3)^2(5c+11)}{480}.
\]

Equality atoms `(1/3,1),(2/3,3/5)` with equal weights give scalar convex envelope
`83/150`. For `f_m=A E₂(W)+(24m/25)E₂(U)`, `25|m`, the same proof gives actual
ratio between `(33/16)(1−1/m)` and `33/16`. At `m=50` this yields the lower bound
`1617/800>2`. The final `243/115` construction is stronger and smaller.

This audit verifies mathematics and scope. It makes no independent claim that the
family or its factorization is absent from all published literature.


## Explicit homogeneous unit-coefficient corollary

The subsequent 52-variable corollary also passes independent review. Introduce
20 distinct variables `z₁,…,z₂₀` and define

\[
g=A E_2(W)+\left(\sum_{j=1}^{20}z_j\right)E_2(U).
\]

There are `16·binom(16,2)=1920` base cubic monomials and
`20·binom(16,2)=2400` padding cubic monomials. Their supports are distinct and
every coefficient is one. Thus this is a homogeneous cubic with exactly 4320
unit-coefficient monomials in 52 variables.

At padding marginals one, its gaps equal those of the 32-variable polynomial
exactly. At padding marginals `999/1000`, all 52 marginals are strictly inside the
cube. The base terms still have lower envelope zero, while every padding term has
marginals `(1/2,1/2,999/1000)` and hence lower envelope zero as well. All term upper
envelopes remain `1/2`, attained together by the common threshold coupling. Thus
`cav g=tbtgap g=2160` exactly.

For every binary coupling, pointwise comparison with the original polynomial gives

\[
0\le f-g=\left(\sum_{j=1}^{20}(1-z_j)\right)E_2(U)
\le120\sum_{j=1}^{20}(1-z_j).
\]

Its expectation is at most `120·20/1000=12/5`. The marginal law on `U,W` remains
feasible for the original convex-envelope problem, regardless of correlations
with the padding variables. Therefore `vex g≥1088−12/5=5428/5`, the hull gap is
at most `5372/5`, and

\[
\frac{\operatorname{tbtgap}g}{\operatorname{chgap}g}
\ge\frac{2700}{1343}>2.
\]

The denominator is positive: for example, any nonconstant base monomial has a
strict positive gap at these interior marginals, and its common-threshold maximum
exceeds its expectation under fully independent rounding. Positivity of the other
coefficients preserves that strict inequality. This finite construction needs no
probabilistic coefficient-removal theorem and no limiting dimension argument.
