# Stage 5, round 1 — independent review 4

## Verdict

**No major issues. One minor scientific wording correction is needed in the introduction.** The deterministic calculations, archive provenance, plotted formulas, proof relocation, and stated numerical scope check out independently.

I read `stage-5-author.md`, the new introduction, numerics, and conclusions, the revised main file, README, coverage record, reference entries, figure code, standalone exact solver, independent checker, and relevant theorem dependencies. I did not read any other current-round report, edit the manuscript, or delegate. My numerical calls imported the checker functions without invoking their file-writing entry points.

## Actionable issue

### R4.1 — Restore the distinction for unbounded observables in the introduction

- **Severity:** minor; local scientific clarification, with no effect on any proof or numerical result.
- **Location:** `sections/introduction.tex`, second paragraph: “It is stronger than agreement of thermodynamic potentials, energy density, or any specified finite set of averages.”
- **Reason:** This suggests an unconditional implication from TV convergence to those other convergence notions. The framework correctly explains that convergence of unbounded observables requires additional uniform integrability. Energy density remains unbounded in the spin–momentum model, and the general weak-support theorem deliberately assumes no moments. Normalized probability-law TV also does not by itself identify thermodynamic partition-function normalizations. The correct intended comparison is that matching these other quantities does not generally imply full-state TV.
- **Correction:** Replace this sentence with a one-way statement, such as: “Agreement of thermodynamic potentials, energy density, or a specified finite set of averages does not in general imply full-state TV convergence.” Either briefly repeat the uniform-integrability qualification for the reverse implication or direct the reader to the framework's existing explanation. Keep the preceding correct statement that TV controls bounded measurements.
- **Evidence:** The four-atom physical-bath example recorded in my Stage 1 report has TV tending to zero while the mean-energy error grows as `N^3`, hence the energy-density mean error grows as `N^2`. The general framework permits such a law. No new counterexample construction is needed; the new synthesis should remain consistent with the already corrected framework.

## Deterministic calculation audit

### Exact finite-system solver

The occupation-orbit enumeration uses the correct permutation multiplicities, multinomial factors, and canonical exponent. Equal-energy aggregation preserves the energy likelihood calculation. The kinetic integral produces the correct `A+c` occupation exponent and `Beta(A,c+1)` conditional law. The returned `energy_tv` uses the two crossings of the full spin–momentum likelihood; `config_tv` separately measures the spin-configuration marginal. Figure 1 uses `energy_tv`, as claimed.

The physical secant calibration and relative log normalization are consistent with the manuscript's formulas. The code handles inaccessible kinetic intervals and protects the upper root at the bath cutoff. Its omitted-canonical-mass bound uses a conservative floating-point threshold and the global maximum of the normalized likelihood to detect possible revival under reweighting. The documentation correctly treats floating-point results as numerical checks rather than interval certificates.

### Archive and fresh checks

I independently obtained:

| Check | Result |
|---|---|
| Archive SHA-256 | `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1` |
| Archive versus original research file | Byte-for-byte identical |
| Number of archive rows | 18 |
| `N=12000`, smaller boundary coefficient | Full TV `0.14834067165793124` |
| `N=12000`, larger boundary coefficient | Full TV `0.0373037383423388` |
| Explicit labeled-spin checks | All eight sizes, `N=1,...,8`, passed |
| Additional density check, `N=14`, Gamma shape 7, capacity 35 | Direct quadrature `0.12907595778894462`; exact-CDF code `0.12907595777661585` |
| Same additional density check, likelihood identity | Maximum absolute error about `3.0e-14` |
| Independent `N=1000`, `c=0.5 N^(3/2)` recomputation | `0.10999302354890839`, versus archive `0.10999302354890816` |

The `N=14` test and the `N=1000` archive comparison add cases beyond the author's reported fresh `N=12` and `N=300` checks. No expensive full archive regeneration was needed to establish distinct additional confidence.

### Figure formulas and rendering

I independently integrated the weighted shifted-normal densities for the secant limits, rather than simply calling the figure's CDF helper. For boundary coefficients `0.5` and `2`, I obtained `0.1573918218751486` and `0.03798598066534446`. These agree with the figure-derived values `0.15739182188178924` and `0.0379859806585022` to about `7e-12`. The numerical paragraph rounds both limits and the largest finite-system values correctly.

All 801 rows of the boundary-optimization CSV agree with `2 Phi(lambda/2)-1` and its minimum with one half at the stored precision. The crossing constant is correct. Both PNG figures were visually inspected: labels, legends, asymptotes, and axis scales are legible and match the numerical text. The finite-size plot only extends the boundary sequences to `N=12000`, as its caption states.

The manuscript explicitly distinguishes:

- exact finite-system formulas evaluated in floating point from asymptotic formulas;
- full spin–momentum TV from the spin-only marginal distance;
- secant-calibrated finite data from optimization over all composite energies;
- the mean-field enumeration from a short-range simulation;
- the universal limiting curve from finite-size Potts observations.

These distinctions are accurate. The visual trends are used as illustrations, not as numerical proofs of the threshold exponents.

## Proof relocation and manuscript consistency

I reconstructed the previously accepted microscopic section by removing the new main-text proof guide and returning the appendix body with its original heading level. The reconstructed file's SHA-256 is exactly

`4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2`.

This independently confirms that the accepted short-range proof was moved without mathematical alteration. The main-text guide correctly summarizes its two positive phase partitions and bond-to-spin transfer. The Gaussian and capillarity results remain included in the PDF through their appendix inputs.

An independent scan found no duplicate labels, no missing reference labels, and no missing bibliography keys among the 23 cited entries. The existing compiled PDF has 47 pages and the expected title metadata. Its log has no undefined references/citations or overfull/underfull warnings. I inspected the existing build rather than modifying the frozen review artifact with another build.

The coverage table maps the relevant reservoir notes to actual theorem and equation labels. The exclusions are separate research directions and do not remove a dependency needed for the reservoir proofs. The synthesis consistently preserves the sufficiently-large-fixed-`q` condition, the restricted two-dimensional boundary coefficient range, the optional kinetic sector, the explicit capillarity-model status, and the separate entropy argument for growing microscopic spaces. The source discussion credits established finite-reservoir, Gaussian-ensemble, conditioning, and correlation mechanisms and avoids promising exhaustive historical priority.

## Reproducibility and limitations

The README provides the setup, build command, quick checks, figure regeneration, archive plan, output behavior, and capacity convention needed to reproduce the displayed calculations. The PDF build does not require Python or network access. The archival data are preserved separately from recomputations. The support records distinguish internal review from external acceptance and accurately leave the final whole-manuscript review as a separate stage.

This review does not certify exhaustive bibliographic priority or independently reproduce all large-size archive rows. The exact derivation, archive integrity check, independent small-system calculations, additional finite-size check, and transparent reproduction code support the numerical claims actually made.
