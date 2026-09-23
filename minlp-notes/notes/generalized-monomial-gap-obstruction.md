# Positive power laws do not inherit the multilinear gap bound

Date: 2026-09-04. Status: elementary proof independently checked; see `notes/review-generalized-monomial-gap.md`. This is a
scope counterexample, not a publication-novelty claim. Cancellation of opposite
curvatures is a familiar reason why termwise convexification can be weak.

The sharp positive-multilinear theorem requires multilinearity. Positive
coefficients alone do not give a uniform ratio for generalized monomials,
even with one variable and two terms whose exponents stay bounded.

For 0<epsilon<1, take the interval [1,3] and

```
f_epsilon(x)=x^(1-epsilon)+x^(1+epsilon).
```

The first term is strictly concave and the second strictly convex. Their sum
is strictly convex, since

```
f_epsilon''(x)
 = epsilon x^(-1-epsilon)
   [(1+epsilon)x^(2epsilon)-(1-epsilon)] > 0
```

on this interval. Thus the exact convex envelope of the sum is the sum itself,
and its concave envelope is its endpoint secant. The individual term hulls
are likewise bounded by each term and its own endpoint secant, with opposite
orientations for the two terms.

At the midpoint x=2, the sum of the individual envelope widths is exactly

```
T_epsilon = 3 sinh(epsilon ln 3)-4 sinh(epsilon ln 2),
```

whereas the exact envelope width of the sum is

```
H_epsilon = 1+3 cosh(epsilon ln 3)-4 cosh(epsilon ln 2).
```

Strict concavity and convexity imply T_epsilon>0, and strict convexity of
f_epsilon implies H_epsilon>0. Taylor expansion at epsilon=0 gives

```
T_epsilon = (3 ln 3-4 ln 2) epsilon+O(epsilon^3),
H_epsilon = [3(ln 3)^2-4(ln 2)^2] epsilon^2/2
              +O(epsilon^4).
```

Both displayed leading coefficients are positive. For the first,
`3 ln 3-4 ln 2=ln(27/16)>0`; for the second, strict convexity of
`x (ln x)^2` on [1,3] gives its positive midpoint secant gap directly.
Consequently

```
T_epsilon/H_epsilon
 ~ [2(3 ln 3-4 ln 2)/(3(ln 3)^2-4(ln 2)^2)]/epsilon.
```

The ratio diverges as epsilon tends to zero. Choosing epsilon=1/k for integers
k>=2 keeps both exponents rational and in [1/2,3/2], with one variable, two
positive unit coefficients, and the same fixed positive interval throughout.
The divergence therefore does not require zero-domain endpoints, large
exponents, many terms, or many variables.

For process models involving real power laws, the positive-multilinear
relative-width theorem cannot be applied merely because all coefficients
are positive. This observation concerns envelopes in the original variable;
it does not rule out useful transformations or convex formulations of a
particular power-law model.

Under the change of variables x=exp(y), both terms become convex exponentials
on [0,ln 3]. Their convex envelopes are exact and their endpoint secants add,
so termwise and full widths coincide in that representation. The obstruction
is therefore explicitly tied to convexification in the original variable.
