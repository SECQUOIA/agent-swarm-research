# Independent review: Stage 00, round 01, reviewer 1

Reviewer: `paper_reviewer_1`. Date: 2026-09-07.

Independence: I prepared this report without reading other reviewers' reports or coordinating conclusions. I reviewed the scaffold, not an unwritten substantive manuscript. Existing statements labelled verified were not treated as proof.

## Snapshot and files

I read `PLAN.md`, `claims-map.md`, `notation.md`, `README.md`, `main.tex`, `preamble.tex`, `sections/00-status.tex`, `reviews/README.md`, all three review templates, and the Stage 00 author handoff. Principal SHA-256 hashes:

| File | SHA-256 |
|---|---|
| PLAN.md | `943457d6888a441c054a0e23b5c3dc69ac0bc6262e71387dc1cf9aca81cdb14a` |
| claims-map.md | `aae5c9883aa3de7c81b5a916a76f9c9ea7634ce3ddc93a39597f7663fa8342f6` |
| notation.md | `6fbcb755c8306fa62f40554696864fe766268b6115d661d3f98be1c9f2d1739b` |
| main.tex | `11f0cd99bd54159fbceec18943ecb3abbf2a5e33c72ff46782189dcc135b5c13` |
| preamble.tex | `69757a0786a132d9f837548aadfe1bd55e7503acb870508d66234e2d74e54572` |
| reviews/README.md | `156af753f118d69a8f9b2ac7d14e8beac9c2bc0a918e70d284e917a675dcd430` |

## Checks performed

1. **Workflow.** The plan implements one author, five independent reviews of the same snapshot, coordinator adjudication, a different correction agent for all valid findings, renewed five-reviewer rounds after any valid major issue, and minor correction before the next stage. It also requires an actual complete-draft review and reopening dependencies invalidated by later changes. This matches the requested process.
2. **Physical interpretation.** The inventory distinguishes quenched wall-to-wall disorder moments from displacement moments and requires an independent identification of the variational quantity with stationary long-time dispersion. It does not define physical dispersion merely to make a Schur formula hold. The nonzero-mean, constant-affinity, fixed positive bulk-diffusivity, and connected-wall conditions are explicit. The distinction between tangential and axial surface diffusion is recorded.
3. **Functional analysis.** Arbitrary nonnegative integrable designs remain eligible for lower bounds. Positive-background realizations, possible infinite responses, trace domains, the constant whole-line source, weighted-form closure, and infinite-energy subtraction are explicit Stage 1/2 obligations. In particular, the text does not already claim a finite inverse for every degenerate design. The measurable-policy versus pointwise-infimum distinction is also explicitly assigned for resolution.
4. **Units.** Independently checking the proposed conversion gives dimensions `[D]=L^2/T`, `[M]=L^3/T`, and `[J]=LT`. The conversion `J_phys=(ell_ref/k_ref)J'` is correct. With a two-dimensional cross-section, `[KV^2/Z]=L/T^2`, so multiplying the dimensional response gives a dispersion with units `L^2/T`. The scaffold correctly prevents direct transfer of dimensionless constants by the prefactor alone.
5. **Selected internal algebra.** The convexity target for all positive q is plausible directly from the quotient representation: for a fixed nonzero test function, the qth power of its quotient is a positive constant times a negative power of an affine nonnegative energy; taking a supremum preserves convexity. This observation does not supply the required domain and extended-value argument. The proposed finite-resolution crossover is algebraically consistent with both listed endpoints: its large-argument endpoint gives a factor `2^(6/5-2+1/20)=2^(-3/4)` and weight `(1-c^2)^(-4/5-3/40)=(1-c^2)^(-7/8)`, yielding the stated beta parameter `1/8`. This is only a consistency check, not a localization proof.
6. **Scope.** The plan includes the baseline, unrestricted moment design, generic folds, exact observation, finite precision, and full-bulk transfer, with the necessary deterministic placement lemma included locally. Excluding general deterministic phase diagrams and unrelated channel constructions is coherent. Both previously open sharp-limit questions remain mandatory investigations, rather than being represented as proved by their order laws or endpoints.
7. **Build.** I ran `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex` from the manuscript folder. Latexmk 4.83 returned success and reported the PDF up to date. This verifies the present entry point, not a future bibliography or final clean build.

## Findings

**No valid Stage 00 defect identified, major or minor.** The potential mathematical problems above are explicitly assigned to substantive stages with suitable exit criteria; their absence from this status-only scaffold is not a proof gap in Stage 00.

The following remain obligations for later reviewers, rather than correction requests for this stage:

- Stage 1 must actually establish the physical/form identification and policy measurability; mentioning these issues does not settle them.
- Stage 3 must settle the sharp supercritical investigation by proof or an explicitly justified corrected theorem; a scaled formal infimum is insufficient.
- Stage 6 must prove conditional variational localization and the intermediate limit; the endpoint algebra checked here cannot replace those arguments.
- Stage 7 and the final audit must inspect primary literature, build the complete document cleanly, and assess its readability and scientific claims. Scaffold approval certifies none of those future tasks.

## Overall assessment

**Accept Stage 00 as a scope and process scaffold.** No major issue was found. The structure is sufficiently explicit about domains, measurable information, physical meaning, dimensional conversion, and outstanding mathematics to support the next stage without pre-certifying its results.
