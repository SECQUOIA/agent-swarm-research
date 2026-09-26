# Checkable lower bounds for convex MINLP

This directory contains the complete anonymous review manuscript, **Checkable
Lower Bounds for Convex Mixed-Integer Nonlinear Optimization through Rational
Outer Approximations**, and its source/reproduction materials. Read `main.pdf`.
No public repository upload or DOI is claimed. The paper's mathematical proofs
are self-contained; repository research notes are not needed to read or build it.
The current `main.pdf` was last rebuilt in commit `aee2afbf` (2026-09-24),
which revised the manuscript sources, including Section 6. An earlier rebuild
added the clarified formal-coverage wording for the
[September 20 documentation follow-up](../notes/lean-verification-documentation-followup.md).
The dated review records in `process/` (stages 1–6 and the R1–R3 clarity
revision, 2026-09-13 to 2026-09-14) cover earlier manuscript versions; no
review of the later revisions, including `aee2afbf` and any 2026-09-25 audit
follow-up edits, is claimed. The source
archive, `PAPER-SHA256SUMS` and `paper-source-archive.json` were produced on
2026-09-18 (commit `2071ed80`) and were not refreshed, so they do not contain
the current sources. The formal fingerprints retain the scope stated below.

## Reading the empirical evidence

Section 6 is organized around three scientific questions: which checkable bounds
the uniform protocol produces and how strong they are; what exact audits establish
about failures; and what storage, replay, and memory limits constrain use.
Appendix A gives the portable reproduction commands. Appendix B retains the full
frozen protocols, production/phase accounting, historical checking costs, and
separate V1/V2/V3 repair cohorts. Reference comparisons remain distinct from
primal certificates, and the merged catalogue remains distinct from uniform-run
coverage. The numerical records, generated tables, checker sources, and
experimental archives are unchanged by this presentation revision. The later
formal extension is documented below and in Section 5.

## Build the paper

Install a TeX distribution with pdfLaTeX, BibTeX, latexmk and the packages in
`main.tex` (including TikZ). From a freshly extracted source archive:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Within a working directory that may contain earlier auxiliary files, use:

```bash
bash scripts/build-paper.sh
```

The script always compiles a fresh temporary copy of the current sources and
writes `main.pdf`, `main.bbl` and `build/current-*.log`. The source archive
`certified-minlp-paper-source.tar.gz` includes all sections, generated tables,
bibliography, the TikZ diagram source, and the focused Lean sources. It excludes
old auxiliaries, duplicate build trees, installed dependencies, and experiments'
large proof archives. `PAPER-SHA256SUMS` identifies the included source bytes;
`paper-source-archive.json` identifies the compressed archive.

## Three separate artifacts

| Artifact | Contents | Size/scope |
|---|---|---|
| `certified-minlp-paper-source.tar.gz` | Complete LaTeX sources, selected bibliography, generated table/data files, current evidence maps, formal proofs and pins | Compact source package; no experiment archive needed to build |
| `supplement/certified-minlp-core.tar.gz` | Current checker, all 289 campaign models, compact frozen records, source/primal and failed-step audits, source snapshots, tests, representative complete bundles | 6,478,681 bytes compressed |
| `supplement/certified-minlp-certificates.tar.gz` | Historical/new completed proofs, including rejected and fallback attempts | 30,664,561,063 bytes compressed; approximately 93.7 GB of regular-file contents |

The core/bulk SHA-256 values and exact sizes are in `supplement/archives.json`.
Those two archives are delivered separately from the paper-source archive. Their
portable entry point is `minlp-certified-evidence/README.md` after core extraction.
The outer `supplement/README.md` is also included with the paper source.

Start with the core: it supports manifest verification, four complete example
replays, exact original-model audits, fifteen failed-step audits, and regeneration
of thirteen saved-record tables/catalogue outputs without licensed solvers.
Python 3.13 plus the five pinned checker dependencies are sufficient. The
current 161-test suite separately requires pytest. The bulk is only needed for
full proof replay or archive readback. Its complete 5,207-entry readback was
already validated; small reproduction does not need to repeat that large read.

Recorded historical outcomes are 188 verified / 92 rejected / 9 missing; frozen
primary V1 replay is 203 / 19 / 67. V2's twelve regenerated cases all verify;
V3's two targeted `tls12` replays verify previously unreportable exact bounds.
The default checker is V3. Its expected full replay of primary fixed artifacts
is 204 / 18 / 67, which is not represented as another completed primary campaign.
The core documents restoration of the exact V1/V2/V3 source versions and shared
test/example data. The descriptive catalogue covers 222 identical-model entries
selected from 405 accepted records; it is not a uniform-run success rate.

Numerical generation additionally needs Gurobi, IPOPT, exact SCIP and VIPR tools;
portable commands and pinned provenance are in the core README. Libraries and
solver binaries are not bundled. MINLPLib models retain their attribution;
user-supplied literature PDFs are not distributed.

## Focused formal verification

The Lean development now covers 49 mathematical obligations across 27 modules,
including executable structured-proof and rational PSD checkers. See
[coverage](formal/COVERAGE.md) and [current checks](formal/VERIFICATION.md).
The existing Python pipeline and benchmark artifacts are not formally verified.

During local repository work, run targeted checks only. Project-wide
verification is assigned to CI; do not run it locally or inspect CI. The
committed workflow, `.github/workflows/lean.yml`, builds only the canonical
`formal/` project, so CI verification of this standalone project is assigned
but not configured. For full standalone reproduction, install Elan, Git and
Python 3, then run from `formal/`:

```bash
sha256sum -c verification/extension-SHA256SUMS-2026-09-25
lake exe cache get
bash scripts/verify.sh
```

The fingerprint manifest `extension-SHA256SUMS-2026-09-25` records the
current sources; both audit programs passed on them on 2026-09-25. The
historical manifest `verification/extension-SHA256SUMS` records commit
`875a71ab` (2026-09-17). Commit `fa2a6f42` (2026-09-20) later wrapped
log-message lines in `Verify.lean` and `verification/ExtensionAudit.lean`,
so on current sources that manifest reports mismatches for those two files;
see [formal/README.md](formal/README.md).

The exact Lean 4.33.1 and mathlib 4.33.1 dependencies are pinned. The accepted
proof sources, import audit, transitive axiom audit, and kernel-replay scripts
are preserved. `formal/COVERAGE.md` lists theorem assumptions and exclusions.
This does not formally verify Python, numerical interval computations, the VIPR
executable kernel, or benchmark artifacts. Dependency download/build caches are
excluded from the source archive.

## Source packaging and review records

`python3 scripts/package-source.py` creates a deterministic source archive and
its manifests from the explicit source inventory. It neither reads nor rebuilds
the core/bulk archives. Dated development/review logs remain in `process/` in the
working repository; current maps in `evidence/` summarize the claim-to-source
and literature relationships. The archive includes the two current maps and
formal validation records, rather than duplicating the internal review history.
