# Supplied fixed-rank quadratic coupling permits exact cellwise LP

Date: 2026-09-05. Status: independently reviewed direct corollary of
[the reviewed fixed-aggregate response theorem](../results/bilevel-fixed-aggregate-response-algorithm.md),
with a simpler linear-programming proof in this quadratic specialization.
This is not presented as a separate novelty claim or as an algorithm for
finding a suitable diagonal-plus-low-rank decomposition.

The [independent proof review](review-bilevel-fixed-rank-quadratic-corollary.md) passed.

Fix leader dimension `r` and rank parameter `k`. Let the rational follower
Hessian have a supplied decomposition

```
Q=Diag(d)+U H U^T,
d_i>0,   U in Q^(N x k),   H=H^T in Q^(k x k),   Q positive definite.
```

For a leader `x` in a rational polytope `X subset [0,1]^r`, let the follower
uniquely minimize

```
(1/2)z^TQz+(c+C x)^Tz,   z in [0,1]^N.
```

The leader may impose any explicit rational affine constraints in `(x,z)`
and minimize a rational affine objective. Feasibility and, when feasible,
an exact rational global optimizer can be computed in polynomial time for
fixed `r,k`. There is no numerical bound on the coupling norm, coefficient
magnitudes, or condition number. The decomposition and positive definiteness
are part of the stated input assumptions.

Indeed introduce only the `k` aggregate coordinates `w=U^Tz`. At a follower
optimum, coordinatewise box KKT conditions are equivalent to

```
z_i=clip_[0,1](-(c_i+C_i x+U_i H w)/d_i).
```

The two clipping thresholds for each coordinate are affine hyperplanes in
`(x,w)`, a space of fixed dimension `r+k`. Enumerate their realizable sign
cells and use closed cells, including lower-dimensional cells and constant
thresholds. On each closed cell every displayed clipped function is a
specified affine function of `(x,w)`; formulas agree at clipping boundaries.
Impose `w=U^Tz` after these affine substitutions. All consistency equations,
leader constraints, and the objective are then linear in `(x,w)`.

Every feasible point of such a linear program gives a box-feasible vector
satisfying the complete follower KKT conditions. Since `Q` is positive
definite, that vector is the unique global follower optimum. Conversely,
every feasible leader-response pair lies in a clipping cell and satisfies
its consistency equations. Thus the finitely many LPs exactly cover the
bilevel feasible set, including leader constraints that involve the response.

For compactness one can explicitly impose

```
sum_i min(U_iell,0) <= w_ell <= sum_i max(U_iell,0).
```

These bounds follow from `w=U^Tz` and the unit box. Every nonempty cell LP
therefore has an attained rational optimum. There are `N^{O(r+k)}` cells;
standard fixed-dimensional affine arrangement enumeration, rational LP,
and rational substitutions have polynomial bit complexity. This gives
exact rational recovery directly, with no real-algebraic elimination.

The proof is a specialization of the fixed-aggregate theorem with
`phi(w)=(1/2)w^THw`. Low-dimensional multiplier cells for separable quadratic
optimization are classical; see the
[source comparison](bilevel-fixed-aggregate-response-novelty.md), especially
[Megiddo and Tamir (1993)](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf).
The cell argument and the use of a supplied low-rank coupling are not claimed
here as an independently new algorithmic principle.

Together with [near-identity hardness](../results/bilevel-well-conditioned-box-exact-hardness.md),
this distinguishes a fixed number of supplied aggregate interactions from
small interaction magnitude. Arbitrarily small unrestricted coupling can
retain exact hardness, whereas the stated fixed-rank decomposition permits
exact optimization even at large coupling magnitude. The hardness family
does not promise such a fixed-rank decomposition.
