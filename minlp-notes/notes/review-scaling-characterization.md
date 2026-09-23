# Independent review: universal separation of scale-only costs

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.

Status: the characterization below is correct. This is a mathematical audit, not a
literature novelty assessment. It concerns **scale-only costs**, with no additional
operating cost. In particular it does not validate the original Theorem 4 in
`results/scaling-disjunctions-hull.md`.

## Precise statement

Let `E` be a nonempty compact subset of `R^p × R^q`. Write
`C = conv E`, `A = proj_ξ C`, and `B = proj_T C`. Let `Λ` be a finite subset of
`[0,M]`, with `M > 0`, containing `0`, `M`, and at least one `s` with `0 < s < M`.
Define

```
F = { (λ, λξ, T) : λ ∈ Λ, (ξ,T) ∈ E },
H = conv F,
F_f = { (λ, λξ, T, z) : λ ∈ Λ, (ξ,T) ∈ E, z ≥ f(λ) },
f̌(λ) = min { Σ_j μ_j f(λ_j) : μ ≥ 0, Σ_j μ_j = 1,
                                  Σ_j μ_j λ_j = λ }.
```

Here `f : Λ → R` is finite-valued. At scale zero the intensive variable therefore
ranges over `proj_T E`; no larger off-state set is allowed in this statement.

The following conditions are equivalent:

1. For every `f : Λ → R`,
   `conv F_f = { (λ,X,T,z) : (λ,X,T) ∈ H, z ≥ f̌(λ) }`.
2. This equality holds for the single cost `f(s)=0`, `f(λ)=1` for `λ≠s`.
3. The scale-`s` slice of `H` is exactly `{ (s,sξ,T) : (ξ,T) ∈ C }`.
4. `C = A × B`.

Consequently a single interior catalogue size and a single diagnostic cost suffice
to test the universal assertion.

## Proof, including the closure issue

For finite `Λ`, the graph set
`G_f = { (λ,λξ,T,f(λ)) : λ∈Λ, (ξ,T)∈E }` is compact. Hence

```
conv F_f = conv G_f + { (0,0,0,r) : r ≥ 0 }
```

is closed. Compactness of `conv G_f` proves this directly: in a convergent sequence
of sums its compact component has a convergent subsequence, and its vertical
component then converges as well. No closure of a convex hull is silently required.
The minimum defining `f̌` is attained, since its feasible weight vectors form a
nonempty compact polytope for every `λ ∈ [0,M]`.

The two-endpoint argument gives the following exact description of the scale-`s`
slice, with `r=s/M`:

```
H_s = { (s,sξ, r u + (1-r)v) : (ξ,u) ∈ C, v ∈ B }.
```

Indeed every intermediate original-scale point is an affine combination of the
zero and `M` copies of the same per-unit point. Convexifying each endpoint gives
`{(0,0,v):v∈B}` and `{(M,Mξ,u):(ξ,u)∈C}`, and the scale coordinate fixes the mixing
weight to `r`.

`1 ⇒ 2` is immediate. For the diagnostic cost in condition 2, `f̌(s)=0`, all original
epigraph points have nonnegative cost, and an epigraph convex combination with
cost zero can use only scale-`s` points of cost zero. Thus its base point belongs
to the convex hull of the original scale-`s` set, which is `s ⊙ C`. Condition 2
requires every point of `H_s` to have a zero-cost lift. This proves `3`.

For `3 ⇒ 4`, fix any `ξ ∈ A`. Its fibre `C_ξ = {u:(ξ,u)∈C}` is nonempty and compact.
The slice formula and condition 3 imply

```
r C_ξ + (1-r) B ⊆ C_ξ.
```

For arbitrary `u_0∈C_ξ` and `v∈B`, induction gives
`u_k = r^k u_0 + (1-r^k)v ∈ C_ξ` for all integers `k≥0`. Since `0<r<1`, this sequence
converges to `v`. Closedness of the fibre gives `v∈C_ξ`. Thus every fibre is `B`,
and `C=A×B`.

For `4 ⇒ 1`, the endpoint formula gives

```
H = { (λ,X,T) : 0≤λ≤M, X∈λA, T∈B }.
```

The claimed separated epigraph is convex and contains `F_f`, so it contains
`conv F_f`. Conversely take a point of that epigraph and optimal envelope weights
`μ_j`. When `λ>0`, put `ξ=X/λ∈A`; when `λ=0`, choose any `ξ∈A` (then `X=0`). Because
`C=A×B`, `(ξ,T)∈C`. For each `j`,

```
(λ_j,λ_j ξ,T,f(λ_j)) ∈ conv F_f,
```

as follows by expressing `(ξ,T)` as a finite convex combination of points of `E`
at the fixed scale `λ_j`. Averaging with the weights `μ_j` gives
`(λ,X,T,f̌(λ))∈conv F_f`. Adding nonnegative vertical slack proves the claim.

## Concrete strict failure when the product condition is absent

Take `E = {(ξ,T): ξ=T∈[0,1]}`, `Λ={0,1,2}`, and
`f(0)=f(2)=1`, `f(1)=0`. The point `(λ,X,T)=(1,1,1/2)` is the average of
`(0,0,0)` and `(2,2,1)`, so it belongs to `H`. The separate scale-cost envelope
assigns lower bound zero there. The actual epigraph hull requires `z≥1`.

To see the exact lower bound, let `p_i` denote total weight at scale `i` in any
representation. The scale equation gives `p_0=p_2`, and the cost is at least
`p_0+p_2=2p_2`. Every scale-zero point has `X-T≤0`, every scale-one point has
`X-T=0`, and every scale-two point has `X-T≤1`. Since the target has `X-T=1/2`,
`p_2≥1/2`, proving cost at least one. The endpoint representation attains one.

## Scope and material caveats

- The product condition concerns `conv E`, not `E`. Nonconvex per-unit operating
  sets are allowed.
- An interior scale is essential. If `Λ={0,M}`, every cost separates even when
  `C` is not a product: the mean scale fixes the endpoint weights and therefore
  the cost. Thus the stated equivalence would be false without an interior scale.
- Compactness gives closed fibres, bounded endpoint convex hulls, and attained
  epigraph representations. The proof should not be extended to arbitrary
  nonclosed sets without replacing or checking these arguments.
- An enlarged off-state intensive domain changes the slice formula. The theorem
  as stated uses the original projection domain exactly.
- An additional operating cost must be convexified jointly with the per-unit set.
  Convexity of an operating cost alone does not permit replacing the hull of its
  restricted epigraph by its values on `conv E`. For example,
  `E={-1,1}`, `Λ={0,1,2}`, `g(λ,X)=|X|` give
  cost exactly `λ` on every original operating point, while `g(1,0)=0` on the base
  hull. Thus even with no intensive variables, the original operating-cost
  separation claim fails on nonconvex `E`.
