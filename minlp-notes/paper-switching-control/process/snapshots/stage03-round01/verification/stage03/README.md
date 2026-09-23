# Stage 3 verification

Run from the manuscript root or any relocated copy containing this directory:

```sh
python verification/stage03/run_checks.py
```

Python 3 and its standard library suffice. Do not use `-O`: the checkers use
assertions. The runner checks SHA-256 hashes against the origin manifest and
writes one log for each script. All imports and data reads use bundled files;
no checker reads the surrounding research repository.

`check_new_results.py` checks the mode-removal branches, elementary and seeded
coefficients, formal power-series coefficients, plateau arithmetic, predecessor
identities, all-light boundaries, and rational schedules. These finite checks
support the analytic proofs over measurable controls; they do not prove those
universal statements by sampling.

`check_chronological.py` verifies the original relaxation witness, then proves
the exact optimum of one strengthened event chamber. It reconstructs all rows
from `reference/general_reach_research.py` and appends the 378 adjacent
coordinate-monotonicity rows. The chamber permutation is computed from the
original witness and checked against the saved certificate. It verifies rational
dual signs, the nonnegative dual residual, the exact dual bound, all primal
rows, and the matching explicit uniform-control primal. The certificate is
`chronological_chamber_certificate.json`. This is a proof dependency only for
the single-chamber proposition. It proves neither the general weighted
three-block inequality nor the five-block reach theorem.

The unchanged original scripts and witness are in `verification/reference`,
with their source paths and hashes in `origin-manifest.json`. In particular,
`general_reach_research.py` and `check_seeded_review.py` retain historical clipped
formulas alongside the final unclipped refinement; the manuscript uses the
unclipped coefficient. Their interface defaults are preserved to keep the
original files byte-for-byte intact.

Optional discovery can be rerun with SciPy and NumPy installed:

```sh
python verification/stage03/discover_chronological.py
python verification/stage03/check_chronological.py
```

The first command overwrites the chamber certificate with a newly rationalized
dual candidate. A numerical solver may return another optimum or a candidate
that fails rationalization; the second command is required before trusting
that candidate. The bundled certificate already passes the exact checker.
The recorded discovery used SciPy 1.18.0 (HiGHS). The full verification runner
does not import SciPy or execute discovery.

`build.log` records the initial successful LaTeX build, including first-pass
references resolved on the final pass. `final-build.log` records the final
build. `manuscript.txt`, page images 21–32, and three contact sheets record the
reviewed layout of the stage 3 material.
