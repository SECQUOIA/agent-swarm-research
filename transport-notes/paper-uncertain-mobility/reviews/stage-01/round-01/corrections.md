# Corrections: Stage 01, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the Stage 01 author. Date: 2026-09-07.

Input reviewed snapshot: `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`, preserved in [snapshot.json](snapshot.json). I read all five reports and the [coordinator adjudication](adjudication.md). The adjudication accepts three minor issue groups and no major issue.

| Accepted findings | Corrected source locations | Correction and reasoning |
|---|---|---|
| R1-01, R3-01, R4-01, R5-01 | `sections/01-model-transfer.tex`, lines 23–24 and 246–254 | Added `0≤D_b^x<∞` and nonnegative `D_s^x∈L¹(Γ)` at their first introduction. Explained that stationarity gives finite expected integrated diffusivity `t D_mol`, so the Brownian stochastic integral is square integrable with variance `2t D_mol`; its conditional mean given the transverse path is zero. Preserved the final comparison's separate uniform-bound requirement. |
| R1-02, R4-02, R5-02 | Same section, lines 266–278 | Added the kernel projection `g_0`, zero-energy trials `w_n=n g_0`, and objective `2n‖g_0‖²→∞`. On the complementary positive spectral subspace, specified inverse cutoffs on `[1/n,n]`, their objectives, and monotone convergence, including divergence without a zero atom. Both sources of an infinite spectral inverse are now covered explicitly. |
| R4-03 | Same section, lines 112–119 | Defined closability by its precise null-limit, energy-Cauchy sequence criterion. Explained that it makes the form completion embed unambiguously in L² and identifies a unique minimal closed form. The following positive-background proof already verifies this criterion. |

Only `sections/01-model-transfer.tex` differs among the nine files in the reviewed manifest. Its corrected SHA-256 is `1a9675e3d4ba4507806067672113afea7a0bc0c1ec3696b0b48badaf8f0213b0`. The manifest, all five reports, and the author handoff remain unchanged. No later-stage text or historical source note was edited.

Verification:

- Forced the manuscript and bibliography build with `latexmk -pdf -g -interaction=nonstopmode -halt-on-error -file-line-error main.tex` from the manuscript directory. It exited with status 0 and produced the eight-page PDF.
- Checked the final `main.log`: no warnings, undefined-reference notices, overfull boxes, or underfull boxes.
- Compared all source hashes against the reviewed manifest; only the intended section changed.
- Ran `git diff --check`; it passed.
- Rechecked the added zero-mode objective and the cutoff objective directly. The kernel projection is in the closed form domain with zero energy; the bounded positive inverse cutoffs are also form-domain elements, so these trials are legitimate.

These edits clarify assumptions and complete local explanations; they do not change the main flow-only comparison, admissible policy class, or substantive stage scope. No correction exposed a major issue.

Editing is complete. The coordinator must verify the minor fixes and separately record acceptance. This record does not accept Stage 01 or authorize starting Stage 02.
