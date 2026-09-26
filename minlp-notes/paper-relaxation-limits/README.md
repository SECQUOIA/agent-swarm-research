# Convex relaxation gaps and spatial certificates

The integrated manuscript is [main.pdf](main.pdf), with source [main.tex](main.tex). It treats simultaneous envelope gaps, structural and physical-box laws, and spatial certificates under specified node oracles. Supporting appendices distinguish scaling and coordinate effects, global conic lift size, integer precision and primitive FBBT.

**Authoring status: complete.** All six authoring stages and the separate whole-paper review were accepted: **135 reports across nine rounds**. The final fifteen reports were all PASS with no requested manuscript repairs. The recorded final clean build had 111 pages. See [FINAL-REPORT.md](FINAL-REPORT.md) for the results and process, and [PROCESS.md](PROCESS.md) for stage accounting.

Those reports describe the reviewed authoring snapshot of 2026-09-07. The
manuscript sources were revised afterwards: by the source corrections of the
[September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md),
by the topic 19 coverage updates below (2026-09-20), in commit `aee2afbf`
(2026-09-24), and in any 2026-09-25 audit follow-up edits. The current PDF
was last rebuilt in commit `aee2afbf`. The authoring reviews do not cover
these later revisions; earlier build and review records retain their
original scope.

## Lean coverage

Separate packages verify the following mathematical results in this larger manuscript:

- [Multilinear completion](../formal/topics/10-multilinear-completion/COVERAGE.md): envelope foundations, exact dyadic gap and attainment, construction counts and sparsity, actual-family asymptotics, and sharp leading degree/dimension growth on nonnegative boxes.
- [Cubic completion](../formal/topics/11-cubic-completion/COVERAGE.md): the universal `31/12` upper bound, optimality of the fixed `18:6:7` mixture for uniform termwise guarantees, and the analytic lower family, together with the earlier exact finite witnesses.
- [Marginal-floor package](../formal/topics/12-marginal-floor/COVERAGE.md): finite upper bound, both sharp leading limits, and original-box transfer. The floor concerns normalized evaluation means, not physical lower endpoints.
- [Positive-box package](../formal/topics/18-positive-box/COVERAGE.md): `max{2,rho} ≤ C_box(rho) ≤ rho+2` for `rho>1`, the finite-dimensional `rho+beta_N` bound, and original-box transfer and lower constructions. It does not determine the exact supremum at a fixed aspect ratio.
- [Structural gaps, topic 19](../formal/topics/19-structural-multilinear/COVERAGE.md): the feedback-variable bound on nonnegative boxes; sharp frequency-two and odd-girth bounds and bipartite exactness; convex-cardinality and common-aspect box extensions; and the sharp incidence-treewidth-two bound. The proofs discharge the original graph hypotheses, construct the required laws and verify the sharpness families. The unequal-aspect `7/6` obstruction is included. General-feedback positive-monomial sharpness and a general-positive-box frequency-two `3/2` bound remain unresolved. Matching-based algorithms and bit complexity are outside this scope; see the [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md) for completed checks and source snapshots.
- [Primitive FBBT](../formal/topics/02-fbbt/COVERAGE.md): the circuit's doubly exponential update lower bound and fair-limit theorem; the separate PosSLP reduction and serialized input-size estimate are outside the package.

Each package's verification record identifies its checked source snapshot.
In particular, [topic 18's record](../formal/topics/18-positive-box/VERIFICATION.md)
distinguishes the completed checks from later odd-dimensional declarations.
These packages do not certify the whole manuscript. The verified multilinear
finite upper certificate uses a rational harmonic estimate; the constant 24,
optimized fixed-point and Lambert W certificates, second-order expansion,
and homogenization in the broader manuscript are outside that coverage.
The spatial-certificate chapters are also outside these packages. The focused
[multilinear](../paper-multilinear-gap/README.md) and
[cubic](../paper-cubic-gap/README.md) standalone bundles have their own scopes
and do not include the later marginal-floor or positive-box packages.

## Build

From the repository root:

```sh
python paper-relaxation-limits/verification/build_and_check.py
```

Or, from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For the topic 19 documentation update, this targeted `latexmk` command passed
and produced a 113-page PDF. Its final pass had no unresolved references or
citations, duplicate labels, or overfull boxes. Three underfull boxes remain:
two in the introductory navigation table and one in the structural auxiliary
appendix. This is a manuscript build check, not the final Lean proof audit.

The build script writes `main.pdf`, `verification/manuscript.txt`, `verification/build-output.txt` and `verification/build-report.json`. It checks duplicate/unresolved labels and citations, records layout warnings and SHA-256 input digests, and confirms that the printed Stage 2 executable matches its source. Inspect the warning list as well as the exit status: an overfull box is recorded but does not itself make the script exit nonzero. The recorded final clean build had no tracked warnings, unresolved references/citations, duplicate labels or overfull boxes. Three underfull bibliography lines were harmless in the inspected output. [final-build-validation.json](verification/final-build-validation.json) records that the then-current manuscript inputs and extracted PDF text matched the reviewed version; the PDF bytes differed only in build dates and trailer ID. It does not validate subsequent source edits.

Required TeX components are a standard pdfLaTeX installation with latexmk, Latin Modern, AMS math, geometry, microtype, booktabs, natbib and hyperref; Poppler supplies `pdfinfo`, `pdftotext` and optional `pdftoppm` renders. [verification/environment.json](verification/environment.json) records the actual environment: Python3.12.14, SymPy1.14.0, NumPy2.5.2, SciPy1.18.1, NetworkX3.6.1, latexmk4.83, TeX Live2023 and Poppler24.02.0. The conda path below is the local environment used, not a portable installation requirement.

## Replay mathematical checks

The narrow integration check uses SymPy and exact rational arithmetic. It independently enumerates the eliminated scaling polytope at three parameter sets, checks rational rotation and signed-slack identities, verifies every ledger label, and compares all 21 accepted mathematical/macro files with the Stage 5 snapshot:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_stage06_integration.py
```

The following paper-local checks exercise distinct core arguments; run from the repository root. The finite cubic checker uses only the standard library. The remaining commands can all use the recorded conda environment (or another Python installation with their imports installed).

```sh
python paper-relaxation-limits/verification/check_stage02_finite.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_stage02_symbolic.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_cardinality_refinement.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_radix_cutoffs.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_unequal_box_bipartite.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_stage04_author.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_univariate_lift_refinement.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_spatial_tolerance_and_tree.py
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/check_stage05_author.py
```

The earlier selected repository replay is available as:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-relaxation-limits/verification/run_repository_checks.py bilinear global structural spatial
```

The runner saves commands, script hashes, exit status and output in `verification/repository-checks/`. Existing successful replay is historical evidence; the integration author did not rerun unchanged stages. Some broader repository experiments require solvers or licenses; those are not needed to compile the paper or run the integration checker. A solver installation alone does not imply a working license. The source-level proofs and exact finite certificates remain readable without those experiments.

## Navigation and provenance

- [process/claim-coverage.md](process/claim-coverage.md): exhaustive source-to-final-label coverage, bounded developments, inherited inputs and exclusions.
- [process/stage-06-author.md](process/stage-06-author.md): integration changes, fresh source checks, validation and access/version limits.
- `sections/01-foundations.tex` through `15-finite-certificates-affine.tex`: accepted core mathematics; the first five appendices preserve distinct proofs and executable certificates.
- `sections/16-supporting-comparisons.tex`, `17-synthesis.tex` and the six supporting appendices: integrated comparison and open questions.
- `references.bib`: paper-local primary bibliography; author-version locators are identified explicitly where they differ from published numbering.
- `process/snapshots/`, complete reviews and adjudications: preserved staged evidence. Source PDFs in the literature collection are read-only and are not redistributed here.

The general proofs, finite exact checks, numerical experiments, source inspections,
internal reviews, and scoped Lean proofs are different forms of evidence.
Only the statements identified in the Lean coverage maps are presented as
proof-assistant results. None of these records establishes exhaustive priority
clearance or external peer review.
