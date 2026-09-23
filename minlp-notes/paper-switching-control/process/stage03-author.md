# Stage 3 author handoff

Status: author draft complete and ready to freeze for five independent reviews.
This report does not accept the stage. No stage 4 work was undertaken.

The manuscript now has 32 pages. Stage 3 appears in Sections 8–10, on pages
21–32, through the new source files `sections/06-general-budgets.tex` and
`sections/07-predecessors-and-frontier.tex`. `main.tex` includes both files.
The accepted Sections 1–7 (source files 01–05), `macros.tex`, and
`references.bib` remain byte-identical to `stage02-accepted`. The abstract,
introduction, and final literature synthesis are left for stage 6 as assigned.

## Coverage and mathematical development

| Required topic | Manuscript locator and disposition |
| --- | --- |
| Mode removal for arbitrary measurable input | Lemma `lem:mode-removal` (Lemma 8.1), equations `eq:mode-removal`–`eq:removal-contract`: both largest- and smallest-mass choices, reciprocal equality, positive prefix error, the constant-mode branch, completed rates, and both one-sided error phases. The transform `eq:eta-transfer` retains negative values. |
| Elementary arbitrary-budget coefficient | Theorem `thm:general-coefficient` (8.2): full base and induction, including the zero transform at the final spare-mode boundary. |
| One-sided/equal-mass/full consequences and uniform lower bound | Corollary `cor:general-bounds` (8.3), with uniform lower coefficient `eq:uniform-lower-general`, and the accepted heavy reduction. |
| General exact plateau | Corollary `cor:general-plateau` (8.4), positive denominator and exact factorization `eq:plateau-factor`. The statement explicitly uses k>=2; k=1 and n=2 are separately identified. |
| Sharp first asymptotic correction | Proposition `prop:general-asymptotics` (8.5), including a derivation of both second-order bounding coefficients and the exactly vanishing k=1 gap. |
| General and four-block seeds | Theorem `thm:seeded` (8.6), with explicit positive-seed domain, unclipped transform, proof of strict improvement over the elementary coefficient, and retained four-block certificate dependency. |
| Seeded closed consequences | Corollary `cor:seed-consequences` (8.7): an integer plateau criterion, the n16/k5 exact full value, and negative-transform diagonals. The full equal-mass conclusion survives clipping; the strict one-sided improvement does not. |
| General seed asymptotic gap | Proposition `prop:seed-series` (8.8): full formula for every established seed ell<=4, with a short formal-series derivation. For ell4/k5 the coefficient is 2/5, half the elementary 4/5. No exact second-order general minimax claim is made. |
| All-light lemma and boundaries | Lemma `lem:all-light` (9.1) proves the capped greedy construction. Corollary `cor:light-boundaries` (9.2) treats n<=k through the automatically heavy case, with no sharpness claim there, and gives the k<n<=2k exact full plateau. |
| New equal-mass instance band | Corollary `cor:light-boundaries` (9.2) proves OPT_(k−1)(A)=T/n for **every** equal-mass input whenever (n−k)^2<=k. This is an instance identity, not merely a worst-case claim. It includes all deficits d=n−k once k>=d^2. |
| Dimension-free value | Proposition `prop:dimension-free` (9.3), with strict finite-mode upper bounds, limiting uniform lower witnesses, and explanation of the classical integral-prefix rounding route. Final external literature synthesis remains stage 6. |
| Certificate-free analytic four-block predecessor | Proposition `prop:analytic-four-upper` (9.4) derives the repository rational U_n from the analytic three-block seed, including the minimum-mass branch at n5. It proves exactly the n5–11 certificate-free plateau criterion and derives the asymptotic gap above the now-established exact value. |
| Third-largest-terminal-mass condition | Lemma `lem:third-mass` (9.5) has a shorter complete proof from the accepted two-block reach lemma. A concrete n8 terminal-mass class gives a guarantee strictly below the unrestricted minimax coefficient, so this information is not discarded as subsumed. The old global V_n is explicitly dominated. |
| Higher-order exclusion identity | Lemma `lem:general-exclusion` (10.1) derives the actual-event recurrence and clearly separates its unproved weighted premise. It specifies maximizing S, uncapped events, available-set sizes, and the exact implication to reach. |
| Negative relaxation witness | Subsection `subsec:negative-relaxation` (10.2) gives the complete constraint schema and the exact counts/objective. It checks the two incomparable events and their 4/645 mode2 decrease across a 184/645 increase in time. The assignment is explicitly nonphysical. The stronger all-S relaxation is distinguished from the sufficient maximizing-S premise. |
| Event interpolation | Lemma `lem:event-interpolation` (10.2) proves chronological coordinate monotonicity plus conservation is sufficient for a piecewise-affine admissible trajectory. It explicitly does not establish the inverse/max reach identities. |
| New chronological investigation | Proposition `prop:chronological-chamber` (10.3) proves an exact target bound in one fixed chronological chamber by a new rational dual and matching uniform primal. Scope is confined to that permutation and the specified pair/triple maximizers. |
| Adjacent-repeat frontier | Last paragraph of Section 10 distinguishes the unused largest-heavy-mode strengthening from the accepted existential theorem; accepted counterexamples remain in source05. |

The general seed expansion and the broader all-light equal-mass consequence were
also proposed independently by the primary agent during authoring. I checked
their algebra independently, supplied the manuscript proofs, and added exact
verification. No additional author or reviewer agent was spawned in this stage.

## Further reach investigation

The old six-mode witness satisfies 3660 inequalities, 64 equalities, and
nonnegativity for 454 variables, with objective 40328/387<13104/125. Its event
allocation data fail common-trajectory monotonicity. I sorted its 64 events by
time, breaking ties by the original event enumeration, and added 378 adjacent
coordinate-order inequalities. This fixes one weak chronological chamber; it
does not fix the old numerical times.

SciPy 1.18.0/HiGHS located a dual optimum for that chamber. After rationalization,
the standard-library checker verifies all dual signs, all 454 residual
coordinates, and the exact bound 13104/125. The certificate has 254 nonzero dual
rows. The explicit primal has all first reaches 6/5, all pair times 66/25, all
triple times 546/125, and allocations time/6; it is the uniform-control event
assignment. Every primal row and the objective equality are verified exactly.
The original witness has 239 decreasing coordinate comparisons in the selected
order, with largest decrease 224/645.

This development proves that chronological information closes the exhibited
gap in one chamber. It does not prove the target across all chronological
permutations, all global maximizers, or other dimensions. It does not
characterize the inverse reach identities. The five-block reach theorem, the
general weighted three-block inequality, exact general finite-mode minimax
outside the proved plateaus, and the largest-heavy adjacent-pair strengthening
remain genuinely unresolved here. No theorem relies on any of these questions.

## Verification performed

From the paper root:

```sh
python verification/stage03/run_checks.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Both pass. The runner verifies all 19 recorded original-artifact hashes, then
runs six original scripts and two new exact checkers. Relevant results:

- Original arbitrary-block construction: 330 arbitrary and 66 equal-total inputs.
- Original specialized heavy construction: 1859 rational inputs across all its
  three branches.
- Original global two-switch construction: 1440 rational inputs across all six
  branches; its equal-total dependency also passes 792 profiles and 12 sharp
  uniform cases.
- Original coefficient investigation: 6786 cases. Independent original seeded
  review: 3900 coefficient cases, 97 formal series, 768 minimum-mass contracts.
- New checker: 12170 exact seed coefficient cases, 1344 branch contracts,
  314 formal seeded series, 75 rational recursive seeded constructions spanning
  minimum/maximum/constant branches, and 171 all-light constructions.
- Both original witness organizations verify 454 nonnegative variables,
  3660 inequalities,64 equalities, and the stated rational objective.
- New chamber checker verifies 4038 inequalities,64 equalities, the exact dual
  certificate, and the matching uniform primal.
- `check_chronological.py` rejects Python `-O` explicitly; this rejection was
  tested after the primary agent identified an assertion-based guard issue.

A temporary relocated copy inside the stage03 verification directory included
only manuscript sources and bundled verification files. Its entire standard-
library suite and clean LaTeX build passed. The temporary copy was removed;
`relocated-checks.log` and `relocated-build.log` preserve the results. Neither
build nor checker depends on mutable files outside the paper folder.

I rendered and visually inspected all affected pages 21–32 in three contact
sheets. Equations, proof breaks, headings, and the new certificate scope text
fit cleanly. The final LaTeX pass has no warnings, undefined references, or
overfull/underfull boxes. `build.log` includes normal first-pass unresolved
references that disappear on the final pass; `final-build.log` and the final
`main.log` reflect the completed build. Page images and extracted text are in
`verification/stage03/`.

## Source and artifact dispositions

The manuscript proofs were rederived from the current accepted definitions and
results; repository notes were treated as claims to verify. The following
original programs/data were copied **unchanged** into `verification/reference`
and added to `origin-manifest.json` with repository origin paths and SHA-256
hashes:

- `code/cia_tv_conjecture/arbitrary_block_certificate.py`
- `code/cia_tv_conjecture/three_switch_heavy_certificate.py`
- `code/cia_tv_conjecture/two_switch_global_certificate.py`
- `code/cia_tv_conjecture/two_switch_equal_mass_certificate.py` (local dependency)
- `code/cia_reopened/general_reach_research.py`
- `code/cia_reopened/check_seeded_review.py`
- `code/cia_reopened/general_reach_relaxation_witness.json`

The two reopened source scripts preserve historical clipped defaults alongside
their unclipped checks; this is documented in the verification README. The
manuscript and newly authored coefficient/construction checks use the final
unclipped formulation. Original scripts are supplementary checks of historical
special cases or analytic constructions; the only new computer-assisted proof
dependency is the local chamber certificate and exact checker. The seeded
four-block upper also retains its previously accepted certificate dependency.

`results/cia-arbitrary-block-one-sided-bound.md`,
`cia-arbitrary-switch-global-bound.md`, and
`cia-seeded-arbitrary-switch-bound.md` are covered in Section 8.
`cia-three-switch-global-upper.md`, `cia-three-switch-heavy-mode.md`, and
`cia-two-switch-global-upper.md` are covered or explicitly subsumed in Section 9.
`notes/cia-many-mode-switching-investigation.md`,
`cia-reopened-general-reach.md`, and `cia-adjacent-repeat-investigation.md`
are covered through the dimension-free proof and the precisely scoped Section 10
investigation, together with the accepted structural section.

`verification/stage03/README.md` documents optional SciPy discovery, its
certificate-overwrite behavior, and the requirement to rerun the exact checker
before trusting a newly discovered candidate. Standard verification never
invokes numerical discovery. `README.md`, `PROCESS.md`, and the claim-coverage
map now mark stage 3 as drafted and awaiting independent review.

All author writes stop at this handoff. The stage is ready for freezing and the
required five-reviewer round.
