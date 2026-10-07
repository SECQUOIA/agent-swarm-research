# Regression author source, proof, and contribution map

Date: 2026-10-05. Assigned files: sections/regression.tex,
appendices/regression-proofs.tex, and this report. Sol authorship follows
the root's explicit user-authorized fallback after the Claude usage limit.
No experiment was rerun; no literature search, CI inspection, project-wide
check, or change outside these three files was performed.

The selected manuscript results are complete. Independent final mathematical
review checked the actual section and appendix and found no substantive
gap. Root performs integration and standalone LaTeX compilation.

## Governing evidence incorporated

I read BRIEF.md, AUTHORING-CONVENTIONS.md, ARCHITECTURE-DECISION.md,
INCOMING-AUDITS.md, ISSUES.md, the regression parts of AUDIT-DISCRETE.md,
the architecture's regression source map and superseded exclusion, and the
complete REVIEW-PWE-R1.md. The root decision supersedes the architecture's
old proposal to omit stronger sparse lifts.

The final chapter incorporates DEC-1/DEC-2: negative root and forced-in
results compare with the planted-support value; the hard pairwise-hull
theorem fixes the projected root lift and retains zero-fixed helper
columns. It incorporates the complete hard-side development in
AUDIT-DISCRETE.md, lines 233–290, rather than the original proof sketch.

Before handoff I reread INCOMING-AUDITS.md, ISSUES.md,
LITERATURE-KEYS.md, the regression audit source map and normalization
sections, and the independently verified PWE statement and proof.
LITERATURE.md was not yet present when checked. Literature remains owned
by the Luna lead. The stable-key map and root's verified comparator
messages supply all literature claims used here.

## Source-to-manuscript map

Paths below are relative to the repository root. PT denotes
research-20260928b/bb-complexity/sparse-regression/phase-transition.md;
SR denotes the adjacent stronger-relaxations/thresholds.md.

| Manuscript result | Source and independent evidence | Complete manuscript proof |
|---|---|---|
| Perspective and dual identities | PT Section 1.2; PWE Boolean formulation; Xie–Deng perspective connection | regression:primal, regression:dual, completing-square explanation |
| Exact planted-support condition | PT Corollary 2.4; PWE Corollary 2; REVIEW-PWE-R1 weak-inequality KKT argument | regression:exact-condition, section proof |
| C1 path application and removal-only certificate | PT Lemmas 1.2–1.3; generic path proof owned by lattice author | regression:c1 invokes lattice:path and supplies the integer-tight singleton identity; removal-only proof is in section |
| Capped residual certificate | PT Lemmas 2.1–2.2 and Proposition 2.3 | regression:capped, section proof |
| Uniform coefficient and residual estimates | PT Lemmas 3.6–3.7 and Section 3.3 Step 1 | regression:fit-concentration; app:regression:tools |
| Root and single-variable thresholds | PT Theorems 3.1–3.2, Sections 3.3–3.4; sparse easy review/recheck; AUDIT-DISCRETE | regression:easy-thresholds; app:regression:easy; auxiliary regression:forced-primal |
| Optimized ridge and linear-tree/root-inexact window | PT Corollary 3.3 and end of Section 3.4 | regression:window; app:regression:sample-sizes |
| Fixed square-root ridge obstruction | PT Corollary 3.4, exact bound tau<=b/sigma | Paragraph after regression:window, with proof from the definitions |
| Local hull order, validity, selected block dominance | SR Lemmas 1.2–1.4 | regression:local-lift; app:regression:hull; regression:mixture |
| Deterministic local-hull completion | SR Lemma 4.1 with explicit qmax<1 and zero-C case | regression:completion; app:regression:completion |
| Local lift thresholds unchanged in stated aspect-ratio regime | SR Lemmas 4.2–4.3 and Theorem 4.4; stronger-relaxations review/recheck | regression:lift-thresholds; app:regression:lift-easy |
| Perspective hard conflicts | PT Lemmas 4.1–4.2 and Theorems 4.3–4.4; sparse hard review/recheck | regression:hard-theorem; regression:opt-lower; app:regression:hard |
| Pairwise-hull hard conflicts with retained helpers | SR Corollary 4.6 source sketch completed by AUDIT-DISCRETE lines 233–290 | Same theorem/appendix; simultaneous event regression:uniform-hard-design and uniform theta/qmax bounds |
| Richer moment matrix variance price | SR Definition 5.0 and Proposition 5.1; stronger-relaxations recheck scope correction | regression:variance-price; app:regression:variance |
| Fixed-dimensional PWE discrepancy | PT Remark 3.5; research-20260928b/reviews/pwe-verification.md; complete REVIEW-PWE-R1.md | regression:pwe-theorem; app:regression:pwe, including support uniqueness, conditional probability, and transfer to global exactness |

Older reviews inspected include research-20260928b/reviews/
sparse-easy-review.md, sparse-hard-review.md, sparse-recheck.md,
stronger-relaxations-review.md, and stronger-relaxations-recheck.md.
Their archived computations are not reported as new verification.

## Exact hypotheses and quantified conclusions

- Easy regime: standard Gaussian design, deterministic support/signs, fixed
  positive per-coefficient magnitude b and per-entry noise standard deviation
  sigma; unnormalized squared loss plus lambda times squared coefficient norm;
  log^6 p <= n <= p, k <= C0 n/log p, sqrt n <= lambda <= n/log^2 p.
- For each allowed deterministic ridge sequence, the root planted-support
  comparison changes at tau_lambda^2 = 2 log p with fixed constant slack.
  The C1 planted comparison changes at 2 log(p lambda/n); the negative
  single-variable result uses k >= 5000/delta^2.
- Positive C1 proves planted uniqueness. Thus k=p^{gamma+o(1)},
  n=a k log p, 2-gamma<a<2 gives a globally inexact root and <=2p+1
  variable nodes under an optimal incumbent or strict-C1 best-bound search.
  It does not give a rule-independent large-tree result below that window.
- Local lift easy comparison requires s n log p=o(p), validity, lower
  domination by perspective at every node, and upper domination by L_s only
  at the root and forced-in nodes. Its converse uses k>=20000/delta^2
  and at most 2n/log^2 p exceptions. Zero-column deletion is compatible
  with that easy theorem if these comparisons hold.
- Hard regime: k->infinity, k/n->0, lambda/n->0,
  (2/n)log binomial(p,k)->x in (0,x0), where x0 is the positive root
  of exp(-x)(1+2x)=1. Pure noise means y independent of X and nonzero
  almost surely. The planted extension needs bounded total signal-to-noise
  ratio kappa<exp(-x)(1+2x)-1, not fixed per-coefficient SNR.
- Hard conclusion: a midpoint clique of size exp(c k log(p/k)) =
  binomial(p,k)^{c+o(1)}; at least that many leaves for all convex-piece
  certificates under the fixed projected perspective or retained-column
  pairwise lift, with epsilon below a fixed positive fraction of the
  response-energy scale. Charged binary incumbent removals give at least
  clique/(p+1) nodes. This node inequality can be weak when division by p
  consumes the exponent.
- PWE comparison: fixed 1<=k<d, fixed nonzero planted coefficients and
  sigma>0, n->infinity, lambda=sqrt n, iid per-entry variance sigma^2.
  Unique planted support holds with probability tending to one, while global
  value exactness tends to [1-2 PhiBar(bmin/sigma)]^{d-k}<1.
  The sample-size requirement in the printed Theorem 2 holds eventually,
  whereas its printed exponential probability bound tends to one.

## Repairs and contribution boundaries

The chapter proves certificate distinctions and selected-lift comparisons
without claiming a universal complexity barrier. It credits the Boolean
formulation and deterministic certificate to PWE, the perspective
connection to Xie–Deng, safe dual fixing rules to Atamtürk–Gómez, and
antecedent second-moment/rank-one convexification to Dong–Chen–Linderoth
and Atamtürk–Gómez. The audited primary comparators do not establish
these B&B certificate-complexity thresholds. The hard proof uses the
existing conflict mechanism from the lattice chapter, not a newly
claimed generic midpoint argument.

Material author repairs:

1. Source sample-size statements say a ridge “meets (a)” with the same
   slack. That literal reading fails because tau^2<n/k. The manuscript
   promises the positive conclusion and invokes a smaller fixed slack.
2. Weighted pairwise completion assumes qmax<1. Positive definiteness
   alone is insufficient when the helper matrix is square.
3. General completion treats zero C as a diagonal PSD case instead of
   invoking a positive definite helper block with zero variance.
4. Squared singular-value lower bounds have their needed positivity
   stated before squaring.
5. Forced-in lift points include the zero-coefficient forced coordinate
   j in F, with its covariance row padded by zero. The helper-independent
   Y matrix remains common to all nonexception j.
6. The hard lift theorem proves uniform completion over all unions of
   at most 2k features, including maximal column norm and leverage.
   It does not assume selected-support independence.
7. The PWE proof calculates exactness at the planted support before
   conditioning on optimality, then transfers by a vanishing-probability
   event. Unscaled null correlations are not claimed independent.
8. The C1 path invocation supplies integer-tight surviving singletons.
   Top_t is defined when fewer than t free coordinates remain.
9. Each ridge is a deterministic sequence; no adaptive or unstated
   simultaneous uniform-in-ridge conclusion is claimed.

The manuscript does not assert an unproved fixed-SNR repair of PWE,
a sharp total-energy-noise constant, invalidity of the Boolean
formulation, a general split-tree consequence from C1, practical
exponent constants, a threshold for the richer moment relaxation, or
unconditional recovery hardness. The deterministic block gadget is
owned by the lattice author and is not duplicated.

## Independent manuscript review

Read-only supporting agent regression_review checked source saturation,
constants, and retained-helper completion. It found the same-slack and
qmax omissions repaired above and no further material gap.

Root's independent final reviewer review_regression_final checked the
actual TeX, with a separate review_local_hull proof pass. Completion,
lift-easy, retained-helper hard uniformity, richer variance price, and
PWE limit were approved. Top_t and deterministic-ridge clarifications
were applied and the revised section reread. Final mathematical
approval is unconditional within the stated scope.
The final PASS report is REVIEW-MANUSCRIPT-REGRESSION-R1.md; it
records no unresolved mathematical or readability issue.

Reviewed section SHA-256:
abb0dd9920afe7fcfe466c766d4c38e2982bb4ff4dadcaa3c9776e047d600d09.
Reviewed appendix SHA-256:
0a396fa09ab8de93c6730f6066cef11e4c6b6eaf3842bf2ba81a2ce043fd0d05.

On 2026-10-06, root authorized a citation-only update to the
probability input paragraph. The Luna lead verified
laurentMassart2000ChiSquare, Lemma 1 and (4.3)–(4.4), p. 1325,
and davidsonSzarek2001LocalOperatorTheory, Theorem II.13, p. 353,
together with davidsonSzarek2003Corrigendum, item 5, p. 1819.
The appendix now cites these sources and states the rescaling from
entry variance 1/d to independent standard Gaussian entries.
Its equations, hypotheses, and proof steps did not change.
The section hash remains unchanged; the citation-updated appendix
hash is 759760aff46a9376db68a325f9207a642bd0c3d02b0957d404c2db59fc8274a9.
A narrow-read and review-hash refresh was requested from the same
independent final reviewer.

## Targeted local commands and results

Read-only work used cat, sed -n, rg, rg --files, and wc -l on the
assigned source families and project evidence. Exact targeted reads
included:

    cat ../AGENTS.md evidence/BRIEF.md evidence/AUTHORING-CONVENTIONS.md evidence/ARCHITECTURE-DECISION.md evidence/INCOMING-AUDITS.md evidence/ISSUES.md evidence/AUDIT-DISCRETE.md evidence/REVIEW-PWE-R1.md
    sed -n '233,331p' evidence/AUDIT-DISCRETE.md
    sed -n '250,515p' phase-transition.md
    sed -n '636,901p' phase-transition.md
    sed -n '947,1245p' phase-transition.md
    sed -n '303,515p' stronger-relaxations/thresholds.md
    sed -n '516,578p' stronger-relaxations/thresholds.md
    rg -n 'xie|dongChen|atamturkGomez|laurent|davidson|gordon' references.bib evidence/LITERATURE-KEYS.md
    sha256sum sections/regression.tex appendices/regression-proofs.tex

apply_patch wrote only the assigned files. A targeted Python text scanner
checked both TeX files for unexpected control characters and single
terminal backslashes: neither was present after the first draft's
escaping repair. No numerical model, experiment, test suite,
project-wide build, or CI check was run. Root's integrated standalone
LaTeX build is separate from these mathematical and text checks.

## Concrete remaining integration requests

- Keep the section and appendix reachable from main.tex and preserve
  lattice:path, sec:lattice, and sec:experiments cross-references.
- Use the Luna lead's final bibliography records for the cited stable keys.
  In particular, Xie–Deng's preprint key contains 2018, while the
  inspected later primary manuscript is dated 2020.
- The standard probability attribution request is resolved by the
  2026-10-06 citation-only integration recorded above.
- Record the final independent review and root's targeted TeX build
  in the global coverage and review-resolution reports.
