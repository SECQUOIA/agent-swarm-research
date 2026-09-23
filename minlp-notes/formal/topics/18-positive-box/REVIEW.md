# Positive-box multilinear gaps: independent review

Current status: the PB07, PB10, PB32, and PB37 gaps are closed. All forty-six
obligations are covered with the PB44 source corrections described below. The
initial review and its historical checks are retained here; the verification
record distinguishes completed checks from subsequent additions in [VERIFICATION.md](VERIFICATION.md). A further source-only
review confirmed the four closures and corrected the PB41 limit wording: `rho`
and `eps` stay fixed, while `b = L^2` varies.

Three independent reviewers initially examined the package on 2026-09-20, one per branch
of [CLAIMS.md](CLAIMS.md). None of them wrote the proofs they reviewed. Each was
pointed at the **frozen obligation text**, not at the coverage map, and was
asked to find defects rather than confirm success, to build scratch
instantiations outside the repository, and to modify nothing.

Reviews are internal research-agent checks. They are not journal peer review.

| Branch | Obligations | Modules | Initial outcome |
|---|---|---|---|
| Lower bound | PB32-PB44 | `RadixFamily`, `RadixIncidence`, `RadixTermwise`, `RadixHullGap`, `BilinearGraph` | No incorrect theorem. One obligation partial by design (PB37), one **error found in the source**, one packaging defect, two documentation corrections |
| Coefficient inequality and headline | PB13-PB22, PB25, PB45, PB46 | `CoefficientInequality`, `CommonAspectBound`, `PositiveBoxHeadline` | **No gaps and no errors.** Four places where Lean is stronger than the obligation |
| Laws, moments and transfer | PB01-PB12, PB23, PB24, PB26 | `PositiveBox`, `PhysicalEnvelope`, `OrientationMoments`, `OriginalBoxTransfer`, `TransferInterpretation` | No incorrect theorem. One route substitution (PB10), one universe restriction, one caveat that was itself wrong |

**No reviewer found an incorrect theorem or an unsound proof.** The initial findings were
of four kinds: one obligation discharged only in part, one discharged by a
different route, defects in the sources, and defects in this package's own
documentation. All are recorded below and in [COVERAGE.md](COVERAGE.md).

## What the reviewers did themselves

The reviews did not rest on reading proofs.

- **Every use site of the partial result was traced.** The lower-bound reviewer
  took PB37, which was then proved only in the upper direction, and enumerated every
  reference to `incidence_expect_le_of_means` in the whole tree. At the time
  there was exactly one, `expect_coverage_le` in `RadixHullGap.lean` (line
  398), and it consumes the result as an upper bound; nothing needed the lower
  direction, so the partial discharge was not a hole in the lower bound. There
  are now **two**: closing attainment added a second at
  `RadixAttainment.lean:805`, inside `isGreatest_incidenceValues`, where it
  supplies the upper half of the `IsGreatest`. An earlier version of this
  bullet kept saying "exactly one" in the present tense after that second site
  appeared.
- **The chain was rebuilt from source in a shadow `LEAN_PATH`.** The
  coefficient-inequality reviewer compiled `CoefficientInequality.lean` and its
  dependencies outside the repository's build tree, so the reviewed artifacts
  could not be the committed `.olean` files.
- **The induction was traced case by case.** The same reviewer walked PB18's
  induction on support cardinality looking for circularity (a case appealing to
  the statement being proved) and for vacuity (a case whose hypotheses are
  unsatisfiable, making the step true but empty). Neither was found.
- **The Schur counterexample was reproduced exactly.** The sources' four-variable
  witness that `F` is *not* Schur-concave was recomputed independently, which is
  what justifies PB17's global minimum/maximum hypotheses rather than a
  mean-preserving-spread hypothesis.
- **The PB07 folding was confirmed numerically and by hand.** The third reviewer
  derived the folding `t = min(2u, 2(1-u))` independently and checked it against
  the two branches of `orientationProbability` at **2,998 sampled points** and
  **520 random mean vectors**, with **zero mismatches**. The conditional success
  probability of the unfolded construction maps onto the two branches exactly
  and depends on `u` only through `t`, so conditional independence is preserved.
- **Non-vacuity was checked where hypotheses are bundled.** Feasible instances of
  the strictly positive aspect class, the balanced law at small `N`, a
  disconnected support for the radix family and the degenerate dimensions zero
  and one were each instantiated and compared against hand computation.

## Findings and their resolution

### PB37: attainment gap closed

Initially only the upper direction of `max E ∑_j A_j N_j = 1 + (L-1)/b`
was proved. The use-site review confirmed that this sufficed for the downstream
lower bound. `RadixAttainment.lean` now supplies exact attainment under
`b ≥ 2` and `2 ≤ L ≤ b + 2`, including the source's `2 ≤ L ≤ b` regime.

The upper proof uses the source's LP dual certificate: weights `0` at the top
level and `b^j` below it give a pointwise inequality whose expectation is
`1 + (L-1)/b`. That proof needs only `1 ≤ b` and `1 ≤ L` — an earlier version
of this paragraph named `1 ≤ b` alone, but `1 ≤ L` is in the signatures of both
`incidence_expect_le` and `incidence_expect_le_of_means`. The stronger
assumptions above are sufficient for the matching construction; no necessary
condition is proved.

### An error in the source `positive-multilinear-positive-box-lower.md`

The lower note's PB44 paragraph asserts that positive affine scaling to **any**
nondegenerate box leaves the bilinear gap ratio unchanged. **That is false for
unequal coordinate widths.** The reviewer produced two counterexamples, both
reproduced independently for this record by exact linear programming over the
`2^n` binary laws with all means one half:

| dimension | widths | true ratio | source's `2(n-1)/n` |
|---|---|---|---|
| `n = 4` | `(1, 1, 2, 2)` | `13/9 ≈ 1.4444` | `3/2` |
| `n = 6` | `(1, 1, 1, 1, 1, 3)` | `25/16 = 1.5625` | `5/3` |

The intended reading — scaling to the **common** box `[1, rho]^n`, where every
coordinate gets the same width — is correct, and it is what Lean states
(`bilinearGraph_box_ratio_eq`, `bilinearGraph_mem_commonAspectBoxRatios`). The
published conclusion `C_box(rho) ≥ 2` is unaffected. Nothing in the package
claims the false general form.

### A packaging defect, fixed

At review time **no topic-18 module was imported by `Formal.lean`**, so the
sixteen modules were not part of the canonical project: the project-wide import
check would have passed while the package was unreachable. The sixteen imports
were added, and the import check at that stage reported 433 modules. The three
subsequent closure modules are also imported by `Formal.lean`. These are
historical results, not a new project-wide check.

### `CLAIMS.md`'s PB44 omits a parity qualifier

PB44 as frozen says the complete positive bilinear graph "at normalized means
one half has ratio `2(n-1)/n`". That formula holds in even dimension `n = 2m`
with `m > 0`, as `bilinearGraph_cube_ratio` proves. In odd dimension
`n = 2m+1 ≥ 3`, the mean success count is a half integer, so the convex envelope
is attained by mixing the two adjacent counts. `bilinearGraph_cube_ratio_odd`
proves the ratio `2n/(n+1)`, and `bilinearGraph_cube_ratio_odd_ne` proves that it
differs from `2(n-1)/n`. Both statements require `m > 0`. At `n = 1` both gaps
vanish and the totalized ratio is zero.

The odd-dimensional formula was previously source-review arithmetic. The new
declarations formalize that observation; they do not overturn its mathematics.
`CLAIMS.md` remains frozen, and the PB44 row of [COVERAGE.md](COVERAGE.md)
records the parity correction. The conclusion `C_box(rho) ≥ 2` is unchanged:
the even-dimensional witnesses already prove it.

### PB32: partition nesting gap closed

Initially the actual blocks were defined at each level but no theorem related
them across levels. `Radix.blockEquiv_fst_val_of_le` now identifies the coarse
index as the fine index divided by `b^(k-j)`. For `1 ≤ b` and `j ≤ k`,
`Radix.block_subset_unique` proves that every level-`k` block is contained in
exactly one level-`j` block. This includes equal levels.

### PB10: slab-integrality gap closed

The initial construction `exists_adjacentLaw` established the adjacent-count law
by induction, leaving the named slab-integrality statement unproved.
`SlabIntegrality.lean` now proves equality of the slab with the convex hull of
its binary vertices and that every extreme point is binary. It also derives the
adjacent-count law by the geometric route. Two initial reviewers independently
identified the missing geometric statement.

### A universe restriction

`boxAspectRatios` and `commonAspectBoxRatios` quantify over `(I : Type)`, that
is `Type 0` only. Mathematically nothing is lost — every finite type is
equivalent to some `Fin n`, which lives in `Type 0` — but **there is no
transport lemma in the tree**, so the restriction is literal rather than
cosmetic. Recorded in the conventions section of [COVERAGE.md](COVERAGE.md); no
statement was changed.

### A review caveat that was itself incorrect, and is corrected here

The third review suggested that the PB07 folding gap **reaches PB28 through
fairness**: that because the fair orientation law was then related to the
obligation's construction by an unformalized folding, the balanced law of Tier F
inherited the gap. **That is wrong, for two independent reasons.**

1. **PB28 explicitly does not require fairness**, and fairness genuinely fails
   for odd `N`: a coordinate is low with probability `⌊N/2⌋/N`, which
   `balancedSubsets_mem_ne_half_of_odd` proves is not `1/2` for odd `N`. So
   there is no fairness property for the gap to travel along.
2. **The balanced law is an explicit unfolded construction.**
   `BalancedOrientation.lean` never references `orientationProbability` or
   `CubicGap.orientationLaw`; it builds `orientedProb`, `orientedLaw` and
   `balancedOrientationLaw` from a uniform low set and one uniform variable
   directly. The folding appears nowhere in Tier F.

The original PB07 gap was confined to the fair-law construction. It is now
closed by `fairOrientationLaw_eq_orientationLaw`; the earlier numerical checks
are historical supporting evidence, not the proof of the current claim.

### Four places where Lean is stronger than the obligation

The second reviewer found no gaps and no errors, and recorded four
strengthenings. They are in [COVERAGE.md](COVERAGE.md) in full; in brief:

- **PB23/PB25: fixed coordinates need not be removed.** The obligation and the
  source both say to remove them first. The transfer needs only **surjectivity**
  of the affine map (`exists_originalBoxPoint`), not injectivity, so
  `positiveBoxAspectBound_add_two` holds on every strictly positive box with no
  nondegeneracy hypothesis and no preprocessing step anywhere in the package.
- **PB26: the concave side is an equality, not an inequality.** PB24 gives
  `tbtgap_original ≤ tbtgap_expanded`; `originalMonomial_concaveEnvelope_eq_sum`
  gives the concave envelope of the original monomial as *exactly* the sum of
  the expanded concave envelopes, because one common law attains all of them.
- **PB19: the identity holds over the full degree range.** The sum runs to
  `j = n + 1`, and the top coefficient is `C_n - P_n`. Lean proves only that it
  is nonnegative (`coeffF_card_add_one_nonneg`); that it is generically
  nonzero, and hence that truncating at `j = n` would make the identity false,
  is source-review mathematics rather than a separate Lean counterexample
  theorem. Earlier wording did not distinguish those kinds of evidence.
- **PB31: dimensions zero and one are proved, not assumed away**, and joined
  inside `commonAspect_termwiseGap_le_balanced`, so the final statement carries
  no dimension hypothesis at all.

## The fix made in response to the reviews

Two supremum statements for the common-aspect class,
`two_le_commonAspectBoxSupremum` (PB44) and `rho_le_commonAspectBoxSupremum`
(PB43), each carry an explicit `BddAbove (commonAspectBoxRatios rho)` hypothesis.
Nothing in the package discharged it, so **both were permanently conditional**:
`sSup` of an unbounded set is junk in Lean, and without boundedness the
statements said nothing.

Two declarations were added to `PositiveBoxHeadline.lean` to close this:

- `commonAspectBoxRatios_bddAbove_of_lt`, which obtains boundedness of the
  common-aspect class from `boxAspectRatios_bddAbove_of_lt` through the PB02
  inclusion `commonAspectBoxRatios_subset_boxAspectRatios`;
- `le_commonAspectBoxSupremum`, the unconditional
  `max 2 rho ≤ commonAspectBoxSupremum rho`.

This is the same circularity-breaking pattern the general class already used:
the `rho + 2` upper bound supplies the boundedness that makes the lower bounds
meaningful, and both lower bounds are stated in `BddAbove`-free forms so they
can be applied before boundedness is known.

## Errors found in the sources, and their scope

The unequal-box assertion is a source error. The incidence hypotheses can also
be weakened. Neither observation changes the headline conclusions.

- **`positive-multilinear-positive-box-lower.md`**: positive affine scaling to
  any nondegenerate box does **not** leave the bilinear gap ratio unchanged;
  two counterexamples with unequal widths are tabulated above. The intended
  common-box reading is correct and is what Lean proves.
- **`positive-multilinear-incidence-sharp-growth.md`** (imported as PB37): the
  hypothesis `b ≥ L` is stronger than the upper direction needs. The dual
  certificate requires only `1 ≤ b` and `1 ≤ L` (an earlier version omitted the
  second). For attainment, `2 ≤ L ≤ b` is sufficient, but
  not necessary: the formal construction works under `b ≥ 2` and `2 ≤ L ≤ b + 2`.

## Notes recorded rather than changed

- The necessity of `L ≤ b + 2` for incidence attainment is not formalized and
  is not part of PB37. The existing downstream bound uses only the upper direction.
- `RadixTermwise.lean` deliberately does **not** import `PhysicalEnvelope.lean`,
  deriving the closed-form envelopes for its own family independently of PB05.
  This is duplicated *reasoning*, not duplicated code: the two arguments sit at
  different levels of generality, and the separation keeps the lower-bound
  branch independent of the upper-bound branch. If the duplication were ever
  removed, `Radix.expect_term_le` is the single re-routing site.
- PB42 appears in two modules for two genuinely different maps — the
  multiplicative `[1/rho, 1] → [1, rho]` at arbitrary degree for the radix
  family, and the affine unit-cube map restricted to degree-2 supports for the
  bilinear graph. Neither subsumes the other; they share only the mean-exact
  splitting lemma `hullGap_of_meanExact_split`.
- PB26's hull-gap reading is **disproved** with an explicit counterexample. The
  obligation as frozen says "deficiency" and is fully discharged; the
  counterexample refutes a stronger statement that nothing in the package or the
  sources asserts.

## Closure of the findings

Four gaps identified across the reviews have been closed: three in new modules
and PB32 in `RadixFamily.lean`. The new proofs were also reviewed independently.

**PB07 (formalization gap).** Both the second and third reviews confirmed that
the folded `CubicGap.orientationLaw` was being used without a Lean proof that it
is the construction PB07 names. `FairOrientationFolding.lean` now proves
`fairOrientationLaw_eq_orientationLaw`, an equality of laws with no cube
hypothesis, so every moment result transfers verbatim. The pointwise folding
identity can fail only at `t = x i` or `t = 1 - x i`, and for a given
coordinate value at just one of them — at `t = 1 - x i` when `x i < 1/2`, at
`t = x i` when `x i > 1/2`. An earlier version of this paragraph said it fails
at both; that was wrong, with no effect on soundness, since the exceptional set
the proof discards is a superset of the true one. Rather than glossing the
failure, the module records an explicit counterexample
(`fairCoinProb_ne_orientationProbability_foldUnit`, the instance `x = 1/4`,
`t = 3/4`) and compares the integrands off a finite, hence null, set.

One caveat attached to that review was **incorrect and is recorded as corrected**.
It suggested the folding gap reached Tier F through fairness of individual
orientations. It did not: PB28 explicitly does not require fairness — fairness
in fact fails for odd `N` — and `BalancedOrientation.lean` never references
`orientationProbability`, building its own explicit orientation subset. The gap
was confined to the fair law of Tier C throughout.

**PB10 (route substitution).** Two reviewers independently found that the named
slab-integrality statement was absent. `SlabIntegrality.lean` now supplies it
as the hull equality `convexHull_slabVertices_eq`, with the one-sided
`extremePoints_slab_subset` as
its corollary, and `exists_adjacentLaw_of_slab` typechecks as the exact
statement of the pre-existing construction at `s = Finset.univ`. The geometric
route does **not** subsume the operational one: `exists_adjacentLaw` is stated
for an arbitrary support `s` and PB11 needs that generality, as the PB10 row of
[COVERAGE.md](COVERAGE.md) and the `SlabIntegrality.lean` docstring both say.
An earlier version of this paragraph claimed subsumption, contradicting them.

**PB37 (partial discharge).** The first review verified that nothing downstream
needed the missing attainment direction. `RadixAttainment.lean` now proves it, so
the obligation's equality holds. Two simplifications over the source: the
digit-reversal ordering and digit-shift action proved unnecessary, because every
failure count in the two profiles is a power `b^t` and a residue class then has
the correct hit count at every level simultaneously; and the more general sufficient regime
is `b >= 2` and `2 <= L <= b + 2`, including `2 <= L <= b`.

That last point **corrects a supplementary claim** recorded earlier in this
package, that the bound is tight exactly when `b >= L`. Exact LP, run
independently twice, shows `(L, b) = (3, 2)` and `(4, 2)` are tight with `b < L`;
the formal result proves sufficiency under `b >= 2` and `2 <= L <= b + 2`, consistent with those
examples. Necessity is not proved. The earlier claim generalized from the single
failing point `(5, 2)`. The source's hypothesis remains sound: sufficient but
not necessary.

**PB32 (nesting).** The quotient-index identity and unique coarse-block
containment are now proved for the actual radix partitions, closing the remaining
structural claim.

## A hole in this file's own review coverage, since closed

The three reviews recorded above covered PB01–PB12, PB13–PB22 and PB32–PB44.
**PB27–PB31 — the finite-dimensional balanced-orientation refinement — fell
outside every branch**, and the modules `BalancedMoments.lean` and
`BalancedRefinement.lean` appear in no module column. `README.md` nonetheless
described the package as independently reviewed. This was a gap in the initial
assignment. It does not establish that later all-topic reviews also omitted the
tier; the initial assignment and the later review are recorded separately.

A fourth independent review has since covered PB27–PB31. **Verdict: all five
discharged** — no gap, no narrowing, no mathematical error. What makes that
verdict worth something is that the reviewer tested the tier adversarially rather
than confirming it:

- It checked the design claim that resampling is impossible, and found the
  *stated* form of that claim false — `pairOppositeProb S.card` does typecheck.
  The definitions and proofs retain the ambient law and constant as the support
  shrinks; this is not a prohibition imposed by the types. The descriptions in
  `COVERAGE.md`, `README.md` and both module docstrings now make that distinction.
- It showed the same-`β_N` requirement is **load-bearing**, by substituting
  `β_{#S}` against the ambient law and finding `F` negative in 28 of 2386 random
  exact-rational cases, with a hand-checkable smallest instance.
- It re-derived PB27's constants three independent ways — brute-force enumeration
  of all `⌊N/2⌋`-subsets, the closed definition, and the choose-form — agreeing at
  every `N = 2..12`, and confirmed the `N ≤ 1` junk values make the `2 ≤ N` guard
  necessary rather than cautious.
- It confirmed fairness is nowhere assumed: `balancedSubsets_mem` is used by
  exactly one declaration, the one recording that fairness *fails* for odd `N`.

**Explicitly not claimed, and now recorded as such:** whether `β_N` is the
*minimal* constant for which `F_{S,j} ≥ 0` holds ambiently is unverified in
either direction. A grid search at `β_N - 1/100` found no violation. It is not an
obligation — PB27 only defines `β_N` and PB31 only asserts the bound — but the
package should not be read as claiming sharpness.
