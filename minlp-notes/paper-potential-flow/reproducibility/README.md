# Passive potential-flow optimization: standalone Paper A

The archive contains the complete anonymous manuscript, its PDF, selected original code and rational data, exact certificate verifiers, and reproduction scripts. The 28-page main narrative is followed by references and all complete technical proofs. The appendices are included in the same PDF and require no research notes or companion paper.

Commands below run from the archive's top-level `potential-flow-paper-a/` directory. In the repository, run them from its root instead. Every path used by the scripts is relative to its own location; no parent repository or local account path is required.

## Build the complete manuscript

Required: Python 3, latexmk, pdfLaTeX, BibTeX, and TeX Live with AMS mathematics, natbib, booktabs, tabularx, TikZ/PGF, microtype, hyperref, cleveref, and T1 Computer Modern fonts. Tested with TeX Live 2023/Debian, pdfTeX 1.40.25, latexmk 4.83, and BibTeX 0.99d. The source uses no external images or shell escape.

```sh
python paper-potential-flow/reproducibility/build_paper.py
```

The output is `paper-potential-flow/complexity/build/main.pdf`. The command builds only Paper A, saves `build/build-check.json`, and fails on errors, undefined references or citations, duplicate labels, or any overfull box. Do not use the legacy two-paper CLI in `verification/build_and_check.py`; the A-only wrapper imports its `build('complexity')` function.

## Recheck rational witnesses without scientific packages

Python 3.12.14 was used for the retained replays. Only the standard library is required for this command:

```sh
python -S paper-potential-flow/reproducibility/reproduce.py --output exact-replay.json
```

This reruns exact certificate, rejection, support, curvature, directional-coefficient, and saved-profile checks. Important verifier paths are exercised both normally and with `-S -O`, so their mathematical checks do not depend on assertions or installed scientific packages. All code and data are copied to a temporary directory before execution, preserving distributed records. The report records every relative command, return code, and full output. Files with `review` in their names are executable diagnostic programs, not research-agent review reports.

A minimal original-instance check is:

```sh
python -S -O code/potential_flow_mpd/certified_envelope.py verify code/potential_flow_mpd/certified_envelope_example.json
```

A deterministic energy certificate proves the instance in its own file. The integrated `certified_envelope.py` verifier additionally checks the original uncertainty instance, envelope mapping, target orientation, and recovered scenario. Rational input scenarios can have irrational physical states; a verified zero scenario loss need not give a rational exact flow value.

## Optional scientific diagnostics and numerical proposals

Use a separate Python 3.12 environment. The tested versions are pinned in `paper-potential-flow/reproducibility/requirements-numerical.txt`:

```sh
python -m pip install -r paper-potential-flow/reproducibility/requirements-numerical.txt
python paper-potential-flow/reproducibility/reproduce.py --numerical --output numerical-replay.json
```

This adds the earlier mathematical regression diagnostics, the ten-case original-instance benchmark, and producer/scaling checks. It also repeats the exact suite. The runner uses isolated copies because numerical benchmark producers rewrite adjacent example and result JSON files. Numerical outputs can vary with platform and solver; inspect their freshly verified rational bounds. `optimal_inaccurate` is a proposal status and never substitutes for verification. The producer accepts no requested accuracy guarantee; extreme coefficient ratios can widen certificates or cause a numerical failure.

The code does not implement every theoretical algorithm. In particular, the fixed-dimensional quantifier-elimination algorithms and the general many-block nomination compilers are proofs of algorithms, not implemented software. `exact_weighted_cactus.py` requires supplied independent blocks and fixed nominations; it does not perform graph decomposition. Its exact profile and separately represented block values do not constitute an exact global scalar comparator. Some earlier diagnostics use Decimal, grids, finite differences, or numerical roots; they provide finite regression evidence, not universal proofs.

## Data and evidence

`manifest.json` records every distributed file's SHA-256 except itself. `evidence/` contains the final clean source-build record and portable exact/numerical replay records. Saved rational examples and the earlier ten-case benchmark data are under `code/potential_flow_mpd/`. The mathematical proofs establish universal results; exact replay establishes the particular saved witness claims.

The water-topology instance reuses only topology and pipe geometry from Vrachimis, Eliades, and Polycarpou, *Real-time hydraulic interval state estimation for water transport networks: a case study*, Drinking Water Engineering and Science 11 (2018), 19–24, DOI [10.5194/dwes-11-19-2018](https://doi.org/10.5194/dwes-11-19-2018), and its [Zenodo dataset](https://doi.org/10.5281/zenodo.1185136). The [original INP header](https://zenodo.org/records/1185136/files/Vrachimis2018NetDWES.inp) names Copyright 2018 KIOS Research and Innovation Center of Excellence, University of Cyprus, and states “Licensed under the EUPL.” This notice concerns the source dataset. The included instance uses synthetic quadratic proxy laws, nominations, and resistance intervals. It does not reproduce source measurements or leakage results. Original INP data and copyrighted literature PDFs are not distributed.

## Regenerate the deliverables

After changing source, rebuild and rerun relevant checks. To refresh retained replay evidence before packaging, direct the two replay commands to `paper-potential-flow/reproducibility/exact-replay.json` and `paper-potential-flow/reproducibility/numerical-replay.json`. Then run:

```sh
python paper-potential-flow/reproducibility/package.py
```

It checks that the manuscript hashes match the most recent clean build, then creates `paper-potential-flow/dist/potential-flow-paper-a.tar.gz`, `paper-a.pdf`, and `package-manifest.json`. The same command works after extraction. It includes only Paper A, selected code/data, and portable evidence; it excludes the parent repository, other manuscript, managed literature, internal review reports, and temporary build files.
