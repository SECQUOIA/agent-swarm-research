# Audit of the McCormick gap bounds

Date: 2026-09-04. This is an independent mathematical review by a separate AI agent,
not external peer review. The owned result is
[Density and degeneracy bounds](../results/mccormick-gap-degeneracy-bound.md).

**Later novelty correction:** the separate Sidon review found that Davidson–Donsig's
Schur-pattern theorem plus Grothendieck's inequality already implies the square-root density
order. The exact transfer and its independent check are recorded in
[the density-characterization note](../results/mccormick-hereditary-density-characterization.md).
The initial unsuccessful search below must not be read as a current novelty claim for that
order. The explicit constant 4 and elementary McCormick proof remain possible contributions.

## Findings and corrections

The original polarization identity, sharp `p=1` Khintchine application, degeneracy-order
colouring argument, and use of the induced-subgraph gap characterization are correct.
In particular, with `f(s)=Σ_{ij}a_ij s_i s_j`, the cut range is `osc(f)/2`, and complementary
supports in `(s+s')/2,(s−s')/2` give the exact identity

```
R(H) = μ⁺(H)−μ⁻(H) = max_{S⊆V(H)} ||A_{S,V(H)\S}||_{∞→1}.
```

There was no missing factor of two in that identity. The original `4√d` inequality remains
valid. The audit made the following corrections.

- The definition of `c*` now restricts the multiplier to `c≥0`. Without this restriction,
  the zero function would have `c*=-∞` under the old definition.
- Zero-coefficient edges are removed from the support graph. Edgeless induced subgraphs
  require the undivided `0≥0` inequality, not division by zero. The maximum of induced ratios
  is taken over nonempty weighted support, with value zero when there are no such subsets.
- Statements that `c*=1` on forests or under the cycle characterization require nonempty
  support; otherwise `c*=0` under the chosen convention.
- Boland et al.'s random-sign proof gives `(1−1/n)√n/2.4`, not literally `√n/2.4`. Its published
  theorem states the weaker `√n/4`. The Hadamard statement `√n/3` for `n≥18` was verified in
  the local PDF, page 7.
- The best universal constant multiplying `√d` is at least `√2`, because the four-cycle with
  one negative unit edge has total absolute weight 4 and cut range 2. An asymptotic constant
  restricted to `d→∞` is a different quantity. The earlier text conflated these questions.
- A computable lower bound for the full graph cut range bounds the centre gap ratio only.
  A bound uniform in `x` must hold for every induced subgraph.
- Claims of external refereeing and completed novelty verification were removed. Numerical
  evidence does not establish mathematical correctness or originality.

## Stronger inequalities obtained during the audit

A partition locally maximal for the nonnegative cut objective `Σ_crossing a_ij²` satisfies
`||a_{i,opposite}||₂≥||a_i||₂/√2` at every vertex. Apply the Khintchine bound to both sides and
use the larger side. This yields

```
R(H) ≥ (1/4) Σ_i ||a_i||₂ ≥ ||a||₁/(2√Δ(H)).
```

The resulting McCormick/hull bound is `c*≤2√Δ`, improving the previous `2√2√Δ`.
The local-cut proof is existential; no polynomial-time bound on an arbitrary sequence of
local moves with real weights is asserted.

More generally, put `ρ(H)=max_{∅≠U⊆V(H)} |E(H[U])|/|U|`, half the maximum average degree.
A standard fractional orientation has `θ_ij+θ_ji=1`, `θ≥0`, and `Σ_jθ_ij≤ρ(H)`.
Weighted Cauchy–Schwarz gives

```
||a||₁ = Σ_i Σ_j θ_ij |a_ij| ≤ √ρ(H) Σ_i ||a_i||₂.
```

Consequently `R(H)≥||a||₁/(4√ρ(H))`, and induced-subgraph monotonicity proves
`c*≤4√ρ(G)`. This implies the old degeneracy bound because `ρ≤d`. The result file includes a
complete max-flow/min-cut proof of the fractional-orientation characterization. This
characterization is standard, including its LP duality formulation in Theorem 1 of
[Local Density and Its Distributed Approximation, STACS 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol327-stacs2025/LIPIcs.STACS.2025.25/LIPIcs.STACS.2025.25.pdf).
The new combination, not fractional orientation itself, is the candidate contribution.

The root agent checked this density argument independently and assigned another separate
agent to review it. The completed review passed and is recorded in `notes/review-mccormick-density.md`.
That reviewer also identified the direct bipartite corollary
`c*≤√(2 min{Δ_P,Δ_Q})`, now included in the result with its short proof; it improves the
complete-bipartite application to `√(2 min{m,n})`. The frustrated four-cycle attains its
universal constant. This consequence uses the standard bipartite Khintchine estimate.

## Numerical verification

All commands below were run successfully during this audit.

- `python code/mccormick_degeneracy/check_cut_inequality.py`: the seeded 4000-trial run passed
  the old degeneracy bound and the strengthened degree and row-norm bounds. Empty random
  graphs are skipped by this historical script, so the actual checked graph count is less
  than 4000. The largest observed ratio divided by `√d` was `1.4142`.
- `python code/mccormick_degeneracy/audit_cut_identity.py`: independent enumeration checked
  the exact polarization identity, the squared-weight cut condition, the row-norm bound,
  and the density bound on 240 seeded weighted graphs and six boundary examples. These
  include zero vertices, one vertex, an edgeless graph, zero weights, one negative edge,
  and the frustrated four-cycle. Each density is enumerated over induced subgraphs.
- `python code/mccormick_degeneracy/kn_pm1_ratio.py`: exhaustive enumeration confirmed the
  reported centre maxima `1.5,1.5,2.5,3,2.625` for `K_3,...,K_7`. These are centre ratios, not
  necessarily the full induced-subgraph maximum for each individual coefficient pattern.

## Literature comparison and limits

[Boland et al., open manuscript](https://arxiv.org/abs/1507.08703) was checked against the
local PDF, especially Lemma 1, Corollary 1, the two lower-bound constructions, and the proof
of the `600√n` upper bound. Their proof already relies on weighted Khintchine and older
signed discrepancy arguments. The present constant improvement alone therefore should not
be presented as a new general technique.

[Bollobás–Scott, Discrepancy in graphs and hypergraphs](https://people.maths.ox.ac.uk/scott/Papers/disc.pdf)
was checked especially at Lemma 6, Theorem 8, and Section 4, Theorem 16 and Lemma 17. These
contain closely related weighted and subgraph discrepancy estimates. The displayed
statements checked do not give the particular McCormick bounds here; adapting their
arguments may recover related structural bounds. A search failing to find a displayed
formula is not enough to establish a substantive new theorem.

Search terms included signed cut discrepancy, weighted graph discrepancy, maximum degree,
degeneracy, McCormick gap, Sidon constants, degree-two polynomials, Walsh characters,
fractional orientations, and maximum subgraph density. The exact scope of every retrieved
paper was not fully audited. No claim of exhaustive coverage is made.

A significant alternative formulation is harmonic analysis. Let
`C(G)=sup_{a≠0} ||a||₁/||Σ_ij a_ij s_i s_j||∞`. These are real Sidon constants for the
edge-indexed degree-two Walsh characters. Because the polynomial has mean zero,

```
||f||∞/2 ≤ osc(f)/2 = R(H) ≤ ||f||∞.
```

Thus signed cut-range constants and these Sidon constants differ by at most two. A
separate agent was assigned that literature search; its findings should be incorporated
before any publication-level novelty claim. More informative than clique-family
sharpness would be a graph-by-graph lower bound from random signs on a densest induced
subgraph. This direction was passed to the root agent.
