# Stage 3, round 1: implemented repairs

A separate repair agent implemented only M1 and m1–m4 accepted in `adjudication.md`, plus the affected coverage descriptions. No later stage was started. The repaired section is frozen for root inspection and the required second round of 15 independent full-stage reviews; this repair record is not an external certification or a completed-stage verdict.

## Exact manuscript changes

- **M1, introductory certificate scope:** stated input qualities in `[0,1]` and only upper output quality bounds in `{0,1}` before invoking `s1:endpoint-or`. The sentence now explicitly concerns threshold decision.
- **M1 and m4, `s3:local-degrees` and `s3:all-two-thm`:** named “pooling threshold decision” and stated that only upper output quality specifications are imposed. The hardness reductions, degree restrictions, and flow-bound hypotheses are unchanged.
- **M1, `s3:weighted`:** explicitly limited output quality specifications to upper bounds. The tolerance proposition inherits the corrected upper-only family through `s3:all-two-thm`.
- **m1, weighted proof:** each retained mode edge is bounded by the minimum of its pool capacity and the capacities of its two physical arcs, omitting absent arc bounds. The proof explicitly notes that these edge bounds are integral before applying bipartite-flow integrality.
- **m2, `s3:matsui` proof:** replaced the vacuous negative lower bound on a magnitude with the lower bound on each signed term. The displayed separation inequality is unchanged.
- **m3, `s3:constant-thm` proof:** changed only the first comparison in `V_i <= u_0 + s p^{2n} < 3P_4` from strict to non-strict. The strict bound below `3P_4` and all normalization conclusions remain unchanged.

Updated four rows in `process/coverage.md`: `results/pooling-one-quality-degree-two-hardness.md`, `results/pooling-all-degrees-two.md`, `notes/pooling-positive-tolerance-extension.md`, and `notes/pooling-all-degrees-two-investigation.md`. They now state the upper-only quality scope, identify threshold decision for the initial NP-completeness claims, retain physical arc capacities in the weighted description, and mark the second full review as pending.

## Checks

- Compared the repaired section with the frozen round-1 snapshot using `diff -u`; every change is one of the accepted repairs or local line wrapping.
- Checked the corrected certificate hypotheses against the accepted endpoint certificate in Section 1. Arbitrary additional lower quality restrictions are excluded by the repaired statements.
- Checked that the minimum mode capacity enforces both physical arc bounds and remains integral; the original throughput is feasible in that retained-mode network, so the existing integral replacement argument applies.
- Checked the signed estimate: for a remaining pair other than `(k,k)`, `i+j <= 2k-1` and `s_ij-r_i r_j >= -1`, giving the stated lower bound `-p^{2k-1}`.
- Checked the attained bound at the unrestricted `s_nn` generator: `X=0` and `Y=s p^{2n}`, so `V_i=u_0+s p^{2n}`. The following strict estimate is preserved.
- Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `papers/pooling`. Exit status 0; `main.pdf` was produced with 40 pages. Inspected `main.log`: no LaTeX/package warnings, overfull or underfull boxes, undefined references or citations, multiply defined labels, or rerun requests. Matches for package metadata containing the words “warning” or “rerun” were not diagnostics.
- Verified that Sections 1–2 and `bibliography.bib` retain their pre-repair SHA-256 hashes.

## Frozen hashes

| File | SHA-256 |
|---|---|
| Round-1 input `process/snapshots/stage-03-round-01.tex` | `2d8f3082b7fce0a5da15fac5a3f4d20e44bafbe6b3cf209831e25a0c4b7f44a3` |
| Repaired `sections/03-restricted-hardness.tex` | `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40` |
| Updated `process/coverage.md` | `98124249aae09b78c542a747d637c93eaedf2f70803646dd58850524432ad9aa` |
| Unchanged `sections/01-foundations.tex` | `be6256a4ad55a371cc280523072277ac682518ab3527cc82f496e78d17ea97bf` |
| Unchanged `sections/02-algebraic-complexity.tex` | `8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67` |
| Unchanged `bibliography.bib` | `aa9efeccf304e14810335df77e351c088e97f9311b6c44635ec51c28917ed64c` |
