# A fractional-power law restores an exact arc-flow arithmetic barrier

Date: 2026-09-05. Status: passed [independent proof review](../notes/review-potential-flow-fractional-power-arc.md). A [separate bounded source audit](../notes/potential-flow-fractional-power-arc-novelty.md) found no matching precise theorem, while crediting known arithmetic concerns. This is an exact arithmetic lower bound, not NP-hardness; novelty remains provisional.

The reviewed [exact arc-capacity theorem](potential-flow-exact-arc-capacity.md)
uses polynomial edge laws. Its proof cannot automatically be extended to
algebraic fractional powers. Already the fixed common law

```
pi_i-pi_(i+1)=beta_i phi(x_i),
phi(x)=sign(x)|x|^(3/2),       beta_i>0,
```

on a single cycle with fixed rational nominations has Square-Root-Sum-hard
exact arc-capacity comparison. This law is continuously differentiable,
strictly increasing, and zero at zero. No resistance uncertainty is needed.

## Reduction

Take a Square-Root-Sum instance of positive integers `a_1,...,a_N` and a
positive integer threshold `K`, asking whether `sum_i sqrt(a_i)<=K`.
The trivial zero-threshold and zero-radicand cases can be handled directly.
One- and two-term input-size edge cases can be decided directly or padded
by fixed unit radicands and the corresponding increase in `K`.

Use an oriented simple cycle with `N+1` edges. Let

```
c_i=a_i, beta_i=1/a_i           (i=1,...,N),
c_(N+1)=-1, beta_(N+1)=K.
```

Prescribe each vertex's injection as its outgoing `c` minus its incoming
`c`, so the nomination vector is integral and balanced. Conservation
then represents every possible flow as `x_i=c_i+z`, with one scalar
circulation `z`. The physical cycle equation is

```
h(z)=sum_(i=1)^(N+1) beta_i phi(c_i+z)=0.
```

The continuous function `h` is strictly increasing and has limits of
opposite infinite sign at the two ends of the real line. It therefore
has a unique root `z*`, which supplies the unique physical flow and
consistent node potentials. At zero,

```
h(0)=sum_i (1/a_i) a_i^(3/2)-K
    =sum_i sqrt(a_i)-K.
```

Strict increase gives

```
sum_i sqrt(a_i)<=K
  iff h(0)<=0
  iff z*>=0
  iff x_(N+1)>=-1.
```

Thus one rational lower arc-flow capacity tests the original exact
comparison. Reversing the objective arc's orientation converts this to
a rational upper capacity `-x_(N+1)<=1`, if an upper-only convention is
preferred. All coefficients and nominations have polynomial binary
encoding length. The graph has maximum degree two, treewidth two, and
one block of cycle rank one.

Because the nomination and resistance scenario is a singleton, the same
reduction applies to robust capacity validation with degenerate uncertainty
boxes. It does not require optimizing over uncertain loads.

## Optional integer-resistance version

Let `A=prod_i a_i`, which has polynomial binary encoding length. Multiply
every resistance by `A`: use `beta_i=A/a_i` and `beta_(N+1)=AK`.
Every resistance is now a positive integer, and the cycle equation is
scaled by the common positive constant `A`, preserving its root. Thus
the reduction also has integral resistances and nominations. The rational
capacity remains the constant `-1` (or `1` after reversal).

## Interpretation and limits

This result explains a concrete boundary of the polynomial-law exact
algorithm. For a fractional power, testing a circulation at one rational
threshold may already require comparing a sum of independent radicals.
The bounded cycle rank does not remove that arithmetic issue.

No converse reduction for arbitrary fractional-power instances is claimed,
so the current statement is Square-Root-Sum-hardness, not completeness.
No claim is made about polynomial additive approximation, strong hardness,
or hardness under fixed small-magnitude nominations. The polynomial-law
exact arc theorem and its dense piecewise-polynomial extension remain
unaffected.

Independent review checked the injection sign convention, capacity
direction, uniqueness, simple-cycle padding, and bit lengths. Its separate
checker passed 103 small-cycle tests, including equality cases and common
resistance scaling. The source audit distinguishes this precise reduction
from established warnings about power-law arithmetic and earlier exact
cycle results under different constitutive assumptions.


## Other fixed rational powers with even denominators

The independent review also verified the same obstruction for every fixed
reduced exponent `p/q>1` with even `q`. Coprimality makes `p` odd. Replace
the positive-edge data by

```
c_i=a_i^(q/2),       beta_i=a_i^(-(p-1)/2).
```

For `phi(x)=sign(x)|x|^(p/q)`, each positive contribution at zero is
`beta_i phi(c_i)=sqrt(a_i)`. Keep the last `c=-1,beta=K`. Since the
exponent is fixed, all rational data still have polynomial encoding length.
Multiplying by a common positive integer clears the resistance denominators.
The same capacity equivalence follows. This is a fixed-law statement,
not an algorithm taking arbitrary binary-encoded exponents.
