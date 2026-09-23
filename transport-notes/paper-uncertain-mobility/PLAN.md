# Sequential development and review plan

Prepared 2026-09-07. This plan records the sequential development and review procedure used for the completed manuscript. Development resolved the sharp supercritical coefficient (X1) and the finite-ratio precision crossover (X2). All stages and the separate five-reviewer whole-manuscript audit have been carried out. Coordinator decisions and accepted snapshots are recorded in the [review ledger](reviews/README.md), with whole-manuscript findings in the [final adjudication](reviews/final/round-01/adjudication.md). The requirements below governed the work; prior repository reviews were leads, not automatic clearance.

## Mandatory stage workflow

The coordinating agent must complete the following cycle before starting the next stage.

1. Assign one agent to author the stage, including any mathematical development needed to close its claims. The coordinator may inspect sources and prepare review questions concurrently, but may not begin writing a later stage.
2. Freeze the changed files, record their snapshot manifest before dispatch, and obtain five independently written reviews from five agents. Each reviewer sees the same stage snapshot and its prerequisites. Reviewers should not read one another's reports before submitting their own. Preserve each reviewed manifest; record the corrected version separately at acceptance.
3. The coordinator assesses every finding, including rejected criticisms, with a reason. A major issue is a false or insufficiently justified claim, a material missing assumption, a proof gap affecting a result, unsupported novelty, or an omission that prevents the intended reader from assessing the result. Severity depends on effect, not wording or who raised it.
4. If any valid issue exists, assign a different agent to correct all valid issues, including minor ones. The author may answer questions but must not be the assigned correction agent. The fixer records exact locations and how each issue was resolved.
5. If the round contained any valid major issue, obtain another five independent reviews after correction. Repeat until a five-reviewer round contains no valid major issue.
6. Correct all remaining valid minor issues through the separate fixer, verify those corrections, and record an acceptance decision. Only then proceed.

The same cycle applies to Stage 0 and, after all substantive stages, to the entire manuscript. Final reviewers must assess the actual complete draft, not merely aggregate prior section approvals. Later changes that invalidate an accepted dependency reopen that dependency and the affected claims. All findings remain in the review ledger, including reasonable criticisms rejected by the coordinator.

## Stage 0: scope, notation, and audit infrastructure

Deliverables: this plan, a claim/dependency inventory, notation ledger, minimal compiling document, review templates, and an explicit list of unfinished questions to investigate. Acceptance requires a coherent scope covering the uncertainty results and no unsupported claim that the manuscript is complete.

## Stage 1: transport model, admissible designs, and finite-bulk comparison

Target text: model and mathematical setting; finite-bulk proof may ultimately be placed in an appendix for reading order. Establish dimensional quantities and nondimensionalization before powers or logarithms of the budget appear. Derive constant-affinity equilibrium, mean velocity, the scalar variational response, and the finite-response Schur identity from the bulk–surface model. Specify the closed-form realization for positive-background coefficients, the extended smooth-test response for arbitrary integrable designs, admissible measurable observation policies, and what full-bulk quantity is being optimized.

Prove the logarithmic remainder lemma and same-budget, same-information transfer for every fixed positive moment. Audit positivity and coercivity, trace duality, domains for unbounded coefficients, zero modes, and the distinction between an extended lower bound and an identity requiring a finite inverse. Establish policy/measurability facts needed by later exact-observation and conditional problems. Do not assume existence of an optimizer.

Claims: M1–M4. Exit criterion: later scalar theorems have a fully specified physical interpretation and a self-contained transfer theorem under fixed positive bulk diffusivity, nonzero mean speed, and connected one-dimensional wall assumptions.

## Stage 2: local resolvents and the undesigned disorder baseline

Target text: common localization lemmas and uniform-design comparison. Reprove the local harmonic response and its constant, the quartic unfolding response and both parameter tails, finite-interval bracketing bounds, and compact-wall localization. Treat the constant whole-line source through its energy dual rather than assuming it belongs to L². Prove all three uniform-mobility moment regimes with exact constants and the critical logarithmic matching. Include the Gaussian amplitude-collapse counterexample and the related marked-zero warning at the level needed to delimit the bounded ensemble.

Claims: L1–L4. Exit criterion: all localization tools used later are stated with genuinely uniform error bounds; normalization between constant mobility and total budget is checked; baseline variance and numerical constants are distinguished from particle-displacement claims.

## Stage 3: predetermined mobility and positive-moment optimization

Target text: principal design theorem. Prove convexity for every q>0, justify ensemble symmetry, and give the arbitrary-competitor moving-root certificates. Develop subcritical sharp constants, the critical sharp logarithmic coefficient, and supercritical matching orders with globally admissible graded tails.

Mandatory further investigation: resolve the proposed sharp supercritical local optimization problem as far as a rigorous theorem permits. In particular, investigate whether a whole-line variational constant gives an exact asymptotic, addressing weak limits of designs, escaped mass, finite-measure relaxation versus L¹ fields, paired folds, tails, recovery sequences, and budget allocation. A named infimum without a limit proof does not resolve this question. A closed elementary expression or unique limiting profile is not required if a finite positive variational constant and a proved sharp equivalent fully settle the value. Do not convert an order theorem into an equivalent by dimensional scaling alone. Any remaining limitation must be mathematically identified and adjudicated, not hidden by deleting the investigation.

Claims: D1–D4, investigation X1. Exit criterion: every displayed equivalent has both unrestricted lower and admissible upper proofs; no trial profile is called a finite-budget optimizer without a certificate.

## Stage 4: smooth kinetic families with generic folds

Target text: geometric robustness of the optimized moment orders. Give a precise compact-family theorem, prove uniform root counts and rate anchoring, construct parameter-dependent fold coordinates, and adapt lower shells and upper designs without relying on cosine symmetry. Check additional ordinary roots, stationary root branches, parameter-density assumptions, and the distinct-fold hypotheses actually used.

Claim: G1. Exit criterion: all three orders, and their full-bulk consequences, follow under explicit sufficient assumptions; no generic sharp constant, simultaneous-fold extension, or arbitrary-random-field result is inferred without proof. Discuss excluded sampling and degeneracy patterns concisely.

## Stage 5: exact observation and the local placement problem

Target text: the value of measuring the kinetic realization exactly; local results needed by finite precision. Reprove the quadratic whole-line placement profile, global dual optimality certificate, compact-wall localization, and multiple-defect budget allocation. Include enough detail that the companion deterministic paper is not a prerequisite. Then prove the exact-observation expected asymptotic with uniform fold-layer domination and measurable admissible policies.

Claims: O1–O2. Exit criterion: the sharp oracle constant and blind/oracle comparison are justified; the local response is not mistaken for a stationary process on an infinite wall; potential zero-mobility interfaces and extended-form conventions agree with Stage 1.

## Stage 6: finite measurement precision, including the interior crossover

Target text: equal-bin observation policies, local uncertain-center value, joint budget–resolution law, and sharp endpoints. Prove the conditional lower bound over arbitrary mobility fields, uniform regular-bin trials, and fold-bin bounds. Audit quantizer alignment, nonnested partitions, exact per-observation budgets, and joint limits.

Mandatory further investigation: resolve the finite positive ratio Δ/M^(1/5) limit. Develop uniform variational localization of the conditional optimization, the whole-line uncertain-center value and its regularity, lower compactness or explicit dual certificates, and matching recovery policies. A convergent integral involving a rigorously defined local value is a suitable exact crossover theorem; a closed elementary formula is not required. Endpoint agreement alone is insufficient. If the proposed formula fails, establish and prove the corrected statement rather than preserving it as a conjecture.

Claims: P1–P3, investigation X2. Exit criterion: the local and global intermediate regimes have a justified relation, endpoints have correct factors, and the final information-resolution interpretation matches noiseless quantization rather than arbitrary noisy sensing.

## Stage 7: numerical evidence, literature, and complete manuscript synthesis

Target text: introduction, abstract, result roadmap, numerical methods/results, discussion, conclusion, bibliography, and any proof appendices needed to improve reading order. Use all relevant results accepted above and explicitly separate inherited mathematical tools from this paper's contributions. Verify citation metadata and inspect primary literature, including current searches for close singular-design and observation-resolution results. Consult `literature/AGENTS.md` before using or modifying literature packages.

Re-run the computations actually used in the manuscript. Include grid and parameter-quadrature refinement, complete finite-domain and tail specifications, and independent lower certificates where finite-dimensional optimization is reported. Label all trial curves, discrete optima, asymptotic constants, and numerical estimates accurately. Preserve finite-budget counterexamples to simplistic practical interpretations. Generate manuscript figures and tables from documented commands.

Claim/support item: N1 and every novelty statement. Exit criterion: no argument relies on an unpublished repository note; references and proofs are complete; the introduction, abstract, theorem statements, and numerical captions agree; the build is clean and the PDF has been visually inspected. This is an assembled draft, pending the whole-manuscript review below.

## Final complete-draft audit

Dispatch five independent reviewers of the entire manuscript. They must check mathematical correctness, literature/novelty support, consistency across dependencies, completeness relative to this scope, physical assumptions and interpretation, numerical evidence, and readability for transport researchers. Apply the mandatory correction and repeat-review cycle above. Resolve every valid minor issue before final delivery. Record the final manuscript snapshot, exact build, reproducibility checks, and any substantive scope limitations as theorems' explicit boundaries. Do not promise immunity to unknown peer-review concerns or claim novelty solely from absence of a search match.
