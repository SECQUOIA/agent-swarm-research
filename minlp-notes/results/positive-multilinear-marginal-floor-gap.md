# Sharp multilinear gap growth as the smallest mean approaches zero

Date: 2026-09-04. Status: full proof passed two independent reviews; no unresolved mathematical issue identified. Novelty is provisional.

For 0<δ<1, let C(δ) be the supremum of the term-by-term gap divided by the convex-hull gap
for positive-coefficient multilinear polynomials on unit cubes, over all dimensions
and degrees and all points with every coordinate at least δ. Ratios are taken
where the hull gap is positive. Then

```
C(δ) ~ ln(1/δ) / ln ln(1/δ)       as δ decreases to zero.       (1)
```

Both leading constants are one. Thus keeping the evaluation point away from the
lower faces controls the gap independently of monomial degree. This is a bound
on the point at which the envelopes are evaluated, not a change to their box.

## A finite bound

For 0<δ<=1/2, define

```
B = max{2, ln(1/δ)},
τ = δ/B²,
L = ln((1+τ)/τ),
κ = 2/(1-exp(-1)),
I = integral_0^1 [1-exp(-1/[L(z+B^-2)])] dz.
```

Then I>0 and

```
C(δ) <= 1/I + κ.                                           (2)
```

For 1/2<δ<1, monotonicity gives the finite bound C(δ)<=C(1/2).
The proof uses one joint distribution for all terms at the given point, together
with independence. Neither distribution depends on the objective coefficients.

## Deficiencies and the easy terms

Discard affine terms, which have zero gap. For each monomial e choose an anchor
with smallest mean u and let S be the sum of the failure means 1-x_i over the
other variables in that monomial. Its termwise gap is T=min(u,S). For any
Bernoulli vector X with E X=x, its deficiency is

```
D_e = X_anchor - product_(i in e) X_i >= 0.
```

Positive monomials simultaneously attain their concave envelopes under a common
threshold distribution. Therefore the hull gap is the maximum expected weighted
sum of these deficiencies over all distributions with the prescribed means.

Call means at most 1/2 low and the others high. A term with exactly one low
variable is hard; its anchor is that low variable. Independence gives deficiency
at least T/κ to every other term. Indeed, for an all-high term,

```
E D_e >= u(1-exp(-S))
      >= u(1-exp(-1)) min(1,S)
      >= (1-exp(-1)) T/2.
```

For a term with at least two low variables, a nonanchor success mean is at most
1/2, so E D_e>=u/2>=T/2>=T/κ. These observations include zero-gap terms.

## A common density and exact marginal completion

On (0,1), put

```
h(t) = 1/[L(t+τ)].
```

The choice of L ensures that h integrates to one. Let U be uniform on (0,1), and
set each low variable to X_i=1[U<=x_i]. For a high variable with failure mean
p=1-x_i, define

```
q_p(t) = min{1, p h(t)},
m_p = integral_0^1 q_p(t) dt,
q'_p(t) = q_p(t) + [(p-m_p)/(1-m_p)] [1-q_p(t)].            (3)
```

Since 0<=m_p<=p<1/2, the denominator is positive and the coefficient in square
brackets belongs to [0,1]. Thus q'_p lies in [q_p,1] and integrates exactly to p.
This also covers p=0. Conditional on U=t, make all high-variable failures
independent with their respective probabilities q'_p(t). This gives one global
Bernoulli law with every required mean exactly correct.

For any collection of high variables whose failure means sum to S, their
conditional probability of at least one failure is at least

```
1-exp(-S h(t)).                                           (4)
```

If some p h(t)>=1, that variable has q_p=q'_p=1 and failure is certain. Otherwise
none of these probabilities is clipped, so q'_p>=p h(t), and the product bound
`product(1-q'_p)<=exp(-sum q'_p)<=exp(-S h(t))` proves (4).
The clipping case is essential; a bound on the sum of clipped probabilities
alone would not give the asserted exponential expression.

## A simultaneous guarantee for every hard term

For a hard term its low anchor succeeds when U<=u, where u>=δ. Applying (4),

```
E D_e >= integral_0^u [1-exp(-S/[L(t+τ)])] dt.              (5)
```

When S=0 the requested gap guarantee is zero. Otherwise change variables t=uz,
put y=S/u and ε=τ/u<=B^-2, and divide (5) by T=u min(1,y). For every a>=0,

```
[1-exp(-ay)]/min(1,y) >= 1-exp(-a),       y>0.             (6)
```

For 0<y<=1 this follows from concavity of y↦1-exp(-ay) and its zero value at
y=0; for y>=1 it follows from monotonicity. Applying (6) pointwise and then
using ε<=B^-2 yields

```
E D_e/T
 >= integral_0^1 [1-exp(-1/[L(z+ε)])] dz
 >= I.                                                   (7)
```

Thus the single distribution (3) gives at least I times every hard term's
individual gap, simultaneously. Mix this law with independence with weights
proportional to 1/I and κ. Hard terms and all other terms then each receive at
least T/(1/I+κ) expected deficiency. All extra contributions are nonnegative.
Summing with the positive coefficients proves (2).

## Asymptotic evaluation

As δ decreases to zero, B=ln(1/δ) tends to infinity and

```
L = B+2 ln B+o(1),        L/B² -> 0.
```

Since L>1, the upper estimate 1-exp(-a)<=min(1,a) gives

```
I <= integral_0^1 min{1,1/(Lz)} dz = (1+ln L)/L.
```

For a lower estimate, restrict the integral to z in [1/L,1] and use
`1-exp(-a)>=a-a²/2`. On this interval,
`z+B^-2 <= z(1+L/B²)`, while `z+B^-2>=z`. Therefore

```
I >= ln L/[L(1+L/B²)] - (L-1)/(2L²).
```

Both estimates imply I~ln L/L. Consequently (2) gives

```
C(δ) <= (1+o(1)) ln(1/δ)/ln ln(1/δ).                     (8)
```

## Matching lower bound

Use the dyadic construction in
[the positive multilinear gap result](positive-multilinear-gap.md).
With ell levels its smallest mean is 2^-ell, its other low means are 2^-j,
and its high means are 1-2^-ell. Its exact ratio is asymptotic to

```
ell / log_2 ell.
```

For a given sufficiently small δ, choose ell=floor(log_2(1/δ)). All means in
this construction are at least δ. Since ell differs from log_2(1/δ) by less
than one, this ratio is

```
(1-o(1)) ln(1/δ)/ln ln(1/δ).
```

Together with (8), this proves (1). The lower examples have unit coefficients.

The same sharp asymptotic holds if every mean must lie in the two-sided strip
`[δ,1-δ]`. In the chosen lower examples the smallest anchor is at least δ,
the largest anchor is 1/2, and each leaf failure mean is also at least δ.
Thus the examples already lie in that strip. The upper bound follows because
the strip is a subset of the original marginal-floor class. This is an
asymptotic assertion as δ decreases to zero, not an equality of the two
worst-case functions for every fixed δ.

## Nonnegative boxes and scope

The same upper bound applies on a finite box with nonnegative lower bounds when
every nonfixed coordinate has normalized mean `(x_i-l_i)/(u_i-l_i)>=δ`.
Expand each original monomial after the positive affine rescaling to the unit
cube. All expansion coefficients are nonnegative. The actual polynomial and
its hull gap are unchanged, while replacing each original term's exact hull
by the sum of its expanded subterm hulls can only increase the termwise gap.
Every expanded subterm still uses coordinates with means at least δ. Hence (2)
bounds the original, unexpanded termwise gap as well. Fixed coordinates are
substituted first. This expansion is legitimate for the marginal-floor
parameter; unlike frequency and incidence sparsity, that parameter is preserved.

The statement does not assert that a fixed positive lower box endpoint alone
bounds the gap uniformly over every point. Nor does it assert exact separation
or an optimization approximation guarantee for a constrained MINLP. It concerns
the scalar envelope-gap comparison at the stated points.

## Verification and novelty status

The [Lean verification package](../formal/topics/12-marginal-floor/README.md)
covers all 32 mathematical obligations in this note, including the finite
bound, sharp asymptotic, two-sided strip, and original-box extension. Its
[coverage map](../formal/topics/12-marginal-floor/COVERAGE.md) links the claims
to declarations. The warning-free build, transitive axiom audit, import
coverage, and kernel replay passed on 2026-09-17; see the
[verification record](../formal/topics/12-marginal-floor/VERIFICATION.md).

The [first independent review](../notes/review-multilinear-marginal-floor.md)
and [second independent review](../notes/review-multilinear-marginal-floor-second.md)
checked the marginal completion, clipping case, uniform integral bound,
matching lower sequence, two-sided strip, and box extension. Supplemental
high-precision numerical checks passed; the analytic proof is the certificate.

The [primary-literature screen](../notes/multilinear-marginal-floor-novelty.md)
found no matching sharp theorem. Fixed-δ finiteness is already an elementary
consequence of an O(1/δ) bound and is not a novelty claim. The proposed
contribution is the sharp logarithmic growth and leading constant one, obtained
with a correlated law that preserves the exact marginals. The search remains
qualified and does not certify publication priority.
