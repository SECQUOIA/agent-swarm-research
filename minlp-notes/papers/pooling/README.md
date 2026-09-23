# Pooling complexity manuscript

This folder contains **The Complexity of Pooling: Algebraic Barriers and Structural Algorithms**, its LaTeX sources, bibliography, verification scripts, and review records. The manuscript is anonymous; no author or submission status is implied.

The main results concern existential-real completeness, restricted physical hardness, and exact structural and contract algorithms. Section 6 explains their implications and the remaining classification question. Appendix A gives physical response and geometry proofs, Appendix B treats isolated rank-one costs, and Appendix C proves exact and uniform approximate convexification bounds.

All essential proofs are included in the manuscript or use explicitly stated results from the cited primary literature, including identified preprints. The thirteen former companion-note citations are no longer proof dependencies: the repository evidence in [source-index.md](source-index.md) records which five results were incorporated and which eight tangential comparisons were removed. A standard LaTeX build does not require the repository literature archive or those research notes.

## Build

From this directory, run:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. The required source directories are `sections/`, `appendices/`, and `figures/`, together with `main.tex` and `bibliography.bib`. The build uses standard LaTeX packages and BibTeX.

## Current revision and evidence

The links, logs, scripts, and commands in this section and below are repository evidence. They assume this folder remains at `papers/pooling/` in the full repository and are not included in the submission archive. [submission-README.md](submission-README.md) supplies the portable build instructions used as `README.md` in that archive. Exact inspected versions of the two author-hosted conic sources are recorded internally in [primary-source-versions.json](revision-20260909/primary-source-versions.json).

The September 9, 2026 revision is complete. Deliverables are the [105-page paper](main.pdf), [portable LaTeX archive](pooling-latex-source.zip), and [final report](FINAL-REPORT.md). Four development stages and a whole-manuscript stage each received five independent reviews followed by a separate correction pass. Root adjudicated all findings and verified every accepted correction; no accepted issue remains unresolved. The [status record](revision-20260909/STATUS.md) links the retained evidence. The source archive was extracted into an empty directory and built using its own README command; [final validation](revision-20260909/checks/final-package-build/validation.json) records source hashes, artifact hashes, all 39 cited bibliography entries, and the clean build. [The Stage 4 author report](revision-20260909/reports/stage4-author.md) records the standalone appendix development and source decisions.

Earlier process and verification directories are historical evidence for earlier source versions. They do not certify the current revision. Internal review and finite computational checks are not external peer review or formal proof certification.

The Stage 4 exact checks additionally cover the imported unit-margin penalty and correlation-face rounding bounds:

```sh
python ../../code/rank_one_zero_lower/verify_penalty.py
python ../../code/rank_one_hardness/audit_face_stability.py
```

Both use the Python standard library. The latter exhausts equal-total margin pairs on the quarter grid for one and two paired indices; it checks the constants and boundary cases, not the published conic extension-complexity theorems. Current Stage 4 logs are under `revision-20260909/checks/`.

## Supplemental exact checks

These scripts use Python's standard library:

```sh
python verification/check_foundations.py
python verification/check_endpoint_scope.py
python verification/check_one_pool_etr_exact.py
python verification/check_reviewer02_physical.py
python verification/check_matsui_source_bound.py
python verification/check_positive_tolerance_boundary.py
python verification/check_stage03_reviewer07_gadgets.py
```

They check cyclic decomposition and conditioning examples, nonfacial integrality counterexamples, endpoint-quality scope, and physical witnesses for the algebraic reductions using exact rational arithmetic. Their finite checks supplement the manuscript's proofs.

The final three scripts check the repaired positive-product source estimate, a physical example where positive quality tolerance destroys integral optimality, and local copy/averaging/splitting identities. Logs for additional repository checks are retained in `verification/logs/`; those using LP or nonlinear solvers are explicitly distinguished from exact rational checks in the process records.

Two independent reviewer checks require NumPy and SciPy:

```sh
python verification/check_stage03_orientation.py
python verification/check_stage03_signed_modes.py
```

They compare small physical endpoint-branch LPs with exact combinatorial enumeration, including omitted pool bounds, signed rewards, and separate arc capacities. Their LP comparisons use floating-point arithmetic.

The source-diagram check requires SymPy:

```sh
python verification/check_etr_source_identities.py
```

It verifies exact rational identities and full-box interval enclosures for the two external arithmetic diagrams used by the algebraic-degree argument. It does not verify the external paper's broader universality claims.

The structural-stage checks use the existing repository scripts (paths below are relative to this manuscript directory):

```sh
python ../../code/fixed_core_blocks/check.py
python ../../code/pooling_bypass_copy/check_structure_mapping_review.py
python ../../code/pooling_bypass_paths/check_boundary_projection_review.py
```

The first requires NumPy, SciPy, and SymPy and combines exact support identities with numerical LP comparisons. The second requires SymPy and checks exact arc ownership and balance identities. The third uses only the standard library and checks exact planar compositions and degenerate slices. They do not implement the full algebraic optimization algorithm or establish the asymptotic size bounds. Root logs are `fixed-core-support.txt`, `bypass-structure-mapping.txt`, and `boundary-projection-exact.txt` under `verification/logs/`.

The contract-stage checks also use existing repository scripts:

```sh
python ../../code/pooling_bypass_paths/check_fixed_product_contracts.py
python ../../code/pooling_bypass_paths/check_quality_scaled_cuts.py
python ../../code/pooling_bypass_paths/check_fixed_rank_scaled_cuts.py
python ../../code/pooling_bypass_paths/check_fixed_rank_chart_algebra.py
python ../../code/pooling_bypass_paths/check_path_cut_clamps.py
python ../../code/pooling_bypass_paths/check_box_divergence_support_review.py
python ../../code/pooling_bypass_paths/check_box_rank_support_second.py
python ../../code/pooling_bypass_paths/check_two_quality_convex_feasibility.py
python ../../code/parametric_path_lp/check_affine_strip_projection_review.py
```

The fixed-product and two-quality checks require Gurobi and a working license. The two cut comparisons use NumPy/SciPy through their local helper module; the chart-identity check uses SymPy. The clamp, two divergence-support checks, and affine-strip check use the standard library and exact rational arithmetic. Logs prefixed `stage05-` and [the root audit](process/root-stage-05-check.md) distinguish exact arithmetic from numerical physical-network comparisons.

The response and geometry checks use exact standard-library arithmetic:

```sh
python ../../code/parametric_path_lp/exact_shadow_check.py
python ../../code/parametric_path_lp/exact_physical_penalty_check.py
python ../../code/parametric_path_lp/exact_fixed_alphabet_check.py
python ../../code/parametric_path_lp/exact_rank_one_slab_check.py
python ../../code/parametric_path_lp/exact_strict_local_check.py
python ../../code/verify-rank-one-costs.py
```

The additional projected-box test requires NumPy, SciPy and SymPy:

```sh
python verification/check_interaction_rank_two.py
```

It verifies all proposed hull classifications and comparisons using exact rational certificates. Its scope and the other checks' limits are recorded in [the stage-6 root audit](process/root-stage-06-check.md), with logs prefixed `stage06-`.

The independent physical-interface comparison uses NumPy and SciPy:

```sh
python ../../code/parametric_path_lp/physical_vertex_forcing_check.py
```

It assembles original network balances and quality rows at fixed pool qualities and compares numerical LP optima with the exact predicted vertex extensions. It does not certify a global nonlinear optimization algorithm.

A separate exact physical reconstruction check uses only the standard library:

```sh
python verification/check_stage06_physical_exact.py
```

It checks original network constraints and economics for the descending path, the two-quality relay with the nonlinear interface, and nongeometric supply sequences, at endpoint and midpoint flows with several clean-flow amounts. The retained run covers 4,482 rational cases; it supplements the general proof.

The zero-lower/unit-upper general-cost margin refinement has a separate exact checker:

```sh
python ../../code/rank_one_zero_lower/verify_penalty.py
```

Its retained run passed 2,000 rational repair and objective-penalty cases. The historical whole-paper reviewers also retained distinct [integer-flow/cut and greedy-support checks](process/whole-round-02/review08-check.py), [symbolic residual equations](process/whole-round-02/review09-check.py), and [physical interface and slab checks](process/whole-round-02/review11-check.py), each with its output beside it. Run those scripts from the repository root; the symbolic check requires SymPy, and the other two use only the standard library. These checks supplement the general proofs.
