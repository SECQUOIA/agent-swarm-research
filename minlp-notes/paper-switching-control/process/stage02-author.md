# Stage 2 author handoff

Status: draft complete; ready for the required five independent reviews. This
report is an author record, not stage acceptance. All changes are inside
`paper-switching-control/`. Accepted stage 1 proofs were not rewritten.

## Manuscript changes

- `sections/03-heavy-and-reach.tex`: integral prefix flow with an enforced
  repetition; complete first-repeat deadline reordering; extension/truncation;
  the universal heavy-mode theorem; the exact full-to-one-sided minimax reduction;
  analytic one-, two-, and three-distinct-block reach proofs.
- `sections/04-four-block-certificates.tex`: complete necessary-event LP; explicit
  symmetry types and variable orbit construction; affine multiplicity/topology
  proof; finite and symbolic integer dual certificates; analytic passage from the
  weighted pair inequality to the four-distinct-block theorem.
- `sections/05-small-budget-minimax.tex`: common exact one-sided and full minimax
  theorems through four blocks; exact equal-terminal-mass minimax, including its
  stronger small-mode conclusions; exact two-/three-switch transitions and
  asymptotics; three structural counterexamples.
- `main.tex`: includes those three new files. The main abstract remains a stage 1
  abstract as planned; stage 6 is responsible for the integrated abstract and
  introduction. The current build has 20 pages.
- `README.md` and `verification/reference/README.md`: current stage status,
  reproducibility instructions, proof dependencies and optional checks.

## Claims and coverage locators

| Repository development | Manuscript disposition |
| --- | --- |
| Universal heavy-mode theorem | `thm:heavy`, `lem:prefix-repeat`, `lem:first-repeat`; proof covers all n and all s, strict heavy threshold, plateaus, arbitrary measurable inputs, and shortened horizons |
| Exact one-sided reduction | `thm:one-sided-reduction`, equation `eq:one-sided-reduction`, for every 1<=k<n, repeated modes allowed |
| Analytic two-distinct-block reach | `lem:reach-two`, including the one-block base |
| Analytic three-distinct-block reach | `thm:reach-three`, including both first-reach inequalities, the excluded-pair aggregate, and strict latest-endpoint contradiction |
| Two-switch full minimax | `thm:small-full`, equation `eq:two-switch-exact`, n>=4 |
| Earlier two-switch equal-mass result | `cor:equal-masses`; retained as a genuinely stronger restricted-class conclusion at n=5,6,7, and extended in the same proof to all established reach counts |
| General four-distinct-block reach | `thm:reach-four`, `lem:weighted-pair`; complete event constraints `eq:event-mass`–`eq:event-equal-P`; exhaustive ten-type table; complete finite/symbolic certificate logic |
| Three-switch full minimax | `thm:small-full`, equation `eq:three-switch-exact`, n>=5; explicitly computer-assisted |
| Plateau transitions and expansions | `sec:small-minimax`, subsection 6.1 in this draft, including exact shifted sign polynomials |
| n=4 three-block certificates | Explicitly subsumed by analytic `thm:reach-three`, with frozen optional verifier and all 30 certificates |
| n=5 four-block certificates | Explicitly subsumed by `thm:reach-four`, with frozen optional verifier and all 360 certificates |
| n=3,k=3 distinct-reach failure | `prop:three-mode-failure`, full rational knot table and all six inverse compositions; strengthened to the true one-sided instance optimum as described below |
| Arbitrary prescribed heavy adjacent pair is false | Section 7.2: exact rate table, all three positions excluded, valid existential witnesses |
| Prescribed pair position at first integer mass-one prefix is false | Section 7.3: exact rate table, terminal-prefix contradiction and valid alternative witness |

Stage 3 owns the all-light lemma, predecessor upper bounds, general/seeded bounds,
and higher-block investigations. This stage does not state any unproved higher-k
formula as a theorem.

## New development and critical verification

The parent identified a possible strengthening of the three-mode counterexample.
I independently derived and verified it, and included the complete proof in
`prop:three-mode-failure`. At horizon 57/8 its terminal masses are
(5281,3985,3217)/1752. The support inequality for an error-one schedule excludes
omission of either mode 0 or mode 1. Thus any repeated-mode competitor with at
most three blocks must be 010 or 101, allowing zero-length padding. For a word
p,q,p with endpoints u,v, the proof establishes the necessary middle-service
bound

`v-u <= A_q(v)+1 <= A_q(M_2)+1 = M_2-R_p`.

The final occupation of p requires strictly more service to q: the respective
exact gaps are 781/876 and 1057/876. Together with the six distinct-word failures
this excludes all schedules at error one. Attainment gives an optimum strictly
greater than one. A direct uniform geometric schedule and the block-end recurrence
prove that the uniform input's one-sided optimum is exactly one even though the
stage 1 full-uniform theorem has a smaller stated k-range.

This is stronger than the source note: the spare-mode boundary matters for the
actual one-sided minimax, not merely for a distinct-mode construction. No exact
value of G^-_{3,3} is asserted. Reviewers should scrutinize this new argument.

I also replaced the separate equal-mass construction by a common corollary of
the proved reach counts and the automatic positive discrepancy bound T/n. This
derives the new four-block equal-mass conclusion while preserving the earlier
two-switch result's sharper small-n guarantee. It does not rely on the universal
heavy theorem.

The largest-heavy-mode adjacent-pair conjecture remains explicitly unused. The
repository investigated it using finite rational/flow searches and a numerical
cutting-plane experiment, but none of those finite observations proves it. The
existential heavy theorem is fully proved and supplies every subsequent result;
requiring the repeated mode to be largest is unnecessary. This stage retains
the conjecture only to distinguish it accurately from the two refuted stronger
shortcuts. No theorem, certificate, or algorithm in this stage depends on it.

## Bundled computational proof

Ten original files were copied unchanged to `verification/reference/`, including
the all-dimension verifier and 179 finite/10 polynomial certificate data, both
optional special-case proof packages, the original distinct-word counterexample
checker, and the heavy-flow/DP checks. The manifest records their original
repository-relative paths and SHA-256 digests. The two pre-existing stage 1
artifacts remain unchanged. Execution reads no original repository file.

The paper explains the relaxation only in the necessary direction. It explicitly
does not infer physical cumulative trajectories from its partially ordered event
variables. It explains why every symmetry type is covered, why the quotient
preserves the objective under averaging, why coefficients are affine or cubic,
why signs reverse in the dual inequality, and why the finite checks plus
polynomial identities prove every n>=5. Numerical discovery is not trusted.

## Verification performed

Run `python verification/stage02/run_checks.py` from the paper directory.
The runner verifies all bundled hashes and writes individual logs. All checks
passed using the standard library and exact arithmetic:

- 179 finite and 10 polynomial four-block certificates.
- 30 optional n=4 event-order certificates.
- 360 optional n=5 weighted-pair certificates.
- Original n=3 rational knot and all six distinct-word compositions.
- Universal heavy construction on 1,612 exact inputs: 909 already adjacent and
  703 requiring first-repeat reordering.
- Independent DP heavy audit on 1,415 inputs, including equality and plateau cases.
- `check_new_results.py`: independent exact polygon feasibility over all 27
  padded three-block words and 972 switching-time cells, ruling out error one
  for the strengthened n=3 counterexample without a greedy repeated-mode
  assumption. Every cell is a bounded closed polygon; all pairwise constraint
  intersections are tested using rational arithmetic, including degenerate
  point/segment possibilities. Also checks support/middle-service arithmetic,
  exhaustive words in both prescribed-adjacent-pair counterexamples, aggregate
  substitutions, plateau values, equal-mass refinements, and asymptotic coefficient
  convolutions.
- `check_symbolic_quotient.py`: checks all ten symbolic quotient matrices and
  objectives against direct finite quotients at n=11,23,37, away from the n=9,10
  affine reconstruction. This supplements rather than replaces the mathematical
  topology argument.

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded. The final
log has no warnings, overfull or underfull boxes, undefined references, or errors.
Rendered pages 15 and 18 were visually inspected; the certificate formulas,
paths, and theorem statement fit the text area. Build and verification
logs are in `verification/stage02/`.

Limitations: finite construction tests do not prove universal analytic claims;
the written proofs do. The four-block weighted inequality remains an explicitly
computer-assisted theorem with a frozen exact verification dependency. Broad
literature attribution and introduction integration remain assigned to stage 6.
