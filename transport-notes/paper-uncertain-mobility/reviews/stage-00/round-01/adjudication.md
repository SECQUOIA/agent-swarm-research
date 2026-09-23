# Coordinator adjudication: Stage 00, round 01

Coordinator: `/root`. Date: 2026-09-07.

Reviewed snapshot: `1e46dddf69ca6d87bf8b3b56792a8e0181bb493a561d9ac29e4f4ba26b88bd5f`, recorded in [snapshot.json](snapshot.json). All five reports identify the same principal source hashes. The author stopped editing before reviews were dispatched; the manifest was recorded during the review round before any corrections.

Five independent reports were received from `paper_reviewer_1` through `paper_reviewer_5`. Each describes its own checks; none relied solely on historical verification labels. Reviewers 1 and 5 found no actionable defects. Reviewers 2–4 identified overlapping minor omissions. The coordinator agrees with their substance and severity: these are defects in the preparation documents, while the associated model derivations remain expressly assigned to Stage 1.

| Finding | Source | Decision and severity | Required correction |
|---|---|---|---|
| R2-01; R3-02; ensemble portion of R4-01 | Reviewers 2, 3, 4 | Valid, minor. Exact constants depend on a rate law, circle length, and probability density not yet stated together in the inventory. | Define the dimensionless circle, `k_c=(c+cos s)^2`, and uniform `c∈[-2,2]`; identify its equal-bin observation. |
| R2-02; R3-01; wall-drift portion of R4-01 | Reviewers 2, 3, 4 | Valid, minor at this stage. Constant affinity alone does not give the displayed mean or constant surface source. | State zero longitudinal surface advective drift, distinguish axial molecular diffusion, and restrict the reversibility statement to the transverse process. |
| R2-03; R3-03; R4-02 | Reviewers 2, 3, 4 | Valid, minor. The Gaussian example conflicts with the reserved area symbol. | Use independent standard Gaussian amplitudes `ξ_1,ξ_2` and update the lower bound and notation ledger consistently. |
| R4-03 | Reviewer 4 | Valid, minor. The handoff conflates recording the reviewed version with recording acceptance. No mixed-version review occurred. | Link the round manifest and clarify that future manifests precede dispatch; accepted corrected versions receive a separate record. Preserve the present manifest. |
| C00-01 | Coordinator | Valid, minor. The broad periodic-removal audit is not the closest source for singular surface exchange. | Change the final surface-exchange audit link in `claims-map.md` to `../notes/singular-exchange-prior-art.md`. |

No findings were rejected. Explicit future proof obligations are not accepted theorems and are not defects caused by their absence from the scaffold. In particular, the domain, measurable-policy, supercritical sharp-limit, and interior-crossover investigations remain mandatory stage work.

A separate correction agent will fix every item above and record the edits. There is **no valid major issue**, so the user process does not require a second five-reviewer round for these minor corrections. Stage 00 remains unaccepted until the coordinator checks the fixes and records acceptance.
