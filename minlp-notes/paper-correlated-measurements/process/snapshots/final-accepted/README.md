# Globally certified measurement selection with correlated errors

This folder contains a complete standalone research manuscript, its LaTeX
sources, and a portable computational supplement. The manuscript presents
explicit relative locality bounds, approximation guarantees, rational global
certificates, virtual-noise relaxation comparisons, a nested latent-anchor
hierarchy, and computational studies with their limitations. The author block
is anonymous; no author identities, affiliations, funding or publication
metadata have been invented.

## Read and build

The compiled manuscript is [build/main.pdf](build/main.pdf). Build from this
folder with a LaTeX distribution containing pdfLaTeX, BibTeX and latexmk:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

To force regeneration of all LaTeX and bibliography outputs:

```sh
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The source manuscript consists of `main.tex`, `macros.tex`, `references.bib`,
`sections/`, and `appendices/`. Copy these together to build it independently
of the repository; no literature files, original code, or generated scientific
results are needed for the PDF. The manuscript uses the standard article class
and no journal-specific template.

## Validate the computational evidence

From [supplement/](supplement/), after installing `uv`:

```sh
uv sync --frozen
uv run --frozen python validate.py
```

The supplement can be copied outside this repository. After dependencies are
installed, full validation needs no network, commercial solver, original
repository, or literature collection. It checks file integrity, proof fixtures,
all 2,347 public-source schedules by independent exact covariance inversion,
kinetic sensitivities, the fresh nested-anchor and complete-block experiments,
and all 46 principal saved certificates. Validation writes its own results and
logs without replacing the frozen scientific inputs. `--quick` omits expensive
checks and is not the full validation.

[supplement/README.md](supplement/README.md) provides a table-to-artifact map,
dependency versions, exact replay commands, and separate commands for numerical
proposal reproduction. Optional historical mixed-integer comparisons require
Gurobi and an appropriate license. Replaying a certificate does not reproduce
an optimizer's stopping time; reported historical times retain their original
single-run provenance.

## Scope and source provenance

The manuscript distinguishes the public source kinetics dataset with independent
time blocks from the stipulated temporal-covariance kinetic experiments and the
abstract approximation theorems. Exact arithmetic certifies the stated rational
inputs. Independent sensitivity checks do not constitute validated ODE bounds,
physical covariance validation, or global nonlinear identifiability. The
large-polynomial spectral-set algorithms are theoretical; the practical studies
use support pricing and independently checked witnesses.

The public sensitivity data retain their pinned source revision, original file
path and SHA-256 hash in `supplement/source_kinetics/README.md`. No third-party
literature originals or authors' stored pickled selections are redistributed.
No new license is asserted for third-party data.

## Development record

[process/coverage.md](process/coverage.md) maps the repository's substantive
measurement-design developments to actual manuscript labels, supporting
artifacts, superseding results, and explicit exclusions.
[process/literature.md](process/literature.md) records inspected primary sources,
version/access limits, and contribution boundaries. `PROCESS.md` and the
numbered author, reviewer and correction reports document the sequential
five-reviewer gates and final manuscript review. These records are internal
development evidence, not external peer review or scientific citations.

`process/` and `verification/` are development records and are not needed to
build or validate the standalone deliverables. A manuscript source submission
needs the source files listed above; its computational attachment is the whole
`supplement/` directory, excluding disposable environments, caches, and rerun
logs. The frozen input and source manifests belong with that attachment.
