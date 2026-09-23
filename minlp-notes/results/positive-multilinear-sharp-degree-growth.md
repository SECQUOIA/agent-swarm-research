# Sharp asymptotic degree dependence of positive multilinear relaxation gaps

Date: 2026-09-04. Status: full theorem, leading constant, dimension interpolation, and nonnegative-box extension independently audited by two reviewers; no unresolved mathematical issue identified. This sharpens the logarithmic degree bound and matches the asymptotic lower bound in the multiscale counterexample. The new ingredient is a harmonic conditional-failure coupling.

Lean extension (2026-09-12): the [sharp growth package](../formal/topics/09-sharp-multilinear/README.md)
formalizes both leading-constant-one limits, full nonnegative-box transfer
(including fixed coordinates), and exactly-n dimension. Its finite harmonic
certificate uses `1/(1+1/b^2)` instead of the Taylor factor below. The
asymptotic conclusions are the same; the displayed finite constant 24 and
later optimized fixed-point/second-order certificates are not asserted as
formally verified. See the package's [coverage](../formal/topics/09-sharp-multilinear/COVERAGE.md).
The [focused paper](../paper-multilinear-gap/README.md) states and proves the
verified finite certificate explicitly; its September 16 completion also
covers the supporting envelope results and actual lower-family asymptotics.

## Theorem

Let f(x)=sum_e a_e product_(i in e)x_i on [0,1]^n, with a_e>=0 and maximum monomial degree d>=2. Put

```
L=max{16,1+ln d},       c=1-exp(-1).
```

Then, at every point of the box,

```
tbtgap_f(x) <= [24 L/(c ln L)] chgap_f(x).                 (1)
```

Consequently, if R(d) is the supremum of the term-by-term/convex-hull gap ratio over all dimensions, positive-coefficient polynomials of degree at most d, and points with positive hull gap, then

```
R(d) ~ ln d/ln ln d as d tends to infinity.               (2)
```

The stronger asymptotic equivalence (2), including leading constant one, follows from the refinement below. The upper bound uses only three explicit distributions on binary vertices with the prescribed means. It is a relaxation-strength theorem, not an algorithm for evaluating the exact convex envelope.

## Deficiencies and easy terms

Affine terms do not affect either gap. For each remaining monomial choose an index r(e) minimizing its coordinate, and write

```
u_e=x_(r(e)),
S_e=sum_(j in e without r(e))(1-x_j),
T_e=min{u_e,S_e}.
```

The term-by-term gap is sum_e a_e T_e. For a binary random vector X with E X=x, define

```
D_e(X)=X_(r(e)) 1{some X_j=0 for j in e without r(e)}.
```

Then E D_e=u_e-E product_(i in e)X_i>=0, and positivity gives

```
chgap_f(x)=max_(E X=x) E sum_e a_e D_e(X).                 (3)
```

Indeed, nested Bernoulli variables attain all monomial concave envelopes simultaneously, and the multilinear convex envelope is the minimum expected value over binary-vertex distributions of mean x. Details appear in [the preceding degree bound](positive-multilinear-degree-upper-bound.md).

Call a coordinate low if x_i<=1/2, and high otherwise. Under independent Bernoulli rounding, every monomial with at least two low coordinates has deficiency at least T_e/2. For an all-high monomial, u_e>1/2 and

```
u_e(1-product_(j!=r(e))x_j)
 >=c u_e min{1,S_e}>=(c/2)T_e.
```

Here 1-z<=exp(-z) and 1-exp(-s)>=c min{1,s}. Independence thus handles every term except those with exactly one low coordinate. Deficiencies are nonnegative under every coupling, so distributions may be combined without subtracting losses on other terms.

## Two couplings for terms with one low coordinate

Set M=exp(L-1), so M>=d and 1+ln M=L. Both couplings below use a uniform random variable U on (0,1). Every low coordinate is X_i=1[U<=x_i]. For a high coordinate let p_i=1-x_i, with 0<=p_i<1/2.

**Threshold coupling.** Each high coordinate fails exactly when U<=p_i. Its failure probability is p_i, so all means are correct.

**Harmonic coupling.** If p_i=0, set X_i=1. Otherwise define

```
h_i=min{M p_i,1},
a_i=1+ln(h_i/p_i)=1+ln min{M,1/p_i},
q_i(t)=(1/a_i)min{1,p_i/t}1{t<=h_i},   0<t<1.
```

Conditional on U=t, let the high coordinates fail independently with probabilities q_i(t). Since a_i>=1, these are valid probabilities. Their integrals are

```
int_0^1 q_i(t)dt=[p_i+p_i ln(h_i/p_i)]/a_i=p_i.
```

Thus all means are correct. For active coordinates, meaning t<=h_i, the bound a_i<=L implies

```
q_i(t)>=(1/L)min{1,p_i/t}.                                (4)
```

Each coupling is defined once from the entire marginal vector and the degree bound, independently of which monomial is evaluated.

## The harmonic gain estimate

Fix a monomial with one low anchor of marginal u<=1/2. Write p_1,...,p_r for its high-coordinate failure marginals, where r<=d-1, and put

```
S=sum_j p_j,       T=min{u,S},       p_max=max_j p_j.
```

The case T=0 is immediate. Suppose T>0.

If p_max>=T/sqrt(L), the threshold coupling has deficiency

```
min{u,p_max}>=T/sqrt(L)>=T ln L/L.                        (5)
```

The last inequality follows from ln L<=sqrt(L) for L>=1: the maximum of ln t/sqrt(t) over t>=1 is 2/e<1.

Otherwise p_max<T/sqrt(L). Consider t in [T/sqrt(L),T/2]. This interval is contained in (0,u), and L>=16 makes it nonempty. All p_j<t. A coordinate is active in (4) precisely when p_j>=t/M, because t<1. The total of inactive failure marginals is at most r t/M<=t. Hence

```
sum_(j active)p_j>=S-t>=S-T/2>=S/2>=T/2,
sum_j q_j(t)>=(1/(Lt))sum_(j active)p_j>=T/(2Lt).
```

By conditional independence,

```
P(some high coordinate fails | U=t)
 >=1-exp(-sum_j q_j(t))>=c T/(2Lt).
```

The last step uses T/(2Lt)<=1/(2sqrt(L))<1. The low anchor is active throughout this interval, so the harmonic coupling has deficiency at least

```
int_(T/sqrt(L))^(T/2) cT/(2Lt)dt
 =cT/(4L)[ln L-2ln2]>=cT ln L/(8L).                      (6)
```

The final inequality holds because L>=16. Equations (5)-(6) show that the sum of the threshold and harmonic deficiencies is at least cT ln L/(8L) for every term with exactly one low coordinate.

## Completing the upper bound

Take the uniform mixture of independence, the threshold coupling, and the harmonic coupling. All components have mean x. Independence supplies at least cT_e/2>=cT_e ln L/(8L) for its two easy classes; the other two couplings supply that bound in sum for the remaining class. Every omitted contribution is nonnegative. The mixture therefore has deficiency at least

```
cT_e ln L/(24L)
```

for every monomial. Multiplying by nonnegative coefficients, summing, and applying (3) proves (1). QED.

## Refinement: the optimal leading constant is one

The harmonic family also gives the sharper asymptotic upper bound needed for (2). In this subsection choose

```
L=max{exp(6),1+ln d},     M=exp(L-1),
b=ln L,                 a=L/b^2,        beta=1/b,
h=[(1-1/b)(1-1/(2b^2))(b-3ln b)]/L.
```

Use exactly the same threshold and harmonic coupling definitions with this value of M. Here b>=6, a>1, and h>0. To verify positivity, b-3ln b is increasing for b>=6, and its value at six is positive because ln6<2.

For a unique-low term with T>0, if p_max>=T/a, threshold rounding gives deficiency at least T/a. Otherwise integrate harmonic deficiency over

```
T/a <= t <= beta T.
```

The interval is nonempty because its endpoint ratio beta a=L/b^3 has logarithm b-3ln b>0. It lies in (0,u), and every p_j<t. As before, inactive marginals total at most t, so the active sum is at least S-t>=(1-beta)T. The sum of the conditional failure probabilities is therefore at least

```
z(t)=(1-beta)T/(Lt).
```

On this interval, z(t)<=a/L=1/b^2. Even if the actual sum of failure probabilities is larger, monotonicity permits use of this lower bound. Since 1-exp(-z)>=z-z^2/2,

```
P(some high coordinate fails | U=t)
 >=[1-1/(2b^2)](1-beta)T/(Lt).
```

Integration gives harmonic deficiency at least hT.

Now set Z=1/h+a+2/c, and mix the three distributions with probabilities

```
harmonic: (1/h)/Z,
threshold: a/Z,
independent: (2/c)/Z.
```

These probabilities are positive and sum to one. A monomial in an easy class gets deficiency at least T/Z from the independent component. Every other monomial gets at least T/Z from the threshold or harmonic component according to its case. Thus

```
R(d)<=Z=1/h+a+2/c.                                      (7)
```

As d tends to infinity, L~ln d and b~ln ln d. Moreover,

```
h~b/L,      a=L/b^2=o(L/b),      2/c=o(L/b).
```

Therefore R(d)<=(1+o(1))ln d/ln ln d. The optimized mixture is important: equal mixture weights would lose a constant factor. QED.

## Matching the degree lower bound

The [dyadic counterexample](positive-multilinear-gap.md) with m=2^ell leaves has maximum degree d_ell=2^(ell-1)+1 and exact ratio asymptotic to ell/log_2 ell, hence asymptotic to ln d_ell/ln ln d_ell. For arbitrary sufficiently large degree allowance d, take the largest ell with d_ell<=d. Then d_ell and d differ by at most a constant factor. Monotonicity of R(d) transfers the asymptotic lower bound with leading constant one to every sufficiently large d. Combining with (7) proves (2).

The lower-bound family uses unit coefficients and fewer than twice as many monomials as variables. The upper bound permits arbitrary nonnegative coefficients and any number of variables and monomials.

## Dimension growth and finite nonnegative boxes

Let C(n) be the worst ratio among positive multilinear polynomials on n variables, with no degree restriction beyond multilinearity. Since d<=n, the upper bound gives C(n)<=(1+o(1))ln n/ln ln n. For the lower bound choose the largest dyadic example with 2^ell+ell<=n and add unused variables if necessary. Its dimension differs from n by at most a constant factor, so

```
C(n) ~ ln n/ln ln n.
```

The same degree upper bounds apply on any finite box with nonnegative lower bounds, comparing the original unexpanded term-by-term relaxation. After deleting fixed coordinates and making the coordinatewise affine map to the unit cube, each original monomial expands as a sum of positive monomials of no larger degree. For that sum, simultaneous comonotone attainment makes its concave envelope the sum of the expanded concave envelopes, while its convex envelope is at least the sum of the expanded convex envelopes. Hence the original monomial's gap is at most the sum of the expanded monomial gaps. Summing over original monomials gives original tbtgap<=expanded tbtgap; the full-function hull gap is unchanged by the coordinate transformation. Apply (1) or (7) to the expanded positive polynomial. A detailed independently checked version of this comparison is in [the preceding degree-bound note](positive-multilinear-degree-upper-bound.md).

## Verification and novelty status

A later [finite harmonic-coupling bound](positive-multilinear-second-order-upper.md) retains the complete deficiency curve and tunes the cutoff. It improves the upper certificate to N/[ln N−ln ln N+o(1)]+2/(1−e^−1), where N=1+ln(d−1), while preserving the sharp leading constant proved here.

The leading-constant result was developed jointly by the new-directions and multilinear agents. The full written upper proof, matching lower interpolation, and box extension passed two independent audits: [the first review](../notes/review-positive-multilinear-sharp-upper.md) and [the second review](../notes/review-positive-multilinear-sharp-upper-second.md). [The root review](../notes/review-positive-multilinear-sharp-root.md) also passed. The lower-bound construction was separately audited. The [dedicated literature screen](../notes/positive-multilinear-degree-novelty.md) is complete; novelty remains provisional.

Coordinates zero or one are covered by zero deficiencies and the explicit p_i=0 convention. The nonnegative-box extension above includes the necessary comparison with the original unexpanded term-by-term gaps.
