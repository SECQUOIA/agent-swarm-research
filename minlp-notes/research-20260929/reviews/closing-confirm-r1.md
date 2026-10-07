# Closing confirmation, round 1: the closing revision of the September 29 continuation

Date: 2026-09-30. Reviewed: the closing revision that answered the round-1
closing-audit findings (A1–A41, B1–B38). It covers the root documents
(`SYNTHESIS.md`, `closing-research-results.md`, `open-instances-summary.md`,
`README.md`, `PROGRAM.md`, the repository README paragraph) and the notes
whose status lines or remaining review items were edited. I did not write
any of this material. I checked each finding against the current text and
against the notes and reviews it cites, judged each refusal, and looked for
claims made stronger than their sources. I edited no file and committed
nothing.

*Provenance note.* The agent's tool environment did not allow `.md` report
writes. It returned this text for the root to save verbatim.

## Verdict

**Fixes needed (minor).**

- Every finding is resolved in substance.
- Every refusal and deviation is justified (Section 2).
- I found no strengthened claim except one. A sentence added for A3 says
  that every displayed dual bound in the summary table is itself a valid
  bound. This is false for the four camshape rows, by 2e-15 to 4e-15 (R1).
- One status table still says three proofs are "not re-checked", although
  the confirmation checked them (R2).
- One README table row does not render its verification links in
  GitHub-flavoured Markdown (R3).
- Three small wording residues remain (R4–R6).

## 1. Findings checked

| Findings | Checked against | Result |
|---|---|---|
| A1, B1 (tree sandwich) | consistency note, Summary (B), Section 3 Remarks, Section 7.4 | resolved. Upper end attained in T1 at `K = 0`; lower end attained numerically in 515 of 900 T3 cases; in T1 approached as `K` grows and proved not attained at finite `K` |
| A2 (one independent check each) | audit status table; `bound-audit-recheck.md` Section 1 | resolved in SYNTHESIS §5, the summary and the README row |
| A3 (outward rounding) | exact comparison with `cops-verification`, `catmix-recheck` and `open-instances-verification` values | chain, catmix and lnts100 resolved. The new header sentence is false for the camshape rows (R1) |
| A4 | bang-bang report, Section 9.2 | resolved |
| A5, A24, B7 (open questions) | face-exact Summary; extension-adaptive Summary and Sections B.5–B.6; coupling Theorem 4.5 | resolved |
| A6, A26, A35 (PROGRAM.md) | table ratios 4.9, 4.2, 6.5 and 8.4, 3.1, 4.9; scaling study Summary and §1.3 | resolved |
| A7, B2, A27 (Evidence bullet) | scaling study lines 31–37; face-exact Summary item 7; census | resolved |
| A8 (split table) | summary structure; 28 rows counted | resolved |
| A9, B22 (verification paragraph) | each named note's header and dated root entry | resolved, apart from one stale status table (R2) |
| A10, A38, B38 (README links) | link check | resolved in the text; one row does not render (R3) |
| A11 (tolerance-feasible primals) | open-instances verification (lnts 4.7e-15 to 6.7e-15; dtoc5 1.8e-20; lukvle10 3.5e-15); cops verification (chain 2.3e-16 to 3.6e-16); wave 3 and the extension (2.1e-13, 1.2e-12, 7.9e-12) | resolved; the count of 13 is right. The other 15 primal points are exactly feasible: camshape (envelope point), optcdeg2, hvycrash, ex6_2_*, etamac, pricing050, pindyck, and catmix (exact simulation of float controls) |
| A12 (ex6_2_*) | wave-2 small verification, lines 314–324 | resolved in all four documents and in wave-2 §11 |
| A13, A14, B14 | calibration note, Theorems 3.1 and 3.3, Summary item 5 | resolved |
| A15, A16, B5 | face-exact Summary item 2 and §9.3; Consequence A (`kappa = 0`) | resolved |
| A17 | waterno2 report and verification | resolved |
| A18, A19, B11 | decomposition Summary, Proposition 2.6, Remark 3.6 | resolved |
| A20, A41 | repository README | resolved |
| A21, A22, A23, B3, B6 | SYNTHESIS | resolved; 17 = 28 − 11 |
| A25, B9 | summary, "What the pattern shows" | resolved |
| A28 | extension-n2 Summary item 4 and §4.1 | resolved |
| A29, B19 | face-exact Theorem 1 (`D/(2b) <= 1.99`; `eps <= 1e-4`, `r >= 1/2`); `sqrt(2e/pi) = 1.31548925` | resolved |
| A30 | `2 beta = 0.560339` | resolved |
| A31, B15 | consistency note, Summary | resolved |
| A32, B21 | coupling recheck item 7 (14.8%); census (13.6%) | resolved |
| A33 | lnts gaps 5.547e-13, 5.545e-13, 5.545e-13, 5.546e-13 | resolved |
| A34 | 4790.820715/770.7362 = 6.216; 263.735/165.19 = 1.597 | resolved |
| A36, A37 | scout `targets.md` §1 | resolved |
| A39, A40 | calibration and face-exact notes | resolved |
| B4 | decomposition Summary item 5; extension-adaptive A.5 and A.6 | resolved |
| B8, B10, B12, B13 | literature audit; consistency Summary D/F; bang-bang Theorem 2.3 | resolved |
| B16, B17, B18 | face-exact §9 (Griewank–Toint 1984, Theorem 4); coupling Theorem 5.1 prior art; RLCT Summary item 3 | resolved |
| B20 | decomposition §6; face-exact §11 | resolved |
| B23 (coupling) | M1–M7 in the text; §11.1 | resolved. M8 and the docstring label are declined and recorded |
| B24 (calibration) | four points in the text; §11.1 | resolved, apart from one residue (R4) |
| B25 (extension-n2) | items 1–10 in the text; §11.1 | resolved, apart from the status table (R2) |
| B26 (RLCT) | W1–W4 and O1–O2 in the text; §11.2 | resolved |
| B27 (pindyck) | gap ≤ 5.44e-14; §5 narrowed; mpmath wording; radius ≤ 3.7e-13; header | resolved. The script's log overwrite is declined and recorded |
| B28 (powerflow) | `diag_tight.log` (41869.05150199783, difference 9.322e-6); §6 log note; 3.3e-3 | resolved |
| B29 (wave 3) | 40.07%; the Δ wording matches the verifier's row 1b; pointer to the extension | resolved |
| B30 (decomposition header) | header; §8.5 | resolved |
| B31 (root log) | appended entry; `closing-audit-b.md` does not exist | resolved, with one wording slip (R5) |
| B32–B37 | SYNTHESIS §5; closing record item 4; wave-2 small report; scaling study; rocket values; note headers | resolved |

## 2. Refusals and deviations

All are justified.

- **Script edits** (coupling M8, the `jn_lifted_cert.py` docstring, the
  pindyck log overwrite). They are outside a text-only revision and are
  recorded where a reader will find them: coupling §11.1, pindyck §8 and the
  closing record.
- **No new review agent.** The closing record, the SYNTHESIS §2 header and
  the decomposition header name what is still unrechecked: decomposition
  §8.1, face-exact §13 item 5, scaling-study §9, the wave-3 root
  corrections and the closing revision itself.
- **B18 wording.** The chosen wording is more accurate than the suggested
  one. RLCT Summary item 3 says that the factor depends on `n`, `alpha`,
  `alpha'`, `M`, `s0` and the smallest value of `m` at non-optimal
  vertices, not on `n` alone.
- **B13 citation.** The window law is the bang-bang note's Theorem 2.3,
  proved under (W1)–(W5). Corollary 4.3 belongs to the calibration note,
  whose Summary item 4 now states that conditional.
- **B7 softening.** Proposition A.6 is proved only on the path family.
- **B31.** Appending a dated entry preserves the log's history, and
  `closing-audit-b.md` does not exist.
- **A22, O3, B28 item 2.** A22 was superseded by the B3 wording, O3 was
  optional, and B28 item 2 was addressed by a note in extension §6.

## 3. Remaining problems

**R1 (error). `open-instances-summary.md`, lines 22–25 (camshape100–800,
column "our rigorous dual"), read with the new sentence on lines 10–11.**
The exact optima are shown truncated toward zero, which moves negative
numbers up. Each displayed value therefore lies above the verified optimum
(`reviews/open-instances-verification/verification-report.md`, lines
22–25):

| instance | displayed | verified exact optimum | displayed − exact |
|---|---|---|---|
| camshape100 | −4.28414712174674 | −4.2841471217467438034 | +3.8e-15 |
| camshape200 | −4.27850023299272 | −4.2785002329927222919 | +2.3e-15 |
| camshape400 | −4.27568847892554 | −4.2756884789255432152 | +3.2e-15 |
| camshape800 | −4.27427414195419 | −4.2742741419541941011 | +4.1e-15 |

So the claim "Displayed dual bounds are truncated or rounded outward, so
each displayed value is itself a valid bound" is false for these rows.

*Fix:* show the values rounded down, `−4.28414712174675`,
`−4.27850023299273`, `−4.27568847892555` and `−4.27427414195420`, and write
"(exact optimum, rounded down)".

*Optional, same table, line 37:* powerflow0039r shows `41869.05148327244`.
That is 7e-12 above the certificate that the extension and its review cite,
`41869051483272433/10^12`. It is still below the review's own floor,
`41869051483289675/10^12`, so it is valid. Writing `41869.05148327243`
would match the cited certificate.

**R2 (stale). `theory-bangbang/extension-n2.md`, Section 9 status table,
lines 1078, 1079 and 1083.** The rows for Lemma 14, Proposition 15 and
Proposition 12 still say "not re-checked" or "revision not re-checked".
`reviews/ext-bangbang-n2-confirm.md` checked all three line by line
(Verdict, lines 15–17), and its remaining item 4 says "the status line
'revision not re-checked' can be updated". The paragraph just above the
table already says that the confirmation checked them, so the table
contradicts it.

*Fix:*

- Lemma 14: "proved; added after review; checked in
  `reviews/ext-bangbang-n2-confirm.md`".
- Proposition 15: "proof added after review; checked in
  `reviews/ext-bangbang-n2-confirm.md`; the blow-up of `P̄` is float
  numerics".
- Proposition 12: "...; revision checked in
  `reviews/ext-bangbang-n2-confirm.md` (two harmless imprecisions, fixed in
  Section 11.1)".

**R3 (minor, rendering). `research-20260929/README.md`, line 13
(decomposition row).** The content cell contains
`` `O(|T| C^{w+1} log(|T|/eps))` ``. In GitHub-flavoured Markdown, unescaped
pipes split table cells even inside code spans. The row therefore has 6
cells under a 3-column header. The renderer keeps only the first 3, so the
content cell is cut off and the Verification cell is not displayed. That
cell holds the r1–r3 links added for A38.

*Fix:* write `` `O(\|T\| C^{w+1} log(\|T\|/eps))` ``.

Two table rows edited in this revision have the same defect. Escape their
pipes too:

- `theory-coupling/coupling.md`, line 124 (Proposition 1.1 status,
  `||A||` and `||∇²g||`);
- `theory-decomposition/decomposition-certificates.md`, line 168
  (Section 3.4 status, `|T|`).

Other rows had the pattern before this revision, for example decomposition
lines 165, 166 and 172 and extension-adaptive lines 164–170. Fixing them is
not needed to close this revision.

**R4 (minor). `theory-calibration/scouting.md`, lines 1572–1573 (Section 7,
attack plan).** The text still says "was observed and derived to leading
order". The confirmation's point 3 asked for "formal leading-order
derivation". The root changed Remark 5.2(e) and the status table but not
this place.

*Fix:* "was observed and obtained by a formal leading-order derivation".

**R5 (nit). `root-research-log.md`, closing entry.** "The closing revision
applied coupling M1–M7" overstates M4, which was applied in the note only.
The `jn_lifted_cert.py` docstring still says "(c)" (coupling §11.1,
item 3).

*Fix:* "applied coupling M1–M7 (M4 in the note only; the
`jn_lifted_cert.py` docstring still says (c))".

**R6 (optional). `theory-consistency/consistency-relaxations.md`, header
(lines 3–19).** The header does not cite `reviews/consistency-confirm-r1.md`,
which confirmed the third revision. The root edit at line 2229 cites it.

*Fix:* add "The third revision was confirmed by
`reviews/consistency-confirm-r1.md` (no mathematical error; its two optional
points were applied by the root at the end of Section 12)."

*Suggestion, not a defect.* Once these items are applied, the sentence "These
root edits have not been rechecked" in the closing record and the root log
can cite this confirmation, and the closing record can link
`reviews/closing-audit-a.md`.

## 4. Checks run

All checks were targeted.

- A link check (inline Python) over 22 edited documents: 515 relative links,
  none broken.
- Exact-rational comparisons (inline Python, `fractions`) of every
  displayed dual bound in the summary table with the values in the
  verification reports. The same script confirmed:
  - the camshape excesses of R1 and the outward values;
  - the lnts gaps;
  - the waterno2 ratios;
  - `sqrt(2e/pi)` and `2 beta`;
  - the optcdeg2 gap of 9.0e-16;
  - the powerflow0039r difference of 7e-12.
- A scan of the tables in the edited documents for unescaped pipes inside
  code spans.
- Reading with `grep` and `sed`: notes, reviews, logs (`diag_tight.log`)
  and `git diff README.md`.

I ran no project-wide verification and did not inspect CI. I edited no file
and committed nothing.
