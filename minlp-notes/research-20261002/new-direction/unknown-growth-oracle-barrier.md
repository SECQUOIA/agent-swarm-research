# Unknown-growth oracle obstruction with arbitrary optimal sets

Date: 2026-10-02. Status: independently checked argument and targeted exact
arithmetic checks. No external literature search or priority claim.

Even in one dimension, unknown quadratic growth toward an arbitrary optimal
set does not permit an instance-conditioned, polylogarithmic-accuracy
algorithm from pointwise smooth-function oracles alone. A deterministic
algorithm that is correct for every admissible objective must use
`Omega(eps^-1/2)` queries on the identically zero objective, whose
conditioning parameter can be one.

This is an algorithmic oracle lower bound. It is stronger than a limitation
of one grid certificate, but it is **not** a lower bound for explicitly
encoded rational quadratic programs.

## 1. Oracle model and admissible objectives

The domain is `[0,1]`. The algorithm receives the valid curvature bound
`L=1` and may query exact function values, first derivatives, and second
derivatives at adaptively chosen points. Each objective is globally `C^2`,
has `|f''|<=1`, and satisfies

```
f(x)-f* >= g dist(x,S)^2
```

for some positive, unknown `g`, where `S=argmin f`. The optimal set may be
nonunique. The algorithm must be correct for all such objectives; neither
`g` nor an upper bound on `kappa=max(1,L/g)` is supplied.

The base objective is `f0(x)=0`. Here `S=[0,1]`, so the growth inequality
holds with `g=1` and `kappa=1`. Every oracle answer is zero.

For rational `c,w` with `0<w<1/2` and `[c-w,c+w]` contained in `(0,1)`,
define the alternative

```
f_(c,w)(x) = -(w^2/6)(1-t^2)^3     if |t|<=1,
             0                    otherwise,
t=(x-c)/w.
```

This is a piecewise rational polynomial with a unique optimizer `c` and
optimum value `-delta`, where `delta=w^2/6`.

## 2. Smoothness and quadratic growth

Inside the support,

```
f'(x)=w t(1-t^2)^2,
f''(x)=1-6t^2+5t^4.
```

At both support endpoints, `f`, `f'`, and `f''` are zero. Thus the extension
by zero is globally `C^2`. For `|t|<=1`,

```
f''+4/5=5(t^2-3/5)^2>=0,
1-f''=t^2(6-5t^2)>=0.
```

Consequently `-4/5<=f''<=1`, so the supplied upper curvature is valid and
the gradient is globally 1-Lipschitz.

Inside the support, the objective gap is

```
f(x)-f* = delta[1-(1-t^2)^3]
        >= delta t^2
         = (x-c)^2/6
        >= delta (x-c)^2.
```

The first inequality follows from
`1-(1-t^2)^3-t^2=t^2(1-t^2)(2-t^2)>=0`; the last uses `w<=1`.
Outside the support the gap is `delta`, which is at least
`delta(x-c)^2` on the unit interval. Thus every alternative satisfies the
required growth condition with `g=delta>0` and valid parameter
`kappa=6/w^2`. No alternative violates the unknown-growth promise.

## 3. Lower bound on the flat instance

Run a deterministic algorithm on the zero objective until it stops after
`q` point queries. For an approximate-point guarantee, also include its
returned point among the query locations. These at most `q+1` points,
together with the interval endpoints, leave an open gap of length at least

```
1/(q+2).
```

If

```
q+2 < 1/(2sqrt(6eps)),
```

this gap has length greater than `2sqrt(6eps)`. Choose rational `w` strictly
between `sqrt(6eps)` and half the gap length, and choose rational `c` so
the closed support fits strictly inside the gap. Density of the rationals
permits both choices, even when the query locations are arbitrary reals.

All queried values and derivatives are then identical to the zero
transcript. Determinism gives the same future queries, stopping decision,
and output. The returned point lies outside the support, so its objective
gap on the alternative is

```
0-(-delta)=delta=w^2/6>eps.
```

The output therefore cannot be an `eps`-optimal point for both admissible
objectives. Correctness for the full class forces

```
q >= 1/(2sqrt(6eps))-2 = Omega(eps^-1/2)
```

on `f0` itself, despite its parameter `kappa=1` and dimension and bag size
equal to one.

The same argument applies to a certified objective interval of width at
most `eps`: the identical interval cannot contain both zero and
`-delta` when `delta>eps`. For an approximate scalar value with absolute
error at most `eps`, choose `delta>2eps`; only the constant changes.

For exact optimization, any finite zero transcript leaves a nonempty open
gap. A positive-width bump supported there produces the same transcript
but a different optimum and makes the unchanged returned point suboptimal.
Thus no such oracle algorithm can terminate after finitely many queries on
`f0` while guaranteeing exact optimization over the full class.

## 4. Consequence and limits

With requested accuracy `eps=2^-b`, the query lower bound is exponential
in `b` on an instance with `n=p=kappa=1`. Hence the proposed unknown-growth,
arbitrary-optimal-set extension cannot follow from the smoothness,
semiconcavity, and quadratic-growth oracle assumptions alone. A valid
supplied conditioning bound changes the class of indistinguishable
alternatives and is a material source of information.

The argument does not apply when the objective's explicit quadratic
coefficients are supplied. The alternatives are piecewise degree-six
functions; their hidden support is part of the oracle description.
It also does not cover an oracle that supplies certified range bounds or
other global information. The result here is deterministic; no randomized
lower bound is asserted.

## Targeted verification

An inline `python3 -` check using exact `fractions.Fraction` arithmetic
passed 1,604 second-derivative bounds, 1,604 growth inequalities, and 51
hidden-support transcript constructions. It also checked the matching
function, gradient, and Hessian values at support endpoints. These finite
checks support the displayed identities and indistinguishability proof.
No project-wide verification, CI inspection, or external search was used.
