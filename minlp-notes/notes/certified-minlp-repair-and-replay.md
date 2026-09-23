# Certified convex MINLP: repair, replay, and readiness

Updated 2026-09-13. This record supersedes the certification claims in the September 12 method note, closeout, and historical benchmark summary. The paper directory has not been edited. Independent reviews below were performed by separate research agents; they are not journal peer review.

Status addendum, 2026-09-20: the record below describes the September 13 state. The [manuscript](../paper-certified-minlp/README.md) now includes a Lean extension completed on September 17 that covers [49 mathematical obligations and typed reference checkers](../paper-certified-minlp/formal/COVERAGE.md). Its [targeted verification record](../paper-certified-minlp/formal/VERIFICATION.md) distinguishes the new checks from the historical three-module replay. References below to future formal verification should now distinguish this completed mathematics from the remaining work to verify Python execution, parsing, library outputs, and their correspondence to the Lean inputs. No Lean proof of the deployed pipeline or benchmark artifacts is claimed. The historical replay outcomes below are unchanged.

The required correctness repairs and final frozen replay are complete. All 289 historical records have an explicit outcome: **188 verified, 92 rejected, and 9 missing artifacts**, with no timeouts or execution errors. The repository supports beginning a scoped methods/software paper, with the qualifications below. A failed replay does not generally establish a false mathematical bound: it can indicate an unsupported curvature rule, an insufficient cut enclosure, an invalid or unsupported proof step, absent evidence, or a resource limit.

## Correctness and interface repairs

The checker no longer trusts a success message from the external VIPR checker. The reported `SOL 0` attack accepted a lower bound of 1,000,000 for `min x` with `x>=1`, whose optimum is 1. A second reproduced upstream defect rounded the continuous inequality `x>=1/2` to `x>=1`. Independent exact proof replay now rejects both. The new kernel validates linear combinations, integer rounding, branch assumptions and their discharge, solution cutoffs, references, lifetimes, declared counts, and the claimed bound. It checks the entire proof, including material after an already sufficient derivation. External checking is optional corroboration.

The nonlinear components now interpret the same exact loaded expression tree. Floating-point leaf values are rationalized before subsequent arithmetic; exact affine extraction, curvature recognition, bounds, fixed values, row shifts, symbolic differentiation, and interval evaluation agree on that interpretation. In particular, `0.1*x*x + 0.2*x*x - 0.30000000000000004*x*x` is recognized as `-2^-55*x*x`, not zero. Original domain conditions are checked before cancellations, and unsupported or singular derivatives are rejected. Unsafe perspective recognition was removed; geometric-mean recognition retains rigorously justified product ranges.

The numerical producer runs on a separate model and contributes proposed points and slopes only. Its floating-point row decomposition does not define the certified mathematics. Both producer and checker use exact reconstructed rows. Master checking retains objective constants and sense, exact integrality/bounds, and a bijective variable mapping. The complete checker exposes a bound only after every obligation passes. Partial checking has a separate status and never returns `ok=True` or a certified numerical bound.

The replay harness preserves historical files, checks every record including prior successes, pins source/environment/tool hashes, and hashes artifact contents before and after checking. It uses separate output files and explicit timeouts, including child processes. Resume is permitted only with matching inputs. Summary comparisons use exact rational values and the original objective sense; reference values remain unverified comparison data.

## Mathematics, novelty, and independent review

The complete [soundness argument](certified-minlp-soundness.md) proves rational cut safety on finite boxes, half-lines, and free coordinates; feasible-point preservation under rational propagation; and objective-preserving transfer from the master. It states the finite-support and domain hypotheses and covers unattained infima. Master-solution cutoffs are handled separately from nonlinear primal witnesses. The theorem is conditional on its arithmetic and checking components; it promises neither completeness nor polynomial proof size.

The [primary-literature audit](certified-minlp-literature-audit.md) corrects the earlier missed comparison to Halbig et al. (2024), and covers safe rounding, outer approximation, VIPR, Wood et al., CakeML, SCIP, and related interval-based software. Certificates for convex MINLP and independent verification are established ideas. The candidate contribution is this particular exact nonlinear-to-MILP replay integration and its computational reliability evidence. No first-certificate or first-formal-verification claim is made; publication priority remains qualified.

Independent audits:

- [Exact semantics, domains, and supporting bounds](review-certified-minlp-exact-semantics.md).
- [Discrete proof parser and inference rules](review-certified-minlp-proof-replay.md).
- [Producer/checker integration and signed objectives](review-certified-minlp-driver.md).
- [Replay, resource handling, and result reporting](review-certified-minlp-replay.md).

The [proof replay contract](certified-minlp-vipr-replay.md) identifies the accepted syntax and trusted arithmetic. The reviews and adversarial tests do not constitute a formal verification of Python, SymPy, mpmath, or python-flint/GMP. No Lean proof of this pipeline is claimed.

The replay cohort is the 289 historical attempts in `cert_all.jsonl`. The earlier selection started from 299 library instances and excluded seven load failures and three cases not recognized as convex. The new replay does not claim to cover every current MINLPLib model. Exact loaded-tree semantics and the repaired sufficient recognition rules can also reject members of that historical cohort.

## Complete historical replay and validation

The authoritative September 13 campaign is recorded in the [complete replay](../code/minlp_solver_lab/results/cert_replay_20260913_complete.jsonl), its [frozen manifest](../code/minlp_solver_lab/results/cert_replay_20260913_complete.jsonl.manifest.json), and the [exact summary](../code/minlp_solver_lab/results/cert_replay_20260913_complete_summary.json). The [campaign audit](../code/minlp_solver_lab/results/cert_replay_20260913_complete_audit.json) supplies every rejected or missing instance name, diagnostics, cohort counts, and integrity checks. The original cohort and every rejection remain in the denominator.

| Current outcome | Records | Interpretation |
| --- | ---: | --- |
| Verified finite bound | 188 | All nonlinear, master-identity, internal proof, and optional external corroboration checks passed. |
| Domain or curvature rejection | 67 | Outside the repaired sufficient recognition rules. |
| Cut-check rejection | 13 | The saved cuts did not pass the repaired sufficient checks. |
| Exact proof-inference rejection | 12 | The saved proof contains an invalid linear-combination step. |
| Missing artifacts | 9 | Required evidence was absent. |
| Timeout, execution error, or detected artifact mutation | 0 | None occurred. |
| Total | 289 | Every original record accounted for exactly once. |

All 188 verified records came from the 269 historically accepted records; 81 historical acceptances did not survive current checking. The 20 previously unaccepted records produced 11 rejections and 9 missing-artifact outcomes. These counts supersede the old 269/289 certification claim. They do not imply that the mathematical bounds of all rejected records are false.

An [independent arithmetic audit of the 12 failed proofs](../code/minlp_solver_lab/results/cert_proof_failure_audit_20260913.json) confirms eleven claimed right-hand sides stronger than their exact linear combinations justify, and one combination of incompatible inequality directions. These are defects in the saved proof steps, rather than reasons to relax the checker. Corrected evidence is needed to recover those cases.

The campaign used six concurrent jobs with a 1,200-second per-record limit, including checker child processes. [Measured wall time](../code/minlp_solver_lab/results/cert_replay_20260913_complete_timing.json) was 1,465.381 seconds (24 minutes 25 seconds). The 188 verified proofs total 38,826,726,525 bytes (38.827 decimal GB). Their summed per-record checker wall time was 7,987.954 seconds; the longest verified check took 463.845 seconds. Summed worker times overlap and must not be reported as campaign elapsed time or pure proof-kernel time. These measurements characterize replay on this recorded environment, not a solver-speed comparison.

Of 188 checked bounds, 52 have nonnegative normalized distance at most `1e-4` from the recorded primal reference, and 81 at most `1e-2`. The normalization is `sense * (reference - bound) / max(1, abs(reference))`. Another 23 references lie strictly beyond their checked bound, all by less than `6e-10` in normalized magnitude; the strict summary does not count those as closed gaps. Reference rounding or numerical feasibility can matter, and none of these comparisons alone certifies optimality. The summary also records 18 solver-objective comparison flags at its stated `1e-6` scale threshold. Apart from the independently audited cases below, those flags have not been attributed to a solver defect.

The final frozen-source regression suite passed **152 tests** in 2.20 seconds. It includes adversarial arithmetic, parser, domain, integrality, signed-objective, producer, replay, and process-timeout cases. The [final validation record](../code/minlp_solver_lab/results/certified_minlp_final_validation.json) additionally confirms unique record coverage, exact bound/sense arithmetic, absence of bounds on rejected records, unchanged source and historical-input hashes, three successful fresh replays, and no paper changes. This structural audit is distinct from the independent source reviews and is not a second proof-checker implementation.

Two preliminary campaigns were stopped after conservative proof-format compatibility gaps were corrected. Their records and partial summaries are retained as incomplete evidence; neither contributes to the authoritative counts above.

## Fresh generation and independent case studies

After the repairs, the producer generated new certificates for `batchdes`, `clay0204m`, and `risk2bpb` using 60 seconds of OA search and 90 seconds per exact-SCIP attempt, one requested solver thread, and three concurrent jobs. All three passed complete checking and a [separate frozen replay](../code/minlp_solver_lab/results/cert_regenerated_20260913_complete_summary.json). The [generation records](../code/minlp_solver_lab/results/cert_regenerated_20260913.jsonl) preserve the attempts and budgets. These are targeted repair regressions, not a full new solver-performance benchmark. The producer can try a fallback configuration, and completion/checking time is additional to the search budgets.

The [old `risk2bpb` first-cut audit](../code/minlp_solver_lab/results/solver_discrepancy_audit/risk2bpb_cut1_replay.json) shows that its intercept exceeds its newly justified safe intercept by about `1.169668e-12`. This fails a sufficient verification condition; it does not prove that the old cut is globally invalid. The new producer computes admissible intercepts and obtains a fully checked bound approximately `-55.87613939501907`. No tolerance is used to admit the old cut. The checked bound rounds to its recorded MINLPLib reference, `-55.8761394`, at the displayed precision. The tiny strict reference/bound disagreement is therefore consistent with reference rounding and does not establish a solver error.

The [solver discrepancy audit](certified-minlp-solver-discrepancies.md) independently checks symbolic source-model equivalence under a common exact-binary64 interpretation and returned-point residuals for the two highlighted cases. SBB's `clay0204m` point violates two linear rows by 4.5 and 3; its actual status was Integer Solution, not Optimal. SHOT's `risk2bpb` point sets two variables to one despite bounds fixing them to zero. These are invalid returned solutions in the recorded integrations; they do not identify the responsible internal solver component.

For `clay0204m`, the checked lower bound is exactly 6545 and a separately checked rational feasible point has objective 6545. The [joined certificate](../code/minlp_solver_lab/results/solver_discrepancy_audit/clay0204m_optimality.json) therefore proves its exact optimum. This claim is supported by the actual nonlinear witness and is not inferred from a rounded reference value. Other near-reference lower bounds are not labeled optimality certificates.

The [self-contained quadratic bundle](../code/minlp_solver_lab/certify/examples/quadratic/README.md) supplies a small source model, nonlinear lemmas, rational master, complete proof, and feasible witness. It establishes optimum `1/4` and was replayed in an isolated environment with only the five listed checker dependencies, without numerical solver packages.

## Remaining boundaries

The implementation deliberately refuses cases outside its sufficient curvature/domain/derivative and proof rules. Perspective recognition on actual ratio domains, general nonsmooth subgradients, nonlinear equalities, general nonconvex optimization, and broader modeling syntax are not supported. Supporting them is further research or engineering, not an implicit claim of this result.

Large proofs and difficult nonlinear models can exceed the replay budget. A timeout or conservative rejection must remain visible in experimental reporting. The historic 269 acceptance labels cannot substitute for a successful current replay. The benchmark's original mixed search budgets also preclude a fair solver-speed ranking.

The trusted base remains the loader, exact reconstruction and curvature rules, interval and symbolic libraries, master identity code, exact proof kernel, arithmetic libraries, and runtime. Formalizing a few lemmas would not verify this whole executable. A full proof-assistant checker, automatic nonlinear primal certification for the entire benchmark set, proof compression, and broader convexity recognition are possible extensions rather than prerequisites for the scoped lower-bound method.

Reproduction commands and supported contracts are in [certify/README.md](../code/minlp_solver_lab/certify/README.md). The full benchmark models and large proof files remain local data excluded from version control; the replay manifests identify their contents by hash. Reproducing that campaign requires those artifacts. The small quadratic example is included in the repository and can be replayed independently.

## Research readiness

The repository now provides enough mathematical, implementation, and experimental evidence to begin a focused methods/software paper on checkable convex-MINLP bounds. No further mandatory research blocker has been identified for that stated scope. Rejected and missing historical certificates limit demonstrated coverage and must remain in the denominator; recovering every one is not a prerequisite for describing the implemented method honestly.

This does not mean the topic is fully developed or that an unwritten manuscript is submission-ready. Broader convexity coverage, general nonlinear primal certification, formal verification, and proof-size improvements remain useful extensions. The publication case rests on the concrete integration and its reliability evidence, with a careful comparison to existing certificate methods. The paper should use the corrected replay results and explicit trust assumptions rather than the superseded historical acceptance and optimality counts. No paper text was written or edited in this task.
