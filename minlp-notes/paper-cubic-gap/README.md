# Positive cubic relaxation gaps

This is the focused paper package for the universal cubic upper bound,
fixed-mixture optimality, and an analytic lower-bound family. The main bounds
are

\[
1610000/743033 \le R(3) \le 31/12.
\]

Here `R(3)` ranges over all finite nonnegative boxes and positive-gap points
of multilinear polynomials of degree at most three with nonnegative
coefficients. The numerator uses the exact envelopes of the original terms.

- Read the [paper PDF](main.pdf) or [LaTeX source](main.tex).
- Find every mathematical claim in the [Lean coverage guide](formal/COVERAGE.md).
- Run the proofs using the [formal-project instructions](formal/README.md).
- Consult the [verification record](formal/VERIFICATION.md) for checks and their scope.
- Inspect the [delivery fingerprints](verification/SHA256SUMS).

The [completion review](verification/completion-review.md), the verification
record and the delivery fingerprints cover the 2026-09-16 delivery snapshot
(commit `413aaccb`). The manuscript sources were revised afterwards: on
2026-09-18, in commit `aee2afbf` (2026-09-24), which also rebuilt `main.pdf`
and the paper build records, and in any 2026-09-25 audit follow-up edits. The
fingerprints were not refreshed, so `sha256sum --check` reports mismatches for
`main.tex`, `main.pdf`, `formal/Verify.lean`, five build records under
`verification/`, and this README, which was updated with this note;
`formal/Verify.lean` changed on 2026-09-20. No review of the
later revisions is claimed. To check the fingerprinted snapshot, extract it
from a repository clone with
`git archive 413aaccb paper-cubic-gap | tar -x -C <empty directory>`.

The upper bound uses one marginal-preserving law for every term. Its weights
are optimal among the specified three fixed laws for a uniform termwise
guarantee. That does not determine the exact cubic supremum. The analytic
family provides a convergent lower certificate for the actual ratios; a
limit of the actual ratios is not asserted. The package also includes seven
previously verified exact finite examples.

General coefficient removal, equal-marginal classification, and the general
two-level asymptotic family are outside this focused paper. They remain
separate research topics rather than implicit claims of this package.

## Reproduce

With the pinned Lean toolchain and dependencies available:

```sh
cd formal
bash scripts/verify.sh
```

From this paper directory, build and inspect the distribution:

```sh
python3 scripts/build_paper.py
python3 scripts/check_bundle.py
sha256sum --check verification/SHA256SUMS
```

The paper checks use `latexmk`, a TeX installation, `pdfinfo`, `pdftotext`,
and `qpdf`. `scripts/export_proofs.py` is a maintainer tool: given the canonical
`formal/` directory, it exports the dependency closure, or compares it with
`--check`. The exported package can be verified without the parent repository.
