# S5a author handoff: continuous design and convex performance

The author stage is complete and frozen for the required five independent reviews. This is an internal author verification record, not independent review acceptance or formal proof certification. No commit was made. Paper B was not edited or built. Root owns the completion plan and coverage map; neither was edited by this author.

## Scope and concrete coverage

Added `complexity/sections/08-design.tex` and its input before the current conclusion. The section integrates the eight promoted results through shared theorems, rather than repeating the quadratic, capacitated, and polynomial proofs. All statements below refer to labels in that new section.

| Promoted result | Complete manuscript treatment |
| --- | --- |
| `potential-flow-cactus-convex-design.md` | `thm:a-design-convex` and `cor:a-design-quadratic`: unrestricted-cycle convex minimization, rational surrogate box, exact parameter recovery, and accuracy-bit guarantee. |
| `potential-flow-cactus-capacitated-convex-design.md` | `thm:a-design-independent`, `thm:a-design-convex`, `cor:a-design-quadratic`: exact interval clipping, rational and irrational singletons, rational endpoint profiles, exact final capacities. |
| `potential-flow-convex-polynomial-design.md` | `lem:a-design-perspective`, `thm:a-design-convex`: dense growing-degree objectives, cube-only convexity promise, explicit global convex Lipschitz extension, rational value/subgradient oracle and bounds. |
| `potential-flow-cycle-polytope-resistance-design.md` | `thm:a-design-root`, `thm:a-design-independent`, `cor:a-design-quadratic`: arbitrary-dimensional H-polytopes within cycles; exact endpoints, rational optimizing profiles, capacity and design conclusions. |
| `potential-flow-correlated-polynomial-cycle-design.md` | `eq:a-design-law`, `eq:a-design-cycle`, `thm:a-design-independent`, `thm:a-design-convex`: passive existence, orientation reversal, shifted fixed partitions, growing dense degrees, rational interpolation, exact linear-objective scenarios. |
| `potential-flow-cactus-convex-performance-hardness.md` | `thm:a-design-maxcut`: maximum-degree-three bounded-data cube realization, unweighted Max-Cut identity, strong hardness, unit optimum gap, absolute-error-1/4 barrier, restricted NP/coNP membership. |
| `potential-flow-cactus-few-measurement-maximization.md` | `thm:a-design-measurements`, `cor:a-design-fixed-rank`: rational direction arrangement, algebraic lengths, exact original endpoint profiles, additive candidate comparison, finite quadratic sets, N^{O(k)} dependence. |
| `potential-flow-global-correlation-arc-validation.md` | `thm:a-design-global-capacity`: one exact capacity-feasibility LP under global correlations, robust LP validation and violating witnesses, exact individual arc extrema on the capacity-filtered polytope. |

The essential supporting note `monotone-polynomial-root-polytope-optimization.md` is proved in full as `thm:a-design-root`, including arbitrary parameter dimension, lower-dimensional polytopes, common Cramer denominator and height, squarefree-factor/discriminant separation, fixed rational piece partitions, equality and breakpoint roots, and final rational LP-vertex recovery. The proof uses no derivative lower bound, no enumeration of all vertices, and no common algebraic field across cycles. Dense degree and uniform monotonicity promises remain explicit.

## Mathematical development and resolutions

One strengthening needs explicit attention in all five reviews: `thm:a-design-measurements` extends the original quadratic fixed-measurement theorem to independent correlated polynomial-law cycle polytopes, including the permitted local capacities. The proof uses the already-established exact algebraic endpoints and rational endpoint profiles; measurement directions remain rational, and separate dense-degree root refinement supplies the additive comparison. The finite-set clause remains the established quadratic, unfiltered model. It does not claim finite-law generality or a finite-set capacity-filtered convex hull.

The design proof uses stored exact constrained endpoint profiles in every model. This unifies the earlier freezing constructions and gives the 2mη projection plus mη recovery bound and loss at most 11ε/16. This is a common implementation of mechanisms already present in the corpus, not a separate algorithmic paradigm.

Root identified one minor statement omission during drafting: the independent linear-objective and fixed-measurement outputs needed to say that infeasibility is decided before a scenario is returned. Both theorem statements and the measurement proof now say so. Root caught a sentence splice introduced by that repair; it was corrected and the manuscript rebuilt. Author self-check restricted the linear-fractional predecessor sentence to the single-piece degree-one case. Three first-build overfull lines were corrected. Root also identified an ambiguity in the new diagnostic: its infeasible global example described a second physical capacity without explicitly defining that second cycle law. The checker now constructs that inequality from a separate passive polynomial balance with alternate coefficient sum 1+gamma and direct coefficient 1+alpha; the changed check was rerun successfully. No mathematical defect in the promoted results was found, and no change to accepted sections 01–07 was needed.

All distinctions are retained: exact local extrema versus exact scalar sums; rational parameter profiles versus possibly irrational flows; exact capacity recovery versus surrogate feasibility; independence within the design theorem versus a globally correlated capacity LP; convex minimization versus maximization; finite maximization versus finite target realization. No validation of general correlated passivity or polynomial convexity is asserted. Moving breakpoints, sparse binary exponents, uncertain nominations, potential constraints, and coupled cross-cycle flow constraints remain outside the design theorem. No energy/global-total-flow hardness, shared-cycle counterexample, or sharp rounding result is duplicated from the next planned stage.

## Source evidence and contribution scope

Read the result statements, their corresponding notes/reviews, the abstract root note and both reviews (including the piecewise addendum), and the root, cactus geometry, convex performance, and global correlation source assessments. Inspected the relevant diagnostic code before running it. Prior review acceptance was treated as guidance, not as a substitute for the present proofs.

Primary passages inspected directly during this author stage:

- Aßmann–Liers–Stingl–Vera, local original PDF pages 20–22, Proposition 4.9, Lemma 4.10 and Proposition 4.11: scalar quadratic cycle balance, interval halfspaces, and preservation of polyhedral uncertainty. The section gives explicit prior credit for capacity linearization and treats conjunction across cactus cycles as a direct extension. [Primary preprint](https://arxiv.org/pdf/1808.10241).
- Onn–Rothblum, local original PDF pages 4–6, Lemmas 2.1–2.3, Algorithm 2.5 and Theorem 2.6: vertex count, exposing directions, normal-fan refinement and reduction to linear optimization. Its rational-data geometric mechanism is explicitly credited. [Primary preprint](https://arxiv.org/pdf/math/0309083).
- Agrawal–Boyd, Sections 2.1 and 3: quasiconvex/quasiconcave level sets and feasibility bisection. This supplies classical context, not the claimed exact vertex recovery theorem. [Author copy](https://web.stanford.edu/~boyd/papers/pdf/dqcp.pdf).
- Megiddo, Section 2 theorem and parametric comparison argument: exact affine-ratio optimization using bounded additions/comparisons. The manuscript gives predecessor credit, without silently applying that operation model to a general bit-polynomial LP algorithm. [Author copy](https://theory.stanford.edu/~megiddo/pdf/rational.pdf).
- Mignotte's integer-factor inequality was checked directly as Theorem 1.2 of Nahshon–Shpilka's primary research article, where it is explicitly attributed to Mignotte 1974, Theorem 2. The original 1974 proof was not retrieved/read in this stage. The manuscript attributes the bound to Mignotte and derives the conservative separation estimate explicitly. [Inspected theorem](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD).
- Dadush, Theorem 2.5.9 (printed page 48) and Section 2.5.1: global Lipschitz convex value oracle, centered body, rational feasible output and input encoding convention. [Primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf).
- Boyd–Vandenberghe, Sections 3.2.5–3.2.6 (printed pages 87–89): partial minimization and perspective convexity. The explicit extension/oracle calculation is proved here. [Primary textbook](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf).

Ferrez–Fukuda–Liebling 2005 receives scope-level predecessor credit for fixed-rank convex binary quadratic maximization by zonotopes, with no detailed theorem locator. The previous bounded assessment inspected its primary publisher abstract and indexed introduction; this stage's publisher full-text request failed. Root separately confirmed author-publication metadata. The complete geometric argument is supported by directly inspected Onn–Rothblum and is also proved in the section. No unrestricted priority claim is made for any network-specific combination. The old unread Hasler–Wang nonlinear tolerance source remains a priority gap already recorded in the repository; nothing here asserts it has been cleared.

Six bibliography entries were added: Agrawal–Boyd, Megiddo, Mignotte, Boyd–Vandenberghe, Onn–Rothblum, Ferrez–Fukuda–Liebling. Existing Aßmann, Dadush, BPR, and Del Pia–Dey–Molinaro keys are reused. Contemporary conductance/infrastructure network-design results are not conflated with these fixed-hardware parameter/performance formulations; detailed manuscript-wide comparison remains part of the framing stage.

## Reproducible verification

`completion-s5a-checks.json` retains all nine command lines, script hashes, exit codes, full stdout/stderr, runtimes, and limitations. All passed under `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`:

- Convex design: 12 coupled numerical QPs, 24 exact rational cycle recoveries, six narrow frozen cycles; largest observed reference loss 1.6074184507886002e-6 at requested 1e-3.
- Capacity recovery: 403 exact cases, 229 feasible and 174 infeasible, 227 retained rational recoveries and two frozen endpoints, including singleton cases.
- Cycle-polytope roots: 32 polytopes, 254 enumerated diagnostic vertices, 6,314 exact bisection steps.
- Correlated polynomial laws: 72 exact root brackets, 216 zero/hinge controls, 215 rational target recoveries, degrees 1–7.
- Convex polynomial extension: 1,600 exact Jensen/Lipschitz/agreement checks and 5,580 exact support inequalities including boundary ties.
- Max-Cut hardware: 5,184 exact states over all 64 four-vertex comparison graphs.
- Historical measurement check: 18 projected quartics, 286 cones versus 1,512 exhaustive endpoint scenarios, using numerical LP and 70-digit values.
- New `verification/check_s5a_design.py`: eight exact rational sign cones versus 64 polynomial endpoint scenarios, six rational capacity clips, degrees 3–9, repeated/zero measurement directions, an irrational singleton with rational original profile, and exact feasible/infeasible globally shared parameter capacity LPs. Candidate comparison uses separate exact root brackets and an explicit objective error bound, not high-precision floating point or a common algebraic field.

The numerical QP and historical measurement comparisons are diagnostics, not implementations of the certified general convex oracle or exact arrangement algorithm. The vertex-enumerating root diagnostic is deliberately a small independent oracle, not the theorem's algorithm. The new test uses exact SymPy rational simplex LP on small cases; it is not a complete implementation of the general monotone-root theorem. Universal statements rest on the supplied proofs and cited classical tools.

Paper A alone was built by importing `verification/build_and_check.py` and calling `build('complexity')`; its CLI was not used. The final build has zero LaTeX errors, undefined references, undefined citations, duplicate labels, and overfull boxes. The full 15-input manifest is in `completion-s5a-build.json`; every hash was compared to the current file. Compared with the accepted S4b manifest, only main.tex and references.bib changed among existing inputs, and the new 08-design.tex is the fifteenth input. Sections 01–07 and all other accepted build inputs remain byte-for-byte unchanged. The resulting Paper A PDF has 142 pages; final reading-order/appendix decisions belong to the scheduled framing stage.

## Frozen inputs

Freeze time: 2026-09-10T09:07:01.903879+00:00

- `complexity/sections/08-design.tex`: `85ea7d7942ab63a9a94d4a91dd10b9e3b30b736982a4f58c6a2af52007807295`
- `complexity/main.tex`: `bffb0b29aded280f656511e1410966d531bca6ad1c08aab40900a76f6bbc77fa`
- `complexity/references.bib`: `f85cadccd793c884f9895d875710945130a7929d6a3e5e1df24f88aed83f9c5a`
- `verification/check_s5a_design.py`: `be1dbd6726761425f19f6658de9ba09a4c7439a8b442b5fc707dbbb5bcd388b5`
- `process/completion-s5a-build.json`: `d86423e71725ea52eb0ce50c4998ff12d9a4bcd2b57482d1bcb1a2b074185fef`
- `process/completion-s5a-checks.json`: `315268e7889bbd008d46b40718a1a973e7775ff005828c7a040abcbb88552bf4`

No further author edits will be made to the frozen manuscript or diagnostic before the five-reviewer handoff.
