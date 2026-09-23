# Empirical survey: chord-law conditioning exponents on Netlib instances

Date: 2026-09-02
Status: empirical companion to the chord-law and two-cluster notes;
script `notes/scripts/netlib_conditioning_survey.py` (qipm env, uses the
repository's cached standard-form Netlib instances). Numbers below are
one run; the script is deterministic given the cache.

## What was measured

For each small Netlib LP (presolved standard form from
`cache_dir/netlib`): log-barrier central path via damped Newton on
\(\ker A\); tail fit \(\kappa_{\rm red}(g)\sim g^{-\alpha}\) over the
last four gap decades; eigenvalue cluster count (log-gap > 1 decade
heuristic) and CG iteration count (tol \(10^{-8}\), cap 4000) at the
deepest point.

## Results

| instance | m | n | alpha | kappa_end | clusters | CG its |
|---|---|---|---|---|---|---|
| adlittle | 55 | 136 | 2.07 | 1.7e13 | 2 | 4000 (cap) |
| afiro | 9 | 18 | 2.00 | 3.8e12 | 2 | 20 |
| beaconfd | 11 | 30 | 0.02 | 1.3e6 | 3 | 28 |
| bore3d | 36 | 65 | 0.03 | 3.4e11 | 3 | 521 |
| kb2 | 46 | 71 | 0.36 | 9.6e9 | 4 | 198 |
| sc105 | 34 | 65 | 0.03 | 9.9e3 | 1 | 55 |
| sc205 | 67 | 125 | 0.03 | 7.2e5 | 1 | 286 |
| sc50a | 17 | 33 | 0.01 | 1.5e3 | 1 | 20 |
| sc50b | 15 | 29 | 0.00 | 5.8e2 | 1 | 16 |
| scagr7 | 93 | 147 | 1.30 | 8.1e12 | 2 | 4000 (cap) |
| scorpion | 77 | 136 | 0.12 | 1.1e5 | 1 | 160 |
| seba | 10 | 17 | 0.00 | 1.3e3 | 2 | 7 |
| brandy | 107 | 211 | (numerical failure) | — | — | — |
| recipelp | 63 | 107 | (numerical failure) | — | — | — |

## Reading

1. **Universality classes are visible in the wild.** The two dominant
   classes are exactly the chord law's endpoints: \(\alpha\approx2\)
   (positive-dimensional optimal face: afiro, adlittle) and
   \(\alpha\approx0\) (unique-optimum/vertex class: the sc family,
   sc50b's \(\kappa\) frozen at \(582\), seba, scorpion, beaconfd,
   bore3d). afiro's fit is \(\alpha=2.00\) with \(\kappa g^2\) constant
   over four decades.
2. **Intermediate exponents resolved by direct sublevel-geometry
   measurement.** A second, independent computation
   (`notes/scripts/netlib_sublevel_exponent.py`) measures \(D(g)\) directly by
   direction-LPs over the sublevel polytope — no eigensolves, no
   float64 wall — and fits local exponents \(\theta\) in
   \(D(g)\sim g^\theta\), which the chord law converts to
   \(\alpha=2-2\theta\):
   - afiro: \(\theta\to0\) exactly (\(D\) freezes at \(126.84\)),
     predicting \(\alpha\to2.000\) — matching the path-measured
     \(2.00\). Two entirely different computations agree.
   - sc50b: \(\theta\to1\) exactly (\(D/g\) frozen at \(126\)) — a weak
     sharp minimum, predicting \(\alpha=0\), matching \(\kappa\) frozen
     at \(582\).
   - kb2: \(\theta\) climbs \(0.08\to0.99\) across the gap decades — a
     textbook Corollary E near-degeneracy crossover observed in the
     wild; its \(\kappa\) will plateau, and the survey's
     \(\alpha\approx0.36\) was a mid-knee slope, not an asymptotic
     exponent.
   - scagr7: slopes remain unsettled (\(0.1\)--\(0.6\)) at the probed
     depths; possibly a slow multi-scale crossover; left unresolved.
   No fractional *asymptotic* exponent is claimed for any Netlib
   instance; the singularity-degree mechanism that provably produces one
   is so far exhibited only by the constructed SDP witness.
3. **Two-cluster benignity holds asymptotically but can be practically
   voided by instance-scale spread.** afiro
   (\(\kappa=3.8\times10^{12}\), 20 CG iterations), seba (7), sc50a (20)
   confirm the benign structure. adlittle is the instructive
   counterpoint: a follow-up probe (`notes/scripts/adlittle_spectrum_probe.py`, spectra at
   \(\mu\)-scales where float64 is safe) shows its reduced Hessian
   spectrum is a **single continuum of 81 eigenvalues with no decade
   gaps**, spanning 4.3 decades at \(\kappa=4\times10^4\) and 9 decades
   at \(\kappa=1.3\times10^9\), with CG growing accordingly (250, 985,
   2935 iterations — also exceeding the 81-dimensional exact-arithmetic
   bound, i.e. float64 conjugacy loss). This *answers* the open item of
   the two-cluster note: natural sparse LPs do exhibit genuinely spread
   central-Hessian spectra at practical depths. Proposition 1's split is
   real but asymptotic — the separation \(1/\mu^2\) must first clear the
   \(\mu\)-free intra-cluster spreads (here \(\gtrsim10^9\)), which for
   adlittle happens only past the float64 wall. Consequences: (i)
   classical CG cost is governed by min(dimension, spread) plus
   finite-precision effects; (ii) for the quantum polynomial route the
   situation is strictly worse: QSVT has no dimension shortcut on
   spread spectra, and by the companion note's Theorem Q (final,
   literature-grounded form) clustered spectra still cost
   \(\widetilde\Theta(\kappa)\) with plain block-encodings and
   \(\widetilde\Theta(\sqrt\kappa)\) under factor access; (iii) the corrected
   benign-\(\kappa\) message: the \(\mu\)-divergent part of the
   conditioning is never the **classical** bottleneck, while the
   \(\mu\)-free instance spread can be, and the quantum polynomial
   route pays for \(\kappa\) either way.
4. **Numerical failures are informative.** brandy and recipelp produce
   indefinite finite-precision reduced Hessians at deep \(\mu\)
   (negative computed eigenvalues at \(\kappa\gtrsim10^{15}\)) — the
   float64 wall itself, consistent with M. Wright's classical analyses
   of finite-precision interior methods.
5. Practical takeaway for QIPM resource estimation: the exponent
   \(\alpha\) is measurable from a few moderate-\(\mu\) path points and
   extrapolates the deep-path \(\kappa\); the two-cluster ratios (not
   \(\kappa\)) predict iterative-solve cost; both are cheap classical
   diagnostics to run before any \(\kappa\)-scaled quantum estimate.

## Caveats

- Presolve/rank-reduction and Phase-I choices affect which face the
  path approaches; \(\alpha\) is a property of the presolved instance.
- The cluster-count heuristic (decade gaps) is crude; intra-cluster
  ratios were not tabulated in this run.
- Fits use four points on a fixed \(\mu\) grid scaled by the initial
  gap; instances whose knee sits inside the window show intermediate
  slopes by construction.
