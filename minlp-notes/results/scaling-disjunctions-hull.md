# Convex hulls of scaling disjunctions: integer multiplicities and discrete sizes with shared intensive variables

Status: independently agent-reviewed and corrected 2026-09-04. The original Theorem 4 was
false and has been replaced by a counterexample and restricted results. Theorems 1–3 and 5
are elementary hull identities; no publishable novelty is established. A separate agent
reviewed the replacement Theorems 4A and 4B; see `notes/audit-scaling.md` and
`notes/review-scaling-characterization.md`.

## Motivation

Process models routinely contain a *scale* decision that multiplies extensive quantities
without changing intensive ones: the number `n ∈ {0,…,N}` of identical parallel units (parallel
reactors, membranes, compressors, trains, modular skids), or the size `s` of a unit chosen from a
catalogue `{s_1,…,s_K}` of standard sizes, where the unit model is scale-invariant (throughput,
area, duty, cost scale with `s`) while the operating conditions `T` (temperature, pressure,
composition, conversion) are shared by all parallel units or are intensive. Written naively,
such models contain products `n·T` or `s·T` between a discrete scale variable and continuous
intensive variables, which are then relaxed by McCormick envelopes and branched on.

## Definitions

Let `E ⊂ R^d × R^p` be a nonempty compact set of admissible per-unit operating points `(ξ, T)`, where `ξ`
collects the *extensive* per-unit quantities (throughput, duty, area, cost, …) and `T` the
*intensive* ones. For a scale `λ ≥ 0` define the scaled copy

```
λ ⊙ E := { (λ ξ, T) : (ξ, T) ∈ E }        (extensive coordinates scaled, intensive ones not).
```

Let `Λ ⊂ [0, ∞)` be a nonempty compact set of admissible scales (e.g. `Λ = {0,1,…,N}` or a finite
catalogue), `λ_min = min Λ`, `λ_max = max Λ`. Two feasible sets are of interest:

- the *size* set `F^size(Λ,E) = { (λ, X, T) : λ ∈ Λ, (X, T) ∈ λ ⊙ E }`, i.e. one unit of size `λ`;
- the *multiplicity* set `F^mult(N,E) = { (n, X, T) : n ∈ {0,…,N}, X = Σ_{i=1}^n ξ_i, (ξ_i, T) ∈ E ∀i }`,
  i.e. `n` identical units sharing `T` (for `n = 0`: `X = 0`, `T` free in `proj_T E`).

For `n = 0` the constraint on `T` is a modelling choice (free `T` in the projection is used below;
a larger convex compact off-state set could be used, but its zero-scale block must then
replace the zero-scale block in the formulas below). Assume `N` is a positive integer;
`N = 0` consists only of the off-state slice and requires no division by `N`.

## Theorem 1 (two-endpoint hull)

For every compact `E` and compact `Λ ⊂ [0,∞)`,

```
conv F^size(Λ,E) = conv( F^size({λ_min},E) ∪ F^size({λ_max},E) )
                 = conv( {λ_min} × (λ_min ⊙ conv E)  ∪  {λ_max} × (λ_max ⊙ conv E) ).
```

In particular `conv F^size(Λ,E) = conv F^size([λ_min,λ_max],E)`: **discreteness of the scale set
costs nothing in the convex hull**, and the hull depends on `Λ` only through its extreme scales.

Proof. If `λ_min = λ_max`, the first equality is immediate. Otherwise fix `(ξ,T) ∈ E` and `λ ∈ Λ`; write `λ = θ λ_max + (1−θ) λ_min` with `θ ∈ [0,1]`. Then
`(λ, λξ, T) = θ (λ_max, λ_max ξ, T) + (1−θ) (λ_min, λ_min ξ, T)`, a convex combination of a point of
`F^size({λ_max},E)` and a point of `F^size({λ_min},E)`, because the map `λ ↦ (λ, λξ, T)` is affine
and `T` is unchanged. Hence `F^size(Λ,E) ⊆ conv(F_{λ_min} ∪ F_{λ_max}) ⊆ conv F^size(Λ,E)`. The
second equality uses `conv(λ ⊙ E) = λ ⊙ conv(E)` (the map `(ξ,T) ↦ (λξ,T)` is linear) and
`conv(A ∪ B) = conv(conv A ∪ conv B)`. ∎

## Theorem 2 (identical parallel units)

`conv F^mult(N,E) = conv F^size({0,…,N}, E) = conv( {0} × {0} × proj_T E  ∪  {N} × (N ⊙ conv E) )`.

Proof. For fixed `n` and `T`, the `X`-fibre of `F^mult` is the `n`-fold Minkowski sum of
`E_T := {ξ : (ξ,T) ∈ E}`, which contains `n E_T` (take all `ξ_i` equal) and is contained in
`n · conv(E_T)`; since `conv(A_1 + … + A_n) = conv A_1 + … + conv A_n` and `C + … + C = nC` for
convex `C`, the fibre has convex hull `n · conv(E_T)`. Taking the union over `T` and then the hull,
`conv F^mult_n = conv( ∪_T {n} × (n conv E_T) × {T} ) = {n} × conv(n ⊙ E) = {n} × (n ⊙ conv E)`,
which is the `n`-th slice of `F^size({0,…,N}, conv E)`. Now apply Theorem 1 with `E` replaced by
`conv E` (Theorem 1 holds for any compact set, convex or not). ∎

## Theorem 3 (explicit extended formulation)

Let `C = conv E` and `P_T = proj_T C` (both convex compact). Then `(λ, X, T) ∈ conv F^size(Λ,E)`
iff there exist `θ ∈ [0,1]`, `X¹, X², T¹, T²` with

```
λ = (1−θ) λ_min + θ λ_max,      X = X¹ + X²,      T = T¹ + T²,
(X¹, T¹) ∈ (1−θ) · (λ_min ⊙ C),        (X², T²) ∈ θ · (λ_max ⊙ C),
```

where `θ·K = {θ k : k ∈ K}` is the usual scaling (and `0·K = {0}`). This is the Balas
(disjunctive) extended formulation of the union of two compact convex sets, with the
disaggregated variables of the *scale* eliminated. In the multiplicity case (`λ_min = 0`):

```
n = θ N,   X¹ = 0,   T¹ ∈ (1−θ) P_T,   (X², T²) ∈ θ · (N ⊙ C),
```

and, substituting `θ = n/N`, the hull of `n` identical units sharing `T` is

```
{ (n, X, T) : ∃ T² :  (X, T²) ∈ (n/N)·(N ⊙ C),   T − T² ∈ (1 − n/N) P_T,   0 ≤ n ≤ N }.
```

If `C` is a polytope `{(ξ,T) : A ξ + B T ≤ b}` and `P_T = {T : D T ≤ e}`, this is the linear system

```
A X + N B T² ≤ b n,      D (T − T²) ≤ e (1 − n/N),      0 ≤ n ≤ N,
```

so the **hull is polyhedral and described by one extra copy of the intensive variables**, with
no bilinear term. If `C` and `P_T` are conic representable, homogenizing their affine
conic constraints gives an exact conic formulation. To check zero weights, suppose
`K_0 = {z: ∃y, A z + B y + b ∈ K}` is nonempty compact, where `K` is a convex cone.
The scaled formulation is `A z + B w + t b ∈ K`, `t ≥ 0`. At `t > 0`, division by
`t` gives exactly `z ∈ tK_0`. At `t = 0`, any feasible `(z,w)` is a recession direction
of the lifted set: add any nonnegative multiple to a fixed feasible lift. Compactness of
its projection `K_0` forces `z = 0`. Conversely `(z,w)=(0,0)` is feasible at `t=0`.
This justifies the boundary even when the auxiliary-variable lift is unbounded.

Proof. Balas' theorem: `conv(K_1 ∪ K_2) = { (1−θ) k_1 + θ k_2 : θ ∈ [0,1], k_i ∈ K_i }` for compact
convex `K_i`. Apply it to `K_1 = {λ_min} × (λ_min ⊙ C)` and `K_2 = {λ_max} × (λ_max ⊙ C)` and read off
the components. ∎

## Corollary 1 (bilinear `n·T` terms)

Assume `0 ≤ l < u`, `l_T < u_T`, and `N ≥ 1`. Let `E = { (ξ, T, ω) : ξ ∈ [l,u], T ∈ [l_T,u_T], ω = ξ T }` (extensive `ξ, ω`, intensive `T`), so that
`F^mult` is the set of `(n, X, T, W)` with `n ∈ {0,…,N}` units, `X ∈ [nl, nu]` total load, shared
`T`, and `W = X T`. Since `conv E` is the McCormick polytope of `ξT` on its box, Theorem 3 gives the
polyhedral hull. For `N = 3, [l,u] = [1,2], [l_T,u_T] = [0.5,1.5]`, a direct facet computation
(`code/scaling_disjunctions/bilinear_multiplicity_hull.py`) confirms that the hull is the
convex hull of the six points `(0,0,l_T,0), (0,0,u_T,0), (N,Nl,l_T,Nl l_T), (N,Nl,u_T,Nl u_T),
(N,Nu,l_T,Nu l_T), (N,Nu,u_T,Nu u_T)` and consists of

```
n l ≤ X ≤ n u,   0 ≤ n ≤ N,
McCormick of W = X T over the global box X ∈ [0, N u], T ∈ [l_T,u_T]   (4 inequalities),
W ≤ u_T X + l [ N T − N l_T − n (u_T − l_T) ],
W ≥ l_T X + l [ N T − N u_T + n (u_T − l_T) ].
```

The last two inequalities are the McCormick inequalities that use the *scaled* lower bound `nl`
on `X` (which would contain the bilinear term `n·T`) with `n·T` replaced by its RLT linearization
against `(N − n) ≥ 0`: e.g. `W ≤ u_T X + n l T − n l u_T` plus `l (N − n)(T − l_T) ≥ 0`. In the random
test of the script, 13.5 % of the points of the naive relaxation "global McCormick ∩ {X ∈ [nl,nu]}"
are cut off by the hull.

## Correction to the original Theorem 4: scale costs need not separate

The formerly stated formula `conv epi_F(g + f) = epi_convF(g + f̌)` is false,
even when `g = 0` and `E` is convex. The failed proof tried to preserve a decomposition's
intensive coordinates while changing its scale distribution. These distributions cannot
generally be chosen independently.

Take `Λ = {0,1,2}`, `E = {(ξ,T): ξ = T ∈ [0,1]}`, and
`f(0) = f(2) = 1`, `f(1) = 0`. The point

```
(λ,X,T) = (1,1,1/2) = (1/2)(0,0,0) + (1/2)(2,2,1)
```

belongs to `conv F^size`. Its cost under the proposed separated expression is
`f̌(1) = 0`. Its actual minimum convexified cost is **1**. Indeed, `X ≤ 2T` holds
on every scale slice. At the displayed point equality holds, so every point in a convex
representation satisfies equality. At scale 0 or 1 this forces `T = 0` and hence `X = 0`.
Only scale 2 can contribute to `X`. If its total weight is `q`, then `X = 1` implies
`q ≥ 1/2`, whereas `λ = 1` implies `2q ≤ 1`. Thus `q = 1/2`, all other weight is at
scale 0, and the expected scale cost is 1. Multiplying `f` by any positive constant
makes the error arbitrarily large.

There is a second independent obstruction to the original formula: convexifying a
nonconvex per-unit domain does not preserve a convex nonlinear cost. With no intensive
variable, `Λ = {1}`, `E = {-1,1}`, and `g(λ,X) = |X|`,
the convexified cost at `X = 0` is 1, whereas `g(1,0) = 0`. The cost must be lifted
before convexification. Also `λ c(X/λ,T)` need not be jointly convex in `(λ,X,T)`
when `c` is convex: `c(ξ,T) = T²` gives `λT²`.

## Theorem 4A (correct factorization with extensive variables only)

Let `E ⊂ R^d` be nonempty compact, let `c:E→R` be continuous, let `Λ` be a nonempty
finite subset of `[0,∞)`, and let `f:Λ→R`. Define

```
H = conv{(ξ,c(ξ)): ξ ∈ E},
h(x) = min{z: (x,z) ∈ H},      x ∈ conv E,
F_c = {(λ, λξ, Z): λ ∈ Λ, ξ ∈ E, Z ≥ λc(ξ) + f(λ)}.
```

Let `f̌` be the lower convex envelope of the finitely many points `(λ,f(λ))`.
Then, at positive scales,

```
conv F_c ∩ {λ > 0} = {(λ,X,Z): λ ∈ conv Λ, λ > 0, X ∈ λ conv E,
                     Z ≥ λ h(X/λ) + f̌(λ)}.
```

If `0 ∈ Λ`, include the zero-scale slice `{(0,0,Z): Z ≥ f(0)}`.
In particular, if `E` is convex and `c` is convex and continuous, then `h = c`.
The same formula applies to identical units with additive per-unit costs and no shared
intensive coordinates, by applying Theorem 2 to the lifted set `{(ξ,c(ξ)):ξ∈E}`.

Proof. In a finite convex combination with mean scale `λ > 0`, write its weights as
`μ_j`, its scales as `λ_j`, and its per-unit points as `ξ_j`. The weights
`μ_j λ_j/λ` sum to 1, so the per-unit contribution to cost is at least
`λ h(X/λ)`. The scale contribution is at least `f̌(λ)`. At mean scale zero,
nonnegativity of the scales forces every scale to be zero.

Conversely, choose a finite representation
`(X/λ,h(X/λ)) = Σ_i ν_i (ξ_i,c(ξ_i))` and weights `μ_j` attaining
`f̌(λ) = Σ_j μ_j f(λ_j)`, `λ = Σ_j μ_j λ_j`. These exist because the relevant
convex hulls are compact. The product weights `μ_jν_i` on
`(λ_j,λ_jξ_i,λ_jc(ξ_i)+f(λ_j))` give the claimed point with equality in cost.
Any additional nonnegative epigraph slack can be added to every constituent. ∎

## Theorem 4B (when all scale-only costs separate with shared intensive variables)

Let `E ⊂ R^d × R^p` be nonempty compact and `Λ ⊂ [0,∞)` finite, with
`0,s,M ∈ Λ`, where `0 < s < M = max Λ`. Put
`C = conv E`, `Q = proj_ξ C`, `P_T = proj_T C`, and `F = F^size(Λ,E)`.
The following three statements are equivalent:

1. For every `f:Λ→R`,
   `conv{(λ,X,T,Z):(λ,X,T)∈F, Z≥f(λ)}
    = {(λ,X,T,Z):(λ,X,T)∈conv F, Z≥f̌(λ)}`.
2. That identity holds for the single cost `f(s)=0`, `f(λ)=1` for `λ≠s`.
3. `C = Q × P_T`.

Thus universal separation of scale-only costs is possible exactly when the convexified
per-unit model has no coupling between its extensive and intensive coordinates. This
criterion concerns arbitrary scale-only costs; it does not say that every nonrectangular
model fails for every particular cost. For example, affine scale costs always separate.

Proof. Statement 1 implies statement 2. Assume statement 2. Since `f̌(s)=0`, every
`(s,X,T)∈conv F` has a cost-zero representation. Every constituent in that representation
must have scale `s`, since the other scales have cost at least 1. Hence

```
{(X,T):(s,X,T)∈conv F} = s ⊙ C.                       (*)
```

Set `α=s/M∈(0,1)`. For any `(ξ,T_1)∈C` and `T_0∈P_T`, the endpoint slices of
`conv F` contain `(M,Mξ,T_1)` and `(0,0,T_0)`. Their convex combination of weights
`α,1−α` is `(s,sξ,αT_1+(1−α)T_0)`. By (*),
`(ξ,αT_1+(1−α)T_0)∈C`. Iterate with the same `ξ,T_0`; this shows
`(ξ,α^kT_1+(1−α^k)T_0)∈C` for every `k`. Closedness gives `(ξ,T_0)∈C`.
Every `ξ∈Q` has some such `T_1`; therefore `Q×P_T⊆C`. The reverse inclusion holds
by definition, proving statement 3.

Assume statement 3. The base hull equals
`{(λ,X,T):0≤λ≤M, X∈λQ, T∈P_T}`. For a positive-scale point, write `X=λξ`
and take scale weights attaining `f̌(λ)`. The same `(ξ,T)∈C` is available in the
convexified slice of every scale, so these weights represent the base point with cost
`f̌(λ)`. Each of those slice points has a finite representation by points of `E` and
the cost is constant within its slice. Thus the representation lies in the hull of the
original epigraph. At scale zero only the zero slice is possible. Jensen's inequality
for `f̌` proves the other inclusion. ∎

The new criterion is a candidate observation arising from the independent audit.
A targeted literature search has not located this exact equivalence; novelty is unconfirmed.

## Theorem 5 (several unit types over an integral count polytope)

Let unit types `k = 1,…,K` have nonempty compact per-unit sets `E_k ⊂ R^{d}` (extensive variables only, aggregated
additively: `X = Σ_k X_k`), and let the vector of counts `n = (n_1,…,n_K)` be restricted to
`P ∩ Z^K` for an *integral* polytope `P ⊆ [0,N]^K` (bounds, total-count budgets, and any
totally-unimodular count constraints with integral right-hand sides). Then

```
conv { (n, X) : n ∈ P ∩ Z^K,  X ∈ Σ_k (n_k-fold sum of E_k) } = { (n, X) : n ∈ P,  X ∈ Σ_k n_k conv E_k }.
```

Proof. "⊆" follows from `n_k-fold(E_k) ⊆ n_k conv E_k` and convexity of the right-hand side (it is
the image of a convex set under a linear map: `{(n, Σ_k w_k) : n ∈ P, w_k ∈ n_k conv E_k}` is convex
because `{(n_k, w_k) : w_k ∈ n_k C_k}` is a cone section). "⊇": let `n ∈ P`, `X = Σ_k n_k w_k` with
`w_k ∈ conv E_k`. Write `n = Σ_j ρ_j n^j` with integral vertices `n^j` of `P`. Then
`(n, X) = Σ_j ρ_j (n^j, Σ_k n^j_k w_k)`, and `Σ_k n^j_k w_k ∈ Σ_k n^j_k conv E_k = conv(Σ_k n^j_k-fold E_k)`,
so each `(n^j, Σ_k n^j_k w_k)` lies in the hull of the left-hand side. ∎

## Theorem 6 (classical Shapley–Folkman bound, with its scope)

For `n ≥ 1` identical units with extensive aggregation only, every point
`X ∈ n · conv E` can be written as `X = Σ_{i=1}^n ξ_i` with all but at most
`min(d,n)` of the `ξ_i` in `E` and the remaining ones in `conv E` (Shapley–Folkman).
Replacing each exceptional point by any point in `E` changes the sum by at most
`min(d,n) diam(E)` in any fixed norm. Consequently the Hausdorff distance between the
`n`-fold Minkowski sum of `E` and `n conv E` is at most `min(d,n) diam(E)`.

For an `L`-Lipschitz objective minimized over these two aggregate sets, **without further
aggregate constraints**, the gap is between 0 and `L min(d,n) diam(E)`. A relative bound
`O(d/n)` additionally requires an objective value or other explicitly chosen normalization
bounded below by a positive constant times `n`, with `L` and `diam(E)` bounded uniformly.
It does not follow from multiplicity alone. Adding balance equations or demand constraints
can make the rounded point infeasible, so this distance estimate alone supplies no
constrained optimality-gap bound. These are classical consequences of Shapley–Folkman,
recorded for context, with no novelty claim.

## Relation to known results

- *Convex per-unit model, integer count, no intensive variables.* The statement "the continuous
  relaxation of the aggregated perspective model is the convex hull" is Theorem 3 of Wu, Li, Lu,
  Deng, Fang, "Variable aggregation-based perspective reformulation for mixed-integer convex
  optimization with symmetry", [arXiv:2602.04123](https://arxiv.org/html/2602.04123v1#S4)
  (2026); their Lemma 3 is the identity
  `conv(r ⊗ F) = r ⊗ conv(F)` used in Theorem 2. Knueven, Ostrowski, Watson (IEEE TPWRS 2018) use
  total unimodularity / integer decomposition for aggregated identical generators (Theorem 5's
  mechanism in the MILP setting). Bertsekas et al. (1983), Starr (1969), Aubin–Ekeland (1976) give
  Theorem 6's substance.
- *Affine dependence on one variable.* The mechanism of Theorem 1 (a set that is a union of affine
  images of `Λ` has the hull of its two extreme slices) is the elementary endpoint
  interpolation used for bilinear graphs. Jach, Michaels, and Weismantel's
  [The Convex Envelope of (n–1)-Convex Functions](https://epubs.siam.org/doi/10.1137/07069359X)
  (2008) is related envelope literature; its title and abstract alone do not establish
  that it contains the exact set-valued statement here.
- *Novelty assessment after audit.* Theorems 1–3 are direct affine interpolation and
  disjunctive convexification; the six-point bilinear hull is a small polyhedral special
  case. Theorem 5 follows by keeping each type's per-unit convex point fixed while
  decomposing the count vector; it requires no integer-decomposition property. These
  may be useful modeling observations but are not established research novelties.
  The original cost-separation claim was false. Theorem 4A is a standard perspective
  and product-distribution argument. Theorem 4B gives an exact obstruction criterion
  worth further checking; no claim of publishability is made.

A block hull need not remain exact after imposing process balances or other linking
constraints: in general `conv(F ∩ L) ⊊ conv(F) ∩ L`. Accordingly, the equalities here
refer to the stated local sets. They do not imply that a complete process MINLP has no
integrality gap, nor that intermediate catalogue sizes can be removed from the original
feasible model.

## Negative remark (scale invariance is essential)

If the per-unit model is not scale-invariant, e.g. `E(λ)` depends on `λ` non-homogeneously
(pressure drop growing with pipe length, efficiency curves that depend on size), then
`F = ∪_λ {λ} × (λ ⊙ E(λ))` is no longer a union of affine images and intermediate scales can stick
out of `conv(F_{λ_min} ∪ F_{λ_max})`; a one-dimensional example is `E(λ) = {ξ = λ}` on `Λ = {1,2,3}`
(so `X = λ²`), where `(2,4)` is not in the segment between `(1,1)` and `(3,9)`. In that case the
full disjunctive hull over all scales is needed.
