# Sharp gaps for positive multilinear relaxations

Read [main.pdf](main.pdf) for a self-contained proof of the counterexample to
the Luedtke–Namazifar–Linderoth conjecture, the exact counterexample gap,
and the sharp degree and dimension asymptotics. Its source is
[main.tex](main.tex), with a local [bibliography](references.bib).

The [standalone Lean project](formal/README.md) verifies these results and
the explicit finite upper bound used in the note. It also verifies general
envelope attainment and interpretation, exact individual envelopes, all
construction-size claims, the actual family asymptotics, and every printed
example. The
[coverage guide](formal/COVERAGE.md) maps the paper's claims to declarations;
the [verification record](formal/VERIFICATION.md) describes the recorded checks.
The proofs use actual continuous graph-hull widths and exact individual-term
envelopes. They require no optimization solver.

## Read or share

Send this entire folder, or a ZIP of it, keeping its relative paths intact.
The PDF contains local links to the Lean source and verification documents.
Some PDF viewers disable local links; the coverage guide supplies the same
paths and declaration names. The PDF itself contains the full mathematical
argument and can also be read independently.

No files from the parent repository are needed to read the note, compile the
PDF, or verify the bundled proofs. The first Lean setup needs internet access
to obtain the pinned toolchain and dependencies. Dependency downloads and
build caches are not part of the distribution. No public hosting, email
delivery, or journal submission is performed by this package.

## Build the paper

Install a standard pdfLaTeX distribution with latexmk, Latin Modern, AMS
math, mathtools, geometry, microtype, booktabs, natbib, xurl, and hyperref.
Python 3 and Poppler's `pdfinfo` and `pdftotext` support the checked build.
From this folder run:

```sh
python3 scripts/build_paper.py
```

Or compile directly with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The checked build records the final LaTeX log, PDF text, page count, warnings,
and source/PDF fingerprints under `verification/`. It fails on unresolved
references or citations, duplicate labels, and overfull boxes. Underfull
boxes are reported for inspection. The recorded delivery build has 11 pages.

An additional distribution check uses qpdf to inspect the actual PDF links,
checks the Markdown links and exported proof fingerprints, and checks the
printed finite examples and cutoff-mixture boundary cases with rational
arithmetic:

```sh
python3 scripts/check_bundle.py
```

## Verify the proofs

Install Elan, Git, and Python 3; put Elan's binaries on `PATH`. Then run:

```sh
cd formal
lake exe cache get
bash scripts/verify.sh
```

Lean 4.33.1 and Mathlib v4.33.1 are pinned. The script builds all 48 bundled
proof modules, checks import coverage, audits all bundled declarations and
their transitive axiom dependencies, and replays the project declarations
through Lean's installed kernel. See [the formal README](formal/README.md)
for the trust boundary and endpoint commands.

The delivery fingerprints in `verification/SHA256SUMS`, the
[completion review](verification/completion-review.md) and the recorded
checks cover the 2026-09-16 delivery snapshot (commit `413aaccb`). The folder
was revised afterwards: `main.tex` and `main.pdf` on 2026-09-18,
`formal/Verify.lean` on 2026-09-20, the manuscript, PDF and paper build
records in commit `aee2afbf` (2026-09-24), and any 2026-09-25 audit
follow-up edits. The fingerprints were not refreshed. In the current folder,
`sha256sum -c verification/SHA256SUMS` therefore reports mismatches for
`formal/Verify.lean`, `main.tex`, `main.pdf`, four paper build records
under `verification/`, and this README, which was updated with this note; all 48 bundled proof-module entries still match. No
review of the later revisions is claimed. To check the fingerprinted snapshot
itself, from a clone of the original repository:

```sh
mkdir /tmp/multilinear-20260916
git archive 413aaccb paper-multilinear-gap | tar -x -C /tmp/multilinear-20260916
cd /tmp/multilinear-20260916/paper-multilinear-gap
sha256sum -c verification/SHA256SUMS
```

A PDF rebuilt by a recipient may differ in metadata while containing the same
mathematical text. Delivery fingerprints identify one snapshot, not every
future rebuild. Rebuilding the paper also replaces its local build records.

## Scope and provenance

The source conjecture is Conjecture 4.1 on p. 349 of Luedtke, Namazifar, and
Linderoth (2012), or Conjecture 1 on p. 22 of their linked author manuscript.
The note proves a counterexample and matching sharp leading growth. It does
not include optimized fixed-point, Lambert W, second-order,
coefficient-removal, or homogenization results. Formal verification and
internal reviews do not establish publication priority or external peer review.

This is a frozen export of the original project's canonical Lean sources,
with a new focused paper and standalone verification harness. The
[export manifest](formal/verification/export.json) fingerprints each copied
source and dependency configuration. The shared name `CubicGap` is retained
for stable imports; only seven general infrastructure files from that
namespace are included, with no cubic example modules.

Maintainers should edit the canonical proofs and export them again rather
than develop a second copy. The optional maintenance command is:

```sh
python3 scripts/export_proofs.py /path/to/canonical/formal
python3 scripts/export_proofs.py /path/to/canonical/formal --check
```

The external source path is used only by this optional export command, never
by the paper build or proof verification. After an export, rerun verification,
update the coverage and verification records if needed, and regenerate
delivery fingerprints with `python3 scripts/fingerprint.py`.
