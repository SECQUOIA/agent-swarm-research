# Removing all upper constraints from the dense-box hardness construction

Date: 2026-09-05. Status: reviewed and integrated, with one redundant
auxiliary block removed, in
[the final result](../results/bilevel-scalar-leader-spd-box-np-completeness.md). This is a short extension of
[the dense-box theorem](bilevel-dense-box-hardness-investigation.md), with
its notation `rho,w_i,eta`, base variables `y`, and absolute-value
coordinates `p,q`.

Let the 3SAT instance have `m` clauses, each on three distinct variables.
For clause `a`, write `ell_a(y)` for the sum of its three continuous
literal values, and add one follower coordinate `v_a in [0,1]`. Put

```
xi=eta/(m+1).
```

Add the term

```
(xi/2) sum_(a=1)^m [v_a-1+ell_a(y)]^2                 (5)
```

to the follower objective (2). Keep the follower domain a pure unit box.
There are no upper constraints other than `x in [0,1]`. Use the affine
upper objective

```
F=n-sum_i(p_i+q_i)+2 sum_a v_a.                       (6)
```

**Candidate strengthened theorem.** The dense-box NP-completeness and
constant-gap conclusion remains valid with no upper constraints other
than the scalar leader bound. The lower domain is exactly
`[0,1]^(3n+m)`, its fixed Hessian is positive definite, and its linear cost
is affine in the leader. The objective with its leader-only term retained
is jointly convex. Every leader is feasible and has a unique follower.
The optimum is zero for satisfiable formulas and at least two otherwise.

## Conditional responses

Each added coordinate appears only in its own square. Therefore at every
full follower optimum,

```
v_a=clip_[0,1](1-ell_a(y))=max(0,1-ell_a(y)),
```

where the second equality uses `ell_a(y)>=0`. The existing exact formulas
for `p,q` are unchanged. Hence, on every follower response, with
`D(y)=sum_i min(y_i,1-y_i)`,

```
F=2D(y)+2 sum_a max(0,1-ell_a(y)) >= 0.               (7)
```

The full residual matrix, ordered by `(y,p,q,v)`, is block lower triangular
with diagonal blocks `L,I,I,I`; every weight is positive. Thus its follower
Hessian is positive definite. All residuals are affine in leader and
followers, so the complete square objective is jointly convex when its
leader-only term is retained.

## Boolean response preservation

At any Boolean vector `b`, choose `p=b`, `q=1-b`, and let `v_a` equal one
if clause `a` is false under `b`, and zero otherwise. This gives the exact
conditional minimizers. If a clause contains `k` true literals, its new
residual is zero for `k=0,1`, one for `k=2`, and two for `k=3`.

Each derivative of `ell_a` with respect to a base coordinate is zero or
`+/-1` because the clause has distinct variables. The absolute extra base
gradient contribution from (5) is consequently at most `2m xi<2eta` per
coordinate. Together with the previous `p,q` contribution, total feedback
opposing the base margin is less than `4eta`. The proven base margin is
strictly larger than `w_i/3^n>=w_n/3^n`, and

```
4eta=4rho w_n = w_n/(25*3^n) < w_n/3^n.
```

The strict box KKT signs at `y=b` are therefore preserved at its leader
`x_b`. The auxiliary coordinates obey their conditional optimum signs.
Strict convexity proves this full Boolean/auxiliary point is the unique
follower response. The assertion holds for every Boolean assignment,
regardless of whether it satisfies the formula.

## Gap and complexity

If the formula is satisfiable, take its satisfying vector and associated
leader `x_b`. Every clause shortfall is zero and `D(b)=0`, so `F=0`.

If it is unsatisfiable, round any follower base vector as in the earlier
proof. Some clause is false under the rounded bits. Each literal of that
clause equals the corresponding minority amount, and its three variables
are distinct. Therefore `ell_a(y)<=D(y)`. Equation (7) gives

```
F>=2D(y)+2 max(0,1-D(y))>=2.
```

This holds for every leader, since upper feasibility no longer imposes any
clause conditions. The constant unit-box follower domain guarantees a
response for every `x in [0,1]`; strict convexity and continuity give a
continuous response and an attained upper minimum.

All additional weights and coefficients have polynomial rational encoding
length, since `xi=eta/(m+1)`. The number of additional variables is `m`.
The original active-status argument for NP membership applies unchanged:
for a guessed follower box face, the unique free response is affine
rational in one leader coordinate, and the objective threshold plus KKT
conditions describe a rational interval.

Thus the earlier theorem can be strengthened without adding a new result
family: the upper-level constraint list can be empty. This modification
uses the same bounded quadratic feedback argument, together with a linear
penalty for clause shortfalls realized as exact boxed follower responses.
