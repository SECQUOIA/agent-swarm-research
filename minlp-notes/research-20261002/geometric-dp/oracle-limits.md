# A point-oracle limit on conditioning dependence

Date: 2026-10-02. Status: elementary adversarial construction, derived and
checked by two research agents. This is a standard hidden-well black-box
argument, not a novelty claim or a lower bound for explicit polynomial
optimization. It complements the [geometric-grid theorem](theorem.md).

For fixed bag size `p`, point evaluations alone can require
`Omega_p((L/c)^(p/2))` queries, even at fixed accuracy, under the theorem's
coordinate-curvature and global quadratic-growth hypotheses. Thus its
conditioning exponent has a natural worst-case explanation in this oracle
model. This construction says nothing sharp about its logarithmic factors,
or about the best algorithm when explicit factor formulas are available.

Fix `D>0`, `0<r<=1/4`, and a point `z` whose radius-`r` ball lies in
`[0,1]^p`. Put

```
psi(t) = exp(-t/(1-t))    for 0 <= t < 1,
psi(t) = 0               for t >= 1,

f_z(x) = -D psi(||x-z||^2/r^2).
```

The function is smooth, has the unique minimizer `z` with value `-D`, and
is identically zero outside its open radius-`r` ball. All derivatives vanish
at the boundary of that ball. A single factor containing its `p` variables
has a supplied one-bag decomposition of width `p-1`.

For `0<=t<1`,

```
-log(1-t) = integral_0^t 1/(1-s) ds <= t/(1-t),
```

so `psi(t)<=1-t`. Therefore

```
f_z(x)-f_z(z)
  >= D min{||x-z||^2/r^2, 1}
  >= (D/p)||x-z||^2,                         x in [0,1]^p.
```

The last inequality uses `r^2<=p` and `||x-z||^2<=p`. Every member thus
has the same valid global growth constant `c=D/p`. Global here means on
the feasible cube. The bounded plateau cannot satisfy quadratic growth
on all of Euclidean space.

For an explicit upper coordinate-curvature bound, write `u=(x-z)/r` and
`t=||u||^2<1`. Differentiation gives

```
psi'(t)  = -psi(t)/(1-t)^2,
psi''(t) = psi(t)(2t-1)/(1-t)^4,

partial_ii f_z(x)
  = (D/r^2)[2 psi(t)/(1-t)^2
             - 4 u_i^2 psi(t)(2t-1)/(1-t)^4].
```

With `v=(1-t)^-1>=1`, the first term in brackets is
`2 e v^2 exp(-v)<=8/e`. For `t>=1/2`, the second term is nonpositive.
For `t<=1/2`, its positive contribution is at most

```
4 t(1-2t)/(1-t)^4 <= 8,
```

because `t(1-2t)<=1/8` and `(1-t)^-4<=16`. Hence the common bound
`L=12D/r^2` is valid everywhere, including at the smooth support boundary.
At the minimizer the coordinate second derivative is `2D/r^2`; the
curvature scale is genuinely inverse quadratic in `r`. The supplied
conditioning ratio is

```
kappa = L/c = 12p/r^2.
```

This scale does not result from deliberately loose supplied constants. A
farthest cube corner has squared distance at least `p/4` from `z`, lies
outside the ball, and has gap `D`. The largest valid growth constant is
therefore between `D/p` and `4D/p`, while the smallest valid upper curvature
bound is between `2D/r^2` and `12D/r^2`.

Let `m=floor(1/(2r))`. Choose candidate centers whose coordinates belong
to `{r,3r,...,(2m-1)r}`. Their `N=m^p` open radius-`r` balls are pairwise
disjoint and lie in the cube. Since `r<=1/4`,

```
N >= (4r)^-p = (kappa/(192p))^(p/2).
```

Give the algorithm the candidate set, `D,r,c,L`, and even the optimum value
`-D`. Hide only which candidate center is active. A query may return the
exact value, gradient, Hessian, any finite collection of derivatives, or
the entire derivative jet at its requested point. Every such answer is
zero outside the active ball, including on its boundary.

Fix `0<eps<D`. Any `eps`-optimal output must lie inside the active ball.
Follow a deterministic algorithm along the transcript consisting entirely
of zero answers. Each point query is in at most one candidate ball, and
its final output is in at most one further ball. If `q+1<N`, there is an
uninspected candidate whose ball contains neither a query nor the output.
Choosing it makes the entire transcript consistent with `f_z`, but the
output has objective gap `D>eps`. Consequently, every algorithm with a
uniform guarantee needs

```
q >= N-1 = Omega_p(kappa^(p/2))
```

in the worst case. The subscript `p` matters: the dimension-dependent
constants are displayed in the preceding packing inequality.

For a randomized algorithm with a cap of `q` queries, choose the hidden
center uniformly among the `N` candidates. For each fixed random seed,
there are at most `q` candidates whose ball is hit along the zero-answer
path, and at most one additional candidate on which the final output can
succeed without a hit. The average success probability is therefore at
most `(q+1)/N`. A success probability of at least `1-delta` on every
instance requires `q>=(1-delta)N-1`.

These assumptions allow suboptimal stationary plateaus. Quadratic growth
controls objective values relative to the global optimum; it does not
exclude such plateaus and is weaker in that respect than gradient conditions
that force every stationary point to be globally optimal. The construction
also shows why assuming knowledge of the growth constant alone does not
identify the basin.

The limit is specifically about point-oracle information. If the formula
above is supplied as explicit input, it reveals `z` directly. A region
range oracle or other additional structural information may also locate
the well cheaply. The argument therefore cannot be advertised as a lower
bound for arbitrary explicit polynomial factors, for practical solver
implementations, or for every sparse factor class. It does show that the
candidate theorem cannot generally replace its conditioning power by a
polylogarithm while keeping this oracle model and these hypotheses.

Verification: the derivative formulas, curvature inequalities, global
growth inequality, packing, and adversary were checked algebraically by
the author and a delegated reviewer. No numerical experiment, project-wide
verification, or CI inspection was used for this note.
