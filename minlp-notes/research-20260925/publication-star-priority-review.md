# Publication priority review: subsetwise moments for indicator quadratics on stars

Review date: 2026-09-25. This is an independent source and significance audit,
not a new proof audit. It covers the accepted claims in
[the quantitative theorem](star-subset-accuracy-lower.md),
[the uniformly conditioned construction](star-uniform-condition-subset-gaps.md),
and [the moment transfer](tree-indicator-moment-gluing.md).

The defensible contribution is a specific transfer and its quantitative
consequence: a relaxation of an original indicator-quadratic epigraph can
pass every prescribed subset-parent test and still have a certified gap,
with rational polynomial-length input, fixed spectral bounds, bounded means,
and bounded positive true cost. None of the examined sources states that
combination. This is a scoped comparison, not proof of publication priority.

Several ingredients are established theory. In particular, the subsetwise
compatibility hierarchy, arbitrary-order qubit incompatibility, conversion
of incompatibility into an optimization advantage, and inverse-square
planar approximation effects must not be presented as new.

## Exact object under comparison

The relaxation shares one real symmetric center matrix `M` and binary
marginals `M_i` across all subsets. For every `J` with `|J| <= k`, it has
its own positive semidefinite parent matrices `G_S^J` summing to `M` and
with marginals `M_i`. Parents on different subsets need not have the same
higher-order marginals on intersections. When `M` is positive definite,
congruence by its inverse square root makes this precisely an intersection
of binary real-qubit joint-measurability conditions. It is not a general
moment hierarchy with overlap consistency.

The strongest rational theorem has `2k` leaves, `I/39 < Q < 12I`, input
length `O(k^2 log(k+1))`, and a relative epigraph gap at least
`1/(56920320 k^2)`. The main novelty candidate is the simultaneous
optimization realization and normalization, including an affine inequality
in the original variables that separates the relaxed point. Mere separation
in auxiliary moment space would not suffice.

## Quantum compatibility sources examined

1. **Common positive semidefinite parents and matrix-convex geometry.**
   Bluhm and Nechita, *Joint measurability of quantum effects and the matrix
   diamond*, Journal of Mathematical Physics 59, 112202 (2018);
   [arXiv:1807.01508v3](https://arxiv.org/html/1807.01508v3),
   version dated 2018-09-26, Theorem 5.3 and its proof.
   The source explicitly identifies joint binary measurements with positive
   semidefinite matrices indexed by Boolean outcomes, with their sum and
   one-coordinate marginals prescribed. Thus the normalized parent cone and
   its matrix-convex interpretation are prior work. Interpreting its real
   `2 x 2` matrices as scalar second moments is elementary; it should be
   introduced as the bridge to the optimization model, not a newly discovered
   quantum cone.

2. **The same subsetwise compatibility notion.**
   Sun, Wang, Li-Jost, and Fei, *A Note on the Hierarchy of Quantum Measurement
   Incompatibilities*, Entropy 22(2), 161, published 2020-01-30;
   [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7516579/),
   DOI [10.3390/e22020161](https://doi.org/10.3390/e22020161), Section 2,
   definitions preceding Proposition 1 and equations (1)--(7).
   Their `(n,k)`-compatibility means that every `k`-member subfamily is
   compatible. They discuss its hierarchy and noise thresholds. After
   normalization, this is exactly the compatibility condition imposed here.
   They do not give the original-variable positive-definite star epigraph
   lower bound. The local relaxation architecture therefore has an existing
   name and must not be claimed as a new abstract hierarchy.

3. **Arbitrarily large minimal incompatible planar families.**
   Andrejic and Kunjwal, *Joint measurability structures realizable with qubit
   measurements: Incompatibility via marginal surgery*, Physical Review
   Research 2, 043147 (2020);
   [arXiv:2003.00785](https://arxiv.org/html/2003.00785),
   Corollaries 7--8, especially equation (93).
   For every `N`, their real planar binary qubit family can be incompatible
   while all its proper subsets are compatible. The published interval
   between the full-family and proper-subset thresholds directly supplies
   the initial Specker examples used in the local notes. Arbitrary-order
   incompatibility itself is wholly prior. The short-arc construction is
   used here to retain uniform quadratic conditioning and bounded data
   after the star transfer.

4. **Generic incompatibility-to-optimization transfer.**
   Carmeli, Heinosaari, and Toigo, *Quantum Incompatibility Witnesses*,
   Physical Review Letters 122, 130402 (2019);
   [arXiv:1812.02985v2](https://arxiv.org/html/1812.02985v2),
   Theorems 1--2, represent incompatibility witnesses through discrimination
   tasks. Their explicit presentation uses pairs and notes the extension to
   finite collections. The strongest direct arbitrary-family comparator is
   Skrzypczyk, Šupić, and Cavalcanti, *All sets of incompatible measurements
   give an advantage in quantum state discrimination*, Physical Review
   Letters 122, 130403 (2019);
   [arXiv:1901.00816v1](https://arxiv.org/html/1901.00816v1),
   dated 2019-01-03, equation (5). Their optimized discrimination advantage
   equals one plus incompatibility robustness. Accordingly, a generic claim
   that quantum incompatibility produces an optimization gap adds nothing.
   The proposed addition is realization by a fixed-mean indicator quadratic
   with star sparsity, positive definiteness, and quantitative uniform bounds.

5. **Planar geometry and an earlier inverse-square-root lower bound.**
   Zhang, Zhang, and Chitambar, *Cost of Simulating Entanglement in Steering
   Scenario*, [arXiv:2302.09060v3](https://arxiv.org/html/2302.09060v3),
   dated 2025-02-01, Section 4, Proposition 4, Corollary 2, and Appendix A.
   Their compatible regions are planar zonotopes of perimeter four.
   Proposition 4 uses `n^-1 cot(pi/(2n))`; Corollary 2 gives a lower bound
   proportional to `(2/pi-r)^(-1/2)` on parent-measurement outcome count.
   This is a close geometric precedent for the exponent in the present
   accuracy result. The parameters differ: their resource is the number of
   outcomes in one global parent; ours is the maximum number of leaves
   simultaneously checked by separate parents. Neither parameter can be
   substituted for the other. The exponent two and the underlying curvature
   calculation carry no independent novelty claim.

6. **General unbiased qubit compatibility is already characterized.**
   Grinko and Uola, *On compatibility of binary qubit measurements*,
   [arXiv:2407.07711v1](https://arxiv.org/html/2407.07711v1),
   dated 2024-07-10; journal version *Compatibility of Binary Qubit
   Measurements*, Physical Review Letters 135, 200201 (2025),
   [DOI](https://doi.org/10.1103/vv1h-5mf9).
   Theorems 1--2 provide a complete Fourier-based criterion for any finite
   family of unbiased binary qubit measurements; Section VI explains its
   second-order cone formulation. Their counterexample to an angle-ordered
   polygonal-walk conjecture does not refute the local perimeter criterion:
   the latter uses the actual symmetric convex hull. The present work must
   not suggest that general unbiased joint measurability lacks a criterion.

7. **A strong positive approximation comparator.**
   Porto, Designolle, Pokutta, and Quintino, *Measurement incompatibility and
   quantum steering via linear programming*, Quantum 10, 2141, published
   2026-06-19; [arXiv:2506.03045v3](https://arxiv.org/html/2506.03045v3),
   dated 2026-06-10, equation (9), Theorem 1, and Section 3.3.
   A fixed polytope of `L` states gives an LP with `O(m q L)` variables and
   constraints for `m` measurements and `q` outcomes. Its depolarizing
   robustness error is controlled by `r^-1-1`, where `r` is the polytope's
   shrinking factor. Their hierarchy has polynomial dependence on measurement
   count and inverse accuracy for fixed dimension. It imposes a common
   global representation, not only small-subset parents. Consequently our
   lower bound is no barrier to efficient global compatibility approximation,
   and cannot be marketed as such. Transferring their robustness guarantee
   to the variable-center quadratic objective is a separate theorem not
   established by either comparison.

8. **Terminology warning: other “n-wise” hierarchies differ.**
   Tendick, Budroni, and Quintino, *Strict hierarchy between n-wise measurement
   simulability, compatibility structures, and multi-copy compatibility*,
   [arXiv:2506.21223v2](https://arxiv.org/html/2506.21223v2),
   dated 2025-07-07, Sections 4.2 and 5.
   They distinguish intersections requiring simultaneous subset compatibility
   from convex combinations of different compatibility structures, and from
   simulation with several measurements or copies. Their main strict
   inclusions concern those competing models. They should not be conflated
   with the intersection defining `R_k`. This source reinforces the need
   to state equations for the hierarchy instead of relying on its name.

## Indicator-quadratic competitors

The separate [indicator-source audit](publication-star-indicator-priority.md)
records theorem locations and full bibliography for the following comparisons.

- Bhathena, Fattahi, Gómez, and Küçükyavuz, *A parametric approach for solving
  convex quadratic optimization with indicators over trees*, Mathematical
  Programming, online 2025-05-02;
  [journal source](https://doi.org/10.1007/s10107-025-02222-3), Theorem 2,
  gives an `O(n^2)` time and memory algorithm for positive-definite tree
  instances. Hence a gap in this relaxation is not hardness of star or tree
  optimization. The algorithm depends on the objective; a single compact
  ideal formulation is a different question.
- Choi, Fattahi, Han, Gómez, and Lozano, *Convexification of mixed-integer
  quadratic optimization via decision diagrams*,
  [arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1),
  dated 2026-08-24, Section 7.2, Corollary 1, gives an exact tree SOCP of
  size `O(n^(ell+1))` with `ell` rooted leaves. The authors explicitly note
  exponential size on stars. Their Section 8 approximation result requires
  uniform graph-volume and boundary bounds; a growing star has a
  radius-one neighborhood of growing size. Neither their exact formulation
  nor their approximation theorem is contradicted by the local construction.
- Wei, Atamtürk, Gómez, and Küçükyavuz,
  [arXiv:2201.00387v2](https://arxiv.org/abs/2201.00387v2),
  dated 2022-11-27, supplies a general exact hull framework using an auxiliary
  polytope of padded principal-submatrix inverses. Such full-support
  information is stronger than the small-subset parent tests considered here.
- Liu, Fattahi, Gómez, and Küçükyavuz,
  [arXiv:2110.12547v1](https://arxiv.org/abs/2110.12547v1), Section 3,
  Example 1, already exhibits a four-node star where dropping an edge-square
  produces a loose relaxation. Thus even a general “first relaxation gap
  on a star” claim is false. Their relaxation differs from the present one.

## Publishability assessment and safe claim

The strongest candidate is a focused theorem about a natural but precisely
specified formulation strategy. Its substantive content is that a continuous
separator of dimension one and uniformly benign quadratic spectra do not
make subsetwise second-moment parents sufficient, even approximately at fixed
order. Projection to the original epigraph and the rational normalization
make this more than a restatement of qubit incompatibility.

A safe claim is: “Using established planar joint-measurability geometry, we
construct rational, uniformly conditioned indicator-quadratic stars whose
subset-parent relaxations have an explicit inverse-square lower bound on
relative epigraph error.” The literature comparison supports investigating
publication of that statement. It does not support “first quantum-to-MINLP
transfer,” a new compatibility hierarchy, a universal conic-size lower bound,
a sharp hierarchy convergence rate, or a new efficient algorithm.

The strict-gap examples, uniform-conditioning theorem, and rational accuracy
theorem belong in one contribution; presenting them as several unrelated
novel findings would inflate their significance. The highest-strength result
should lead. The smaller examples explain why projection and shared moments
matter. The scalar-moment closure argument and witness transfer are reusable
supporting lemmas.

On the examined evidence this is a credible specialized theoretical
contribution, with a narrower impact than a compact exact star hull or a
matching approximation theorem. Either of those extensions could add
substantially, but neither is required to make the existing lower-bound
statement complete. They remain open questions, not publication-readiness
requirements. No computational speedup, practitioner adoption of this precise
relaxation, or external peer-review validation has been established.

## Search and verification boundary

This audit read the cited primary theorem passages rather than relying only
on abstracts. Searches covered “joint measurability,” “k-wise” and “(n,k)
compatibility,” Specker structures, planar polygon and zonotope approximation,
state-discrimination witnesses, star/tree indicator hulls, and combinations
of quadratic optimization with compatibility. Later sources through
2026-09-25 were considered, including the final 2026 LP paper and the August
2026 decision-diagram preprint. Dates above use version metadata, not the
occasionally regenerated date printed inside arXiv HTML renderings.

The comparison found no theorem subsuming the full stated star realization.
That negative search result is not a novelty proof. This audit did not run
mathematical checks or CI and does not replace the independent proof reviews
linked by the main theorem. Further ordinary referee and priority scrutiny
remains part of publication, even after the repository package is complete.
