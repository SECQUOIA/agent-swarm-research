# Stage 5C source-ledger helper record

This bounded author task updates source routing and packaging only. It does
not perform an independent mathematical review or close Stage 5C.

Read `source-map.md` and `root-stage5-preparation.md` in full, together with
`workflow.md` and the complete final `stage5b-assessment.md`. The latter
confirms closure after five clean second-round reports. Current manuscript
locations were checked directly for the three dynamic-scale labels in 12c
and the blockwise relative-entropy subsection in 12e.

## Changes

- Added a controlling current routing/status summary, manuscript-location
  table, final promotions and explicit comparator/exclusion rules.
- Marked the original plan and inventory as historical. The initial Stage 1
  PDF claim and all prospective routing remain legible as historical text.
- Preserved every authored stage appendix byte-for-byte, from the Stage 2
  verification heading through the final Stage 5B correction disposition.
- Removed `scripts/map_sources.py`, an unused initial generator whose
  `write_text(header+chunks)` would erase the appended verification records.
  The generator was read but never executed. `rg -n 'map_sources' .` found
  only the historical warning in `root-stage5-preparation.md`; no build or
  manuscript dependency uses it.

## Exact checks

On 2026-09-20, a read-only Python check compared all linked inventory targets
against every `workbench/*/*.md` path: 201 links, 201 unique paths, 201 current
files (200 active, one parked), no missing paths, no stale paths, no broken
inventory links and no duplicate inventory entries. All other local Markdown
links in the updated ledger resolve after this report is written.

The initial group counts are 6, 44, 25, 27, 26, 10, 3 and 60. The first five
supply 128 included sources; six initial context sources and two initially
excluded sources are promoted, giving 136 included. Four remaining initial
context sources and two scoped solver comparators give six comparator-only
sources. Removing the two promotions and two comparators from the initial
60 exclusions leaves 56 excluded; three navigation sources complete 201.

The preserved appendix suffix is 42,637 UTF-8 bytes with SHA-256
`12ead510a27260eb5ca2b06193d4943dbe25fa10d87b8aa40525b16bf3ab16a2`.
Its before/after equality was asserted directly. Each of `newt:dynamic-scale`,
`newt:scale-service`, and `newt:fixed-scale` occurs exactly once as a label in
`sections/12c-newton-comparisons.tex`.

No manuscript, bibliography, README, existing workbench file or other audit
was changed by this helper. No TeX build is needed for this ledger-only edit;
the parent author owns the integrated build and remaining stage work.

## Final comparator-only sources

- `spectral-ball-low-rank-objective-path`
- `spectral-ball-low-rank-readout-separation`
- `spectral-ball-sharp-subgeodesicity`
- `spectral-rho-geodesic-shortcut-algorithm`
- `bounded-treewidth-full-output-no-advantage`
- `sparse-newton-dequantization-envelope`

The first four retain only attributed movement overlap; the last two retain
only the structural/access comparisons proved in 12c. Their separate
algorithms and trajectory projects remain outside this manuscript's claims.

## Final excluded sources

The following exact slugs identify the 56 remaining separate-project sources.
Their complete working paths and titles are in the historical inventory.

- `adaptive-normalized-shift-hierarchy`
- `affine-slice-lp-value-lower`
- `boxed-parity-chain-readout-separation`
- `canonical-box-barriers-do-not-remove-centrality-tax`
- `checkpoint-span-recycling`
- `coherent-inverse-quadratic-frontier`
- `constant-relative-parity-chain-lp-audit`
- `degenerate-lp-reduced-hessian-limit`
- `eccentricity-profile-socp-preconditioner`
- `exact-optimal-dense-coupled-box-barrier-tax`
- `exact-optimal-hyperoctahedral-box-barrier-tax`
- `exact-optimal-hyperoctahedral-box-discrete-tax`
- `exact-scalar-centrality-dilation`
- `exact-two-cluster-shift`
- `exponential-mixture-support-lower-bound`
- `exponential-sq-separation-one-cone-socp`
- `facet-regular-coupling-box-centrality-tax`
- `fixed-factor-multivariate-tilted-jet-compiler`
- `fixed-instance-sparse-kkt-temporal-collapse`
- `forrelation-thresholded-single-optimizer-coordinate`
- `gaussian-quadrature-exponential-cone-compiler`
- `general-inner-small-success-composition`
- `generalized-power-newton-sq-dequantization`
- `genuinely-coupled-symmetric-box-barrier-tax`
- `growing-factor-tilted-jet-refinement`
- `inverse-quadratic-polyfactor-lower`
- `inverse-quadratic-product-composition-obstruction`
- `joint-accuracy-normalized-shift-lower`
- `joint-accuracy-normalized-shift`
- `joint-accuracy-pinned-gate`
- `jordan-spectral-interval-distance-centrality-tax`
- `local-full-kkt-parity-mass-obstruction`
- `lorentz-newton-sq-dequantization`
- `multiplexed-lp-central-path-direct-sum`
- `multiplexed-socp-decrement-direct-sum`
- `network-flow-explicit-output-no-advantage`
- `nonabelian-a5-holonomy`
- `normalized-shift-staircase`
- `one-cone-socp-scalar-observable`
- `parameterized-one-cone-scalar-frontier`
- `positive-slope-exponential-moment-compiler`
- `robust-signed-exponential-moment-grid-compiler`
- `sharp-separable-centrality-tax`
- `simplex-search-central-path-treewidth-boundary`
- `single-scalar-central-path-parity-saturation`
- `sparse-box-lp-geodesic-centrality-tax`
- `sparse-box-primal-dual-completion-tax`
- `sparse-lp-newton-access-separation`
- `sparse-sq-affine-lp-value-upper`
- `sparse-sq-conditioning-frontier`
- `sparse-sq-inverse-quadratic-lower`
- `sparse-sq-newton-decrement-upper`
- `tilted-jet-entropic-risk-ecp`
- `two-cluster-interval-shift-upper`
- `zero-query-state-conversion-radius`
- `lorentz-cone-condensation`
