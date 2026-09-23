# Density and degeneracy bounds on the McCormick-versus-hull gap of bilinear functions

Status: mathematical proof audited by separate AI agents on 2026-09-04;
not externally peer reviewed. The audit preserves the degeneracy constant 4 and improves the
maximum-degree constant from `2√2` to `2`. A fractional-orientation argument also
strengthens `4√d` to `4√ρ`, where `ρ` is maximum subgraph edge-to-vertex density.
Boundary conventions and sharpness statements were
corrected. Numerical checks support the inequalities but do not prove them. Novelty is
limited: the density order follows from known Schur-multiplier results and Grothendieck's
inequality, as detailed in the companion density-characterization note. The explicit constant
4 and elementary McCormick-gap proof remain possible contributions. See
`notes/audit-mccormick.md` for the audit and search scope; the strengthened density
argument also passed the independent check in `notes/review-mccormick-density.md`.

The bounds improve the upper bound in Theorem 2 of Boland, Dey, Kalinowski, Molinaro,
Rigterink, "Bounding the gap between the McCormick relaxation and the convex hull for bilinear
functions", Math. Program. 162:523–535 (2017), [open manuscript](https://arxiv.org/abs/1507.08703);
local copy `literature/papers/boland2017-bounding-the-gap-between-the/`.

## Setting (Boland et al.)

Let `G = (V,E)` be a graph on `V = {1,…,n}` and `b(x) = Σ_{ij∈E} a_ij x_i x_j` a bilinear function on
`[0,1]^n`. Let `cav[b], vex[b]` be the concave and convex envelopes of `b` over the box, and
`mcu[b], mcl[b]` the upper and lower McCormick envelopes (obtained by replacing every product by
its own McCormick variable). Put

```
chgap[b](x) = cav[b](x) − vex[b](x),      mcgap[b](x) = mcu[b](x) − mcl[b](x),
c*(b) = inf { c ≥ 0 : mcgap[b](x) ≤ c · chgap[b](x)  for all x ∈ [0,1]^n }.
```

Delete zero-coefficient edges when defining the support graph. If no edges remain, both gaps
vanish and `c*(b) = 0`. Thus statements below asserting `c* = 1` assume nonempty support.

Known: `c*(b) ≤ 2 − 1/⌈χ(G)/2⌉` if all `a_ij > 0` (Luedtke–Namazifar–Linderoth 2012);
`c*(b) ≤ 600 √n` for arbitrary signs, and random `±1` weights on the complete graph give
`c*(b) ≥ √n/4` asymptotically almost surely (Boland et al. 2017); `c*(b) = 1` iff every cycle of
`G` has an even number of positive and an even number of negative edges (Boland et al., Thm 4).
The gap between `√n/4` and `600√n` and the question of structural (graph-parameter) bounds
for mixed signs are the research directions recorded in `notes/open-problems-from-literature.md` (#14).

For `X ⊆ V` write `γ(X)` for the edge set of the induced subgraph `G[X]`, `μ⁺(X)` and `μ⁻(X)` for
the maximum and minimum weight of a cut of `G[X]` (the empty cut has weight 0, so
`μ⁺(X) ≥ 0 ≥ μ⁻(X)`). Boland et al., Corollary 1: if `Σ_{ij∈γ(X)} |a_ij| ≤ c (μ⁺(X) − μ⁻(X))` for
all `X ⊆ V`, then `mcgap[b](x) ≤ c · chgap[b](x)` for all `x ∈ [0,1]^n`.

The *degeneracy* `d(G)` is the smallest `d` such that every nonempty subgraph of `G` has a vertex of degree
at most `d`; equivalently `G` has an acyclic orientation with all out-degrees at most `d`.
Every induced subgraph satisfies `d(G[X]) ≤ d(G)`; `d(G) ≤ Δ(G)` (maximum degree) and
`d(G) ≤ tw(G)` (treewidth); forests with an edge have `d = 1`, series–parallel graphs `d ≤ 2`, planar graphs
`d ≤ 5`, `K_n` has `d = n−1`, `K_{m,n}` has `d = min(m,n)`.

Define the maximum subgraph density

```
ρ(G) = max_{∅ ≠ U ⊆ V} |E(G[U])| / |U|,
```

with `ρ(G) = 0` if `V` is empty. This is half the maximum average degree;
it is different from fractional arboricity, whose denominator is `|U|−1`.
It satisfies `ρ(G) ≤ d(G)` and `ρ(G) ≤ Δ(G)/2`, and is monotone under taking subgraphs.

## Theorem

For every graph `G`, every bilinear `b` on `G` with arbitrary real coefficients, and every `x ∈ [0,1]^n`,

```
mcgap[b](x)  ≤  4 · √ρ(G) · chgap[b](x),          i.e.   c*(b) ≤ 4 √ρ(G),
mcgap[b](x)  ≤  4 · √d(G) · chgap[b](x),          i.e.   c*(b) ≤ 4 √d(G),
mcgap[b](x)  ≤  2 · √Δ(G) · chgap[b](x),        i.e.   c*(b) ≤ 2 √Δ(G).
```

More precisely, for every weighted graph `H = (X, γ(X))` with weighted adjacency matrix `A`,

```
μ⁺(X) − μ⁻(X)  =  max_{S ⊆ X} ‖A_{S,X∖S}‖_{∞→1}  ≥  (1/√2) · max_{S ⊆ X} Σ_{i∈S} ‖a_{i,X∖S}‖₂ ,        (★)
μ⁺(X) − μ⁻(X)  ≥  ‖a_{γ(X)}‖₁ / (4 √ρ(H))  ≥  ‖a_{γ(X)}‖₁ / (4 √d(H)),      μ⁺(X) − μ⁻(X)  ≥  (1/4) Σ_{i∈X} ‖a_i‖₂  ≥  ‖a_{γ(X)}‖₁ / (2 √Δ(H)),
```

The expressions dividing by `ρ(H)`, `d(H)`, or `Δ(H)` apply only when `H` has an edge;
for an edgeless `H` use the undivided statement `0 ≥ 0`.

Here `a_{i,T}` is the vector of weights of edges from `i` to `T`, `a_i = a_{i,X}`, and `‖B‖_{∞→1} = max_u ‖Bu‖₁`
over sign vectors `u`.

The dependence on `ρ`, `d`, and `Δ` is best possible up to the constant: Boland et al. prove that
random `±1` weightings of `K_{n}` (degeneracy `n−1`) have `c*(b) ≥ (1−1/n)√n/2.4` with probability
tending to one (their Theorem 1 is stated with the weaker constant `1/4`), and their explicit Hadamard
construction gives `c*(b) ≥ √n/3` for every `n ≥ 18`.

## Proof

Fix `X` and write `A` for the symmetric weighted adjacency matrix of `H = G[X]` (zero diagonal).
For a sign vector `s ∈ {±1}^X`, the cut `({i : s_i = 1}, {i : s_i = −1})` has weight
`Σ_{ij∈γ(X)} a_ij (1 − s_i s_j)/2 = a(γ(X))/2 − f(s)/2` with `f(s) = Σ_{ij∈γ(X)} a_ij s_i s_j = sᵀAs/2`
(the empty cut corresponds to `s = ±1`). Hence

```
μ⁺(X) − μ⁻(X) = (max_s f(s) − min_s f(s))/2 = max_{s,s'} (f(s) − f(s'))/2.
```

Step 1 (signed bipartite form). For sign vectors `s, s'` put `u = (s+s')/2`, `v = (s−s')/2`; then
`u, v ∈ {−1,0,1}^X` have complementary supports `T = {i : s_i = s'_i}` and `S = {i : s_i ≠ s'_i}`,
and by symmetry of `A` (the cross terms `sᵀAs'` and `s'ᵀAs` cancel)

```
f(s) − f(s') = (sᵀAs − s'ᵀAs')/2 = (s−s')ᵀ A (s+s') / 2 = 2 vᵀ A u = 2 Σ_{i∈S, j∈T} a_ij v_i u_j .
```

Conversely every `S ⊆ X` and every choice of signs `v ∈ {±1}^S`, `u ∈ {±1}^T` arises this way
(`s = u + v`, `s' = u − v`). Therefore

```
μ⁺(X) − μ⁻(X) = max_{S⊆X} max_{v∈{±1}^S, u∈{±1}^T} vᵀ A_{S,T} u = max_{S⊆X} ‖A_{S,T}‖_{∞→1},
```

where `A_{S,T}` is the `S × T` block of `A` and `T = X ∖ S`; the quantity is symmetric in `(S,T)`.

Step 2 (Khintchine). For fixed `S`, let `u` be uniformly random in `{±1}^T`. For each `i ∈ S`,
`(A_{S,T}u)_i = Σ_{j∈T} a_ij u_j` is a Rademacher sum, and Szarek's sharp Khintchine inequality
(Studia Math. 58, 1976; all `p` in Haagerup, Studia Math. 70, 1981) gives
`E|Σ_j a_ij u_j| ≥ ‖a_{i,T}‖₂/√2`. Taking expectations and then the best `u`,

```
‖A_{S,T}‖_{∞→1} ≥ E ‖A_{S,T} u‖₁ ≥ (1/√2) Σ_{i∈S} ‖a_{i,T}‖₂ =: X_S/√2 ,
```

and by the symmetry of Step 1 also `‖A_{S,T}‖_{∞→1} ≥ (1/√2) Σ_{j∈T} ‖a_{j,S}‖₂ =: Y_S/√2`. This is (★).

Step 3a (degeneracy: greedy two-colouring). Fix a degeneracy ordering `v_1,…,v_m` of `H` (each `v_k`
has at most `d = d(H)` neighbours among `v_{k+1},…,v_m`) and orient every edge from the earlier to
the later vertex, so `|out(i)| ≤ d`. Colour the vertices in the order `v_m, v_{m−1}, …, v_1`; when
`i` is coloured all of `out(i)` is already coloured, and since
`‖a_{i,out(i)∩S}‖₂² + ‖a_{i,out(i)∩T}‖₂² = ‖a_{i,out(i)}‖₂²`, one of the two sides receives out-weight
of `ℓ₂`-norm at least `‖a_{i,out(i)}‖₂/√2`; put `i` on the *other* side. Every vertex then has
`‖a_{i, opposite side}‖₂ ≥ ‖a_{i,out(i)}‖₂/√2`, hence

```
X_S + Y_S ≥ (1/√2) Σ_i ‖a_{i,out(i)}‖₂ ≥ (1/√2) Σ_i ‖a_{i,out(i)}‖₁/√d = ‖a_{γ(X)}‖₁/(√2 √d),
```

using Cauchy–Schwarz on at most `d` out-edges and the fact that every edge is an out-edge of exactly
one vertex. With Step 2, `μ⁺ − μ⁻ ≥ max(X_S, Y_S)/√2 ≥ (X_S + Y_S)/(2√2) ≥ ‖a_{γ(X)}‖₁/(4√d)`.

Step 3b (maximum degree: a cut locally maximal for squared weights). Choose a bipartition
`S,T` that is locally maximal, under moving one vertex, for the nonnegative cut objective
`Σ_{ij crossing} a_ij²`. Such a partition exists because there are finitely many partitions.
For every vertex `i`, moving it cannot improve this objective, so the sum of squared weights
crossing from `i` is at least the sum not crossing. Therefore

```
‖a_{i,opp(i)}‖₂ ≥ ‖a_i‖₂/√2,
X_S + Y_S ≥ (1/√2) Σ_i ‖a_i‖₂,
μ⁺ − μ⁻ ≥ (X_S + Y_S)/(2√2) ≥ (1/4) Σ_i ‖a_i‖₂.
```

For each nonisolated vertex, Cauchy–Schwarz gives
`‖a_i‖₂ ≥ ‖a_i‖₁/√deg(i) ≥ ‖a_i‖₁/√Δ`. Isolated vertices contribute zero.
Since `Σ_i ‖a_i‖₁ = 2‖a_{γ(X)}‖₁`, this proves
`μ⁺ − μ⁻ ≥ ‖a_{γ(X)}‖₁/(2√Δ)` for `Δ > 0`.

Step 3c (fractional orientations and maximum subgraph density). A fractional orientation assigns
numbers `θ_ij, θ_ji ≥ 0` to each edge `ij`, with `θ_ij + θ_ji = 1`. There exists such an assignment
with `Σ_j θ_ij ≤ ρ(H)` for every vertex. This is the standard densest-subgraph/fractional-orientation
duality; see Theorem 1 in
[Local Density and Its Distributed Approximation (STACS 2025)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol327-stacs2025/LIPIcs.STACS.2025.25/LIPIcs.STACS.2025.25.pdf).
For completeness, the following max-flow proof establishes exactly the form needed here.

Build a network with a source, one node per edge of `H`, one node per vertex, and a sink.
The source-to-edge arcs have capacity 1; each edge node has an arc of capacity `|E(H)|+1` to
each endpoint; each vertex-to-sink arc has capacity `t`. A source/sink cut with capacity at
most `|E(H)|` cannot cut an edge-to-endpoint arc. If its source side contains vertex set `U`,
only edge nodes for edges wholly inside `U` can be on that side. For this `U`, including all
those edge nodes minimizes the cut capacity to `|E(H)|−|E(H[U])|+t|U|`.
Thus every cut has capacity at least `|E(H)|` when `t = ρ(H)`; max-flow/min-cut gives a flow
saturating every source-to-edge arc. The two flows leaving each edge node define `θ_ij, θ_ji`.
Conversely, summing vertex loads over `U` shows that any feasible load bound `t` must satisfy
`|E(H[U])| ≤ t|U|`, so `ρ(H)` is precisely the smallest possible load bound.

For this fractional orientation, weighted Cauchy–Schwarz at each vertex gives

```
Σ_j θ_ij |a_ij|
    ≤ (Σ_j θ_ij)^(1/2) (Σ_j θ_ij a_ij²)^(1/2)
    ≤ √ρ(H) ‖a_i‖₂.
```

Here `0 ≤ θ_ij ≤ 1`, and a zero row contributes zero. Summing over vertices counts every
absolute edge weight exactly once, giving `‖a_{γ(X)}‖₁ ≤ √ρ(H) Σ_i ‖a_i‖₂`.
Step 3b now implies `μ⁺−μ⁻ ≥ ‖a_{γ(X)}‖₁/(4√ρ(H))` when `H` has an edge.
This also yields the degeneracy bound, since a degeneracy orientation has load at most `d(H)`
and hence `ρ(H) ≤ d(H)`. Step 3a remains an independent proof of that weaker bound.

Step 4. Maximum subgraph density, degeneracy, and maximum degree are monotone under induced
subgraphs. The corresponding inequalities give the hypothesis of Boland et al., Corollary 1,
with `c = 4√ρ(G)`, `c = 4√d(G)`, or `c = 2√Δ(G)`. ∎

Note that Corollary 1 is in fact an equality, `c*(b) = max_{X⊆V} ‖a_{γ(X)}‖₁/(μ⁺(X) − μ⁻(X))`
(take `x = 1/2` on `X` and `0` elsewhere in Lemma 1 and Lemma 3.9 of Luedtke et al.), so the
theorem is exactly a lower bound on the signed cut range of induced subgraphs. The maximum
is over subsets with nonempty weighted support; its value is defined as zero if no such subset
exists. A nonzero edge ensures positive cut range, directly by (★).

## Bipartite corollary

Suppose the support graph is bipartite with fixed parts `P,Q` and has an edge. Put
`Δ_P=max_{i∈P}deg(i)` and `Δ_Q=max_{j∈Q}deg(j)`. Then

```
c*(b) ≤ √(2 min{Δ_P,Δ_Q}) ≤ √(2 min{|P|,|Q|}).
```

Indeed, choose `S=P` in (★). Every edge crosses this partition, so

```
R(G) ≥ ||A_{P,Q}||_{∞→1}
     ≥ (1/√2) Σ_{i∈P} ||a_i||₂
     ≥ ||a||₁/√(2Δ_P).
```

Transpose the block to obtain the corresponding bound with `Δ_Q`. The same argument applies
to every induced subgraph, whose degrees within the inherited parts can only decrease; then
apply the gap characterization. The second inequality follows from `Δ_P≤|Q|`, `Δ_Q≤|P|`.
The four-cycle with one negative unit edge has `c*=2` and `Δ_P=Δ_Q=2`, so the universal
constant `√2` in this maximum-degree-within-a-part bound cannot be improved.
This is a direct consequence of the standard bipartite Khintchine estimate. It was identified
in the independent density review and is not asserted to be a new harmonic-analysis theorem.

## Remarks and corollaries

1. **General boxes.** For `b` on a box `Π[l_i,u_i]`, the affine change of variables
   `x_i = l_i + (u_i − l_i) x̃_i` maps `b` to a bilinear function on `[0,1]^n` with the same graph plus
   linear terms; envelopes and McCormick envelopes commute with affine changes of variables and
   are shifted equally by linear terms, so the bounds hold on every box (edges with `u_i = l_i`
   disappear, which can only lower `d`).
2. **Structural corollaries.** `c* ≤ 4` for forests (where in fact `c* = 1`), `c* ≤ 4√2 ≈ 5.7` for
   series–parallel graphs, `c* ≤ 4√3 ≈ 6.93` for planar graphs (`ρ ≤ 3`), `c* ≤ √(2 min{m,n})` for the complete
   bipartite interaction graph `K_{m,n}` of a pool with `m` proportion variables and `n` flow
   variables. In process models where each flow multiplies at most `K` intensive variables and each
   intensive variable multiplies at most `K` flows (`Δ ≤ K`), the term-by-term McCormick relaxation is
   within a factor `2·√K` of the convex hull, independently of the model size.
3. **Comparison with Boland et al. and numerics.** For `G = K_n` the maximum-degree bound gives `c* ≤ 2√(n−1)`,
   replacing the constant 600 in `600√n`; for sparse graphs it replaces `√n` by `√d(G)`. Exhaustive
   computation over all `±1` weightings (`code/mccormick_degeneracy/kn_pm1_ratio.py`) gives the
   *centre* ratios `‖a‖₁/(μ⁺(V) − μ⁻(V))` (the gap ratio at `x = (1/2,…,1/2)`) 1.5, 1.5, 2.5, 3.0, 2.625
   for `K_3,…,K_7`; since `c*(b)` is a maximum over induced subgraphs, `max_b c*(b)` on `K_n` is
   monotone in `n` and is at least 3.0 for `n ≥ 6`. In a seeded 4000-trial run on random weighted graphs with up to 9
   vertices (edgeless samples skipped) the ratio `‖a‖₁/(μ⁺−μ⁻)` never exceeded `√2·√d` (`check_cut_inequality.py`; the value
   `√2·√2 = 2` is attained by `C_4` with one negative edge). The best universal constant `κ` in
   `c*(b) ≤ κ √d(G)` lies in `[√2, 4]`: the lower bound follows from the frustrated `C_4`,
   where `‖a‖₁ = 4`, `μ⁺−μ⁻ = 2`, and `d = 2`. A separate asymptotic question restricts to
   sequences with `d → ∞`; the random complete-graph lower bound then gives at least `1/2.4`.
   These two optimization questions must not be conflated. For the density bound
   `c* ≤ κ_ρ√ρ`, the corresponding universal constant lies in `[2,4]`, again using the
   frustrated `C_4` (`ρ = 1`).

4. **Per-instance certificate.** (★) and the row-norm bound `μ⁺ − μ⁻ ≥ (1/4) Σ_i ‖a_i‖₂` are
   lower bounds on the signed cut range that need no graph parameter. The row-norm bound is
   directly computable; any chosen bipartition supplies another certificate. Maximizing
   `Σ_{i∈S}‖a_{i,X∖S}‖₂` over bipartitions (a max-cut-like problem) yields an instance-specific bound on
   the centre ratio. A uniform bound on `c*(b)` must cover every induced subgraph.
5. **Why degeneracy and not chromatic number.** Luedtke et al.'s positive-coefficient bound uses
   `χ(G)`; for mixed signs `χ` cannot work: Boland et al. remark (Section 2.4) that on the complete
   bipartite graph on `n` vertices with equal parts (`χ = 2`, degeneracy `n/2`) almost all `±1`
   weightings have `mcgap ≥ (√n/8)·chgap` at the centre of the box, matching the degeneracy up to
   constants. Degeneracy is the right sparsity parameter here: it is monotone under induced
   subgraphs (which Corollary 1 needs), it is at most treewidth and maximum degree, and `K_{d+1}`
   and balanced complete bipartite graphs show it is attained up to constants.
6. **Novelty limits.** Khintchine row-norm estimates, polarization, locally maximal cuts, and
   degeneracy orientations, and fractional-orientation duality are standard. The possible contribution is their combination into
   explicit graph-parameter bounds for the mixed-sign McCormick/hull ratio. The original
   Boland et al. proof already uses discrepancy arguments and weighted Khintchine estimates;
   improving its constant alone should not be described as a new principle. The bounded
   initial search documented in `notes/audit-mccormick.md` found no exact prior statement.
   Subsequent research found that Davidson–Donsig's Schur-pattern theorem combined with
   Grothendieck's inequality already implies the same density order, with a larger constant.
   The transfer is recorded in the [companion characterization](mccormick-hereditary-density-characterization.md).
   Therefore the density order must not be presented as a new principle. The explicit
   constant and elementary proof may remain useful; publication priority is unestablished.

## Further development

[Graph-by-graph density characterization](mccormick-hereditary-density-characterization.md)
combines the density upper bound here with a random-sign lower bound on a densest induced
subgraph. It treats worst coefficients on each fixed graph, a stronger statement than
sharpness only along complete-graph families. Its proof and audit status are recorded there.

## Files

- `code/mccormick_degeneracy/check_cut_inequality.py` — random checks of degree, degeneracy, and row-norm bounds with exact max/min cuts.
- `code/mccormick_degeneracy/audit_cut_identity.py` — independent finite checks of (★), local squared-weight cuts, and the density bound, including boundary cases.
- `code/mccormick_degeneracy/kn_pm1_ratio.py` — exact worst `±1` ratios on `K_3..K_7`.
