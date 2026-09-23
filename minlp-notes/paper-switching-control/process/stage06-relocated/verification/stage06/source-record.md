# Stage 6 primary-source and data audit

Accessed 2026-09-07. This is a targeted comparison, not an exhaustive priority
search. The literature folder's AGENTS.md was read. No literature package,
original PDF, or generated literature index was changed. No original literature
PDF is redistributed. Previous precise source audits in stage04/source-record.md
and stage05/source-record.md remain part of the evidence.

## Sources used in the introduction and synthesis

- Sager, Jung, Kirches, *Combinatorial integral approximation*, Mathematical
  Methods of Operations Research73(3),363–380(2011), DOI10.1007/s00186-011-0355-4.
  Primary publisher abstract and metadata were accessed at
  https://link.springer.com/article/10.1007/s00186-011-0355-4 . It explicitly
  describes the switch-constrained NLP/MILP decomposition and tailored branch
  and bound. The local open manuscript's formulation and source notes were
  consulted; the introduction claims this established formulation and method,
  not a new decomposition or a generic invention of CIA.
- Knuth, *Two-way rounding*, SIAM Journal on Discrete Mathematics8(2),281–290
  (1995), DOI10.1137/S0895480194264757. Read the local primary arXiv manuscript
  pp.1–3, including the two-order floor/ceiling conditions, integral network
  construction, and the convex-hull observation. Open primary version:
  https://arxiv.org/abs/math/9504228 . It supports general attribution of
  integral-prefix flow methods; the paper does not identify Knuth's problem
  with the present hard-switch minimax.
- Zeile, Robuschi, Sager, *Mixed-integer optimal control under minimum dwell
  time constraints*, Mathematical Programming188,653–694(2021),
  DOI10.1007/s10107-020-01533-x. Fresh publisher text inspected at
  https://link.springer.com/article/10.1007/s10107-020-01533-x . Corollary1,
  printedp669/localPDFp17, states theta* <=(2n−3)/(2n−2)*maximumwidth for
  unrestricted CIA, with a separate tightness condition N>=n−1. The local
  p17 extraction loses the equation, so the primary HTML equation and root's
  visual PDF inspection are the equation evidence. Applying its bound on k
  equal cells gives the explicitly attributed comparison equation
  eq:classical-small-mode. No hard-budget tightness is inferred from the
  source's unrestricted-grid tightness. The issue year2021 is distinguished
  from online publication2020.
- Bestehorn–Kirches support matching and Bestehorn–Hansknecht–Kirches–Manns
  SCARP: stage05/source-record.md records the inspected final primary PDFs,
  exact locators, support condition, mode-exponential bound, and dwell scope.
  The stage6 author read that source record and retained its precise scope.
  Sources: https://d-nb.info/122645075X/34 and
  https://d-nb.info/1223084523/34 . PAMM volume20 is dated2020, with online
  publication2021; the bibliography explicitly preserves this distinction.
- Zeile, Weber, Sager, *Combinatorial Integral Approximation Decompositions for
  Mixed-Integer Optimal Control*, Algorithms15(4),121(2022),
  DOI10.3390/a15040121. Read local final-text Section3.4,p8, and Theorem1 and
  Corollary1,pp8–9, with surrounding discussion of the regularity assumptions
  and state-error interpretation. Its switch-limited class is explicitly
  deferred to other bounds in Section3.4. This supports the stated boundary
  between discrepancy and a dynamics-dependent state guarantee. Final source:
  https://mdpi-res.com/d_attachment/algorithms/algorithms-15-00121/article_deploy/algorithms-15-00121-v2.pdf .
- Abbasi-Esfeden, Plate, Sager, Swevers, *A dynamic programming-inspired approach
  for Mixed Integer Optimal Control Problems with dwell time constraints*,
  Journal of Process Control154,103522(2025), DOI10.1016/j.jprocont.2025.103522.
  The primary indexed publisher preview provided the complete introduction
  and abstract on this run:
  https://www.sciencedirect.com/science/article/abs/pii/S0959152425001507 .
  Its introduction explicitly explains loss of optimal substructure and the
  resulting absence of a general global-optimality guarantee. The manuscript
  states only this methodological distinction and dwell scope. Direct opening
  returned403, and the final full PDF was not retrieved: this is not a claim
  to have audited its full algorithm or numerical experiments. Publisher
  metadata supplies October2025,volume154,article103522 and all four authors.
- Kirches, Lenders, Manns, *Approximation Properties and Tight Bounds for
  Constrained Mixed-Integer Optimal Control*, SICONTROL58(3),1371–1402(2020),
  DOI10.1137/18M1182917. Local primary manuscript abstract and the existing
  theorem-locator record were consulted for its tight SUR setting. The
  introduction here only cites tight sum-up-rounding bounds, without
  transferring a SUR-specific constant to an optimum with fixed budget.
  Local open source: https://optimization-online.org/wp-content/uploads/2016/04/5404.pdf .
- Kirches, Manns, Ulbrich, *Compactness and convergence rates in the combinatorial
  integral approximation decomposition*, Mathematical Programming188,569–598
  (2021), DOI10.1007/s10107-020-01598-8. Read the local final-PDF title/abstract
  and source record: grid refinement, weak-star convergence and a compact
  control-to-state operator are the setting; fixed hard budgets are not added.
  The final issue is2021, despite the repository slug and online date2020.
- Bestehorn, Hansknecht, Kirches, Manns, *Non-uniform Grid Refinement for the
  Combinatorial Integral Approximation*, arXiv2305.12846v1(2023). Read local
  primary manuscriptpp1–3 and the fresh arXiv record:
  https://arxiv.org/abs/2305.12846 . It proposes adaptive SCARP grids preserving
  CIA approximation properties. The present certificate concerns an exact
  optimum under a fixed hard budget and additive accuracy. The citation is
  explicitly to the inspected preprint, not an unverified final publication.

Sager–Zeile's final49-page source, its conjectured equality, Corollary5, and the
preconjecture half-grid argument retain the source records and exact locators
from stages4–5. This stage changes no published-source mathematical comparison.
No author was contacted and no claim of first discovery follows from the search.

## Public data

Pinned commit6b073fe29984186dccfc7e2108bfba9692a6cc9c, file
examples/data/mmlotka_nt_12000_400.csv, retrieved directly from the public
pycombina repository using the URL in README.md and experiments.py. SHA-256
1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883 was verified
before parsing. The exact source date is not asserted; the bibliography uses
n.d. and the access date. Derived cell integrals and numerical facts are stored;
the source CSV can be fetched again and is not bundled. The public profile
comes from an application example, but the experiment solves only its CIA
rounding subproblem. No trajectory or original nonlinear objective claim is
made.
