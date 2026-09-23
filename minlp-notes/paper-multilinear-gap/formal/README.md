# Standalone Lean verification

This project verifies the mathematical claims in [the accompanying paper](../main.pdf).
It contains 48 proof modules: 41 in `MultilinearGap` and seven shared
finite-law and envelope modules in `CubicGap`. All sources are included;
there are no imports from the parent repository or its other topics.

| Result | Main declarations in namespace `MultilinearGap` |
|---|---|
| No universal constant | [`Results.lean`](Formal/MultilinearGap/Results.lean): `unbounded_gap_ratio`, `no_uniform_positive_multilinear_bound` |
| Exact finite gap and attainment | [`ExactResults.lean`](Formal/MultilinearGap/ExactResults.lean): `polynomial_exact_minimum`, `hullGap_exact`, `exists_hullGap_exact` |
| Explicit shared-law cube upper bound | [`SharpUpper.lean`](Formal/MultilinearGap/SharpUpper.lean): `sharp_cube_gap_bound` |
| Transfer to original terms on nonnegative boxes | [`BoxTransfer.lean`](Formal/MultilinearGap/BoxTransfer.lean): `degree_gap_bound_on_box` |
| Sharp degree and exactly-n dimension growth on all boxes | [`SharpAsymptotics.lean`](Formal/MultilinearGap/SharpAsymptotics.lean): `sharp_positive_growth` |

## Reproduce

Install Elan, Git, and Python 3 and make the Elan binaries available on
`PATH`. From this directory run:

```sh
lake exe cache get
bash scripts/verify.sh
```

`lean-toolchain` pins Lean 4.33.1; `lakefile.toml` pins Mathlib v4.33.1;
`lake-manifest.json` records exact dependency revisions. The first run needs
network access. The script has no dependency on any original-repository
scripts, numerical datasets, proprietary solver, or license.

For only the three original principal endpoints (this omits the completion modules):

```sh
lake build --wfail Formal.MultilinearGap.Results \
  Formal.MultilinearGap.ExactResults Formal.MultilinearGap.SharpAsymptotics
```

The full verification script also runs:

```sh
python3 scripts/check_imports.py
lake env lean Verify.lean
LEAN_NUM_THREADS=1 lake env leanchecker -v Formal
```

## Meaning and trust boundary

`CubicGap.envelopeValues` is the vertical slice of the convex hull of the
original continuous cube graph. `hullGap` is its supremum minus its infimum.
The vertex-law representation, endpoint attainment, and positive denominators
needed by the results are proved. The all-box theorem uses the original
individual monomials, not a redefinition of their gaps after expansion.

`Verify.lean` audits every declaration owned by a bundled module, including
private helpers. It permits only `propext`, `Classical.choice`, and `Quot.sound`
as transitive axioms. This rejects `sorryAx`, custom axioms, and
native-computation axioms. Noncomputable definitions use ordinary classical
real-number mathematics; they do not admit proofs. No external solver result
is a trusted step.

`leanchecker` replays compiled project declarations through the installed
Lean kernel with their imported dependencies as its base. It is an additional
kernel check, not an independently implemented verifier, and it does not
replay all of Mathlib from scratch. The correspondence between the statements
and the formal definitions is documented in [COVERAGE.md](COVERAGE.md).

[VERIFICATION.md](VERIFICATION.md) records the actual local run and its
limits. These checks do not certify novelty or external peer review.
