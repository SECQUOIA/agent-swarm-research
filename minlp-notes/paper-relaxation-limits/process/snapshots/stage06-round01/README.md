# Convex relaxation gaps and spatial certificates

The integrated manuscript is [main.pdf](main.pdf), with source [main.tex](main.tex). It treats simultaneous envelope gaps, structural and physical-box laws, and spatial certificates under specified node oracles. Supporting appendices distinguish scaling and coordinate effects, global conic lift size, integer precision and primitive FBBT.

**Status:** Stages 1–5 accepted; Stage 6 author-complete, with its fifteen full-stage reviews and the separate whole-paper loop pending. See [PROCESS.md](PROCESS.md). A compiled draft is not final review acceptance.

## Build

From the repository root:

```sh
python paper-relaxation-limits/verification/build_and_check.py
```

Or, from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The build script writes `main.pdf`, `verification/manuscript.txt`, `verification/build-output.txt` and `verification/build-report.json`. It checks duplicate/unresolved labels and citations, records layout warnings and SHA-256 input digests, and confirms that the printed Stage 2 executable matches its source. Inspect the warning list as well as the exit status: an overfull box is recorded but does not itself make the script exit nonzero. The integrated author build has no warnings.

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

The general proofs, finite exact checks, numerical experiments, source inspections and internal reviews are different forms of evidence. None is presented as proof-assistant certification, exhaustive priority clearance or external peer review.
