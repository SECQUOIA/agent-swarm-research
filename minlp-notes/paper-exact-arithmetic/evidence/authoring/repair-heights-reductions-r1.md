# Repair record: heights and reductions after the first manuscript review

Author: Opus main-revision writer. Date: 2026-10-05.

This record answers `evidence/reviews/heights-r1.md` and
`evidence/reviews/reductions-r1.md`, together with the nine unresolved items
the root listed. Line numbers refer to the files as they stand after this
repair.

Files edited: `sections/07-heights.tex`, `appendices/F-heights.tex`,
`sections/04-reductions.tex`, `appendices/B-reductions.tex`, and this record.
No other file was changed. In particular, `sections/08-fields.tex`,
`macros.tex`, `main.tex`, and `references.bib` were not edited. No literature
search, source browsing, or KB ingestion was done. No experiment,
mathematical script, project-wide check, or CI inspection was run. The
`paper-exact-arithmetic/` tree is untracked in Git, so the diffs below were
measured against copies saved in `/tmp/hr-r1-orig` before editing.

## Readiness

All nine listed findings are repaired in the text. Every theorem, lemma,
hypothesis, and proof step is unchanged, apart from the scope sentences named
below. No hypothesis was added. The four files keep their 110 labels and
their citation keys. No key was added or removed.

The repair is ready for integration. Five integration items remain: the
bibliography entries, the two commutator-prior-work citations, the open
source-locator checks, harmonization of the letter N, and any new finding
from the independent Opus R1 review that is still running. These are listed
at the end of this record.

## Responses to the nine listed items

### 1. Rational circuits cannot output irrational objects (heights-r1, P2)

Locations: `07-heights.tex:39–50`, `58–63`, `742–745`, `786–788`, and
`815–834`.

- Summary item (vi), lines 39–50, now states only the proved contracts. For
  every certified quartic, a polynomial-size shared rational circuit, built
  without a sign oracle, gives a strictly feasible point when the minimum is
  negative (Proposition `prop:upper-circuit-witness`). It gives a positive
  definite Gram when the minimum is positive (Theorem `thm:circuit-gram`).
  Over general certified quartics, validating either output is as hard as
  the exact decision. The item names the rational circle objects
  separately. It then says that a circuit with rational constants and
  operations has rational values, so it cannot describe the irrational
  optimizers and certificates of item (iii).
- The motivation paragraph, lines 58–63, had a parallel broad claim:
  "compact implicit outputs avoid it". It now names the same two outputs,
  which exist only when the certified quartic has them, and the constructed
  long rational optimizers.
- The opening of the shared-circuit subsection, lines 742–745, now says
  that the expanded lower bounds disappear "for two of the objects above".
- Lines 786–788 now say that validation costs are stated over general
  certified quartic inputs.
- A new paragraph at the end of the subsection, lines 815–834, covers the
  circle family. For `f_k` and `\tilde f_k`, k complex squarings compute the
  optimizer, followed by multiplications with powers of two for
  `\tilde p`. The entries of `ee^T` are monomials of degree at most four in
  the optimizer. `ee^T` is the optimal moment matrix and, up to a positive
  factor, every exposing matrix (Theorem `thm:heights-moment`(b),(e)). The
  maximal-rank Taylor Gram `T_p(A)` comes from the fixed formula
  `eq:heights-taylor-gram`. The entries of `C_U(p)` and `C_V(p)` are integer
  polynomials of degree at most two in p, so `T_p(A)` has a circuit of size
  polynomial in n, and hence in k. This is the only new positive statement,
  and it follows immediately from the displayed formula.
- The same paragraph states the negative direction from Theorem
  `thm:heights-moment`(c),(e). When the optimizer is irrational, no rational
  maximal-rank optimal Gram and no nonzero rational exposing matrix exists,
  so a rational circuit cannot describe them. Circuits with root gates are
  named as a different output model, and the section makes no claim about
  them. Nothing is generalized to algebraic circuits.

### 2. Validation hardness in the family table (heights-r1, P2)

Locations: `07-heights.tex:853`, `872`, and `882–890`.

The table cells for `g_k` and `h_k` now give only the circuit sizes. The
validation statements moved to prose after the table, lines 882–890.
Over general certified quartic inputs, deciding whether the circuit witness
satisfies `f(\hat x) < 0` is PosSLP-complete. That predicate is equivalent
to `min f < 0`, so the claim follows from `thm:quartic-complete`(i). Deciding
positive definiteness of the circuit Gram is PosSLP-hard. The prose also
says why the table cannot carry these claims: since `min g_k < 0` and
`min h_k > 0`, both predicates are always true on the displayed families. The
generic reductions in Section 7.7, items (i) and (ii), are unchanged.

The maximal-rank row also gains the circuit for `T_p(A)` from item 1,
`07-heights.tex:864–865`.

### 3. The initial circle point is not dyadic (heights-r1, P3)

Location: `F-heights.tex:448–451`.

The text now says that for j ≥ 1 the real and imaginary parts of `\hat z_j`
are dyadic rationals with `O(k + log(1/η))` bits and absolute value at most
two. The absolute-value bound holds because `|\hat z_j| ≤ |z_j| + e_j ≤ 1 + η ≤ 2`;
it justifies the bit count. The initial parts 3/5 and 4/5 of `\hat z_0` have
constant bit length. The induction, the error bound `e_j ≤ (3^j − 1)h ≤ η`,
and the running time are unchanged.

### 4. N for the Gram dimension (heights-r1, P3)

Locations: `07-heights.tex:96` defines `N = binom(n+2,2)`. All Gram-dimension
uses of D were replaced: 13 lines in Section 07 (lines 121, 462, 469, 472,
596, 600, 603, 606, 609, 681, 687, 702, and 762), and 34 occurrences on 29
lines in Appendix F (lines 6, 9, and 565–824). No D for the Gram dimension
remains in either file.

Conflict check: the only earlier N in these files was the local nonzero
integer `M_k^2 a^3 − (M_k^2+3) b^3` in the proof of `thm:heights-witness`. At
`F-heights.tex:341–349` it is now written out without a name, as in the
main-text sketch at `07-heights.tex:290–293`. The longer display was split
into an `align*` to avoid an overfull line. The inequality chain is unchanged.

Section 08 cites `sec:heights-conventions` only for z and w. It uses D
locally for radical degrees (`08-fields.tex:131–142`, `468–481`), which does
not conflict. Section 01 writes `binom(n+2,2)` without naming it
(`01-models.tex:464`). Harmonization is left to the root, as instructed.

### 5. Positive definite Gram of the block sum (reductions-r1, item 1)

Location: `04-reductions.tex:725–733`.

The paragraph now distinguishes the following cases.

- The block sum always has a rational positive semidefinite Hessian Gram,
  obtained by embedding the block certificates.
- When m ≥ 2, so that there are at least two nonempty blocks, no Hessian
  Gram on the full basis is positive definite. This is the cross-monomial
  argument of `rem:models-gram-kinds`.
- With a single block, F is itself a quartic of
  `thm:singleton-field`. For degree d ≥ 3 this is the power-coordinate
  quartic. For a rational root it is `(x−α)^2 + (x−α)^4`. In both cases part
  (v) supplies a positive definite rational Hessian Gram.
- For the empty list, `z^2 + z^4` is the case α = 0, and its Hessian Gram on
  `(v, zv)` is `diag(2,12)`, because `v^2 F''(z) = 2v^2 + 12 z^2 v^2`.

The proposition and its proof are unchanged. The text now notes that the
PosSLP upper bound uses only the supplied curvature bound `∇²F ⪰ I`.

### 6. Necessity claim after the naive-lifting example (reductions-r1, item 2)

Location: `04-reductions.tex:225–234`.

The blanket claim was that only a quadratic with a positive definite
quadratic part can dominate squared indefinite quadratics. It was replaced
by three statements:

- In the example, `ε(y − x^2)^2` contributes `−4εy` to `∂_x^2 H` at x = 0,
  which is unbounded below as y grows.
- The construction in this paper controls negative curvature with one
  additional square, that of a gate-specific exposing quadratic with
  positive definite quadratic part. After scaling, the whole sum is
  uniformly strongly convex (`lem:quartic-realization`(b)).
- This is a feature of the construction, not a necessary condition. The
  identity `(x^2 − y^2)^2 + (2xy)^2 = (x^2 + y^2)^2` gives a convex quartic,
  although both quadratic parts, `diag(1,−1)` and `[[0,1],[1,0]]`, are
  indefinite.

Proposition `prop:reductions-obstacles` and its proof are unchanged.

### 7. Bits of the first parameter radicand (reductions-r1, item 3)

Location: `B-reductions.tex:315–318`.

The text now says that the boxes and the first parameter radicand
`1 + 3δ_0^2 = 1 + 3·1000^{−2(Q+3)}` have O(Q) bits each, and that the
remaining radicand coefficients (1, ±3, 3/8, and the square-gate constants)
have constant size. With `Q = r_0 + r_1 + 9T + 1 = 12T + 7` and at most Q
gates, the total is still `O(T^2)` bits.

### 8. Derived parameters versus input constants (reductions-r1, item 4)

Location: `B-reductions.tex:1003–1010`.

"All constants" was replaced by an explicit list of the derived scale and
rounding parameters `ω_i, μ, Λ, β, ν, ε, t, η, h` and the rounded
coefficients `\hat p_i`. These have `O(k + N log N)` bits:

- `ω_i = 16^{−(i−1)}`;
- `ν = (4N)^{−(N−1)}`;
- `log(1/ε)`, `log(1/η)`, and `log(1/h)` are `O(k + N log N)`;
- each `\hat p_i` is a multiple of h with absolute value at most two.

The given rational generators may have coordinates of any bit length. They
enter the constant-gate residuals exactly. Every coefficient of G, of the
square factors of F, and of the canonical Hessian Gram is therefore
polynomial in the total input length. G is linear in the `\hat p_i`, in the
given constants, and in the `ω_i`. The factors divide by `tν` and `ν`. The
Gram entries are fixed degree-two expressions in the factor coefficients
(`lem:quartic-realization`(c)). The algorithm itself is unchanged.

### 9. Prior work on commutators and matrix circuits (reductions-r1, item 5)

Location: `04-reductions.tex:163–176`.

No vetted keys are available. `evidence/literature.bib` does not exist yet,
and `references.bib` has no Dawson–Nielsen or König–Lohrey entry. I
therefore inserted no `\cite` with an unresolved key. Instead:

- The prose now credits the prior work as described in the vetted
  `evidence/literature-review.md`, line 54. Commutators of near-identity
  rotations are used in the Solovay–Kitaev algorithm for approximate
  synthesis in SU(2). Identity testing for shared circuits over linear
  groups has also been studied. The text then states the difference, in the
  vetted report's terms: those works concern approximate synthesis and
  identity testing, and do not decide the sign of a designated rational
  coordinate in a fixed compact group.
- A `ROOT-CITE` comment at lines 167–172 records the exact insertion points:
  - after "synthesis in `$\mathrm{SU}(2)$`" (line 165): the Dawson–Nielsen
    citation, KB package `dawson2006-the-solovaykitaev-algorithm`,
    pp. 7–9;
  - after "has also been studied" (line 166): the König–Lohrey citation,
    KB package `konig2015-evaluating-matrix-circuits`, p. 9.
- Ben-Or–Cleve (1992) is not in the vetted literature report, so the text
  gives it no credit. The comment says to add it only after Luna
  verification.

The EY2010 sentence was settled in the same paragraph, at lines 154–157. It
now states the Luna-cleared contract that the root relayed: Lemma 5 reduces
PosSLP, with a circuit of linear size over {+, ×, /} whose gate values all
lie in (0,1), to an order comparison of that circuit's output. The key
`EY2010` in `references.bib` is the SIAM J. Comput. 39(6), 2531–2597 version.
I did not inspect the source. The text deliberately leaves the comparison
threshold unnamed, because the relayed contract does not give it. The
`LIT-REQUEST` comment for EY2010 was removed.

## Further repairs in the same files

- **The √2 X_1^2 example** (heights-r1, P2, in-file part):
  `07-heights.tex:208–210`. The remark said "positive Gram (√2)", which is
  positive definite only on the reduced basis (X_1). It now says that the
  polynomial has a positive semidefinite Gram over Q(√2), namely the matrix
  whose only nonzero entry is the diagonal entry √2 at the monomial X_1. The
  field argument is unchanged. Section 08 already says "positive
  semidefinite Gram" (`08-fields.tex:106`) and was not edited.
- **Jiang's parameter unit** (heights-r1, source contract 3):
  `07-heights.tex:416–419`. The old sentence called the parameter "a bound on
  the common denominator" but gave it the value `2^k log_2 5`, which is a
  logarithm. The sentence now makes no claim about units. It states the
  proved fact that the least common denominator of the coordinates of p is
  `5^{2^k}`. The citation and locator are unchanged and still need Luna's
  unit check.
- **The Gärtner–Magron–Vallentin margin** (heights-r1, source contract 2):
  `07-heights.tex:723–729`. The sentence no longer says "polynomial time when
  a lower bound ... is supplied with its encoding". It now holds whether
  that theorem depends on the margin value or on its bit length. For `h_k`,
  every lower bound on the least eigenvalue of a positive definite Gram is
  below `M_k^{−2^{k+1}}`. Its encoding alone therefore has more than
  `2^{k+1} log_2 M_k` bits. By part (c), every printed rational positive
  definite Gram of `h_k` has `Ω(k 2^k)` bits. The locator still needs Luna's
  check.

Checked and left unchanged:

- `rem:heights-cyclic-fields` ("does not exclude short circuit or other
  implicit descriptions") and the "Three limits" paragraph are non-claims.
- The circuit summaries in `00-introduction.tex:375–412` and
  `11-discussion.tex:36–49` are already format-specific.
- The Slot–Steurer–Wiedmer `LIT-REQUEST` comment at `04-reductions.tex:181–182`
  is still present. `literature-review.md`, line 50, already restricts that
  comparison to arXiv v1, as the text does. The root may delete the comment
  during bibliography integration.

## Residual integration items for the root

1. **Bibliography.** BibTeX reports 15 cited keys missing from
   `references.bib`, all pre-existing in the heights chapter:
   `BasuPollackRoy1996`, `BorweinWolkowicz1981`,
   `ChuaPlaumannSinnVinzant2017`, `GaertnerMagronVallentin2026`,
   `HeltonNie2010`, `Jiang2021`, `KolmogorovNaldiZapata2024`,
   `Laplagne2020`, `Lasserre2009`, `ODonnell2017`, `PatakiTouzov2024`,
   `PeyrlParrilo2008`, `RaghavendraWeitz2017`, `SafeyElDinZhi2010`, and
   `Zhang2020`. The reductions keys (`AllenderEtAl2009`, `TarasovVyalyi2008`,
   `EY2010`, and `SlotSteurerWiedmer2025`) are present. The duplicate
   versions `Lasserre2008`/`Lasserre2009` and
   `ChuaPlaumannSinnVinzant2016`/`...2017` still need harmonizing with
   Sections 00 and 08.
2. **Commutator citations.** Insert them at the `ROOT-CITE` comment,
   `04-reductions.tex:167–172`, then delete the comment. Ben-Or–Cleve stays
   out unless Luna vets it.
3. **Source locators still open.** heights-r1 lists six source-contract
   items. Item 1 is HeltonNie2010, Lemmas 7–8, and Lasserre2009,
   Theorems 2.6 and 3.3. Items 2 and 3 are the Gärtner–Magron–Vallentin
   Corollary 1.3 margin encoding and Jiang's parameter unit; the text no
   longer depends on either answer. Item 4 is PatakiTouzov2024 and
   Zhang2020, Example 2.5.3. Item 5 is Laplagne2020 and
   ChuaPlaumannSinnVinzant2017, Lemma 1.5. Item 6 is the version
   harmonization in item 1 above. The Basu–Pollack–Roy contract is cleared.
4. **The letter N.** Section 07 and Appendix F now use
   `N = binom(n+2,2)`. If the shared model reserves N, Section 01 may name it
   at `01-models.tex:464`. Section 04 uses its own local `N = Σ n_i` and
   `N = 4k`; these are defined in their statements, so a reader can tell
   them apart. The heights author report's recommendation to unify on D is
   superseded.
5. **Independent Opus R1 review.** It may add findings, which would need a
   new revision round.

## Checks actually run

All checks were scoped to the four edited files. None is a CI result.

- **Scratch build** in `/tmp/hr-r1-build`, outside the repository. The
  harness used the `main.tex` preamble, `macros.tex`, the four edited files,
  22 stub labels for references defined in other chapters, and a copy of
  `references.bib`. I ran `pdflatex` five times and `bibtex` once. Final
  result:
  - exit 0 and no LaTeX errors;
  - no undefined references and no overfull or underfull boxes;
  - 47 pages;
  - BibTeX reported only the 15 pre-existing missing keys above.
- **Label resolution** (inline Python). All 22 external labels used by the
  four files are defined in other chapter files on disk. None of my labels
  is duplicated anywhere.
- **Hygiene** (inline Python, compared with the `/tmp/hr-r1-orig` backups).
  No citation keys or labels were added or removed. Uncommented text has no
  match for the unfinished-text pattern of `verification/check_manuscript.py`
  and no repository path. There is no trailing whitespace, and final
  newlines are present.
- **Read-through.** I read the changed passages in the rendered output,
  extracted with `pdftotext`.
- **This record.** An inline Python check found no trailing whitespace, no
  control characters, and a final newline.
  `git diff --no-index --check /dev/null` on this file printed no whitespace
  error. Its exit status 1 only reflects that the new file differs from
  `/dev/null`.
- **Not run:** `verification/check_manuscript.py`, which checks the whole
  manuscript closure; any project-wide check; CI; experiments; mathematical
  scripts; and literature search.
