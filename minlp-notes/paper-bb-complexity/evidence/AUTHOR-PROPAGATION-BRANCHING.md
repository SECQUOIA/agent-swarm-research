# Propagation and branching author report

Saved 2026-10-05. Owned files are `sections/propagation.tex`,
`sections/branching.tex`, `appendices/propagation-proofs.tex`, and
`appendices/branching-proofs.tex`. All selected nonstandard results have
complete proofs in these submission files. This report is internal evidence,
not a submission dependency.

## Decisions and audit versions incorporated

I read BRIEF, AUTHORING-CONVENTIONS, ARCHITECTURE-DECISION, the full
AUDIT-BRANCHING, the propagation portion of AUDIT-SPATIAL, the relevant Opus
architecture entries, and REVIEW-SHARP-INDUCTION-R1 (dated 2026-10-05). I
reread INCOMING-AUDITS, ISSUES, the complete sharp-induction review, the
branching audit, and the latest LITERATURE-KEYS before completion. The key map
now includes `belottiCafieriLeeLiberti2012FBBT`; the reference is already in
the shared bibliography. A full LITERATURE.md was not present at the last
source check. Architecture-decision scope overrides the architecture's stale
one-sided dichotomy and its earlier exclusion of the completed induction.

The final independent propagation/branching reviewer inspected the saved
chapters while they were being completed. Its concrete findings were
incorporated: explicit fairness; the lower half of the -1 flat example;
positive local-exactness width and derivative radii; a neighborhood in N
for the CND logarithmic consequence; positive ND1 growth constants; a simple
exact three-piece certificate for the 11/5 example; correct information
quantifier order; the positive-budget/no-local-zero dependency in the phase
proof; precise fixed coordinate-wise selection in the induction; an explicit
sharp-coordinate example; and a proof that each smoothed objective is
nonanalytic. Final saved-file approval is recorded in
`REVIEW-MANUSCRIPT-PROPAGATION-BRANCHING-R1.md`: accepted within the stated
mathematical scope, with no remaining mathematical repair requests. A later
typesetting-only repair braces interval-first array cells so that a literal
`[` after a row break is not parsed as optional row spacing; the reviewer
was notified to refresh that appendix hash. Approval is the independent
reviewer's disposition, not inferred from this author report.

## Propagation claim and proof map

All source paths in the next table are under
`research-20260928b/bb-complexity/cutoff-propagation/cutoff-propagation.md`
unless stated otherwise.

| Manuscript label | Source result | Hypotheses and cost | Complete proof |
|---|---|---|---|
| `prop:fixed-point` | Lemmas 1.1–1.2, Proposition 1.4, HC4 partial-step repair | Finite continuous objective DAG; compact forward domains; exact elementary revises; fixed constants; fair exact or forward/backward schedule; strict closed-cutoff emptiness/removal | `app:propagation-fixed-point` |
| `prop:flat-formula` | Theorem 3.1 | Root children distinct; repeated references collected; continuous unary terms; variable bases for exact minimization formula; endpoint maxima, not full maxima | Main proof after theorem |
| `prop:one-sided` | Corollaries 3.3, 3.5, Proposition 3.6 | Sufficient one-sided intervals; lifted coordinate groups; at most one positive forward excess; exactness if exposed image equals its box | Main proof after corollary |
| `prop:local-exactness` | Theorem 3.8 | Unconstrained compact root; positive width threshold; local pi at least f-star; Lipschitz objective and quadratic upper bound error; fixed optimal incumbent; ideal empty-limit decision; nodes only | Main width-potential proof |
| Unconstrained `f_star+abs(f-f_star)` example | Proposition 2.3 plus spatial audit qualification | Encodes known answer; exact representation only where f at least f-star; no constrained-global representation claim | Main one-paragraph construction |
| `prop:witness` | Lemma 4.1, general DAG Remark 4.1a, Corollary 4.2 | Distinct root coordinates over arbitrary continuous DAG; single-use needed only for exact forward term ranges | Main lifted-range proof |
| `prop:cnd-transfer` | Lemma 4.4, Theorems 5.1–5.2; hybrid Lemma 2.1 repaired by ownership audit | Uniform coordinatewise no-dominance; local C2 bounds; objective-only inherited phases; minimum cutoff over full inheritance chain; disjoint half-open rectangular owners; event K, nodes only bounded phases/node | `app:propagation-transfer` |
| `prop:nd1` | Theorems 5.4–5.5 | Uniform aggregate derivative loss; quadratic remainder; arc fully transverse to every coordinate; or n at least 2 interior quadratic-growth minimum with small gradient; events rather than unrestricted node counts | `app:propagation-face-loss` |
| `prop:slow-rounds` | Proposition 3.9 | Expanded quadratic with distinct term nodes; specified forward/cutoff/backward schedule; fixed interval around positive a; lower bound on rounds, not schedules in general | `app:propagation-rounds` |
| `prop:fast-rounds` | Proposition 3.10 | Exposed u=t-squared endpoint; U0 upper bound on u in (0,1/2); specified schedule; double-log upper bound on rounds | `app:propagation-rounds` |

The CND covering formula defines its covering balls by radius, not diameter;
this accounts for the factor two relative to source notation. The arcsine
per-box constant and the event transfer are proved directly, without an
unstated dependency on another writer's label. The ND1 integral treats n=2
separately from negative-power estimates. None of these owner families is
declared a fully valid closed-box cover.

## Branching claim and proof map

Source abbreviations:

- CB: `research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md`.
- ND: `research-20260928b/bb-complexity/branching-competitiveness/n-dimensional.md`.
- SO: `research-20260928b/bb-complexity/branching-competitiveness/separable-omega.md`.
- RB: `research-20260928b/bb-complexity/robust-branching-points/robust-branching.md`.
- Review example: `research-20260928b/reviews/competitive-review.md` Section 2.4 and archived `competitive/rmin_11_5.log`.

| Manuscript label | Source result | Hypotheses and cost | Complete proof |
|---|---|---|---|
| `branching:four-competitive` | CB Theorem 1 and crossing lemmas; AUDIT-BRANCHING Section 2 | Continuous f; unconstrained 1D; exact fixed-alpha bound; positive epsilon; fixed optimal incumbent; any minimizer tie/history; root-valid case; one bound per node | Main crossing/counting proof |
| `branching:ratio-range` | CB two-piece refinement; review 11/5 example | Five-node two-piece upper; explicit 11/5 lower; supremum at most 4, not strictly below 4; not a sharp-global-constant claim | `app:branching-small-certificates` |
| `branching:germ-obstruction` | CB Theorem 3; audited completed smooth extension | Explicit nonanalytic class; convex underestimators; identical root and endpoint germs; for every rule one of two instances bad; deterministic 5/3 or expected randomized 4/3 | `app:branching-information` |
| Full node information greedy statement | CB full-information comparison, completed audit proof | Entire objective available; hereditary-valid intervals; counts selected certificate, not optimal-cut computation | Main greedy endpoint induction |
| `branching:persistent-clamp` | CB Proposition 4; audited restricted clamp family | Fixed lambda/theta symmetric clip map; fixed kink; exact oracle; logarithmic node count | Main relative-position orbit proof |
| `branching:recentring` | RB price-of-safety/recentring; audit Section 4 | Safety bound samplewise even randomized; worst kink can vary with epsilon; recentring theta at most 1/3; fixed-kink boundedness; optimal zero-tolerance hitting, not finite-tolerance optimality | `app:branching-safety` |
| `branching:separable-brackets` | SO Proposition 3.1 / ND separable brackets | Slice uses full epsilon; product uses allocated epsilon; N_rect versus N_tree separate | Main slice/product argument, with interval-cover conversion proved in induction appendix |
| `branching:dimension-obstruction` | SO Theorems C/C-prime; closing corrected deterministic average; audit Section 3 | Explicit n-labelled piecewise quadratic nonanalytic family; fixed epsilon 1/100; c=1/(5n); node-local rule; coordinate-wise minimizer selection; corner germs allowed; exponential dimension cost, not accuracy lower bound | `app:branching-dimension` |
| `branching:multi-separation` | ND Theorem N3 | x-squared on unit square; alpha=1; all-coordinate interior-minimizer multisection; processed boxes counted, comparator binary guillotine certificate | `app:branching-multi` |
| `branching:phase-lemma` | SO Lemma T / Theorem A | Fixed coordinate-wise selection; m nonnegative, no local zero necessary; positive b; integer kappa; separate N=1 case | `app:branching-sharp` |
| `branching:sharp-induction` | Completed AUDIT-BRANCHING induction, independently approved REVIEW-SHARP-INDUCTION-R1 | One arbitrary plus r sharp coordinates; original minima zero; fixed optimal incumbent; exact separable oracle; fixed selection satisfying sharpness or every sharp minimizer sharp; r-dependent constant; correct leaf-to-node conversion | `app:branching-sharp`, including frontier refinement inequality |

The eleven-node construction now uses the simple certificate
`[0,2/5],[2/5,3/5],[3/5,1]` rather than rational greedy breakpoints. Its
shifted minima are respectively `209/160000,0,209/160000`, so the manuscript
proof has no dependency on a greedy-computation script. The knot table and
five exact invalid-node values specify the objective and tree completely.

## Limits preserved in submission prose

- One-sidedness and local exactness are sufficient conditions; no exactness
  dichotomy is asserted for arbitrary DAGs.
- Propagation phases, revise rounds, event certificates, tree nodes, and
  bound evaluations are distinct. Arbitrarily many phases do not yield a
  generic node lower bound. Fixed-point exactness does not bound rounds.
- General bounded-round exponent claims remain open. ND1 does not establish
  the dimension-p rate for p at least 3.
- The 1D proof assumes no convexity of f. With a nonconvex underestimator,
  computing its exact minimum can be expensive; node counts omit that cost.
- Analytic germs and sibling-learning rules are outside the information
  lower bounds. The coordinate-ambiguity construction permits corner germs,
  not germs along entire facets.
- General omega competitiveness in fixed dimension at least 2, including
  general separable objectives, remains open. The phase lemma is not used
  for a general global phase sum or a deficit-rule claim.
- No unrestricted branching-tree localization is claimed; the separate
  decomposition writer owns the path comparison. Its unrestricted extension
  was disproved, as recorded by the audit.
- Historical software formulas/defaults, randomized clamp drift bounds,
  tolerance-dependent inexact-minimizer extensions, and the separate
  McCormick safe-selection model are not necessary premises of the selected
  exact-oracle chapter. No current software-default or practical-speedup
  statement is made.

## Literature and integration

Citations used are the verified-key scopes available at authoring:
`belottiCafieriLeeLiberti2012FBBT` for the established fixed-point viewpoint;
`schichlMarkotNeumaier2014ExclusionRegions` for objective cutoff/exclusion;
`duKearfott1994Cluster` and `wechsungSchaberBarton2014Cluster` for the
exact-bound absence-of-clustering mechanism. The main results have complete
manuscript proofs and no unsupported novelty language. Root was asked to
route any missing fixed-point/branching precedent queries through Luna; the
FBBT key is now available. Precise prior comparison for the competitive
framework belongs to the literature lead/root framing.

Concrete integration requests: include both owned appendix files as already
planned, run the integrated standalone LaTeX build, and keep the final review
disposition alongside this author report. No remaining mathematical premise
is intentionally left to an internal report.

## Targeted checks actually run

No experiment scripts, formal builds, project-wide verification, CI status,
or CI logs were run or inspected. Root owns integrated LaTeX compilation.
Source reads used `rg`, `sed`, and `cat`.

An independent small `python3 - <<'PY'` Fraction calculation directly
interpolated the printed eleven-node H table, evaluated its affine shifted
functions at all contained knots and endpoints, checked convex H slopes,
the simple three-piece certificate, the six terminal minimizer intervals,
and the five unique invalid minima. It exited zero and printed:

```text
three-piece value: 209/160000
three-piece value: 0
three-piece value: 209/160000
eleven-node example: all terminal intervals valid; convex H verified
invalid node: 0 1 -6/25 1/2
invalid node: 0 1/2 -2791/160000 3/16
invalid node: 3/16 1/2 -9/1600 7/16
invalid node: 1/2 1 -2791/160000 13/16
invalid node: 1/2 13/16 -9/1600 9/16
```

A second `python3 - <<'PY'` check read only the four owned TeX files and
checked unique labels, resolution of their own cref/eqref references, and
proper begin/end environment nesting. It exited zero:

```text
PASS: owned chapter labels, cross-references, and environment nesting; 50 labels; 41 references
```

These are new targeted identity/source checks, not reruns of archived
computational experiments. The independent final reviewer separately
reconstructed the mathematical proofs and controls its own final hashes.
After the integrated build reported the array optional-spacing parse, I ran
`rg -n '^\s*\['` on all four owned TeX files. It returned no literal-leading
bracket rows after the braces repair. Root controls the resumed LaTeX build.
