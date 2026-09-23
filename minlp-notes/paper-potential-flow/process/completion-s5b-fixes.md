# Stage 5b minor correction report

All three corrections accepted in `completion-s5b-adjudication.md` are applied. The correction agent read that adjudication, the current Section 9, the build helper, the verifier's parsing and checking code, and the supplied extract of the original Groß et al. PDF, pages 7–8. No applicable on-disk `AGENTS.md` was present in this worktree or its ancestor chain; the supplied global instructions governed the work.

Before editing, all 16 Paper A source hashes matched the frozen `completion-s5b-build.json`. The initial Section 9 SHA-256 was `51b97d72b27619fa890ec977d9c9166beb5ee0c933edb3f29fa5df348e950f13`.

## Repairs and justification

1. **Short rational radius and center.** The correlated strict-margin witness argument now handles zero nominations first: every physical flow is zero, and rational LP returns a polynomial-bit profile in the nonempty rational polytope with the same arc bounds. For nonzero nominations, it chooses `delta = 2^(-k)` with the least nonnegative integer `k` satisfying `delta <= min{1, beta_L gamma/(4mM)}`, and chooses the center on the grid with spacing `delta/4`. Minimality bounds `k` by the input length and the positive part of `log(1/gamma)`. The coefficient bounds control the integer parts of the center coordinates; the grid controls their denominators. Thus the center and box inequalities have polynomial encoding length. The box contains the original profile, so its intersection with the bounded rational polytope is nonempty, including when affine equalities are present. Determinant bounds give a short rational vertex. Every such vertex is within `3 delta/4` of the original profile and preserves at least half the original arc slack under the existing elementary sensitivity estimate. This specifies the proof's approximation data without changing a sensitivity constant or theorem statement.
2. **Verifier encoding.** The implementation paragraph now states that polynomial verification counts expanded rational numerator and denominator bit lengths. Additional exact-string forms accepted by `Fraction`, including exponent notation, are assessed after expansion, not by raw JSON length. This matches the existing mathematical rational bit model: for example, an exponent string representing `10^(10^n)` can have a token length proportional to `n` while its expanded numerator has exponentially many bits. The qualification makes no claim of polynomial verification in that compressed length. Parser behavior and all code remain unchanged. Final reproducibility instructions should preserve this distinction.
3. **Classical homogeneous dual citation.** The existing Groß et al. attribution now names Lemma 3.4 and equation (8), alongside the existing equation (7) locator, and explicitly calls both the energy principle and its homogeneous dual classical. In the inspected primary-source formula, setting homogeneity exponent `r=2` and scale `alpha=1` gives the manuscript's conjugate `2 |d|^(3/2)/(3 sqrt(beta))`. The normalized potential gauge does not change the dual objective for balanced nominations. No bibliography entry or duality claim was added.

## Files and validation

Authored files are limited to:

- `complexity/sections/09-correlations-energy.tex`: the three repairs above.
- `process/completion-s5b-build.json`: the refreshed Paper A build result and all 16 source hashes.
- `process/completion-s5b-fixes.md`: this report.

The correction agent imported `verification/build_and_check.py` and called only `build('complexity')`. Its CLI was not invoked. The helper ran `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` in `complexity`. The build returned zero, produced the PDF, and reported zero errors, undefined references, undefined citations, duplicate labels, and overfull boxes. The overfull-box count was checked explicitly in addition to the helper's `passed` field.

All 16 refreshed source hashes were verified after the build. Only Section 9 differs from the initial source freeze; the other 15 source hashes remain identical, including the accepted sections, main file, macros, and bibliography.

`completion-s5b-checks.json` is byte-identical to its initial version and still records 13 passing diagnostics. Before and after the repairs, every recorded diagnostic script hash, all 73 dependency hashes, and the certificate hash matched the current files. The verifier and parser were therefore unchanged. No diagnostic code was altered or broad diagnostic suite rerun for these prose and encoding clarifications; the recorded finite diagnostics remain supporting checks, not proofs of universal assertions.

Final SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `complexity/sections/09-correlations-energy.tex` | `09945e86ae4c62933ff65d238260ab07716b8265af0ff640a6aa0e65a926db88` |
| `process/completion-s5b-build.json` | `4b7963e18e24574259fba0209871fd4825adf27d370f9bf33c8b4c44bf8a735c` |
| `process/completion-s5b-checks.json` (retained) | `071806d92dc6e70e4a79149667e89653ac6fe79031afe78995917fdf8e07d4b9` |

## Scope and remaining limits

No theorem, conclusion, sensitivity bound, accepted earlier section, bibliography entry, main file, parser, or other code was changed. Paper B was neither edited nor built. No managed-literature file was edited and no commit was made.

The witness argument remains conditional on existence of a strictly feasible real profile. It does not locate that profile or its center; LP recovers a witness when an adequately accurate center is supplied. The verifier's polynomial claim uses expanded rational encodings. The precise citation identifies an existing classical dual, not a new duality principle. No major issue emerged from the corrections or their validation. Section 9 and its build manifest are frozen for the lead's final inspection; final acceptance, coverage, and planning remain with the lead.
