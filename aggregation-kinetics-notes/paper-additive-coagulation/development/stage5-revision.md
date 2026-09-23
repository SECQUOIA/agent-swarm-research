# Stage 5 revision record

Date: 2026-09-07. Revision agent: `paper_revision_agent`, separate from the stage author and five independent reviewers.

Both minor corrections accepted in `reviews/stage5-round1/assessment.md` are implemented. No accepted issue remains unresolved. Coordinator verification and Stage 5 acceptance are pending. The full-manuscript review has not started.

## Exact changes

| ID | Location | Change |
|---|---|---|
| S5-A1 | `sections/fourier-identification.tex`, discussion after `thm:fourier-identification` | Replace the claim that strictly smaller daughters are essential to identification. Explain that a hypothetical fraction-one atom contributes nothing directly to the exponent but is recoverable when daughter count and mass are known. Define the visible negative-jump measure, display the bounded-integral formula for selection and the formula for zero-jump mass, and give the resulting daughter recovery for positive selection. Explicitly retain the paper's forward support assumption. |
| S5-A2 | `sections/introduction.tex`, abstract | Add critical balance `sigma=lambda m` to the sentence covering finite-population count accuracy and logarithmic-time mass-distribution discrepancy. |

Updated the corresponding coverage description. Appended dated corrections to `stage5-author.md` and `stage5-coordinator-checks.md`, with coordinator authorization, preserving their historical bodies and explicitly correcting their original necessity claim. The appendices to those records also identify the abstract correction and current review status.

Added the same dated endpoint qualification immediately after the fraction-one paragraph in `research/results/fourier-identification.md` (relative to the repository root). No historical independent review report, assessment, or snapshot was edited.

README, WORKFLOW, and COVERAGE now report completed Stage 5 reviews and minor corrections, with coordinator verification pending. No acceptance is asserted by this revision.

## Proof checks

In the hypothetical enlarged expected-daughter class, set `nu_-=sigma(log)_#(B restricted to (0,1))` and `z=sigma B({1})`. A zero log jump has zero contribution to the exponent, so the existing one-sided uniqueness lemma determines `nu_-`. The two known constraints are

`nu_-(R)+z=2 sigma` and `integral exp(y) nu_-(dy)+z=sigma`.

Subtracting gives `sigma=integral (1-exp(y)) nu_-(dy)`. Its integrand lies between zero and one on the negative half-line, so no logarithmic moments or noisy continuation to a complex argument are used. The count constraint then gives `z=2 sigma-nu_-(R)`. For positive selection, division by `sigma` recovers `B`, including its endpoint atom. The zero-selection exception still leaves an unused daughter law unidentified. This is an algebraic qualification of the claimed necessity, not an extended forward theorem.

The abstract's added condition matches `prop:finite-count` and `thm:finite-discrepancy`; their statements and proofs are unchanged. No estimator constant, numerical calculation, or other theorem was changed.

## Build and artifact checks

- `make -B` completed successfully using the existing recipe. The final `main.pdf` has 55 pages (685,032 bytes). Build transcript: `/tmp/ramki-stage5-revision-build.log`.
- Final `main.log` and `main.blg` have no warnings, errors, unresolved references or citations, or overfull or underfull boxes. Extracted text contains no unresolved-reference placeholders.
- Rendered and visually inspected pages 1, 39, 40, and 55: the abstract, structural-identification theorem, endpoint recovery formulas, and bibliography ending are legible and within the margins.
- The required text changes naturally leave four complete bibliography entries on the last page. The original two-line final-entry orphan is absent. The final bibliography spacing, fonts, and `main.tex` are unchanged.
- Hash comparison with `reviews/stage5-round1/snapshot.json` shows changes only to the two corrected section files, README, and COVERAGE among frozen files. All other mathematical sources, bibliography, Makefile, and numerical code/data/artifacts are unchanged.
- No accepted numerical supplement or test was rerun. No additional agent or reviewer was dispatched.
