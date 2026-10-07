# Round 2: verification of the round-1 changes

Review date: 2026-10-04. Scope: the 59 numbered issues in the seven reviews
specified in the brief, the revised mathematical statements and proofs, changed
numeric displays, and the KAN and eg follow-up evidence. Paths and line numbers
below are relative to `paper-open-minlplib/`, unless stated otherwise. They refer
to the revised sources, not the round-1 sources.

**Verdict: minor revision.** The substantive mathematical corrections and all
changed certified numeric displays checked below pass. I found no new error that
invalidates a theorem, certified bound, optimum enclosure, or refutation. Three
new documentation/scope findings and five remaining findings need attention.
The public availability claim remains unverified; a valid local artifact index
does not establish public deposit.

## All numbered round-1 issues

There is one row per original numbered issue, including duplicates between
reviews. For a mixed issue with a rejected subpart, the assessment explains which
part was fixed and why the rejection is or is not justified. The two
`rejected-justified` rows concern proposed remedies whose underlying problems
have been addressed by another valid remedy.

| Original review and issue | Topic | Status | Revised evidence and assessment |
|---|---|---|---|
| sol-math-main 1 | Admissibility in the value-function recursion | resolved | `sections/04-split.tex:62` specifies nonempty control sets and maps from `Y_(i-1) × U_i` into `Y_i`; `:63` then gives the recursion. The missing domain condition is present. |
| sol-math-main 2 | Rationality of the camshape deficit | resolved | `sections/05-other.tex:71` says the bound is rational **when epsilon is rational**; `sections/B3-camshape.tex:210` gives the same qualification in its definition. |
| sol-math-main 3 | lukvle10 gap versus search tolerances | resolved | `sections/04-split.tex:296` says “dominated by,” rather than equal to, the summed tolerances; `sections/B1-lnts-lukvle10.tex:270` gives the two tolerances and the approximately `3.5e-16` difference. Global optimality remains unproved (`:271`). |
| sol-math-main 4 | catmix evidence level | resolved | `tables/tab-trust.tex:23`, `sections/B4-chain-catmix.tex:431`, and `sections/I-reproduction.tex:146` consistently classify the dual certificate as rerun. The supplement explicitly says its per-stage values are not stored. |
| sol-math-supp1 1 | Gibbs Hessian endpoint lower bound | resolved | `sections/B5-small.tex:158` defines both matrices with lower diagonal ends and the two off-diagonal ends; `:162` proves the pointwise quadratic bound; `:164` uses the smaller unconstrained minimum as a lower bound, rather than claiming equality with the box minimum. Outward evaluation of the centre value and gradient is explicit at `:165`. |
| sol-math-supp1 2 | LNTS mutation test description | resolved | `sections/B1-lnts-lukvle10.tex:68` now says changing the acceleration coefficient fails the model-structure assertion. It no longer attributes this rejection to the root-sign test. |
| sol-math-supp1 3 | lukvle10 exact gap attribution | resolved | `sections/B1-lnts-lukvle10.tex:269`–`:271` preserves the small discrepancy and the absence of a global-optimality proof; `sections/04-split.tex:296` agrees. |
| sol-math-supp1 4 | etamac fixed K1 margin | resolved | `sections/B5-small.tex:331` restricts the `0.047` margin to nonfixed variables and states that K1 equals its fixed value exactly. |
| sol-math-supp2 1 | KAN subnormal halving and vertex-location gap | resolved | `sections/B9-ann-kan.tex:317`–`:340` describes the guarded routine, exact fallback, complete six-model replay, and retained shared premises. It matches `development/reviews/round1/kan-guard/report.md`. The copied 72,240-case exact test passes; all six saved replay results have zero guard/fallback counts and reproduce the old rigorous-exp bounds. See the checks below. |
| sol-math-supp2 2 | False eg second-order remainder estimate | resolved | `sections/F-eg-rounding.tex:257`–`:261` replaces the false estimate with a positive-series bound for `exp(d)-1` and the affine estimate actually needed by the pad. The three rational inequalities and the copied follow-up math check pass. |
| sol-math-supp2 3 | eg binary64 primal claim under H0 alone | resolved | `sections/B7-eg.tex:327` explicitly adds correctness of the interval-mode implementation and its reader to H0. |
| sol-math-supp2 4 | eg exponential self-test bypass | resolved | `sections/B7-eg.tex:322` and `sections/C-points.tex:268` disclose the original bypass and name the separate enclosure/reciprocity test. Keeping the old self-test is acceptable because the replacement test actually exercises both signs of `1234/7`; its copied rerun passes 452 reciprocity checks. |
| sol-numbers 1 | Three unsafe S4 second-proof upper ends | resolved | `sections/E-audit.tex:276`, `:278`, `:284` print `-983842.2577881223`, `0.0079302187993`, and `-1.12968744117115`. Exact comparisons with the raw checker `obj_hi` values show that each is an upward decimal rounding. |
| sol-numbers 2 | SCIP binary64 violation cap | resolved | `sections/08-solvers.tex:68` prints `2.93e-15`. Exact evaluation of all eight copied witness models gives maximum `32122061/10995116277760000000000`, below the cap. |
| sol-numbers 3 | methanol50 coefficient-change cap | resolved | `sections/E-audit.tex:550` prints `2.39e-16` and the exact maximum `1/4196280000000000`. Re-reading both copied model files reproduces all 360 coefficient differences and this maximum. |
| sol-numbers 4 | Powerflow point objective-width cap | resolved | `tables/tab-points.tex:22` prints `2.83e-42`. Re-evaluating the objective over each stored proof box at the stated 80-digit precision gives widths approximately `2.28361418e-42`, `2.820814334e-42`, and `2.820814334e-42`; all pass exact rational comparisons with the cap. |
| sol-numbers 5 | Scope of automatic display checks | resolved | `data/make_tables.py:13`–`:21`, `sections/10-reproducibility.tex:31`, and `sections/I-reproduction.tex:47` restrict the automatic claim to generated certified displays and distinguish hand-written tables/fixed metadata. The copied generator passes 798 checks. The separate, broader assertion about the number file itself is still false: see N3. |
| sol-literature 1 | Unqualified negative literature claims | resolved | `sections/01-introduction.tex:111` restricts the benchmark assertion to records inspected in the search; `sections/D-literature.tex:173` scopes the tap-free-model assertion to the described search. |
| sol-literature 2 | Halbig verification standard | resolved | `sections/01-introduction.tex:113`–`:114` distinguishes convex certificates constructed/verified through auxiliary Gurobi solves from the paper's exact or outward-rounded verification. It does not imply that the precedent used the same arithmetic standard. |
| sol-literature 3 | Recent rigorous global optimization | resolved | `sections/01-introduction.tex:122`–`:123` discusses IbexOpt, certified LP post-processing, equality tolerances, and the reason no interval-solver comparison was run; `sections/B9-ann-kan.tex:117` connects the ANN approach to that work. `references.bib:62` adds Araya et al.; using issue 3 follows the local source record rather than the review's draft issue 2. |
| sol-literature 4 | Recent exact MIP/certificate literature | resolved | `sections/01-introduction.tex:125` names the propagation/dual-analysis, black-box VIPR, and numerical-correctness work, with their linear-MIP scope. The new Borst and Szeider entries are present at `references.bib:268` and `:1563`; all cited keys resolve. |
| sol-literature 5 | Page/version locators | resolved | `sections/01-introduction.tex:23` gives slide 23/PDF page 38, and `:26` gives Section 3.3/author-manuscript page 23. `sections/D-literature.tex:231` explicitly says page locators refer to the versions read and lists the relevant manuscripts, including Bertsimas et al. |
| sol-literature 6 | Dagstuhl report/contribution attribution | resolved | `references.bib:245` identifies the edited report and Berthold's contribution, Section 3.6/page 71; `sections/01-introduction.tex:118` attributes the cited discussion to that contribution. |
| opus-math-main 1 | Reading-(b) scope and unproved reading-(c) infeasibility | partly | The default-and-exceptions rule is corrected at `sections/02-semantics.tex:45`, and actual residual arguments are supplied at `sections/A-semantics.tex:82`–`:89`. However, `sections/11-conclusion.tex:53` again says **all** claims concern reading (b); the purported exception list at `sections/02-semantics.tex:46` also omits the audit's transfers. See U1. |
| opus-math-main 2 | Conflicting definitions of the display unit | resolved | The conflicting definition is removed from Section 2. The single definition at `sections/07-audit.tex:20` uses the largest power of ten dividing the nonzero displayed value, so the `10/9` argument at `:40` has the required meaning. |
| opus-math-main 3 | Forced slopes and costates | resolved | `sections/04-split.tex:89` explicitly says part (c) does not apply with dynamics equality rows kept. Its cross-reference leads to `sections/G-proofs-split.tex:197`–`:203`, which states the interiority requirement after eliminating those rows. The certificates still check their own slopes. |
| opus-math-main 4 | H0 versus Python conversion properties | resolved | `sections/02-semantics.tex:158` now makes correctly rounded Fraction/decimal conversion an additional assumption, rather than an IEEE consequence. |
| opus-math-main 5 | ANN inequality count | resolved | `sections/05-other.tex:286` states two-sided bounds on 722 determined variables plus the purity row: `2×722+1 = 1,445` one-sided inequalities. |
| opus-math-main 6 | Powerflow shifts and leaf relaxations | partly | The shift explanation is fixed at `sections/05-other.tex:170`–`:171`; the full proof identifies the angle-augmented leaf relaxation at `sections/B6-powerflow.tex:216`, and `:249`–`:256` gives the angle-free alternative. But `sections/05-other.tex:168`–`:169` still applies the stored 0039p multipliers to leaves defined without the angle rows. See U5. |
| opus-math-main 7 | QPLIB round-to-nearest assumption | partly | `sections/H-solvers.tex:108`–`:118` and `sections/08-solvers.tex:45` use the safe one-unit thresholds and margins; the exact comparisons pass. But `sections/B3-camshape.tex:289` still calls the old half-unit thresholds the upper ends of *all* numbers that display as the reported values, without assuming nearest rounding. See U2. |
| opus-math-main 8 | Maximization convention for U | resolved | `sections/02-semantics.tex:80` explicitly uses the lower enclosure end for maximization. |
| opus-math-main 9 | LNTS point/width conflation | resolved | `tables/tab-points.tex:17`–`:18` separates the attaining point from the Krawczyk witness. `sections/06-points.tex:68` gives the attaining point's integer-arithmetic width; `sections/B1-lnts-lukvle10.tex:112`–`:114` distinguishes the 110-digit enclosure from the stored 60-digit enclosure and replaces “contain” with “overlap.” |
| opus-math-main 10 | ANN second-code data reading | resolved | `sections/A-semantics.tex:44` identifies the rounded reading; `sections/B9-ann-kan.tex:138` explains outward enclosures and the additional rounding-error slack that covers it. `tables/tab-trust.tex:32` consistently summarizes the two codes as outward/rounded. |
| opus-math-main 11 | chain GAMS/OSIL identity overstatement | resolved | `sections/B4-chain-catmix.tex:24` now claims agreement of step, length, endpoints, and sampled row values, with a reference to the numerical comparison in `sections/A-semantics.tex:66`. It does not silently increase the exact-comparison count. |
| opus-math-main 12 | Replay-tier definition and assignments | partly | `sections/10-reproducibility.tex:45` gives precise per-instance thresholds, and the previously wrong lukvle10/ex6_2/catmix assignments are corrected at `:60`–`:62`. However, all six KAN enclosures remain Tier 2 even though the three r3 checks take under ten minutes. See N2. |
| opus-math-main 13 | Dropping the LNTS constant objective | resolved | Both `sections/04-split.tex:165` and `sections/G-proofs-split.tex:340` explicitly drop the constant `Nh` before invoking the zero-cost infeasibility form. |
| opus-claims 1 | AI provenance and meaning of separately written | resolved | `sections/02-semantics.tex:177`–`:191` discloses agent provenance, shared filesystem, first-code reading, shared components, side comparisons, and weaker/partial second checks; `:200` states the common-mode risk. `sections/11-conclusion.tex:76`–`:79` contains the AI-use declaration and marked author confirmation. This fixes the provenance problem; confirmation is visibly pending, not silently represented as completed. |
| opus-claims 2 | Unreviewed rocket/audit comparisons in the headline | rejected-justified | R-14 justifiably rejects reducing the headline to 19/15: the condition for retaining 22/18 has been met. `sections/E-audit.tex:477` records the second rocket rerun and `:549` records the exact model-comparison rerun; `development/open-items.md:56`–`:62` closes the task. The saved second brackets and three changed displays were checked. |
| opus-claims 3 | catmix stored versus rerun | resolved | `tables/tab-trust.tex:23`, `sections/B4-chain-catmix.tex:431`, and `sections/I-reproduction.tex:146` now agree on rerun. Its point check remains a stored exact evaluation, correctly distinguished from the dual search. |
| opus-claims 4 | Mechanical statuses and stale claim index | rejected-justified | The substantive fixes are implemented: explicit register statuses (`sections/I-reproduction.tex:105`), status parsing (`artifact/build_claims.py:22`–`:34`), and a passing current index (`sections/I-reproduction.tex:61`–`:63`). R-07 justifiably rejects calling conditional computer-assisted proofs “computed” merely because the second check is weaker: `sections/02-semantics.tex:195`–`:197` defines the distinction and the register marks weaker/partial second checks. The copied validator passes all 65 claims and hashes. |
| opus-claims 5 | Unscoped SCIP trigger | resolved | `sections/04-split.tex:322` limits the mechanism to the 15 wrong runs that were traced and refers to the solver section. It no longer explains all wrong runs by this identity. |
| opus-claims 6 | Equality-chain tolerance amplification | resolved | `sections/01-introduction.tex:63` describes coupled rows and separates the proved camshape bound from numerical attainment; `sections/05-other.tex:75`–`:76` names row-violation weights and the approximately 87% numerical example. `sections/11-conclusion.tex:22` uses the corrected formulation. |
| opus-claims 7 | Every point allegedly re-proved by separate code | resolved | The overbroad introductory sentence is removed; `sections/02-semantics.tex:191` and `sections/06-points.tex:77` explicitly name etamac/pricing050 as single-implementation primal claims. |
| opus-claims 8 | catmix per-stage agreement scope | resolved | The retained full certificate at `sections/B4-chain-catmix.tex:430` gives N=100, all 99 stages on the 324-ray grid, and 40 stages on the band grid. The old unqualified main box is removed. |
| opus-claims 9 | Library accuracy and math.fsum attribution | resolved | `sections/02-semantics.tex:152` names the second audit checker's accurate 90-digit exponential assumption. `sections/B8-waterno2.tex:274` treats correctly rounded math.fsum as a further program assumption, explicitly outside H0; `tables/tab-trust.tex:31` retains it. |
| opus-claims 10 | Missing shared readers/components | resolved | `sections/02-semantics.tex:187` includes waterno2, powerflow, and the small-family instances, and `:188` gives the separately checked reader outputs. `sections/B8-waterno2.tex:271`–`:274` explicitly names the shared reader and the second line's shared builder/relaxation/node bound. |
| opus-claims 11 | KAN path-II unchecked NaNs | resolved | `sections/05-other.tex:329`, `tables/tab-trust.tex:33`, and `sections/B9-ann-kan.tex:285`, `:358` all state path II's unchecked no-NaN premise. The guarded path-I evidence supplies the additional protection described above. |
| opus-claims 12 | Category A versus diagnosed tolerance cause | resolved | `tables/tab-claims.tex:8` defines the name as a category, not a diagnosis; the lukvle10 and ex6_2_5 entries mark the unknown cause/no reported violation. `sections/H-solvers.tex:85` says the same. |
| opus-claims 13 | Prior status of copies/restrictions | resolved | `tables/tab-closures.tex:33`, `:35` classify both camshape copies as related models. `sections/03-results.tex:70`–`:85` and `sections/D-literature.tex:54` retain the dtoc5 default-bound caveat. Independent counting reproduces 7/9/15. |
| opus-claims 14 | KAN “no optimal value” | resolved | `sections/03-results.tex:64`–`:65` states the stored optimum is positive infinity and distinguishes this from closure and from the relaxation bounds. |
| opus-claims 15 | camshape agreement “to all digits” | resolved | `sections/05-other.tex:67` says “to all printed digits,” consistent with the directed-rounding implementation. |
| opus-claims 16 | hvycrash witness-check count | resolved | `sections/05-other.tex:248`, `sections/06-points.tex:78`, and `sections/B5-small.tex:53` consistently say two codes checked the first witness and a third checked a second witness. |
| opus-claims 17 | Multiplier control stated for all certificates | resolved | `sections/02-semantics.tex:101`–`:103` restricts the claim to Lagrangian-type bounds and points that satisfy the kept constraints, and gives the norm bound explicitly. |
| opus-claims 18 | Register mapping and present public-archive assertion | rejected-unjustified | The result-level register mapping is fixed at `sections/01-introduction.tex:104` and `sections/10-reproducibility.tex:32`. R-17 does not justify the remaining present-tense public-deposit assertion: a promise to deposit before submission is not evidence of current deposit. `macros.tex:129`–`:131` still prints a DOI placeholder and `artifact/README.md:30` says it is to be added. This is a draft/publication-status issue, not a failure of the local artifact. See U3 and N3. |
| opus-claims 19 | Version of SCIP's witness acceptance | resolved | `sections/01-introduction.tex:93` and the proposition at `sections/08-solvers.tex:68` identify SCIP 10.0.2 for the eight-witness feasibility check. |
| opus-claims 20 | MINOTAUR wording outside category B | resolved | `sections/01-introduction.tex:97`, `sections/08-solvers.tex:125`, and `sections/D-literature.tex:104` use “invalid as recorded” with cause unknown and the input-equivalence assumption, rather than diagnosing a defect. |
| opus-claims 21 | Unscoped LNTS novelty / novelty of own KAN construct | resolved | `sections/B1-lnts-lukvle10.tex:125` scopes LNTS novelty to the literature search; `sections/D-literature.tex:61` says RP is the paper's own construction. |
| opus-claims 22 | Missing second reading of extended-value proofs | resolved | The premise has changed: the round-1 mathematical reviews did check those proofs. `sections/11-conclusion.tex:50` and `development/open-items.md:19` record that check and its agent provenance. Adding the old “not checked” caveat would now be false. |
| opus-claims 23 | Contradictory audit-priority development record | partly | `sections/D-literature.tex:35`–`:43` now lists the relevant readings, and `development/open-items.md:66`–`:70` acknowledges the priority sentence. But the next bullet (`:75`–`:77`) still includes the audit-novelty search among uncompleted prerequisites and says the paper makes no such sentence. See U4. |

| Status | Count |
|---|---:|
| resolved | 51 |
| partly | 5 |
| not resolved | 0 |
| rejected-justified | 2 |
| rejected-unjustified | 1 |
| **Total** | **59** |

## New findings from the revision diff

### N1 — minor: the new model-comparison summary omits audit exceptions

**Where:** `sections/02-semantics.tex:203`.

**Problem:** The new mitigation paragraph says the exactly compared GAMS and
OSIL forms agree except for catmix coefficients. It gives no restriction to the
43 principal instances. The same paper reports a different audit exception:
360 methanol50 objective coefficients differ (`sections/E-audit.tex:549`–`:551`),
and it also reports 30 differing lop97icx objective coefficients (`:552`).

**Evidence:** This sentence is new relative to the extracted archive. The exact
copied methanol50 comparison reproduces all 360 differences and maximum relative
change `1/4196280000000000`; thus its omission is not a merely hypothetical
exception. `sections/02-semantics.tex:51` also needs to make clear that its
instance comparison concerns the 43 principal instances, not every audited
instance mentioned in the paper.

**Fix:** Restrict the new sentence explicitly to the 43 principal instances and
refer to S4 for the audit comparisons and their exceptions. Alternatively, give
the exceptions wherever the broader comparison is asserted. Do not describe
numerical sample agreement as an exact identity comparison.

### N2 — minor: the precise new tier rule conflicts with KAN assignments

**Where:** `sections/10-reproducibility.tex:45`, `:62`;
`sections/I-reproduction.tex:215`–`:216`;
`sections/B9-ann-kan.tex:360`. Cross-listed under opus-math-main 12.

**Problem:** The revision defines Tier 1 by under ten minutes of recorded wall
time **per instance**, but assigns every KAN enclosure to Tier 2. Its own rows
give times as short as 22–23 seconds per model. The r3 instances qualify for
Tier 1 under the new rule. The family-wide maximum is not the defined criterion.

**Evidence:** The complete guarded replay report's time table gives r3 search
times of 24.74, 22.71, and 58.86 seconds. These agree with the short end of the
revised time ranges and contradict the uniform Tier-2 label. The record's six
concurrent processes are historical evidence, not processes run by this review.

**Fix:** Split the KAN assignment into r3/Tier 1 and r5/Tier 2 wherever a tier is
printed, or define explicitly that a grouped family takes its slowest member's
tier and apply that convention consistently. Keep wall time distinct from CPU
time.

### N3 — minor: the new introductory number-file promise is broader than the file

**Where:** `sections/01-introduction.tex:104`; repeated at
`sections/10-reproducibility.tex:30`.

**Problem:** To repair the register's “every number” claim, the revision now
promises that the number file has the exact source of **every displayed number**.
It does not: run times and some fixed metadata are outside that file. This moves
the universal assertion rather than making its scope accurate. The Section 10
version was already present before revision; the introductory promise is new.

**Evidence:** `sections/10-reproducibility.tex:14` explicitly says the times in
that section are not in `data/numbers.json`; `sections/I-reproduction.tex:47`
likewise distinguishes fixed metadata from the generated display checks. For
example, the replay times in Section 10 are sourced in its comments and register,
not stored with an exact value/source/rounding entry in the number file. The
generator's revised documentation at `data/make_tables.py:13`–`:21` correctly
states the narrower checking scope.

**Fix:** Say the file stores the generated certified bounds, primal ends, gaps,
and derived margins, and name the separate sources/checks for timings and fixed
metadata. This requires no additional data system or experiment.

## Remaining findings

### U1 — minor: the conclusion repeats the universal reading-(b) assertion

**Where:** `sections/11-conclusion.tex:53`;
`sections/02-semantics.tex:46`. Original opus-math-main 1.

**Problem and evidence:** The default rule at `sections/02-semantics.tex:45` is
correct, but the conclusion again asserts that all claims concern reading (b).
The catmix transfer, the binary64 solver statements, and the audit's GAMS transfer
at `sections/E-audit.tex:538`–`:543` are explicit counterexamples. The audit also
discusses binary64 checks at `:555` onward. The list introduced as “The exceptions
are” at Section 2 does not list the audit transfers. The new exact residual proofs
in Appendix A do fix the mathematical half of the original issue.

**Fix:** Refer to the Section 2 default rule and its named exceptions in the
conclusion. Make the exception list non-exhaustive or include the audit transfers.

### U2 — minor: the QPLIB-copy paragraph retains an unqualified half-unit claim

**Where:** `sections/B3-camshape.tex:289`. Original opus-math-main 7.

**Problem and evidence:** This unchanged sentence calls `-4.2843015` and
`-4.27735` the upper ends of the numbers that display as the reported values.
They are upper ends only under rounding to nearest. The corrected full statement
and proof at `sections/H-solvers.tex:108`–`:118` instead use one-unit thresholds
`-4.284301` and `-4.2773`, with nearest rounding explicitly conditional. Both
deficit bounds also exceed these safer thresholds, so the result survives.

**Fix:** Use the one-unit thresholds here too, or add the nearest-rounding
qualification and refer to the stronger one-unit result in the proposition.

### U3 — minor: public deposit is still asserted without verifiable evidence

**Where:** `sections/01-introduction.tex:104`,
`sections/10-reproducibility.tex:28`, `sections/11-conclusion.tex:72`;
`macros.tex:129`. Original opus-claims 18; adjudication R-17.

**Problem and evidence:** These are current public-archive/archived assertions,
while the DOI is a marked placeholder and `artifact/README.md:30` says it is to
be added before submission. I verified the local index, not a public release.
The evidence does not prove that no deposit exists, but it does not establish
the asserted deposit either. “Will be deposited before submission” is a future
action and cannot verify the present assertion; this is why R-17 is not a
justified resolution of the issue as reviewed.

**Fix:** Supply a verifiable deposited release, or describe the package as
prepared for deposit until that step is completed. Marking the draft DOI is
acceptable; representing unverified public availability as established is not.
No licence or author declaration needs to be invented by an editing agent.

### U4 — minor: the audit-priority record contradicts its own adjacent bullet

**Where:** `development/open-items.md:66`–`:77`. Original opus-claims 23.

**Problem and evidence:** The new first bullet says the audit-priority sentence
exists and the search sources are now listed. The next bullet still includes the
audit-novelty search among the readings required before any priority sentence and
says “The paper makes no such sentence.” The source list in
`sections/D-literature.tex:35`–`:43` supports closing the audit part of that item.

**Fix:** Remove the audit-novelty search from the remaining unread-area list, or
explicitly say it is closed and restrict “no such sentence” to the other areas.

### U5 — minor: the main powerflow sketch still omits the angle-row augmentation

**Where:** `sections/05-other.tex:168`–`:169`. Original opus-math-main 6.

**Problem and evidence:** The sketch defines its leaf relaxation by adding a box
and four affine rows to Q, which explicitly omits angle rows (`:128`). It then
applies the duality proposition with the leaf's stored multipliers. For 0039p
those multipliers include nonzero angle-row multipliers; the full proof correctly
uses the augmented relaxation Q_i^angle (`sections/B6-powerflow.tex:216`). The
next main-text sentence's acknowledgment of tiny angle-row multipliers does not
add their rows to the previously defined leaf relaxation. The full certificate
is valid, and the angle-free alternative at `sections/B6-powerflow.tex:249`–`:256`
also proves a stronger bound, so this is a defect in the sketch's application,
not a failure of the theorem.

**Fix:** Say that the stored 0039p certificate uses the angle-augmented leaf
relaxations, with a cross-reference to the full definition. Alternatively, base
the sketch explicitly on the checked angle-free multipliers and its zero shift.

## Targeted checks actually run

All repository executable sources were copied under `/tmp/sol-round2-verify/`
before execution or import. The old paper was extracted under that directory
from the supplied tar archive. No paper source was edited, no commit was made,
and no project-wide verification or CI inspection was run. Numerical-library
thread limits were one; no more than two checks ran concurrently, within the
four-core limit.

The following are local targeted results, not CI results:

| Check/command, executed on a copy unless it is a reviewer-written inline check | Result |
|---|---|
| `python3 /tmp/sol-round2-verify/new/paper-open-minlplib/data/make_tables.py` | 798 checks, zero failures. The generated certified ends/gaps for all 43 principal instances pass. |
| `python3 /tmp/sol-round2-verify/new/independent.py` | 470 independent numeric/display checks, zero failures. |
| Copied `make_campaign_table.py` and `make_points_table.py` | Both exit successfully. |
| `python3 /tmp/sol-round2-verify/check_revision.py` | Exact changed S4 endpoints, coefficient cap, campaign/prior partitions, guarded KAN log comparison, eg affine inequalities, and powerflow box-objective widths pass. |
| Reviewer-written exact check of all eight SCIP witness models using the copied `exact_check` module | Every decimal-model witness is exactly feasible; binary64-data maximum row violation is `32122061/10995116277760000000000 ≈ 2.92148442895e-15 ≤ 2.93e-15`. |
| Reviewer-written Fraction checks of the two QPLIB display margins and deficit thresholds | Safe margin lower bounds are `0.0031128485282566` and `0.0001547321953883`; both exceed the revised downward displays. The deficit comparisons still hold with the one-unit thresholds and objective-row tolerances. |
| `python3 eg_dyadic_check.py eg_int_s eg_disc_s eg_disc2_s`, in `/tmp/sol-round2-verify/eg/` | All bounds/integrality checks exact; all 28 row margins positive for each point. Smallest objective-row slacks approximately `5.5744e-20`, `7.8003e-20`, `7.4919e-20`. |
| `python3 exp_test.py`, in that copied eg directory | 227 negative-point, 453 signed-interval, and 452 exact reciprocity tests pass. |
| `python3 check_math.py`, in that copied eg directory | The affine weight estimate passes; the counterexample to the removed second-order estimate is reproduced. |
| `python3 test_minquad.py`, in `/tmp/sol-round2-verify/kan/` | All 72,240 rational comparisons pass; scalar/broadcast/empty/signed-zero/invalid-input and conversion tests pass. The original subnormal counterexample remains unsafe, while the guarded routine returns a safe bound. |
| Copied `artifact/check_claims.py`, pointed at the revised working tree read-only | PASS: 65 claims, 5,334 SHA-256 references, 1,894 distinct files, all paths and LaTeX labels valid. |
| Reviewer-written source reference/citation scan, including infobox label options | 401 distinct labels, 1,486 reference occurrences, 406 citation occurrences; no missing reference, duplicate label, or missing bibliography key. |
| `pdftotext -layout` on the existing `build/main.pdf` and `build/supplement.pdf`, with output in `/tmp` | The changed caps/partitions and reviewed text are present in the built documents. No rebuild was performed by this review. |

The independent campaign partition, read directly from the copied `results.csv`,
is **109 = 79 + 6 + 6 + 18**: same-model finite duals with a globality guarantee,
BARON-disclaimed values, SCIP-tightened-domain values, and KAN values. The groups
are disjoint. The 79 split as BARON 23, Gurobi 30, SCIP 26. The prior-status
partition is **31 = 7 + 9 + 15**: four fp closures plus three fp near-closures;
one listed solve, five related models, one value-only record and two unread
sources; fifteen with no prior global result found. These agree with the revised
tables and main-text counts.

The S4 upper-end checks used the raw second-checker `obj_hi` fields, not merely
the displayed values or the table generator's acceptance. For each revised
display `d`, the exact test was `obj_hi ≤ d < obj_hi + 10^(-decimal_places)`.
The methanol50 comparison re-read the actual copied GAMS and OSIL objectives,
not just the archived reported maximum. The powerflow width check evaluates the
objective on the stored boxes; it does **not** re-execute the Krawczyk existence
proofs, whose certificates and unchanged results were inspected.

For KAN I compared all six guarded JSON results to the previous rigorous-exp
results, checked completion/open-box/guard/fallback fields, and compared each
bound with the exact paper bound. The guarded source hash is
`e5783a244eda1b24e0767a4c676931a4a5b995fcf6946407b34a783a18df57eb`, matching the
source prefix printed at `sections/B9-ann-kan.tex:355`. I read the guard proof and
matched the revised trust paragraph to the follow-up report. I did **not** rerun
the six complete searches or the full eg dual audit in this round; their complete
retained runs are evidence reviewed here, distinct from the targeted executions
above. The eg primal/exponential/math checks were executed afresh.

The diff review compared the main and supplement inputs, all section sources,
generated tables, numeric data, bibliography, and artifact status builder. An
inventory of the labeled theorem/lemma/proposition/corollary/hypothesis
environments found 129 in each version, with 40 changed bodies. I checked the
changed hypotheses, statement relocations and condensed arguments, including
extended-value conventions, eliminated-stage interiority, the optcdeg2 split
reindexing/telescoping, the Gibbs quadratic lower bound, and the eg affine
padding estimate. The KAN and eg corrections preserve the premises they need;
no lost hypothesis or broken full proof was found. The main powerflow sketch
still has the application mismatch in U5. N1–N3 are the new problems found in
that comparison; U1–U5 identify remaining round-1 problems.

Scratch sources and final logs are retained in `/tmp/sol-round2-verify/`, notably
`generator.log`, `independent.log`, `exact.log`, `scip-eight.log`,
`eg-primal.log`, `eg-exp.log`, `eg-math.log`, `minquad.log`, `claims.log`, and
`crossrefs.log`.
