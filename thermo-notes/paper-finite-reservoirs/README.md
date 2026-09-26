# Finite reservoirs at phase coexistence

[Read the manuscript PDF](main.pdf) or [LaTeX source](main.tex).

This folder is the standalone manuscript and numerical reproduction bundle. It supersedes the reservoir notes linked in [COVERAGE.md](COVERAGE.md). The paper studies full-state canonical accuracy under an exact physical power-law bath, microscopic realizations, shared-bath correlations, boundary calibration, and related exact Gaussian and capillarity models.

The manuscript was developed in sequential stages with five independent internal reviewers after each author stage. [WORKFLOW.md](WORKFLOW.md) records the process and its current status. These are internal mathematical and scientific reviews, not external peer review or a guarantee of publication priority. Authorship and affiliations have intentionally not been assigned. Nothing in this folder has been submitted or sent externally.

The manuscript is complete: 49 pages, 31 references, two figures, and all proofs included. All five author stages and two whole-paper review rounds are closed, with every accepted major and minor issue corrected. The review folder preserves 40 independent reports and the corresponding adjudication and correction records. A subsequent referee-style revision (recorded at the end of WORKFLOW.md) restructured the presentation, closed several minor proof gaps, and added citations; no theorem statement changed except for tightened hypotheses noted there.

## Build the paper

Run from this folder:

    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

A standard TeX Live installation with latexmk, BibTeX, Latin Modern, the plainurl bibliography style (urlbst), and the packages named in main.tex is sufficient. The included figure PDFs and bibliography source make the LaTeX build independent of Python, network access, and the local literature folder.

The main text contains the physical reservoir framework, sharp criteria, microscopic statements and mean-field calculation, shared-bath statistics, boundary optimization with the exact secant interior gain, numerical illustrations, and discussion. Appendix A is the full positive-contour proof; Appendix B the exact Gaussian geometry; Appendix C the capillarity model and accuracy diagnostics; Appendix D the shared-bath extensions to fixed phase counts and linear capacity. Every theorem proof is included.

## Python setup

Python 3.10 or newer is recommended:

    python -m venv .venv
    . .venv/bin/activate
    python -m pip install -r requirements.txt

The bundle was checked with Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, and Matplotlib 3.11.1. requirements.txt states minimum compatible package versions rather than an exact environment lock.

## Quick verification and figure regeneration

Run from this folder:

    python code/check_potts_finite_bath.py
    python code/check_stage4.py
    python code/make_figures.py
    python code/potts_phase_statistics.py

The first script independently enumerates all labeled spins for N=1 through 8, checks the Voronoi phase probabilities and conditional variances using distances to the four minima, and uses direct absolute-density quadrature at N=12 to check the Gamma/Beta CDF calculation. It writes data/potts-independent-check-results.json. The second checks the weighted-normal TV formula and optimizer, physical phase-population compensation, and the square-torus inequality. The third regenerates both PDF/PNG figures and their derived values; it uses the archived exact Potts data and proved limiting formulas.

The fourth script reproduces the pure-spin phase statistics quoted in Section 7 at N=3000 and N=12000, along with their limiting constants and the saddle rate excess. It writes data/potts-phase-statistics.json. Voronoi distance is Euclidean in the three occupation fractions, with ordered–disordered ties assigned to the combined ordered phase: max(n_j) >= N/2. Ties among ordered cells do not affect these combined statistics. The calculation sums occupation orbits one row at a time, without aggregating equal energies, because the Voronoi label depends on occupations. It does not evaluate the spin–momentum reservoir CDFs used for the figures.

These deterministic checks use ordinary floating-point arithmetic. They provide numerical verification, not rigorous interval enclosures.

## Exact Potts data and full reproduction

The main finite-system model has J=1, beta=4 log(2), and kinetic Gamma shape N/2. code/potts_finite_bath.py enumerates occupation triples modulo color permutations, aggregates equal energies, integrates kinetic energies analytically, and locates the two scalar crossings of the normalized likelihood. It reports full spin–momentum TV separately from spin-configuration marginal TV.

The figure's archived data are data/potts-finite-bath-results.json: 18 size/regime points at N=300, 1000, 3000, 6000, and 12000. The final size has only the two boundary regimes. The file is copied unchanged from the repository's earlier independently checked calculation at research/verification/potts-finite-bath-results.json. Its SHA-256 is:

    93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1

data/potts-original-independent-check-results.json preserves the earlier independent checks. The source algorithm is copied from research/verification/potts_finite_bath.py; the standalone copy adapts the command-line/output layer and adds an underflow guard that reports (as the extra key log_upper_bound_underflowed_posterior_mass) any posterior mass lost to floating-point underflow, raising an error if it is not negligible. The archived JSON predates that key.

A modest recomputation is:

    python code/potts_finite_bath.py --sizes 300

This evaluates all four regimes and writes data/potts-recomputed.json. It was rerun during manuscript preparation; all four full-TV values agree with the archived values to within 1e-11.

To regenerate the entire archived size/regime plan:

    python code/potts_finite_bath.py --all-archived --output data/potts-recomputed-full.json

This can require substantial time and memory because the occupation count grows quadratically. The N=12000 calculation was not rerun merely to regenerate the figures. The archived calculation, exact derivation, and independent smaller checks are retained separately. Recomputed output does not overwrite the archival data unless an explicit output path requests that.

The historical JSON key bath_heat_capacity stores the dimensionless exponent c, hence the surface-entropy capacity C_B/k_B. It is not the canonical bath capacity c+1. Figure and manuscript notation use c consistently. No short-range Potts numerical simulation is included.

## Figure provenance

- figures/potts-scaling.pdf: exact microscopic mean-field occupation sums and Gamma/Beta CDFs; dotted lines are the physical secant boundary limits. It is not a Gaussian approximation to the finite-size points.
- figures/boundary-optimization.pdf: evaluation of the proved limiting balanced equal-variance physical boundary formula. It is not finite-size Potts data.
- data/figure-derived-values.json: phase constants and plotted boundary limits.
- data/boundary-optimization.csv: the universal boundary curve and its optimized version.

## Literature and claim boundaries

refs.bib supplies the manuscript citations; the LaTeX build does not require downloaded source PDFs. Research source locators and interpretation are recorded in the stage author reports and review records. Some earlier historical reviews were not available in full text; those access limits are preserved in the source audit rather than treated as evidence of absence.

The known finite-bath, Gaussian-ensemble, conditioning, phase-response, and correlation mechanisms are credited. The paper's precise theorem statements distinguish optimized strong-distance requirements from thermodynamic or local-observable equivalence. Internal review and a bounded literature search do not establish historical priority.

See [COVERAGE.md](COVERAGE.md) for every relevant source note, the corresponding manuscript result, newly completed arguments, and deliberate exclusions.
