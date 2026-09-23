# Stage 3 independent review 1

Reviewed 2026-09-13. Scope: all three Lean proof modules, umbrella imports, the audit and verification scripts, package configuration and manifest, coverage/readme, source fingerprints and fresh author logs, Section 5, the revised introduction, and their agreement with Sections 3–4. No proof or manuscript file was changed.

## Verdict

**No major or minor issue found.** The actual declarations prove the mathematical claims assigned to them. Their premises are explicit and appropriate, and the manuscript does not inflate those results into verification of the executable checker, the entire soundness argument, or individual benchmarks. No correction or major-issue review cycle is required by this review.

## Mathematical strength and correctness

### Coordinate domains and rational corrections

`Coordinates.lean` defines membership in the intended bounded, lower-bounded, upper-bounded, and free real domains using rational endpoints. Infinite bounds are constructors. There is no conversion of infinity to a real sentinel. Requiring the support point to belong to the interval prevents inconsistent bounded intervals from being silently used.

The bounded proof splits on the actual real residual's sign. It first moves the tested point to the correct box endpoint and then moves the residual to the appropriate enclosure endpoint. The multiplication directions are correct in both cases. The lower-half-line proof derives nonnegative residual from the accepted lower enclosure; the upper-half-line proof derives nonpositive residual from the accepted upper enclosure. The free-coordinate proof derives an exactly zero real residual from the rational zero enclosure. The rational casts of maxima, multiplication and subtraction match the formulas in the manuscript table.

`fixed_correction` proves zero directly from equal endpoints and support coordinate. `correction_nonneg` substitutes the support point as the tested point in the universal correction theorem. The latter has a real enclosed residual as a premise; Section 5 states that premise accurately. Neither result mistakes a pointwise numerical sample for a universal statement.

### Finite sums and the main safe-cut theorem

`safe_affine_of_shift_bounds` expands and sums the actual residual `p+q-a`, then combines the support and intercept inequalities to prove the affine underestimator. I checked its displayed sum identity and the sign of every contribution. The theorem's support premise is a support inequality at the tested point, not the final cut assertion.

`SafeCuts.lean:41–66`, `rational_enclosure_cut`, is the substantive specialization: rational row/cut/support-point/enclosure data coexist with a real function and support vector. The genuine value enclosure is a lower bound for `g(z)+q·z+c-a·z`; the residual enclosures bound `p+q-a`. Its rational intercept test uses the explicitly defined coordinate correction. The proof derives every shift bound from `coordinate_correction_sound`, casts the rational finite sum exactly, and concludes underestimation for every point in the box. It does not assume underestimation. No feasibility assumption on the support point beyond box membership is introduced.

The arbitrary `Fintype` coordinate type has no nonemptiness premise. Hence an empty coordinate set is admitted with empty sums, as claimed. A finite-dimensional rational certificate theorem does not require every true gradient or function value to be rational; these are correctly real-valued here.

### Transfer, epigraph, cutoff and primal completion

`objective_preserving_transfer` assumes feasible embedding, exact objective equality, and a master lower bound. Those are the explicit interface obligations, not an asserted original-model lower bound disguised as a premise. The theorem is elementary but correctly scoped.

The epigraph specialization defines the master set and actually proves graph membership from base-set inclusion and cut validity. It then applies objective-preserving transfer to `(x,h(x))`. The separate underestimator lemma establishes the epigraph cut implication. The family of cuts and base inclusion remain semantic inputs rather than an implemented rational LP construction; Section 5 says so.

`Transfer.lean:70–78`, `incumbent_cutoff_lifting`, assumes a bound only on master-feasible points no worse than an actual feasible incumbent. It derives the bound at the incumbent and proves the remaining points have a larger objective. The desired global bound is the conclusion, not a premise. No minimizer or optimum-attainment assumption appears. The coverage text correctly excludes the VIPR inference invariant that would establish the restricted-set premise.

The sign-normalization and empty-master transfer theorems have the expected conclusions. Empty sets are treated pointwise. `primal_infimum_bounds` proves objective-image nonemptiness from an actual feasible witness and boundedness below from a finite real lower bound before applying real conditional-infimum lemmas. The resulting gap inequalities have the correct directions. The theorem does not identify the real infimum of an empty set with positive infinity. `matching_primal_attains` combines upper and lower inequalities at the witness to prove objective equality and pointwise optimality, rather than presupposing attainment.

## Scope and presentation

Section 5 and `COVERAGE.md` accurately distinguish the proved sufficient correction inequalities from the unformalized supremum equalities and necessity directions. Convexity-to-support reasoning, actual enclosure computation, propagation, rational endpoint extraction, executable parser/kernel behavior and benchmark checking are explicitly excluded.

The revised introduction claims coordinate correction, safe-cut composition, and selected transfer/primal results, which agrees with the sources. The broader handwritten soundness argument in Sections 3–4 is not represented as wholly mechanized. The restrictions are deliberate coverage choices, not unresolved defects in the formalized theorems.

## Independent verification

- Read every theorem statement and proof in the three project modules, rather than relying on the author's theorem map or passing build alone.
- Rechecked `verification/SHA256SUMS`: all 13 recorded source/configuration files matched.
- Reran `scripts/check_imports.py`: all three proof modules are imported exactly once.
- Independently ran `lake env lean Verify.lean`, without a concurrent full build: **95 project-owned declarations passed the transitive axiom audit**. The printed main-theorem dependencies were exactly the permitted standard axioms `propext`, `Classical.choice`, and `Quot.sound`.
- Inspected the audit's module-ownership criterion, private/generated-declaration coverage, nonempty-audit guard, and axiom allowlist. Inspected the pinned Lean toolchain and complete Lake manifest.
- Inspected both author logs. They record successful builds, complete axiom audits and `leanchecker` replay of all project proof modules. The separate source-copy build reused the pinned dependency cache, as honestly disclosed. I did not repeat a full Lean build or a fresh rebuild/replay of all mathlib dependencies.

The saved logs and independent audit support the stated execution claim under the Lean/mathlib dependency base. They are not evidence for unclaimed executable MINLP verification.

## Later-stage obligations

Preserve this coverage boundary in the final abstract, discussion and supplement instructions. Ensure the eventual source archive includes the pinned formal sources and manifest but excludes the development-only dependency symlink. These are packaging/integration obligations already documented, not current mathematical issues.
