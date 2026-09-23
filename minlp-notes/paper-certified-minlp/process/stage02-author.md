# Stage 2 author report

Completed 2026-09-13. Authored the standalone soundness and implementation sections; no checker source, historical artifact, or unrelated paper folder was changed. The existing optional inputs in `main.tex` include both new sections without a main-file edit.

## Written artifacts

- `sections/03-soundness.tex`: propagation, support corrections, interval formulas, worked rounding example, full discrete inference invariant, incumbent-conditioned bound lifting, nonlinear extension, signed-objective transfer, and primal completion.
- `sections/04-implementation.tex`: artifact/API contract, exact expression interpretation, curvature and domain recognizers with proofs, interval replay, master identity, complete proof grammar and streaming, defects and repairs, producer/replay workflow, and trusted components.
- `references.bib`: added Grant–Boyd–Ye's DCP chapter, using the inspected author publication page. No new priority claim.
- `process/stage02-analytic-validation.py` and `.json`: exact symbolic/rational formula checks, bundled full replay, and current hashes.
- `process/stage02-author-build.log`: full clean build transcript.

## Theorem map

| Label | Mathematical assertion | Necessary premises/limits |
|---|---|---|
| `lem:propagation` | Rational row-based propagation and integer endpoint rounding preserve every original mixed-integer feasible point. | Finite useful rest bounds; no fixed-point or convergence requirement. Empty boxes are rejected by the finite-bound API. |
| `thm:safecut` | A support vector and finite box corrections imply a rational affine underestimator. | Genuine finite supporting vector; not convexity plus arbitrary finite boundary partials. |
| `cor:enclosure` | Rational gradient/value enclosures yield sufficient intercept tests. | Includes finite intervals, half-lines, free and fixed coordinates, all residual terms. |
| `ex:rounding` | Rounding a tangent slope can exclude a feasible point; corrected intercept restores safety. | All identities checked exactly; correction need not be the largest admissible intercept. |
| `prop:vipr-invariant` | Accepted asm/sol/lin/rnd/uns semantics preserve an incumbent-conditioned invariant with explicit assumption sets. | Actual feasible witnesses; integral forms for rounding/splits; correct signs and domination. |
| `thm:master-bound` | An assumption-free target gives an unconditional master bound. | Uses the best supplied witness to lift the cutoff-restricted proof; no optimum-attainment assumption. Infeasibility requires no solution witnesses. |
| `thm:transfer` | Objective-preserving extension transfers the master bound and original objective sense. | Exact master identity, valid cuts/bounds, correct constants; no Slater or attainment assumption. Mathematical infeasibility implication is not an implemented nonlinear infeasibility API. |
| `cor:primal` | Independent original-model feasibility and objective enclosure complete a gap or exact optimum proof. | Master incumbents and recorded primal references do not suffice. |
| `lem:quadratic-recognition` | Exact Schur elimination tests PSD; homogenized PSD proves square-root quadratic convexity. | Norm representation is an existence argument, not a rational factorization computed by the checker. |
| `lem:monomial-recognition` | Accepted monomial sign/exponent conditions imply convexity/concavity. | Positive domain, or stated continuous boundary extension; Hessian congruence and Schur-complement proof included. |

The one-variable linear-fractional rule and scalar composition rules are also justified explicitly. The first/second derivative formulas do not require an unsupported general ratio/perspective rule.

## Source audit and resolved distinctions

Read root-current-audit and current soundness/replay notes, independent semantics/proof/driver reviews, and all requested checker sources. Confirmed actual current behavior rather than extending historical prose:

- Restricted VIPR **subset**, not a logically complete proof system; complete supplied proofs and every suffix are checked.
- Any earlier assumption-free dominating derivation can establish the target. The original last-row restriction in the early review was superseded.
- Optional `global` metadata cannot discharge assumptions. Zero multipliers still require valid references but add no semantic dependencies.
- Exact master comparison admits positive row scaling and a bijective uniform transformed-name prefix. It does not recognize negative equality scaling or arbitrary row equivalence.
- The standalone proof kernel supports both senses and infeasibility; the MINLP interface exposes finite normalized minimization lower bounds only.
- The nonlinear-point contract includes every row variable; absent cut coefficients mean zero, with residuals still checked.
- Domain checks use declared bounds before cancellations; propagated affine bounds strengthen cuts later. General nonsmooth gradients and perspectives remain unsupported.
- Added the explicit segment-derivative bridge to support at boundaries. Finite coordinate one-sided derivatives are insufficient, illustrated by `-sqrt(x*y)` at the origin. Current symbolic quotient derivatives reject that point. The bridge remains an obligation of the trusted expression/differentiation implementation, not a claimed formal software theorem.
- Thirty-digit downward intercept shortening is described as a producer choice, with no guaranteed margin between evaluations. Acceptance requires exact comparison against the rechecked enclosure. Existing misleading heuristic comments were not treated as mathematical claims or used to justify acceptance; code bytes were preserved.
- Frozen hashing gives provenance/change detection, not protection against adversarial change-and-restore races. Stable files and trusted model execution remain explicit assumptions.

No new behavioral defect was found during this bounded audit. Thus no checker code repair or replacement of the frozen source was necessary. This is not a proof that no undiscovered executable defect exists.

## Validation and evidence

1. Full certification regression suite: `152 passed in 2.51s` using the solver-lab environment and `pytest -q certify/tests -p no:cacheprovider`.
2. Exact manuscript checks: rounding/exclusion identities, bounded and half-line corrections, one-variable fractional second derivative, and three-variable symbolic monomial Hessian identity all passed. The proof text supplies the general mathematical arguments.
3. Bundled quadratic replay passed: 11 nonlinear cuts, 39 derivations, exact lower bound `1/4`; the exact feasible point calculation matches. No external solver/checker used.
4. Clean isolated build in `build/stage02-author/` using latexmk/PDFLaTeX/BibTeX produced 21 pages for current sections 1–4 and bibliography. The final log contains no undefined citations/references, LaTeX warnings, overfull boxes, or underfull boxes. The isolated directory prevents use of stale root bibliography files.
5. Audited source hashes are recorded in `stage02-analytic-validation.json`; all seven requested checker files retain their prior bytes.

## Literature

Added the established DCP reference after checking the primary author page:
https://stanford.edu/~boyd/papers/disc_cvx_prog.html
Grant, Boyd, Ye, chapter in *Global Optimization: From Theory to Implementation*, 2006, pp.155–210. No claim rests on a secondary search result. Existing Wood/Cheung sources support the discrete semantics comparison; the paper provides its own standalone invariant for the actual restricted rules. No literature packages or original PDFs were changed.

## Remaining work outside this stage

Five independent Stage 2 reviews and their adjudication/corrections are required before acceptance. The later Lean stage must mechanize only precisely stated theorem coverage; experimental and supplement stages must supply their promised tables/artifacts. No large-proof campaign or new performance experiment was conducted here. No unresolved Stage 2 mathematical finding was identified that invalidates the scoped paper.
