# Review of CLOSEOUT.md (round 1)

Date: 2026-10-04. Reviewer: independent Opus critic, run as four parallel
sub-checks (three-variable streams; scip-rule-fidelity and multiround;
intersection-literature, split-practice and binary-separation; minor-sets,
ratio-bound and orbit-closure). The critic's own combined write-up was lost
when the session restarted; the coordinating agent assembled this file from
the four sub-check reports without changing their findings. "Reviewed" means
checked by another research agent.

**Verdict: major problems (local).** Every quoted number that was checked
matches the notes, review histories match the verdict lines, renumbering and
commit-status statements are correct, and all links resolve. Five stream
summaries restate a proved result incorrectly, and several corrections, open
questions and results are missing. All fixes are local to CLOSEOUT.md, plus a
few nits inside notes.

## Major

1. **Three-variable completeness, solver relevance (CLOSEOUT ~562–563).**
   "Completeness in three variables would justify a compact exact replacement"
   contradicts three-var-completeness/note.md:100–103: if Conjecture 2.11
   holds, `R` plus caps is exact but uses 27 localizing and 24 5×5 blocks,
   more than the six 4×4 DNN blocks of the Anstreicher–Burer lift. "Exact
   replacement" is the computation note's wording for its Conjecture 1. Also
   add the stream's actual solver-relevance result (note:93–99): for
   three-variable box QPs that already use the disjoint system, family blocks
   are needed only when the cross coefficients have positive product
   (Theorem 2.5); in larger models the relevant quadratic is a dual
   aggregate.
2. **Multiround (CLOSEOUT ~184).** "Proved: … arbitrarily shallow
   bound-optimal choices can fail" is not shown. Proposition 5 shows only
   that bound-optimal sets need not be uniformly deep (multiround
   note:1168–1170: "Proposition 5 does not show that the bound-optimal loop
   fails"); open question 2 (note:1602–1605) lists a provably failing rule as
   open. Use "bound-optimal choices need not be uniformly deep
   (Proposition 5)".
3. **Orbit-closure Corollary 4 (CLOSEOUT ~288–289, ~844).** Corollary 4 says
   closure exactness holds iff single-cut exactness holds (smooth face,
   |J^c| ≤ 1), not that the bounds are equal. The closure can still be
   larger (up to 0.084 of z_K for (B), orbit note:79–81; §7 rows adv8_1,
   adv8_4). Errata item 8 already words this correctly. Fix ~844 too:
   combining cuts can improve the bound in support-two directions, but
   cannot make it exact unless one cut already is.
4. **Minor-sets Proposition 11 (CLOSEOUT ~225–228).** It is in §6, not §7.3.
   SCIP's set (2√δ) and the BCM family (≤ 11.1√δ) both vanish; the point-rule
   and orbit families attain z_K (minor note:540–541, 563–564).
5. **Orbit-closure ratios (CLOSEOUT ~303–304, ~903–904).** The note's factor is
   ρ = sup_w z_K/z_cl. "Closure/single-cut improvement is unbounded" contradicts
   Proposition 5 (z_1 ≥ z_cl/N). Open question 2 should be finiteness of ρ_A
   and ρ_B at the Theorem 14 corner (orbit note:593–594, 1069–1071).

## Minor — stream summaries

- **three-var-computation review history (~515–517):** r1's main finding was
  the 70.01% artefact (important issue; strict re-audit by reviewer), AP
  mismatch and timing; r2 raised headline precision (conditional exact-depth
  bounds 0.079%, 0.56%/0.60%); r2's ε = 10⁻⁷ sensitivity premise was corrected
  by the author (note:453–455). r1 verdict: minor fixes, issue 1 required
  before verification.
- **three-var-computation cost (~504–508):** add the cactus result (XF/F
  2.1–5.7: block type, not selection, dominates there).
- **three-var-computation omissions:** the edge-sharing `ht` result (methods
  closed at most 0.514% of the gap, note:83–84, 842–851) qualifies "performs
  well on constructed instances" (~21, ~503); the three random-sparse
  instances with unresolved U − B 0.13–0.39 and stored gain terms 5.97%,
  2.82%, 19.88% (note:622–626).
- **three-var-completeness package 3 (~976, ~1000):** add the novelty caveats
  (note:1063–1065: Theorems 4.2 and 2.5 are short consequences of BKT/BNW
  and may be known) and that BNW is a recent preprint read but not verified
  line by line (note:1282–1283).
- **three-var errata:** erratum 25 should also update
  ../research-20260925/three-positive-exploration.md §7 (lines 411–413);
  "containing K_4" → "containing a K_4 minor" (~789–790); erratum 28 cite
  family note §5 only; erratum 27 should convey that the 21,000 instances
  already had positive cross coefficients (note:732–737).
- **three-var nits:** S1 rerun was by the author in the r2 revision
  (logs/check_boundary_rank_symbolic_r2_revision.txt), not by the
  coordinating agent (~568–569); use "positive-loop hull H_n^+" (~534, ~553);
  Theorem 4.4 needs a *pointed* cone (~555); add computation open question 4
  (cheaper selection rule, note:1309–1311).
- **scip-rule-fidelity (~85–88):** the four records are of one instance,
  `waterund32` k=651, 715, 1138, 1292; drift is the ≈1e-14 LP value of the
  bilinear partner of `t_x612`, "present in the dumped LP values". Solver
  estimates were used only for ρ ≥ 4 (232 records); ρ ≤ 2 exact up to
  floating point, ρ = 3 by KKT enumeration (note:511–519).
- **scip-rule-fidelity omissions:** gap numbers (positive-z_K MINLPLib corners:
  median 0.923 per corner, 0.818 instance-weighted, about a third below 0.5;
  generator medians 0.976 and 0.992); main mechanism (183 of 371 low-ratio
  records: SCIP's set exits a zero-rate ray never reaching S); failure rates
  (37.7% generate a cut, 49.5% dynamism aborts, 12.7% zero basis status);
  source-audit findings (`ignorebadrayrestriction`/`ignorenhighre` do the
  opposite of their descriptions; cut limit counts generated cuts, reset at
  restarts). Fidelity r1 verdict was "Minor fixes" with one major-rated
  issue M1 (~104–105).
- **multiround (~166, ~730–731):** the withdrawn claim attributed about 40%
  (0.017 of 0.044) of the reversal to the bug, not "most".
- **multiround (~172):** one orbit round at the root already costs about
  half of the orbit rule's loss (o1s pooled −0.006 [−0.011, −0.002]); state
  it that way.
- **multiround (~173–174):** +0.004 is an AUC over rounds 1–10 (Holm
  p = 0.025); after round 10 alone Holm p = 0.33.
- **multiround (~182–183):** Theorem 2 needs only uniform depth; pointed
  cones enter via Corollary 3/Lemma 4; scope is the loop cutting every
  violated term or a one-cut loop on a most-violated term (Remark 3a); the
  observed cones become flat (pointedness 0.001), so the theorem does not
  apply to the experiments.
- **multiround nits:** "not confirmed by the within-rule or the intervention
  test", underpowered (~169–170).
- **scip-set-selection (~121–136, ~821–822):** the 81.6% figure is the floored
  corner criterion min_j w̃_j α_j attained at a zero-cost ray (a positive
  surrogate while the true single-cut bound is zero), from a full scan of
  109,389 corners on 305 root instances, not a sample; only fully degenerate
  corners (9%) hit the acceptance threshold. The 24-angle grid applies only
  for dim λ = 2 (projected subgradient ascent otherwise). Round 2 also
  withdrew the "instrumentation distortion" attribution. Final status:
  review round 3 (`scip-set-selection/reviews/review-r3.md`) **verified** the
  r2 revision — update CLOSEOUT and PROGRAM.md accordingly.
- **minor-sets (~231–232):** principal minors with det M̄ > 0 are proved (§8:
  PSD cone is the unique maximal set, SCIP's cut attains z_K); only
  det M̄ < 0 is not studied. Nit (~213): "although" → SCIP's ratio is lower
  still.
- **ratio-bound (~257–265, ~273–274):** the lower end 1/(1+√2) is Theorem A's
  analytic proof; only 1.54 is computer-assisted (B3(4)); the margin is a
  relative discriminant, not an angle; add the positive result H_cyl > 1
  sufficient with sharp threshold 1 (Theorem C(4), Proposition C3). r1's
  three minor issues were: wrong reason for three failed box searches;
  numerical values presented as exact; unstated SCIP scope.
- **ratio-bound open question 1 (~901–902):** the open boundary case of
  Theorem C(3) is for family (A); the (B) question is whether the interval
  test extends; Proposition C2 disproves any angle-only criterion.
- **orbit-closure omissions:** Proposition 5 (closure gains at most a factor N
  over the best single cut); (B) exact at the W-corner (Theorem 11(d)); BP has
  ρ = ∞ already at the Theorem 14 corner (Theorem 11(a)).
- **intersection-literature (~338–350, ~623):** Prop 2(b) is KY Ex. 4.3 "with
  a quadratic sublevel set in place of their discrete sequence"; for bilinear
  S, containment holds iff the full-cone condition holds, so Proposition A
  applies to none of the 120 corners; KY Cor. 3.12′ is "proved, given KY
  Prop. 3.11", not every step of Prop. 3.11 was checked, KY is an unrefereed
  draft; Kılınç-Karzan–Steffy Cor. 2 has no cone hypothesis.
- **split-practice (~375, ~388–396):** "three capped results remain
  uncertified, two of them dense and shown cap-sensitive"; 171 + 12 ≠ 187 —
  four closed or nearly closed points of rank 2–12 sit in between; use w as
  in Lemma A; Prop. C(a) holds for every psd Y; Proposition D is
  "NP-complete in the ordinary sense".
- **binary-separation (~440–457):** (q+3)/(4qN) is the maximum over pure
  hypermetric and odd clique families at εd̃; the (18) maximum is at d″
  (Letchford 2022 numbering — say so); gap-0 separation is NP-complete but
  strong NP-completeness is not shown; r1 found the encoding issue and
  proposed the fix, the first revision applied it. Package 1: proofs of the
  bit-complexity bounds are given and reviewed (say "formalize/polish", not
  "write as complete proofs"); list the unread earlier sources (Deza–Laurent
  Ch. 28 full text, Laurent–Poljak 1996, Boros–Hammer 1993, Erdahl 1992) and
  the folklore caveat (note:1132–1144).

## Minor — errata and open questions

- Erratum 22: the split note does not cite Laurent–Poljak; reframe as a
  citation caution (the mix-up is in GKL 2012's reference list).
- Erratum 19: also the split note §8 Limits bullet "The hard points need not
  satisfy binary structure" (line 706), answered by binary Corollary 6; and
  split-separation-review.md "still open" at lines 24, 371, 395.
- Erratum 14: add the §9.2 correction (62 corners, was 60; 22, was 26;
  sfree:1164–1165).
- Erratum 15: add completion B 4×4 round 1 0.863→0.891 and 6×8 rounds 2/3
  0.796/0.832→0.799/0.828; 4×4 "8 of 12 better, 1 worse" → "9 of 12, none
  worse"; the §9.3 "wins the first round on average" qualification.
- Erratum 13: other unrechecked uses of `core.corner_bound` (validation,
  adversarial and random corners); fidelity says only "probably not
  affected"; the firmer statement is multiround's.
- Erratum 18: location is sfree §3 (lines 338–342), not §11.
- New erratum: sfree §11 (lines 1344–1347) says SCIP's set is a
  reimplementation, not extracted cuts; fidelity §8 now extracted SCIP's cuts
  and found they match.
- Errata 10/12: also the sfree Summary "Open" paragraph quote "0.028 near ∂S"
  (line 103); the 97% at line 70 stays roughly right with 0.0305.
- Errata 8: "§3.4" of the scouting report is not traced to the orbit note's
  corrections; source it or drop it.
- Consolidated open questions — add: gap-0 strong hardness; intersection-
  literature §15 (equality-case attainment characterization; Eckstein–Nediak
  route); a later KY version / Prop. 3.11; fidelity OQ4 (why most checkable
  cuts never enter an LP; intended per-expression limit) and OQ6 (full-space
  formulation for ρ ≥ 4 brackets); multiround OQ3 (switching schedules inside
  SCIP) and OQ4 (causality of shorter steps, unmeasured rules, better-powered
  maj2 vs rnd0.33, tie-free bound-optimal set); orbit OQ1 (closure exact
  while no single cut is, support one) and OQ3 (why P/BP closure equals the
  single cut); minor OQ4 (closure exactness for minors) and OQ6 (whether
  `nlhdlr_quadratic` produces C_U cuts — also a work-not-run row); ratio OQ2
  (margin μ dependence), OQ3 (cheap repair of SCIP's +1 constant), OQ6 (SCIP
  Case 2); three-var computation OQ4.

## Nits inside notes (fix in the notes)

- scip-rule-fidelity/note.md:1126 "This is too large to commit" is stale:
  113 dump files under `logs/runs_minlplib` (2.20 GB) are tracked since
  commit c3514f03e.
- multiround/note.md: orbit ties on 10×20 "13–34%" (lines 74, 475) vs
  "17–34%" (line 504); Limits (line 1578) says Theorem 2 needs pointed cones —
  it does not.
- three-var-computation/note.md:1296 restates Conjecture 1 without
  Y_ii ≤ x_i (line 693 includes it); line 1250 Clarabel tolerance 10⁻⁹ vs §2
  (line 209) 10⁻⁸ — check and make consistent.
- three-var-completeness/note.md:3 "continued 2026-10-02" — revisions were
  made on 2026-10-03.
- binary-separation/note.md:7 "Complete proofs … are in §10" — proofs are in
  §§3–6; §10 is checks.
- minor-sets header still "revised 2026-10-03 after review round 3"; r4
  optional edits recorded only in §10.3 — add a short §10.4 entry or header
  note.
- ratio-bound "Dates" paragraph omits the 2026-10-03 r2 revision.
- scip-set-selection: update header, Summary last sentence and round-2
  revision entry to cite review round 3 (verified); optional r3 items O1
  (cross-reference the within-batch 1.0999 common-solved comparison in
  §§7.1–7.2), O2 (§7.3 still lists matching wall/CPU ratios as mitigating),
  O3 (gabriel01 shared rows differ only in time/memory columns).

## Checks run by the sub-checks

Read-only: reading all notes, reviews, coordination files and CLOSEOUT.md;
grep audits for stale numbering and commit statements; `git diff`, `git log`,
`git ls-files`; small inline arithmetic for quoted ratios; `wc`, `grep -c` and
`sha256sum` on the stopped BP log. No files were edited by the critic.
