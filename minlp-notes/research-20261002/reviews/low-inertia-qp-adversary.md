# Fresh adversarial review of convex-slab quadratic optimization

Date: 2026-10-02. Verdict: no blocking mathematical issue found.

Reviewed
[`convex-modulator-qp.md`](../new-direction/convex-modulator-qp.md),
including the bounded-polytope extension, against the supporting
core-refinement and rational-height arguments. The separate rational
spectral-normalization theorem is taken conditionally, as requested; this
review does not duplicate its active review. The exact polynomial-bit
convex-QP oracle is also used as the cited theorem, not independently
re-audited against its historical paper.

The independently reviewed Fenchel formulation is recorded separately in
[`negative-inertia-qp-review.md`](negative-inertia-qp-review.md).

## Slab lower bounds and pruning

For `A=P-T^T D T`, the displayed chord identity is correct:

```
F(x)-q_B(x) = (1/2) sum_i d_i(t_i-a_i)(b_i-t_i),  t=Tx.
```

On the feasible slab this lies between zero and
`delta_B=sum_i d_i(b_i-a_i)^2/8`. A minimizing convex-QP witness therefore
provides both a lower bound and an original-feasible upper bound within
`delta_B`. This remains true for lower-dimensional slabs and dependent
rows of `T`; empty slabs are separate infeasible states.

Pruning at `L_B>=U` is sound, including equality. After a later incumbent
improvement, an old discarded lower bound is still at least the new
incumbent. If the incumbent is strictly above the true optimum, every
currently generated cell containing an optimal projection has
`L_B<=F*<U` and survives. If the incumbent already equals the optimum,
the approximation inequality is automatic, and pruning every cell
certifies exactness.

The interval-width assertion also holds for every retained cell:
`U<=F(x_B)<=L_B+delta_B`, because its own witness was included in the
incumbent update. It is not necessary that the global incumbent come
from the cell attaining the smallest lower bound.

## Packing and parameter dependence

The retained witness inequality gives

```
||Tx_B-t*|| < h sqrt(k d/(4g)).
```

Thus the cell intersects that ball. Its projection onto each coordinate
axis intersects an interval of radius `R`, which can meet at most
`2R/h+4` intervals of the clipped uniform lattice. The bound
`(sqrt(k kappa)+4)^k` is safe, including closed boundaries, terminal
clipping, dependent projection rows, and a lower-dimensional image.
Each retained cell has at most `2^k` children.

The number of relaxations per level is consequently a function of
`k,kappa`, not a power of the input size whose exponent depends on `k`.
Each relaxation is a rational convex QP of uniform polynomial bit
complexity. Its coefficients contain the original data and dyadic grid
coordinates; their encoding length is polynomial in the original input
and the level index. Composing these polynomial bounds preserves an
absolute input exponent.

For general rational polytopes, the safe level statement is
`poly(I)+O(q)` rather than automatically the box section's literal
`O(I+q)`: projection-range endpoints are obtained by rational LP and have
uniformly polynomial encoding length. This distinction does not change
the stated FPT theorem. It was communicated to the parent as a minor
presentation clarification.

## Rational heights and exact recovery

The minimal-face height argument is valid on every nonempty bounded
rational polytope, including a lower-dimensional one. Choose an optimizer
whose smallest containing face has minimum dimension. It lies in that
face's relative interior. Its Hessian restricted to the face tangent
space is PSD. A nonzero null tangent direction has zero first-order and
second-order objective change and can be followed until a smaller face is
reached. Boundedness guarantees such an endpoint, contradicting the
choice. Thus the restricted Hessian is positive definite, with the
zero-dimensional case understood vacuously.

A direct computable denominator bound follows without an explicit tangent
basis. Let `E x=f` be independent active input rows defining the face's
affine hull. The optimizer and face multipliers solve

```
[ A  E^T ] [x]   [-b]
[ E   0  ] [v] = [ f].
```

This matrix is nonsingular: a homogeneous solution has `E x=0`; taking
the inner product of the first equation with `x` and using positive
definiteness on `ker E` gives `x=0`, and independence of the rows then
gives `v=0`. After clearing rational denominators, ordinary determinant
bounds give a uniform, computable polynomial-bit bound for the common
coordinate denominator. The objective denominator and the denominator of
`Tx` inherit polynomial-bit bounds. The face is used only in this proof;
the algorithm need not find or enumerate it.

When every optimizer has the same projection, the polynomial-height
optimizer just established supplies a height bound for that common
projection even if the original optimizer set contains a continuum.
Narrow-interval rational reconstruction of the optimum value is sound.
Projection reconstruction is also sound because candidate acceptance
requires a feasible slice optimizer with objective exactly equal to the
isolated optimum. An unsuccessful early candidate cannot be accepted.

Projected growth makes the incumbent projection close enough after
`poly(I)+O(log kappa)` levels. The algorithm never uses the growth
constant to prune, stop, or validate a candidate. Its role is solely in
the work and eventual-reconstruction bound.

## Unique projected optima imply qualitative growth

The finite-piece argument survives the move from boxes to polytopes.
For each fixed projection `t`, select a slice optimizer in a face of
minimum dimension. The Hessian is positive definite on the face tangent
space intersected with `ker T`, by the same feasible-null-direction
argument. On the affine consistency space of feasible `t`, constrained
stationarity then supplies a unique affine candidate. Requiring that
candidate to belong to the face gives a closed polytope; it is bounded
because `t=Tx` and the original polytope is bounded.

There are finitely many faces. Every slice optimizer has one of these
candidates, and each candidate value is a quadratic bounded below by the
global optimum. A piece attaining that optimum has the unique minimizer
`t*`. A piece not attaining it has a positive gap by compactness.

The supporting lemma that a quadratic with a unique minimizer on a compact
polytope has quadratic growth is correct, including lower-dimensional
domains. A sequence violating growth has normalized directions converging
to a nonzero direction in the closed polyhedral tangent cone. The exact
quadratic expansion forces zero directional derivative and nonpositive
quadratic curvature; feasibility of a short ray and optimality force zero
curvature. The entire short ray would then be optimal, a contradiction.
Singleton pieces impose no restriction on the growth constant.

Taking the minimum over finitely many positive piece constants proves the
qualitative claim. It supplies no useful quantitative lower bound by
itself and does not make the complexity dependence on conditioning
disappear.

## Targeted checks

Ran a separate inline exact-rational command, `python - <<'PY'`, on a
lower-dimensional polytope with a flat residual coordinate:

```
X = {(x,y,z): x=y, 0<=x<=1, 0<=z<=1},
F(x,y,z) = x^2-y^2/2-x/3+1/18,
T(x,y,z)=y,  P=diag(2,0,0),  D=[1].
```

The common optimal projection is the nondyadic value `1/3`, while `z`
is unconstrained by the objective. Nine slab levels and 17 exact convex
slab solves passed the chord-error, pruning, certified-interval, and
projected-growth inequalities. This specifically exercises the
lower-dimensional and nonunique-residual cases absent from a simple
unique full-vector example.

The same invocation tested Fenchel refinement and premature
reconstruction; those results are described in the companion review.
These checks support the formulas rather than prove the theorem. No
project-wide checks, CI inspection, or external literature search ran.

## Scope of the verdict

The theorem is for continuous rational QP with the stated supplied
decomposition or the separately certified spectral normalization. The
conditioning parameter remains essential. This review does not prove a
result parameterized by negative inertia alone, extend the convex oracle
to mixed-integer residual problems, establish practical solver speed, or
settle publication priority.
