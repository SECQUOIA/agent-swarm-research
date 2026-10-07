# Confirmation review (round 1): `cell-slopes.md` after revision

Date: 2026-10-01. Note checked:
[`../open-instances-wave2/waterno2/cell-slopes.md`](../open-instances-wave2/waterno2/cell-slopes.md),
the version revised after the first review
([`waterno2-cellslopes-review.md`](waterno2-cellslopes-review.md), seven issues
in its Section 8). I did not write the note or the first review. I edited no
note and no root file, and I committed nothing.

My script and its output are in
[`waterno2-cellslopes-confirm-r1-checks/`](waterno2-cellslopes-confirm-r1-checks/)
(`recount.py`, `recount.log`). I also read the cited logs and documents
directly. All checks were targeted and run with `OMP_NUM_THREADS=1`. I ran no
project-wide verification and did not consult CI.

## Verdict: verified

All seven issues are fixed correctly. I rechecked each against the logs and
documents, not against the reviser's report. No result changed. The certified
value is still 278.230573774, exact 39157472136693483/140737488355328
(`cellslopes/logs/certB_verify.json`, fields `bound_exact` and
`bound_rounded_down`). No file under `cellslopes/` or `sepbranch/` is newer
than the first review, so no computation was re-run or altered. The new text
introduces no error. Two optional nits remain (Section 3), and neither comes
from the revision.

## 1. The seven issues, rechecked

**1. Review status (header, Summary, Sections 4.3, 5.4). Fixed.**
`reviews/waterno2-cellslopes-review-checks/logs/rebound_summary.log` gives
49,315 records re-bounded, none not run: 33,899 certified, plus 3,118 finite
and 12,298 infinite records proved empty (15,416 in total), and no failures. It
also gives the exact DP from the vbb2 values alone,
39157472136693483/140737488355328, identical to the authors' value.
`rebound_breakdown.log` gives the 556 distinct leaf tasks. Of these, 255 + 181 =
436 were certified and 1 + 119 = 120 proved empty. The 256 and 300 split quoted
in Section 5.4 also matches. The origins (5,158 cert3, 19,679 certA, 24,478
certB) match. The header, Summary and Section 5.4 now report these numbers and
cite the review, and Section 4.3 points to Section 5.4. No stale "not
independently reviewed" or "rests on `rbb.py` alone" statement remains, except
as quotations in Section 10. The relative links resolve.

**2. Distinct records (Summary, Section 5.4). Fixed.** Recounted from
`crosscheck_certB_{near,rand2000}.jsonl`:

- The files hold 2,313 record runs. The rand2000 file re-runs the same six path
  records, so 2,307 runs are counted in the table.
- These runs cover 2,293 distinct records: 1,663 certified and 630 proved empty.
  No record has conflicting statuses.
- The two random samples share 3 records. 11 records of the 2,000-sample are in
  the near-optimal or path group, and none of the 99-sample is.
- The random samples cover 2,096 distinct records (2,099 runs): 1,466 certified
  and 630 empty. Counted by runs, the earlier 1,467 and 632 were correct.
- All 2,293 records are certA (937) or certB (1,356) runs.
- certA's 298 record runs are 298 distinct records.

`compare_other_runs.log` of the review confirms the 2,293 common records and
the 1,663/630 split. The new table row (6 columns) renders correctly.

**3. SCIP share (Section 8). Fixed.** The four `stats_*.log` files give the
following SCIP CPU:

| stage | CPU |
|---|---|
| planning up to planF | 143,116 s |
| certA refresh | 163,270 − 143,116 = 20,154 s |
| planG | 16,166 s |
| certB refresh | 21,917 s |

These sum to 201,353 s, which is 55.2% of 364,667 s. Planning alone is
159,282 s (43.7%), the two refreshes are 42,071 s (11.5%), and rbb is
154,539 s (42.4%). The note's numbers match. The first review wrote 20,155 s
for the certA refresh. The log gives 20,154 s, the note's table value, and only
that value makes the total 201,353 s.

**4. plan3 gain (Section 6.1). Fixed.** `sepbranch/logs/plan3.log` goes from
round 0 (271.2238, 7,012 estimates) to round 89 (272.6353, 12,922 estimates,
904 s). That is +1.4115 for 5,910 estimates, or 0.239 per 1,000. The note's
"+1.41", "about 5,900" and "0.24 per 1,000" are correct.

**5. Füllner and Rebennack (Section 7). Fixed.** The folder
`literature/papers/fullner2022-non-convex-nested-benders-decomposition/`
contains `fulltext.md`, `original.pdf` and `paper.md`. Its front matter has
`status: "read"` and `added: "2026-09-04"`. The note's one-sentence description
agrees with the summary in `paper.md`: refined binary state expansions,
Lagrangian cuts in the lifted space, and a projection to nonconvex
piecewise-linear cuts in the original state. The novelty statement is
unchanged and still claims nothing.

**6. Definition 1.2 (Sections 2 and 6.7). Fixed, and the statement is
correct.** I checked it against Definition 1.2, Lemma 1.3 and the "Touching
pairs" remark of `theory-decomposition/decomposition-certificates.md`. Read in
the path case, the leaf of period t is the pair box (D_{t−1}, D_t). Its child
bound for link t is the cell's own minorant l_{t,D_t}.

- (CM) as stated also quantifies over cells D'' that only touch D_t. A jump in
  λ or β across the face can violate it there.
- The remark needs (CM) only for D'' whose interior meets int D_t. That leaves
  only D'' = D_t, where (CM) is trivial.
- (LC) does not need the remark. For a cell D that touches D_{t−1}, the pair
  (D, D_t) is in the DP and D is closed. So the pair bound of (D, D_t) covers
  points on the shared face.

The note therefore names the right condition, and only that one. It correctly
adds that Proposition 1's direct proof needs no such remark.

**7. Certification cost (Section 6.1). Fixed.** `stats_certB.log` gives 67,618
cellslopes rbb runs and 154,539 CPU-s (43,140 + 24,478 runs; 99,680 + 54,859
s). cert3 used 9,631 runs and 25,308 s (`stats_planF.log`). The new paragraph
explains why splits cannot lower the rigorous DP value: child cells inherit the
parent's slope, so the parent's records apply with zero correction. This is
correct, given that the verifier takes the best containing record. The 243.10
at certA's slopes matches `certA.log` (243.097042). The conclusion "not
established" is unchanged. The note also does not copy the first review's
phrase "for cert3, which gained less". That phrase is inaccurate: cert3 gained
8.85 over wave 2, against 5.65 for certA and certB.

**Section 10 (revision log).** It has one entry per issue, names the logs used,
and states that the certified value is unchanged. Each number in it matches my
recounts above.

## 2. No other change of results

These items agree with the first review and the logs:

- the result table and gap figures (1.67%; 1.65% relative to the primal; 55% of
  the gap closed);
- certA's value 277.093321045 (`certA_verify.json`);
- the Section 5.1 table;
- the vbb2 totals (8,775.3 s, longest run 69.1 s, 2,359 certB vbb2 runs).

The root documents that cite the note (`README.md`, `SYNTHESIS.md`,
`open-instances-summary.md`) already call it verified. The revised status line
is consistent with them.

## 3. Optional nits (not from the revision; no change required)

- Sections 2, 6.7 and 7 call the certificate "the path case of Definition 1.2
  and Lemma 1.5" and say both "allow one affine minorant per separator cell".
  Definition 1.2 allows cell-dependent slopes. Lemma 1.5, however, assumes one
  slope per separator, so the note uses its path-case analogue, not the lemma
  itself. This wording was in the reviewed version.
- Section 6.1: the 67,618 rbb runs also certify the split rounds of planC,
  which took cells from 113–162 to 148–240 per link. So not all of that cost
  is due to slopes. The paragraph's mechanism argument still supports its
  hedged conclusion.

## 4. Commands

Run from `research-20260929/` with `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`:

```
python3 reviews/waterno2-cellslopes-confirm-r1-checks/recount.py   # recount.log
```

I also read these files directly:

- `rebound_summary.log`, `rebound_breakdown.log` and `compare_other_runs.log` of
  the first review;
- `cellslopes/logs/cert{A,B}.log`, `stats_*.log` and `cert{A,B}_verify.json`;
- the literature folder above;
- Sections 1.3–1.4 of the decomposition note.

I compared modification times against the first review's file. Only targeted
checks were run. No project-wide checks were run and no CI results were
consulted.
