# Stage 2, round 1 — reviewer 12

Primary lens: hardness, positive-optimum amplification, complexity parameters, and construction versus optimization.

Major findings: 0
Minor findings: 0

I found no concrete major or minor defect in this review. The stage's main conclusions are supported by the arguments checked below. This is a bounded independent assessment, not a formal verification or a guarantee that no defect remains.

## Snapshot and coverage

I read all 1,546 lines of `sections/02-quadratic-finite.tex`, the process/protocol, bibliography, and coverage inventory, including all thirteen stage-2 canonical rows and six stage-2 supporting developments. I rechecked the stage-1 representation, parity, shared-prefix, covariance, principal-compression, shrinking, finite capacity, and rational-preview dependencies. I had independently read the entire stage-1 section in the previous review; unrelated smooth proofs were not reviewed anew for this round.

All six SHA-256 hashes matched `reviews/stage2-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `04faf5b34942a13d79028d42728aeb6443b34c66a575f8293bc546a1ec8fb47e` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `92931390c89c837f079fa63121c50d7fd2ad9b5ff7b4cab8ff88276f2206e177` |
| `references.bib` | `3dcfb568784b51d38f1255ff6135ecefa8be1b9c17b1fef7e8927764022bc900` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `2d6d05e3f346561242f44ecab130c9b01016b101bb4843eaeb11724eef7a9d2d` |

Original-source comparison included the complete `results/quadratic-integer-precision-approximation-hardness.md`, the rational-construction source's setup and analytic interfaces, and `notes/rational-block-logdet-convex-body-oracle.md` and `notes/covariance-determinant-optimality-certificates.md`. I independently reconstructed the remaining arguments from the manuscript, rather than rereading every corresponding repository result in full. Prior audit labels were not used as proof.

## Findings

None identified. In particular, I do not classify a deliberately loose constant, a conservative polynomial iteration bound, or a theorem left for a later stage as a defect without a concrete failure.

## Hardness assessment

I checked `lem:zero-count-maxcut` and `thm:count-hardness` in full.

- Coordinatewise convex maximization gives `max f_G = M(G)`. Complementary maximum-cut vertices have equal graph output, and their midpoint input has value zero. Thus a continuous convex lift cannot remove the zero-count obstruction. The strip LP proves the converse, including equality at the tolerance threshold.
- Choosing tolerance `k - 1/2` with `k >= 1` makes zero count equivalent to `M(G) < k`. The coNP-completeness claim is expressly confined to this family, whose complement has an ordinary cut witness. No general coNP-membership claim is made for arbitrary convex formulations.
- Replication creates an incompatible packing of size `2^t`. Any two different packing points have a coordinate block with graph midpoint error above its component tolerance. Selecting one exact lift per point and applying parity therefore proves `p >= t` for arbitrary integer ranges. The proof does not assume binary assignments or additivity of minimum integer dimension.
- Dividing each output by the positive rational `k - 1/2` preserves convexity, has polynomial encoding, and fixes every tolerance at one. The reduction need not compute a maximum cut: maximum-cut vertices occur only as witnesses in the proof.
- The appended output `8z^2` has minimum exactly one. Its endpoint midpoint error is two, and the supplied one-binary formulation has error at most one half. Its endpoints double the packing, giving the promised gap of one versus at least `t+1`.
- For fixed `0 < delta <= 1`, choosing a fixed integer `q > 1/delta` and `t = n^q` makes `C(tn+1)^(1-delta) < t` eventually. Both additive and positive-optimum multiplicative guarantees distinguish the cases solely by reading the output integer count. Replication and explicit rational data remain polynomial in the original instance size. The handling of finitely many small dimensions is legitimate.
- The manuscript correctly limits the consequence to fixed sublinear powers. It does not claim to rule out `N/log N`, prove a sharp linear lower bound, or transfer the componentwise reduction to a single total-absolute-error budget. The replacement of `N` by common nonlinear input rank follows in the stated power range because that rank is at most `N`.

The primary Garey–Johnson–Stockmeyer scan explicitly identifies simple Max-Cut with all edge weights one and states its NP-completeness in the abstract. This supports the imported starting problem. [Primary paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf).

## Checks across the rest of the stage

I independently checked the covariance scaling `Sigma/c_n`, the factor `1/8` in the shared-grid output error, and the determinant-to-count conversion. The certificate uses a geodesically convex Lagrangian and a valid distance bound from `det P`; its rational residual is nonnegative. The commuting reduction preserves earlier sign symmetries and does not assume ordinary diagonal deletion works for indefinite Hessians.

The rational noncommutative-rank proof now supplies the previously deferred obligations: rational shrinking coordinates, polynomial coordinate heights, dyadic depth accounting, and the capacity scaling power `D_H^(-2r)`. Combining the imported integral capacity estimate with the principal-slice volume gives the stated explicit lower bound. The claim remains construction-time, not MILP solution-time.

For the finite algorithm, I checked the exact penalty repair, trace-one gradient normalization, polynomial search radius, local inexact recurrence, and the rational grid sandwich. The trace-normalized energy gradient is positive semidefinite even for an indefinite Hessian, since it is a matrix square. The Jacobi argument uses a uniform absolute residual and exact rational orthogonality, not an eigenvalue-gap assumption. I checked the matrix-function perturbation estimates and the polynomial-denominator accounting at the level of the written proof; I did not implement the whole numerical algorithm.

For grouped and total-absolute-error budgets, the common residual matrix controls the entire error vector. The correlation-matrix repair is exactly feasible, and normalization by `tr Gamma` gives the required relative objective bounds. I checked GLS1981's original Definition (5), printed page 172: its objective guarantee compares against every point in the body, as the manuscript needs. Theorem (3.1) then supplies the weak-separation/optimization interface. The log-determinant hypograph has the stated interior ball, and its central-ball repair preserves exact feasibility even when the original budget body is unbounded.

I also checked the oracle ellipsoid centering argument, nonlinear output-image equivalence, common-input-kernel quotient, rational zonotope separator, and rational LDL normalization. The inner-volume term is retained. The PSD block proof uses positivity and unconditional domination at the necessary steps; the intrinsic block refinement relies on a product of zonotopes from genuinely disjoint input blocks. The diagonal, integer-feature, and forest constants follow from those specializations. The integer minor lower bound and the forest face-tiling argument give the asserted volume bounds. The thin-domain example preserves exact graph containment and demonstrates why independent-domain transfer is unavailable.

The cached Zhang–Sra Corollary 8 and DPV Theorem B.5 were checked directly for the specific imported inequalities and rounding interface. IQS's rational witness and field-extension statements and GGOW's integral capacity theorem were already checked from primary texts in the preceding stage review and were matched to their use here. This review does not claim a fresh full reading of all cited papers, a publication-priority audit, or inspection of the compiled PDF.

## Executed independent check

I wrote and ran `verification/reviewer12-stage2-hardness.py`, using exact rational arithmetic. It enumerates every simple graph through four vertices, checks all relevant integer thresholds, checks every pair in three replicated blocks plus the scalar-endpoint packing for each high instance, and checks both residual-square envelope endpoints and exact square values on a rational grid.

Result: **PASS — 280 graph/threshold cases, 21,600 augmented packing pairs, and 606 scalar-lift checks.** These finite checks supplement the general argument; they do not replace it.
