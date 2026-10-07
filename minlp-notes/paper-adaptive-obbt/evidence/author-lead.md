# Lead author report

Lane: lead (framing, foundations, all September local-rate developments).
This report records what the lead files contain, the corrections and
developments relative to the September and October sources, the September
coverage, the integration of the audits and reviews, citation needs, and the
checks actually run.

## Files written

| File | Content |
| --- | --- |
| `main.tex` | Shared preamble, title, anonymous author, input order of all sections in the brief's planned order, unnumbered supplementary-material statement, both appendices, bibliography (`plainurl`, `references.bib`). No table of contents. |
| `abstract.tex` | Provisional abstract (about 230 words). |
| `sections/introduction.tex` | Problem, three decisions, the three limits, results by part, relationship between rates and certificates, significance of the empirical finding, qualified attribution, organization. |
| `sections/related.tex` | Related work following the preliminary literature audit and the vetted keys in `references.bib`. |
| `sections/foundations.tex` | Problem, relaxation family, validity and whole-construction monotonicity, lifted monotonicity, attainment, operator, update schemes, schedules lemma, sublevel hull, fixed boxes, persistence, limit and greatest fixed box under closedness, non-fixed-limit example, three limits. |
| `sections/local-rates.tex` | All September local contraction and stalling results, exact quadratic results, composite McCormick expansion, boundary theorem, consequences for gaps and stopping. |
| `sections/discussion.tex` | Starting, stopping, repeating, width versus search cost, scope. |
| `appendices/local-proofs.tex` | Full proof of the composite expansion (five lemmas and the induction), proofs of the boundary lemma and theorem. |

## Shared preamble

Packages: `fontenc`, `inputenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`,
`mathtools`, `booktabs`, `array`, `enumitem`, `geometry`, `natbib`
(`numbers,sort&compress`), `url`, `microtype`, `hyperref`. Theorem
environments share one counter numbered within sections: `theorem`,
`proposition`, `lemma`, `corollary` (plain); `definition`, `assumption`,
`example` (definition style); `remark` (remark style). Macros: `\R`, `\Q`,
`\norm`, `\abs`, `\hull` (box hull), `\conv`, `\dist`, `\diam`, `\supp`,
`\midop` (median), `\sgn`.

Notation fixed in foundations and local rates: `B=[\ell,u]`, `w(B)`,
`p(B)=(-\ell,u)`, family domain `\mathfrak B`, projected objective `\phi_B`,
lifted set `R(B)` with objective `v`, `K_U`, `T_U`, `\epsilon=U-f^*`,
relaxation bound `L(B)`, sublevel hull `H_U`, fixed box, sequential round
`S_U`, shapes `d=(d^-,d^+)`, `D(d)`, gauge `g_u`, tangent model `Q`, `S_c(d)`,
`\Phi_c`, `\Phi`, `r^*`, face values `m_i^\pm(d)`, active and free sets `A`,
`F`, admissible cone `\mathcal S`, `Q^F`, `G^F`, coordinate width `w_i(B)`.
Lifted products use `y_k`, matching the certificates and algorithms lanes.

## Coverage of the September results

| September result | Location | Treatment |
| --- | --- | --- |
| Setting, R1–R2, Jacobi versus sequential rounds | `foundations.tex`, eqs. `eq:validity`, `eq:monotonicity`; `lem:sequential` | Whole-construction monotonicity, lifted monotonicity, attainment premise for lifted sets. Schedules lemma: `T^m(B) ⊆ C_m`, complete blocks inside `T(C_j)`, equal limits for fair schedules. Analytic Jacobi/sequential example with factors 1/2 and (9+√17)/32. |
| Lemma 1 | `lem:order`, `prop:fixed-limit` | Proved; intersection identified as a fixed box only under `eq:closed-family`; `ex:not-fixed` shows the failure. |
| Proposition 2 (sharp minima) | `prop:sharp-growth` | Separate zero and positive slack, `tau=0` case; attribution to marginals-based range reduction. |
| Proposition 3 (quadratic growth) | `prop:quadratic-growth` | Envelope statement at positive slack; cluster-threshold connection; failure on the model problem. |
| Assumption T, consequences, `Phi_c`, `r*` | `ass:tangent`, `lem:tangent-properties`, `lem:cw` | `Phi_c` only for `c>=0`; `r*` equals the `Phi`-based Collatz–Wielandt number under lower semicontinuity; no nonlinear Perron–Frobenius identity claimed. |
| Theorem 4, Corollary 5 | `thm:tangent-contraction`, `cor:tangent-rate` | Gauge form with explicit envelope; `O(sqrt eps)` upper bound, matching lower order only under extra premises. |
| Theorem 6 | `thm:local-stall` | Strict margin with remainder; zero-remainder non-strict version in `prop:quadratic-rows`; stall implies `r*=1`; cutoff improvements cannot remove the fixed boxes but can tighten outside them. |
| Lower-bound remark | `prop:tangent-eigenrate` | Exact `Theta(rho^k)` and `r*=rho` with an elementary argument; `rho=0` separated. |
| Section 4 quadratic model | `eq:quadratic-Q`, `eq:cube-Q` | Translation and scaling argument; `H_ii<0` chord noted; indefinite `H` needs constraints that exclude negative curvature. |
| Proposition 7 | `prop:two-variable-rate` | Exact cube rate, `Theta(rho^k)` from interior boxes, no successive-ratio claim, scaled version. |
| Numerical checks of Section 4 (power iteration values, `n=3,a=0.5` value, stalls at `n=5,10,20`) | `ex:many-term` | Superseded by an exact formula `t_n(a)` and the exact stall threshold `a(n-1)(n-2)>=2`; no numerical values quoted. |
| Proposition 8 and its scaled version | `prop:quadratic-rows`(a) | Non-strict condition, rectangular scaling, zero half-widths. |
| Strongly convex example | `ex:many-term` | Exact dichotomy; `a=1/10`, `n>=6`; diagonal dominance does not prevent the stall. |
| "Row condition not necessary" (random test) | `ex:signed-stall` | Replaced by an exact signed three-variable strict stall. |
| Section 4b, Theorem 12 and the proofs-12-11 Part A | `sec:local-rates-factorable`, `thm:composite-expansion`, `sec:local-proofs-composite` | Full recursion, explicit upper product rule, all three properties proved together, clipping, `C^{2,1}` order, degenerate cases, representation dependence, nonsmooth cancellation example. Numerical tables of A.5 not reproduced (the theorem is proved). |
| Remark on auxiliary-variable relaxations | paragraph after the theorem | Objective-only auxiliaries give the termwise model with exact squares, the finite-square model with tangent squares; otherwise the assumption must be verified. |
| Corollary 9 | `cor:local-gap`, `prop:two-variable-cutoff-floor`(c) | Constant `(2G/delta+1)eps`, asymptotic version, `eps=0`, sharp case; exact model gap `a eps/(1-a^2/4)`. |
| Lemma 10 | `lem:sublevel-hull` | Hull and fixed boxes are independent enclosures of the limit; symmetry prevents singleton convergence, not all tightening. |
| Proposition 11, Lemma B1, Part B proofs | `thm:boundary`, `lem:boundary-step`, `sec:local-proofs-boundary` | Terminal-case repair (`N>=2` for the refined estimate), admissible start shape, upper enclosures only, lower bounds (ii) and (iv) with negative-numerator case, zero-gradient and all-active cases. |
| Part B numerical check (2.3094 sqrt(eps), 2.333 eps) | `ex:boundary` | Reproduced exactly by an analytic decoupled example: `(4/sqrt3) sqrt(eps)` and `7 eps/3` at `a=1`. |
| Section 6 practical rule and caveats | `sec:local-rates-consequences`, `discussion.tex` | Rounds bound as an upper bound with `max{0,ceil}`; observed ratios as heuristics with exact examples; certificate regimes; symmetry. |
| Review-theory items (Jacobi 0.7247 vs sequential 0.7053; translated-cube eigenvectors; Corollary 9 numerics) | `foundations.tex` example after `lem:sequential`; `prop:asymmetric-eigenboxes`; `prop:two-variable-cutoff-floor` | Numerical sequential factor removed (archived operator was variable-block); replaced by an exact analytic example. Eigenbox interval exact: `r/(1+r)<=c<=1/(1+r)`, about `[0.4367,0.5633]` at `a=1`, not `[0.41,0.5]`. Corollary 9 constants derived exactly. |
| September external-presolve study | Described by the algorithms lane (`sec:experiments-precursor`, `precursor-study.tex`); summarized in the introduction and discussion with corrected interpretation. |

## Corrections relative to the sources

1. The false chain `H_U ⊆ P ⊆ B_∞` (root finding) is replaced by two
   independent inclusions with a counterexample showing neither box need
   contain the other.
2. The boundary proposition's refined active estimate is restricted to
   `N>=2`; the coarse estimate covers `N=1`; the free statement is an upper
   enclosure; the start shape must be admissible.
3. "Exact asymptotic rate" claims became upper bounds, with equality only
   for a positive eigenvector and zero remainder.
4. The archived sequential factor 0.705 was produced by a variable-block
   scheme (foundations review). It is no longer quoted. A narrow check run by
   the lead (below) gave 0.705323 for signed-direction updates as well, but
   the manuscript follows the root's instruction and uses only the exact
   analytic example.
5. The translated-square eigenvector range is exact and narrower than the
   archived approximation.
6. The local conditions are presented as sufficient, not exhaustive, with the
   critical example (sublinear convergence, limit width `2 eps^(1/3)`).
7. Selective schedules inherit Jacobi lower enclosures but no upper bound.
8. Indefinite-`H` wording reversed to "constraints that exclude
   negative-curvature directions".
9. Cutoff improvements in the stall regime: cannot remove the fixed boxes,
   may still tighten outside them.
10. A single minimizer at a node does not supply the local hypotheses.

## Developments beyond transcription

- Schedules lemma with fair-schedule equality by monotonicity alone (from
  the integration notes, proved in the text), closedness lemma for
  continuous lifted families, greatest-fixed-box characterization,
  non-fixed-limit example on all subboxes.
- Face test (`cor:face-test`) organizing contraction and stall tests.
- Sufficient row condition for contraction (`prop:quadratic-rows`(b)),
  attained by the signed stall example.
- Exact `n`-variable dichotomy with eigenvalue `t_n(a)`; exact
  positive-slack limit for every bounded start containing the floor cube,
  with error ratio `a/2`; exact asymmetric eigenvector condition; centered
  rectangle map and the first-round ratio 0.485 from a thin rectangle.
- Finite-tangent square example linking the local theory to the
  certificates' reference family.
- Exact decoupled boundary example; free-gauge non-contraction example.
- Explicit upper product rule, sign-selection proof for all cases,
  nonsmooth cancellation example.
- Linear-equation remark reduced to a pointer to the constraints lane's
  `prop:restricted-tangent-con`, which proves the restricted contraction
  theorem; the remark states that all results of the subsection restrict.

## Audit and review findings applied

All findings of `audit-rates.md`, `review-foundations-r1.md`,
`review-local-r1.md` (main-section and appendix findings, including the
remaining-items checklist), and the lead-relevant items of
`INTEGRATION-NOTES.md` were applied. The `proposed-critical-example.tex`
content was verified and inserted as `ex:critical-scalar` in the lead's
style. The `(B-asym)` active-width asymptotic equality of the rates audit was
not added; lemma parts (iii) and (iv) give the same first-order sharpness.

## Integration notes for the root

- Labels defined by the lead and used by other lanes all exist:
  `eq:validity`, `eq:monotonicity`, `eq:projected`, `eq:closed-family`,
  `lem:order`, `lem:sequential`, `lem:sublevel-hull`, `lem:fixed-persist`,
  `prop:fixed-limit`, `ex:not-fixed`, `prop:quadratic-growth`,
  `prop:quadratic-rows`, `ex:many-term`, `ex:shape-change`,
  `ex:finite-square`, `cor:face-test`, `sec:foundations`, `sec:local-rates`.
- At the last build, undefined references remained only in other lanes:
  `sec:histories-con` (residual), `eq:order-lipschitz` and
  `thm:residual-tail` (constraints). They appear to follow concurrent renames.
- Overlap: the "observed ratios" paragraph of `sec:local-rates-consequences`
  points to the constraints and residual history results rather than
  restating them.
- The abstract and introduction are provisional pending the final literature
  audit. The title is provisional.
- The supplementary-material paragraph distinguishes October frozen inputs
  from September retained inputs; please confirm it against the companion
  README before submission.

## Citations used and requests for the literature lead

Keys cited by the lead files: `caprara2010-global-optimization-problems-and-domain`,
`caprara2016-theoretical-and-computational-results-about`, `belotti2012fbbt`,
`tarski1955fixpoint`, `ryoo1995-global-optimization-of-nonconvex-nlps`,
`wechsung2014-the-cluster-problem-revisited`,
`kannan2017-the-cluster-problem-in-constrained`,
`bompadre2012-convergence-rate-of-mccormick-relaxations`,
`najman2016-convergence-analysis-of-multivariate-mccormick-relaxations`,
`mccormick1976-computability-of-global-solutions-to`,
`mitsos2009-mccormick-based-relaxations-of-algorithms`,
`scott2011-generalized-mccormick-relaxations`,
`gleixner2017-three-enhancements-for-optimization-based`, `scip2026obbt`,
`coramin2023filters`, `cengil2025learning`, `gomezcasares2025domain`,
`badilla2024tradeoffs`, `pineda2025sweetspot`, `gonzalezdiaz2025lifted`,
`jachymski2016perov`, `borrelli2003parametric`,
`hoffman1952-on-approximate-solutions-of-systems`,
`robinson1973-bounds-for-error-in-the-solution-set`, `walker2011anderson`,
`hendel2018adaptive`, `chmiela2023scheduling`, `hay2012computations`.

Claims to verify against the sources:

1. Ryoo–Sahinidis 1995: the marginals test confines a variable at a bound of
   the relaxation optimum, with marginal `lambda>0`, to within `(U-L)/lambda`
   of that bound.
2. Wechsung–Schaber–Barton: `K<=lambda_1/8`; Kannan–Barton: `tau*<=gamma/8`;
   their prefactors bound minimum-value gaps.
3. Bompadre–Mitsos: second-order pointwise convergence of McCormick
   relaxations under smoothness conditions; Najman–Mitsos: multivariate
   McCormick convergence analysis (cited only as an extension).
4. Mitsos–Chachuat–Barton: the product rule and median rule as written.
5. Scott–Stuber–Barton: the standard procedure clips to interval bounds;
   monotonicity theorem and its premises (argument intervals inside the
   scalar domains, Lipschitz scalar functions); remark that the unclipped
   rule can violate monotonicity.
6. Caprara–Locatelli: one-variable iterated reduction equals the parametric
   reduction; order independence of cyclic sweeps. Caprara–Locatelli–Monaci:
   lower limit, two-variable class, examples without any reduction.
7. Belotti et al.: greatest fixed point, possibly infinite iteration, LP for
   linear constraints.
8. Gleixner et al.: filtering, ordering, Lagrangian variable bounds as an
   approximation of repeated OBBT, and the remark that a zero-tightening call
   can still yield a useful dual inequality. SCIP source: root-only OBBT
   with a budget tied to root LP effort; generalized-bound propagator reacts
   to incumbent improvements.
9. Hoffman and Robinson are cited only as the classical source of error
   bounds that the feasible-repair argument resembles.

Sources not cited because they are not in the vetted bibliography, but
which would strengthen related work if vetted: Zamora–Grossmann 1999
(published contraction sequence with a constant per-step ratio), Castro 2023
(gap after repeated OBBT versus cutoff quality), Puranik–Sahinidis 2017
(remark on slow convergence of iterated tightening), Neumaier 2004 (the
`o(eps^2)` remark on the cluster effect), Ryoo–Sahinidis 1996
(branch-and-reduce and its improvement-threshold loop), and documentation of
round caps and improvement thresholds in BARON, Couenne, ANTIGONE, Alpine,
MAiNGO, EAGO, and Coramin. No literature search was run by the lead.

## Verification actually run

All checks are targeted. No experiment was rerun, no project-wide check was
run, no CI status or logs were inspected, and no literature search was run.

1. `python3 /tmp/lead-checks/seq_check.py`: exact one-dimensional
   minimizations with bisection for `x^2+y^2+xy` with McCormick at cutoff
   zero from `[-1,1.3]x[-1.2,1]`. Output: Jacobi late-round ratio 0.724745;
   signed-direction sequential ratio 0.705323 for the orders
   `(x+,x-,y+,y-)` and `(x-,x+,y-,y+)`. Used only to understand the archived
   value; the manuscript does not quote it.
2. `python3 /tmp/lead-checks/family_check.py`: compared `t_n(a)` with
   numerical face minimization for `(a,n)=(0.5,3),(0.8,3),(0.2,4),(0.15,4),(0.3,5)`
   (all agree to six digits; the last stalls) and printed `rho(a)`, `r`, and
   the eigenbox lower endpoint for `a=0.5,1,1.5,1.9`.
3. Scratch LaTeX builds in `/tmp/lead-build` through `/tmp/lead-build4`
   with `pdflatex`, `bibtex`, and two further `pdflatex` passes on a copy of
   the manuscript. Intermediate builds showed undefined references only in
   other lanes' files. Final build (`/tmp/lead-build4`): 91 pages, no
   errors, no undefined references or citations, no overfull boxes. Pages 1,
   18, and 22 of an earlier build were rendered with `pdftoppm` and
   inspected.
4. `python3 verification/check_sources.py` from the manuscript root. Earlier
   runs reported only other lanes' undefined labels and a stale citation
   key; the final run is recorded below this list.
5. A scan of the lead files for `TODO`, `FIXME`, `TBD`, private paths, and
   `run:` links found none.

Final `python3 verification/check_sources.py` output:
`SOURCE_CHECK=ok: 16 TeX files, 237 labels, 28 citations`.

All mathematical statements in the lead files were derived or checked
analytically while writing; the scripts above are supplementary.
