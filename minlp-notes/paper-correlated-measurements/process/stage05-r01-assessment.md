# Stage 5 first-round adjudication

The coordinator read all five complete reports and the computational main text,
model appendix, new supplement scripts and both source-ranking programs. All 204
frozen files remained unchanged. No major issue was reported; the coordinator
agrees. Independent mathematical reconstructions establish that the current
witnesses and reported bounds satisfy the premises missing from a few checker
assertions. Those omissions are localized verifier-contract defects, not false
scientific results. The failed spacing command is a localized reproduction CLI
defect and does not affect saved witnesses or full validation.

All findings are accepted, consolidated into eight minor corrections:

1. R1: restore static-cost measurement (SCM) and dynamic-cost measurement (DCM).
2. R1: document the intended dropped-zero time labels 7.5,...,60 and the source
   optimizer spacing-map shift to 0,...,52.5, with source lines. Pairwise time
   differences and every feasible schedule are unchanged. Keep all selections,
   times and objective results unchanged; add a short main-text note and source
   README provenance explanation.
3. R2: describe independent standard-normal entries and disclose exact prefixes
   between same-seed 48 and 96 arrays. Do not imply six independent replications.
4. R2: assert exact sum(z)=k for the all-diagonal replay and list feasibility
   among its verified fields. The current saved point already satisfies it.
5. R3/R5: explicitly verify nuisance-block SPD, exact stationarity C G+B^T=0,
   and equality between the direct Schur matrix, quadratic matrix and stored
   mixture_information before accepting a mixture lower bound. Handle empty
   anchors directly. A perturbed-G negative check should exercise this premise.
6. R4: distinguish separator grids: reference and nuisance witness 10^8, bridge
   regression coefficients 10^12, features 10^18, scores 10^8, final logs 10^12.
7. R5: append first-case to the spacing reproduction command and run the fixed
   wrapper in a separate copy, preserving frozen legacy inputs.
8. R5: verify both archive-manifest and source-manifest before validation;
   refresh affected source hashes and check rejection of a changed new source
   or fresh result. Keep hash-integrity checks distinct from witness mathematics.

A separate correction author will resolve all eight, with focused positive and
negative checks and a clean build. No repeat five-reviewer round is required
because no major issue was accepted. Acceptance remains conditional on actual
correction inspection. No finding is rejected or deferred.

The coordinator independently completed the final strengthened full validation
outside the repository in a base-only environment with Gurobi and CVXPY absent:
all 46 archived certificates, all 2347 source schedules and 14,082 objective values,
finite theory checks, sensitivities and fresh witnesses passed in 157.27 seconds.
The record is verification/stage05-root/portability-final.json. Reviewer checks
supply distinct direct covariance inverses, all 31,900 spacing arcs, 1,530 direct
separator patterns, 224 Schur identities and 112 full block sandwich inequalities.
These checks are finite evidence, not formal proof-assistant or external review.

Final disposition: the coordinator inspected all eight corrections in the actual
source, read the focused positive/negative evidence, verified the ten-file diff
and unchanged scientific records, and checked the clean 61-page build. All
accepted findings are resolved. Stage 5 is accepted; the source snapshot and
full 204-file accepted hashes are in process/snapshots/stage05-accepted/.
