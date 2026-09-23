# Minimum sampling gaps and finite-horizon spectral certificates

Date: 12 September 2026. Status: bound and helper accepted by fresh independent review; constrained
solver and certificate integration are under separate review.
The [independent review](research-20260912-noisy-markov-spacing-independent-review.md)
checks 22,734 exact models and independently enumerates 1,428 row-pricing
problems. This is an extension of the [reviewed noisy-Markov bound](research-20260912-noisy-markov-memory.md),
with no separate publication-priority claim. Minimum sampling gaps are a
practical restriction in the inspected kinetics measurement-design model.
The present result concerns a stationary scalar temporal covariance; it does
not assert that this temporal covariance was used in that source model.

## Setting

Write the observation covariance as
`R_ij=P*a^(abs(i-j))+r*1(i=j)`, where `P>=0`, `r>0` and `|a|<1`.
Only sets with consecutive selected times at least `g>=1` calendar positions
apart are feasible. Retain the same genuine local conditionals using all
selected observations in the previous `L` positions. Put `b=|a|` and
`kappa=P/(P+r)`. Covariance parameters remain fixed mean-parameter data.

The unrestricted theorem can be applied directly. A sharper bound uses this
spacing restriction twice: in each earlier residual's regression history,
and in the set of distances contributing to a residual covariance row.

## Local innovation floor

For a prediction variance `x<=P`, one observation followed by a transition
over `d` calendar positions gives the next prediction variance

```text
T_d(x)=P*(1-b^(2d))+b^(2d)*r*x/(r+x).
```

This function is increasing in `x`, and is nondecreasing in `d`. A local
history has at most `m=floor(L/g)` observations, each separated from the next
and from the target by at least `g`. Its first observation has unconditional
prediction variance `P`. Iteration of `T_g` from `P` decreases and stays in
`[0,P]`. Therefore every local target variance satisfies

```text
d_t >= d_* = r + T_g^m(P).
```

The last step remains true for fewer than `m` past observations because the
iteration decreases. This floor is rational for rational data; no Riccati
fixed-point approximation is required. The observation-gain bound remains
`kappa=P/(P+r)`, independently of this larger normalization floor.

## Residual-pair majorants

Take selected times `s<t`, let `h=t-s`, and use the residual-pair identity
from the original proof. Necessarily `h>=g`. For `h>L`, every earlier
history distance `d=s-j` is at least `g`, and the distances are `g` apart.
The nonincreasing weights `b^(2d)` have total no greater than their sum at
`d=g,2g,...,floor(L/g)*g`. Hence

```text
|Cov(Z_t,Z_s)| <= phi(h),
phi(h)=P*b^h*(1+kappa*sum_(j=1)^floor(L/g) b^(2gj)),  h>L.
```

For `g<=h<=L`, regression orthogonality removes the direct term and all
history observations at least `t-L`. The remaining distances lie in
`[max(g,L+1-h),L]` and remain `g` apart. With
`ell=max(g,L+1-h)`, the corresponding valid bound is

```text
phi(h)=P*kappa*b^h*sum_(d=ell,ell+g,...<=L) b^(2d).
```

This only maximizes a nonnegative bound on a pair covariance. It does not
assume that one selected set attains all these pair bounds simultaneously.
Absolute values permit negative transitions as in the original scalar proof.

## Exact row-bound pricing

Let `B(M)` maximize the sum of `phi(h)` over distances in `{g,...,M}` that
are at least `g` apart. Its elementary weighted interval scheduling recurrence
is

```text
B(M)=0                                    for 0<=M<g,
B(M)=max(B(M-1), phi(M)+B(M-g))             for M>=g.
```

At a fixed anchor `t` on the zero-based horizon `0,...,n-1`, selected distances
to its left and right satisfy those separate restrictions. Thus

```text
delta_(n,L,g) = max_(t=0,...,n-1) [B(t)+B(n-1-t)]/d_*
```

is a uniform absolute row-sum bound on the normalized residual covariance
minus identity. The same eigenvalue and congruence argument as in the original
proof gives

```text
(1-delta) R_SS^-1 <= Q_L(S) <= (1+delta) R_SS^-1
```

for every feasible selected set. Consequently the prior-aware logdet tangent
certificate remains valid when `delta<1`. This statement adds a constraint to
the feasible design family; a certificate using it is invalid if optimization
or incumbent validation drops that spacing constraint.

For `L>=n-1`, every local history is complete and the exact bound is zero.
For `g>=n`, feasible sets have at most one member and the bound is also zero.
These cases should be handled directly rather than through loose pair bounds.

## State count and implementation

Only separated masks can occur in a calendar graph. The number of valid
`L`-bit masks is

```text
1 + sum_(q=1)^ceil(L/g) binom(L-(g-1)*(q-1),q).
```

This counts placements after subtracting `g-1` compulsory empty positions
between consecutive set bits. A compact graph also needs enough memory to
enforce the next minimum gap: if `L<g-1`, add a cooldown state or retain
`max(L,g-1)` bits while calculating information from only the latest `L`.
Discarding this distinction would permit infeasible selections. Exact-count
layers and terminal conditions must also respect `k<=ceil(n/g)`.

`code/research_20260912/noisy_markov_spacing_bound.py` implements the rational
floor, pair majorants, row pricing and mask count. It does not yet implement
the constrained design oracle. The recurrence and combinatorial state count
are classical; their use here is intended to improve a conservative certificate
and exploit a real sampling restriction.
