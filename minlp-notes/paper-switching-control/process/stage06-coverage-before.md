# Claim coverage and development map

This inventory tracks substantive results, rather than every historical search or repeated proof. Acceptance locators are filled as stages finish. Earlier result files sometimes retain obsolete statements of what was open; final theorems take precedence only after fresh verification.

| Repository development | Planned manuscript treatment | Stage |
| --- | --- | --- |
| `cia-uniform-switching-obstruction` | Uniform continuous optimum, exact integer recurrence, finite and asymptotic conjecture counterexamples, continuous one-switch minimax, three-cell formula | 1 |
| `cia-exact-two-switch-worst-case` | Analytic three-distinct-mode reach, full minimax, exact one-sided minimax | 2 |
| `cia-two-switch-equal-masses` | Exact equal-total minimax, including the sharper small-mode guarantee; not subsumed by unrestricted full minimax | 2 |
| `cia-universal-heavy-mode-rounding` | Integral prefix rounding, first-repeat reordering, universal heavy-mode theorem, exact one-sided reduction | 2 |
| `cia-general-four-block-reach` | Complete event relaxation and symmetry coverage, finite and polynomial certificates, full reach consequence | 2 |
| `cia-exact-three-switch-worst-case` | Full minimax, plateau transition, asymptotics | 2 |
| `cia-five-mode-four-block-reach` and four-mode three-block certificates | Explicitly subsumed positive cases; retain independent verification where useful, avoid duplicate main proofs | 2 |
| `cia-adjacent-repeat-investigation` | Counterexamples to prescribed heavy mode and prescribed pair position; investigate surviving strengthening as appropriate | 2–3 |
| `cia-distinct-reach-investigation` | Exact three-mode/three-distinct-block counterexample, explaining spare-mode hypothesis | 2 |
| `cia-three-switch-heavy-mode` | General heavy theorem subsumes specialized proof; retain all-light greedy lemma and its extra boundary implications | 2–3 |
| `cia-two-switch-global-upper` | Preserve third-largest-total sufficient condition if not subsumed; document earlier global bound as dominated by final exact theorem | 3 |
| `cia-three-switch-global-upper` | Certificate-free four-block upper obtained from three-block seed, including its exact plateau and asymptotic comparison | 3 |
| `cia-arbitrary-block-one-sided-bound` | Mode removal, closed coefficient, equal-total and one-sided consequences | 3 |
| `cia-arbitrary-switch-global-bound` | Full arbitrary-profile bound, exact plateau, sharp first correction | 3 |
| `cia-seeded-arbitrary-switch-bound` | Unclipped minimum/maximum-mass recurrence, four-block seed, extra plateau, improved second-order gap | 3 |
| `cia-many-mode-switching-investigation` | Dimension-free limit, classical attribution, general exclusion recurrence and its precise unresolved premise | 3 |
| `cia-reopened-general-reach` | Investigate five-block route; exact nonphysical relaxation witness and rigorous boundary if still unresolved | 3 |
| `cia-finite-grid-one-switch-minimax` | Both LP reductions, explicit formula, compressed extremizers, bit complexity, retained failed simplification | 4 |
| `cia-exact-three-mode-one-switch` | Explicit residue-class formula and sharp witnesses or derivation from general formula, including N=1 exception | 4 |
| `cia-five-interval-two-switch-minimax` | Exact chamber enumeration, boundary continuity, pure lower witness, published Corollary 5 correction | 4 |
| `cia-fixed-switch-budget-algorithm` | One-switch dominance, crossing rule, fixed-prefix suffix rule, subset DP, candidate labels, dwell contracts | 5 |
| `cia-sharp-grid-transfer` | Supported prefix rounding and chronology, strict sharp uniform transfer, binary nonuniform refinement, source's half-grid argument | 5 |
| New certified coarsening consequence | Exact additive certificates, rational preprocessing, input/accuracy complexity, implementation and independent checks | 5–6 |
| Existing exact public-profile computations | Fresh reproduction with pinned input and fair comparable grids | 6 |
| Computational development | Accuracy-grid certificates, scaling and controlled exact comparisons; state/objective evidence only if actually developed | 6 |
| Literature and source corrections | Primary-source locators and exact quantifiers, established ingredients credited, no proof-of-priority claim | 1, 4–6 |

## Completion criterion

Every row must have an explicit final disposition and manuscript locator. A result is not omitted simply because another statement has a similar title. Stronger hypotheses can support stronger conclusions. Searches that failed to find a counterexample are not proofs. Open problems may remain as clearly stated research questions, but manuscript theorems and algorithms must be complete and independently reviewed.

## Accepted coverage locators

- Stage 1 (`stage01-accepted`): `sections/01-foundations.tex` establishes the common model, compactness, attained extrema, and cell-averaging comparison. `sections/02-uniform-one-switch.tex` contains `thm:uniform`, `thm:uniform-grid`, `thm:one-switch`, `cor:one-switch-grid`, `prop:three-cells`, and the two published-conjecture counterexamples. These cover the uniform obstruction row and the initial literature correction. Final bibliography synthesis remains stage 6.

## Developments to carry into later reviewed stages

During independent stage 2 review, reviewer 02 obtained exact primal and dual certificates for all 972 word/time-cell LPs of the strengthened three-mode example. The exact one-sided instance optimum is reported as 18673/18396, attained by word 021 at times 8341/4599 and 17639/4599. The primary agent subsequently derived an analytic exact-value proof, independently confirmed by reviewer 02. Stage 2 is being strengthened before acceptance and will receive a fresh five-reviewer round; see stage02-round01-adjudication.md. The reviewer’s optimization remains independent corroboration rather than the intended proof dependency. Stage 6 can use the accepted exact value as a reproducibility case.

Stage 5 may develop the elementary finite word/time-cell LP decomposition for piecewise-affine cumulative inputs as an exact continuous-instance benchmark. This would explain and verify the above audit and distinguish exact continuous optimization from grid restriction. Attribute switch-time enumeration as established; any claimed complexity and new implementation must be proved and reviewed in stage 5. The principal grid algorithm retains its better mode-count dependence.

- Stage 2 (`stage02-accepted`): `03-heavy-and-reach.tex` (`thm:heavy`, `lem:prefix-repeat`, `lem:first-repeat`, `thm:one-sided-reduction`, `lem:reach-two`, `thm:reach-three`); `04-four-block-certificates.tex` (`thm:reach-four`, `lem:weighted-pair`, complete event/certificate subsections); `05-small-budget-minimax.tex` (`thm:small-one-sided`, `thm:small-full`, `cor:equal-masses`, plateau/asymptotic subsection, `prop:three-mode-failure`, both adjacent-pair counterexamples). The original n3 distinct failure is strengthened to exact all-word instance optimum 18673/18396 with an analytic proof and matching schedule. Earlier n4/n5 certificate cases are explicitly subsumed and bundled as optional independent checks. The largest-heavy-mode strengthening is accurately distinguished as unused and unproved; its surviving status does not support any theorem. General all-light/predecessor bounds remain assigned to stage 3.

## Candidate development for stage 4: exact continuous three-mode/two-switch boundary

The accepted stage-1 cell-averaging comparison gives F_cont<=F_grid. If stage 4 freshly verifies the existing five-cell theorem F_grid(3,5,s=2)=Delta, scaling immediately yields F_{3,2}(T)<=T/5 for arbitrary measurable input. There is a simple matching candidate lower witness that deserves independent author/reviewer checking: on T=5 take successive pure modes 0,1,2,0,1, each for one unit. Terminal masses are (2,2,1), and each mode first accumulates one unit at times d=(1,2,3). If full error E<1 were possible with at most three blocks, all three modes must be used, hence each exactly once. For whichever mode i is last, its start v must be less than d_i (otherwise its unserved allocation is already1), while its terminal negative-error inequality requires v>=5-m_i-E>5-m_i-1. But 5-m_i-1=(2,2,3)>=d_i for every i, a contradiction. Thus error>=1. The word012 with switches at2 and4 attains1. Combined with the reviewed five-cell upper, this would establish F_{3,2}(T)=T/5, extending the continuous two-switch result to the boundary n=k=3. Verify source attribution before describing it as new: the published conjecture's continuous second branch predicts this value and may already provide its lower construction. This is a candidate note for the next stage, not an accepted theorem or a dependency of stage 3.

## Stage 3 accepted coverage (`stage03-accepted`)

- `06-general-budgets.tex`: `lem:mode-removal` proves both mass choices and the
  constant-mode branch; `thm:general-coefficient`, `cor:general-bounds`,
  `cor:general-plateau`, and `prop:general-asymptotics` cover the arbitrary-block
  and arbitrary-switch results. `thm:seeded`, `cor:seed-consequences`, and
  `prop:seed-series` cover the unclipped four-block seed and general seed
  propagation, an integer plateau test, the n16 four-switch plateau, and all
  established-seed second-order gap formulas.
- `07-predecessors-and-frontier.tex`: `lem:all-light`, `cor:light-boundaries`,
  and `prop:dimension-free` retain the light-input reach result and develop
  the exact equal-mass instance band `(n-k)^2<=k`. `prop:analytic-four-upper`
  gives the certificate-free rational predecessor and its n5–11 plateau;
  `lem:third-mass` retains the useful input-dependent three-block condition.
  Specialized heavy results and the older two-switch global coefficient are
  explicitly subsumed, with their original verification retained.
- `lem:general-exclusion` identifies the exact higher-block missing premise.
  Subsection `subsec:negative-relaxation` specifies and exactly checks the
  nonphysical n6 witness. `lem:event-interpolation` distinguishes trajectory
  realizability from inverse reach identities. `prop:chronological-chamber`
  newly proves the target weighted bound for one fixed chronological chamber
  using a rational dual and uniform-control primal. Other chambers and the
  general five-block reach theorem remain unresolved and unused. The separate
  largest-heavy adjacent-pair strengthening is also explicitly unused.
- `verification/stage03/` holds the new exact checks and chamber certificate;
  `verification/reference/origin-manifest.json` covers all added unchanged
  original scripts/data and their local dependency. Primary literature
  synthesis and final attribution remain assigned to stage 6.

## Candidate stage-4 development: a compact three-mode floor-chamber automaton

For a generic three-mode unit-grid input with every nonzero-prefix coordinate nonintegral, let f_j=floor A(j) and sigma_j=j−sum f_j in {1,2}. The three allowable integral prefix-count vectors are f_j+e_i if sigma=1 and f_j+ones−e_i if sigma=2. At the first cell f_1=0,sigma_1=1. Adjacent floor increments d=f_j−f_(j−1) have coordinates0/1 and sum1+sigma_old−sigma_new. Thus transition choices are:1->1 d=e_p (3 choices);1->2 d=0 (1);2->1 d=ones−e_p (3);2->2 d=e_p (3). For nodes u,v the count difference determines the emitted mode. Every such local bipartite transition has no isolated row or column, so every node lies on a full word path. Averaging all these integral words realizes strict floor/ceiling inequalities at every coordinate/prefix; conversely every generic control has one of these paths. This appears to give an exact simpler chamber representation: counts from initial vector(1,0) evolve by [[3,1],[3,3]], yielding396 total chambers at N5 (matching the existing exhaustive result),1872 at N6,8856 at N7.

An independent stage-4 author should verify this carefully. It could simplify the five-cell proof and permit a finite-state min-plus investigation for arbitrary three-mode budgets. Track minimal switches by (prefix-count node,last active mode), nine entries, then normalize costs and quotient label permutations; a closed finite-state potential certificate might establish a general switch bound, but no such theorem is claimed yet. Generic inputs can be reached by perturbing toward a constant rational simplex vector whose denominator is prime>N, then using continuity to handle integer-prefix boundaries. The original N5 perturbation denominator7 works only for that fixed N.

Do not assume a general continuous lower witness from a cyclic pure word: for N7, input0120120 has a three-switch schedule0120 at times1.2,2.7,4.4 with full error0.8<1. The N5 witness01201 argument above is special and remains valid. Any arbitrary-budget exact claim needs a separate lower proof/source audit.

## Stage 4 accepted coverage (`stage04-accepted`)

- `08-finite-grid-one-switch.tex`: `thm:finite-one` gives both closed LP
  families, full maximizer coverage, symmetry compression, every elimination
  bound, exact formula, rational reconstruction, and O(N²) arithmetic/bit
  complexity. `cor:three-unit-one` gives every residue with matching witnesses
  and N=1 exception. `ex:five-nine` gives a standalone analytic upper/lower
  proof of 17/5; the nonuniform failed simplification is explicitly retained.
- `09-three-mode-floor-chambers.tex`: `prop:floor-automaton` fully proves the
  candidate all-N three-state floor-history characterization and its realization
  by averaging full integer paths. `thm:five-cells` reproduces the repository's
  five-cell minimax with a new exact transition enumeration and two unchanged
  historical coverage checks. `cor:three-two-continuous` closes F_{3,2}=T/5;
  its lower bound is credited to Sager–Zeile Proposition 4 and also proved
  directly with the alternative pure word01201.
- Further developed and independently checked by the author from root research:
  `cor:six-cells` gives F_grid(3,6,s3)=1; `prop:seven-cell-instance` gives an
  exact 4/3 supplied-input optimum; `thm:seven-cells` proves full minimax
  F_grid(3,7,s3)=4/3 by classifying all8856 chambers, identifying exactly six
  exceptional mode permutations, and giving three explicit repair words whose
  exceptional allocations sum to at most4. Thus the proposed unit-error
  extension on2s+1 cells is disproved at s3, rather than left as an untested
  possibility. The resulting continuous band T/7<=F_{3,3}<=T/6 is stated
  accurately; the source's T/7 lower is also verified by a direct activation
  argument. No exact continuous three-switch boundary value is claimed.
- Subsection12.4 corrects the published Corollary5 at n3,N5,s2, preserving
  Corollary4's attainment restriction and distinguishing Proposition4's valid
  continuous lower bounds. Primary-source page/eq locators and downloaded
  final-PDF hash are recorded in `verification/stage04/source-record.md`.
- All six newly bundled historical artifacts are unchanged and hash recorded.
  `verification/stage04/run_checks.py` runs the exact, portable standard-library
  checks. Optional LP audits use SciPy only for discovery/corroboration; the
  closed formula and new floor certificates do not require it. Stage4 is
  accepted in `stage04-accepted` after five reviews and correction of all valid
  minor findings. The seven-cell comparison now distinguishes refutation of
  the published equality from satisfaction of its upper-bound consequence.

## Stage 5 accepted coverage (`stage05-accepted`)

- `10-instance-algorithms.tex`, `thm:linear-one-switch`: three candidates per
  boundary, largest-final-mass dominance, exact O(nN) solve, fixed initial
  mode, eligible boundaries, constants, and the crossing-neighbor
  O(n log(N+1)) query consequence with its preprocessing contract.
- `lem:final-residual`: optimal one-block completion after an arbitrary fixed
  prefix, including signed residuals and a fixed eligible final-label set.
- `prop:subset-DP` and `thm:fixed-budget`: full subset costs including unused
  modes, exact standard partition recurrence, traceback and space, all
  nominal block partitions, representation of fewer switches by subdivision,
  O(nN^2) for two switches, fixed-budget polynomial bit complexity and the
  limitation on fixed-parameter tractability in the budget alone.
- Subsection 13.3: mode-specific minimum dwell on maximal runs including both
  horizon ends, unused modes unconstrained, adjacent selected blocks merged,
  infeasibility, generic unary restrictions with subdivision invariance, and
  exclusion of coupled transition restrictions. `lem:candidate-labels`
  retains the d²+d bound for fixed equality-pattern roles with a complete
  exchange proof and careful scope.
- Subsection 13.4: further developed exact continuous word/time-cell LP
  enumeration for piecewise-affine input, n^k C(N+k-2,k-1) cases with k=s+1
  even when k>N, endpoint-only constraints, separate one-sided criterion,
  compact rational LPs, complete active-constraint vertex enumeration,
  degenerate and zero-duration cases, and fixed-k polynomial bit complexity.
  The standard-library implementation is explicitly a small-instance
  benchmark and does not replace the more mode-efficient grid DP.
- `11-transfer-and-coarsening.tex`, `thm:sharp-transfer`: full supported
  integral-prefix flow proof, strict error<h, chronological subsequence
  argument including repeated labels, switch preservation, rational
  polynomial-bit construction in explicit grid length.
- `cor:opt-transfer`: instance inequalities and the stronger strict minimax
  transfer now justified using accepted cell-averaging domination and an
  attained grid maximizer. This resolves the old note's comparison caution.
- `prop:binary-transfer`: arbitrary nonuniform binary half-mesh bound and
  supplied-schedule sharpness. `prop:transfer-sharpness`: universal
  coefficient-one sharpness in the valid source budget regime, n4/N5/s3
  gap≥9/16, and the full repeated-cycle m family. Source p615/p139 claims
  are identified as preconjecture arguments, not proved theorems.
- `thm:certified-coarsening` and `cor:coarse-perturbation`: new exact
  coarsening with original cumulative endpoints on nonaligned input grids,
  strict interval and clipping convention, actual returned schedule, epsT
  additive scheme, exact rational complexity, joint budget/accuracy
  parameter dependence, nested fine-grid certificate, quantified input
  perturbation and h+2delta guarantee. Stronger half-mesh special cases and
  exact zero-switch case are stated without conflating them with the
  implementation's uniform general certificate.
- `ex:dwell-grid-gap`: new explicit refinement obstruction suggested by the
  root and verified by the author: pure binary half/half input, budget 1,
  minimum dwell 1/2 for both modes, continuous optimum 0 but grid optimum 1/2
  on every odd uniform grid. Thus the unrestricted coarsening certificate
  cannot generally be used for dwell-constrained optima.
- `verification/stage05`: new portable coarsener, exact continuous LP solver,
  direct original-input and nested-grid checks, nine exact continuous test
  optima, complete documentation, and source audit. Five newly bundled
  historical scripts are unchanged and hash-recorded, giving 30 total
  originals. Application benchmarks remain assigned to stage 6.
