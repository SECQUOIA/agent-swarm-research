# Open items for the review round

Date: 2026-10-04. These items were `\TODO` notes in the LaTeX sources. They
were moved here so that they no longer print in the PDFs. Each item names the
text that relies on it. Status after round 1 (2026-10-04, adjudication item
G7-17): items 1 to 3 are resolved by separate agent sessions (not by persons
outside the authors), and item 4 is resolved except the O-8 readings, which
remain open; the resolution is recorded under each item.

## 1. Separate check of the extended-value proofs (Appendix B)

- Was: `sections/G-proofs-split.tex`, first paragraph.
- Needed: a separate check of the extended-value proofs of Appendix B, in
  particular the minorant induction (`app:splitproofs-minorant`) and the
  finite potentials (`app:splitproofs-cellwise`).
- Register: PT-06 (one confirmation pass of 2–4 reviewer-hours whenever these
  proofs are included); J-38.
- Relies on it: `thm:catmix-bound` and `thm:waterno2-bounds` use these proofs.
- **Resolved (round 1).** Two separate agent sessions checked the
  extended-value proofs of Appendix B and found them correct, without proof
  changes (`reviews/round1/sol-math-main.md`, `reviews/round1/opus-math-main.md`;
  adjudication G2-14). The paper's limitations say that no person outside the
  authors has checked any proof.

## 2. Review of the dyadic eg primal check

- Was: `sections/B7-eg.tex`, subsection `app:eg-primal`, after the paragraph
  on the slacks of the points.
- State: the library-free dyadic check
  (`development/dossiers/primal-points-checks/eg_dyadic_check.py`) has been
  read and rerun once by a second party.
- Needed: one review, with a saved log of its exponential test, before the
  paper calls the check reviewed.
- Register: EG-07, PP-02, C-54.
- Relies on it: the primal values of `thm:eg-bounds` (S1.7, `tab:eg-points`;
  S2, `app:points-instances`). The text describes the check and does not call
  it reviewed.
- **Resolved (round 1).** A separate agent session reran the dyadic check, read
  it in full and confirmed the three points (`reviews/round1/eg-dyadic/primal-rerun.log`);
  a separate exponential test (`eg-dyadic/exp_test.py`, log `exp-test.log`)
  checks enclosures and reciprocity at 452 arguments, because the built-in
  self-test skips reciprocity above 100 (`reviews/round1/sol-math-supp2.md`,
  adjudication G6-07, G7-10). S1.7 and S2 now say this.

## 3. Reviewer rerun of the second rocket proof and of the GAMS/OSIL comparison

- Was: `sections/E-audit.tex`, subsection `app:audit-rocket`.
- State: the second `rocket` proof and the exact GAMS/OSIL comparison were
  read and judged sound by the audit critique, and the section writers
  replayed them on copies on 2026-10-04 with identical results.
- Needed: the reviewer rerun that the register requires before the paper
  relies on them (`D/checks/audit/`, `D/checks/audit-r2/`; minutes).
- Register: C-44 (AU-03, AU-04, AU-15).
- Relies on it: Section 7 (the `rocket` refutations, `cor:audit-tolerance`(b))
  and S4 (`app:audit-rocket`, `app:audit-history`).
- **Resolved (round 1).** A separate agent session reran the second `rocket`
  proofs and the exact GAMS/OSIL comparison from clean copies: every inclusion
  test passed, the three brackets and the pinned counts 76/64, 151/127, 315/254
  reproduce, and the comparison gives 23 identical models, the `methanol50`
  exception and the three detections (`reviews/round1/sol-numbers.md`). S4
  records the reruns; the headline keeps 22 bounds on 18 instances
  (adjudication R-14, G7-08).

## 4. Further items noted in the same pass (not former TODOs)

- **Audit-priority sentence and audit-novelty search (round 1, opus-claims 23;
  closed in round 2, sol-verify U4 and opus-claims 14).** The paper makes one
  priority sentence about the audit (Section 1.4 and S3.1, qualified by "within
  the search"). The audit-novelty search is done: S3.1 lists the sources read
  for it. It is therefore no longer one of the open O-8 readings below.
- **Literature reading, register O-8.** The list of unread sources in S3.3
  (`app:literature-unread`) is final for the search that ended on 2026-10-04.
  Register O-8 asks for a reading of Ghaddar et al. 2015, Carøe–Schultz,
  Berenguel et al., Kocuk–Dey–Sun, Coffrin et al., Hansen 1992 and the
  Floudas handbook / McDonald–Floudas before any comparison or priority
  sentence in those areas. The paper makes no such sentence in these areas
  (the audit sentence above rests on the completed audit-novelty search). If
  any of these is read, update S3.3 and the sentences that name it (S1.6 last
  paragraph, S1.8 after `prop:waterno2-cells`, Section 6 on Hansen).
- **Claim index (resolved in round 1, G7-15).** `artifact/build_claims.py`
  now reads the status column of the register; the index was rebuilt after the
  round-1 edits and validated (counts in S7.1 and `artifact/logs/check_claims.log`).
  Any later edit to a hashed file makes it stale again: rebuild and validate
  after the last edit.
- **Artifact README (resolved in round 1).** The obsolete paragraph and the
  instructions to paper-editing agents were removed.
- **Claim index and artifact files (round 2, G7-01 to G7-07).** The register in
  S7.3 is compact (file names only); `artifact/RUNS.md` holds the full checker
  paths, commands, expected outputs and run records per row, and
  `build_claims.py` reads both, matched by row number (27 rows, equal labels).
  The builder keeps the `waterno2` displays, writes the status per instance
  (`eg_disc2_s`, the `etamac` and `pricing050` points: proved) and attaches
  recorded commands by working folder and script path. `artifact/HISTORY.md`
  holds the former S8 table of unsafe strings and the superseded displays that
  round 1 removed from S1 without a home (earlier `lnts` dual, two earlier
  `dtoc5` bounds, the `optcdeg2` progression, the earlier `camshape` code; build
  r3 open item 3). `artifact/RELEASE.md` takes the PDF hashes in the Build
  phase. The index must be rebuilt after the last edit of round 2 (G7-09).

## 5. Authors' confirmation of the Section 2.6 disclosure (build r3)

- Was: `sections/02-semantics.tex`, first paragraph of
  `sec:semantics-protocol`, a printed `\TODO` after "No person outside the
  authors has checked the code or the proofs."
- Now: the printed declaration placeholder in `sections/11-conclusion.tex`
  ("Use of AI tools") asks for this confirmation as well, so that only
  declaration placeholders print.
- Needed from the authors: confirm the AI-use wording in both places and the
  sentence on outside checks, and state in Section 2.6 which proofs or codes
  the authors read themselves. The records do not identify the model of every
  session; the text says so. Since round 2 (LD2-2) the wording also appears,
  identically in substance, in `artifact/README.md`.
