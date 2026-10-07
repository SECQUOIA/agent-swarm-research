# Closing audit A: consistency and correctness of the root documents

Date: 2026-09-30. Auditor: closing auditor A. I wrote none of the material
under audit. Scope: the root documents `closing-research-results.md`,
`SYNTHESIS.md`, `open-instances-summary.md`, `README.md`, `PROGRAM.md` (all in
`research-20260929/`) and the September 29 paragraph at the top of the
repository `README.md`. Every quantitative or status claim was compared with
the latest revision of the underlying note and with its latest review or
confirmation. I edited no file other than this report. Nothing was committed.

## Verdict

**Fixes needed.** The headline results are supported. All links resolve,
and the count of 28 closed instances is right. But the root documents
contain:

- two factual errors about the notes: the tree lower bound "not attained"
  and the SCIP growth rate in PROGRAM.md;
- one overstatement of verification: "all 19 confirmed by two independent
  checks";
- displayed "rigorous" dual bounds that are rounded up. For chain50,
  catmix100 and catmix800, the displayed bound lies above the optimum;
- a broken summary table, and a stale bang-bang confirmation link;
- a verification paragraph in the closing record that is false for about a
  dozen notes: several notes do not link their latest review, and some
  residual review items were never applied;
- several stale statements in `SYNTHESIS.md`, such as "Eleven open
  instances" and open questions that are already answered;
- a group of smaller overclaims.

None of these affects a proved theorem or a certified bound.

## Method and commands (targeted only)

- A Python script extracted every Markdown link from the six root texts
  and tested whether each target exists. Result: 136 links, all resolve.
  The script paths named in code blocks (`census.py`, `analyze.py`,
  `families.py`, `chain_boxqp.py`, `probe2.py`, `probe3.py`,
  `scip_unreliable.py`) and the cited constrained note also exist.
- I read the summaries, status lines and revision sections of every note,
  and the verdicts and remaining-issue lists of every latest review. I used
  `grep` to check whether residual review items appear in the current note
  text, and file times to order notes and reviews.
- I checked the arithmetic behind the discrepancies below in exact
  rational arithmetic (`python3` with `fractions`): the waterno2 ratios, the
  optcdeg2 bracket, the lnts gaps, the displayed chain/catmix/lnts bounds
  against the certified values and the optima, and the PROGRAM.md node
  ratios.
- I ran no project-wide verification and did not inspect CI. I did not
  rerun any certificate.

## Recount of closed instances

My count from the notes is **28**, the same as the root documents. Each of
the 28 has a separate verification:

| instances | count | note | verification |
|---|---|---|---|
| lnts50, 100, 200, 400 | 4 | `open-instances/open-instances-report.md` | `reviews/open-instances-verification/` |
| dtoc5 | 1 | same | same |
| camshape100, 200, 400, 800 | 4 | same | same (exact rational) |
| lukvle10 | 1 | same | same (verifier's own B&B, gap 1.42e-9) |
| optcdeg2 | 1 | `theory-bangbang/report.md` Section 5 | `reviews/bangbang-verification/` (exact rational, bracket 9.0e-16) |
| hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050 | 5 | `open-instances-wave2/small/report.md` | `reviews/wave2-small-verification/` |
| chain50, 100, 200, 400 | 4 | `open-instances-wave2/cops/report.md` | `reviews/cops-verification/` |
| catmix100, 200, 400, 800 | 4 | same | `cops-verification` (100, 200), `catmix-recheck` (400, 800) |
| powerflow0030p | 1 | `open-instances-wave3/report.md` | `reviews/wave3-verification/` |
| powerflow0039p, 0039r | 2 | `open-instances-wave3/powerflow/extension-report.md` | `reviews/powerflow0039-review.md` |
| pindyck | 1 | `open-instances-wave2/small/pindyck-extension.md` | `reviews/pindyck-review.md` |
| **total** | **28** | | |

The other counts are also right: 6 KAN instances (relaxation certified,
models exactly infeasible); 5 waterno2 instances improved; 19 invalid
listed dual bounds on 15 instances (11 pairs on 9 instances, plus 8 pairs
on 6 instances); 283 scouted candidates with 146 still open (the first-wave
11 were excluded from the 283).

**Primal side of the closures.** For 13 of the 28, the primal point that
closes the gap is only tolerance feasible. It has not been shown to be, or
to lie near, an exactly feasible point:

- lnts50–400: row violation 4.7e-15 to 6.7e-15;
- dtoc5: 1.8e-20;
- lukvle10: MINLPLib p5, 3.5e-15;
- chain50–400: 2.0e-16 to 3.6e-16;
- powerflow0030p, 0039p, 0039r: MINLPLib p1, 2.1e-13, 1.2e-12 and 7.9e-12.

The powerflow extension report says this explicitly. The KAN case shows
that such points can exist even when a model has no exactly feasible point
(finding 11).

## Findings

Severity: **error** (a statement contradicts a note or its review),
**overclaim** (stronger than the note supports), **stale** (was true
earlier, no longer is), **missing** (a needed qualifier is absent),
**minor**.

### Errors

1. **SYNTHESIS.md, Section 3b, "Trees" bullet.** The text says
   "(lower end approached, not attained)". The latest consistency note
   (Summary (B) and the Theorem 3.1 status row) says that the lower end is
   attained, numerically to 1e-7, in 515 of 900 random three-bag
   instances (T3). Only in family T1 is it approached as `K -> inf` and
   not attained at finite `K`. The "approached" wording comes from the
   note's first revision and was later superseded.
   *Fix:* "(both ends are attained in some instances: the lower end in 515
   of 900 random three-bag instances, numerically; in family T1 it is
   approached but not attained)".

2. **SYNTHESIS.md, Section 5 ("all 19 were confirmed by two independent
   checks"); open-instances-summary.md, "Systematic audit" paragraph ("All
   19, and the exact optima of all four emfl instances, were confirmed by
   two independent checks with separate code"); README.md, bound-audit row
   ("[recheck](…) (all 19 confirmed)").** The audit report's status table
   and the recheck say something different. The first verification
   confirmed 14 of the 19 pairs and the emfl050_3_3 bounds. The recheck
   confirmed the other 5 pairs and the other three emfl instances. It used
   emfl050_3_3 only as a control. So each pair was confirmed by one
   independent check, and the two checks together cover all 19.
   *Fix (SYNTHESIS, summary):* "all 19, and the two-sided optimum
   enclosures of the four emfl instances, have been confirmed with code
   independent of the audit's (14 pairs by the first verification, the
   other 5 and three emfl instances by the recheck)". *Fix (README):* move
   the parenthesis after both links: "(together they confirm all 19)".

3. **open-instances-summary.md, table "Instances closed or nearly closed",
   rows chain50–400, catmix100–800 and lnts100, column "our rigorous
   dual".** These displays are rounded to nearest, not outward, so they
   lie above the certified bounds:
   - "5.0686–5.0723": chain50's certified bound is 5.072261493982863. The
     display 5.0723 exceeds even chain50's optimum, by 3.9e-5.
   - "−0.0480694 … −0.0480559": catmix100's bound is −0.048069432038882705
     and catmix800's is −0.048055901841076894. Both displays exceed the
     optima, by 3.2e-8 and 1.3e-9. That is more than the stated gaps.
   - lnts100: "0.5545954011664" is 4.3e-14 above the certified
     0.5545954011663566.

   The audit and the bang-bang note use outward rounding for rigorous
   values. *Fix:* chain "5.06862 … 5.07226"; catmix "−0.04806944 …
   −0.04805591"; lnts100 "0.5545954011663". Or state that the displayed
   values are rounded to nearest and are not bounds.

4. **SYNTHESIS.md, Section 8, optcdeg2 bullet.** "exact certificate value
   293.87607509587509238". The exact value is
   293.87607509587509237940…. The bang-bang note (Section 9.2, M7) and its
   round-2 confirmation removed this rounded-up form ("No rounded-up form
   ('…09238') remains"). *Fix:* "293.876075095875092379… (truncated)".

5. **SYNTHESIS.md, "Open questions", second bullet.** "The right base in
   Theorem 1 (data suggest about 2 per variable)". The face-exact note
   gives the following rates:
   - 2.7–3.5 per variable for termwise relaxations (the toy B&B, and SCIP
     with the minor separator off);
   - 2.5–3.2 for minimal grid certificates.

   The 2.1–2.3 of default SCIP is outside the theorem's relaxation class.
   *Fix:* "(termwise relaxations grow by 2.7–3.5 per variable in the data;
   minimal grid certificates by 2.5–3.2)".

6. **PROGRAM.md, "First evidence", paragraph after the larger study.**
   "Growth is roughly a factor 2–3 per two added variables." The page's
   own table gives ratios of 4.9, 4.2 and 6.5 (seed 0) and 8.4, 3.1 and 4.9
   (seed 1) per two variables. The paragraph just above it and the
   scaling study give "about 5x per two variables". *Fix:* "Growth is
   roughly a factor 5 per two added variables (2–3 per variable)".

7. **SYNTHESIS.md, "What this means for solvers", "Evidence" bullet.**
   "SCIP 10 behaves as predicted on these families." The decomposition
   note (Significance) says: "SCIP's default PSD-minor cuts escape both
   single-tree bounds, so the theorem does not explain the program's SCIP
   counts". The face-exact note says that default SCIP is outside the
   theorem's class. *Fix:* "SCIP 10's node counts grow about fivefold per
   two variables on these families, but its default PSD-minor cuts put it
   outside the proved bounds' relaxation class, so the theorems do not
   explain its counts."

8. **open-instances-summary.md, lines 32–38.** A blank line (line 33)
   splits the table. The rows for KAN, powerflow0030p, 0039p, 0039r and
   pindyck have no header row, so they do not render as a table. The KAN
   row also sits under the heading "Instances closed or nearly closed",
   although those models are exactly infeasible and not closed. No row is
   "nearly closed" any more. *Fix:* delete the blank line; rename the
   heading "Instances closed (28)"; move the KAN row to its own short table
   or section, "Relaxation certified; OSIL models exactly infeasible".

9. **closing-research-results.md, "Verification", first paragraph.**
   "Every note links its reviews" and "with fix-and-confirm loops until
   the confirmer found no remaining issue. The last residual wording
   issues were applied by the root and are recorded in each note." Both
   statements are false for the following notes:

   | note | latest review, not linked from the note | state of the note |
   |---|---|---|
   | `theory-calibration/scouting.md` | `reviews/recheck-calibration-confirm.md` | header says the second revision "has not been rechecked"; the confirmation's four wording points (Summary item 4, Section 4 closing paragraph, Remark 5.2(e), "linear-cost certificate") are not applied |
   | `theory-coupling/coupling.md` | `reviews/coupling-recheck.md` | header says "has not been rechecked"; recheck items M1–M8 are not applied (note last changed 05:50, recheck 08:09) |
   | `rlct/rlct-node-complexity.md` | `reviews/rlct-recheck2.md` | header says the second-round edits "have not been re-reviewed"; W1–W4 are not applied |
   | `theory-bangbang/extension-n2.md` | `reviews/ext-bangbang-n2-confirm.md` | header says "the revision has not been re-checked independently"; ten minor items are not applied, including the float caveat on the bold "Consequence" sentence in Section 4.1 and the broken table at line 1045 |
   | `theory-bangbang/report.md` | `reviews/bangbang-root-fixes-confirm-r2.md` | header says "that third revision has not been re-checked independently", but r2 checked it; the final root edit cites `bangbang-root-fixes-confirm.md` for a nit that comes from `-r2.md` |
   | `theory-robust-lb/robust-lower-bound.md` | `reviews/robust-lb-confirm-r1.md` | header says "The third revision has not been rechecked", but r1 confirmed it with no remaining problem |
   | `open-instances-wave2/small/pindyck-extension.md` | `reviews/pindyck-review.md` | header says "Not yet independently reviewed"; the review's two wording fixes are not applied ("gap ≤ 5.43e-14" is rounded the wrong way, it should be ≤ 5.44e-14; the "entrywise interval Hessian over any box" overclaim) |
   | `open-instances-wave3/powerflow/extension-report.md` | `reviews/powerflow0039-review.md` | header says "Not independently reviewed"; the review's three minor items are not applied (the 41869.05037 diagnostic, the log bound, "within 3e-3") |
   | `open-instances-wave2/cops/report.md` | `reviews/catmix-recheck.md` | header says "Not independently reviewed at the time of writing" |
   | `open-instances-wave2/waterno2/report.md` | `reviews/waterno2-recheck.md` | header says "not independently reviewed" |
   | `bound-audit/audit-report.md` | `reviews/audit-confirm-r2.md` (round 3, clean) | header table ends at round 2 |

   Smaller cases of the same kind:
   - The headers of `decomposition-certificates.md` ("the fixes of
     Sections 8.1 and 8.4 have not been rechecked"; r3 rechecked 8.4) and
     `extension-adaptive.md` (no mention of confirm-r2's verification) are
     out of date.
   - `open-instances-wave2/small/report.md` still says "Not yet
     independently reviewed", and its Section 7 ("no global dual bound")
     does not point to the pindyck extension that supersedes it.

   *Fix (root document):* replace the two sentences with: "The README
   links each note's reviews. Every extension and second-round revision
   was checked by a fresh agent. Minor wording items raised by the last
   check remain unapplied in the calibration, coupling, RLCT, bang-bang
   `n ≥ 2`, pindyck and powerflow-extension notes, and several note
   headers predate their latest review." *Fix (notes, if the user
   authorizes it):* add the missing links and update the listed status
   lines.

10. **README.md, row `theory-bangbang/report.md`, column Verification.**
    "[confirmation of fixes](reviews/bangbang-root-fixes-confirm.md)" links
    the round-1 confirmation. Its verdict is "Fixes needed", and it lists
    R1–R5, which were fixed later. The latest confirmations are
    `bangbang-root-fixes-confirm-r1.md` (round 2) and
    `bangbang-root-fixes-confirm-r2.md` (round 3: "All three issues are
    fixed correctly"). *Fix:* link `-r2.md` as "confirmation", or list all
    three rounds.

### Overclaims

11. **closing-research-results.md, item 4 ("28 instances listed as open were
    closed for the models as written"); SYNTHESIS.md, one-paragraph answer
    and end of Section 5; open-instances-summary.md, "Coverage"; top of
    repository README.md.** For 13 of the 28 (listed in the recount
    section), the primal point is tolerance feasible only. For those
    instances, "closed" means that the rigorous dual meets the value of a
    point with row violations between 1e-20 and 8e-12. It does not mean a
    rigorous bracket of the exact model's optimum. The KAN finding shows
    that the difference can matter. *Fix:* add one sentence in the closing
    record and the summary: "For lnts50–400, dtoc5, lukvle10, chain50–400
    and powerflow0030p/0039p/0039r, the primal side is a point feasible to
    row violations of 1e-20–8e-12. For these, closure is measured against
    that point's value; no exactly feasible point was constructed."

12. **closing-research-results.md, item 4 ("ex6_2_7, ex6_2_5 (prior
    ε-global solutions exist)"); SYNTHESIS.md, Section 5 (same words);
    open-instances-summary.md, ex6_2_7 row ("prior ε-global solution:
    McDonald–Floudas 1997").** The verifier found GLOPEQ, an ε-global
    method for these problems. It wrote: "I could not access the handbook
    text to confirm the global values it reports", and concluded that the
    phase splits "were very likely known to be ε-global". *Fix:* "(an
    ε-global method, McDonald–Floudas 1997, very likely solved them; not
    confirmed)".

13. **SYNTHESIS.md, Section 8, first "Proved" bullet.** "an exact affine
    calibration exists iff the discrete costates make every stage residual
    globally minimal on the trajectory (the Leitmann–Stalford condition,
    with a mesh-uniform version for Euler)". The calibration note
    (Theorem 3.1) says "iff some multipliers" do this, that the "only if"
    needs `f*` to be attained, and that the multipliers must be the
    discrete costates only with smooth interior data. After the recheck
    (R1), the note calls the pointwise condition behind the mesh-uniform
    Theorem 3.3 a sufficient form of the Leitmann–Stalford condition, not
    the condition itself. *Fix:* "an exact affine calibration exists iff
    some multipliers (the discrete costates, for smooth interior data) make
    every stage residual globally minimal on the trajectory ('only if'
    needs `f*` attained); a mesh-uniform version for Euler holds under
    Mangasarian with margin or a strict pointwise sufficient form of the
    Leitmann–Stalford condition".

14. **SYNTHESIS.md, Section 8, transfer theorem.** "gives exact
    certificates for every sufficiently fine transcription". Theorem 5.2
    covers Euler transcriptions. It also needs a `C^4` strict calibration,
    interior optimal controls and uniformly convergent Euler KKT points.
    *Fix:* "for every sufficiently fine Euler transcription (with interior
    optimal controls and uniformly convergent discrete KKT points)". The
    closing record's "exact certificates for fine transcriptions" needs the
    same word, "Euler".

15. **SYNTHESIS.md, Section 1, Theorem 2 bullet.** "the mechanism
    disappears for a split factorization". The face-exact note says that
    it disappears *near `x*`*, where the split factors are convex. Whether
    split factorizations need exponentially many leaves outside that
    region is open (Section 9.3). *Fix:* "the mechanism disappears near
    `x*` for a split factorization (outside that region the question is
    open)".

16. **SYNTHESIS.md, Section 3, last bullet.** "three remedies, each proved
    to avoid the exponential in its own setting". The third remedy (tree
    Lagrangians plus exact windows, Section 5) is supported by instance
    certificates, not by a theorem. *Fix:* "the first two proved to avoid
    the exponential in their own settings, the third shown to work on the
    closed instances".

17. **open-instances-summary.md, "SCIP 10.0.2 wrong optimal values"
    bullet.** The text says: "cause: an invalid in-tree bound reduction in
    the nonlinear constraint handler's propagation". The waterno2
    verification established that an invalid node-local domain reduction
    removed the optimum. On the component it says only that "the evidence
    points to node-level domain propagation of the nonlinear constraint
    handler … A debug build would be needed to pin it down". *Fix:* "cause:
    an invalid in-tree bound reduction, most likely in the nonlinear
    constraint handler's propagation". The closing record's wording is
    already correct.

18. **closing-research-results.md, item 1, second bullet.** "constant child
    bounds provably need `Omega(eps^{-1/2})` cells". Proposition 2.6 is
    proved for a child of the root with a 1-D separator. The general case
    is sketched. *Fix:* add "(proved for a child of the root with a
    one-dimensional separator)", as `SYNTHESIS.md` already does.

19. **SYNTHESIS.md, Section 2, Theorem 3.4 bullet.** "this condition is
    real (a copy-drift pattern makes the gap grow linearly in `n` when it
    fails)". The decomposition note labels Remark 3.6 as "observed
    numerically; mechanism explained". *Fix:* "computations show that this
    condition is real: …".

20. **Repository README.md, September 29 paragraph.** Two claims need
    qualifiers:
    - "decomposition-aware certificates … need `O(|T| C^{w+1}
      log(|T|/eps))` work" omits "under quadratic growth".
    - "an exact identity: the gap is twice the distance to the band of
      exact splits" holds for one separator only; on trees there is only a
      two-sided bound.

    *Fix:* add "under quadratic growth" and "for one separator".

### Stale statements

21. **SYNTHESIS.md, "What this means for solvers", "Evidence" bullet.**
    "Eleven open instances yield to structure-aware duality in seconds to
    minutes." The count is now 28. Run times also go well beyond minutes:
    the catmix certificates took 21–70 min (the recheck took 43 min per
    instance), and the waterno2 period certification took hours. *Fix:*
    "28 open instances yield to structure-aware certificates, most within
    minutes and the largest (catmix800) in about an hour".

22. **SYNTHESIS.md, "Plausible capability" bullet.** "The second
    certification wave is testing how broadly this works." Waves 2 and 3
    are complete. *Fix:* "The second and third waves closed 17 more
    instances with this pattern."

23. **SYNTHESIS.md, "Novelty position".** "certificates for the 11
    instances". *Fix:* "certificates for the 28 instances".

24. **SYNTHESIS.md, "Open questions".**
    - "An adaptive decomposition algorithm with complexity guarantees that
      does not know `x*`": answered by Theorem A.5 of the extension, with
      an extra `(sqrt|T|)^{w+1}` factor that is real for that algorithm
      (Proposition A.6). *Fix:* "An adaptive algorithm without knowledge
      of `x*` that avoids the extra `(sqrt|T|)^{w+1}` factor of
      Theorem A.5".
    - "A two-sided characterization … (lower half proved)": the lower half
      holds with a `w`-dependent power of `|T|` (Proposition B.1) and is
      false with a fixed-degree polynomial (Theorem B.2). *Fix:* "(lower
      half proved with a `w`-dependent power of `|T|` and false with a
      fixed degree; upper half open beyond one separator; revised as
      Conjecture B.5)".
    - "Handling dense linear coupling …": the coupling note now gives
      Theorems 3.1 and 4.5 and a lower bound. *Fix:* "Whether the depth
      factor of the partial-sum certificate (coupling note, Theorem 4.5) is
      necessary".

25. **open-instances-summary.md, "What the pattern shows".** "…
    consistency-relaxation theory …, which is under review". The note has
    been reviewed, rechecked and confirmed. *Fix:* delete "which is under
    review".

26. **PROGRAM.md, status line.** "Status: active research program; nothing
    here is reviewed yet unless a review file says so." The program is
    closed. *Fix:* "Status: closed on 2026-09-30 at the user's request;
    results in `closing-research-results.md`. This page is the original
    program definition, with corrections marked inline."

27. **closing-research-results.md, census bullet ("constant-width families
    (waterno2, camshape, lnts) become open as they grow"); SYNTHESIS.md,
    "Evidence" bullet ("Constant-width MINLPLib families become open as
    they grow").** This continuation closed lnts50–400 and camshape100–800.
    The census note itself says it "does not show that width causes the
    difficulty". *Fix:* "in MINLPLib's listing before this work, …
    (lnts and camshape have since been closed; the obstacle was the
    relaxation)".

### Missing qualifiers and minor points

28. **SYNTHESIS.md, Section 8, `n ≥ 2` bullet.** It does not say that the
    local `eta_L` result does not feed into the transfer theorem. In the
    global form that Theorem 4.1 needs, the sign of `eta_L` does not decide
    existence (extension-n2, Summary item 4; report, Remark 3.3). *Fix:*
    add "This settles the local formulation only; in the global form that
    the transfer theorem needs, even `eta_L > 0` does not ensure existence
    (Example C, float)." (minor, missing)

29. **SYNTHESIS.md, Section 1, Theorem 1.** The hypothesis
    `D/(2b) <= 1.99` is omitted. *Fix:* add "when `D/(2b) <= 1.99`".
    (minor)

30. **SYNTHESIS.md, Section 3b, "Kinks".** "numerically n·gap → 2 ×
    0.2801" mixes two cases:
    - for a zero-width kinked band, the limit `2 beta = 0.5603` follows
      from the identity and Bernstein's theorem;
    - for a positive band width, the same limit is only a conjecture with
      weak support.

    *Fix:* "for a zero-width band, `n·gap → 2 beta = 0.5603` (Bernstein's
    constant); for a band that opens quadratically this limit is a
    conjecture". (minor)

31. **SYNTHESIS.md, Section 3b, "Novelty".** "One direction of the
    identity is in Korda–Magron–Ríos-Zertuche". The note gives this
    attribution:
    - the one-sided bound is de Farias–Van Roy's;
    - its positive-width sufficiency form is Grimm–Netzer–Schweighofer
      (2007, Lemma 3);
    - the quantitative version is KMRZ (Lemma 11).

    *Fix:* use that attribution. (minor)

32. **SYNTHESIS.md, Section 3c versus Section 6; closing record.** The
    small-width baseline is 13.6% in the census and "about 15%" (14.8%) in
    the coupling statement. The coupling note uses `min(w_full, w_free)`
    as the baseline, which differs from the census heuristic. *Fix:* say
    so once, for example "(14.8% with the coupling note's baseline, which
    takes the smaller of two width heuristics; 13.6% in the census)".
    (minor)

33. **open-instances-summary.md, lnts rows, "gap after" "5e-13".** The
    verified gap is 5.5e-13 (lnts50: 5.547e-13). *Fix:* "5.5e-13".
    (minor)

34. **closing-research-results.md, item 4, and SYNTHESIS.md, Section 5,
    and repository README ("factors of 1.6–6").** The largest factor is
    6.22 (waterno2_18). *Fix:* "1.6–6.2". (minor)

35. **PROGRAM.md, correction paragraph.** "global minima with 2–5
    coordinates at ±1" should read 2–27 (4–27 at `n = 1000`; scaling
    study, Section 1.3). "fails" was evidence in the study and was proved
    for 9 instances by the review. *Fix:* "(eps-optimal points with 2–27
    coordinates at ±1; boundary optima proved for 9 instances)". (minor)

36. **open-instances-summary.md, "Tolerance artifacts in listed primal
    values".** "SCIP's camshape100 incumbent (row violation 1e-8, 5.3e-5
    below the optimum)" is not a listed value, and the verifier marks it
    "Unchecked". *Fix:* move it out of the "listed" sentence and mark it
    "(not independently checked)". (minor)

37. **open-instances-summary.md, "Coverage".** "the scout found 146 open
    instances among 283 … the tables cover 28 instances closed". The 283
    exclude the 11 first-wave instances, which are among the 28. *Fix:*
    add "(plus the 11 first-wave instances, which the scout excluded)".
    (minor)

38. **README.md, verification column.**
    - The decomposition row omits the three non-dyadic confirmations
      (`decomposition-nondyadic-confirm-r1/-r2/-r3.md`).
    - The calibration row omits `recheck-calibration-confirm.md`, the
      latest check of that note.

    *Fix:* add the links. (minor)

39. **closing-research-results.md, item 3.** "Every certificate for a
    transcribed control or variational instance is a discrete calibration"
    reads as a universal theorem. The note says that the certificates that
    closed these instances fit the framework. *Fix:* "Every certificate
    that closed a transcribed control or variational instance here is a
    discrete calibration". (minor)

40. **closing-research-results.md, "Verification".** "wrong solver-bound
    counts in a first version of the toy B&B". The face-exact note says
    that the first version pruned on uncertified HiGHS QP values, which
    made some leaf counts too small. *Fix:* "leaf counts made too small by
    uncertified QP-solver bounds in a first version of the toy B&B".
    (minor)

41. **SYNTHESIS.md, one-paragraph answer, and repository README.** "19
    listed solver dual bounds on 15 instances provably invalid" is stated
    without saying that 8 are tolerance-scale and that 7 of the other 11
    are below common 1e-4 tolerances. The audit calls the gross errors,
    above all four clear pairs, "the substantive findings". *Fix:* add
    "(8 of them at tolerance scale)". (minor)

## Checked and consistent

These were checked and match the latest notes and reviews:

- Theorem 1 base and constant (`0.57 (5/3)^n`); Theorem 2 base 1.205;
  Corollary 2.1 base 1.31549 and constant 0.068.
- Theorem 3.4 size form; Proposition 2.6 constant; Theorem 4.1 ratio
  `3e-10 (2e/pi)^{n/2}/sqrt(n)` for `n >= 3`, `eps <= 1e-4`; crossovers
  `n = 29` and 9.
- Adaptive Theorem A.5 and Proposition A.6; Theorem B.2.
- Robust-lb bases 1.003, 1.05 and 1.063, and observed growth 2.85 and 2.0.
- The consistency identity; the kink lower bound `1/(30(3+c)n)`; factors
  7.9 and 11.8.
- Coupling counts `C(n+1,(n+1)/2)` and `3n^2 − 3n + 2`.
- The RLCT statements and the 4-D counterexample.
- SCIP node ranges and the prototype figures (8192 variables, 13–19 s,
  `n^1.6–1.8`, 33 bracketed instances).
- Census shares 13.6% and 62.7%.
- Every closed-instance value in the summary table other than those in
  finding 3.
- Waterno2 duals and gaps; the KAN claims; ann_cumene_tanh.
- The audit's class counts, margins and per-solver split; the LINDO rocket
  and methanol50 margins.
- The optcdeg2 bracket 9.0e-16 (9.006e-16 recomputed).

## Not checked

- I did not rerun any certificate, solver run or review script. Numerical
  agreement was checked against the notes' and reviews' stated values and
  stored logs only (for example `reviews/wave2-small-verification/logs/pricing050.json`,
  whose gap 1.041e-17 matches the summary's 1.0e-17).
- I did not check the mathematics of any proof, the literature claims or
  the MINLPLib pages.
- I did not check `root-research-log.md` beyond the completion entries.
