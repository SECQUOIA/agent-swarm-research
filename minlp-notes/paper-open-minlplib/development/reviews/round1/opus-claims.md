# Round 1 review: claims, qualifiers and trust base (lens: opus-claims)

Date: 2026-10-04. Reviewer lens: overclaiming and qualifier drift in the main
paper and the supplement; novelty statements; "proved" vs "verified by a
separately written implementation" vs "computed" vs floating-point output vs
interpretation; the trust base of each certificate (Table 1 against the text);
category A/B language for solvers and published results; outline section 8
("claims that must NOT be made").

Paths are relative to `paper-open-minlplib/` unless they start with `R/`
(`research-20260929/`) or `D/` (`development/`).

## Verdict

**Major revision before submission (1 blocker, 5 major, 17 minor).**
Most of the outline section 8 list is respected. The numbers I checked
against `data/numbers.json` are consistent, including the audit counts, the
campaign counts, the 12-of-31 headline count, the 11 gaps at most 3.00e-13
and the branching census of Section 9. The category A/B vocabulary is used
carefully for BARON, the QPLIB copies, the KAN values and the emfl points. The
problems are elsewhere:
- the provenance of the "separately written" code and the "separate reviews"
  is not disclosed;
- the headline audit count includes refutations whose required review rerun
  has not been done;
- the evidence level of catmix contradicts its own supplement;
- the archived claim register assigns proof-status labels mechanically and is
  currently invalid;
- the SCIP trigger and one of the three headline lessons are stated more
  broadly than the evidence allows.

## Checks run (targeted, local)

- Read all main-text sections, Appendices A and B, and supplement sections
  B1–B9, C, D, E, F, H, I and J, in whole or in part, together with the
  generated tables `tab-trust`, `tab-closures`, `tab-unclosed`, `tab-kan`,
  `tab-points` and `tab-claims`.
- Read the cross-references in `D/outline.md` (sections 0.4, 3, 4 and 8),
  `D/decision-register.md`, `D/terminology.md`, `D/open-items.md`,
  `D/revision-notes.md`, `D/data-semantics.md`, `D/integration-notes.md` and
  `D/numbers-check.md`, the dossiers and critiques for waterno2, small and
  chain-catmix, `R/open-instances-summary.md`, `R/open-instances-scout/targets.md`,
  `R/open-instances-wave3/report.md`, and the KB notes for halbig2024,
  nowak2008, kuznetsov2024, bonami2018 and the MINLPLib documentation.
- Recomputed the following from `data/numbers.json` with inline Python:
  - audit solver and instance counts, the class (i) split (11 gross, 8
    tolerance-scale) and the 12 exact-rational refutations;
  - campaign totals (129 runs, 109 finite duals, 5 improvements);
  - the listed-dual-below-|U|/2 count (12) and the δ ≤ 3e-13 count (11).
- Copied `artifact/check_claims.py` to `/tmp/claimchk` and ran it read-only
  against the repository. Result: `FAIL: 256 errors; 66 claims; 1841 files checked`.
- Read `artifact/build_claims.py:179` (the label rule). Listed the
  `verification_label` of every entry of `artifact/claims.json`.
- No CI results are referred to. No repository script was run in place, and
  no paper file was edited.

---

## Blocker

### 1. The AI-agent provenance of the implementations and reviews is not disclosed, and the text reads as if humans did independent work (blocker)

- **Where.**
  - `sections/02-semantics.tex:192`: "the supplement calls the two the *authors' code* and the *verifier's code*".
  - `sections/02-semantics.tex:206`: "All implementations were written within this project".
  - `sections/01-introduction.tex:54`: "We built each dual bound by hand"; also `sections/08-solvers.tex:129` and `sections/11-conclusion.tex:61`.
  - "Second party" and "different party": `sections/03-results.tex:54`, `sections/B8-waterno2.tex:219`, `sections/B9-ann-kan.tex:67,258,323`.
  - "A separate review read …": `sections/B5-small.tex:184`, `sections/B9-ann-kan.tex:316`, `sections/F-eg-rounding.tex:420`, `sections/I-reproduction.tex:318`.
  - `sections/11-conclusion.tex:1-2`: the comment "No AI-use statement (revision decision 8)".
- **Problem.**
  - The paper's main robustness argument is that a second, separately written implementation rechecked each certificate (abstract l.11; §2.6). Several hand proofs were also "read" by a "second party" or a "separate review".
  - Per the development record, the certificates, the second implementations and the reviews were all produced by AI-agent sessions. The paper never says so.
  - Phrases such as "by hand", "the authors' code", "second party" and "separate review" will be read as independent human work. This overstates how independent the checks are: same-model agent sessions can share systematic misreadings beyond the OSIL-semantics risk that §2.6 names.
  - The disclosure is also inconsistent within the paper. B3:292 and B4:497 say "none is peer review", while B1, B2 and B5–B9 say nothing.
- **Evidence.**
  - `D/outline.md` §4.6 marks the disclosure as required in §2.6 and in the declarations.
  - Outline §8 item 10 forbids "'Independent' without the definition and the AI-agent disclosure", "Independently reviewed by humans, unless true" and "Describing internal verification as peer review".
  - `D/decision-register.md` G-09 says to distinguish "reproduced by a separate implementation in this project (AI agent)" from a human review. O-3 says the critics' passes "are AI-agent reviews and should be described as such".
  - `D/integration-notes.md:267-275` records that decision D7 removed every AI statement and conflicts with outline §8 item 10.
  - `D/dossiers/primal-points.md:471`: "The authors and reviewers are AI agents".
  - MPC is a Springer journal. Springer's editorial policy requires LLM use to be documented in the methods.
- **Fix.** Reopen decision D7 with the lead author. This is a submission-policy and honesty issue, not a style choice.
  - Add to §2.6, after l.206: "The certificates, both implementations of each check and the code and proof readings called 'reviews' in the supplement were produced by separate AI-agent sessions (large language model) under the authors' direction; no human reviewer has rechecked them. 'Separately written' means that one session wrote the second implementation without importing or reading the first session's code. Sessions of the same model can share systematic errors, so separately written code reduces common-mode risk less than code by different people would."
  - Replace "by hand" with "individually for each instance" at intro:54, §8:129 and §11:61.
  - Replace "second party" and "separate review" with "a separate agent session (not a human review)" at every location listed above.
  - Put an AI-use statement in "Statements and declarations" (§11:79).
  - Make the B1–B9 verification records uniform. Either every one carries the B3/B4 sentence, or none does and §2.6 states it once.

---

## Major

### 2. The headline audit count includes the rocket refutations and the GAMS/OSIL statement before the review rerun that the register requires (major)

- **Where.**
  - `sections/00-abstract.tex:12` ("we prove 22 on 18 instances invalid") and `sections/01-introduction.tex:8`.
  - `sections/01-introduction.tex:112`, `sections/07-audit.tex:109-111` ("two implementations agree … In all, 22 bounds on 18 instances").
  - `sections/07-audit.tex:58-59` (the refutation "also holds for the GAMS form …; an exact comparison (one implementation) found the two forms identical for 14 of the 15") and `sections/E-audit.tex:554-566`.
- **Problem.**
  - The outline's abstract and C5 plan count 19 bounds on 15 instances. `numbers.json` `headline.audit` still records 19 and 15.
  - The paper raised the headline to 22 on 18 by adding the three rocket bounds. Their second proof has not had the reviewer rerun that the register makes a condition for inclusion.
  - The second rocket proof also rests on mpmath's non-interval `exp` at 90 digits (E-audit:513).
  - rocket100's margin is 1.06 display units. That is below 10/9, so it needs Hypothesis H itself (§7:110).
  - The same unmet condition applies to the statement that the refutations hold for the GAMS form.
- **Evidence.**
  - `D/decision-register.md` AU-04: "Rocket second implementation unreviewed. Include after the reviewer rerun (C-44)".
  - AU-03: "Include 'certificates hold for both forms' only after a reviewer reruns `gms_osil_drive*.py` … otherwise say 'OSIL model'".
  - C-44 is marked "do (review)".
  - `D/open-items.md` §3: "Needed: the reviewer rerun … before the paper relies on them. Relies on it: Section 7 (the rocket refutations, cor:audit-tolerance(b))". Item 3 says this has not been done.
- **Fix.** Either run C-44 (minutes) and record it in E-audit and the open items, or scope the claims as follows.
  - Abstract l.12: "…we prove 19 on 15 instances invalid under a stated hypothesis on page displays, and three more on `rocket` whose second proof awaits an independent rerun."
  - Intro l.8: "19 (and three further `rocket` bounds)".
  - §7:111: "In all, 22 bounds on 18 instances are proved invalid under Hypothesis H, 16 of them LINDO's; the second proofs of the three `rocket` refutations and the exact GAMS/OSIL comparison have not been rerun by a reviewer."
  - §7:58-59: drop "it also holds for the GAMS form …", or keep it with "(one implementation, not independently rerun)".

### 3. The catmix evidence level is "stored" in Table 1 and the main certificate box, but "rerun" by the supplement's own account (major)

- **Where.** `tables/tab-trust.tex:27` (level "stored"); `sections/04-split.tex:307` (certificate box "Evidence level: stored"); the register row in `sections/I-reproduction.tex` (catmix "3; stored"); `sections/03-results.tex:60` ("For the ten closures at evidence level rerun").
- **Problem.**
  - §2.5 defines *stored* as a stored finite certificate checked by replay, and *rerun* as a check that needs a deterministic rerun of a search whose tree is not stored.
  - The catmix check recomputes the whole chord-minorant dynamic program (20–46 min per instance, Tier 3). Floating-point steps decide where to cut (B4:401), and the per-stage values are not stored.
  - B4 says so: "The per-stage values w^(i) are not stored, so checking requires a rerun".
  - The Table 1 level is therefore too strong, and the "ten closures" count at level rerun should be 14.
- **Evidence.** `sections/B4-chain-catmix.tex:401,412`; `D/decision-register.md` CC-11 ("Per-stage w not saved").
- **Fix.** Set catmix to `\evid{rerun}` in `make_tables.py` (Table 1), in `sections/04-split.tex:307` and in the register row. Change `sections/03-results.tex:60` to "For the 14 closures at evidence level rerun".
  - Alternative: redefine *stored* as "replayed from stored inputs without a search" and state that the catmix check recomputes, but does not store, its value-function data. In that case B4:412 must not say "rerun".

### 4. The archived claim register assigns proof-status labels by a mechanical rule that contradicts §2.6, and the index is currently invalid (major)

- **Where.**
  - `artifact/build_claims.py:179`: `level='proved' if '\evid{P}' in trust else 'verified by a separately written implementation' if '\evid{S}' in trust else 'computed'`.
  - `artifact/claims.json` (`verification_label`); `sections/I-reproduction.tex:48-51`; `sections/02-semantics.tex:204`.
- **Problem.** §2.6 defines three statuses:
  - *proved*;
  - *verified by a separately written implementation* (a second implementation reproduced it);
  - *computed* (one implementation produced it).

  The paper never assigns these per result; only the archive does. The builder derives them from the evidence level (hand, stored, rerun), which is a different property. As a result:
  - Results with level "rerun" are labelled "verified", including some whose second code does not reproduce the displayed value:
    - lukvle10 (register-04): the second code certifies only 352.238025369202;
    - eg (register-17): the second certificate covers only part of eg_disc2_s;
    - ann (register-18): §2.6 lists the second code as an exception to "separately written".
  - Results with level "stored" are labelled "computed", although the paper reports two or more separately written implementations:
    - powerflow (register-14, register-15);
    - KAN infeasibility (register-19), with two exact codes;
    - the audit (register-22), where every refutation was repeated by a second checker;
    - the SCIP witnesses (register-24), with six to eight checkers;
    - the points (register-21).
  - The builder tests for the old macros `\evid{P}`/`\evid{S}`, but the paper now writes `\evid{hand}`/`\evid{stored}`/`\evid{rerun}`. A rebuild would label every entry "computed".
  - `check_claims.py`, run on a /tmp copy, currently reports `FAIL: 256 errors; 66 claims`. I-reproduction:51 says that at build time the index was "all valid"; that is true only historically.
- **Evidence.** The `verification_label` listing of `artifact/claims.json`; the validator output above; `D/open-items.md` §4 ("claims.json … is now stale").
- **Fix.**
  - Add an explicit `verification_status` per register row, chosen by the rule of §2.6:
    - "proved" (hand proof, possibly with a stored check) for lnts, dtoc5, camshape and hvycrash;
    - "verified by a separately written implementation" where the second code reproduces the displayed value: chain, waterno2, powerflow, KAN (the weaker L), ex6_2_*, the audit's 19 pairs, the SCIP witnesses and the primal points except etamac and pricing050;
    - "computed (second code certifies a weaker bound / part of the domain)" for optcdeg2, lukvle10, catmix, etamac, pindyck and eg_disc2_s;
    - for ann, state the exception.
  - Print this status as a column of Table 1 or of `tab:repro-register`.
  - Fix `build_claims.py` to read that column instead of the evidence macros.
  - Rebuild and validate the index after the last edit. Change I-reproduction:51 to describe the state at submission.

### 5. The SCIP trigger is stated without scope in §4.5, contradicting §8 and the outline (major)

- **Where.** `sections/04-split.tex:368`: "All five points use identities of the decimal data such as 0.7³=0.343, and this cube identity is the one that triggers the SCIP error."
- **Problem.**
  - The mechanism was traced only in 15 instrumented runs.
  - One wrong run (pair2236, seed shift 11) first loses the witness at a 0.85 station, where the tightest enclosure meets the bound. It "is not linked to the mechanism" (§8:90; H-solvers:284), and two further runs were not traced.
  - The sentence asserts that the cube identity is *the* trigger of *the* error, which is a forbidden claim.
- **Evidence.** `D/outline.md` §8.6: "That the SCIP mechanism explains every wrong run". Register SV-13 and SV-17.
- **Fix.** "…such as 0.7³=0.343; in the 15 wrong SCIP runs that we traced, the binary64 residual of this cube identity triggered the error (Section 8.2)."

### 6. Headline lesson 3 attributes tolerance amplification to "long chains of equality rows", which the evidence does not show (major)

- **Where.** `sections/01-introduction.tex:66`: "Some listed and published optimal values hold only within tolerances, and long chains of equality rows amplify such tolerance effects."
- **Problem.**
  - The only quantitative evidence is camshape. Its proved deficit bound D_n(ε) ≤ 0.61 n² ε accumulates violations of the inequality rows G_j through the Chebyshev weights U_m (§5.1:86). It is a proved upper bound, and attainment (about 87%) is numerical evidence.
  - No equality-chain instance shows an amplified deficit. lnts50 p1, with violation 9.1e-10, lies only 4.3e-11 below the optimum.
  - §2.2:101 says only that the multiplier mass "can grow".
  - This is one of the three headline lessons, repeated in §11:76.
- **Evidence.** `sections/05-other.tex:21-23,82-88` (G_j rows at l.21); `tab-claims` rows lnts50 and camshape; decision register J-09 and CS-05.
- **Fix.** "Some listed and published optimal values hold only within tolerances, and along long chains of coupled rows a tolerance can lower the objective by far more than its own size: for `camshape` we prove a deficit bound of about 0.6 n²ε, and explicit tolerance-feasible points reach about 87% of it (numerical evidence)."

---

## Minor

### 7. "Re-proofs by separately written code" for every point overstates (minor)

- **Where.** `sections/01-introduction.tex:92`.
- **Problem.** The etamac and pricing050 primal claims each rest on one implementation (§2.6:199; §6.3:82; Table 1 rows 29–30).
- **Fix.** "What is new is the points themselves and, for all but `etamac` and `pricing050`, their re-proofs by separately written code."

### 8. The scope of the catmix per-stage agreement is dropped in the main certificate box (minor)

- **Where.** `sections/04-split.tex:306`: "agrees with the first per stage within 9.44e-15 on identical inputs".
- **Problem.** The agreement was tested only on test inputs for N = 100: all 99 stages on a 324-ray grid and 40 stages on a 2^-21-band grid (B4:411; register CC-02).
- **Fix.** "…and, on identical test inputs for N=100, agrees with the first per stage within 9.44e-15."

### 9. "No displayed result assumes an error bound for a floating-point library function" needs scoping, and B8 misattributes exact summation to H0 (minor)

- **Where.** `sections/02-semantics.tex:158`; `sections/E-audit.tex:322,513`; `sections/B8-waterno2.tex:218,288`.
- **Problem.**
  - The audit checker V1, which supplies the second proof for glider100, ghg_3veh and the rocket instances, "needs mpmath's exp at 90 digits to be accurate far beyond its widening of 10^-60". That is a non-interval library-accuracy assumption, and it is outside the trust-base list of §2.5. T-mp covers only mpmath interval arithmetic.
  - B8:288 lists "exactly rounded summation (hyp:fp-ieee)" for V_fl. H0 covers single operations, conversion and `nextafter`, not exactly rounded n-term summation (a library routine such as `math.fsum`).
- **Fix.**
  - §2.5: "No proof of record assumes an error bound for a library function; the second audit checker V1 assumes an accurate 90-digit mpmath exponential (Section S4)."
  - B8:288: replace "(hyp:fp-ieee)" with "(Python's correctly rounded `math.fsum`, an additional T-code assumption)", and list it in Table 1's waterno2 row.

### 10. The list of named shared components in §2.6 is incomplete (minor)

- **Where.** `sections/02-semantics.tex:193-195`.
- **Problem.** §2.6 names mpmath, the KAN exponential and interval core, and one OSIL reader cross-checked "for ann_cumene_tanh and the KAN instances". It omits:
  - the waterno2 lines: both branch-and-bound codes share the OSIL reader (B8:50), and V_ex and V_fl share the builder, relaxation and node bound (B8:286);
  - the small-family verifier, which shares the parser `osilx.py` with the authors (`D/dossiers/small.md:787`).
- **Fix.** "A third is one OSIL reader used by several decoders (among them both `waterno2` branch-and-bound codes and both small-family dual codes); a separately written reader reproduced its output exactly for `ann_cumene_tanh`, the KAN and the `waterno2` instances."

### 11. The KAN redundancy claim omits the unchecked NaN assumption of path (II) (minor)

- **Where.** `sections/05-other.tex:383`; `tables/tab-trust.tex:37`.
- **Problem.**
  - The text says L "is valid if either code is correct". B9:285 says path (II) "discards NaN bounds silently, so it assumes, without a check, that none occurred".
  - B9:323 says "Neither code was read line by line by a third party".
  - So the redundancy rests on path (I), or on path (II) together with an unchecked assumption. The main text and Table 1 do not say this.
- **Fix.** Add to §5.5:383: "(path (II) assumes, without a check, that no NaN bound occurred)". Add to Table 1's KAN cell: "path (II) assumes no NaN".

### 12. "Tolerance artifact" is applied to values without evidence of a tolerance cause (minor)

- **Where.** `tables/tab-claims.tex:8` (caption "category A, tolerance artifacts"), row 34 (lukvle10 SIF SOLTN 352.237) and row 38 (Kosolap's ex6_2_5 "optimum" −70.9586, at least 0.206 below L).
- **Problem.**
  - Category A is defined by non-attainability alone (Def. 2.4). The name nevertheless attributes the value to a tolerance.
  - A deficit of 0.29% on ex6_2_5 with no reported violation, and a SIF value with no optimality claim and an inferred origin, may come from other model data or from errors.
  - The register uses "cause unknown" wording elsewhere.
- **Fix.** Put "cause unknown; violation not reported" in the qualifier column of both rows. In the caption write "(category A: not attainable under exact feasibility; 'tolerance artifact' names the category, not a diagnosed cause)".

### 13. Prior-status classes are applied inconsistently to copies and restrictions (minor)

- **Where.**
  - `tables/tab-closures.tex:41,43` (camshape200 "listed solve", camshape800 "none").
  - `sections/D-literature.tex:116-127`.
  - `sections/01-introduction.tex:81` ("floating-point closures or near-closures of the same model"); dtoc5 "fp closure".
- **Problem.**
  - Octeract's listing for the rounded copy QPLIB_2480 makes camshape200 a "listed solve", although D-lit:119 says that "a closure of the copy … is not one of camshape200".
  - MINOTAUR's listed solve of the copy QPLIB_3177 leaves camshape800 at "none".
  - dtoc5's "fp closure" is MINOTAUR's solve of a copy under assumed default bounds, that is, a bounded restriction (B2:85). D-lit:14 defines "same model" as the stored file or an algebraically identical copy.
- **Fix.**
  - Treat both camshape copies alike: either both "related model", or camshape800 also "listed solve (rounded copy)".
  - Intro:81: "For seven of them, floating-point closures or near-closures of the same model, or for `dtoc5` of a copy under assumed variable bounds, were reported."

### 14. The paper says it claims "no optimal value" for the KAN models although it proves v* = +∞ (minor)

- **Where.** `sections/03-results.tex:72`, against `sections/B9-ann-kan.tex:253` ("So v*=+∞ for the six OSIL models").
- **Fix.** "No KAN instance is closed: the stored models have optimal value +∞ (no exactly feasible point), and our bounds do not concern their tolerance-feasible points."

### 15. camshape: "agree on v_n to all digits" (minor)

- **Where.** `sections/05-other.tex:72`.
- **Problem.** One of the three codes uses directed rounding and cannot reproduce a rational "to all digits". Table 1 (l.24) and the register say "to all printed digits".
- **Fix.** "…agree on v_n to all printed digits."

### 16. The number of codes that checked the hvycrash witnesses differs between places (minor)

- **Where.** `tables/tab-trust.tex:33` ("two codes"); `sections/05-other.tex:284` ("three codes checked the witnesses"); `sections/06-points.tex:83` ("the two computer checks"); `sections/B5-small.tex:44`.
- **Problem.** B5 says two codes checked witness 1 and the verifier's code checked witness 2.
- **Fix.** Use one count everywhere: "two codes checked the first witness and a third code a second witness".

### 17. "Only by an amount that the multipliers control" is overgeneral (minor)

- **Where.** `sections/02-semantics.tex:98`.
- **Problem.**
  - The control holds only for Lagrangian-type certificates, and only if the kept constraints X hold exactly.
  - It says nothing about the comparison certificates (camshape), the identity (hvycrash) or the Taylor-model and branch-and-bound certificates. For the KAN instances, B9:330 gives a different mechanism.
- **Fix.** "For a Lagrangian-type certificate, a point that satisfies the kept constraints and violates the dualized rows by at most τ can lie below L only by an amount that the multipliers control."

### 18. "A claim register that maps every reported number" conflicts with §10, and "archived" is stated as present fact while the DOI is a placeholder (minor)

- **Where.** `sections/01-introduction.tex:146`; `sections/10-reproducibility.tex:24-26,86`; `sections/00-abstract.tex:15`; `sections/11-conclusion.tex:77,82`; `macros.tex:129`.
- **Problem.**
  - The number file covers every displayed number. The claim register has 66 entries (27 results and 39 reported values).
  - `\archiveDOI` prints a red placeholder, and the claim index currently fails validation (issue 4).
- **Fix.** Intro:146: "…a number file with the exact source of every displayed number, a claim register that maps each result to its checkers and inputs, …". Keep "archived" only once the DOI exists (decision D8).

### 19. "SCIP's own feasibility check accepts" the witnesses does not name the version (minor)

- **Where.** `sections/01-introduction.tex:122`; `sections/02-semantics.tex:116`.
- **Problem.** Only SCIP 10.0.2's check was run on the eight witnesses (§8:54), while the claim concerns 10.0.2, 10.0.3, 10.1.0 and dev.
- **Fix.** "…which SCIP 10.0.2's feasibility check accepts…".

### 20. MINOTAUR's report is called "false", outside the fixed category-B wording (minor)

- **Where.** `sections/01-introduction.tex:127`; `sections/08-solvers.tex:115`; `sections/D-literature.tex:104`.
- **Problem.** §2.4:121 promises "fixed wording", and Def. 2.4(B) gives "invalid as listed" or "invalid as recorded; cause unknown".
- **Fix.** "…is invalid as recorded (cause unknown), assuming that its `.nl` file encodes the MINLPLib model `optcdeg2`."

### 21. Two novelty statements are unscoped or concern our own construct (minor)

- **Where.** `sections/B1-lnts-lukvle10.tex:136` ("what is new is the attaining control, the scalar equation g(ν)=0 and the rigorous enclosure"); `sections/D-literature.tex:59` ("…for the six KAN instances … a rigorous enclosure of the optimal value of R_P").
- **Problem.**
  - The discrete linear-tangent law is a discretization of a classical steering law, and B1 does not limit the statement to the search.
  - R_P is a model we defined, so "no earlier result" about it is vacuous. Outline §8.1 forbids any "first" about R_P.
- **Fix.**
  - B1:136: "…to our knowledge, within the search of Section S3, the attaining discrete control, the scalar equation g(ν)=0 and the rigorous enclosure are new."
  - D-lit:59: drop "and a rigorous enclosure of the optimal value of R_P", or replace it with "(R_P is our own construction)".

### 22. The limitations do not say which hand proofs have had no second reading (minor)

- **Where.** `sections/11-conclusion.tex:50-55`; `sections/G-proofs-split.tex`.
- **Problem.**
  - `D/open-items.md` §1 records that the extended-value proofs of Appendix B, on which `thm:catmix-bound` and `thm:waterno2-bounds` rest, have had no separate check (register PT-06: 2–4 reviewer-hours).
  - lnts Theorem 3 and the dtoc5 certificate did have separate readings.
  - The paper presents all of them alike, as proved.
- **Fix.** Add to §11.2: "The extended-value proofs of Appendix B, used by the `catmix` and `waterno2` theorems, have not been checked by a second reader; the `lnts` and `dtoc5` proofs and the `eg` rounding analysis have (by agent sessions; see §2.6)."

### 23. Development record: open-items says the paper makes no audit-priority sentence, but it does (minor)

- **Where.** `D/open-items.md` §4 ("The paper makes no such sentence"), against `sections/01-introduction.tex:117` and `sections/D-literature.tex:39`.
- **Problem.** Register O-8 and AU-02 make the "audit-novelty search" reading a precondition for any priority sentence about the audit. The paper contains such a sentence, with a search qualifier.
- **Fix.** Either record in D-literature §S3.1 which audit-novelty sources were read (the paragraph "Benchmark checks and solver reliability" partly does this) and close O-8 for the audit, or correct `D/open-items.md`. No paper change is needed if the reading was done.

---

## Items checked and found consistent (no action)

- **Outline §8 items respected:**
  - no unconditional "first";
  - no "zero duality gap", "exact dual value" or "7.2e-43" for dtoc5 (§4.2:223; B2:55,70);
  - no lukvle10 global optimality (§4.4:335);
  - camshape and hvycrash results stated for reading (b) only;
  - "15 of 31", not "most";
  - catmix is not an instance of Lemma 4.1 (§4.1:70);
  - no BARON failure, and BARON's tolerance-level closures credited;
  - MINOTAUR camshape800 is category A only;
  - SCIP's listed bounds are not called wrong (§8:94);
  - "later patch releases not tested";
  - no speed ranking;
  - eg: no exact optimum, …993 not …994;
  - waterno2: 1.68% and 6.21, and p4 not claimed as ours;
  - no unsafe display of §8.11 printed as a bound (all appear only in Appendix J).
- **Category language:** BARON camshape100/200, the QPLIB copies, the KAN SCIP values and the emfl primal values are consistently category A. The SCIP, CAMINO and MINOTAUR findings are category B, and "defect" is reserved for SCIP.
- **Counts:**
  - audit: 13 LINDO class-(i) bounds on 13 instances; 11 gross and 8 tolerance-scale (1.91e-9 to 3.32e-7); 12 exact-rational refutations; 10 instances marked solved;
  - campaign: 109 finite duals, 5 improvements, 35 values beyond a certified bound;
  - closures: 12 of 31 with the listed dual more than |U|/2 below U; 11 with δ ≤ 3.00e-13;
  - branching census: 12 + 6 + 7 + 2 + 1 + 3 = 31.
- **Priority qualifiers** in C1 and C3 and in §3.4 match outline C1/C3 and the unread-sources list in D-literature §S3.3.
- **eg trust statement:** the revision-notes items 1–4 from the eg audit review are applied (F:337,343; F:275; F:360-366; F:32,36).
