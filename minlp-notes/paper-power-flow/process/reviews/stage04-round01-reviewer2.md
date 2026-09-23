# Stage 4, round 1 — independent reviewer 2

**Verdict: no major finding; two minor corrections required.**

I reviewed all integration changes and their consistency with the accepted proofs, checked the frozen manifest before and after review, and read the author report as scope documentation. I did not read other stage-4 review reports or edit the manuscript.

## Required minor corrections

1. **State a lower bound on girth, not a prescribed exact girth.** `main.tex:20–21` and `README.md:5–6` say “any prescribed fixed girth.” The proved restriction is *girth at least a prescribed fixed bound*. In particular, a bipartite graph cannot have an odd finite girth, so “any prescribed ... girth” can be read as a false exact-value claim. Replace it with “girth at least any prescribed fixed bound,” or similar wording. The introduction's explicit theorem overview already states the correct inequality.

2. **Specify the supported Python version.** `README.md:30` requests only “Python 3,” but `checks/check_resistive_exact.py` evaluates `str | None` without postponed annotations. Python 3.9 and earlier cannot evaluate that annotation. The smallest coherent correction is to require **Python 3.10 or later** in the README; no compatibility code is needed.

## Integration and scientific scope

- The abstract, introduction, conclusion, and README now retain the rational coefficient-field qualification for basic-closed rational universality. The general semialgebraic topology statement remains correctly separate. The appendix's source correction and self-contained arithmetic proof remain intact.
- The introduction accurately identifies all simultaneous graph restrictions and explains their construction. Its AC summary distinguishes real lifts, local principal differences, and reference-fixed boxes. It explicitly exempts the size-dependent positive principal cosine from the fixed numerical alphabet. One-sided reactive intervals are not promoted to symmetric tolerance robustness.
- The numerical overview correctly distinguishes an exact decision problem, the tiny-residual family, approximate certificates under a gap promise, and stability estimates. It does not turn the accuracy-bit example into an exact decision-time lower bound.
- The only change to accepted mathematical sections is the Bienstock–Verma version-specific citation, as confirmed against the accepted snapshot hashes. The new material creates no additional proof dependency or unsupported theorem claim.

## Independent source checks

- Gan–Low's [primary Caltech paper](https://smart.caltech.edu/papers/optimalflow.pdf) distinguishes physical DC networks from the linear AC approximation and states sufficient SOCP exactness conditions involving nonbinding or uniform upper voltage bounds and negative lower injection bounds. The introduction uses a scoped comparison and does not assert unconditional exactness.
- Jeeninga–De Persis–van der Schaft Part I fixes source voltages, defines the feasible demand set, proves its convexity, and gives both exact and interior alternatives in Theorem 3.22. The introduction preserves those distinctions and does not infer an exact Turing algorithm from an LMI characterization. Checked against local primary text, `[[jeeninga2023-dc-power-grids-with-constant]] p.3`, p.12-13.
- Lehmann–Grastien–Van Hentenryck fix all magnitudes to one and use a star-network subset-sum reduction. The introduction's tree/star and active/reactive model comparison is accurate. Source: `[[lehmann2016-ac-feasibility-on-tree-networks]] p.1-2`.
- Bienstock–Muñoz Theorem 7 and Corollary 8 have the stated scaled feasibility/optimality approximation scope; the manuscript does not interpret them as exact decision algorithms. Source: `[[bienstock2018-lp-formulations-for-polynomial-optimization]] p.4`.
- The Bienstock–Verma lossless fixed-magnitude model and Section 1.3 approximate-membership question were checked against the archived primary version. Using the separate explicit v2 entry resolves the previous journal/preprint attribution risk. Source: `[[bienstock2019-strong-np-hardness-of-ac]] p.1`, p.6.
- I inspected cached primary Lavaei–Low Appendix B, Case 2, which imposes real admittance and zero reactive injections before its stronger discrete-phase assertion. The introduction credits only the resistive/zero-reactive connection and supplies its own real-lift theorem and counterexamples. It does not import that stronger assertion. My attempted fresh web fetch failed, so this check uses the cached primary text at `/tmp/pfaudit/lavaei.txt`.

Previously audited arithmetic, crossover, triangulation, oscillator, and polynomial-minimum citations preserve their accepted scope. The bibliography and introduction make no unsupported priority or literature-absence claim.

## Verification appendix and packaging

I checked all eight example rows against the source equations and the legacy program. There are exactly six feasible systems, each with the displayed unique bounded solution, and two infeasible systems. The two irrational rows are correct. The short analytic arguments below the table establish uniqueness and the interval checks, not merely numerical agreement.

The historical AC sizes and squared-imaginary-voltage statistic match the saved result and audit notes. The text accurately says the licensed solver was not rerun and that historical floating-point bounds do not certify exact phase equality. The current four suites are explicitly finite supporting checks.

I independently reran the new appendix counts most directly relevant to the integration: the resistive checker returns 12,751 profiles and 606 source solutions; the legacy winding checker returns 360 scaled pairs, 4,136 cycles, and 256 nonzero windings. The other reported suite counts agree with the identical accepted checker sources and their reviewed execution output. The recurrence implementation counts `49+43k` buses and `54+47k` lines agree with the actual saved examples.

The README's commands, paths, log descriptions, and standard-library claim are otherwise consistent with the package. The ignore file excludes generated build/image artifacts while preserving source and useful logs. Eight relevant source files were independently compared between the two named worktrees and are byte-identical; the coverage map's disposition for them is supported.

## Artifacts and build

Under `verification/reviewer2/stage04-round01/`:

- `resistive.log` and `legacy-winding.log`: successful independent reruns.
- `worktree-check.json`: the eight-file worktree comparison.
- `build.log` and `build/main.pdf`: successful independent 28-page build with the intended PDF title metadata. The final LaTeX log has no unresolved-reference/citation or overfull/underfull warnings.

All 22 frozen manifest hashes remain unchanged. The two minor wording/environment corrections above are sufficient for this integration review; the separate whole-paper review remains to follow.
