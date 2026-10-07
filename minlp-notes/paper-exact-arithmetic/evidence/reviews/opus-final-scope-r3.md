# Opus final changed-scope review, round 3

Date: 2026-10-05, about 21:50–22:20 UTC. Reviewer: Opus review
sub-agent, new delegated round R3. It continues neither R2 nor any backing
thread.

Scope: the four presentation repairs requested by
`opus-wholepaper-r2.md`, read against the statements they summarize, and
the newly consolidated source-record rows.

This file is the only file I wrote. I edited no manuscript, bibliography or
evidence file. I ran no build, mathematical script, CAS, experiment,
historical diagnostic, project-wide check or CI inspection.

## 1. Verdict

**All four R2 findings are resolved. I found no new defect in the changed
manuscript passages.**

- The new text correctly summarizes the statements it points to.
- It adds no novelty claim.
- It drops no development.
- R2's mathematical acceptance still applies: the 25 source files outside
  the change set are byte-identical to R2's verified snapshot (Section 9).

**Source record.** The consolidated source rows exist. Each states the
inspected version, the locator, the contract, and which parts are imported
and which are proved in the manuscript. I raised two record-level items.
Neither changes a theorem, a proof or a body sentence.

- **S1 (P3), resolved during this round.** The Bombieri–Gubler row
  understated how the book is used: Appendix L cites it for the identity
  between Mahler measure and absolute height, not only for conventions.
  At 22:12–22:14 UTC, while I was writing, the literature report
  (`2bb82f75…`) and `FINAL-VERIFICATION.md` (`56689ef8…`) were updated
  to record this use. I checked the new row; it is correct (Section 5).
- **S2 (P3), open.** The Grigoriev–Pasechnik and Dedieu–Malajovich–Shub
  theorem numbers were checked in arXiv preprints, but they are printed
  against the journal versions. These entries lack the version note that
  Tarasov–Vyalyi and Luo–Zhang carry.

**Outside the changed scope.** While checking S2, I found one printed
bibliography defect:

- **B1 (P3).** Two titles print lowercase Roman numerals: "quadratic maps
  i:" in [48] and "part iii:" in [102].

**Readiness.** From this review's scope, the manuscript text needs no
further change.

- S1 is closed. S2 is a source-record completion for the literature lead
  and the root, possibly with two bibliography notes.
- B1 is a bibliography-only fix (braces in two titles). It changes the
  bibliography, PDF and archive hashes, so it needs a rebuild and a
  bibliography-scoped recheck, but no mathematical re-review.

This is an internal review, not external peer review.

## 2. Scope, baseline and method

**Files read.**

- The brief and the full R2 review.
- The repair response `authoring/repair-final-opus-r2.md`, in all three
  versions seen during the round. The last one records literature-report
  hash `2bb82f75…`.
- `STATUS.md`, in both versions seen during the round.
- `literature-review.md`, in both versions seen during the round
  (`52a8c944…` and `2bb82f75…`).
- `verification/FINAL-VERIFICATION.md`, lines 85–116, in both versions.
- `final-coverage.md`, row F8 and notes 215 and 227.
- The inventory rows for F8: `coverage-map.md`:78 and
  `authoring/fields.md`:29.

**Baseline.** The paper directory is untracked, so git has no history for
it. Byte-exact copies of the three R2-era files are in
`/tmp/exact-paper-submission-final-w6exg0zd/sections/`. Their hashes equal
R2 Section 11 (Section 9 below). I diffed them against the current files.

**Change set.** Exactly 3 of R2's 28 snapshot files differ. The other 25
are unchanged: `main.tex`, `macros.tex`, `references.bib`, Sections 01–07
and 09–11, and Appendices A–L. The diff has five hunks:

| File | Current lines | Change |
| --- | --- | --- |
| `sections/abstract.tex` | 30–35 | "and extend exact cone feasibility to explicitly represented algebraic data" is replaced by a sentence that names the field and fixes both the integer dimension and the Hessian-span dimension. |
| `sections/00-introduction.tex` | 205–209 | The sentence with the unclear "it" is rewritten, with a reference to `rem:recourse-quartic`. |
| `sections/00-introduction.tex` | 421–424 | Two new sentences: SOCP feasibility with unrestricted h is PosSLP-hard (`rem:models-socp`), h can grow with circuit size, and the theorem fixes t and h. |
| `sections/00-introduction.tex` | 573–575 | "the recorded finite rank computations do not establish that assertion" is removed. |
| `sections/08-fields.tex` | 750–753 | "Exact rank computations for n=2 and 4≤n≤16 are consistent with equality; they are recorded diagnostics, not part of any proof here." is removed. |

**Method.** I read each changed passage against the statements it
summarizes:

- Cone sentences: Appendix L opening (L:1–12), `eq:cone-field`,
  `eq:cone-system` and `eq:cone-span` (L:632–668), `thm:cone-feasibility`
  (L:670–679), `thm:cone-witness` (L:990–1005), the introduction's cone
  paragraph (00:406–424) and the discussion (11:54–63, 11:144–155).
- Hardness sentence: `rem:models-socp` (01:451–484) and the prior-work
  paragraph (00:805–819).
- Recourse sentence: `rem:recourse-quartic` (10:572–586), its proof
  (I:1965–1978), 10:31–34, 11:217–220, and the introduction's box-convex
  quartic summary (00:145–148).
- Fields passages: `thm:fields-descent` (08:649–668),
  `cor:fields-product-independence` (08:701–710), `prop:fields-cyclic`
  (08:737–748) and the summary item at 08:59–65.

I did not reread unchanged proofs. To keep this round independent, I did
not read the separate Sol final-scope review.

## 3. The four R2 findings

### Finding 1 (P2, abstract cone scope): resolved

The new text (abstract:32–35) reads:

> For second-order cone systems over one explicitly represented real number
> field, exact feasibility and witness recovery take polynomial time when
> both the integer dimension and the dimension of the span of the
> continuous Hessians of the squared cone residuals are fixed.

Each clause matches Appendix L:

- **Field.** `eq:cone-field` represents K=Q(α)⊂R by a dense primitive
  irreducible integer polynomial and a rational isolating interval. All of
  this is counted in L. "Real field" means a chosen real embedding (L:646).
  The field is part of the input, not fixed in advance, so the sentence
  makes the stronger claim, and Appendix L proves it.
- **Integer dimension.** In `eq:cone-system`, w=(z,x)∈Z^t×R^n, so t is the
  number of integer variables.
- **Span.** Each squared residual is q_i=‖u_i‖²−t_i², and its continuous
  Hessian is H_i=2(A_ix^T A_ix−c_ix c_ix^T). Then h=dim_K Span_K{H_i}.
  L:663–668 shows that this equals the real span rank, so the abstract
  needs no field qualifier. Only the rational span can differ, and no
  reader would assume that span for K-valued matrices.
- **Polynomial time for fixed t and h.** `thm:cone-feasibility` gives
  polynomial Turing time for each fixed t and h; the exponent may depend
  on them. `thm:cone-witness` gives L^{C_h} time for continuous systems
  and polynomial-time recovery of a full feasible point for fixed t and h.
  "Witness recovery" names exactly that statement.
- The word "extend", which implied an unstated prior result, is gone.

The abstract now agrees with 00:406–420, 11:58–61 and 11:148–152.

*Checked, no change needed (O1).* The abstract says "integer dimension"
but not "mixed-integer". Every reading is still true:

- A reader who takes the systems as continuous gets the special case t=0.
- A reader who misreads the phrase as the ambient dimension gets a weaker
  claim than the one proved.

The introduction defines t at 00:407–408.

### Finding 2 (P3, unpublished rank computations): resolved

Both sentences are gone. The remaining text reads correctly:

- 00:573–575 says that the dimension and product-independence statements
  hold for n≥4, and that "Whether the products exhaust the stationary
  quartics for all these points remains open."
- 08:750–757 says that n=3 fails and that equality at all cyclic points is
  open. The next sentence, "If the equality holds for a given n≥4, then
  Theorem~\ref{thm:fields-descent} shows ...", follows directly.

The surrounding results are unchanged and still consistent with this text:

- the conditional `thm:fields-descent`;
- `prop:fields-cyclic`, which gets dimension and product independence
  through `cor:fields-product-independence`, with the cyclic quartic of
  `thm:algebraic-cyclic` as the baseline;
- the summary item at 08:59–65.

A text search of all 25 included TeX files finds no other mention of rank
computations, diagnostics, "n≤16" or recorded computations.

**No development was dropped.** The inventory row F8 (`coverage-map.md`:78;
`authoring/fields.md`:29) is the descent criterion with product
independence. The finite cyclic computations were labelled as context and
were never a result. The final coverage row F8 now says "stationary
equality not claimed for all n". The open equality is a research question,
not a proof gap: no theorem uses it as a premise.

*Checked, no change needed (O2).* At 00:573–574, product independence is
called a "hypothesis". In Section 08 it is proved as a consequence of the
dimension hypothesis and the baseline (`cor:fields-product-independence`).
Read with the next sentence, the meaning is clear: dimension and
independence hold, and exhaustion is open. This sentence is unchanged, and
R2 accepted it.

### Finding 3 (P3, unclear "it"): resolved

The new text (00:205–209) reads:

> For residual quartics no full-point guarantee of this form is expected:
> such a guarantee, applied after adding a dummy core to the box-convex
> quartic reductions above, would give a Las Vegas algorithm with expected
> polynomial running time for Square Root Sum and for PosSLP
> (Remark~\ref{rem:recourse-quartic}).

- "Such a guarantee" refers unambiguously to the full-point guarantee
  named just before it.
- "The box-convex quartic reductions above" are the ones at 00:145–148,
  where accuracy 1/4 decides Square Root Sum or PosSLP.
- The remark (10:572–586) takes a quartic F from
  `thm:points-quartic-lower` and adds a dummy core: f(v,y)=v²/2+F(y), with
  Λ=1. It states the conditional Las Vegas consequence for the source
  problem, which is Square Root Sum or PosSLP.
- The proof (I:1965–1978) supports "expected polynomial running time". It
  takes q=2, k=1 and σ=1, so the factor (1+Λ/σ)^k equals 2, and each draw
  uses log₂M fair coins.
- "Is expected" keeps the remark's status as a conditional statement, not
  a hardness theorem.

The sentence agrees with 10:31–34 and 11:217–220.

### Finding 4 (P3, cone theorem versus SOCP hardness): resolved

The new text (00:421–424) reads:

> Exact second-order cone feasibility with unrestricted h is PosSLP-hard
> (Remark~\ref{rem:models-socp}); in those gate constructions h can grow
> with the circuit size. The polynomial-time bound here fixes both t and h.

I checked by hand that this follows from `rem:models-socp` (01:451–484).
The construction has only continuous variables, so t=0. Write each 2×2
block [[a,b],[b,c]]⪰0 as ‖(2b,a−c)‖≤a+c. Its squared residual is 4b²−4ac.

- **Dual program for A.** Each squaring gate g has its own block variables
  (a_g,b_g,c_g). The residual's Hessian has entry 8 at (b_g,b_g) and −4 at
  (a_g,c_g) and (c_g,a_g), so it is supported on that gate's variables.
  Distinct gates have disjoint supports. Hence h is at least the number of
  squaring gates of A.
- **Primal program for B.** The block [[2x_i,x_j],[x_j,1]] has squared
  residual 4x_j²−8x_i and Hessian 8e_je_j^T. These Hessians are
  independent across distinct squared gates.

So h grows linearly with the number of squaring gates, and "can grow" is
an understatement. Because t=0 throughout the hard family, the sentence
correctly attributes the whole difference to h.

The sentence uses t and h exactly as the same paragraph defines them
(00:407–409). It agrees with the prior-work paragraph (00:805–819), which
credits the hardness to Tarasov–Vyalyi.

## 4. Other checks on the changed passages

- **Novelty.** The changed passages contain no novelty or priority
  wording. The cone result is stated as a result, and 00:418–420 credits
  its sampling and fixed-dimensional integer ingredients to prior methods.
- **References.** Both new references resolve to unique labels:
  `rem:recourse-quartic` at 10:573 and `rem:models-socp` at 01:452.
- **Counts.** Over the 25 included TeX files there are 658 labels, all
  unique, and 1,768 reference commands: R2's 1,766 plus the two new ones.
  No key is unresolved. These counts match the repair response.
- **Hygiene.** The three changed files have no TODO-type markers, comment
  lines, repository paths, trailing whitespace or tabs. Each ends with a
  newline. `\begin` and `\end` balance: 1/1, 5/5 and 34/34.

## 5. Source-record rows

The literature report has the three rows at lines 88–90 of its "Source
contracts used by the proofs" table, and line 95 adds a textbook paragraph.
I first reviewed version `52a8c944…`. At 22:12:55 UTC it was replaced by
`2bb82f75…`, which only rewrites row 90 (see S1). Rows 88–89, line 95 and
the "Unretrieved source content" list read the same in both versions, so
the lines cited below hold for both. I checked what the record states, not
whether the sources say it. I did no literature research.

**Grigoriev–Pasechnik (row 88).**

- Version and locator: Theorem 1.2, printed pp. 2–3, inspected in arXiv
  `cs/0403008`. The journal version is *Computational Complexity* 14(1),
  2005.
- Contract: the theorem samples every connected component of
  {p(Q(u))=0}, allowing degenerate and unbounded sets. Degree and bit
  bounds are (dr)^{O(h)} times the input size.
- Imported versus proved: the face reduction, the zero-dimensional chart,
  the coefficient accounting, the common-field output and the radius are
  manuscript work. Theorem 1.5 is not used.
- Match with the manuscript: yes, at L:96–106, L:125–128, 00:392–396,
  00:903–907 and 01:656–657. L's bound (2d)^{O(h)} is the row's bound with
  deg p=2 and r equal to L's chart dimension d. For the version, see S2.

**Dedieu–Malajovich–Shub (row 89).**

- Version and locator: §5, Theorem 5.1, p. 10, inspected in arXiv
  `math/0312083v2` (19 July 2004). The journal version is *Foundations of
  Computational Mathematics* 5(2), 2005.
- Contract: over an algebraically closed field of characteristic zero, the
  number of isolated common roots is at most
  [U^{N1}T^{N2}]∏(e_iU+e'_iT). Positive-dimensional components are
  allowed.
- Imported versus proved: the KKT bidegrees, nonsingularity,
  specialization and passage to the algebraic closure are manuscript
  work.
- Match with the manuscript: yes, at J:469–484. J also adds an embedding
  argument from C, which covers J's use even if the source states only
  the complex case. For the version, see S2.

**Bombieri–Gubler (row 90).**

- Version and scope: Cambridge University Press 2006, Chapter 1. Only the
  publisher's chapter record was checked, and the row makes no
  theorem-number claim. In `52a8c944…` the row listed §§1.3–1.5. In
  `2bb82f75…` it also lists §1.6, on polynomial height and Mahler measure.
- Contract: absolute values, the product formula and the absolute Weil
  height. `2bb82f75…` adds the Mahler identity used in L.
- Imported versus proved: J.1 prints its conventions, and
  `lem:qc-heights` proves the inequalities.
- Match with the manuscript: in `52a8c944…`, only in part, because the row
  covered J:150–166 but not L:345–351. In `2bb82f75…`, yes. See S1.

**Textbooks (line 95).** The paragraph says that editions and metadata
were checked, that Hoffman was read, and that Deimling and Eisenbud (1995)
were not recorded. It states each book's role. It is honest. It does not
say for each book whether the printed theorem numbers were checked in the
text. This applies to Rockafellar, Hartshorne, Neukirch, Davenport,
von zur Gathen–Gerhard and Kozlov–Tarasov–Khachiyan. The root may add one
clause; I do not raise this as a finding.

### S1 (P3, record accuracy): Bombieri–Gubler is also cited for a quantitative identity. Resolved during this round

**Location.** L:345–351, in the proof of `lem:ncq-common-field`:

> If p_ξ is its primitive integer minimal polynomial, the identity between
> Mahler measure and absolute height~\cite{BombieriGubler2006}, followed by
> expansion in the roots, gives log‖p_ξ‖∞≤De(W+2log2).

**Problem, as reviewed in `52a8c944…`.** Row 90's title covers
Appendices J and L, but its text describes only J's uses. It says the
citation "is limited to the stated conventions and section scope", and
that the full chapter "is not stored as a read KB package".
`FINAL-VERIFICATION.md`:112–113, in version `b7720fac…`, said the same:
"Bombieri–Gubler is used for height conventions; the quantitative height
inequalities used later are proved in Appendix J."

The L step instead imports the identity log M(p_ξ)=[Q(ξ):Q]·h(ξ) for the
primitive minimal polynomial. This is a quantitative fact, not a
convention. J's own minimal-polynomial bound, `eq:qc-minpoly-height`, uses
a different argument (Gauss's lemma and Cauchy's bound on an annihilating
integer polynomial), and L does not use that bound at this step.

Earlier records recognized this import:

- `prewrite-quadratic-contrast.md`, item 10, lists "primitive polynomial
  Mahler-height estimates" among the height imports;
- `nonconvex-r1.md`:38 checked "the new existing-source Mahler-height
  citation".

The consolidated row dropped this use. R2's Section 8 table also said
"conventions only", so R2 missed it as well.

**Effect.** The mathematics is unaffected. The identity is standard, the
manuscript prints no locator, and the displayed bound follows from it as
written: the coefficients are at most 2^δ·M(p_ξ), with δ≤De. The problem is
only that the record understates what the manuscript takes from a book
whose chapter text the record says was not read.

**Repair needed.** Record only: add the L use to row 90, with the row's
existing access status (chapter-level citation, no locator, full text not
read), and make `FINAL-VERIFICATION.md` match. No manuscript change is
needed.

**Resolution, checked.** At 22:12:55 UTC, while I was writing, row 90 was
rewritten (report `2bb82f75…`):

- It is retitled "Absolute heights and Mahler measure for Appendices J
  and L".
- It states that L:346–351 cites log M(P)=[Q(ξ):Q]h(ξ) for the primitive
  minimal polynomial P(X)=a∏_σ(X−σξ).
- It places the Mahler-measure material in §1.6, citing the publisher's
  chapter record, and asserts no theorem or page locator, because the
  chapter was not inspected.
- It derives the identity: primitive P has Gauss norm 1 at each finite
  place, so |a|_v∏_σ max(1,|σξ|_v)=1, and summing over all places gives
  log|a|+Σ_σ log max(1,|σξ|)=log M(P).

I checked this derivation by hand, and it is correct. Multiplicativity of
the Gauss norm gives the finite-place equality. The product formula for
the integer a turns the finite places into log|a|. At the archimedean
places the conjugates are the complex roots of P.

At 22:14:22 UTC, `FINAL-VERIFICATION.md` (`56689ef8…`) was updated to the
same effect, and the repair response (`42df4a53…`) records the new report
hash. S1 is resolved, with no manuscript change.

### S2 (P3, version and locator): two journal citations carry theorem numbers checked only in preprints

**Location.**

- `\cite[Theorem~1.2]{GrigorievPasechnik2005}` at 00:394, 00:905, 01:657
  and L:100;
- `\cite[Section~5, Theorem~5.1]{DedieuMalajovichShub2005}` at J:480.

**Problem.** Rows 88–89 record that these theorem numbers were checked in
the arXiv preprints. The printed entries show only the journal versions
(`main.bbl`; PDF reference [48] for GP), and plainnat does not print the
`eprint` field. The record does not say whether the journal numbering was
checked. `bib-review-d-k.md`:11 and :26 record only that the metadata
agree.

The report's own rule (line 53, Basu paragraph) is to cite the version
whose numbering appears in a statement. The paper follows that rule for
`TarasovVyalyi2008` and `LuoZhang1999` with a printed note. In addition,
line 116 calls the "Unretrieved source content" list complete, but neither
journal text is on it.

**Effect.** If the journal numbering differs, a referee who follows the
printed citation finds the wrong theorem. No mathematical content is
affected.

**Repair.** Either:

- the record states that the numbering was confirmed in the journal
  versions; or
- both entries get a version note like `TarasovVyalyi2008`'s, and both
  journal texts are added to the unretrieved list. The note is a
  bibliography-only change, with no body change.

The root decides. I did not research the sources.

## 6. Incidental finding outside the changed scope

### B1 (P3, bibliography typography): lowercase Roman numerals in two titles

plainnat converts titles to sentence case, and two titles have unbraced
Roman numerals. Both errors appear in `main.bbl` and in the text of the
built PDF:

- [48] `GrigorievPasechnik2005` prints "Polynomial-time computing over
  quadratic maps i: Sampling in real algebraic sets" (`main.bbl`:408).
- [102] `Renegar1992QE` prints "... theory of the reals. part iii:
  Quantifier elimination." (`main.bbl`:842).

**Repair.** In `references.bib`, brace the numerals: `Quadratic Maps {I}:`
and `{Part III}:`. Then rebuild and refresh the archive and hash list.

This is outside the changed scope and does not affect the mathematics. It
does not contradict `FINAL-VERIFICATION.md`:107–108. That statement's
"volume part" is "volume 46, Part 1" (`main.bbl`:295), which prints
correctly.

## 7. Limits

- **Changed scope only.** I did not re-review unchanged proofs. My
  acceptance of the mathematics around the changed passages rests on R2's
  reconstruction and on the 25 unchanged files being byte-identical.
- **Records, not sources.** S1 and S2 concern what the record states. I
  did not check any source's content, any journal numbering, or where
  Bombieri–Gubler states the Mahler identity.
- **Hand checks.** The growth argument for h in Finding 4 is a hand
  reconstruction from the remark's construction. No CAS or script was
  used.
- **Independence.** I did not read the separate Sol final-scope review.
- **Moving records.** No manuscript source, bibliography or build output
  changed during the round. The archive was rewritten at 21:50:40 UTC, as
  the round began. It has not changed since then, and Section 9 records
  that version. The records did change:
  - The literature report changed at 21:55 UTC (`52a8c944…`), which I
    reviewed, and again at 22:12:55 UTC (`2bb82f75…`). The second change
    rewrote only row 90. I reread rows 88–90 and the unretrieved list in
    the final version.
  - `FINAL-VERIFICATION.md` and the repair response changed at 22:14:22
    UTC. I reread the changed passages.
  - `STATUS.md` and `verification/SHA256SUMS` changed earlier in the
    round. At 22:16 UTC, `SHA256SUMS` matched all 32 of its listed files.
  - Any later record edit is outside this review.

## 8. Targeted checks actually run

All checks were read-only and local. None is a CI result. I ran no build,
compile, CAS, mathematical script, experiment, historical diagnostic or
project-wide check.

- `sha256sum -c` of R2's 28-file Section 11 snapshot: 25 match, and 3
  differ (abstract, 00, 08). Rechecked at 22:09 UTC.
- `sha256sum` of the three changed files: equal to the repair response's
  snapshot.
- `diff -u` between the R2-era copies in
  `/tmp/exact-paper-submission-final-w6exg0zd/sections/` and the current
  files.
- `sed`, `grep` and `awk` reading of the passages listed in Section 2 and
  of the evidence records named there.
- `grep` over the 25 included TeX files:
  - label and reference counts and resolution (658 labels, 1,768
    references, 0 unresolved);
  - remaining wording about diagnostics or rank computations;
  - uses of the `GrigorievPasechnik2005`, `DedieuMalajovichShub2005` and
    `BombieriGubler2006` keys.
- `grep` hygiene and wording scans on the three changed files.
- `sha256sum -c verification/SHA256SUMS`: 32 of 32 OK at 22:09 and
  22:16 UTC.
- After the record changes, at 22:16 UTC: the hashes were rechecked, the
  25 unchanged sources and the 3 changed files still matched, and
  `references.bib`, `main.bbl`, `main.pdf` and `submission-source.zip`
  were unchanged. I reread rows 88–90 and lines 114–132 of the final
  report, `FINAL-VERIFICATION.md`:108–116 and the repair response.
- `pdftotext -layout main.pdf` into `/tmp`, then `grep` for the two
  bibliography titles. This only extracts text; it is not a build.
- For this report: `git diff --no-index --check /dev/null` on this file.

## 9. Reviewed hashes

Manuscript sources at the end of the review. The 25 files outside the
change set equal R2 Section 11.

```text
42d390dfbeba1fd2459f150f1ce52901c91420d45e8799dc2ae9ef00a1be3d2b  main.tex
1eb51a834c6285ec54212db5dffc0e85c7d0c59a131df32cd7741cc2a273ebf8  macros.tex
20dbe6573a5b4be6749c6c188a6adbfe3a123e21d7599d14a07ca1fd67e3f7a5  references.bib
491f90e98658426866e4755c8b3b5f4d84d85569f02e083241d5f2cdd4a7cca8  sections/abstract.tex
32a473010509ff4930f8dfa4d67fd1f1efdf014723c23fba142967a388f17f92  sections/00-introduction.tex
f1883295ee64b7b75e17d2c86d26202169f852741934095a4efcff718d900fb0  sections/01-models.tex
9255c3b578fbef9981d96873db3effe3a0f65345fcab796bbed3e16d1f88e010  sections/02-points.tex
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
0216cf2456eb982b40ea206dcb9f0fe4739eefd9b7b029d7b786b38a9599dc9e  sections/05-constraints.tex
cec67b102b0aef0b3a03f1f00abb8ed79cd1dd128f2fac50a0c7d2190a8ea0bb  sections/06-algebraic.tex
2cfaf3f0c8a4e6c144f3fb8b241bcdcba7a3683167c55adac4ea641a8090bbe1  sections/07-heights.tex
1c3b8d8123348933fecdae6a5b6ed677ef6ffc46010782b0005999e925e121be  sections/08-fields.tex
200313954066e5071cf3a25ec9d0f5c7a28e252b375297f2b9ec5a0515165c98  sections/09-certificates.tex
e38150a05d990980800c9e29724c6dcbe011932167b8331ff7ad88fffbe6b6b1  sections/10-recourse.tex
63252f4d6614dca06df90fa9476a6408ed6f8fb43eaeae9000ec77d0fec97440  sections/11-discussion.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
0469412f5fc0bb8a9122329e673a30690a2c6ddf9eb577f3844e7b39f04bde90  appendices/C-points.tex
3e7a43c5d884a915d99d0e9f46026d0d77ef1403ec04ab0157c4da03b194130e  appendices/D-constraints.tex
9fe8e892b59bccab190e7ba51eac50bb8c41faa97ca24bf7631c9a0484fa8b03  appendices/E-algebraic.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
0c4ddf55ba158ccd8c3857002eaea8805d15373d183f46b785777d50117cfeb1  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
f4c21d1ad36fac74449315f3b4a20c4c1652e41e50797e657796c8b0e526d155  appendices/I-recourse.tex
5d01e18401f2fde9d3c2e62d0dde59784101b923ed84980b972266b15e01b3d9  appendices/J-quadratic-contrast.tex
ed88ea5a7c14d38370861141adb3a613a41f7e2cfd4fef42ef663af098568b82  appendices/K-boundaries.tex
6ba31da31c905495c68e575ea27c914efd82dae83b7796857d611530dafe0059  appendices/L-further-arithmetic.tex
```

The R2-era baselines I diffed against, from
`/tmp/exact-paper-submission-final-w6exg0zd/sections/`. These equal R2
Section 11.

```text
2dce96e179d21f96ed1b240bf17e040803b440c88013e8cce2d41b34f96d9537  abstract.tex
697822ed8c772532c85172845cce06742c6a07dd18591d393f8fa55a0506c96b  00-introduction.tex
b05a1d5d0323344ce05eb679f4ac8651dca7cdea96360f5bdb549aeb46e4324e  08-fields.tex
```

Evidence and build files at the end of the review (22:16 UTC):

```text
2bb82f75647aeffc4d69aa9fc50e4e5e9911996f6ef6609484f3c261cada927b  evidence/literature-review.md
42df4a53e8f01c758f591ad98464d04d5dedc57cf920fe0cbb8eeb0e55ca7838  evidence/authoring/repair-final-opus-r2.md
56689ef87b4a26cf47f8d908d334e5c9415f19fa1b4cc234450aa183d11dc721  verification/FINAL-VERIFICATION.md
9cf613ff2bff51e83636a46f4df4e08f10af8bd6a277b9f927456ea384f58315  verification/SHA256SUMS
2c80891cd1066932e70d88f6978d0e78df66a336468170c9842da98c9158e65a  evidence/reviews/opus-wholepaper-r2.md
bcca8b1b6c5d233baa1ab25806bd0a172e8a284a5f0285b2902ad6e167051d97  evidence/STATUS.md
acb7cf21bfe20a5420b831f049c9ed4d90705c0e2a51f1599530766f2140852b  evidence/final-coverage.md
a082c8cf5edc79b05b9a6d5f2db845ba71b0a074aea5c2aed68e0286fd024f32  main.bbl
88920c22ec5571d92ac9289aa04a0fa6d5208d696f13a2a164f63ee2d973a356  main.pdf
f0bbe8a99332223d97a5d427852cd2ffcafb5b4080c1ad037c76e35936704396  submission-source.zip
```

Earlier record versions reviewed during the round:

```text
52a8c9447b30fd066d87501965575d923f3615039a891eae02942eaab635218f  evidence/literature-review.md (21:55 UTC version)
b7720fac9209d9eaa8dd939d7af7d7918a24978157cbce6291fb67268b1b216d  verification/FINAL-VERIFICATION.md (pre-22:14 UTC version)
24f52be6c9cf62c8a6de5a9adbed110151064b7b8d71a6de16576522ec4a6c4a  evidence/authoring/repair-final-opus-r2.md (pre-22:14 UTC version)
```
