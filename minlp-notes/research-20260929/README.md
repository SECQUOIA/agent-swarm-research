# September 29 continuation: structure-exploiting branch-and-bound

Start with the [synthesis](SYNTHESIS.md). The program definition is in
[PROGRAM.md](PROGRAM.md) and decisions are logged in
[root-research-log.md](root-research-log.md). "Reviewed" means checked by an
independent research agent, not journal peer review.

## Main line: single-tree versus decomposition-aware branch-and-bound

| Note | Content | Verification |
|---|---|---|
| [theory-face-exact/face-exact-exponential.md](theory-face-exact/face-exact-exponential.md) | `0.57 (5/3)^n` leaves for single-tree B&B with termwise McCormick on a path with a unique nondegenerate minimizer; per-factor envelopes; factorization dependence; chordal escapes | [review](reviews/face-exact-review.md), [recheck](reviews/face-exact-recheck.md) |
| [theory-decomposition/decomposition-certificates.md](theory-decomposition/decomposition-certificates.md) | decomposition certificates; instance-dependent `O(\|T\| C^{w+1} log(\|T\|/eps))`; slope lower bound; width lower bounds; separation theorem; exactness of split-optimized relaxations on trees | [review](reviews/decomposition-review.md), [recheck](reviews/decomposition-recheck.md), [non-dyadic check](reviews/decomposition-nondyadic-check.md) and confirmations [r1](reviews/decomposition-nondyadic-confirm-r1.md), [r2](reviews/decomposition-nondyadic-confirm-r2.md), [r3](reviews/decomposition-nondyadic-confirm-r3.md) |
| [theory-decomposition/extension-adaptive.md](theory-decomposition/extension-adaptive.md) | adaptive algorithm without `x*` (Theorem A.5, Proposition A.6); Conjecture 3.7 lower half true/false by exponent; new lower bound | [review](reviews/decomposition-adaptive-review.md), [confirmation](reviews/decomposition-adaptive-confirm-r2.md) |
| [theory-decomposition/covering-upper-half.md](theory-decomposition/covering-upper-half.md) | round 3: graded exact splits and a margin-discounted sandwich; upper half of the covering characterization in the exact-bag model for trees with one-dimensional separators; one-edge band-bracket refinement can stall; certificates only in part | [review](reviews/covering-upper-half-review.md), confirmations [r1](reviews/covering-upper-half-confirm-r1.md), [r2](reviews/covering-upper-half-confirm-r2.md) |
| [theory-decomposition/adaptive-matching.md](theory-decomposition/adaptive-matching.md) | round 4: algorithm GR matches Theorem 3.4 without `x*` on path decompositions with `∇F(x*) = 0` (localization lemma); trees open; bound-driven covering rule needs `Omega(n^{3/2} log(1/eps))` cells on a strongly convex quadratic path | [review](reviews/adaptive-matching-review.md), confirmations [r1](reviews/adaptive-matching-confirm-r1.md), [r2](reviews/adaptive-matching-confirm-r2.md) |
| [theory-robust-lb/robust-lower-bound.md](theory-robust-lb/robust-lower-bound.md) | split-robust exponential lower bound (qualitative; bases about 1.003–1.05) | [review](reviews/robust-lb-review.md), [recheck](reviews/robust-lb-recheck.md), [confirmation](reviews/robust-lb-confirm-r1.md) |
| [theory-robust-lb/robust-chains.md](theory-robust-lb/robust-chains.md) | round 4: no split-robust bound growing with `n` on symmetric uniform chains (nondegenerate case) for split classes containing the balanced split; chiral chains give a gadget-free split-robust exponential bound with tiny bases | [review](reviews/robust-chains-review.md), confirmations [r1](reviews/robust-lb-chains-confirm-r1.md), [r2](reviews/robust-lb-chains-confirm-r2.md), [r3](reviews/robust-lb-chains-confirm-r3.md), final [confirmation](reviews/robust-lb-chains-final-confirm-r1.md), [nits](reviews/round4-nits-confirm.md) |
| [theory-consistency/consistency-relaxations.md](theory-consistency/consistency-relaxations.md) | function-class consistency relaxations: exact one-separator identity (gap = 2 × distance to the band of exact splits), tree sandwich, kink bound, h/p/hp comparison | [review](reviews/consistency-review.md), [recheck](reviews/consistency-recheck.md), [confirmation](reviews/consistency-confirm-r1.md) |
| [theory-coupling/coupling.md](theory-coupling/coupling.md) | tree-structured nonlinearity plus dense linear coupling rows (modest, largely negative) | [review](reviews/coupling-review.md), [recheck](reviews/coupling-recheck.md) |
| [theory-calibration/scouting.md](theory-calibration/scouting.md) | discrete calibrations (verification functions) for transcribed control problems; affine class; transfer theorem | [review](reviews/calibration-review.md), [recheck](reviews/calibration-recheck.md), [confirmation](reviews/recheck-calibration-confirm.md) |
| [theory-bangbang/report.md](theory-bangbang/report.md) | window law at bang-bang switches (tangential vs non-tangential calibrations); optcdeg2 closed | [verification](reviews/bangbang-verification/verification-report.md), [confirmation](reviews/bangbang-root-fixes-confirm-r2.md) |
| [theory-bangbang/extension-n2.md](theory-bangbang/extension-n2.md) | state dimension at least 2: the `eta_L` criterion; counterexample to the "no conjugate point" reading | [review](reviews/bangbang-n2-review.md), [confirmation](reviews/ext-bangbang-n2-confirm.md) |
| [theory-bangbang/window-exactness.md](theory-bangbang/window-exactness.md) | round 3: window exactness decided by the sign of `kappa_tau = b(x*(tau))^T w` (no window, one `O(1)` window, or failure for `o(1/h)` windows) | [review](reviews/window-exactness-review.md), confirmations [r1](reviews/window-exactness-confirm-r1.md), [r2](reviews/window-exactness-confirm-r2.md), [r3](reviews/window-exactness-confirm-r3.md) |
| [theory-bangbang/singular-arcs.md](theory-bangbang/singular-arcs.md) | round 3: calibrations on singular arcs (tangency implies Goh's condition; Kelley's condition); Euler sign criterion; accessory symbol and catmix chattering (heuristic) | [review](reviews/singular-arcs-review.md), confirmations [r1](reviews/singular-arcs-confirm-r1.md), [r2](reviews/singular-arcs-confirm-r2.md), [r3](reviews/singular-arcs-confirm-r3.md) |
| [theory-bangbang/kappa-negative.md](theory-bangbang/kappa-negative.md) | round 4: `kappa_tau < 0` (LQ data): only `epsilon`-certificates from node-specific `kappa`-limited calibrations, exact certificates from lifted calibrations on the scalar toys; several switches, close switches, terminal rows | [review](reviews/kappa-negative-review.md), confirmations [r1](reviews/kappa-negative-confirm-r1.md), [r2](reviews/kappa-negative-confirm-r2.md), [r3](reviews/kappa-negative-confirm-r3.md), final [confirmation](reviews/kappa-negative-final-confirm-r1.md), [nits](reviews/round4-nits-confirm.md) |
| [computation/scaling-study.md](computation/scaling-study.md) | SCIP 10 versus a chain DP B&B prototype (to `n = 8192`) | [review](reviews/computation-review.md) |
| [literature/decomposition-bb-prior.md](literature/decomposition-bb-prior.md) | prior-work audit (AND/OR search, MILP separations, two-stage and nested decomposition, Bienstock–Muñoz, ETH obstruction) | audit |
| [treewidth-census/census-report.md](treewidth-census/census-report.md) | treewidth census of MINLPLib | root computation; not independently reviewed |

## Certificates for open MINLPLib instances

Consolidated table: [open-instances-summary.md](open-instances-summary.md).

| Note | Content | Verification |
|---|---|---|
| [open-instances/open-instances-report.md](open-instances/open-instances-report.md) | lnts50–400, dtoc5, camshape100–800, lukvle10, optcdeg2 | [verified](reviews/open-instances-verification/verification-report.md) |
| [open-instances-scout/targets.md](open-instances-scout/targets.md) | best single-solver bounds for 283 low-width instances; 146 open | scouting |
| [open-instances-wave2/small/report.md](open-instances-wave2/small/report.md) | hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050; pindyck (first attempt failed; closed by the extension below); invalid LINDO bounds | [verified](reviews/wave2-small-verification/verification-report.md) |
| [open-instances-wave2/cops/report.md](open-instances-wave2/cops/report.md) | chain50–400, catmix100–800 | [verified](reviews/cops-verification/verification-report.md), [catmix400/800](reviews/catmix-recheck.md) |
| [open-instances-wave2/waterno2/report.md](open-instances-wave2/waterno2/report.md) | waterno2_06–24 improved; SCIP 10.0.2 wrong optimal values on period subproblems | [verified](reviews/waterno2-verification/verification-report.md), [all periods](reviews/waterno2-recheck.md) |
| [open-instances-wave2/waterno2/separator-branching.md](open-instances-wave2/waterno2/separator-branching.md) | round 3: waterno2_06 dual 263.735 → 272.584 (gap 3.78%) by branching on the tank-level separators | [verified](reviews/waterno2-sepbranch-review.md) (all pair bounds re-bounded) |
| [open-instances-wave2/waterno2/cell-slopes.md](open-instances-wave2/waterno2/cell-slopes.md) | round 4: waterno2_06 dual 272.584 → 278.230 (gap 1.67%) with cell-dependent slopes | [verified](reviews/waterno2-cellslopes-review.md) (all pair bounds re-bounded), [confirmation](reviews/waterno2-cellslopes-confirm-r1.md) |
| [open-instances-wave2/small/pindyck-extension.md](open-instances-wave2/small/pindyck-extension.md) | pindyck closed (concavity on a polytope containing the feasible set) | [verified](reviews/pindyck-review.md) |
| [open-instances-wave3/report.md](open-instances-wave3/report.md) | KAN family (relaxation certified; models exactly infeasible), powerflow0030p, ann_cumene_tanh, eg_* (failed in wave 3; closed by the round-4 retry below) | [verified](reviews/wave3-verification/verification-report.md) |
| [open-instances-wave3/ann/extension.md](open-instances-wave3/ann/extension.md) | round 3: ann_cumene_tanh dual −4024.495 → −3386.5403 (gap 0.194%) | [re-certified](reviews/ann-extension-review.md) |
| [open-instances-wave3/eg/retry.md](open-instances-wave3/eg/retry.md) | round 4: eg_int_s, eg_disc_s, eg_disc2_s closed to 1e-9 relative (Taylor models with signed cancellation) | [verified](reviews/eg-retry-review.md), confirmations [r1](reviews/eg-retry-confirm-r1.md), [nits](reviews/round4-nits-confirm.md) |
| [open-instances-wave3/powerflow/extension-report.md](open-instances-wave3/powerflow/extension-report.md) | powerflow0039p/0039r closed (leaf-bus identity plus vertex cuts) | [verified](reviews/powerflow0039-review.md) |
| [bound-audit/audit-report.md](bound-audit/audit-report.md) | validity audit of all MINLPLib listed dual bounds: 19 proven invalid on 15 instances (11 beyond the 1e-6 convention, 8 tolerance-scale); tolerance effects in listed primal values | [verification](reviews/bound-audit-verification/verification-report.md) and [recheck](reviews/bound-audit-recheck.md) (together they confirm all 19), [confirmation](reviews/audit-confirm-r2.md) |

## Secondary line: singularity theory of node counts

| Note | Content | Verification |
|---|---|---|
| [rlct/rlct-node-complexity.md](rlct/rlct-node-complexity.md) | face-integral characterization for `C^{1,1}` objectives; RLCT law; counterexample at boundary minimizers; singular learning theory; order-`k` relaxations | [review](reviews/rlct-review.md), [recheck](reviews/rlct-recheck.md), [second recheck](reviews/rlct-recheck2.md) |

Some agents could not write report files; in those cases the root saved
their report text verbatim and says so at the top of the file. Only
targeted checks were run and CI was not inspected.
