# Source coverage and staged development map

Stage 1 inventory, 2026-09-07. Paths in this document are relative to the
repository root. This is a research and editorial record, not manuscript prose.
A row is an assignment, not certification that its proof has passed a new audit.
The canonical statements, their supporting proofs, negative examples, source
comparisons, code, and historical reviews must be inspected during the assigned
stage. Only new stage review gates determine manuscript acceptance.

## Stage order and deliverables

1. **Foundations:** model, semantics, arithmetic, sources, and this inventory.
2. **Exact responses:** scalar and block compression, global comparison,
   moving normals, optimistic/pessimistic values and attainment, low-rank LP
   corollary, and supporting fixed-core polyhedral elimination appendix.
3. **Robustness and screening:** measurement-fiber theorem, adverse witnesses,
   budget design, attainment and rank boundaries; dense recovery and its
   quantitative ambiguity conditions.
4. **Accuracy:** bounded powers, general signed monotone inverse, one and many
   resources, convex aggregates, rational recovery, and polynomial upper data.
   Put long inverse and quantitative bounds in appendices, but provide complete
   proofs in this manuscript. This stage is deliberately substantial: its
   dependencies must close before the next stage begins.
5. **Boundaries:** zero and negative local curvature, scalar dense SPD
   reductions and conditioned approximation;
   growing leader dimension, bounded vertex integrity, both distinct path
   constructions, and arithmetic/degree barriers. Include affine-strip positive
   projection only with its precise limitation to feasibility.
6. **Algorithms and computation:** complete convex and nonconvex scalar
   algorithms, original-response contact reconstruction, reproducible evidence,
   screening comparisons, and the concrete development below.
7. **Synthesis:** final abstract, contribution overview and theorem comparison,
   conclusions, integrated notation, length/readability pass, full bibliography
   and reproducibility audit. Follow with a new full-manuscript review gate.

Each stage has one author, then five independent reviewers. Root assesses every
finding; a different agent corrects all accepted issues, including minor issues.
Any accepted major issue triggers five fresh reviews after correction. A stage
advances only after no major issues remain and all valid minor issues are fixed.
No independent agent is asked to author the next stage before the current gate
passes. Historical source reviews do not replace this process.

## Canonical and note-only mathematical developments

| Development and source | Stage and required treatment |
| --- | --- |
| `results/bilevel-fixed-aggregate-response-algorithm.md`; `notes/bilevel-fixed-aggregate-response-investigation.md` | 2. Full scalar clipping proof, realizable sign conditions including zeros, rational denominator construction, global KKT-value comparison, exact common-field recovery, and fixed-normal compactness. |
| `results/bilevel-fixed-block-response-algorithm.md`; `notes/bilevel-fixed-block-response-extension.md` | 2. Full local active-normal support reduction, equality basis and multiplier signs, determinant positivity, polynomial local row count, and non-Cartesian global regime selection. |
| `results/bilevel-compressed-response-infimum-semantics.md`; `notes/bilevel-compressed-response-infimum-semantics.md`; `notes/bilevel-moving-local-normal-extension.md` | 2. Rank-changing equality bases and moving shared/local normals; formulas with a fixed number of quantified copies; optimistic infima and pessimistic universal upper feasibility; worst witnesses and nonattainment examples. |
| `notes/bilevel-fixed-rank-quadratic-corollary.md` | 2. Full supplied diagonal-plus-fixed-rank SPD LP-cell corollary, affine upper data, rational output, lower-dimensional cells, and decomposition supplied rather than computed. |
| `results/fixed-core-block-polyhedral-optimization.md`, Sections 1--5 and scope in Section 8; `notes/fixed-core-block-optimization-novelty.md` | 2 appendix. State/prove the general support-function elimination framework insofar as it supports this structural method: local vertices, denominator clearing, Minkowski support membership, fixed-dimensional algebra, and common-field recovery. The stage 2 development replaces the algebraic LP recovery dependency by support tuples and fixed-size Carathéodory reconstruction (proved in the manuscript). It is a related general tool, not a logically necessary replacement for the quadratic KKT proof. Credit support functions, Basu--Pollack--Roy, Adler--Beling. Pooling application corollaries are outside this bilevel paper and should not be reproduced. |
| `notes/fixed-core-convex-leaf-arithmetic-barrier.md`; scalar theorem Section 6 | 4 and 5. Root-sum output degree and exact square-root-sum comparison; distinguish an unresolved exact arithmetic problem from NP-hardness. Include sparse-binary exponent output obstructions. |
| `results/bilevel-fixed-aggregate-response-algorithm.md`, Section 6; `notes/bilevel-fixed-aggregate-response-investigation.md` | 5. Retain both elementary 3SAT reductions as distinct boundaries for positive local curvature. With zero local cost on the unit box, every point is a follower optimum, and upper Boolean quadratic equations plus linear clause rows encode 3SAT. With negative local quadratic coefficients, minimizing `sum_i z_i(1-z_i)` on that box makes the optimum set the Boolean cube, so linear upper clause rows alone suffice. Present these as an elementary example pair with no novelty claim. |
| `results/bilevel-near-optimal-response-robustness.md`; `notes/bilevel-reopened-near-optimal-robustness.md` | 3. Full fixed-measurement fiber argument covering nonstationary near-optimal responses, one criterion at a time, nominal global value, robust objective/rows, separately encoded witnesses, budget as leader decision, convex attainment subclass, positive-budget nonattainment, and growing measurement-rank Max-Cut boundary. |
| `results/bilevel-surrogate-screening-exact-optimization.md`; `notes/bilevel-reopened-approximate-structure.md` | 3. Exact perturbation enclosure, cell-wide sign tests, M times 3^t LPs excluding preprocessing, transition multiplicity bound t <= (r+1)q, a computable neighborhood, approximate certificates when t is large, and failures of small matrix error alone. |
| `results/bilevel-bounded-power-accuracy-bit-algorithm.md`; `notes/bilevel-bounded-power-accuracy-bit-algorithm.md` | 4. Full dyadic rational approximation and arrangement proof; signed upper objective, exact rational leader recovery, polynomial dependence on numerical power; sparse-binary rational output-length lower bound. |
| `notes/certified-positive-polynomial-inverse-approximation.md` | 4 appendix. Retain the sharper positive-coefficient estimates as a stated specialization of the general inverse method; do not silently use positivity in the signed theorem. |
| `notes/certified-monotone-polynomial-inverse-approximation.md` | 4 appendix. Full explicit inverse modulus, real/complex critical-value handling, rational analytic panels, Taylor recurrences and certified errors, polynomial coefficient/degree counts, including interior derivative zeros. This is a major proof dependency, not a black-box repository citation. |
| `results/bilevel-one-resource-accuracy-bit-algorithm.md`; `notes/bilevel-one-resource-accuracy-bit-algorithm.md` | 4. Exact leader projection, bounded scalar multiplier, signed balance-to-response identity, degenerate equality cases, rational recovery, arbitrary strictly increasing signed polynomial marginals. |
| `results/bilevel-fixed-resource-accuracy-bit-algorithm.md`; `notes/bilevel-fixed-resource-accuracy-bit-algorithm.md` | 4. Explicit feasible-leader polytope by fixed-dimensional resource projection, multiplier and Hoffman bounds, degree-dependent uniform convexity modulus, residual/complementarity certificate, rational rounding and entire error ledger. The one-resource identity is not assumed to generalize. |
| `results/bilevel-convex-aggregate-accuracy-bit-algorithm.md`; `notes/bilevel-reopened-nonlinear-aggregate.md` | 4. Convex aggregate mismatch, fixed-dimensional nonlinear branch construction, rational recovery across branch boundaries, and explicit leader-response modulus, without uniform positive local curvature or Slater promises. |
| `results/bilevel-response-constraint-accuracy-bit-algorithm.md`; `notes/bilevel-reopened-response-constraints.md` | 4. Polynomial upper objective/rows, outer bicriteria and inner algorithms, posterior bounds, tightening modulus, strict anchor plus convex reduced constraints, reserve controls, aggregate composition, isolated feasible optimum, irrational-only feasible leader, exact-arithmetic counterexamples. |
| `results/bilevel-scalar-leader-spd-box-np-completeness.md`; `notes/bilevel-dense-box-hardness-investigation.md`; `notes/bilevel-dense-box-no-upper-constraints-extension.md` | 5. Full first scalar SPD box construction including removal of all extra upper rows and rational NP certificate. It has a different numerical scope from the conditioned construction and should remain a theorem/corollary rather than being erased as superseded. |
| `results/bilevel-well-conditioned-box-exact-hardness.md`; `notes/bilevel-well-conditioned-box-exact-hardness.md` | 5. Full ReLU simulation, scaling, coordinate-relative error, coefficient magnitudes <=2, condition number <2, arbitrarily near-identity coupling, exact NP-completeness, and small polynomial-bit gap excluding accuracy-bit optimization. Do not claim strong hardness or an inverse-polynomial absolute gap under these same bounds. |
| `results/bilevel-conditioned-box-additive-algorithm.md`; `notes/bilevel-conditioned-box-additive-algorithm.md` | 5. Saturation range, fixed-dimensional cost grid, response continuity bound, rational leader and follower recovery; runtime polynomial in condition estimate and inverse error, normalized by upper follower coefficient one-norm. Explain compatibility with exact hardness. |
| `notes/bilevel-diagonal-leader-dimension-boundary.md`; `notes/bilevel-diagonal-box-parameterized-hardness-source-audit.md` | 5. Attribute W[1]/ETH boundary to Froese--Grillo--Hertrich--Stargalla; give explicit capped-ReLU transfer and mixed-radix continuous-gap alternative proof, including polynomial duplication for bounded coefficient magnitudes. Avoid a novelty claim for this classification. |
| `results/bilevel-leader-vertex-integrity-boundary.md`; `notes/bilevel-leader-vertex-integrity-boundary.md`; `notes/bilevel-leader-vertex-integrity-source-audit.md` | 5. Growing-leader exact algorithm with supplied fixed core and bounded components, affine candidates and common core arrangement; weak Subset Sum path hardness; identity-Hessian realization; fixed-alphabet exponential elimination messages. This is a path in leader interactions, separate from the follower-constraint path below. |
| `notes/parametric-path-lp-obstructions.md`; `notes/parametric-path-lp-investigation.md` | 5 appendix. Attribute sparse Klee--Minty shadow to Gärtner--Helbling--Ota--Takahashi; prove or cite its precise used statement, explicit linear-time evaluation recurrence, exponentially many message segments, and total-degree obstruction for unextended polynomial descriptions. Do not interpret it as pointwise optimization hardness. Physical blending realizations are outside scope. |
| `notes/klee-minty-rank-one-slab-hardness.md` | 5 appendix. Telescoping nonnegative vertex polynomial, rank-one concave coordinate/slab Subset Sum reduction, fixed local coefficient padding, parabolic exposure identity. These support the following bilevel theorem and must be reproduced sufficiently to make its proof self-contained. |
| `notes/klee-minty-diagonal-follower-bilevel.md` | 5. Scalar leader, diagonal strictly convex follower on a 2VPI path, full vertex-optimality inequality and identity-Hessian rescaling, exponentially many constant response intervals, and NP-completeness with one explicitly nonconvex upper quadratic row plus aggregate slab. Do not claim all-linear upper hardness from this argument. |
| `notes/parametric-affine-strip-path-projection.md` | 5 appendix or short boundary proposition. Exact polynomial feasibility projection for equal-slope affine interval transitions, zero gains, tree/fixed-cycle-rank extension. This distinguishes a valid narrow path elimination from the invalid general message-size inference. Its pooling interpretation is outside scope. |
| `notes/bilevel-reopened-quadratic-algorithm.md` | 6. Exact rational KKT path certificate from numerical proposals; rejection/failure behavior; complete exponential oracle; complete aligned rank-one sweep with signed loadings and allowed signs of the rank-one coefficient under SPD; reusable affine upper rows and tariff objectives. |
| `notes/bilevel-nonconvex-scalar-algorithm.md` | 6. Complete rational nonconvex aligned tariff algorithm: strictly convex fiber allocation, scalar pieces, candidate domains and all true ties/flat intervals, exact envelope, upper feasibility, optimistic maximum and pessimistic supremum/attainment, degree-two output and rational interior samples. |
| `notes/bilevel-nonconvex-source-positioning.md` | 6. Classical conjugate/envelope attribution; prove contact reconstruction with the original nonconvex objective and false-feasibility counterexample. Do not substitute the convexified response set for original global responses. |

## Stage 2 manuscript locations (author draft, pending review)

| Source development | Manuscript label and treatment |
| --- | --- |
| Exact scalar and block theorems | `sec:exact`, `thm:exact-block`, `eq:scalar-clipping`, `lem:local-branches`, `lem:candidate-size`, `eq:global-response-formula`, and `lem:closed-response`: full proof with shared local elimination, scalar explanatory formula, all ties, size bounds and exact common-field recovery. |
| Moving shared/local normals and changing equality rank | `subsec:moving-normals`, `lem:moving-compression`, `ex:moving-nonattainment`: all row subsets, determinant guards, pointwise completeness and optimistic failure of attainment. |
| Optimistic infima and universally feasible pessimistic semantics | `thm:exact-semantics`, `eq:worst-value-formula`, `eq:infimum-predicate`, `ex:pessimistic-nonattainment`: full constant-copy quantified construction, exact value/attainment decisions, joint witness recovery and fixed-normal tie example. |
| Supplied diagonal-plus-fixed-rank corollary | `cor:low-rank-lp`: full affine arrangement and closed-cell LP proof, rational output, supplied decomposition and SPD requirement. |
| New constant-local-Hessian arithmetic refinement | `cor:constant-hessian-degree`: for fixed input degree and structural dimensions, common-field algebraic degree is independent of follower count/row counts/coefficient bit lengths; proved from constant KKT denominators and the degree bounds of Basu–Pollack–Roy. |
| General fixed-core polyhedral theorem | `app:fixed-core`, `thm:fixed-core`, `lem:core-support-membership`: full vertex/support/Minkowski proof and degree tracking, strengthened from the source's fixed-degree statement to polynomial time in actual numerical degree and input bits. |
| New constructive fixed-core block recovery | `lem:core-recovery`: globally enumerated support tuples span the entire fixed-core aggregate image; a common convex combination of at most k+2 tuples recovers all blocks in the sampled field. This removes reliance on a growing-dimensional algebraic LP oracle. It applies to linear block measurements, never to a nonconvex follower reaction graph. |
| Arithmetic/degree and curvature boundaries | Only the elementary cubic response/square-root-sum motivation appears at the end of `sec:exact`; the complete barriers and hardness examples remain assigned to stages 4/5 below. |

The current 17-page compiled draft contains foundations, stage 2, and its appendix.
These location entries record written coverage, not passage of the stage 2 gate.
All stage 3–7 obligations above remain unchanged.

## Computational artifacts and distinct validation purposes

| Artifact family | Required use in stage 6 or earlier proof check |
| --- | --- |
| `code/bilevel_response/`, `code/bilevel_dense_box/` | Exact examples, stationary/global distinction, dense-hardness and conditioned-approximation diagnostics. Re-run only scripts relevant to concrete proof obligations and retain logs. |
| `code/bilevel_bounded_power/`, `code/bilevel_one_resource/` | Accuracy and inverse diagnostics, signed marginals, rational simplex recovery, quantitative resource constants. Primary stage 4 checks. |
| `code/bilevel_vertex_integrity/`, `code/bilevel_parameterized/` | Structural and mixed-radix gap verification for stage 5. |
| `code/parametric_path_lp/` | Exact shadow, fixed alphabet, rank-one slab, diagonal follower, strict-local and affine-strip checks. Physical-penalty/blending checks only if the corresponding non-bilevel application is expressly brought into scope. |
| `code/fixed_core_blocks/` | Small exact support/Minkowski sum checks for the stage 2 appendix; these do not implement general quantifier elimination. |
| `code/bilevel_reopened/README.md`, `quadratic_solver.py`, `quadratic_benchmarks.py`, `quadratic_tariff_benchmarks.py`, recorded JSON results | Complete aligned convex sweep versus generic numerical-proposal path; exact exhaustive and independent MILP validation, heterogeneous sizes versus 10,000-variable sweep. Preserve proposal failures. |
| `notes/bilevel-reopened-screening-computation.md`, `code/bilevel_reopened/screening_milp_comparison.py`, `screening_milp_comparison.json` | Record unfavorable four-case screening-versus-MILP result and all preprocessing, rational/numerical distinctions, not just recovery LP counts. |
| Remaining `code/bilevel_reopened/` diagnostics/reviews and `verification_summary.json` | Robustness, perturbation screening, nonlinear aggregate, upper-constraint identities. Tie every check to a mathematical claim; do not sum heterogeneous counts into a claim of comprehensive formal verification. |
| `code/bilevel_nonconvex/README.md`, `scalar_solver.py`, `check_scalar_examples.py`, `review_one.py`, `review_two.py`, `benchmarks.py`, all benchmark JSON files | Complete exact nonconvex specialization, all ties, independent original-coordinate face oracle, all-pair versus incremental envelope, repeated timing distributions and heterogeneous seeds. Preserve the fact that a fixed-price oracle solves a smaller problem. |
| `notes/bilevel-nonconvex-computation.md`, `code/bilevel_nonconvex/plot_contact_example.py`, `figures/convex_envelope_false_choices.*` | Correctness/scaling illustration, replication with only two types versus heterogeneous breakpoints, contact/false-feasibility figure. Reproduce any figure copied into the paper and state its source parameters. |

Concrete stage 6 development proposed by root: implement an independent complete
continuous-leader baseline by enumerating stationary faces in original follower
coordinates, for rational rank-one Hessians with every principal minor nonzero
(an explicit checked restriction). Compare all feasible candidate values and
solve optimistic/pessimistic upper problems over the resulting graph. This adds
an equivalent full-task comparison to the existing fixed-price oracle. Verify
the completeness restriction and ties, and report exponential enumeration
honestly. Profile and remove demonstrated symbolic bottlenecks if a simple
improvement preserves exactness. No production-solver superiority is presumed.

## Source comparison and historical review inventory

The principal scope/closure sources are `notes/bilevel-paper-scope.md`,
`notes/bilevel-response-complexity-map.md`, `notes/bilevel-classical-positioning.md`,
`notes/bilevel-reopened-status.md`, `notes/bilevel-reopened-closeout.md`,
`notes/bilevel-nonconvex-closeout.md`, `notes/research-closeout.md`,
`notes/research-continuation-closeout.md`, and
`notes/supporting-results-source-closeout.md`. Broad closeouts contain unrelated
research; only their bilevel and named dependency dispositions are relevant.

Each `notes/review-bilevel-*.md`, each inverse/fixed-core/Klee--Minty/path review,
and the linked source audits belong to the corresponding source row above.
They preserve corrections and rejected stronger claims. They are not additional
results requiring duplicated paper sections. Historical investigation versions
are reconciled to the canonical result, with any additional substantive lemma
retained rather than silently discarded.

Focused attribution sources include the exact aggregate/block, resource,
bounded-power, monotone-inverse, conditioned/dense-box, fixed-core, leader
integrity and parameterized novelty/source notes; the reopened literature audit;
and the nonconvex source positioning. Cite the actual primary publications in
the paper. The paper's bibliography must not cite repository reviews as theorem
authority. Source absence in a bounded search is not proof of novelty.

## Completion checks for later stages

- Every table row above has a manuscript theorem, proposition, proof, example,
  algorithm, experiment, or explicit explained exclusion.
- Mathematical claims carry the exact domain, output convention, degree and
  dimension dependence, and attainment qualification used by their proof.
- No closed investigation or negative finding used as a premise remains an
  unproved assertion. Genuine broader open problems are identified as limits,
  not hidden inside a theorem or promised solved by a finite diagnostic.
- Superseded narrower theorems are retained as explained special cases or
  supporting alternative proofs when they provide distinct insight.
- The final text is a coherent publication, not a sequence of repository notes
  or an assertion that no conceivable future research can exist.
