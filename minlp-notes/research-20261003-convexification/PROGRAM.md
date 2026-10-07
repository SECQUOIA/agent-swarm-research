# Completion of the joint-convexification work

The user requested completion of the concrete work left after the first
joint-convexification study, including promising extensions. The earlier
study and its unfavorable benchmark remain unchanged in
`research-20261002-convexification/`.

This phase addresses the five remaining needs explicitly identified in the
conversation. Completion requires working algorithms, proofs where claimed,
independent review, reproducible evaluation, and an honest account of failures.
A favorable performance outcome cannot be guaranteed or substituted for by
changing the test population after seeing results.

## Required deliverables

1. **Integration that retains the original model.** Derive cuts directly in
   original variables from joint support and nonnegative combinations of
   original constraint sides. Retain the native nonlinear rows and presolve
   behavior. Avoid the duplicate graph-auxiliary reformulation used in the
   earlier approach. Include objective directions and a fixed,
   bounded automatic activation policy.
2. **Broader model support without silent changes.** Check original-row
   arithmetic, use certified consequences of original affine constraints,
   support valid variable powers, and explicitly preserve source domains.
   Necessary domain witnesses may be shared by every comparison mode.
   Unsupported cut domains must remain explicit; admitting a model does not
   imply that every expression can receive a certified cut.
3. **Separation with a complete stated return contract.** Implement an
   epsilon-separation procedure that returns a proved separating inequality
   or a proved normalized-distance bound within the specified class. Prove
   termination of its finite fallback, state its actual complexity, and
   distinguish resource exhaustion in the practical bounded mode.
4. **Support beyond pairs and stars.** Prove and implement exact quadratic
   support over bounded rational polytopes in general fixed small dimension,
   including lower-dimensional and singular cases. Establish the hardness
   boundary when block dimension is unrestricted. Attribute classical
   optimization and convexification ingredients accurately.
5. **A new prospective evaluation and final document.** Freeze a new test
   population independently of the old outcomes, use longer runs and
   prespecified repeated seeds, verify every retained cut, and check original
   incumbents independently. Integrate all mathematical, implementation,
   literature, and computational evidence in one reviewed report.

These are completion requirements, not a promise to prove a universal
polynomial-time hull algorithm or a universal runtime improvement. A negative
result must close the corresponding investigation with evidence and a clear
deployment decision, rather than disappear from the report.

## Work boundaries

All new work stays within this topic. Prior datasets and source snapshots
are preserved. Only targeted topic checks are run; no project-wide local
verification or CI inspection is allowed. New solver runs use managed process
groups, explicit limits, one worker, and one solver/BLAS thread. Other ongoing
jobs in the shared workspace are left alone.

No commit, pull request, deployment, or external message is needed. Internal
agent reviews are distinct from external peer review and formal verification.

Status: all five required deliverables are complete and reviewed. All 282
prospective jobs and all 75 matched repair-validation
jobs finished. All 165 recorded cuts passed replay; four original failed-worker
cut logs remain unknown. The corrected cohort has no worker errors or missing
cut logs. The integrated 25-page report is built and reviewed. The completion
record and verification commands are in `CLOSEOUT.md` and `VERIFICATION.md`.
