# Final verification of the round-3 fixes

Checked on 2026-10-05 against the final sources and the final build:

- `build/main.pdf`, 56 pages, SHA-256 `65069e02…0582aba`;
- `build/supplement.pdf`, 131 pages, SHA-256 `4fee2118…6794c6`.

Both hashes equal those in `artifact/RELEASE.md`. No source file is newer than
`build/main.pdf`; only `artifact/RELEASE.md` and two files in `artifact/logs/`
are newer. Each item of the four round-3 reviews was checked in the sources
(file:line below, paths relative to `paper-open-minlplib/`) and, for the paper,
in the text extracted from the PDFs. The pre-round-3 sources used for the diffs
are `/tmp/suppgrp-orig/` (see `development/build-final.md`).

Verdicts: **resolved**; **partly**; **not resolved**; **deviated-justified**
(the fix differs from the reviewer's text for a reason that a fact check
supports). Author actions that the instructions keep open, such as
placeholders and upstream reports, are marked **author action**.

## 1. Result

- **All 39 action items are resolved or deviated-justified.** They are sol-referee
  1–3, sol-status 1–5, opus-referee 1–10 and opus-writing 1–22, with the
  optional opus-referee 8 counted as deviated-justified.
- **No certified number changed.** Every `exact` and `display` field of
  `data/numbers.json` is unchanged; the round only added fields.
- **The corrected §8.2 statement is true.** It agrees with Lemma S6.3, its proof,
  S1.8 and Appendix A.4. Section 2 gives my own exact check.
- **The 155-instance description is correct.** It matches S3.4 and the funnel
  table.
- **The §2.6 status definitions are correct.** They now agree with Table 1, the
  register and `claims.json`.
- **Remaining problems are minor.** Two are small artifact inconsistencies
  (Section 7, items R1 and R2). The others are optional wording points. Author
  actions remain open as instructed.

## 2. The §8.2 rounding fact (opus-referee 1)

`sections/08-solvers.tex:106` now reads: "although $0.7^3=0.343$, the tightest
interval with binary64 ends around $\fl(0.7)^3$ lies strictly below
$\fl(0.343)$; for the other station values $\ell$ and powers $k$ of waterno2,
the residual $\fl(\ell)^k-\fl(\ell^k)$ is smaller than one binary64 spacing, so
the tightest such interval still contains $\fl(\ell^k)$ (Lemma S6.3)."

I checked this with Python `Fraction` on the exact binary64 values. Python's
`float()` parses decimal strings with correct rounding. Script:
`/tmp/verify-r3/cube.py`.

| $\ell^k$ | $\fl(\ell)^k-\fl(\ell^k)$ | spacing on that side of $\fl(\ell^k)$ | tightest binary64 interval around $\fl(\ell)^k$ | contains $\fl(\ell^k)$ |
|---|---|---|---|---|
| $0.7^3$ vs 0.343 | $-9.23706\cdot10^{-17}$ | $2^{-54}=5.551\cdot10^{-17}$ | [0.3429999999999999, 0.34299999999999997] | **no** |
| $0.7^2$ vs 0.49 | $-5.32907\cdot10^{-17}$ | $2^{-54}$ | [0.48999999999999994, 0.49] | yes |
| $0.6^2$ vs 0.36 | $-1.33227\cdot10^{-17}$ | $2^{-54}$ | [0.35999999999999993, 0.36] | yes |
| $0.6^3$ vs 0.216 | $-2.15383\cdot10^{-17}$ | $2^{-55}=2.776\cdot10^{-17}$ | [0.21599999999999997, 0.216] | yes |
| $0.85^2$ vs 0.7225 | $-6.88338\cdot10^{-17}$ | $2^{-53}$ | [0.7224999999999999, 0.7225] | yes |
| $0.85^3$ vs 0.614125 | $-8.01026\cdot10^{-17}$ | $2^{-53}=1.110\cdot10^{-16}$ | [0.6141249999999999, 0.614125] | yes |
| $0.8^2$ vs 0.64 | $+5.77316\cdot10^{-17}$ | $2^{-53}$ | [0.64, 0.6400000000000001] | yes |
| $0.8^3$ vs 0.512 | $+7.46070\cdot10^{-17}$ | $2^{-53}$ | [0.512, 0.5120000000000001] | yes |

Consequences:

- **The old sentence was false.** $\fl(0.6)^3<\fl(0.216)$,
  $\fl(0.85)^3<\fl(0.614125)$ and $\fl(0.7)^2<\fl(0.49)$ all hold, so other
  powers also show a gap.
- **The new sentence is true.** Only $0.7^3$ has a residual larger in magnitude
  than the spacing ($2^{-54}<|r|<2^{-53}$). None of the $\fl(\ell^k)$ is a power
  of two, so the spacing is the same on both sides.
- **Lemma S6.3 checks out** (`sections/H-solvers.tex:272–285`): $a<\fl(0.7)^3<b$,
  $a$ and $b$ are binary64, they print as stated, $\fl(0.343)-0.343\approx2.7\cdot10^{-17}$,
  and every listed residual and spacing is correct.
- **The step trace is correct.** The outward activity
  $[\fl(0.343)-3\cdot2^{-54},\,b]$ prints as
  [0.34299999999999986, 0.34299999999999997].
- **The fm336 bound is correct.** $5\fl(0.343)+\fl(0.1)+2\fl(0.216)>2.247$
  (`H-solvers.tex:265–266`).
- **No contradiction remains** with Appendix A.4 ("for stations A, B2 and D the
  binary64 values violate these identities", `sections/A-semantics.tex:97`) or
  with S1.8 (`sections/B8-waterno2.tex:49–52`, residual $<-9.2\cdot10^{-17}$).
  Those passages say that the identities fail; §8.2 says only the $0.7$ cube
  fails by more than one spacing.

Optional precision point: §8.2 says "smaller than one binary64 spacing"; the
lemma's proof says "smaller in absolute value". Read literally, a negative
residual is always "smaller", so adding "in absolute value" would make the
contrast with $0.7^3$ explicit.

## 3. sol-referee.md

| Item | Verdict | Evidence |
|---|---|---|
| 1. Qualify GAMS/OSIL correspondence | **resolved** in the paper; small artifact residual (R1) | Abstract `00-abstract.tex:17`; C3 `01-introduction.tex:98–100`; Figure 1 caption `03-results.tex:32–33`; §8 opening `08-solvers.tex:52–53`; §8.3 `08-solvers.tex:155–157, 160`; S6.1 `H-solvers.tex:32`; S6.3 `H-solvers.tex:71, 76–77`. The 79/30 split and the BARON credit are kept. Table 8 (`A-semantics.tex:61–72`) gives 17 identical + 4 `catmix` + 22 sampled (16 non-KAN, 6 KAN), which matches the new text. The instances named at `08:157` (lnts, chain, pricing050, etamac, KAN) are all in the sampled rows. |
| 2. Executable guarded KAN replay recipe | **resolved** | `artifact/README.md:281–318` and `artifact/RUNS.md:475–499` hold byte-identical command blocks (diffed). The six-core exception of the archived driver is stated at `README.md:174–178`, `RUNS.md:333–337` and `I-reproduction.tex:51`. The per-instance alternative runs one process at a time. S7.1 links it (`I-reproduction.tex:52`) and so does S7.4 (`:268`). The archived code stays in `development/reviews/round1/kan-guard/`, which is in the archive and hashed by the register, so no copy into `artifact/` was needed. The editors' fresh-copy run of the three `r3` replays passed, with a negative control (`artifact/logs/kan-guard-recipe-test.log`). My checks are listed after this table. |
| 3. Name the replay behind the catmix tier | **resolved** | §10 rule `10-reproducibility.tex:62`; Table 7 `:79`; S1.4 box `B4-chain-catmix.tex:401`; register caption `I-reproduction.tex:118` and row `:153` ("2 (2nd: 3 for catmix800)"); `README.md:255–257, 268`; `RUNS.md:24–26, 122–125`. Times kept: 1,049–4,602 s, so Tier 3 only for `catmix800`. |

My checks of the guarded KAN recipe (item 2):

- `bash -n` on the extracted block and `compile()` on its embedded Python: both pass.
- I staged the recipe's tree in `/tmp/verify-r3/kanwork`: the research-module
  subtrees, the guarded code and the six KAN OSIL files, linked through
  `$HOME/.cache`.
- In that staged copy, `kan_decode`, `kan_iv` and the guarded module import, and
  `decode('kan_r3_h1_n4')` reads the model. `kan_iv` reaches `ia.py` through
  its own relative path, so two `PYTHONPATH` entries suffice.
- The recipe's comparison step passes on the archived results.
- No search was run.

Carried-forward round-2 items that sol-referee marked "partly" all map to
corrections 1 and 2:

- round-2 requests 4 and 5;
- sol-referee items 4 and 13;
- opus items M2, M5 and m13.

Two more were accepted as they stood. m3 (the introduction repeats the
abstract's counts) was accepted by the referee. m16 (upstream reporting) is an
author action; see opus-referee 9. B2 covers the placeholders, which are
expected.

## 4. sol-status.md

| Item | Verdict | Evidence |
|---|---|---|
| 1. EMFL enclosures labelled verified | **resolved** (component status) | Register row `I-reproduction.tex:219–221` now reads "verified (emfl enclosures: weaker second)", and the caption `:118` names the audit code as the first implementation. The S4 certificate box `E-audit.tex:452` says that the displayed enclosures rest on checker V2 alone. §7 `07-audit.tex:95`. `RUNS.md:397–416`. In `claims.json`, `register-23` has `status_by_component` = {emfl enclosures: weaker second} and label *proved*. In exact arithmetic, the audit implementation's wider enclosures (second lines of Table S24) and checker V1's prove every listed dual bound valid. They also prove all four shortfalls (≥1.41e-5, 1.98e-3, 2.92e-4, 6.86e-6) and the `emfl050_3_3` relative claims (≥1.166e-6 for the dual and ≥1.36e-6 for the primal). |
| 2. pricing050 scope and checker count | **resolved** (the "verified" branch); small artifact residual (R2) | §2.6 `02-semantics.tex:200`; §5.2 `05-other.tex:118`; §6.3 `06-points.tex:81`; S1.5 `B5-small.tex:359, 368`; S2 `C-points.tex:246`; Table S17 `tab-points-all.tex:29`; Table S37; register `I-reproduction.tex:171, 213`; `RUNS.md:189–207`; `claims.json` `register-11` *verified* and `register-21` "verified (etamac: proved)". I checked the provenance myself in session record `…/wf_59980c30-1d9/agent-a14f29dbb97bbc878.jsonl`. That session wrote `pricing_check.py` at 07:29:27Z. Before that it opened only the earlier dossier text and `v_pricing050.py`; it inspected the earlier check's log and code only at 07:29:46Z. The two checkers use different readers: `xml.etree` inline, and `r2/osil.py`, which "shares no code with osilx.py". |
| 3. ANN replay called separately written | **resolved** | `B9-ann-kan.tex:65–66` ("A replay driver written in a later agent session, using the first implementation's bounding routines …; The covering argument trusts this reconstruction"); trust base `:152`. The main text (`05-other.tex:292–296`) makes no such claim. The status stays *proved*. |
| 4. "Proved" comparisons resting on 50-digit evaluation | **resolved** (relabelling, an alternative the reviewer allowed) | S6.3 `H-solvers.tex:76–77`: point infeasibility now follows from the trace file's returned objective values, widened by half a unit. S6.4 `:99`: the `etamac` p1 point statement is computed. Captions `tab-claims.tex:10` and `tab-claims-campaign.tex:9–10`. In `claims.json`, `reported-08` is *computed*, the 15 campaign entries are *proved* through `returned_value`, and the 6 listed-point entries are evaluated exactly. I rechecked all 15 `returned_margin` values in exact arithmetic, and all hold. The generator checks all 35 returned values (`data/check.log`). |
| 5. Display check broader than its evidence | **resolved** | Register row `I-reproduction.tex:233–236`: "Generated certified displays", level \evid{stored}. S7.5 `J-displays.tex:9–12`. `RUNS.md:462–472`. `claims.json` `register-27`. |
| Submission action: the "separately written" definition | **author action** (open) | `development/build-final.md` §11 item 3. The per-family facts are now printed in Table S37. |
| Submission action: what the authors checked | **author action** (placeholder kept) | `11-conclusion.tex:63`; §2.6 `02-semantics.tex:186` unchanged. |

The coverage table rows that sol-status marked "consistent" were not changed
and remain consistent: R01–R10, R12–R17, R19, R20, R22, R24 and R26. The rows
it flagged (R11, R18, R21, R23, R25 and R27) are covered by findings 1–5. The
validator checks that every LaTeX register status matches `claims.json`; it
passes.

## 5. opus-referee.md

| Item | Verdict | Evidence |
|---|---|---|
| 1 (major). §8.2 restatement of Lemma S6.3 | **resolved** | `08-solvers.tex:106`; verified in Section 2 above. The reviewer's "still reaches" became "still contains", with the residual condition stated. |
| 2. Which families read the first code | **resolved** | `02-semantics.tex:191` ("in most families it also read the first implementation (see below)") and `:194` ("Table S37 names these families"). Table S37 has a new "read first" column (`tab-trust-full.tex:11`; generator `data/make_tables.py:1351`). Its entries match the G1 session-record check (`development/revise4-result.json`, `edits[0].rejected`): of the 15 families with a second implementation, 11 read first (powerflow0030p only for the format), 2 did not (lukvle10, etamac) and 2 were not checked (eg, KAN). hvycrash is "not checked"; ann is "read; order not recorded". The reviewer's "about nine" is now an exact, sourced list. |
| 3. Meaning of "we" | **resolved** | `02-semantics.tex:184`. |
| 4. §11 list of re-read proofs | **deviated-justified** | `11-conclusion.tex:33`. Checked against the supplement: chain and catmix (`B4-chain-catmix.tex:456–458`); the eg rounding analysis was read "in an earlier written form" (`F-eg-rounding.tex:414`), so the editors wrote that instead of "the eg rounding lemmas"; the eg primal check was "reran and read" (`C-points.tex:269`). The KAN exponential code (`B9:314`) is code, not a proof, so leaving it out is correct. "Extended-value proofs" is gone. |
| 5. camshape "gain is in rigor" | **resolved** | `05-other.tex:67`, merged with opus-writing 12. |
| 6. 1,632 vs 1,633 OSIL files | **resolved** | `08-solvers.tex:120`; `H-solvers.tex:324`; S3.4 `D-literature.tex:292`; S4.1 `E-audit.tex:16`. All now give one reason. I confirmed it: the archived `research-20260929/bound-audit/pages/fct.html` links `ams/`, `gms/`, `gdx/` and `sol/` files but no `osil/` file, whereas other pages do. |
| 7. Pointers that dropped hypotheses | **resolved** | `04-split.tex:86` (bag components interior and $F_t$ differentiable there) and `:118` (finite SP). These match Prop. S1.78 (`B10-split-extras.tex:13–16`) and S1.79 (`:32–34`). |
| 8 (optional). Length | **deviated-justified** | The lnts50 paragraph of §1 was deleted; its fact remains in Table S33 and §9.2 (`09-interpretation.tex:68`). The two §9.1 moves were not made, with the reason in `09-interpretation.tex:24–28`: "Other observations" carries the evidence against the interpretation. Sections 1–11 now take 41.49 pages (`build-final.md` §10); sol-referee accepted the length. |
| 9. Report the SCIP defect; MINLPLib | **author action**; disclosure **resolved** | The dated, uniform wording "As of 2026-10-05, we have not yet …" is at `07-audit.tex:109`, `08-solvers.tex:125`, `H-solvers.tex:341` and `artifact/README.md:57–58`. No "pending … at the time of writing" remains. The tracker search keeps its date (2026-10-02). |
| 10. "Round" vocabulary in the artifact | **resolved** | Definition at `README.md:17–20`, `RUNS.md:32–33` and `HISTORY.md:9–10`. The README prose was reworded ("reruns made during internal review", "run records that the supplement does not print"); no "of the revision" remains. |
| Submission condition: what a person checked | **author action** (placeholder kept, as instructed) | `11-conclusion.tex:63`, extended to name §11's limitations; `02-semantics.tex:186`. |

The section-1 status tables of opus-referee reported round-2 items, not new
requests. Items 2, 14 and 15 there map to items 8, 9 and 10 above.

## 6. opus-writing.md

| Item | Verdict | Evidence |
|---|---|---|
| 1 (major). Description of the 155 | **resolved** | `03-results.tex:51–54`; `11-conclusion.tex:39`; `D-literature.tex:285`. The new text agrees with S3.4 (`D:241–270`) and the funnel table. The 155 are nonconvex, listed as open, meet the width rule, and pass both gap conditions. 41 = 29 + 12; 114 = 155 − 41; 146 = 155 − 9. camshape100 and lnts50 are "among the 294 but not the 155", so they fail only the last condition. "Small heuristic upper bounds on treewidth" matches the width rule (≤ 16, or ≤ 6 with at least 50 nonlinear variables). No other passage uses "open by our selection rule" for the 155. Optional point: "gaps above $10^{-4}$" compresses "or infinite / no finite listed dual". ann_cumene_tanh, for example, has no listed dual bound. |
| 2 (major). §2.6 status definitions | **resolved** | `02-semantics.tex:205–206`, the reviewer's text. Now consistent with the evidence-level definition (`:170`, where \evid{hand} is a level), with the Table 1 caption (`tab-trust.tex:12–14`: proved = no separately written second implementation), with the register statuses and with `claims.json` (ann_cumene_tanh *proved*, hvycrash *proved*). |
| 3. C3 / §8 qualifier | **resolved** | `01-introduction.tex:98–100`; `08-solvers.tex:52`. |
| 4. "Auditor" undefined | **resolved** | Defined at `05-other.tex:268`; also `:275`, Table 1 (`tab-trust.tex:35`), Table 7 (`10-reproducibility.tex:77, 79, 81`), register `I-reproduction.tex:195`, `F-eg-rounding.tex:11, 280–282`. No unqualified "audited"/"auditor" remains in the main text; `07:15` keeps "26 audited" in the §7 sense. |
| 5. Observation 1; "split coordinates" | **resolved** | `01-introduction.tex:58–59`; `09-interpretation.tex:39`. Checked: Θ ⊂ R^112 and 9 leaves (`B5-small.tex:432, 507`); 12 + 15 = 27. |
| 6. Observation 3 | **resolved** | `01-introduction.tex:64–66`, the reviewer's text. |
| 7. C4 | **resolved** | `01-introduction.tex:105–107`. |
| 8. §1 wordings | **resolved** | "thus" removed (`:23`); `:53`; announcement removed; `:82` (ann_cumene_exp). |
| 9. Remark 2.3(1), 17 vs 21 | **resolved** | `02-semantics.tex:55`. |
| 10. "Data reading" in A.2 | **resolved** | `A-semantics.tex:36–47`. Optional: `:49` still says "the outward readings"; it is unambiguous there. |
| 11. Four §4 wordings | **resolved** | `04-split.tex:86, 207, 222, 304`. |
| 12. Five §5 wordings | **resolved**; one **deviated-justified** | `05-other.tex:67, 154, 169, 330`. At `:188`, "fixes the investments $I_1,\dots,I_8$ and the new inputs $LN_t$ and $EN_t$" is more specific than the reviewer's text and matches S1.5 (`B5-small.tex:307`). |
| 13. Prop. 8.1(a) | **resolved** | `08-solvers.tex:59–60`. |
| 14. 1,632 and "5 for $R$" | **resolved** | `08-solvers.tex:120, 163`; `D:292` and `E:16` now agree (checked; see opus-referee 6). |
| 15. §7.4/7.5 sentences | **resolved**; one in substance | `07-audit.tex:87–89, 92–94, 95–96`. At `:107` the repeated solved-mark clause is deleted, but the reviewer's "consistent only with" rewording was not adopted. The current "which only the unproved six-digit rounding explains" is accurate. |
| 16. §7 precision points | **resolved** | `07-audit.tex:27, 41, 71`. Optional: `:41` says "13,723 of the 13,847 … are consistent with this rule", while S4 (`E-audit.tex:164`) adds that 122 more differ only in the sign of zero. The count is a correct lower count, but it reads as if 124 values were inconsistent. |
| 17. §9 order and fonts | **resolved** | `09-interpretation.tex:32, 69–71`. |
| 18. §10 long sentence | **resolved** | `10-reproducibility.tex:56–57`. |
| 19. §11 term and human-check wording | **resolved** | `11-conclusion.tex:33`, merged with opus-referee 4; it now uses the §2.6 wording. |
| 20. Table 3 caption | **resolved** | `data/make_tables.py:642` → `tab-unclosed.tex:11`; matches S1.8 (`B8-waterno2.tex:257`). |
| 21. "same-model", "duals" | **resolved** | `00-abstract.tex:17` was reworded with sol-referee 1 rather than with the reviewer's text: 250 words by the established rule (`/tmp/abscount.sh`). Figure 1 caption `03-results.tex:32`. No "same-model" remains in any source; "duals" remains only in table cells and the Figure 1 legend. |
| 22. Other names for \evid{hand} | **resolved** | Table 1 hvycrash row (`make_tables.py:1329`); `10-reproducibility.tex:48`; `J-displays.tex:11`. No "on paper" or "hand-written" remains. |

The writing review's round-2 table had residuals at its items 4, 8, 17 and 30.
They map to items 6, 3, 11 and 10 above, all resolved.

## 7. New inconsistencies and remaining problems

I looked for inconsistencies that the round-3 edits could have introduced:

- other "one implementation" or "separately written replay" wording;
- status cells in the PDFs, register, JSON and RUNS;
- the numbers file;
- the new returned-value margins;
- §2.6 against Table 1;
- the emfl verdicts against the wider enclosures;
- the read-first column against the session records.

No certified value, count or status conflicts. Rendered pages checked: main
p. 42 (Table 7 and §11) and supplement pp. 119–120 (sideways Table S37 with the
new column, and the register). Both logs report 0 overfull boxes and no
undefined references.

Remaining problems, all minor:

- **R1 (artifact; sol-referee 1).** The 15 campaign entries of `claims.json` and
  the paragraph at `artifact/README.md:94–101` state, as *proved* and without a
  qualifier, that the returned point "is not exactly feasible".
  - For the entries on sample-only instances, this relies on the assumed GAMS/OSIL
    correspondence. They are `reported-20` to `-25` (etamac, pricing050,
    pindyck, chain50) and `-27`, `-28` (KAN). Their `trust_qualifiers` are
    empty.
  - The paper states the assumption (`H-solvers.tex:71`), and the
    `tab-claims-campaign` caption points there.
  - Fix: add a qualifier such as "assumes the GAMS and OSIL forms agree (sampled
    only)" in `build_claims.py` for these instances, or one sentence in
    `README.md:94–101`.
- **R2 (artifact; sol-status 2).** `RUNS.md:203` and `claims.json` `register-11`
  (`expected_output`) say that `v_pricing050.py` prints "the upper bound and the
  exact primal value as in `tab:closures`".
  - That script prints its own 25-digit point, with objective
    −1813.8290784519730578 (`…/wave2-small-verification/logs/pricing050.log`:5).
    This is not $U=-1813.8290784519730769$ of the saved point.
  - This is the conflation that sol-status warned about. The line predates
    round 3.
  - Fix: "the upper bound; the exact primal value of `tab:closures` comes from the
    two primal checkers named above".
- **R3 (wording; sol-referee 1).** `01-introduction.tex:102`: "The runs check the
  status of current solvers on the stored models" predates round 3. The runs used
  the GAMS files, and "stored model" means the OSIL file (Definition 2.1).
  "on these instances" would remove the clash with the sentence before it.
- **Optional precision points.** These are not errors:
  - `08-solvers.tex:106`: add "in absolute value";
  - `07-audit.tex:41`: mention the 122 sign-of-zero displays;
  - `03-results.tex:51`: "above $10^{-4}$ or infinite";
  - `A-semantics.tex:49`: "outward data readings";
  - `02-semantics.tex:196`: this sentence predates round 3. It lists pricing050
    among the families whose two implementations share one OSIL reader, although
    the third code that reproduces the displayed bound has its own reader,
    `r2/osil.py`. The statement is conservative, not false.
- **Author actions (open as instructed).**
  - The `[TODO: …]` and `[archive DOI]` placeholders, including what the authors
    checked themselves.
  - The decision on the definition of "separately written".
  - The SCIP report and the message to the MINLPLib maintainer. If either is sent,
    update `07:109`, `08:125`, `H:341` and the README, revalidate the index and
    rebuild.
  - The guarded `r5` replays and the full S7.1 recipe were not rerun on the final
    sources, as `RELEASE.md` states.

## 8. Commands run for this check

All checks were targeted and local, on at most two cores; the working files are
in `/tmp/verify-r3/`. I did not run `make`, the generators, the short checks or
any scientific script in place. I edited nothing except this file, made no
commit and consulted no CI result.

```bash
sha256sum build/main.pdf build/supplement.pdf; grep SHA artifact/RELEASE.md   # equal
find . -newer build/main.pdf -type f -not -path './build/*' -not -path './development/*'
pdfinfo build/{main,supplement}.pdf; pdftotext [-layout] build/{main,supplement}.pdf /tmp/verify-r3/...
diff -ru /tmp/suppgrp-orig/{sections,tables,data,artifact} <current>          # round-3 diffs
python3 /tmp/verify-r3/cube.py                                                 # Section 2, exact Fractions
cp artifact/check_claims.py /tmp/verify-r3/claims/ && cd /tmp && taskset -c 0,1 \
  python3 /tmp/verify-r3/claims/check_claims.py --repo-root <repo>
#   PASS: 65 claims; 5632 SHA-256 references; 1918 distinct files; ... valid
awk ... README.md > kan-block.sh; bash -n kan-block.sh; diff with RUNS.md block; compile() of embedded Python
# staged copy /tmp/verify-r3/kanwork (copies of the module subtrees, guarded code, KAN OSIL files):
#   import kan_decode, kan_iv and the guarded module; decode('kan_r3_h1_n4'); comparison step on archived results
python3 (inline): emfl verdicts from both enclosures; 15 returned-value margins; numbers.json old/new diff;
                  claims.json status fields; session-record tool calls (read-only)
bash /tmp/abscount.sh sections/00-abstract.tex                                 # 250
grep -a -c Overfull build/main.log build/supplement.log                        # 0, 0
pdftoppm -r 60/70 (main p. 42; supplement pp. 119-120), inspected by eye
```
