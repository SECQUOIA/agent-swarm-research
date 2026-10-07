# Review round 3: consistency and writing

**Resolution (2026-10-04, after this review).** The Part 5S replay finished: `experiments/v5/runs/partS5/replay.json` reports `passed: true`, 47,168 of 47,168 cuts replayed (40,700 polytope, 6,468 star), coverage complete, no failed runs, and all tampering controls rejected in modes agg-star, agg-star4 and rowdir-star4, including the star-certificate mutations in agg-star. `R10_numbers_check.py <extracts> replay` then gave 274,489 recorded cuts, 92,222 distinct rows and passing replays in every part. The campaign-5 summaries were regenerated; only their replay line changed. The blocking finding about the 5S replay is closed.

Scope: the whole typeset text (development/draft-round3/main.txt, identical to
the current sources), checked for consistent terminology, terms used before
they are defined, agreement between the abstract, Section 1, Section 8.7,
Section 9 and the detailed results, cross-references, leftovers, and language.
The manuscript, experiments/ and evidence/ were not edited; this file is the
only output apart from one read-only script.

Locations are given as source file:line (sections/...) and PDF page.

## Checks run (targeted)

- Read the full typeset text (67 pages) and the corresponding sources.
- `grep` over sections/*.tex for placeholders (TODO, FIXME, ??, TBD, draft
  notes): none. main.log: no undefined or multiply defined references, no
  overfull boxes (two underfull boxes in the abstract).
- `verification/R10_consistency_tables.py` (new, read-only): parses Tables
  12–17 from sections/B-tables.tex and recomputes the medians and solved counts
  of Table 4 and Table 5 and several derived statements of Sections 8.5–8.6.
  Command:
  `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python verification/R10_consistency_tables.py`.
  Result: every median and solved count of Tables 4 and 5 matches the
  appendix tables, apart from two third-decimal differences
  (4C4 remainder cap 64n, n=80: 1.000 vs stated 0.999; 4C4 whole row wide,
  n=40: 0.982 vs stated 0.981). Both come from computing medians of values
  that the appendix rounds to four significant digits, so they are not errors.
  The derived statements also match: SCIP's 3C root bound per copy is −0.0354
  to −0.0131; SCIP-nolocks is below the glued level on 20 of 20 instances;
  remainder-wide is above it on 7 of 20; the block closure equals the optimum
  on 13 of 20 (maximum gap 6.47·10⁻⁴); closure−root at the 64n cap is at most
  7.7·10⁻⁴; the 4C4 overall root-gap medians are 0.9526 (remainder) and
  0.9864 (whole row); Table 17 has 8 process-timeout marks.
- Checked the campaign-5 protocol (experiments/campaign-v5-protocol.md), the
  campaign-4 protocol (Part B2 modes), the v3d records (the 100 baseline root
  bounds of Part 3P are 30 + 30 + 20 root runs plus the root bounds of the
  20 full runs, so the count is right), the partS5 summary
  (experiments/v5/results-s5/results.md) and the rerun-spike launch log.
- Waited, as instructed, for the partS5 replay (experiments/v5/runs/replay-partS5.log);
  see finding C0.
- Abstract length: 248 words when each formula counts as one word (JOGO
  allows 150–250 words), so there is almost no room to add text.

These are local targeted checks only. No solver was run. The project-wide
verification scripts and CI checks were not run here.

## Summary

The theory sections are consistent and the cross-references resolve. All
summary-table numbers agree with the appendix tables. The main problems are
these:

0. The headline claim that every recorded cut passed replay includes 47,168
   Part 5S records. Their replay was still running when the 60-minute wait
   ended, and results-s5 says "Replay: not run yet" (C0). This blocks
   submission until the replay passes.
1. Section 8 and Section 9 attribute the in-solver star results to the
   near-linear star algorithm of Theorem 4.4. The solver ran the simpler star
   oracle (M1).
2. Section 9 says all three SCIP settings stopped at the glued pair level. Only
   SCIP-nolocks reached that level (M2).
3. The abstract omits the two caveats that every other summary states: with a
   binding row, SCIP-nolocks did as well and faster, and Gurobi solved more
   star instances (M3).
4. Section 2.1 promises that Section 5.3 relates the joint-range inequalities
   of Xu and Pokutta to the cuts. Section 5.3 does not mention them (M4).
5. Leftovers from the last edits: Section 5.3 and Appendix D repeat each other
   almost word for word; Appendix H uses unprefixed part labels and
   "Campaigns 2–4"; Table 7 uses "mech." and other code names that the text
   does not use (m1–m4).

---

## [critical, blocks submission until resolved] C0. The replay claim covers 47,168 Part 5S records whose replay had not finished when this check ended

**Location.** sections/00-abstract.tex:18 (p. 1); sections/01b-results.tex:2–4
(p. 3); sections/08b-validity.tex:3–9 (p. 25, Section 8.2);
sections/08g-summary.tex:3–4 (p. 34, Section 8.7).

**Issue.** The abstract says "Every recorded cut passed replay". The
introduction, Section 8.2 and Section 8.7 say all 274,489 records passed,
131,222 of them from campaign 5. Section 8.2 also says that "in every part
and cut mode, each of the fourteen corrupted records … was rejected". For
campaign 5 this rests on three replays:
- partC5a: 0 cuts, passed;
- partC5b: 84,054 cuts, passed;
- partS5: 47,168 cuts (root 24,177, full 22,991), including all star-oracle
  certificates and their tamper tests. No result is archived for partS5.

At the end of the bounded 60-minute wait (60 polls, 60 s apart),
experiments/v5/runs/replay-partS5.log was still empty. The replay process
(`replay_v5.py runs/partS5`, PID 169873, started 23:24 on 2026-10-03) was
still running at 00:42 on 2026-10-04, after 77 minutes.
experiments/v5/results-s5/results.md:9 says "Replay: not run yet." Until the
run finishes, 17% of the records behind the headline validity claim, and
every star certificate in the solver, have no replay result.

Two smaller points about the same sentences:
(a) The eight rerun-spike runs of Part 5S recorded 1,135 cuts
(runs/launch-rerun-spike.log). They are not part of the 131,222
(131,222 = 84,054 + 47,168), and no replay log exists for them, yet
Section 8.6 reports these runs. "Every recorded cut" therefore claims
slightly more than the replays cover.
(b) Sections 1 and 8.7 say the records passed replay "against … the row
stored by SCIP". Section 6.3 says replay compares with the stored row as
the separator recorded it, and compares with SCIP's own row only when the
cut is generated.

**Evidence.** `wc -c runs/replay-partS5.log` gave 0 at 23:24 and still 0 at
00:42. `ps` showed PID 169873 running for 77:31. The replay logs of
partC5a and partC5b report `"passed": true` with 0 and 84,054 replayed cuts.
results-s5 tables give 7,326 + 7,626 + 8,039 cuts in the full runs and
7,720 + 8,015 + 8,442 in the root runs. The rerun-spike launch log sums to
1,135 cuts.

**Fix.** Do not submit until replay-partS5.log reports `"passed": true`,
`coverage_complete: true` and 47,168 replayed cuts, with the star tamper
modes rejected. If it passes, the numbers can stay. Change "Every recorded
cut" to "Every cut recorded in the protocol runs" (abstract, Sections 8.2
and 8.7), or replay the rerun-spike directory as well. In 01b-results.tex:3–4
and 08g-summary.tex:3–4, write "… passed a fresh-process replay against the
source model and the recorded SCIP row". If the partS5 replay fails, the
abstract, Section 1, Section 8.2, Section 8.7 and Section 9 must be revised.

---

## [major] M1. The in-solver star results are attributed to the near-linear algorithm, but the solver ran the simpler star oracle

**Location.** sections/08a-setup.tex:19–21 (p. 24, Section 8 introduction);
sections/08f-star.tex:3–6 (p. 33, Section 8.6); sections/09-conclusions.tex:49–51
(p. 35, Section 9).

**Issue.** Section 8 says campaign 5 "runs the star algorithm in the solver".
Section 8.6 says of "the star algorithm of Theorem 4.4": "We test it in two
ways: offline at large scale, and inside the solver". Section 9 ends with
"the near-linear star algorithm makes them cheap to certify". But Section 4.2
(p. 15–16) and Section 7.2 (p. 22) say that the solver uses "the simpler
implementation described at the end of Section 4.2", which costs
O((m+k)³). That oracle certified the star blocks of Section 8.6. The sweep of
Theorem 4.4 ran only offline (Part 4S). A reader who takes Section 8.6 at its
word will credit the 7.8 ms median per call to the sweep.

**Evidence.** experiments/campaign-v5-protocol.md lines 31–35: "Certification
is unchanged: the polytope enumeration (Theorem 4.1) when its dimension and
face budgets allow, else the inherited constrained-star oracle
(`theory/quadratic_star.py` …)". Section 4.2, p. 16: "It certified … those of
the star blocks with up to 16 leaves in Section 8.6". Part 4S (p. 33): the
simpler oracle needs about 70 times more time per tenfold increase in k.

**Fix.**
- 08a-setup.tex:19–21: "Campaign 5 was designed after campaign 4: it tests
  star blocks in the solver, adds the remaining comparators on the fresh
  instances, tests larger cut limits and compares the certificate with a
  numerical global solve."
- 08f-star.tex:3–6: "The blocks of Sections 8.3–8.5 have at most four
  variables, so star blocks were not needed there. We test the star algorithm
  of Theorem 4.4 offline at large scale, and star blocks inside the solver on
  a family whose merged blocks are stars with up to 16 leaves; in the solver,
  the simpler star oracle of Section 4.2 certifies them."
- 09-conclusions.tex:49–51: "On this family, joint blocks larger than the
  separator's default of four variables matter. The simpler star oracle
  certified them in milliseconds, and the near-linear sweep (Part 4S) handles
  stars with 10⁴ leaves in about two seconds."

## [major] M2. Section 9 says all three SCIP settings stopped at the glued pair level; only SCIP-nolocks reached it

**Location.** sections/09-conclusions.tex:37–39 (p. 35).

**Issue.** "With a non-binding coupling row, native SCIP stopped at the level
of glued pair relaxations in all three settings we ran". SCIP closes 0 of its
own root gap by definition, and SCIP-extra closed 0.57–0.66, while the glued
level is 0.89–0.95 (Table 4). Section 8.5 states the correct version: "None of
the three SCIP settings we ran closed any part of the gap between the
pair-hull level and the optimum".

**Evidence.** Table 4 (p. 31) and R10 script: seeds 0–4 SCIP-extra medians
0.64/0.58/0.66/0.59 against glued 0.95/0.89/0.93/0.92; seeds 5–9 0.57/0.64/0.61/0.66
against 0.93/0.92/0.93/0.92. SCIP-nolocks is just below the glued level on 20 of 20
instances.

**Fix.** "With a non-binding coupling row, none of the three SCIP settings we
ran got beyond the level of glued pair relaxations, and only SCIP-nolocks
reached it; the certified cuts went beyond it when …"

## [major] M3. The abstract omits the caveats that the introduction, Section 8.7 and Section 9 state

**Location.** sections/00-abstract.tex:20–23 (p. 1).

**Issue.** The abstract ends: "On constructed path and star families the cuts
closed nearly all of SCIP's root gap, and a configuration fixed in advance
solved all 20 fresh path instances, against at most 10 for SCIP and 5 for
Gurobi." Every other summary adds two caveats: with a binding coupling row,
SCIP without implicit discreteness also solved all 20 and was faster; and on
the star family Gurobi solved more instances (22 against 19). Without them
the abstract claims more than the data show. There are also three wording
problems:
(a) "fixed in advance" hides that the configuration was chosen after the
campaign-3 diagnostic; Section 8.7 says "chosen after the campaign-3
diagnostic and fixed before the fresh instances were generated".
(b) "all 20 fresh path instances" is ambiguous, because there are 40 fresh
instances (Parts 4C3 and 4C4).
(c) "misses either nothing or δ²/2, depending on whether two point sets …
interleave" names the outcomes in the opposite order to the condition: the
loss is δ²/2 when the sets interleave. "Support cuts of the hull of their
joint graph keep it" has an unclear "it".

**Evidence.** 01b-results.tex:22–30; 08g-summary.tex:13–21; 09-conclusions.tex:42–49;
Tables 4 and 5. The abstract is at 248 of 250 words (formulas counted as one word).

**Fix.** Delete the framing sentence "We study when such cuts add strength,
how to compute them exactly for quadratic blocks, and how to keep them
valid." (21 words; the next sentences say exactly this). Replace the opening
and closing sentences as follows (about 247 words in total):
- Sentence 2: "Support cuts of the convex hull of their joint graph retain this
  dependence."
- Sentence on the path family: "For a family of quadratic directions on a
  three-variable path, the glued relaxation misses δ²/2 if two point sets at
  distance δ interleave and nothing otherwise; …"
- Last two sentences: "On MINLPLib models the cuts did not help SCIP. On
  constructed path and star families they closed nearly all of SCIP's root
  gap. A configuration fixed before fresh path instances were generated
  solved all 20, against at most 10 for SCIP and 5 for Gurobi; with a binding
  coupling row, SCIP without one presolve step did as well, faster, and on
  stars Gurobi solved more."

## [major] M4. Section 2.1 promises that Section 5.3 relates the joint-range inequalities and quadratic aggregations to the cuts; Section 5.3 does not

**Location.** sections/02-setting.tex:89–95 (p. 5); sections/05-original.tex:183–203
(p. 18).

**Issue.** Section 2.1: "Aggregations of quadratic constraints … [18, 40],
surrogate relaxations … [94], and the joint-range inequalities of Xu and
Pokutta [129] … are different objects; Section 5.3 relates them to our cuts."
Section 5.3 mentions the aggregation closure of Dey et al. [40] and, through
Appendix D, the surrogate relaxations [94]. Blekherman et al. [18] and Xu and
Pokutta [129] do not appear again. The Xu–Pokutta reference was added in
round 3 (it is absent from draft-round2/main.txt), so the pointer was not
updated. Xu and Pokutta also aggregate rows and convexify the joint range of
two quadratics to obtain solver cuts, which is close to this paper's cuts. A
referee will look for the promised comparison.

**Evidence.** `grep -n "XuPokutta\|Blekherman" sections/*.tex` matches only
02-setting.tex:90–93. evidence/literature-L1.md:360–370 summarizes [129]:
"Project-then-lift cuts … projected to the joint range of two quadratics …
closed form … SDP representation in the convex case".

**Fix.** Add one sentence at the end of Section 5.3 (05-original.tex:203):
"The joint-range inequalities of Xu and Pokutta [129] also aggregate rows and
convexify jointly, but in the two-dimensional image of two quadratic
functions over Rⁿ, where S-lemma arguments give closed forms; our cuts
convexify over a bounded block domain and certify the bound for the stored
row." This wording follows the L1 summary of [129]; check it against the
paper before using it. Alternatively, narrow the pointer in 02-setting.tex:94–95 to
"…are different objects; Section 5.3 and Appendix D relate the aggregation
closure and the surrogate relaxations to our cuts."

---

## [minor] m1. Section 5.3 and Appendix D repeat each other almost word for word

**Location.** sections/05-original.tex:184–203 (p. 18) and
sections/A-feasible-hull.tex:3–6, 33–50 (p. 49).

**Issue.** After Section 5.3 was condensed, both places contain the same text:
the opening "The closure C is a relaxation of the set Σ … Equality holds when
every row has its own free direction in the affine parts", the x² = 1/4
example with the measure 3/4 at 0 and 1/4 at 1, "This is a Lagrangian
duality gap [53, 106]", "closed by convexifying aggregated sets instead of
aggregated functions, as in the aggregation closure of Dey et al. [40]", and
"our implementation keeps nonlinear rows out of D so that the support
problems stay in the classes of Section 4".

**Evidence.** main.txt lines 975–986 and 2600–2639.

**Fix.** In Section 5.3, state the result once and point to the example:
"… Without such free directions the gap can be strict even for the complete
family of cuts: for the equality row x² = 1/4 on [0, 1], C = [1/4, 1/2]
while the feasible set is {1/2} (Example D.2). This Lagrangian duality gap
[53, 106] is closed by convexifying aggregated sets [40] or by placing the
row inside D; our implementation keeps nonlinear rows out of D so that the
support problems stay in the classes of Section 4. Appendix D places C in a
hierarchy with the surrogate relaxations of Müller et al. [94] and shows that
both inclusions can be strict." In Appendix D, replace lines 3–6 with "This
appendix proves the statements of Section 5.3." and delete the sentence
"It is also closed by placing the row inside D, … classes of Section 4."
(A-feasible-hull.tex:48–50).

## [minor] m2. Appendix H uses part labels without the campaign prefix

**Location.** sections/A-instances-D.tex:2–3, 13 (p. 57).

**Issue.** "The structure-selected models of Part B2 are those of Part B. The
pool of Part D consists of … Part D takes the first 20 …". Everywhere else
the labels are 4B2, 3B and 4D (Table 1). Round 2 (W8) asked for the Table 1
labels everywhere, and this paragraph was missed.

**Fix.** "The structure-selected models of Part 4B2 are those of Part 3B. The
pool of Part 4D consists of … Part 4D takes the first 20 …".

## [minor] m3. Mode names in Tables 7, 10 and 11 differ from the text; "mech." is a leftover

**Location.** sections/A-instances.tex:51–52, 62, 72–76 (Table 7, p. 57);
sections/B-tables.tex:56 (Table 10 caption, p. 60) and :102 (Table 11 caption,
p. 61).

**Issue.** The text and Tables 1, 4, 5 and 12–17 write SCIP-nolocks and
SCIP-extra. Table 7 lists the same modes as `baseline-novarlocks` and
`baseline-extra`, and the Table 10 and 11 captions use `baseline-extra`,
`baseline-noaggr` and `all-diag-noaggr`. A reader cannot find "SCIP-nolocks"
in the mode table. Table 7 also says "In the text, mech. (base) limits are
those of all-diag-mech" and has a row "whole row, mech. (Part 3P)", but the
text says only "base limits" (Section 7.2; Tables 4, 12). "mech." appears
nowhere else.

**Fix.**
- Table 7: rename the SCIP rows "SCIP-nolocks (code `baseline-novarlocks`)"
  and "SCIP-extra (code `baseline-extra`)", and the `*-noaggr` row "no
  aggregation (`*-noaggr`)".
- Table 7 caption: "Base limits are those of all-diag-mech and wide limits
  those of frozen-wide."
- Table 7 row: "whole row, base (Part 3P)".
- Tables 10 and 11: write "SCIP-extra" instead of `baseline-extra`, and
  "SCIP and all-diag with presolve aggregation disabled" instead of the code
  names.

## [minor] m4. Table 6 still says "Campaigns 2–4"

**Location.** sections/A-instances.tex:18 (Table 6, p. 56).

**Issue.** The column header is "Campaigns 2–4 (original variables)". Campaign
5 used the same implementation (protocol: "a new snapshot of the campaign-4
snapshot with two additions …, both off by default"), and its default limits
are the same. The header predates campaign 5. Table 7 says "Modes of
campaigns 3 to 5".

**Fix.** "Campaigns 2–5 (original variables)".

## [minor] m5. Section 8.1's rule on cross-campaign comparisons is incomplete, and Section 8.5 breaks it for times

**Location.** sections/08a-setup.tex:36–40 (p. 24); sections/08e-path.tex:166–169
(p. 32).

**Issue.**
(a) Section 8.1 names only Part 4C2 as compared across campaigns. Parts
5C-a and 5C-b also have no baseline of their own; they are compared with the
campaign-4 runs of 4C3 and 4C4 (Tables 4, 14, 15). The evidence for identical
root bounds across campaigns ("all 100 baseline root bounds rerun in Part
3P") covers only campaign 3.
(b) The sentence has no verb: "root bounds of identical runs repeated exactly
across campaigns (…), whereas solved counts and times are not paired across
campaigns".
(c) Section 8.1 says "We compare times only within these paired runs of one
part". Section 8.5 then compares times across campaigns: "SCIP-nolocks …
faster than the cut modes (shifted geometric means 2.0 s against 12 to
13 s)". SCIP-nolocks ran in Part 5C-a, the cut modes in Part 4C4. The factor
of six is far larger than any load effect, and the campaign-5 load (1–20) was
higher than the campaign-4 load (2–9), so the conclusion holds, but the text
should say so. The word "faster" is repeated in 01b-results.tex:26,
08g-summary.tex:17 and 09-conclusions.tex:45.

**Fix.** 08a-setup.tex:36–40: "Parts 4C2, 5C-a and 5C-b have no baseline of
their own; they are compared with the runs of the same instances in the
previous campaign. Root bounds of identical runs were reproduced exactly
across campaigns (all 100 baseline root bounds of campaign 3 rerun in Part
3P). Solved counts and times are not paired across campaigns, and we say so
where it matters." 08e-path.tex:167–168: "… faster than the cut modes
(shifted geometric means 2.0 s in Part 5C-a against 12 to 13 s in Part 4C4;
the runs are from different campaigns, but the factor is far larger than the
effect of host load)".

## [minor] m6. Section 8.1 omits the 300 s root budget of Part 5C-b and the hard process limits

**Location.** sections/08a-setup.tex:44–46 (p. 24).

**Issue.** "root runs have a node limit of one and a budget of 60 s (Parts 3A,
3B, 4B2) or 120 s (path family, Parts 4D and 5S)". The Part 5C-b root runs
had 300 s and up to 40 callbacks (Table 14 caption; protocol 5C-b: "300 s
soft / 360 s hard"). Section 8.6 and the Table 5 caption rely on "the hard
process limit", but Section 8.1 never defines it. The value (360 s) appears
only in the Table 17 caption.

**Fix.** "… or 120 s (path family, Parts 4D and 5S), and 300 s in Part 5C-b.
Each run also had a hard process limit (360 s for full runs), after which the
worker was stopped and the run counted as unsolved." The protocols state
the hard limit for full runs (campaign-v3-protocol.md:32) and for the
campaign-5 root runs (180 s and 360 s); state the others only if they are
recorded.

## [minor] m7. "Removal tolerance" is not defined

**Location.** sections/08b-validity.tex:75–76 (p. 26); Table 2 caption,
08b-validity.tex:25–40 (p. 26).

**Issue.** "The counts change little if the removal tolerance is raised
tenfold." The paper never defines a removal tolerance. The Table 2 caption
defines the threshold for "Wrong", but not the threshold for "cuts off".

**Evidence.** evidence/ablation-verify.md:130–141: "The removal tolerance
1e-6·max(1,‖c‖₁) …". With ten times this threshold the counts become
405→389, 132→128, 506→503 and 27→27, and the model lists do not change.

**Fix.** In the Table 2 caption: "'cuts off' counts the resulting rows that
an incumbent … violates by more than 10⁻⁶ max{1, ‖ĉ‖₁}". In the text:
"With ten times this threshold the counts become 389, 128, 503 and 27, and
the lists of models do not change."

## [minor] m8. "Made the root bound exact" and "closed the root gap that SCIP leaves" are stronger than the data

**Location.** sections/01b-results.tex:27–28 (p. 3); sections/08g-summary.tex:12–13,
18–19 (p. 34); sections/09-conclusions.tex:46–47 (p. 35).

**Issue.** Section 8.6 reports that the star-block root bound was "within
10⁻⁶ (relative) of the optimum". The summaries call this "exact". Section 8.7
also says "On the constructed families, exact block support closed the root
gap that SCIP leaves". With a binding row the cut modes closed medians of 95%
and 99% at the 16n cap, and the prospective configuration of Part 3C closed
19–35%.

**Fix.** Write "made the root bound optimal to within 10⁻⁶" (or "closed the
whole root gap") in all three places. 08g-summary.tex:12–13: "On the
constructed families, exact block support closed all or nearly all of the
root gap that SCIP leaves, once the separator could add enough cuts per
block."

## [minor] m9. Section 8.3 says the cuts had no root effect in Part 3A, then lists a Part 3A model improved by all-diag

**Location.** sections/08c-minlplib.tex:59–60, 71–74 (p. 28).

**Issue.** "At the root the cuts had a visible effect on four models of Part
3B and none of Part 3A." Later: all-diag "improved the root bound beyond the
tolerance on only one more model in each part (cvxnonsep_psig20r and
pooling_bental4pq)". cvxnonsep_psig20r belongs to Part 3A, so the first
statement can hold only for modes all and auto. pooling_bental4pq is already
one of the four Part 3B models, so "one more" must mean "one more than mode
all".

**Evidence.** Table 9: cvxnonsep_psig20r, root bound 35.6 (baseline) and
35.63 (all-diag), a difference of 8·10⁻⁴ relative, which is above the
tolerance of 10⁻⁴.

**Fix.** "In modes all and auto, the cuts changed the root bound visibly on
four models of Part 3B and on none of Part 3A." and "… improved the root
bound beyond the tolerance on one more model in each part than mode all
(cvxnonsep_psig20r in Part 3A, pooling_bental4pq in Part 3B)."

## [minor] m10. The binding-row paragraph puts the cut modes' root closure after the conclusion, with an unclear "they"

**Location.** sections/08e-path.tex:169–173, 183–185 (p. 32).

**Issue.** "With a binding row, most of the gap is thus within reach of SCIP's
own relaxation once implicit discreteness is switched off, and the part that
only the joint blocks close is small. At the root they closed a median of 95%
and 99% of SCIP's root gap." It is unclear whether "they" means the joint
blocks or the cut modes. The reader also cannot see that the remainder mode
(median 95%) closed less at the root than SCIP-nolocks (96–98%). In addition,
"99.9% (remainder directions) and 94% (whole-row directions) of the cuts were
LP directions" does not say which runs are meant. According to
evidence/campaign4-c4-digest.md:22 these are the 4C4 runs with the 16n cap
(11,986 of 12,000 cuts).

**Fix.** "… with a root bound that closed 96 to 98% of SCIP's root gap. At
the root, the cut modes closed medians of 95% (remainder directions) and 99%
(whole-row directions). With a binding row, most of the gap is thus within
reach of SCIP's own relaxation once implicit discreteness is switched off,
and the part that only the joint blocks close is small." And: "In the runs
with the 16n cap, 99.9% (remainder directions) and 94% (whole-row
directions) of the cuts were LP directions, …".

## [minor] m11. The safety-shift example cited in Section 6.1 concerns a different error

**Location.** sections/06-certification.tex:68–71 (p. 19–20).

**Issue.** "If a needed bound is infinite or the correction destroys the
violation, the row is discarded; a fixed safety shift does not replace the
calculation (Section 8.2 gives an example)." The sentence is about the
rounding correction of Proposition 6.1. Section 8.2's example is an error in
an uncertified support bound (Gurobi, 1.8·10⁻⁴). The rounding corrections
were at most 8.5·10⁻¹⁶, and a shift would have covered them.

**Fix.** "… the row is discarded. A fixed safety shift replaces neither this
correction nor the certified bound of (C1); Section 8.2 gives an uncertified
support bound whose error a shift of 10⁻⁶ does not cover."

## [minor] m12. Two citations are printed without brackets

**Location.** sections/06-certification.tex:40 (p. 19): "in src/scip/lp.c of
122)"; sections/A-bounds.tex:17 (p. 50): "(Bernstein enclosure; see, e.g., 50
and the references therein)".

**Issue.** `\citealp` inside parentheses prints a bare number, which reads as
a quantity ("of 122").

**Fix.** "in src/scip/lp.c of SCIP 10.0.2 [122])" (use `\citep`), and "Lemma
E.1 (Bernstein enclosure [50])" followed by "see [50] and the references
therein" in the text.

## [minor] m13. Terms used before they are defined, or never defined

**Location / issue / fix.**
- sections/01-introduction.tex:19 (p. 1): "bᵀF(x)" uses F before Section 2
  defines it. Fix: "… where F = (f₁, …, f_p) and w_j stands for f_j(x)".
- sections/02-setting.tex:162–168 (p. 6): the presolve step is described but
  not named. Sections 8.1 and 8.5 call it "implicit discreteness" and refer
  back to Section 2.1. Fix: add "(implicit discreteness)" after "SCIP's
  presolve then makes the variable binary …".
- sections/05-original.tex:128, 136 (p. 17): "direct cuts" is used nowhere
  else; the paper calls these "aggregated cuts" elsewhere (Theorem 5.2,
  Section 8.5). Fix: "aggregated cuts".
- sections/A-campaigns12.tex (p. 56): "tolerating a failed evaluation of an
  exchange sample" is not defined. Fix: "of a minimizer added to the sample
  set (Section 7.2)".
- Table 1 (p. 25) and Table 7 use the prefix `frozen-` without explanation.
  Fix: add to the Table 7 caption: "`frozen` marks the campaign-3 direction
  rule (remainder directions first)." (campaign-v4-protocol.md:26–30).

## [minor] m14. Section 9's "Second" combines two unrelated points in one 75-word sentence

**Location.** sections/09-conclusions.tex:3–19 (p. 35).

**Issue.** "Two points of the theory matter for solver design. … Second, for
stars, the merged blocks of Section 3, the support problem remains exactly
solvable in nearly linear time when rows couple the center with one leaf at a
time, and, as in safe-cut practice, certification does not constrain how
directions are found: only the final binary64 row, its bound over the whole
block domain and the row that the solver stores need to be checked, and all
of this can be replayed." The second sentence holds a separate result
(certification).

**Fix.** "Three points of the theory matter for solver design. … Second, for
stars, the merged blocks of Section 3, the support problem remains exactly
solvable in nearly linear time when rows couple the center with one leaf at a
time. Third, as in safe-cut practice, certification does not constrain how
directions are found: only the final binary64 row, its bound over the whole
block domain and the row that the solver stores need to be checked, and all
of this can be replayed."

## [suggestion] s1. Smaller wording fixes

- sections/08f-star.tex:46–48 (Table 5 caption, p. 34): "Eight full runs
  stopped at the hard process limit during a load spike count as unsolved"
  reads as a garden path. Fix: "The eight full runs that were stopped at the
  hard process limit during a load spike count as unsolved."
- sections/08b-validity.tex:79–84 (p. 26): one sentence has two colons. Fix:
  "… only one distinct cut, recorded four times on nvs02. Gurobi reported
  optimality with zero gap for a constant 1.8·10⁻⁴ above the true minimum,
  because a slope of −8.9·10⁻⁷ in one variable fell inside its optimality
  tolerance, and over that variable's range of 200 this lost 1.8·10⁻⁴."
- sections/03-composition.tex:290 (p. 10): "this matches the next
  paragraph" is vague. Fix: "…here the nonedge product xz, the product that
  closes the gap in the next paragraph."
- sections/03-composition.tex:350 (p. 11): "as the theorem above predicts".
  Fix: "as the three-variable theorem of Burer et al. predicts".
- sections/08c-minlplib.tex:124–125 (p. 29): "the blocks tried were then
  those with the smallest variable indices" seems to contradict "largest
  first" in Section 7.2. Fix: "…; all had four variables, so the tie-break by
  variable indices decided which blocks were tried."
- sections/08g-summary.tex:28–29 (p. 34): "the measured cost is an upper
  bound on that of a compiled separator" is not shown. Fix: "the measured
  cost likely overstates that of a compiled separator."
- "What we add" occurs four times (02-setting.tex:74, 03-composition.tex:207,
  383, 04-quadratic.tex:71). Vary or drop it, e.g. 03-composition.tex:383:
  "Our addition is that exact pair and star minima evaluate both sides."
- sections/08e-path.tex:10 (p. 30) uses k as a dummy index ({k/64}), while
  Section 8.6 uses k for the number of leaves and {m/64} for the grid. Fix:
  "{j/64 : j = 0, …, 48}".
- sections/08a-setup.tex:94 (Table 1, row 3P): "3A, 3B (root runs); 3C (post
  hoc)" attaches "post hoc" to 3C only, but the whole part is post hoc. Fix:
  "models of 3A and 3B; instances of 3C".
- sections/01-introduction.tex:96–99 (p. 3): the list of comparators leaves
  out SCIP without implicit discreteness, on which the binding-row conclusion
  rests. Fix: "… against SCIP's default, against SCIP without its
  implicit-discreteness presolve step, against SCIP's disabled-by-default
  nonconvex separators, …".
- sections/04-quadratic.tex:252–253 (p. 16): "Section 8.6 also compares the
  two star algorithms on random stars with up to 10⁴ leaves". The simpler
  oracle was run only up to k = 1000 (Part 4S). Fix: "Section 8.6 compares
  the two star algorithms on random stars with up to 1,000 leaves and runs
  the sweep up to 10⁴ leaves."
- sections/99-availability.tex:22: "licence" is the only British spelling
  ("behavior", "favor" and "modeling" elsewhere). Fix: "license".
- Table numbering: Table 7 is cited in Section 7.2 (p. 23) before Table 1,
  and Tables 8–11 are cited in Sections 8.3–8.4 before Tables 4–5. Springer
  asks for tables to be cited in numerical order. Fix: number the appendix
  tables separately (Table H.1, …) or renumber them.
