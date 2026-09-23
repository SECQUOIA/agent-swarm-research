# Stage 6, round 1 — independent review 05

Recommendation: accept the mathematics, implementation and reported evidence after one minor README correction. No major issue was found.

## Snapshot and independence

Reviewed `process/snapshots/stage06-round01`, with manifest SHA-256 `b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`. All 30 listed files matched. The isolated copy, build and supplementary checks are in `verification/stage06-review05/`. A final check confirmed that all 30 source, data and figure hashes still match; see `hash-verification.json` there.

I read the entire new section, all eight new Python files, the data-generation and table logic, the recorded measurements, README, coverage and bibliography. I also read the relevant convex solver, screening/MILP and instance-generator dependencies, and compared the paper scalar solver with its original. The author report and preserved measured sources were inspected as evidence, not treated as proof of correctness. I did not read other current reviews or root conclusions, delegate, edit manuscript or frozen files, or overwrite official results. Repository imports were supplied explicitly for the isolated checks because the frozen copy has a different parent path.

## Major findings

None.

## Minor findings

**R05-M1 — Remove a stale future-tense computation promise.**

Location: `README.md:36`: “Later computation stages will add reproduction commands and their actual logs.” Stage 6 now supplies those commands, inputs and logs in the same README and archive. The sentence is stale and makes the reproduction status less clear.

Requested fix: delete this sentence or replace it with a direct pointer to the stage 6 reproduction section. The following distinction between historical measurements and fresh runs should remain. This is a documentation issue only.

## Mathematical and implementation review

**Convex paths and sweep, section 6.1.** The active-status equations, bound signs and closed interval tests are necessary and sufficient under positive definiteness; checking affine conditions at both interval endpoints is sufficient, including singleton intervals. The small-system formula has the correct order `I+SH`, and its determinant identity does not require invertible or positive-semidefinite `H`. Exhaustive status enumeration supplies complete coverage. The upper objective becomes a rational quadratic, and the endpoint/interior-minimum comparison is complete.

I read `quadratic_solver.py` through validation, pattern recovery, coverage, upper optimization and the aligned sweep. The numerical routine proposes statuses; exact recomputation, query containment, segment verification and final coverage determine acceptance. Failure/cap behavior matches the text. The aligned sweep correctly initializes signed and zero loadings, groups simultaneous events, updates the weighted sums and uses the strictly increasing effective-price map. Negative rank-one coefficients are admitted only when the full Hessian passes the positive-definiteness test. The fused upper objective includes both its quadratic leader term and cross term with the affine response. Its arithmetic-operation count is distinguished from bit cost and input validation.

**Nonconvex scalar atlas, section 6.2.** Strict convexity on each aggregate fiber makes the reduction exact even when the full Hessian is indefinite. Signed multiplier events produce the whole aggregate interval; zero slope intervals and infinite tails contribute endpoints, while a singleton aggregate is handled separately. Endpoints, positive-curvature stationary branches and zero-curvature flat prices are complete candidates. Comparing their original values, rather than stationarity, proves globality. Identically winning value polynomials have equal derivatives and therefore the same aggregate because `gamma` is nonzero; unique fiber allocation then identifies the original response.

The upper-optimization proof correctly treats an interior singleton produced by upper rows, endpoint limits of open price cells, constant revenue, and attained ties. At isolated prices it tests every component, using both endpoints for universal upper feasibility and worst revenue. The proof's degree-two output guarantee is per selected output, not for a compositum containing the entire atlas.

I read `compressed_solver.py` in full. Its rational fiber coefficients, clipped branch domains, original candidate costs, incremental insertion, retained contact list and point reconstruction implement these distinctions. In particular, the point reconstruction compares all valid original candidates and restores flat intervals. Tangencies and isolated branch domains are retained. The insertion argument is valid: a final global tie cannot have been strictly dominated by a branch already present when the later tied candidate was inserted. Open-cell clipping and pointwise optimistic/pessimistic optimization match the theorem. The only algorithmic differences from the original scalar solver are the claimed exact rational sign and midpoint fast paths; the algebraic fallback and contact logic are unchanged.

**Original contacts, section 6.3.** The affine minorant proves equality of tilted optimum values after convexification, while equality between the original cost and envelope identifies the actual contacts. The extra contact condition is essential and is retained in the executable candidate method. The one-variable false-feasibility example has actual contacts `{0,1}` at price two, and its optimistic maximum and unattained pessimistic supremum are correct. I independently checked the three quadratic pieces, the two contact aggregates, original response vectors, common value, capacity selection and `51/160` upper value in the two-variable example. The comparison with the two contacts supplies the claimed behavior on either side of the switch; it does not assume convexity of the middle piece.

**Independent original-coordinate baseline, section 6.4.** The checked nonzero-principal-minor restriction is sufficient: a global minimizer's minimal free-face Hessian is positive semidefinite and nonsingular, hence positive definite. Thus every global response appears among the enumerated stationary faces. Retaining feasible KKT candidates and comparing original quadratic costs removes nonglobal stationary points. Fixed box coordinates correctly need no gradient sign. Nonzero minors preclude a missing flat continuum; the old singular-face argument is correctly described only as preserving a fixed-price global value.

I read `original_faces.py` in full. It does not import the compressed solver. It checks all principal minors, uses exact Sylvester tests for free faces, solves the dense original system, computes its original cost coefficients, intersects valid intervals, and forms all pairwise crossings. Both isolated cut responses and open-cell winners are retained. The independent upper implementation correctly handles row intersections, pessimistic universal feasibility, worst revenue, limits and preference for an attained value in a tie. Rejecting singular inputs is explicit rather than silently skipping a potentially necessary continuum.

**Screening and numerical comparison.** The code uses the accepted ellipsoid/closure certificates, exact dense KKT reconstruction and exact scalar interval intersections. Inversion and screening are included in measured solver costs; the completed status count is a cell/status assignment count and is not misrepresented as the total runtime bound. The displayed MILP has the correct lower/upper indicator and gradient signs, and its big-M bounds are valid for the unit box and bounded price interval. The paper distinguishes the exact real-arithmetic formulation from numerical solution reports. The default numerical discrepancy and the tighter follow-up are retained and are not presented as rational optimality certificates.

## Reproducibility and quantitative evidence

The clean isolated build produced a 73-page PDF. The final log has no warnings, undefined references/citations, or overfull/underfull boxes. I visually inspected pages 45–55, including all new mathematics, the contact figure and all three tables. Labels, legends, captions, columns and displayed equations are readable and stay within the page area. The figure depicts the specified functions and distinguishes the two original contacts from the false convexified segment.

I checked the 60 recorded workers: all have successful exit codes and distinct method/instance/repetition keys. I independently checked agreement of all recorded same-task exact values and attainment flags, including repeated-type values against the proved `51m/160` formula. The tables regenerate exactly from the archived records and historical comparison file. Scalar generated data match the prepared JSON, and the regenerated convex/screening input archive is byte-for-byte identical. The input families, seed arithmetic, indefinite-Hessian normalization and capacity/service rows agree with the prose.

The recorded solver/dependency hashes match the current sources. The two changed driver/helper hashes match the preserved `measured-run-experiments.py` and `measured-check-full-task.py` files. I inspected their diffs: they add output-directory creation, prepared-input archival and hash-list entries outside worker timing. They do not change the measured solver task. The separate profile and ordinary paired measurements, independent column medians, total versus worker wall time, numerical follow-up exclusions, repeated-type population and unattempted large baseline sizes are all qualified appropriately. The results support the stated mixed small-instance timing comparison and negative screening result, not a general speed superiority claim.

The following independent reruns completed successfully in the isolated area:

- `check_full_task.py`: all 18 adversarial/seeded instances pass both upper semantics, response-set comparisons on the original-coordinate strata, and attained-witness checks. Singular rejection, flat intervals, fixed boxes, singleton aggregates and exact fast-path regressions also pass. The produced records are under the isolated `verification/stage06-author/full-task-checks.json`.
- `convex-certificates.log`: 33 dense-LP comparisons, 24 quadratic dense-face comparisons, five hand quadratic cases and five aligned boundary cases pass, along with the diagnostic's corrupt/missing certificate and forced-failure contracts.
- `scalar-envelope-checks.log`: 350 original-coordinate value comparisons, 72 point/cell response comparisons, 30 incremental-versus-full-partition comparisons and 11 explicit edge cases pass against the paper scalar solver.
- `worker-reproductions.json`: reran the convex `N=100` worker and screening `N=8` worker. Exact convex KKT and service checks pass. Screening reproduces the rational optimum `4810519997/235205877942`, exact returned-point checks, and the default MILP difference approximately `-3.37031436e-7`. The forwarded HiGHS option warning is expected and was visible in the rerun.

These checks do not repeat all 60 timings, establish a statistical speed guarantee, or formally verify the general algorithms. I did not overwrite the paper's official measurements, historical files or figures. Recomputed private tables and prepared inputs remained identical to the frozen artifacts.

## Attribution and remaining limits

The new text supplies its own candidate, contact and baseline proofs. I checked the narrow convex-envelope attribution against the original Moehle–Gindi–Boyd–Kochenderfer paper, section 6.3 and appendix B; it does describe recursive piecewise-quadratic envelope construction. The manuscript imports neither its tangent formulas nor a claim that convexified contacts are automatically valid original responses. Source: [published paper](https://web.stanford.edu/~boyd/papers/pdf/portf_constr_lcso.pdf). I did not conduct another broad novelty search or independently recheck every older citation in the manuscript.

The coverage record assigns all required scalar algorithms, original-contact reconstruction, independent full-task comparison and computational qualifications to concrete stage 6 locations. Final abstract, overall synthesis and the final integrated review remain stage 7 obligations rather than missing stage 6 work.

## Optional suggestions

None requiring a separate change. A final whole-paper pagination pass remains appropriate after stage 7 is added.
