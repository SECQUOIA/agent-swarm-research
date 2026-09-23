# Reproducible calculations and particle experiment

All paths below are relative to the manuscript directory. The supplement also contains `observation-design.tex`, a standalone LaTeX note with the finite-grid preparation and initial-rate algebra formerly in a paper appendix; build it with `pdflatex observation-design && bibtex observation-design && pdflatex observation-design && pdflatex observation-design` from this directory. The supplement is self-contained: no script reads the research-note tree. It contains source, saved results, and figure generation, with no compiled executables. Python 3 is required. The particle runner and optional count diagnostic also require `g++` with C++17 support; plotting requires Matplotlib. The LaTeX build uses the supplied figure PDF and does not require Python or C++.

The nine research runs are fixed at initial counts 1,000, 10,000, and 100,000, with seeds 11, 29, and 47 at each size. All 90 snapshots and all nine runs are preserved in `critical_additive_particles.csv`. The source, runner, CSV, and original summary were copied without changing their contents from the verified experiment. The summary records the original compiler, platform, timings, diagnostic references, and 6,588,932 events. New figure layout does not change data. `verify_saved_particles.py` checks the archived CSV and summary without simulating trajectories:

```bash
python3 supplement/verify_saved_particles.py
```

Rebuild the six-panel PDF and PNG from the saved data with:

```bash
python3 supplement/plot_critical_additive_particles.py
```

The paper figure uses three rows and two columns, with panel letters and readable type at manuscript width. All nine trajectories and all original continuum reference curves are retained. Connecting the ten snapshots is a display choice; lines do not resolve every intervening event.

To rerun all nine particle paths without touching the archived data, write the new CSV and summary to a separate directory and plot from there:

```bash
python3 supplement/run_critical_additive_particles.py --output-dir /tmp/particles-rerun
python3 supplement/plot_critical_additive_particles.py --data-dir /tmp/particles-rerun
```

Without `--output-dir` the runner overwrites `critical_additive_particles.csv` and `critical_additive_particles_summary.json` in `supplement/`; `verify_saved_particles.py` checks only that archived location. The runner compiles into a temporary directory, runs the built-in self-test, and removes the executable on completion. Paths may differ across C++ standard libraries and floating-point platforms even with the same seeds. Timing and environment fields in the regenerated JSON will change.

For an explicit standalone build and one run, choose a temporary executable path:

```bash
g++ -O3 -std=c++17 supplement/critical_additive_particles.cpp -o /tmp/critical_particles
/tmp/critical_particles --self-test
/tmp/critical_particles 1000 11 > /tmp/critical_particles_n1000_seed11.csv
```

The built-in self-test checks cumulative selection intervals, tree capacity changes, removal, exact pair-rate algebra, count-generator identities, and conservation over 10,000 events. Every output snapshot checks count against births and deaths, the physical mass ceiling, direct mass, and tree mass. Mass tolerance is relative `1e-10`. The archived CSV prints normalized mass as one at every snapshot, so the summary records zero error in those printed values. Equal splitting preserves dyadic masses in real arithmetic, but their size range does not bound the number of significant bits needed for exact arithmetic. Floating-point rounding occurs in merges and cumulative sums even in these runs; the printed values do not certify exact conservation. Extreme size ratios in longer runs can lose small weights in cumulative sums, and the uniform random draws have 53-bit resolution.

The fitted half-moment decay rate `-log(M_half(10)/M_half(4))/6` on `t in [4, 10]`, quoted in the paper, is computed directly from the archived CSV: seeds 11, 29, 47 give 0.228, 0.275, 0.236 for n = 1,000; 0.311, 0.368, 0.302 for n = 10,000; and 0.496, 0.432, 0.455 for n = 100,000.

A prior independent implementation audit additionally exercised 20,000 randomized array/tree operations under address and undefined-behavior sanitizers; that transient harness was not archived. Its separate 2,000-seed count check used initial count 50 and final time 10, reporting mean 60.473, unbiased variance 1098.2614, and minimum count one. The exact values are mean 60 and variance 1090; the mean error is 0.64071 theoretical standard errors. The following new wrapper reproduces the declared count-check design, printing results without overwriting research data:

```bash
python3 supplement/check_particle_count.py
```

These additional counts are an implementation diagnostic, not part of the nine-run research ensemble. The wrapper was added for reproduction; the retained numerical check above is the original audit result. Three research seeds at each size are descriptive and do not define confidence intervals.

CSV conventions: the archived CSV is CRLF-terminated (written by Python's `csv` module on the original platform); readers should open it with universal newlines or `newline=""`. `normalized_count` is `L/n`; `normalized_mass` is the direct mass sum divided by `n`; `M_half` is `sum(sqrt(x))/n`; log mean and population log variance divide by actual count `L`; number CDFs divide particle counts by `L`; mass CDFs and largest mass fraction divide by total initial mass `n`. CDF thresholds are inclusive. The CSV also retains minimum size, cumulative births/deaths, and fixed and system-relative mass thresholds.

The dashed and shaded plot references concern the continuum equation. No PDE solution or numerical distance between a finite realization and a PDE solution was computed. At time 10 the available continuum mass-CDF discrepancy certificate is only about `0.0000195` for initial count 1,000 and zero for the larger sizes (`best_fractional_bound_mass_CDF_discrepancy_lower_at_time_10` in the summary JSON). These paths do not independently prove the logarithmic-time discrepancy theorem, a Gaussian limit, or log-variance convergence.

For the power-kernel counterexample, run:

```bash
python3 supplement/count_neutral_power.py
```

It compares the direct atomic vector field with the stated formula and uses exact rational arithmetic to certify the positive lower bound `151/500` for the half-moment drift at alpha = 1, p = 1/2, R = 64. Other displayed decimals are illustrative floating-point evaluations.

The earlier exact-product supplement remains available:

```bash
python3 supplement/last_coagulation_exact.py
```

Its supplied JSON includes a rational certificate for the overlap constant. Other numerical examples in that file are not promoted to exact certificates.
