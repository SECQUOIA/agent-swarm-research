# Stage 2 independent review 3

Date: 2026-09-09. Reviewed snapshot: `stage2-round1/paper-network-simplex`, with the frozen code in the sibling `code` directory available for context. Comparison snapshot: `stage1-accepted`. All paths below are relative to `paper-network-simplex/revision-20260909` unless stated otherwise.

**Verdict: accept Stage 2. No major or minor mathematical defect found.** I checked the entire mathematical development, with additional scrutiny of the universality construction, sparse Fibonacci family, and actual-coordinate coefficient transfer. I read the author audit and relevant evidence as leads, independently checked the source diff, and did not read other current-round reviewers' reports. No manuscript or production-code source was changed.

## Enumerated findings

1. **S2-R3-F0 — No actionable finding.** No false theorem, missing essential hypothesis, invalid coefficient transfer, or unsupported complexity implication was identified. There are no major or minor corrections requested by this review.

## Main proof checks

### Coordinate sections and necessary coefficients

`04-bounded-rank.tex`, Lemma `lem:section-facet`, lines 377–406: the two-dimensional local section hypothesis is sufficient for the asserted invariance. A valid affine equation must vanish identically on the free coordinate plane, since the section contains a two-dimensional open subset there. At a boundary point, some nonconstant restricted inequality in any finite description must be active. Feasible motions in both tangent directions force that inequality's free-coordinate normal to be proportional to the local boundary normal. The interior side fixes the positive sign. This establishes the stated conclusion even if the ambient polytope has a nontrivial affine hull; it does not assume facets survive projection.

The five-product K4 example fixes all original coordinates other than its two selected products. Its explicit witness has the right aggregate and observed entries and fits the stated scaled capacities throughout the local neighborhood. It therefore supplies the full local half-plane required by the lemma, not only a necessary inequality. The rank-three sharpness claim consequently addresses original product coefficients, including alternative representatives obtained by adding affine equations.

### Universality and primary-source hypotheses

`05-universality.tex:18–92`: the transfer begins with a nonempty bounded rational polytope in nonnegative coordinates. Adding slacks produces a bounded standard-form extension, and clearing equation denominators preserves its original coordinates. I rechecked De Loera–Onn Theorem 1.1, its definition of representation, and the Section 3.3 injection. The source gives a coordinate-erasing bijection and places the injected coordinates in the first table layer. Composing the earlier injections and retaining the original coordinates rather than their slacks therefore provides precisely the needed cells. The theorem is polynomial-time, not strongly polynomial-time; the manuscript only claims the former. [De Loera–Onn primary article, printed pages 807 and 816–818](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf).

I checked the subsequent network construction directly. The padding forces old–new cross cells to zero and fixes one extra entry per layer to one, without altering the original designated cells. Hence all three layer masses are positive. Fixing aggregate flows sets the cell totals; fixing both explicit labels on boundary arcs sets their row and column margins. Subtraction gives the residual margins. Conversely, any feasible table yields all three state flows. Each nonnegative entry and boundary flow is bounded by its layer's total mass, so the uniform capacity `B` enforces exactly the required scaled upper bounds and excludes no table. The selected interior cells are the only original coordinates left free.

`05-universality.tex:94–133`: common normalization by `B` gives the same ratio `M` on the triangle's sloping edge. The fixed section constants are not data of the original nonlinear network model. Polynomial output size in `log M` is sufficient for the claimed superpolynomial integer coefficient magnitudes. The text correctly distinguishes magnitudes from encoding lengths and makes no separation-hardness or extension-complexity inference. The unit acyclic flow argument also justifies the claim that the resulting hulls are 0/1 polytopes; fractional coordinate sections need not be integral.

### Balanced incidence and Fibonacci growth

`06-series-parallel.tex:27–94`: positivity of the balancing vector converts the profile inequalities into the required section half-plane. In the converse, `alpha^T(-delta+tau)=0` gives zero change in total profile. The displayed neighborhood bounds both the profile perturbation and the one row correction. Every prescribed observed value remains below its state profile, and the selected unobserved entry in row `s` can absorb `tau_s` while staying nonnegative. Thus all state bounds, balances, aggregate flows, and observations hold, including equality on the section line. The proof gives local sufficiency as well as necessity.

`06-series-parallel.tex:139–215`: the column differences impose the Fibonacci recurrence, and the last column removes the remaining homogeneous degree of freedom, establishing invertibility of `D`. The positive balancing vector satisfies `D^T alpha=gamma*1`. The complement remains invertible because `sum(alpha)>gamma`; its balancing constant is positive. Passing to that complement makes the *observed* cells the `5q-4` ones of `D`, while leaving the coefficient ratio intact. The selected free cells in rows `P_q` and `P_1` exist and are actual retained coordinates. Graph counts, cycle rank, and the width-two decomposition agree with the construction. Exponential growth is in `q`; the text correctly derives superpolynomial magnitudes in the explicitly encoded input length `O(q log q)`.

`06-series-parallel.tex:217–244`: splitting each internal join and subdividing each `b_i` adds exactly the stated vertices and arcs. It removes parallel edges and reduces the maximum undirected degree to three. Each old flow, separately in every state, extends uniquely through the new arcs. Fixing their aggregate coordinates in the section leaves exactly the same two free products. Thus the new coordinates do not provide a way to alter the section ratio.

### Remaining mathematical development

I checked the remainder against the full proof reading performed in Stage 1 and reexamined the essential dependencies in this frozen snapshot. The independently generated diff confirms that only the two author-reported passages changed.

- **Disaggregation and blocks:** finite capacities force zero-weight state flows to zero; a positive state exists even for the empty-base equivalence. Fundamental cycles stay within cyclic blocks, including loops and parallel-edge cycles. The gluing proof uses one global weight vector and restores absent states proportionally, without coupling articulation deviations. The integral-flow corollary does not claim an integral `m+1` decomposition bound.
- **Compression:** fixed-arc removal uses the nonempty-base assumption; averaging strictly interior coordinate witnesses proves the reduced affine-hull statement. Network minors and Schur complements justify the unit coefficients. Observation restriction has precisely the unobserved circulation space as its kernel. The individual-product minimum is stated for locally observed block/label pairs on the ambient circulation space. State and residual capacity inequalities are preserved.
- **Structured oracles:** local theta feasibility is checked before summing supports; segment, point, and empty-sum cases are covered. Parallel-path feasibility follows from the shifted transportation cut system, including nonnegative row targets and the zero-total case. Active branch selection produces globally valid cuts. The revised default cycle-coordinate *vector* terminology accurately describes compact recovery.
- **Bounded rank:** local positive circuits are unit by TU. The edge-direction proof includes affine-hull equalities when the state slice is lower-dimensional. Coordinate hyperplanes make arrangement chambers pointed, so finitely many ray support tests suffice. Transforming the defining directions by the unimodular basis gives the multiplier bound without an extra rank factor. Basis enumeration provides recovery even in degenerate intersections. The stated `2^{O(r^2)}` versus `2^{O(r^3)}` factors and the additive denominator-length argument are consistent with the algorithms.
- **Fixed-label chains:** the residual elimination uses that state zero is unobserved. The expanded three-label circuit classification handles the one-negative-singleton case and all singleton/pair covers explicitly. The four families have `7+5+3+1` circuits. The doubled weight occurs only on the negative-full row, which contains no products. Each exceptional bypass coefficient has a selected endpoint from a distinct gadget, making the proposed flow-balance repair valid without creating another doubled flow coefficient. The four-label lower bound uses a genuine coordinate section. The final merger correctly replaces the parameter by the number of observed labels and distinguishes compact from dense output.

## Independent executable evidence

I wrote `stage2-review3-evidence/fibonacci_facets.py` without importing production implementations, author-audit programs, or historical verification code. It constructs the sparse observation pattern and independently enumerates every path–simplex vertex. A floating-point LP proposes a supporting row with the claimed two product coefficients; **all acceptance checks are exact rational arithmetic**. The script verifies the inequality at every vertex, its tight-face affine rank, zero free-product coefficients in every affine-hull equation, and exact exclusion of a small outward section perturbation.

| Instance | Enumerated vertices | Hull dimension | Tight-face dimension | Exact product ratio |
|---|---:|---:|---:|---:|
| Fibonacci `q=3` | 198 | 22 | 21 | 2 |
| Fibonacci `q=4` | 1,032 | 31 | 30 | 3 |

Both supporting rows are therefore actual relative facets of their sparse hulls. The script also independently constructs the simple graph for each instance, checks uniqueness of directed arcs, maximum undirected degree three, the counts `(15,20)` and `(21,28)`, the unchanged cycle rank, and exact balance preservation for all 33 and 129 old paths respectively. Full rational normals, right-hand sides, and results are retained in `fibonacci_facets.json` and `fibonacci_facets-output.txt`.

This is finite corroboration of the facet and graph claims. The asymptotic Fibonacci theorem and universality theorem rest on the reviewed proofs, not these two computations.

## Build, evidence inspected, and limitations

- `stage2-review3-evidence/source.diff` and `source-changes.json` independently identify the two changes from accepted Stage 1: `03-structured-oracles.tex` and `07-fixed-state-chains.tex`.
- A private `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` build succeeds at 50 pages. The final log has no warnings, undefined references/citations, overfull boxes, or underfull boxes. The private build is under `stage2-review3-evidence/build`.
- I read `stage2-author.md`, its source diff, and its independent-math output, while checking the substantive proof claims directly. Author-reported historical check counts were not treated as independent certification.
- I did not reimplement the complete De Loera–Onn universality algorithm. The imported theorem and first-layer coordinate property were checked in its primary article; the additional sparse network embedding was reviewed directly.
- I did not enumerate every possible graph, observation pattern, or bounded-rank library, and did not rerun production benchmarks. No timing or software-certification conclusion is added by this mathematics review.
- This review uses mathematical source inspection and build logs, not a full rendered-page visual audit. I did not coordinate with other reviewers or inspect their current reports.

## Optional preferences

None. No additional exposition change is needed for acceptance from this review.

**Final verdict: accept Stage 2; no major or minor findings.**
