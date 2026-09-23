# Coordinator investigation

## Environment

The existing measurement environment reports Python 3.13.11, NumPy 2.5.3,
SciPy 1.18.1, SymPy 1.14.0 and Gurobi 13.0.3. A quiet, one-variable Gurobi
license smoke test returned status 2 (optimal). `latexmk`, `pdftotext` and
`uv` are available. This smoke test is environment evidence, not numerical
validation of the research algorithms.

## Scientific questions for the staged work

- Preserve all 2,347 source-feasible schedules in the public kinetics reanalysis.
  The exact trace recheck already establishes one changed optimizer. Complete
  exact determinant and trace-inverse comparisons if practical, to remove
  floating-point ties from the other 22 comparisons.
- Use actual covariance of selected observations. The source-model comparison
  is an audit of inspected versions and archived numerical inputs, not a replay
  of all published experiments or a claim about uninspected stored solutions.
- Keep public independent-time/channel-selection evidence distinct from the
  synthetic temporal-correlation and all-or-nothing packet experiments.
- The separator hierarchy compares nested anchor sets and mathematical
  relaxation optima. Arbitrary block sizes need not be nested; incomplete
  algorithmic upper bounds need not be monotone. Fresh experiments should
  distinguish this and include equal information about incumbents and cost.
- Bound certification time, incumbent generation, and numerical proposal time
  must all be accounted for. Historical timings cannot become fresh repeated
  measurements by summing them.
- A useful focused new study is a matched nested-separator/finite-history/dense
  comparison with fixed physical covariance, plus tiny exhaustive original-model
  checks. Broader solver-superiority claims require more than these prototypes.
- Retain the mathematical spectral-set result as relevant supporting theory,
  explicitly separate from the practical implemented certificate algorithms.
- The old general-covariance note's prospective review status is superseded by
  the later independent review. Inspect final theorem/addendum versions.

## Fresh source checks

Online search found the complete primary HTML for Ahipaşaoğlu, Cipolla and
Gondzio, *A column generation approach to exact experimental design* (2026),
DOI 10.1007/s12532-026-00326-1. Its regression-vector model and correlated
synthetic vector generator must be distinguished from selection-dependent
covariance inversion. Complete-design mixtures and column generation are
established methods. Stage 1 author was asked to inspect this source and the
locally available Filová multiresponse design source, and to update stale
full-text availability records based on actual current access.

## Additional primary-source search during Stage 2

2026-09-13: Found accessible Filová, Somogyi and Harman primary preprint
https://arxiv.org/html/2507.04713v1 (2025-07-07), later published ASMB
42(2), e70072 (2026-02-12), DOI 10.1002/asmb.70072. Read Sections 1–4,
especially Section 3 Eq. (4), general PSD elementary information matrices
and independent trials, and Theorem 1, rank-one decomposition with equality
constraints tying copies and binary support indicators. This is an explicit
prior reduction for multiresponse additive design plus linear/sparsity constraints,
not a selected-correlated-error inverse theorem. Stages 3, 4 and 6 should cite
the exact scope, without claiming packet design or rank-one splitting new.
The accepted/final version itself was not retrieved.

Retry for Onn (2010) Chapter 6: official EMS contents
https://ems.press/books/zlam/84/contents lists pp.97–128 behind subscription;
author PDF at https://ie.technion.ac.il/~onn/Book/NDO.pdf did not open.
No new chapter-content inference.

Radovilsky–Shattah–Shimony (2006) primary-paper search located a CiteSeer
copy indexed with full first page:
https://citeseerx.ist.psu.edu/document?doi=c0a8fa313ec7231a4109221ccf42c9c6b4093a9d&repid=rep1&type=pdf
Direct opening failed. This does not resolve the historical fulltext gap.
Institutional metadata confirms DOI 10.1109/ICSMC.2006.385249, pp.2559–2564.

## New Stage 2 development to carry into computations

Root identified and Stage 2 author developed the complete-block far-pair
refinement: in observation-noise-whitened coordinates, the cross covariance
starts at the earlier fresh prediction covariance and propagates through
contractive transitions and full-state updates. Thus the scalar sharp-far
constant 2 Pbar [T_L(rho)+kappa N_L(rho)]/d_* also holds for complete blocks,
without commutativity; the older generic gain-row constant remains valid.
Root's separate noncommuting dense diagnostics passed 378 subset/window cases
and 560 far pairs; author added exact rational checks.

Stage 5 should include a focused numerical comparison of these two constants
on the archived full-block examples (or a matched fresh small block instance),
with any new exact certificate labeled freshly recomputed. Do not silently
replace the bound formula underlying old archived results. This gives a
concrete empirical check of the new theoretical refinement developed while
writing the paper.

## Robust primary source inspected for later-stage handoff

2026-09-13: Root read Wang–Yue2026 user-supplied fulltext first pages and
independently extracted original PDF pp.3–4. The source is a 15-page SSRN
preprint 6484802, not a verified journal article. Equation6 uses additive
per-time information (independent trials), exact sample count, and binary
subset refinement by one-for-one exchanges with multiple starts. Section3.1
compares fixed worst case, alternating updates, and a growing active-scenario
maximin method, with discrete designs refined by Powell-type exchange.
It supports prior robust kinetic sampling and scenario exchange, not novelty
of maximin or robust sampling here. Our distinction must concern correlated
selected covariance and certified finite-scenario normalized guarantees.
Section3.2 D log-expectation identity is valid; its stated E-optimal expected
reciprocal-to-expected-eigenvalue equivalence is not valid in general and
must not be inherited. We need only its D-design comparison. The paper's
experiments do not supply evidence that our finite-scenario certificates
cover a continuous uncertainty region.

## Stage 4 independent reconstruction

The root's separate rational script `verification/stage04-root/check_separators.py`
passed 160 nested Gaussian elimination identities, 40 mixture Schur/Loewner
and determinant orderings, and 120 arbitrary-nuisance quadratic supports.
The fixture has signed nonstationary transitions, heterogeneous measurement
noise, a non-diagonal parameter prior, and empty/interior/full anchor sets.
These finite checks supplement the general proof and carry no timing claim.

For a transparent strict hierarchy example, use n=2, p=1, k=1,
K=[[1,1/2],[1/2,1]], R=K+I, F=(1,-1), J0=1. The equal mixture of singleton
schedules has target information 3/2 with no anchors, 75/44 with anchor {0},
and 9/5 with both anchors. The first and last are their respective hull optima
(constant exact information, and symmetry plus concavity). The middle value
is only an evaluated mixture, not a claimed optimum.

A fresh online source check confirmed VNDesign 0.1.0 was published on CRAN
2026-07-30 (DOI 10.32614/CRAN.package.VNDesign). Its current reference manual
explicitly distinguishes its classical virtual-noise heuristic and efficiency
diagnostics from the convex 2022 formulation. The same manual is already
available locally; no new absence or implementation-comparison claim follows.
Root independently read the Sagnol–Harman reprint's first seven pages and the
Levine–How augmentation proposition; their generalized subsystem criterion,
finite information atoms, and nuisance augmentation are established prior art.
