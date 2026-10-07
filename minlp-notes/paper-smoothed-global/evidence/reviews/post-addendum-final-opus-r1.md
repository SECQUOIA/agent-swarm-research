# Post-addendum final review, Opus R1

Reviewer: fresh independent Opus reviewer. Date: 2026-10-06. This is a
round-1 review of the frozen addendum successor. It does not continue any
earlier child review. Its scope is a targeted check of attribution, the
late mathematical repairs and the presentation. It is not a fresh audit of
every proof, and it is not a literature search. I did no browsing and no
literature research, and I read no companion sources. Companion content is
taken from the supplied Luna source contracts.

## Target and identities

| Item | SHA-256 |
| --- | --- |
| `evidence/snapshots/submission-addendum-r1/manifest.json` (21 sources, predecessor `final-submission-r4`) | `fc756e30029d3d1d430b6e77e1d6b557bbb7e7d7a55b24599b95be5cd28b87f9` |
| R4 predecessor `snapshots/final-submission-r4/manifest.json` | `0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061` |
| `evidence/submission-addendum-r1.diff` | `a0629b1815888a3cf7a3884aa23df4a7b16b927f14f2b11db2c63228afd448a8` |
| `verification/addendum-source-comparison.json` | `ad0a20829dd8a85e5c2ddbb37f3e430693bab874a6244dedbadaec35de63660f` |
| `evidence/companion-overlap-addendum-luna.md` (initial text and dated follow-up) | `fbd34b464a1b4f3272fa667498510bc1e6aadb8c64786c963f53eaa64ce01d5a` |
| `evidence/reviews/late-opus-math-disposition-sol-r1.md` | `abede7bbdc92c0ad83694fed7102ecbd56ea1acccf65f75f824f356707740e91` |
| `evidence/author-reports/attribution-addendum-opus-r1.md` | `cc3b2cf8e88b096e0721a609886a76627e634f430fb48f378591f6a5fe253062` |
| `evidence/author-reports/late-math-repairs-opus-r1.md` | `90b257595a20af06d8546242c168c302ecb0e71b0e18e4f62b6ee975c9172e2c` |
| `evidence/author-reports/front-r1.md` | `b208ce7f88d97841f0f6c7f6d6e0d9a8f9a067cb1152cf72a1b2f787e8805fd0` |
| `main.pdf` (182 pages, supplied by root) | `ac18317098be35feca176e5f5112b3d5d3c6403049ee1245553d2faa0bcfb458` |
| `verification/main-final.txt` | `6bf7c5282f81781435b899f3e959455d426e252dba45766f93683f73da3a134b` |

## What I read

- The full review brief `evidence/attribution-addendum-review-brief.md`.
- The complete exact diff and the complete Luna overlap audit, including the
  dated follow-up. The follow-up supersedes the initial claim that family B
  is not reproduced: the positive-definite variant is the `h=1/4`
  specialization of companion family B. It also adds the TU
  rounding/allowance/filter overlap.
- The attribution writer's report, including its follow-up and final hashes.
- The withdrawal at the top of `front-r1.md`. Its B10 "new as a manuscript
  statement" characterization is explicitly withdrawn, and the line-160
  historical text is preserved under that correction.
- The late-math disposition by Sol, the Opus repair report and its
  follow-up, and the finding index of `reviews/opus-math-r1.md` (NEW-1 to
  NEW-6).
- In the frozen snapshot, every changed passage with its neighboring formal
  results:
  - Section 1: mechanism paragraph (200–235) and companion paragraphs
    (470–561).
  - Section 2: model definition, row-scaled paragraph, base-chosen laws,
    `prop:model:uniform` and its proof, the scalar-law paragraph, the FPT
    paragraph and the regret widths (95–245, 400–500).
  - Section 4: `thm:qp:uniform`, `thm:qp:aligned` and `rem:qp:regret`
    (590–652).
  - Section 5: certified conditional values, `prop:sp:conditional` with its
    proof, and `sec:sp:prior` (575–700, 1105–1145).
  - Section 6: `sec:con:scope` and its Relation paragraph (780–834), plus
    the statement of `thm:int:tu`.
  - Section 7: `lem:rec:value`, examples 7.3 and 7.4, the variant
    paragraph, the core search and `prop:rec:search` (95–262).
  - Section 8: the lattice section opening and `thm:int:lowrank` (652–700).
  - Section 9: from the repair paragraph through `prop:lim:local`, its
    proof, and `prop:lim:conditional` (212–330).
  - Appendix F: the end of the flow-boundary proof, `lem:int:affine-margin`
    and its proof, and the proof of `cor:int:bilinear` (900–975).
- In the PDF, the physical pages that hold every changed passage: 11, 12,
  14, 15, 16, 19, 40, 52, 70, 72, 73, 74, 90, 95, 96 and 169.

## Independent integrity checks

All checks were run locally, read-only.

- **Manifest.** All 21 manifest entries match both the snapshot files and
  the live working tree.
- **Changed files.** `diff -rq` between the R4 and successor snapshots
  shows exactly nine changed sources: Sections 01, 02, 04, 05, 06, 07, 08
  and 09, and Appendix F. `main.tex`, `macros.tex` and `references.bib` are
  byte-identical.
- **Diff file.** I regenerated the unified diff. It has the same content as
  the supplied diff. The only differences are file order and the hunk
  alignment of one blank line in Section 2.
- **Environment extraction (my own script).**
  - Theorems 32/32, lemmas 78/78, corollaries 12/12, definitions 29/29 and
    examples 15/15 are all unchanged.
  - Of 21 propositions, one changed: `prop:model:uniform`.
  - Of 4 remarks, one changed: `rem:qp:regret`.
  - Of 138 proof blocks, one changed: the affine-margin proof. The other
    137 are byte-identical.
  - Labels: 410/410, identical lists.
  - Displayed math blocks: 249/249, identical.
  - The set of cited keys is identical.

  This independently confirms the brief's count.
- **No stale rewrite.** The Section 2 diff contains only the row-scaled
  paragraph, the `prop:model:uniform`(a) clause, the scalar-law phrase and
  the FPT sentences. None of the obsolete front-R2 replacement is present.
- **PDF.**
  - The hash matches root's statement, and the PDF has 182 pages.
  - The text extract contains no `??`.
  - `main.log` has no undefined-reference, multiply-defined or overfull
    lines.
  - `main.blg` shows only the three known sort warnings for the anonymous
    companion entries.
  - Every changed passage appears in the PDF with resolved numbers, for
    example Lemma 7.2(b), Proposition 7.5(a)–(c), Proposition 5.10,
    Corollary 9.3, Example 7.4, Section 6.5, Theorem 8.14, Theorem 8.17 and
    Lemma F.16.

## Claims verified

**Introduction and local attributions agree.**
- The introduction (PDF pp. 11–12) names four deterministic antecedents:
  - the value-function curvature (Lemma 7.2(b));
  - exact-oracle CORE retention, value interval and witness (Proposition
    7.5(a)–(c));
  - the certified bag filter (parts (a) and (b) of Proposition 5.10 and
    Corollary 9.3);
  - both star families.
- Each local passage repeats the same split:
  - 07:126–130 says Part (b) is the curvature part of the companion lemma
    under a fixed recourse feasible set, and that its proof is included for
    completeness. The companion's growth part is not claimed.
  - 05:596–599 says (a) and (b) specialize the certified bag filter and are
    re-proved, and that (c) is the finite-law extension. The duplicate
    after the proof was removed, and `sec:sp:prior` still credits the
    filter.
  - 09:298–301 says (a) and (b) restate the companion guarantees and (c) is
    `prop:sp:conditional`(c).
  - 07:178–188 and 09:224–229 say the deterministic star example is the
    companion's family A, and the positive-definite variant is the `h=1/4`
    case of family B. `prop:lim:local` adds every-draw persistence for
    `σ ≤ 1/1000` and level-0 nonclosure. Both additions are in the
    proposition's statement and proof (Level 0 paragraph), so the
    attribution matches the formal content.
- The family-B credit follows Luna's follow-up, not the superseded initial
  claim.

**CORE exact versus certified.**
- 07:253–258 credits (a)–(c) in exact mode to the companion and says its
  separate query bound uses point growth.
- It describes the addition as allowing certified errors and expected
  queries without a growth premise. The proposition does state this: the
  conditional-on-`γ_R` expected count with `M ≥ 2^J` and `Q_ex`/`Q_ap`.
- It does not claim the companion's CORE part (d), the global lower-bound
  record. It makes no priority claim for the certified mode, only a
  comparison with CORE as stated.

**Oracle scope.** Sections 5 and 9 still say this is a sufficient interface,
not an algorithm, and that no oracle is supplied for general sparse
instances. Nothing in the addendum invents an efficient general outside
oracle.

**TU.**
- Section 6.5 (p. 70) narrows the exclusion to TU constraints on the
  searched coordinates under this paper's smoothed guarantees. It separates
  this from the positive `thm:int:tu`, whose statement confirms that TU
  constrains only the integer recourse.
- It gives the companion's results with their correct premises:
  - fixed-degree approximation certificates without growth, with
    accuracy-dependent tables;
  - exact rational-quadratic termination without growth or uniqueness;
  - set growth bounding the levels;
  - accuracy-independent operation bounds that also need set growth and a
    separate bound on optimal coordinate-value counts.
- It does not claim that these bounds integrate under noise, and it points
  to `sec:sp:width`.
- The direct rounding/allowance/filter credit (Luna follow-up) is present.
  Hoffman–Kruskal remains cited for the integral-vertex fact.
- The smoothed gap stays where it was: no count, closure or tail estimates
  for general TU.

**Closure and enclosure.**
- The face-enclosure paragraph (01:528–536) is unchanged. It still says the
  polynomial closure reuses the companion's strongly convex face enclosure
  and adds finite-noise margin tails and a same-draw fallback.
- The new sentence (01:524–527) frames the addition as the composition
  under noise of re-proved deterministic parts. It is not a blanket
  originality claim for closure certificates. See optional item O1 for a
  small wording improvement.

**Earlier qualifications preserved.** The growth runtime formulas,
graded-grid count, uniform-grid stage bound, rETH product-time scope,
integration limitation, exact-arithmetic and sparse-indicator paragraphs,
and the P1–P5 resolutions are all outside the diff or byte-identical.

**NEW-1: affine-margin proof.** I verified the repaired proof.
- **Nonempty zero set.** Nonzero affine `p` with `Z_p ≠ ∅` forces `π ≠ 0`.
  The case `p ≡ 0` is excluded by "nonzero".
- **Bound on π_min.** A nonzero rational with numerator and denominator of
  at most `H_0` bits has magnitude at least `2^{-H_0}`.
- **Minimizing point.** The coordinatewise minimizer `v` lies in the cube.
  It need not be a vertex, which the text handles by calling it "this point
  of the cube". It has `p(v) ≤ 0`.
- **Path.** Each leg changes one nonzero-slope coordinate monotonically
  toward `v`, so `p` decreases at rate `|π_i|`. The first zero `y` lies in
  the cube, at ℓ1 length at most `p(x)/π_min`. Since Euclidean length is at
  most ℓ1 length, `dist(x, Z_p) ≤ 2^{H_0} p(x)`.
- **Negative values.** The `-p` case is correct.
- **Empty zero set.** The bound `2^{-(q+1)H_0}` is unchanged and correct.
  It also covers nonzero constants.
- **Counterexample.** The reviewer's counterexample
  `p = x_1 − 2x_2 + 1/2` now gives `v = (0,1)` and a zero at length
  `1/4 ≤ 1/2`.
- **Dependency.** The lemma statement is byte-identical. The bilinear use
  sets `μ_0 = 2^{-(k+1)H_0} δ/2` with `δ ≤ 1/4` and face dimension at most
  `k`, and both branches dominate it. So `cor:int:bilinear` and the
  bilinear part of `thm:int:tu` keep polynomial sampling precision. No
  constant changed.

**NEW-2: row-scaled lattice law.**
- The paragraph after Definition 2.2 names the extension: independent
  `U_{σ_i,M}`, specified rational `σ_i`, and one common base-chosen `M`.
- It explains why row rescaling cannot remove unequal scales, because `T`
  enters the objective. It explains why the common `M` fixes the lattice
  spacing.
- It ends with "Every theorem asserts its bounds only for the law it
  states." The overbroad prohibition was removed.
- This matches the setup of `thm:int:lowrank`: "choose a rational
  `σ_i > 0`", `ξ_i ~ U_{σ_i,M}`, "all rows use the same `M`". It also
  matches the Section 8 opening and the bound `H_rat` with `σ_i`.
- `prop:model:uniform`(a) keeps each `σ_i` with one common `M(I)` and the
  reset level cap. The proof and the other items are unchanged. The
  scalar-law paragraph is consistent.
- No other theorem's hypotheses are broadened.

**NEW-3 and NEW-4.** Both were already resolved in R4. Neither passage is in
the diff, which is consistent with the Sol disposition. I did not re-audit
them.

**NEW-5: FPT summary.**
- 02:410–420 (PDF p. 19) restricts the low-negative-inertia FPT claim to
  aligned and Gaussian-like noise. It keeps joint parameterization with the
  numerical ratios.
- It explicitly excludes `thm:qp:uniform`, whose statement and following
  remark (04:595–614) show a power of `n` that grows with `k`.

**NEW-6: regret remark.**
- `rem:qp:regret` now uses `σ̄ W_noise` with original-domain coordinate
  widths. For ambient noise all `n` coordinates are perturbed, so this is
  consistent with the model's definition in `sec:model:original`.
- It explicitly rejects the auxiliary `w_i` and allows continuous-relaxation
  widths as upper bounds on mixed polytopes.
- It keeps the `(b+20)σ` support factor and the aligned bound
  `σ̄ Σ (u_i − ℓ_i)`.
- I checked the Sol counterexample (`X = [0,1]`, regret `1/200`): it is
  covered by `σ · 1` and not by the auxiliary widths.

**Editorial items A8, A9, A12 and A13.** In the current version I find no
substantive reader confusion that requires restructuring:
- The integer routes are under explicit subsections.
- `prop:model:uniform` is a compact specialization with a forward pointer.
- The repeated oracle contracts aid transparency.
- The one real notation collision, `w_i` in the regret remark, is fixed.

## Concerns

None is a defect that blocks the scoped verdict. The three items below are
optional wording improvements. None changes a claim's truth, and in each
case an adjacent sentence already gives the precise version.

- **O1 (01:526).** The list after "What this paper adds is their
  composition under noise:" includes "sound closure tests". Read in
  isolation, this could suggest the closure tests themselves are new. The
  next paragraph explicitly says the closure reuses the companion's
  enclosure, and the R4-reviewed `sec:sp:prior` and Section 6 Relation
  paragraphs use the same composition framing. Suggested tightening:
  "finite-noise margin tails under which sound closure tests succeed".
- **O2 (01:500–501).** "finitely many optimal coordinate projections" is
  imprecise: there are always `n` projections. The intended premise, stated
  exactly in Section 6.5, is a bound on the number of distinct values each
  coordinate takes over the optimal set. Suggested wording: "a bound on the
  size of each optimal coordinate projection".
- **O3 (06:799 and 04:641).**
  - The symbol `r` in Section 6.5 is introduced and never used. Elsewhere
    in Section 6, `r` denotes a face dimension (06:632). It could be
    dropped.
  - `rem:qp:regret` writes "Section~\ref", which renders as capitalized
    "Section 2.6", while the surrounding cleveref text renders lowercase
    "section". The same remark already used "Proposition~\ref" in R4.
    Cosmetic only.

Required fixes: none.

## Verdict

**Scoped PASS** for the frozen successor `submission-addendum-r1` (manifest
`fc756e30…7f9`) and the supplied PDF `ac183170…b458`. This covers:
- the attribution changes in Sections 1, 5, 6, 7 and 9 against the supplied
  Luna contracts, including its superseding follow-up;
- the B10 withdrawal;
- the repairs for NEW-1, NEW-2, NEW-5 and NEW-6, and the already-resolved
  status of NEW-3 and NEW-4;
- the independently verified invariance of all other mathematical
  statements, displayed equations, labels, citations, the bibliography and
  137 proof blocks;
- the rendering of every changed passage in the PDF.

Optional items O1–O3 may be applied at the authors' discretion. None is
required for this verdict.

**Limits.**
- This is not a fresh proof audit of unchanged material. The R4 specialist
  and editorial reviews keep their own scopes.
- I did not read companion sources. Agreement with the companions rests on
  the Luna contracts.
- I did no literature search, so this review makes no worldwide-priority
  statement.
- I did not check the source archive or extraction that root is still
  building.
- I ran no build, experiment, CI or project-wide check.
- This verdict does not guarantee journal acceptance.

**Commands run.** All were read-only: `sha256sum`, `diff -rq` and
`diff -u` between snapshots, Python scripts for manifest hashes and for
environment, label, display and citation comparison, `pdfinfo`, `pdftotext`
on the changed pages, and `grep` on `main.log` and `main.blg`. I made no
source, TeX, bibliography or knowledge-base edits and did not delegate.
This file is the only output.
