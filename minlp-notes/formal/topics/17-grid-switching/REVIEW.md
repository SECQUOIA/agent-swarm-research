# Arbitrary-grid one-switch minimax and sharp grid transfer: independent review

Four independent reviewers examined the package on 2026-09-20, one per tier of
[CLAIMS.md](CLAIMS.md). None of them wrote the proofs they reviewed. Each was
pointed at the **frozen obligation text**, not at the coverage map, and was
asked to find defects rather than confirm success, to build scratch
instantiations outside the repository, and to modify nothing.

Reviews are internal research-agent checks. They are not journal peer review.

| Tier | Obligations | Modules | Outcome |
|---|---|---|---|
| Model and foundations | SC01-SC11 | `Model`, `Cumulative`, `Endpoint`, `Compactness`, `OneSwitch` | No mathematical error; 9 discharged, 2 partial |
| The Section 8 theorem | SC12-SC23 | `LinearPrograms`, `Coverage`, `TwoLarge`, `Symmetrize`, `Elimination`, `FiniteOne`, `ThreeMode`, `Examples` | No blocking or significant defect; **all 12 discharged** |
| Transfer and coarsening | SC24-SC32 | `Rounding`, `UniformTransfer`, `BinaryTransfer`, `Transfer`, `Sharpness`, `Coarsening`, `Dwell` | No blocking defect; 8 discharged, 1 partial |
| Instance algorithms | SC33-SC37 | `InstanceAlgorithms`, `SubsetDP` | No blocking defect; 4 discharged, 1 partial |

**No reviewer found an incorrect theorem or an unsound proof.** Every finding
was either a Lean statement *narrower than the obligation it answered*, or a
documentation claim about the sources that did not hold up. All thirteen findings
are now closed; the partial verdicts above describe the state at review time.

## What the reviewers did themselves

The reviews did not rest on reading proofs. Each reviewer rebuilt mathematics
independently:

- **The elimination formula was re-derived from scratch.** An earlier published
  version of this formula was wrong, caught only by a nine-mode counterexample.
  The Section 8 reviewer derived all eight lower-versus-upper endpoint
  comparisons by hand from `eq:grid-M-interval` and matched each against the
  Lean `Iff` character for character, then checked that the `L` and `U` term
  lists match `eq:grid-L` and `eq:grid-U` with no term duplicated, dropped or
  strengthened, and that the reconstruction verifies all thirteen constraints.
- **Every published number was recomputed independently.** The same reviewer
  re-implemented `eq:grid-H`, `eq:grid-L`, `eq:grid-U`, `eq:grid-admissible` and
  the minimax formula in exact rational arithmetic, obtaining `17/5` for the
  five-mode nine-cell case, `2593/270` and `2077/216` for the nonuniform
  witness, and the full three-mode residue table for `N = 1..13`.
- **The general machinery was cross-checked against an independent route.**
  On the five-mode nine-cell grid they machine-checked that the SC20 formula
  yields `17/5`, matching `Examples.gridF_unit_five_nine`, which is proved by a
  completely separate argument. Agreement between two independent routes is the
  check that would catch a subtly wrong general theorem.
- **The rounding lemma was tested against the case that defeats greedy.** The
  transfer reviewer built the four-mode instance in which two modes
  simultaneously require rounding up, confirmed the theorem applies, and then
  built a **negative control**: a support-feasible selection that violates a
  lower prefix bound. That establishes the prefix bounds are not vacuous.
  That control was scratch work outside the repository; it has since been
  formalized as `exists_supported_not_prefix_bounded` in `Rounding.lean`, with
  one difference worth recording — the Lean witness (`n = 2`, `N = 3`, rows
  `(2/5, 3/5)`, mode `1` everywhere) violates the **ceiling** bound at `k = 3`,
  not the lower bound the reviewer used. Either direction makes the same point.
  Note also that neither the control nor anything else in the package refutes a
  particular greedy rule; an earlier version of this bullet and of the coverage
  map claimed that a single-pass greedy "provably fails", which was unproved.
- **A cited hypothesis was tested for load-bearing.** The algorithms reviewer
  constructed a monotone non-Lipschitz input and showed the completion formula
  fails on it, then separately proved that inside `IsCumulative` the Lipschitz
  field is *derivable* from monotonicity and conservation. That pair of results
  corrected a claim this package had made about the source (below).
- **Non-vacuity was checked wherever hypotheses are bundled.** Feasible points
  of both linear-program families, a `Scenario`-style instantiation, a
  disconnected block subset for the subset cost, the `⊤` base case of the
  dynamic program, and `k = N` for the covering claim were each instantiated on
  concrete data and compared against hand computation.

## Findings and their resolution

No finding was blocking. All are closed.

| Finding | Obligation | Resolution |
|---|---|---|
| The `O(n(N+M))` coarse-data construction for nonaligned grids was unformalized, and the exclusion invoked was broader than `CLAIMS.md` grants — its *correctness* content is in scope | SC30 | New module `Refinement.lean`: the common-refinement sum reproduces exact coarse values with no alignment assumption, the `N + M - 1` size recursion, and a witness where grouping whole fine cells gives the wrong value |
| The "at most `k` maximal runs" clause had no declaration | SC37 | `exists_isReduced_gridSchedule` with `card_positiveBlocks_comp_le` |
| The stated arithmetic and storage bounds were declined entirely | SC37 | Size recursions proved: `2^k` states, `3^k` transitions, and the **exact** enumeration cardinality (upgrading a bound to an equality) |
| Compactness of the schedule class was never stated, though all its consequences were proved | SC07 | `isCompact_bcfScheduleSet`, with both directions of the identification. The literal predicate the reviewer suggested would have been the *wrong* class, since `IsSchedule` asserts a global identity; the agreement-on-horizon form is used instead |
| Merging equal consecutive modes was proved only at the leading position | SC03 | `occupation_merge_at` at an arbitrary position, plus `exists_isReduced` and the run-budget packaging |
| `IsGridConstant` was defined by formula and never tied to a relaxed control | SC04 | `gridRateFun`, `simplexRates_gridRateFun`, `IsGridConstant.exists_simplexRates` |
| `F` was not packaged as a supremum over relaxed controls, leaving SC02's role implicit | SC04 | `F_eq_sSup_simplexRates`, `Gminus_eq_sSup_simplexRates` |
| The three-phase half of the source's sentence was outside the theorem statement | SC20 | Conjoined into `exists_compressed_maximizer` |
| The SC05 sub-clause of SC20 was recorded nowhere | SC20 | `isGreatest_gridOPT_cumulative` |
| The headline rounding lemma was unused and its padding duplicated | SC24 | The transfer now consumes `exists_supported_rounding`; the duplicate deleted |
| The "chronological subsequence" clause was prose | SC24 | `exists_subsequence_blockMap`, `exists_subsequence_uniform` |
| The `n = 2` case of the algorithm was only pointwise dominance | SC33 | Five declarations, including the equality of minima and the `IsLeast` form |
| One-sided scaling analogues absent | SC08 | Seven declarations added |

## A claim this package made about the sources, corrected

The package originally recorded that SC35's negative-residual step "requires the
1-Lipschitz property, which the source does not invoke at that point", and that
"the justification is incomplete". The algorithms reviewer showed this
overstates the case. The Lipschitz bound *is* load-bearing — a monotone
non-Lipschitz input breaks the formula — but inside `IsCumulative` it is
**derived** from monotonicity together with conservation, so the source omits no
assumption; a formal proof merely has to make an implicit step explicit. The
same reviewer also showed the module's stated *reason* why an upper bound breaks
`eq:final-residual` was wrong: any upper bound satisfies the endpoint inequality
that was cited, and the real failure is reading the prefix error as the
discrepancy at the single endpoint rather than the supremum. Both the module
docstring and [COVERAGE.md](COVERAGE.md) are corrected.

## Errors found in the sources, and their scope

These are genuine defects in the manuscript found by formalization. None
changes a published conclusion.

- **Section 8's case split is too weak.** "If `B < T/3` or `Q > T/3`" misses the
  case `x_c = T/3` exactly with `b = c + 1`, where `Q = T/3` is not `> T/3`. The
  non-strict forms cover it and the paragraph's conclusion is unaffected.
- **Unstated hypotheses.** `thm:certified-coarsening` silently needs `T > 0`
  (at `T = 0` its strict certificate reads `0 < 0`); `thm:fixed-budget` needs
  `0 < N`; the attainment witness of `eq:grid-H-witness` needs `0 < T`; and
  `eq:block-subset-cost` as literally written is an empty maximum at `k = 0`.
- **Conditions asserted without proof.** `t_{c-1} <= E` is used but never
  justified; it follows from minimality of the cutoff index.
- **A hypothesis stronger than needed.** `0 < eps <= 1` in the coarsening
  corollary never uses `eps <= 1`.
- **A result true more generally than stated.** The `s = 1` half-mesh refinement
  holds on arbitrary grids, not only the uniform ones it is stated for.

## Notes recorded rather than changed

**Current manuscript reconciliation (2026-09-20).** The source findings above
record the review's earlier assessment. The current manuscript's
`sections/01-foundations.tex` already assumes `T > 0`, positive block counts,
and positive grid sizes globally, so the missing-hypothesis and empty-maximum
items do not describe outstanding defects. Section 8 now includes the
non-strict case split and the cutoff condition from minimality; Section 11
states the arbitrary-grid one-switch half-mesh certificate. Section 10 also
spells out that the prefix error is the exact maximum over the full prefix.
The restriction `eps <= 1` remains a valid, conservative statement. These
are source and documentation changes only; no Lean theorem, frozen
obligation, or historical execution record was changed, and no new Lean
build, kernel replay, or CI check was performed for them.

- SC34's reduction is per fixed ordered pair and does not narrow the
  three-candidate boundary scan, because that scan's third candidate has an
  initial mode depending on the boundary. The source's paragraph reads as
  though it might; the package claims only the correct version, and records
  that the source's own `O(n log(N+1))` algorithm — the union over initial
  modes — does solve the whole problem.
- SC29 is recorded as scope only, in a module docstring, with no theorem. The
  refuted statement is a heuristic preceding a conjecture, not a proved theorem,
  and the example says nothing about the difference of two minimax values.
- The package's transfer theorems do not preserve dwell or transition
  constraints, and SC31 exhibits a dwell-constrained gap that does not vanish
  under refinement.

## Source review after the arbitrary-grid extension, 2026-09-20

A source-only review of commit `80f36418` found no theorem defect in the
arbitrary-grid one-switch extension. Three prose findings are corrected: the
zero-cell uniform-grid case remains admitted; a longest-cell midpoint is
half-mesh from its nearest nodes, not every node; and Hall graph adjacency
requires positive overlap with the particular token interval. The changes are
limited to documentation and a Lean comment. No new proof execution or CI
inspection was performed; the earlier verification results remain historical.
