# Post-addendum final review, Opus R2

Reviewer: fresh independent Opus reviewer, new delegated task (not a
continuation of the R1 review thread). Date: 2026-10-06. Scope: the R2
delta to the frozen addendum successor, and the transfer of the R1 verdict
to unchanged material by verified byte identity. This is not a fresh audit
of every proof and not a literature search. I did no browsing or literature
research, read no companion sources, ran no build, experiment, CI or
project-wide check, made no source edits and did not delegate.

## Target and identities

| Item | SHA-256 |
| --- | --- |
| `evidence/snapshots/submission-addendum-r2/manifest.json` (21 sources, predecessor `submission-addendum-r1`) | `0f1ff4db085a5d732b4e476309deafd2a2793225103a7a0773ae3ae84c2c2d94` |
| R1 predecessor `evidence/snapshots/submission-addendum-r1/manifest.json` | `fc756e30029d3d1d430b6e77e1d6b557bbb7e7d7a55b24599b95be5cd28b87f9` |
| `evidence/submission-addendum-r2.diff` | `f028ae9277f3a7047b336f7eafd7cc8e65fdebb818a92b3ef928c73cdf06fb98` |
| `verification/addendum-r2-source-comparison.json` | `785ce5b60ee0224131100470a350d0d4cbdd0d7ea525f0eeb1b62d3405920e62` |
| `evidence/companion-overlap-addendum-luna.md` (unchanged from R1) | `fbd34b464a1b4f3272fa667498510bc1e6aadb8c64786c963f53eaa64ce01d5a` |
| `evidence/reviews/post-addendum-final-opus-r1.md` | `76ae3e88f01524c8527a47dfffae5e3e1c3e267a011cbae04ab3b9d5c53f96fb` |
| `evidence/author-reports/attribution-addendum-opus-r1.md` (unchanged from R1) | `cc3b2cf8e88b096e0721a609886a76627e634f430fb48f378591f6a5fe253062` |
| `evidence/author-reports/late-math-repairs-opus-r1.md` (unchanged from R1) | `90b257595a20af06d8546242c168c302ecb0e71b0e18e4f62b6ee975c9172e2c` |
| `main.pdf` (182 pages, R2 build supplied by root) | `72dfac22092c60dcebd8f0b081b6baa27d37e35fde0a113e107b9437b2659e9b` |
| `verification/main-final.txt` (R2 text) | `dd8536217dca89aec6a6d1ef84fe859167050d069556c10c05e97f7e9798db96` |

## What I read

- The full brief `evidence/attribution-addendum-review-brief.md`.
- The full R1 review `evidence/reviews/post-addendum-final-opus-r1.md`,
  including its optional items O1–O3 and its limits.
- The R1 author reports' hashes (unchanged from those recorded in R1; their
  content was reviewed in R1 and is not re-reviewed here).
- The full R2 diff, and Section 1 lines 470–545 of the R2 snapshot (the
  decomposition-aware companion paragraph, the following enclosure
  paragraph and the start of the sparse-indicator paragraph).
- For the O2 premise: `sec:con:scope` (06:787–812).
- For the O1 claim: the closure-failure probability argument in
  Appendix D (D:284–296) and the closure-related passages of Section 9.
- PDF page 12 (rendered image and text extract) and page 11 text.

## Independent integrity checks

- **Manifest.** All 21 R2 manifest entries match both the R2 snapshot files
  and the live working tree (0 mismatches). The R1 snapshot also still
  matches its own manifest `fc756e30…7f9`.
- **Changed files.** `diff -rq` between the R1 and R2 snapshots shows only
  `sections/01-introduction.tex` (plus the manifest itself). `main.tex`,
  `macros.tex` and `references.bib` are byte-identical (`cmp`).
- **Diff file.** I regenerated `diff -u` of the R1 and R2 introductions. Its
  hunks are identical to the supplied `submission-addendum-r2.diff`: two
  one-line hunks, at R1 line 502 and R1 line 526.
- **Mathematical identity (my own script over all sections and
  appendices, R1 vs R2).**
  - Theorem/lemma/proposition/corollary/definition/example/remark/proof
    blocks: 329/329, byte-identical as a list; 138 proof blocks among them.
  - Displayed math blocks: 249/249, identical.
  - Labels: 410/410, identical lists.
  - Cited keys: 47/47, identical set.
  - Cross-reference commands: 1082/1082, identical list.
  - Neither changed line contains math, a label, a citation or a reference
    command; the adjacent `\cref{sec:con:scope}` is on an unchanged line.

  This independently confirms `addendum-r2-source-comparison.json`.

## Transfer of the R1 verdict

R1 passed the attribution changes in Sections 1, 5, 6, 7 and 9, the B10
withdrawal, the NEW-1/2/5/6 repairs (including the affine-margin proof),
the 137 unchanged proofs vs R4, and PDF rendering, for manifest
`fc756e30…7f9`. Because every source other than the introduction is
byte-identical to R1, and within the introduction only the two prose
clauses below changed, all R1 findings on statements, proofs, displayed
equations, labels, citations, bibliography and local attributions carry over
to R2 by verified byte identity. The Luna source audit is unchanged
(`fbd34b46…1d5a`, with its dated follow-up superseding the initial family-B
claim), and no source contract is touched by R2.

## O1 and O2 closure

**O1 (01:524–527).** R1 text: "…finite-noise margin tails, sound closure
tests, and an exact same-draw fallback and output." R2 text: "…finite-noise
bounds on closure failure, and an exact same-draw fallback and output."
- The phrase no longer lists closure tests as an addition, so it no longer
  suggests the tests themselves are new.
- The new phrase is supported by the formal content: e.g. Appendix D bounds
  the probability that closure fails at level `J` by `2ρ`, conditionally on
  every `η`, using the finite tails of `lem:count:finite-tails` and
  `lem:con:kkt`.
- No qualification is lost. The removed "margin tails" wording is the
  mechanism behind those bounds and is still stated in the next paragraph
  (01:534–536: the polynomial closure "reuses this type of enclosure and
  supplies finite-noise margin tails and an exact same-draw fallback"). The
  explicit credit of the companion's deterministic strongly convex face
  enclosure, its strict-complementarity and reciprocal-margin runtime
  premises, and "We re-prove the deterministic parts we use" are unchanged.
- No new claim is introduced: "bounds on closure failure" is a narrower,
  more precise statement than the R1 list item. **Closed.**

**O2 (01:501–502).** R1 text: "finitely many optimal coordinate
projections". R2 text: "a bound on the size of each optimal coordinate
projection".
- This matches `sec:con:scope` exactly: "a bound `r` on the number of
  distinct values that each coordinate takes over the optimal set, which is
  a separate premise". The size of the projection of the optimal set onto a
  coordinate is that number.
- The set-growth premise and the "accuracy-independent operation bounds"
  scope are retained, as is the `\cref{sec:con:scope}` pointer. The
  deterministic-only, not-integrated-under-noise qualification remains in
  Section 6.5. **Closed.**

**O3** (unused `r` in Section 6.5; capitalized "Section~\ref" in
`rem:qp:regret`) was retained by the authors as cosmetic. I agree: R1 marked
it optional, and it affects no claim. Not a defect.

## PDF check (R2 build)

- `main.pdf` SHA-256 `72dfac22…9b9e`, as stated by root; `pdfinfo` reports
  182 pages, the same count as R1.
- Both changed clauses render on physical page 12 (printed page 12), in the
  paragraph that begins on page 11. I inspected a rendered image of page 12:
  the paragraph is laid out normally, with no overfull lines or awkward
  breaks, and the references resolve ("(section 6.5)", "section 5.4").
- The full PDF text extract and the page 11–12 extracts contain no `??`.
  `verification/main-final.txt` contains both new phrases.
- `main.log` has no undefined-reference, multiply-defined or overfull
  lines. It has a few underfull-hbox notes, in a Section 4 table cell, a
  Section 8 table cell and the bibliography, none in the introduction or
  the changed passages. They do not affect the content.

## Concerns

None. Required fixes: none. No new optional items.

## Verdict

**Scoped PASS** for the frozen successor `submission-addendum-r2` (manifest
`0f1ff4db…2d94`) and the R2 PDF `72dfac22…9b9e` (182 pages). This covers:
- the exact R2 delta (two prose clauses in Section 1) and the closure of R1
  optional items O1 and O2, with no overclaim and no lost condition;
- the independently verified byte identity of all other sources and of all
  mathematical environments, proofs, displayed equations, labels,
  references, citations and the bibliography with R1, through which the R1
  scoped PASS transfers to R2;
- the rendering and layout of the changed passages in the actual R2 PDF.

**Limits.**
- No fresh proof audit; the R1 and earlier specialist reviews keep their
  own scopes.
- Agreement with the companions rests on the Luna contracts; I read no
  companion sources and did no literature search. This review makes no
  worldwide-priority claim and does not promise journal acceptance.
- I did not check the source archive repack or extraction, which root is
  handling separately.

**Commands run.** All were read-only: `sha256sum`; a Python script
re-hashing every manifest entry against the snapshot and the live tree;
`diff -rq` and `diff -u` between the R1 and R2 snapshots and comparison
with the supplied diff; `cmp` on `main.tex`, `macros.tex` and
`references.bib`; a Python script comparing environment blocks, displays,
labels, citations and references; `sed` and `grep` on the changed and
supporting passages; `pdfinfo`, `pdftotext` (pages 11–12 and full text),
`pdftoppm` for page 12, and `grep` on `main.log` and
`verification/main-final.txt`. This file is the only output.
