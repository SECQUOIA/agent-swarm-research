# Independent final review of the sparse-regression chapter

Date: 2026-10-05; citation-only refresh: 2026-10-06. Reviewer scope: `sections/regression.tex` and
`appendices/regression-proofs.tex`. This report is internal review evidence,
not a manuscript proof dependency.

## Final disposition

**Pass for the mathematical statements and proofs in the reviewed files.**
No unresolved mathematical or readability issue remains in this chapter.
The completed appendix contains the proofs required by the selected
theorems; internal evidence files are not proof dependencies. This is a
chapter review, not a claim that a final integrated LaTeX build or the
entire manuscript has been independently checked here.

The final reviewed SHA-256 hashes are:

| File | SHA-256 |
|---|---|
| `sections/regression.tex` | `abb0dd9920afe7fcfe466c766d4c38e2982bb4ff4dadcaa3c9776e047d600d09` |
| `appendices/regression-proofs.tex` | `759760aff46a9376db68a325f9207a642bd0c3d02b0957d404c2db59fc8274a9` |

The author explicitly reported both files complete and stable for review.
The section hash above includes the subsequent verified citation additions
and the two small clarification edits described below. The appendix was
fully reviewed at hash
`0a396fa09ab8de93c6730f6066cef11e4c6b6eaf3842bf2ba81a2ce043fd0d05`.
The 2026-10-06 refresh adds only concentration citations and their
normalization explanation. Removing those exact additions in memory
reproduces that original hash, verifying that the equations, hypotheses,
and proof steps are unchanged. The mathematical pass therefore applies
to the current hash.

Appendix line locators below refer to the original full-proof review
version. The citation refresh adds seven lines before the main proofs;
the theorem and equation labels remain the stable locators.

## Scope and review basis

I read `BRIEF.md`, `AUTHORING-CONVENTIONS.md`,
`ARCHITECTURE-DECISION.md`, `ISSUES.md`, the sparse-regression portions of
`AUDIT-DISCRETE.md`, `INCOMING-AUDITS.md`, `LITERATURE-KEYS.md`, and the
complete independent `REVIEW-PWE-R1.md`. I inspected the easy, hard,
completion, and variance-price source proofs in
`research-20260928b/bb-complexity/sparse-regression/phase-transition.md`
and `stronger-relaxations/thresholds.md` without changing those sources.

An additional independent supporting reviewer checked the actual completed
local-hull, completion, local-lift easy, hard-helper, saturation, and
variance-price proofs. That reviewer found no mathematical gap in its
assigned scope at appendix hash `0a396fa...fd0d05`. I independently checked
all statements and proofs in both files, including the remaining easy,
sample-size, conflict-code, optimum, and PWE arguments.

## Findings resolved in the completed manuscript

1. **Weighted pair completion needs a strict leverage condition.**
   `W` positive definite alone does not imply `q_max<1`; square helper
   matrices can have leverage one. The completion statement must require
   `q_max<1`, and the applications must supply quantitative bounds tending
   to zero to obtain vanishing objective inflation. The audited hard-side
   uniform event supplies `theta_U,q_max,U=O(n/p)`, so this is a repair to
   the lemma statement rather than an obstruction to the hard theorem.
   **Resolved:** `regression:completion` part (b), appendix line 469,
   explicitly requires `q_max<1`; `regression:uniform-hard-design` and
   its consequences at appendix line 818 establish uniform
   `theta_U,q_max=O(n/p)` before completion is applied.
2. **Include the forced-in coordinate in the completion set.** If the
   lemma requires `F` to contain `supp z`, a forced-in null coordinate
   belongs to `F` even when its coefficient is zero. Pad its covariance
   row and column by zero. This leaves the helper-independent covariance
   image unchanged. **Resolved:** `app:regression:lift-easy`, appendix
   line 642, sets `F=S union V' union {j}`, pads its covariance by zero,
   and explains why the covariance image is common to all nonexceptional
   forced-in indices in a half.
3. **Do not square a negative singular-value lower bound.** Use the
   positive part of `sqrt(m)-sqrt(n)-t`, or require that this expression
   be nonnegative before squaring it. Both intended asymptotic helper
   regimes satisfy this requirement eventually. **Resolved:**
   `regression:singular-tail`, appendix line 24, states the rule, and
   `app:regression:lift-easy`, appendix line 534, proves eventual
   positivity in the intended helper regime.
4. **Handle zero completion variance directly.** If `theta=0`, the
   helper cross covariance is zero and the covariance is block diagonal;
   positive definiteness of the helper covariance is unnecessary.
   **Resolved:** the proof of `regression:completion`, appendix line 507,
   treats a zero maximum in the helper scale by vanishing cross blocks.
5. **Retain the full richer-lift hypotheses.** The variance-price proof
   uses positive semidefiniteness on `(1,z,beta)`, complementarity, the
   off-diagonal product cones, and the binary-product inequalities.
   Positive semidefiniteness on `(1,beta)` and pairwise hull membership
   alone do not support that conclusion. **Resolved:**
   `regression:full-moment` retains these hypotheses, and the Gram proof
   in `app:regression:variance`, appendix line 871, explicitly uses the
   product constraints to eliminate zero-indicator helpers from the
   relevant projected coefficient vectors.

Two additional small clarifications were requested after the complete
proof review and are present in the final section hash. The definition of
`Top_t` at section line 156 sums the largest `min(t,N)` available entries,
so its node formula also covers feasible nodes with fewer free coordinates
than the remaining budget. The sample-size corollary at section line 226
uses each allowed deterministic ridge sequence, making the probability
quantifier precise. It also explicitly identifies the thresholds as
sample-size thresholds. The general model requires `1<=k<p`, so the
standalone null-correlation maximum is nonempty.

The source saturation proof is sound only after checking the residual
perturbation on selected and unselected columns as well as on the capped
violators. Conditioning on all scalar correlations before the spectral
selection, and then on the selected perpendicular components before the
unselected-column bound, correctly handles the data dependence.

## Statement and proof checks

| Statement or contract | Reviewed location | Disposition |
|---|---|---|
| Exact certificate at a specified support | `regression:exact-condition`, section line 68 | Pass. Convex first-order optimality gives the weak correlation inequality. Strict separation gives all wrong-node margins and then global support uniqueness. |
| C1 path bound and removal-only certificate | `regression:single`, section line 91; `lattice:path` dependency | Pass. The section supplies the exact surviving singleton value, the optimal-incumbent convention, and the strict best-bound variant. Removal-only C1 gives a separate `2k+1`-node certificate. |
| Saturated dual certificate | `regression:capped`, section line 134 | Pass. Completing the square gives its cost; top-correlation maximization gives the root and single-fixing bounds. The asymptotic proof controls all null and selected correlations, not only the capped ones. |
| Root planted-support thresholds | `regression:easy-thresholds` (a); `app:regression:easy`, appendix line 117 | Pass. Uniform coefficient/residual concentration and the conditional Gaussian maximum prove both sides. The negative side is stated relative to the planted fit. |
| Positive C1 threshold and strict quantitative margin | `regression:easy-thresholds` (b); appendix line 141 | Pass. The chosen cap yields `(2-o(1)) lambda b^2/log p`; the witness cost is lower order, so the displayed `lambda b^2/log p` margin follows. It proves global planted uniqueness. |
| Negative forced-in planted comparison | `regression:easy-thresholds` (c); `regression:forced-primal`, appendix line 238; proof at line 272 | Pass. The many-violator feasible point pays the budget cost, verifies individual weights and the budget, and proves the stated margin with the declared `5000/delta^2` support condition and exception count. |
| Sample-size thresholds and linear/inexact window | `regression:window`; `app:regression:sample-sizes`, appendix line 330 | Pass. The exact harmonic-mean identity gives `tau_lambda^2<n/k`. The deterministic ridge construction uses smaller fixed threshold slack, rather than promising the original slack at the boundary. The C1-positive/window argument proves planted global optimality before inferring global root inexactness. |
| Local hull validity and selected-block dominance | `app:regression:hull`, appendix line 369 | Pass. Recession, singleton, integer-generator, positive-semidefinite covariance, and epigraph arguments are complete. The support-distribution proof uses the integral cardinality polytope and its faces. |
| Local completion | `regression:completion`, appendix line 445 | Pass. Both general-order and weighted-pair completion prove all tested hull memberships, cancel design variance, and bound the additional ridge trace. Strict leverage and zero cases are explicit. |
| Easy thresholds for the selected stronger node bounds | `regression:lift-thresholds`; `app:regression:lift-easy`, appendix line 521 | Pass. The helper half remains independent of each constructed covariance image; leave-one-out conditioning controls individual helper rows. Forced-in support padding and the common covariance image give the stated uniform exception count and `20000/delta^2` condition. Positive tree bounds use perspective domination, so monotonicity of the stronger bound is unnecessary. |
| Pure-noise and low-total-SNR conflict packing | `regression:hard-theorem`; `app:regression:hard`, appendix line 666 | Pass. The integer optimum has its own all-support lower bound. Top-correlated features, the full greedy code bound, conditional perpendicular concentration, and the strict midpoint margin give the exponential packing. The planted construction uses null features disjoint from the true support. |
| Pairwise-hull hard conflicts | Same theorem; appendix line 812 onward | Pass. The uniform design event covers every union of at most `2k` columns, so data dependence causes no independence gap. It supplies small leverage and an `O(sqrt(n/p))` completion inflation before the strict midpoint margin is reused. Helpers survive zero fixings under the declared projected-root-lift convention. |
| Leaves and incumbent-removal node accounting | `regression:hard-theorem`; appendix line 855 onward | Pass. Each convex certified piece holds at most one code point. Terminal and removed pieces are charged separately; binaries give the stated `(p+1)` node denominator. |
| Richer moment-lift variance price | `regression:variance-price`; `app:regression:variance`, appendix line 871 | Pass. Gram projection, product cones, and the active-design minimum eigenvalue give the additional `(lambda+nu_A) pi` penalty. No sharp threshold or tree law is claimed for this lift. |
| Fixed-dimensional PWE discrepancy | `regression:pwe-theorem`; `app:regression:pwe`, appendix line 908 | Pass. Finite-dimensional support gaps prove unique global planted optimality. Conditional coefficient covariance and residual energy give the exact correlation ratio. The probability calculation precedes conditioning on optimality, and the final sandwich transfers it to global value exactness. |

The easy regime explicitly assumes fixed positive per-entry signal and
noise, `log^6 p<=n<=p`, `k<=C0 n/log p`, and
`sqrt(n)<=lambda<=n/log^2 p`. The hard regime instead uses `k/n->0`,
`lambda/n->0`, and fixed bounded total SNR. The section explains why these
signal regimes do not overlap. The local easy comparison additionally
requires `s n log p=o(p)`; the hard pairwise comparison retains its helper
columns. The statements do not imply unrestricted algorithmic hardness,
a lower bound from C1 failure alone, or a practical value of the
asymptotic packing exponent.

All PWE objectives use one common unnormalized loss and ridge
`lambda=sqrt(n)`. The exact KKT event is derived with weak inequalities,
and ties are then excluded conditionally. The null Gaussian calculation
uses conditional independence and does not claim independence of
unstandardized correlations with their shared random variance. The global
exactness limit is below one despite support recovery tending to one.
The comparison is confined to the printed Gaussian probability statement;
it does not reject the Boolean reformulation or propose an unproved
fixed-SNR or total-energy-noise repair.

## Attribution, reachability, and readability

The final section attributes Boolean exactness to PWE, the perspective
connection to Xie--Deng, safe-screening tests to Atamturk--Gomez, and
second-moment/rank-one strengthening to Dong--Chen--Linderoth and
Atamturk--Gomez using the literature owner's verified keys. The published
PWE statement has the precise Section 3.1, Theorem 2, page 72 locator.
This review did not conduct an independent literature search or make a
new novelty claim.

`main.tex` inputs both reviewed files. A targeted reference scan found
79 owned labels, no duplicated owned labels, and no unresolved owned
references. The only external chapter references are `lattice:path`,
`sec:lattice`, and `sec:experiments`; the path dependency was inspected.
All selected nonstandard mathematical claims are proved in the section or
its reachable appendix. Gaussian, chi-square, singular-value, and binomial
concentration are declared standard inputs; the extra truncated-tail
estimate is derived in the appendix.

The narrow 2026-10-06 check of appendix lines 1--35 passes; the supporting
independent reviewer also passed the same rescaling and citation check at
the current appendix hash. The chi-square
inequalities now cite Laurent--Massart, Lemma 1 and (4.3)--(4.4), page 1325.
The singular-value inequalities cite Davidson--Szarek, Theorem II.13,
page 353, together with item 5 of the 2003 corrigendum, page 1819.
All three keys are present in `references.bib` and were supplied as
verified by the literature owner. Multiplying an entry-variance-`1/d`
matrix by `sqrt(d)` gives the standard Gaussian matrix used in the
display. The normalized threshold `t/sqrt(d)` becomes `t`, and its
exponent becomes `t^2/2`, as required. The warning about squaring a
singular-value lower bound only when nonnegative is preserved.

The section separates model, certificate types, easy thresholds, stronger
lifts, hard regimes, richer moments, and the finite-dimensional check in
a readable order. It states the main limitations at the relevant claims.
No conjecture or heuristic from the source notes is presented as a proved
manuscript result. No concrete readability issue remains.

## Targeted verification

Performed read-only `cat`, `rg`, `sed -n`, `nl -ba`, `wc -l`, and
`sha256sum` inspection of the assigned manuscript and mathematical
evidence. The targeted commands included:

```text
cat sections/regression.tex
sed -n '1,340p' appendices/regression-proofs.tex
sed -n '327,706p' appendices/regression-proofs.tex
sed -n '700,1010p' appendices/regression-proofs.tex
rg -n 'regression|appendix' main.tex
rg -n -C 7 'lattice:path' sections/lattice.tex
sha256sum sections/regression.tex appendices/regression-proofs.tex
```

A short read-only Python scan of these two TeX files collected labels and
references and reported no duplicate or unresolved owned labels. These
were targeted manuscript checks, not CI checks. `apply_patch` wrote only
this report. No literature search, experiment, project-wide verification,
CI query, TeX build, or manuscript edit was performed.

For the citation-only refresh, targeted commands were
`sed -n '1,40p' appendices/regression-proofs.tex`, citation-key `rg`
inspection of `references.bib`, and `sha256sum` of the reviewed files.
A read-only Python check removed the two exact citation insertions in
memory and recovered the original fully reviewed appendix hash. It
reported seven added lines and no other change. No new literature
research, experiment, build, CI query, or mathematical verification
outside this citation scope was performed.
