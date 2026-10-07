# Numerical review repair record

Date: 2026-10-05. Revision writer: GPT Sol, under the user's authorized
fallback after Claude rate limiting. This record responds to
`evidence/reviews/opus-numerical-r1.md` and the root's scoped repair request.
The review reported no mathematical defect in the upper-bound, reduction,
or height proofs. This revision corrects scope, attribution, and wording;
it does not replace those proofs.

Owned manuscript files were `sections/03-upper.tex`,
`appendices/A-upper.tex`, `sections/04-reductions.tex`,
`appendices/B-reductions.tex`, `sections/07-heights.tex`, and
`appendices/F-heights.tex`. Actual edits affect only Section 03, Appendix A,
Section 04, and Section 07, plus this record. Appendix B and Appendix F are
byte-for-byte unchanged from the revision baseline. No bibliography,
shared macro, main file, other author's file, or historical note was edited.

I read `evidence/BRIEF.md`, `evidence/authoring/CONVENTIONS.md`,
`evidence/authoring/DECISIONS.md`, both integration records, and the full
Opus numerical review. I also inspected the actual affected manuscript
passages, the earlier heights/reductions repair record, the relevant Sol
review conclusions, the vetted literature report, and the Appendix K
nullvector construction. The baseline copies are in
`/tmp/numerical-r1-before-duym5tbf`.

## Responses

1. **P2-1: upper bound versus classification.** The Section 03 contribution
   paragraph now states a one-instance upper bound for all six relations
   and arbitrary polynomial observables under the stated strong-convexity
   or strong-monotonicity hypotheses. It attributes matching completeness
   only to strict and weak value and coordinate comparisons for certified
   quartics, and coordinate comparisons for their certified cubic gradient
   maps. Equality retains only the upper bound. The checked-certificate
   languages and the broader upper-bound hypotheses remain unchanged.

2. **P2-2: Allender et al.** Section 03 now credits the source with a
   polynomial-time Turing upper bound for Square Root Sum in
   `P^PosSLP`. Its separate many-one statement is explicitly a consequence
   of this paper's adaptive compilation theorem. The ESY comparison keeps
   its stated many-one reduction and Appendix C locator.

3. **P2-3: GLS acceptance.** The root relayed Luna's primary-source
   verification: Theorem 3.2.1 returns the queried center on oracle
   acceptance, and Remark 3.2.33 retains that alternative while allowing
   cuts valid only on the fixed retained core. The verified theorem locator
   is printed pages 87–88, PDF pages 99–100. Appendix A now states the
   queried-center output explicitly. No acceptance radius, retained-ball
   radius, volume parameter, or algorithm changed.

4. **P2-4: EY2010.** The current Section 04 sentence already matches the
   root-relayed primary-source contract: Lemma 5 uses a linear-size ordered
   circuit over addition, multiplication, and division with every gate
   value in `(0,1)`, and compares its output in order. It is retained. The
   existing bibliography entry has the cleared journal metadata:
   *SIAM Journal on Computing* 39(6), 2531–2597 (2010),
   DOI `10.1137/080720826`. This is comparison prose; none of the internal
   compiler or realization proofs depends on that source.

5. **P3-1: minimum-sign premise.** The signal display in Section 04 now
   uses `u_0 != 0` rather than `u_0 > 0`. Both cases of the proof depend on
   `u_0^2`, so nonvanishing is exactly the premise supplied by the compiler
   theorem and needed for the strict inequalities. The introductory
   explanation now gives the precise squared-signal bound, one eighth of
   the output signal's absolute value. The perturbation, certificate, and
   lower-bound estimates are unchanged.

6. **P3-2: convex warm-start credit.** Section 03 now identifies its actual
   ingredients: the elementary estimate
   `||p|| <= ||grad f(0)|| / mu` fixes a rational box, and
   `lem:convex-value` supplies the value approximation on that box using
   classical ellipsoid machinery. Slot–Steurer–Wiedmer's radius and
   objective-gap results for merely convex programs on unbounded domains
   are credited separately. They are not claimed as the source of this
   section's strongly convex warm-start algorithm.

7. **P3-4: optional explicit separation bound.** I removed the optional
   `rem:upper-explicit-separation` and its JPT2013 numerical bound under
   the root's authorized fallback because no vetted theorem contract had
   arrived by the final pass. No other manuscript passage referred to that
   remark. The load-bearing `lem:separation`, its full proof, its fixed
   constant, and every application remain unchanged. This removes no
   internal result or source-inventory development. I did not research
   JPT2013 independently.

8. **P3-6 and plain wording.** The claim that precision is "the whole
   difficulty" was replaced by the exact one-instance reduction statement.
   The words "obvious" and "trivially" were removed from two nearby
   explanations without changing their mathematical content.

9. **Duplicated nullvector example.** Section 07 retains
   `rem:heights-nullvector` and its maximum-rank/common-kernel argument.
   Its repeated `W/Y` construction was replaced by a concise statement of
   the consequence and actual references to `prop:bnd-nullvector` and
   `app:bnd-nullvector`, where the same construction and full proof remain.
   Appendix K was read but not edited. No nullvector result was omitted.

10. **Additional rationality wording.** The one-dimensional warm-start
    proof now calls the interval midpoints rational numbers of polynomial
    length. For the lemma's arbitrary rational `R_0`, bisection need not
    produce dyadic rationals. This wording correction leaves the algorithm
    and bit-length bound unchanged.

The prior Sol R1/R2 repairs remain in place, including the rational
derivative bounds, oracle-answer encoding, Horner construction, full-basis
PSD example, block-sum certificate distinction, root radicand accounting,
quaternion constant accounting, circle rounding convention, and
format-specific circuit claims. The adaptive `O(S^2)` compiler and
deterministic `P^PosSLP` one-instance theorem are unchanged. There is no
ordinary-P collapse claim, no Las Vegas determinization, and no new equality
hardness claim. Local uses of `N` were not renamed.

An independent delegated read-only review inspected the actual changed
passages and all four diffs. It agreed that the final revisions preserve
the intended scope, queried-center contract, and common-kernel argument.
It identified the squared-signal wording refinement in item 5; after that
change and the optional remark removal, its final disposition was that no
issue remained in the scoped diffs. This is internal review, not external
peer review or a new full proof audit.

## Targeted checks actually run

- `cat`, `sed -n`, and `rg` read the named records and affected passages.
  `diff -u` compared the four edited manuscript files with the baseline
  copies above; each returned 1 because the expected changes were present.
  The complete diffs were inspected.
- A fresh inline Python document check applied only to the six owned
  manuscript files. It checked final newlines, trailing whitespace, control
  characters, uniqueness of their 146 labels, resolution of their 131
  referenced targets, and resolution of their 24 citation keys. Other
  manuscript files supplied label definitions only; no whole-manuscript
  verification was run. Hygiene, owned-label uniqueness, and all reference
  targets passed. The command returned 1 solely for the 12 pending
  bibliography keys listed below.
- `git diff --no-index --check` was run for each owned manuscript file
  against its baseline copy. All six checks printed no whitespace
  diagnostics. A byte comparison confirmed Appendix B and Appendix F were
  unchanged.
- A targeted `rg` scan of the six owned files found no remaining instance
  of the removed optional remark label/citation, the old classification
  sentence, the old Square Root Sum attribution, or the removed informal
  precision claim. The no-match exit status was 1, as expected.
- `sha256sum` produced the final manuscript hashes below. This record was
  separately checked for whitespace, control characters, and a final
  newline; its hash is supplied in the completion handoff.

No compilation, computational experiment, mathematical script, historical
checker, symbolic calculation, project-wide check, or CI inspection was
run. No literature search or KB mutation was performed. These checks are
local revision evidence, not CI results.

## Remaining integration item

The current `references.bib` still lacks these 12 pre-existing height
comparison keys:

`GaertnerMagronVallentin2026`, `HeltonNie2010`, `Jiang2021`,
`KolmogorovNaldiZapata2024`, `Laplagne2020`, `Lasserre2009`, `ODonnell2017`,
`PatakiTouzov2024`, `PeyrlParrilo2008`, `RaghavendraWeitz2017`,
`SafeyElDinZhi2010`, and `Zhang2020`.

This was reported to the root. Luna owns source research and the root owns
bibliography integration; I did not change either. The cleared
`BasuPollackRoy1996` and GLS/EY keys resolve. The removed optional JPT
citation is no longer needed by these files. Final submission readiness
still requires bibliography integration and the root's document checks.

## Final manuscript SHA-256 hashes

```text
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
59d80f97d0d99e05972c70ed37e1f56bf3effcb28621991db3f659bb6cd77901  sections/07-heights.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
```
