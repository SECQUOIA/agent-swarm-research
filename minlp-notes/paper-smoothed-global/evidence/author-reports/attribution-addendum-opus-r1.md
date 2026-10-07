# Attribution addendum, Opus main writer, round 1 (2026-10-06)

Scope: prose-only attribution corrections for the decomposition-aware
companion (`companion-decomposition-aware`), relative to the frozen
predecessor `evidence/snapshots/final-submission-r4` (manifest SHA-256
`0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061`).
No literature research was done. The only source used for the companion
comparison is the Luna audit `evidence/companion-overlap-addendum-luna.md`
(SHA-256 `d0f31e1edb7351beed62103050aaddc6a76ee16b3b3cb2750ef62dae1fce5e31`),
together with the user's addendum and root's precision notes.

## Withdrawal of the B10 novelty characterization

`evidence/author-reports/front-r1.md` described `prop:lim:conditional` (B10)
as "new as a manuscript statement". That characterization is withdrawn.
Root has added the dated withdrawal to that historical report; I did not
edit it. The correct account is:

- Parts (a) and (b) of `prop:sp:conditional` and of its corollary
  `prop:lim:conditional` specialize the retention and witness half of the
  companion's deterministic certified bag filter `thm:cr-filter`
  (`recourse-local.tex:7–77`) to scheduled sparse cells with error at most
  `a e_j`.
- Part (c), the expected near-optimal bag-grid tuple count under the finite
  law `U_{sigma,M}`, is not in the deterministic companion theorem and is
  the extension made here.
- No efficient oracle for general outside-value problems is supplied, by
  the companion or by this paper. The proposition remains a sufficient
  interface.

## Changes (line numbers in the edited files; R4 ranges in brackets)

All changes are running prose outside mathematical environments. No
theorem, lemma, proposition, corollary, example, definition, proof,
algorithm definition, equation, label, or bibliography entry was edited.
Only the five authorized section files and this report were written.

1. `sections/01-introduction.tex:489–503` [R4 489–490], decomposition
   companion paragraph. It now credits corrected coordinate grids,
   min-marginal dynamic programming on a tree decomposition,
   conditional-recourse filtering and boundary output. It names the
   deterministic antecedents: the value-function lemma for
   `lem:rec:value`(b); the exact-oracle core search for
   `prop:rec:search`(a)–(c); the certified bag filter for parts (a),(b) of
   `prop:sp:conditional` and `prop:lim:conditional`; and `ex:rec:star` as a
   member of the first star family. It also notes the TU coupling algorithm
   (certified approximation for fixed degree, exact output for rational
   quadratics), whose accuracy-independent operation bounds need set growth
   and finitely many optimal coordinate projections. It points to
   `sec:con:scope`.
2. `sections/01-introduction.tex:524–527` [R4 511–512]. The sentence
   "Our sparse theorem bounds expected counts ..." is replaced by: we
   re-prove the deterministic parts we use; the paper adds their composition
   under noise (finite-law expected counts without supplied growth,
   finite-noise margin tails, sound closure tests, exact same-draw fallback
   and output). The following face-enclosure paragraph is unchanged, so the
   credit that this closure type is reused from the companion is kept.
3. `sections/05-sparse.tex:596–599` [R4 596]. The (a),(b) versus (c)
   attribution now sits directly before `prop:sp:conditional`.
   `sections/05-sparse.tex:692` [R4 689–692]: the earlier copy after the
   proof was removed to avoid repetition. The prior-work paragraph
   (`sec:sp:prior`) is unchanged.
4. `sections/06-constraints.tex:789–803` [R4 789], opening of
   `sec:con:scope`. The exclusion now applies to general TU constraints on
   the searched coordinates, within this paper's smoothed guarantees only.
   It separates this from the positive TU recourse theorem `thm:int:tu`. It
   then describes the companion's deterministic TU results:
   - approximation certificates for fixed-degree objectives without growth,
     with accuracy-dependent table sizes;
   - exact output for rational quadratic objectives, terminating without
     growth or uniqueness, with a level bound under set growth;
   - accuracy-independent operation bounds that also need set growth and a
     bound `r` on the distinct optimal coordinate values. This is stated as
     a separate premise, not as a consequence of growth.

   It closes by saying that these deterministic bounds do not by themselves
   give expected work bounds under the noise, and points to `sec:sp:width`
   for the limits of integrating the available growth tail. The
   aligned-rounding and missing-count text that follows is unchanged.
5. `sections/07-recourse.tex:126–130` [R4 126]. After `lem:rec:value`:
   part (b) is the curvature part of the companion's value-function lemma,
   which also assumes a fixed recourse feasible set. The companion's growth
   part is not claimed.
6. `sections/07-recourse.tex:178–184` [R4 174]. After `ex:rec:star`: the
   example is a member of the companion's first star family, and
   `prop:lim:local` extends it to every draw of small noise and shows that
   no closure succeeds at level 0. The following sentence now begins "The
   proof of `ex:rec:star`" so that its referent stays clear.
7. `sections/07-recourse.tex:251–256` [R4 241]. After `prop:rec:search`:
   with an exact oracle, parts (a)–(c) are the retention, value-interval and
   witness guarantees of the companion's core search, whose separate query
   bound uses point growth. "Here we also allow certified oracle errors and
   bound the expected number of queries without a growth premise." The text
   does not claim CORE's global lower-bound record (part (d)), and it makes
   no priority assertion about the certified mode.
8. `sections/09-boundaries.tex:224–229` [R4 224–226]. Before
   `prop:lim:local`: the deterministic star example comes from the
   companion; the proposition adds every-draw persistence and level-0
   nonclosure.
9. `sections/09-boundaries.tex:298–301` [R4 295]. Before
   `prop:lim:conditional`: parts (a),(b) restate the companion's certified
   bag-filter guarantees; part (c) is the finite-law count of
   `prop:sp:conditional`(c).

## Luna audit claims used

- `lem:valuefunction(a)` ↔ `lem:rec:value(b)`: curvature inheritance only;
  companion part (b) (growth) is not ours.
- `thm:cr-search` ↔ `prop:rec:search(a)–(c)`; `prop:cr-growth` is a separate
  growth-conditioned query bound; CORE part (d) is not reproduced; the
  expected count without growth is the added statement.
- `thm:cr-filter` ↔ `prop:sp:conditional(a),(b)` and `prop:lim:conditional`;
  the count (c) is not in the companion theorem.
- `prop:star` family (A) is exactly `ex:rec:star`; family (B) is not
  reproduced; `prop:lim:local` is the small-noise every-draw extension.
- `thm:tu-states`, `thm:tu-approx`, `thm:tu-exact`: the premises as stated in
  item 4 above.
- Boundary closure (`thm:boundary`): the face-enclosure concept was already
  credited in R4; only the noise tails, fallback and expected composition
  are additional.

## Preserved qualifications

Unchanged: growth runtime formulas, the uniform-grid lower bound, the rETH
product-time scope, the inverse-growth integration obstruction in
`sec:sp:width`, the exact-arithmetic companion comparisons (cubic,
convexifier, quartic obstructions, output formats), the sparse-indicator
companion paragraph, and the P1–P5 resolutions of
`evidence/reviews/final-editorial-sol-r2.md`.

## Verification (targeted, local)

- An out-of-tree build (`latexmk -pdf -outdir=/tmp/sg-build main.tex`)
  succeeded. It reported one undefined reference, `prop:model:uniform`
  (cited at `01-introduction.tex:305` and `10-discussion.tex:71`). This
  comes from a concurrent edit to `sections/02-model.tex`, which is outside
  my scope. That file differs from R4 and no longer defines the label. I
  did not touch it. Root should resolve this before freezing.
- I diffed the five files against the R4 snapshot. Only the ranges listed
  above changed.
- No CI or project-wide checks were run.

## Remaining concerns

- The positive-definite star variant (`m=d^2` leaves) mentioned after
  `ex:rec:star` is left unattributed. Luna's family (B) uses bounded growth
  (`kappa < 11`, correction of order `sqrt(m) h`). The audit says family (B)
  is not reproduced, so I did not attribute the variant to it.
- The aligned TU rounding argument in `sec:con:scope` carries no companion
  credit. The Luna audit does not identify it as companion content.

## Final hashes (editing stopped)

| File | SHA-256 |
| --- | --- |
| `sections/01-introduction.tex` | `84fcae379b89a0a3ccdc5bfde536dc3209a0cde8e9d614a2f4721b2dabbfa415` |
| `sections/05-sparse.tex` | `1709549e2fa56a0b8adfbf24362cbf5774fb8b9deb5b8236a034c60945ecf60e` |
| `sections/06-constraints.tex` | `4673754153b8e86cb107464d1aa3f69fc26cf6ac22530816372a5a4579872efc` |
| `sections/07-recourse.tex` | `9eddfd741065e516cd86d4277e19a6f2d80c388a9ad319c15f563349c9b3a185` |
| `sections/09-boundaries.tex` | `99453c48a928b58ce2dc1167fe4dd214cf6dd8653898e67ad37480f826b2af4f` |

## Resolution of the two remaining concerns (2026-10-06, follow-up)

Scope of this follow-up: `sections/01-introduction.tex`,
`sections/06-constraints.tex`, `sections/07-recourse.tex`, and this report.
The basis is root's relay of Luna's correction. Luna's initial audit is
preserved as `evidence/companion-overlap-addendum-luna-initial.md` (SHA-256
`d0f31e1e…`), and Luna is appending the correction to the current audit.
No literature research, build, or background watcher was used in this
follow-up. The files `02-model.tex`, `04-quadratic.tex`, and appendix F
belong to another author and were not touched.

1. **Positive-definite star variant.** Luna found that the variant in
   appendix E (lines 840–856) is exactly the case `h=1/4`, `m=d^2`, `d>=8`
   of companion `prop:star` family (B). The objective, Hessian eigenvalues,
   `L=4`, `g=(3-sqrt5)/2`, `kappa<11`, the gap `d/16-3/8`, and the
   adjacent-node error variation `(d-1)h^2` all match. This corrects the
   earlier statement that family (B) is not reproduced. Changes:
   - `sections/07-recourse.tex:186–188`: the variant paragraph now says
     the variant is the case `h=1/4` of the companion's second, positive
     definite star family. No novelty is claimed for the construction.
   - `sections/01-introduction.tex:497–498`: the companion paragraph now
     says that its two star families contain `ex:rec:star` and the
     positive definite variant discussed after it.

   Appendix E is unchanged.
2. **TU rounding layer.** Luna found that the dyadic TU feasible rounding,
   the full-Hessian allowance, and the sound pruning in `sec:con:scope`
   specialize companion `lem:tu-round`, `lem:tu-allow`, and
   `prop:tu-sound`. Change:
   - `sections/06-constraints.tex:811–813`: one sentence credits this
     deterministic rounding, allowance and filtering layer to the
     companion. The classical integral-vertex fact keeps its existing
     Hoffman–Kruskal citation. The next sentence, unchanged, still says
     that the smoothed count, closure and tail estimates are missing.

All edits are running prose. No formula, label, statement, or proof
environment changed.

### Corrected current hashes (editing stopped)

These replace the hashes in the "Final hashes" table above.

| File | SHA-256 |
| --- | --- |
| `sections/01-introduction.tex` | `af1ba8282b410b5270395c7e3b3fc19e23009a5098b6b02ef85761a6a5c31e6e` |
| `sections/05-sparse.tex` | `1709549e2fa56a0b8adfbf24362cbf5774fb8b9deb5b8236a034c60945ecf60e` (unchanged) |
| `sections/06-constraints.tex` | `2d3c87b336c67119979bdb2d7794eeb5c155e912cc24631915281a4f0552dd46` |
| `sections/07-recourse.tex` | `381a032fbe829f8b023314c41ecfa7b22aad9a3247e9f15020178c95563d72fe` |
| `sections/09-boundaries.tex` | `99453c48a928b58ce2dc1167fe4dd214cf6dd8653898e67ad37480f826b2af4f` (unchanged) |
