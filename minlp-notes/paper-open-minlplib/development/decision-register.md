# Decision register for the paper (open MINLPLib instances)

Date: 2026-10-04. R = `research-20260929/`. D = `paper-open-minlplib/development/dossiers/`.

This register consolidates every issue, critic correction and critic
additional issue from the 13 dossiers (`D/<key>.md`), their critiques
(`D/<key>.critique.md`) and `dossier-results.json`. Where a dossier and its
critic disagree, the adjudication and its evidence are in Section 3. Each item
has a final resolution for the paper. Nothing listed here invalidates a
claimed bound, point or gap.

Categories: **NUM** number or display change; **WORD** wording or framing;
**PROOF** proof or lemma to include; **COMP** computation; **DOC**
documentation or reproducibility; **OOS** out of scope or a user decision.

Source IDs are the dossier issue IDs (for example `DO-4`), critic corrections
(`C3` = correction 3 of that family's critique) and critic additional issues
(`A2`, `crit-M1`, `PFC-1`, `CR-A4`, `X3`, ...).

Contents:
1. Lead-author decisions already taken
2. Paper-wide conventions that follow from the items
3. Adjudications (dossier vs critic, and cross-family conflicts)
4. Register by family (13 families)
5. Numbers the paper displays differently from `R/open-instances-summary.md`
6. Proposed computations: cost and recommendation
7. Cheap checks run for this register
8. Decisions still open for the lead author or the user

---

## 1. Lead-author decisions already taken

| ID | decision | items it resolves |
|---|---|---|
| L1 | Adopt the lnts exact-optimum theorem (optimum = N·h*, attained). Independent review later. | LL-01, LL-15, PP-11 |
| L2 | Adopt the dtoc5 exact-rational dual certificate (gap 7.2e-43). Independent review later. | DO-01, DO-02 |
| L3 | Adopt the KAN rigorous-exp rerun (`D/ann-kan-checks/`). Independent review later. | AK-01, AK-12 |
| L4 | eg: Lemma A1 becomes a proved appendix lemma. A2 and the pow hypothesis are removed by an exp- and pow-audited rerun of the independent certifier (route R) on all leaves of all three instances (in preparation). | EG-01 to EG-05 |
| L5 | waterno2_18/24: document that regeneration with `certify.py` gives slightly different valid bounds; no rerun. | WN-01 |
| L6 | No lukvle10 refinement; state mpmath iv as part of the trust base. | LL-06, LL-07 |
| L7 | Exact-semantics language: solver claims that our exact results contradict are "not attainable under exact feasibility (tolerance artifacts)" unless a genuine error is proved. Credit tolerance-level closures (BARON camshape100/200 in our campaign, Octeract, SCIP 8.1 on eg_int_s). | G-02, CS-08, CS-10, SV-01, SV-03, SV-10 |

Requirements this register adds to L4 (from eg `C1`, `C11`, `eg-7`):
- Audit every `np.exp` value and every integer power (`tau**3`, `p**3`, `p**4`;
  `np.power` reaches SVML `__svml_pow8_ha`) used by `indep_cert.py` against a
  rigorous enclosure. The audit tolerance must be the one that Lemma A1
  actually uses (1e-14 per exp value as padded; 9.9e-14 only if Proposition
  A2′ is included). Integer powers can be audited against exact products.
- For independence, the exp auditor should not be the authors' `fexp` or
  `kan_iv` (their relative widths are 9.0e-15 and 3.45e-13; r1's interval exp is
  4.9e-13, too wide). Write a fresh outward-rounded Cody–Waite auditor with
  exact m·L1 and rationally checked constants, or state the coupling to the
  authors' code explicitly.
- Regenerate the deleted recordings `rec_int.npz` and `rec_disc_p*.npz`
  (`record_run.py`, about 1,650 s) and rerun `verify_tree.py` coverage and
  r1's `own_cover.py` for eg_int_s and eg_disc_s.
- Run from `/tmp` copies; check that the decisions (and `res/`) are
  bit-identical to the unaudited run.
- Keep (H0) (IEEE binary64, round to nearest, gradual underflow) as the stated
  hypothesis. The decimal data are converted with relative error ≤ u; Lemma
  A1's fact F1 covers this.

---

## 2. Paper-wide conventions that follow from the items

| ID | convention | sources |
|---|---|---|
| G-01 | **Model definition.** Every certificate is for the stored MINLPLib model with each decimal string read as the exact rational it denotes (reading (b)). The OSiL schema types numbers as `xs:double`, solvers and GAMS use binary64 data, and some OSIL strings are printed binary64 products (catmix `0.045000000000000005`). State this as the model definition, with OSiL defaults, a domain rule (denominators nonzero, `ln`/power bases positive, `sqrt` arguments nonnegative) and a footnote on `xs:double`. Cite exact-MIP practice (Cook et al. 2011; Eifler et al. 2023; Hoen–Gleixner 2025). Claim nothing for binary64 data, except that the lnts and lukvle10 primal points are feasible under both readings. Zero gaps, gaps below 1e-16 relative, the hvycrash constant −0.2185 and the camshape optima are reading-(b) statements. | PP-1, PP `C2`, `C3`, `C13`, `CR-A2`, `CR-A4`; W7; audit `CRIT-A2`; solvers S2 |
| G-02 | **Exact-semantics language (L7).** Use three classes. (A) *Not attainable under exact feasibility; tolerance artifact*: BARON camshape100/200 (valid duals, tolerance-level closures), ANTIGONE QPLIB_2738, MINOTAUR QPLIB_3177, SCIP's KAN values (relative to R), QPLIB reference points 2703/3177, MINLPLib camshape400/800 p2, hvycrash p1/p2, lnts50 p1, emfl listed primal values. (B) *Invalid bound or claim, proved*: the audit's 19 listed bounds (11 gross, 8 tolerance-scale; say which), LINDO rocket100/200/400 (tolerance scale), CAMINO's recorded Gurobi 13.0.0 best bounds (cause unknown), MINOTAUR's infeasibility claim on QPLIB_8803 (assumes .nl = .gms), SCIP's wrong optimal values (waterno2 subproblems, fm336, tiny2). (C) *Display rounding only*: listed displays below our duals only through rounding (lnts100, lnts400, lukvle10, chain50/100/200). Base every artifact claim on an evaluated objective, never on a page display. | camshape `C1`, `crit-M1`; solvers S1, S2, `C9`, S10, S11; PP-5, PP `C5`, `C11` |
| G-03 | **Display rules.** Duals rounded toward the safe side, primal values toward the other side, gaps upward ("rounded in the conservative direction" covers maximization). When the displays cannot reproduce the gap cell, either lengthen the displays or footnote that the gap uses certificate ends. Never quote numbers from older reports; take them from the summary, `R/publication/integration/gap-values.json`, or Section 5 of this register. | LL-09, DO-07, small `C2`, PP `C11`, PT-5 |
| G-04 | **"Open."** "Listed as open" = no S mark. The S mark requires at least 3 solvers claiming global optimality within relative gap 1e-6, or infeasibility (documentation snapshot `vigerske2026-minlplib-documentation-database-snapshot-2026`). The scout's "open" = best single-solver relative gap > 1e-4 on a filtered set. Define both. Avoid "solved on MINLPLib"; write "closed to a certified gap". | PT-1, PF-11, chain-catmix `C7` |
| G-05 | **"Listed dual."** MINLPLib's instance-list dual equals, on all 1,576 pages that list one, the third-best per-solver entry when infeasibility claims (`inf`) are counted, to display rounding. With finite entries only, 1,564 of the 1,568 numeric listings match; the four exceptions are ball_mk4_15, chp_shorttermplan2c, nuclear10a and powerflow0057r. Eight listings are `inf`. The 57 pages with fewer than three entries list no dual. This is an observation consistent with the documentation ("the 1st, 2nd, and 3rd best bound are in bold"), not a documented rule. Tables show the best per-solver bound and say so. | audit `C1`, AUD-13; PT `C4`, X6; chain-catmix `C6`; eg `C4`; check K1 (Section 7) |
| G-06 | **Trust base.** State per instance which libraries and hypotheses each proof uses (IEEE binary64 (H0), mpmath iv, Fraction/integers, hand-checked padding lemmas). mpmath iv remains in the trust base for: the lukvle10 dual (both certificates; L6); the chain dual B&B (both implementations); the ex6_2_*, etamac and pricing050 dual codes (`gibbs_bb.py`, `v_etamac.py`, `v_pricing050.py`); the constant κ in the pindyck review code; and the primal enclosures of hvycrash, etamac, pricing050 and pindyck. The optcdeg2 primal now also has an integer-interval proof. Never write "assumes mpmath" where an exact re-proof exists (lnts, lukvle10, dtoc5, chain, powerflow, water, ANN, KAN, ex6_2_*). | PP-3, PP `C9`, `C10`; I3; CC-3; DO-2; PT `C18` |
| G-07 | **Novelty.** Do not claim the first MINLPLib bound audit (Vigerske's MINLPLib 2 work), the first certified MINLPLib instances (Halbig et al.), the first findings of wrong solver bounds (Neumaier et al. 2005; Nowak 2008 on BARON; Vigerske 2017 on SCIP), or new mechanisms. Use "to the best of our knowledge" and "new as far as found" with the search scope. Make no priority claim for period decomposition (Ghaddar et al. 2015 unread) or for the ex6_2_* optima (McDonald–Floudas unconfirmed). | AUD-2, audit `CRIT-A1`; CC-13; W10; small-gibbs-prior-work-unread; PF-10; AK `C2` |
| G-08 | **Stale R documents.** `R/SYNTHESIS.md`, `R/closing-research-results.md`, `R/publication/reproduction/README.md`, the open-instances report, the wave reports and some review reports contain superseded or unsafe numbers. The paper does not quote them. Corrections there are for the document owners (R/ is not edited here). | LL-09, DO-07, PF-2, PP-4, PT-5, S20, eg-8, W5 |
| G-09 | **Independence statements.** Say who wrote and who checked each code, and name shared components (osilx reader, kan_iv/ia, mpmath iv). Distinguish "reproduced by a separate implementation in this project (AI agent)" from a human review. | camshape `crit-A2`; AK `A1`, `C3`; W2; solvers `A4` |

---

## 3. Adjudications

Each row records a disagreement, the evidence read or computed, and the
decision. "Critic" means the family's critique.

| # | family | dossier position | critic or other position | evidence | decision |
|---|---|---|---|---|---|
| J-01 | lnts-lukvle10 | lukvle10 partial-Lagrangian dual value equals f(x*) "to about 1e-19" (L8) | not supported; dual value known only within 1.42e-9 | `v_lukvle10_bnb.py` line 199: `U = hi(prob.point(x0[0], x0[1]))` (incumbent initialized at the p5 pair; checked here) | Critic. Use its sentence (LL-05). |
| J-02 | lnts-lukvle10 | primal points agree with Theorem 3 to 7e-26 (L2) | 7e-26 is the display width; the 60-digit h enclosures agree to ≤ 3.5e-58 | critic `misc_checks.log` | Critic (LL-01). |
| J-03 | lnts-lukvle10 | the L4 excess comes from `lnts_bound.py` | it comes from the verification-report displays and the open-instances decimals | `minor-fixes-review-r2.md:97`; critic exact check | Critic (LL-09). |
| J-04 | lnts-lukvle10 / primal-points | lnts400 p1 comparison open (critic additional issue) | done by PP-5 | `D/primal-points-checks/logs/lnts_p1_check.log` (files fetched, hashes logged); against the Theorem 3 optimum: lnts50 −4.30e-11, lnts100 +1.49e-12, lnts200 +2.72e-12, lnts400 +1.49e-11 (computed here) | Resolved: only lnts50 p1 lies below the optimum (LL-04). |
| J-05 | dtoc5-optcdeg2 | DO-1 major | minor: the display is already verified and reproducible in 18 s | `reproduction/README.md:99`; critic two-route recomputation | Minor. L2 adopts the exact certificate anyway (DO-01). |
| J-06 | dtoc5-optcdeg2 | uniqueness of the dtoc5 minimizer needs an exact KKT pair | provable from the localization (radius ≈ 4e-19) and strict convexity of the reduced objective | critic `C6`, `A2` (reduced Hessian argument) | Critic. Include the paragraph; review with DO-01 (DO-02). |
| J-07 | dtoc5-optcdeg2 | all optcdeg2 stage losses except stage 3091 are below 1e-24 | stage 47290 loses 4.08e-20 | critic exact all-stage recomputation (23 s) | Critic (DO-12). |
| J-08 | camshape | MINOTAUR camshape800 refutation "upgraded to a proof"; fetch QPLIB_3177.nl | only non-attainability is shown; MINOTAUR's dual is consistent; ε ≈ 9.7e-9 points reach its value (ANTIGONE needs 2.9e-8); no fetch | `D/camshape-critique-checks/minotaur_eps.log`, `antigone_eps.log`; solvers §3.4 | Critic, consistent with L7 (CS-08). |
| J-09 | camshape / solvers / primal-points / summary | "chain amplifies violations up to about 600-fold" (summary); "about 0.6 n²ε worst case" (camshape I3); "Chebyshev weights add up" (S5); multiplier mass (PP-10) | D_n(ε) is a proved upper bound, not the worst case; explicit points reach 87% | camshape `tol_check.log`; critic `tol_attain.log`; solvers `C/r2/tol.log` and the critic's third implementation | One sentence for all (CS-05). |
| J-10 | chain-catmix | optional rerun of the authors' catmix code on the recheck grids (CC-2) | would not certify the stated doubles (1e-14 incumbent tolerance; losses add over N+1 stages) | critic `C5`, `A2`; per-ray deficits up to 9.44e-15 | Critic. No rerun; scoped wording (CC-02). |
| J-11 | chain-catmix | Proposition C6 consequence over all of Ω_N | proved only for strict chord; the boundary needs one line | critic `C1` (50-digit tests N = 3, 7, 50) | Critic (CC-01). |
| J-12 | chain-catmix critic vs pattern-theory critic vs audit critic | chain-catmix critic: listing dual = third-best on "all 1,576 pages with at least three finite duals"; "34" pages without a listing. Pattern critic: 1,564 + 4. Audit critic: .solu rule 589/589 with `inf` counted. | — | check K1 (Section 7): 1,576 pages list a dual = exactly the pages with ≥ 3 entries *including* `inf`; 1,571 pages have ≥ 3 finite entries; 57 pages (not 34) have fewer than 3 entries; all 1,576 match the third-best entry counting `inf`; finite-only 1,564/1,568 | Pattern and audit critics are right; the chain-catmix critic's two counts are imprecise. Use G-05. |
| J-13 | small | pricing050 gap ≤ 2.0e-17 (dossier v1) | 1.915e-14 | `small-checks/pricing_check.log`; `r2/pricing_check.log` | Dossier r2 already corrected; adopt 1.92e-14 (SM-01). |
| J-14 | small | pindyck trust base "only mpmath iv and Fraction" | the review's affine arithmetic uses binary64 with `nextafter`; the displayed dual is the authors' value (γ_n padding), also certified by the review's code | `own_psi.py`; `final_bound.py` | Critic (SM-12). |
| J-15 | eg | S-F is libm-free; Lemma A1 removes A1; option (f) needs only (H0) + Lemma A1 | integer powers go through SVML `__svml_pow8_ha` in S-F and route R | `egfast.py:259`; `indep_cert.py:163,193,194`; critic `libpaths.log`, `powtest.log` | Critic. L4 removes the pow dependency by auditing it (EG-01). |
| J-16 | eg | audit route R with `fexp` | `fexp` is the authors' code; independence needs a fresh auditor or a stated coupling | critic `C11`, `r1exp.log` | Critic (requirements under L4). |
| J-17 | powerflow | inexact multipliers "split" the double zero eigenvalue | eigenvalues stay exactly double (Proposition 6) | critic `eigpair.log`, `jcheck.log` | Critic (PF-15). |
| J-18 | powerflow | angle-free 0039p variant needs an independent replay (1–3 CPU-min) | replayed with the reviewer's independent code in 9 s | critic `noangle_0039p.log` | Done (PF-03). |
| J-19 | waterno2 | B&B deterministic, "replayed bit for bit" | `certify.py` re-derives targets from time-limited SCIP runs; regeneration gives 4790.820086219 (18) and 6576.150434342 (24) | `R/publication/reproduction/water-audit/logs/w18_certify.log`, `w24_certify.log` | Critic; L5 (WN-01). |
| J-20 | waterno2 | replay costs 25–60 CPU-h (20-task speed-up 2.4×) | 2.79× on 1,564 tasks; about 20–30 CPU-h unloaded | critic `replay_audit.log` | Critic (WN-02). |
| J-21 | ann-kan | prior RS formulation has "the same five variables and one inequality" as R | R has 723 inequalities; x647 ≥ −1 is active | arXiv v2 p. 21; dissertation §2.4.4 | Critic (AK-17). |
| J-22 | ann-kan | the two KAN paths are independent ("either code correct") | after the rerun, both use `kan_iv.iexp_pt_fast` and `ia.NI` | `kan_bnb_rigexp.diff` | Critic; disclose (AK-01). |
| J-23 | ann-kan | "same incumbent point in all six runs" | false for kan_r3_h1_n4/n5 (different points, same UB) | wave-3 and rerun JSON logs | Critic (AK-18). |
| J-24 | primal-points | "every primal and dual proof reads decimals exactly" | checked only for chain, dtoc5, optcdeg2 and wave-2-small duals | — | Critic; this register adds a grep-level check of camshape, pindyck, catmix, powerflow, waterno2, ANN, KAN and eg (check K6); the final review should confirm (PP-01). |
| J-25 | primal-points | "five claims rest on a single mpmath-iv implementation" | hvycrash and pindyck have two (both mpmath); etamac, pricing050, optcdeg2 single | — | Critic, updated: the optcdeg2 primal now has the mpmath-free integer-interval proof (DO-2), so four claims rest on mpmath iv (PP-03). |
| J-26 | primal-points | Kearfott (1998) not in the knowledge base | it is, and it is the antecedent of method C2 | `literature/papers/kearfott1998-on-proving-existence-of-feasible/` | Critic (PP-13). |
| J-27 | audit | MINLPLib's aggregate dual is never beaten beyond display rounding in this family | false for eniplac (0.083) and stockcycle (0.31) unless six-digit pre-storage rounding is assumed | `D/checks/audit-r2/agg.log` | Critic (AU-13). |
| J-28 | audit | the four .solu exceptions have no listed point | each has one `inf` entry; with `inf` counted 589/589 match | critic `/tmp/audcrit` script; consistent with K1 | Critic (AU-13). |
| J-29 | audit | Lemma 1(b) as stated | fails for binary64 artefact strings (|d| ≥ 2^26); none of the 22 refuted bounds is affected | critic `C3` | Critic (AU-10). |
| J-30 | solvers | QPLIB_2738 point lies 5.8e-14 *above* the bound | it lies 5.8e-14 *below*; row violations ≤ 2e-14 (printing level) explain it | −4.284146267804670 < −4.284146267804612 (trivial) | Critic (SV-03). |
| J-31 | solvers | 12 rows per waterno2 period are binary64-inconsistent triggers | only the 0.7-station cube row has a binary64 enclosure that misses the bound | check K3 (Section 7) reproduces this: only up(fl(0.7)³) = 0.34299999999999997 < fl(0.343) | Critic (SV-17). |
| J-32 | solvers | S16 (30 flags need evaluated vectors); S15 (one rbb run decides) | S16 misdiagnosed; S15 target lies between the claims | critic `C6`, `C7` | Critic; both items closed without computation (SV-14, SV-15). |
| J-33 | solvers | camshape200 "already solved in floating point (Octeract; BARON 26.5.27)" | Octeract's entry concerns the rounded copy QPLIB_2480 (optimum ≥ 2.3e-6 relative away); BARON is our campaign, not prior work | solvers Prop. 15(5) | Critic (CS-10, SV-01). |
| J-34 | solvers | S18: optional SCIP 10.1.0 runs on waterno2_03/04 | cannot answer the question (listed SCIP duals dated 2022) | `pages.json` dates | Critic; drop (SV-17). |
| J-35 | solvers | Prop. 9(b): SCIP output self-inconsistent "independent of any data semantics" | holds in SCIP's eps semantics; under zero-tolerance binary64 the fm336 dual is valid | Prop. 9(c) (2.247 > 1.505) | Critic's three readings (SV-02). |
| J-36 | pattern-theory | chain census width N+1 | census value is 2N+1 | `census_merged.json` (101 for chain50; the dossier's own log) | Critic (PT-07). |
| J-37 | pattern-theory | pinch regularity needs Γ semiconvex | Γ semiconcave (counterexample Γ = |s|) | critic `C2` | Critic (PT-14). |
| J-38 | pattern-theory | confirmation pass ≈ one reviewer-hour | 2–4 h; two errors survived the dossier's re-derivation | critic `C17`, `ext_checks.py` | Critic (PT-06). |
| J-39 | solvers vs chain-catmix | "catmix certificates were not rerun on the .gms form" (S19/A6) | Proposition M8 (read by the critic) proves the dual transport to c = 9a | chain-catmix `A1` | Use M8 (CC-01, SV-18). |

---

## 4. Register by family

### 4.1 lnts-lukvle10 (LL)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| LL-01 | lnts-exact-optimum; `C4`, `C5`, `C6`, `C14`; lnts-thm3-second-implementation | Proposition 2 at margin 1e-12 leaves gaps of 5.8e-13 to 6.1e-13; Theorem 3 proves the optimum is N·h*, attained by the discrete linear-tangent control. | PROOF, NUM | Adopt (L1). State Theorem 3 with proof; keep Proposition 2 as a remark. Credit the earlier zero-gap observation (`R/theory-coupling/coupling.md` §7.2; `consistency-relaxations.md` §5.1). Present as new: the attaining control with μ* = −ν*N/2, the scalar equation g(ν) = 0 and the rigorous enclosure. Report the agreement with the independently proved primal points (60-digit h enclosures; deviation ≤ 3.5e-58), not the 7e-26 figure. Write \|g\| at the bracket ends as 8e-59 to 4e-56. Width < 1e-60 refers to the rational enclosure (print ≥ 62 digits or say so). Two implementations exist (dossier integer check; critic `thm3_iv.py`). Displays: N-01 to N-04. |
| LL-02 | lukvle10-verifier-display | The verification report's 352.2380254050785 exceeds the certified lower end by 4.4e-14. | NUM | Use 352.2380254050784 only; if the report is cited, say its display is nearest-rounded. |
| LL-03 | lukvle10-primal-display; `C10` | The summary primal 352.2380254064961 is the verifier's nearest display of p5's evaluated objective, not f(x*). | NUM | Display 352.2380254064957 and gap ≤ 1.42e-9 (4.03e-12 relative) (N-06). |
| LL-04 | lnts50-p1-below-dual; lnts400-p1-check; PP-5; PP `C5`, `C16` | lnts50 p1 (violation 9.1e-10) lies below the certified dual. | WORD | Add to the tolerance-artifact table: lnts50 p1 lies 4.30e-11 below the optimum. lnts100/200/400 p1 lie above it (J-04). Credit the verification report (line 122) for the p1 evaluation. |
| LL-05 | lukvle10-duality-gap-wording; `C1` | KKT agreement wording overclaims. | WORD | "The remaining gap, at most 1.42e-9, equals the summed branch-and-bound tolerances. The B&B incumbents never fell below the Lagrangian values at the KKT pairs, and floating-point multistart searches found no lower point. The dual value is known only to within 1.42e-9 of f(x*), and global optimality of x* is not proved." |
| LL-06 | lukvle10-refinement-optional; `C13` | Krawczyk + exclusion refinement could remove the gap. | OOS | Not done (L6). If the second-order loss is mentioned, base it on the 2.04e-14 deviation from the KKT multipliers. |
| LL-07 | lukvle10-mpmath-dependency; `C12` | Both lukvle10 dual certificates use mpmath iv exp/log; leaves not saved. | DOC | State "mpmath 1.3.0 iv encloses exp, log and arithmetic correctly" as a trust assumption (L6). If leaves are mentioned: about 1.65e5, not 3e5. |
| LL-08 | lukvle10-hidden-hypotheses; `C7`; lemma5-inf-not-min | Unstated hypotheses in the box reduction. | PROOF | State Lemma 5 with the sign-free bound inf ψ ≥ min(−\|q\|−\|β\|, −β²/(4(1+q))), hypothesis q > −1, and q_k ∈ [−0.8156, 0] (q_0 = q_995 = 0); write "inf ψ". |
| LL-09 | stale-numbers-in-older-documents; `C8` | Older documents show superseded or unsafe lnts/lukvle10 values. | DOC | G-08. The excess belongs to the verification-report displays and the open-instances report decimals, not `lnts_bound.py`. |
| LL-10 | unverified-352.152-estimate | The full-Lagrangian estimate 352.152 is unverified. | WORD | Omit, or label it (and "the 0.086 gap sits in pairs 497–498") as floating-point estimates. |
| LL-11 | `C2` | "Within 3.8e-5" is rounded down. | NUM | 3.9e-5 (the summary already uses it). |
| LL-12 | `C3` | Göß arXiv paper is in literature/. | WORD | Cite `go2026-clash-of-minlp-relaxations-piecewise`, p. 32. |
| LL-13 | `C9` | COPS agreement holds only under truncation. | WORD | "agree after truncation to six digits". |
| LL-14 | `C11` | p5 residual difference "unexplained". | WORD | "consistent with the 15-digit rounding of the .sol text". |
| LL-15 | summary text | The summary explains lnts gaps via the verifier's N·h2 (5.55e-13). | WORD | Replace with Theorem 3: gap 0, optimum attained. |

### 4.2 dtoc5-optcdeg2 (DO)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| DO-01 | DO-1; `A4` | The dtoc5 display rested on unsaved multipliers; an exact-rational certificate now gives d ≥ 5.389672119181140467423966499136271868831312689…, gap 7.205e-43. | NUM, DOC | Adopt (L2); minor severity (J-05). Displays N-05. Ship `dtoc5_checks.py` and its log (2.6 s replay from the committed exact point). The first verifier's mpmath value agrees to 1.8e-24 (second evaluation). |
| DO-02 | `C6`; `A2` | Uniqueness of the dtoc5 minimizer. | PROOF | Include the one-paragraph proof (reduced Hessian positive definite where 1 + 8u_t > 0; all minimizers within ≈ 4e-19 of x̂, where u_t ≥ −4e-14) and claim uniqueness. Delete "requires an exact KKT pair". Review together with DO-01. |
| DO-03 | DO-10; `C16` | Zero-gap and SDP-tightness wording. | WORD | "The Lagrangian duality gap is at most 7.3e-43"; "the Lagrangian and order-1 SDP relaxations are tight to within 7.3e-43 (proved)"; give interval endpoints. The explanation of solver failure is interpretation. |
| DO-04 | DO-2; `C1` | optcdeg2 primal relied on mpmath iv; the "± 5e-64" objective display is wrong. | PROOF, NUM | Cite the integer-interval proof `optcdeg2_primal_int.py` as primary (mpmath-free) and the reviewer's mpmath proof as second. Objective J = 293.876075095875093277214211424708015934099559491047 (width 4.7e-64). The summary's ≤ 293.87607509587509328 is unaffected. |
| DO-05 | DO-3; `A5` | Regeneration may give a different (valid) optcdeg2 bound; replay scripts overwrite logs. | DOC | Exact replay = `v_states.py` + `v_qcal_exact.py` on the committed npz (sha256 08311d33…) and the stage_lb file, run on copies; regeneration optional. |
| DO-06 | DO-4 | One exact implementation of the optcdeg2 stage minimization. | WORD, COMP | No second implementation (C-07: skip). Cite the authors' independent interval bound 293.8760750958728, the critic's 197-stage falsification search and the exact all-stage loss recomputation (all ≥ 0, sum 8.978e-16) as supporting evidence. |
| DO-07 | DO-5 | Superseded numbers in older documents. | DOC | G-08; older certificates only in a progression table. |
| DO-08 | DO-6 | Mechanism labels. | WORD | dtoc5: "zero Lagrangian duality gap at the discrete costate (Mangasarian-type sufficiency)". optcdeg2: "quadratic Krotov-type verification function"; no Mangasarian label. State λ_t = −2u_t, p_{t+1} = −λ_t. Update the summary's mechanism cells. |
| DO-09 | DO-7 | Imprecise model statements in notes. | WORD | Use the exact model statements of dossier §1. |
| DO-10 | DO-8; PT-13; `X3` | Bang-bang theory is not needed and partly conditional. | WORD | Certificate section self-contained (Lemmas 2–4, Theorem 2). Any theory in its own section with all hypotheses; screenings labelled floating-point; cite calibration note Proposition 4.1 for why affine splits fail. |
| DO-11 | DO-9; `C7`, `C8`, `C9`, `C10` | Citations. | WORD | Lincoln–Rantzer = `lincoln2006-relaxing-dynamic-programming`; Krotov 1967 and Mangasarian 1966 are now in the KB; verify only the still-absent references. Waki et al.: preprint B-411 page numbers, caveats (SeDuMi, random perturbation, possibly added bounds). DTOC5.SIF SOLUTION lines: "tolerance artifacts or a different model version" (floating-point evidence). |
| DO-12 | DO-11; `C3`; `A1` | optcdeg2 gap 9e-16 sits at stage 3091; stage 47290 also loses 4.1e-20. | WORD, COMP | No polishing (C-08: skip). Write "below 1e-24 except stages 3091 (9.0e-16) and 47290 (4.1e-20)". The same wrong sentence is in `R/reviews/bangbang-verification/verification-report.md` A.5 (owner). |
| DO-13 | `C2` | Dossier Table 10.4 shows 293.87607509587509238 (rounded up). | NUM | If 20 digits are shown, use 293.87607509587509237. The summary display 293.87607509587509 stays. |
| DO-14 | `C4` | The diagnostic trajectory is called exactly feasible. | WORD | "a 2^-300-rounded, near-feasible version of the certified trajectory". |
| DO-15 | `C5` | dtoc5 vs QPLIB_8585 "textually identical". | WORD | "identical apart from comment lines, `tolproj` formatting and the solve statement". |
| DO-16 | `C11` | Lemma 4 "=" and Theorem 2 notation. | PROOF | m_t ≥ min(…), equality for the exact set; B = ⌊m_0⌋ + Σ⌊m̃_t⌋ + ⌊m_N⌋; "rigorous evaluation of the certificate". |
| DO-17 | `C12`; `A3` | "Optimal control is bang-bang" describes only the certified point. | WORD | "on the certified (near-optimal) trajectory". Optional A3 proof that every global minimizer is bang-bang to 5.2e-9 on the middle arc (C-09: optional). |
| DO-18 | `C13`, `C14`, `C15` | Smaller wording. | WORD | The exactly feasible point lies 5.96e-12 below the float point's value (explanation plausible only); first-wave point violates rows by 8.9e-16; say which multipliers give 0.6258 and 293.2500703. |

### 4.3 camshape (CS)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| CS-01 | camshape-I1 | The original feasibility proof of E is a sketch. | PROOF | Include Lemma 3 (feasibility for any constants satisfying C1–C5; two cases); cite the exact row check as confirmation. |
| CS-02 | `crit-A1` | Hypotheses implicit. | PROOF | (a) needs C1, c₀ > 0, ū > 0, ℓ > 0; (b) needs C2–C5 and c_H ≤ 2; α ≥ 0 is implied. |
| CS-03 | camshape-I9 | Uniqueness and the greatest-element property are not stated. | PROOF | Include them in Theorem 1. |
| CS-04 | camshape-I2 | "proved analytically" overstates. | WORD | "proved (comparison theorem with exact rational checks)". |
| CS-05 | camshape-I3; `C6`; solvers S5, `C5`; PP-10; PP `C15` | The "600-fold amplification" explanation of p2 deficits is wrong. | NUM, WORD | "Row and bound violations of size ε can lower the objective by at most D_n(ε) ≈ 0.6 n²ε (for ε ≲ 1e-8); for ε = 3e-10 this is at most 2.81e-5 (n = 400) and 1.13e-4 (n = 800). Explicit ε-feasible points reach about 87% of this bound." The p2 points lie at least 8.15e-6 and 3.27e-5 below the optimum (N-27). |
| CS-06 | camshape-I4 | Older notes show upward-rounded optima. | NUM | Use only the summary's floor displays or Theorem 1(d) (no change). |
| CS-07 | camshape-I5; `crit-A4`; solvers S4, `C1` | QPLIB copies: rounding shift and reference points. | WORD, NUM | The copies' exact optima exceed v_n by at least 8.539e-7, 9.823e-6, 3.776e-5 and 8.699e-5. QPLIB's reference points for 2703 and 3177 (violation 3.0e-10) lie at least 8.15e-6 and 3.27e-5 below their copies' optima: tolerance artifacts. QPLIB_2738's point lies 5.8e-14 below (row violations 2e-14, printing level); QPLIB_2480's lies 1.5e-12 above. Drop the BARON-incumbent insensitivity argument. Three implementations agree (two dossier, one critic); no human review. |
| CS-08 | camshape-I6; `C1`; `crit-M1`; `C9`; solvers S3, `A4`, `C11` | MINOTAUR camshape800 (QPLIB_3177) framed as refuted. | WORD | L7: MINOTAUR's value is not attainable under exact feasibility; its implied dual is consistent with our optimum. Reaching its value needs row or bound violations of more than 8e-9, and explicit points with violations 9.7e-9 reach it (ANTIGONE's value on 2738 needs more than 2.5e-8; 2.9e-8 suffices). Same class as ANTIGONE 2738 and BARON camshape100/200. The root closure (1 node, remaining-node bound +∞) is circumstantial evidence of a possible defect, not a proof. No .nl fetch (C-10: skip); state .nl = .gms only where the copy is discussed. Relabel the summary row: "prior global claim on the rounded copy at a value not exactly attainable; our result is the first exact optimum". |
| CS-09 | camshape-I7; `C8` | COPS equality rested on a float slack check; LOQO agreement. | WORD | If COPS is mentioned, use the enclosure with the mpmath qualifier (no rational replacement, C-11: skip). LOQO values agree with −v_n truncated to five decimals. |
| CS-10 | camshape-I8; `C4`, `C5`; solvers S1, `C8` | Novelty framing. | WORD | "First exact (rigorous) proofs of global optimality for camshape200/400/800 and the first exact optimum for camshape100, to the best of our knowledge." Credit Octeract (camshape100, floating point; Bestuzheva et al.) and BARON 26.5.27 in our campaign (valid duals within 1.23e-7 and 4.80e-7 relative; 0.45 s and 23 s). camshape200: Octeract's listing concerns the rounded copy QPLIB_2480, whose optimum differs by ≥ 2.3e-6 relative. Listings for n = 200 and 400 are stale relative to BARON (n = 400: −4.6224 vs −4.9727, gap still large); n = 800 is not improved. |
| CS-11 | camshape-I10; `crit-A3` | Exact-feasibility qualifier. | WORD | State it wherever v_n is compared with listed or solver values. p2 points: maximum violation 3.0e-10 (G_1); hundreds of rows violated by about 1e-10. |
| CS-12 | `C2` | Stale cross-references to solvers propositions. | DOC | Dossier-internal; use Prop. 4 (BARON), 5 (D(ε)), 15 (QPLIB copies). |
| CS-13 | `C3` | α notation. | WORD | Write \|r_2 − r_1\| ≤ α (= 1.5Δθ). |
| CS-14 | `C7` | ANTIGONE margins from the printed value. | NUM | "at least 1.552e-4" and "at least 1.544e-4" (dossier/solvers text only). |
| CS-15 | `C10` | Edge rows and table reference. | WORD | "three edge rows"; Table B2. |
| CS-16 | `crit-A2` | Status of "this dossier only" items. | DOC | "reproduced by an independent implementation (same project)"; no human review. |
| CS-17 | `crit-A5` | LANCELOT COPS values explained by tolerance. | WORD | Optional, as numerical evidence only. |

### 4.4 chain-catmix (CC)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| CC-01 | CC-1; CC-11; `A1`; `C1`; solvers S19, `A6` | Four new proofs (C6, M1, M6, M8) and the transport to the exact-coefficient GAMS model. | PROOF | The critic read all four (A1); apply the C6 fix (strict chord; one line for the boundary; "for end values with L above the chord"). Then state that the catmix lower bounds hold for the GAMS model (c = 9a) too, with gaps ≤ 1.86e-13, 1.90e-11, 6.81e-11, 1.49e-10; drop the "no exact transport" caveat for the duals. COPS 3.0 is a different model. |
| CC-02 | CC-2; `C5`; `A2` | The strongest catmix duals rest on one implementation. | WORD | "Computed by one implementation; a second, independent implementation agrees with it per stage within 1e-14 on identical test inputs (N = 100: all 99 stages on a 324-ray grid and 40 stages on a 2^-21-band grid) and certifies, end to end, bounds weaker by at most 3.7e-10." No rerun (C-13, C-14: skip). |
| CC-03 | CC-3 | mpmath iv shared by both chain B&B codes. | DOC | List mpmath iv as trusted for chain (G-06); the catmix dual uses only directed binary64 +, −, ×, ÷. No Arb rerun (C-15: skip). |
| CC-04 | CC-4 | Authors' chain pruning squares an endpoint without directed rounding. | DOC | Cite the verifier's fully rigorous B&B as the certificate of record; ship the one-line patch (rerun gives identical certificates). |
| CC-05 | CC-5 | catmix400 primal via mpmath. | NUM | Exact rational objective; gap stays ≤ 6.81e-11. |
| CC-06 | CC-6 | "Listed primal values optimal to printed digits" is false. | WORD | Our exact points improve the listed primal values of chain100–400 by at least 1.5e-10 and of catmix100–800 by at least 2.2e-8. |
| CC-07 | CC-7; `C3` | Two incorrect remarks in the COPS verification report. | WORD | Spacing is quartered (2^-9 → 2^-11). The authors' extra catmix100 slack is interpolation in the stretched transported window (both runs use the same window rays; identical bounds), consistent with Lemma M6. |
| CC-08 | CC-8 | READINESS catmix runtimes are the authors' weaker runs. | DOC | Report both sets, labelled by the bound each produces: record (verifier/recheck) runs 2,358/1,170/2,578/2,595 s (reproduction 46.0/20.2/45.2/46.1 min); authors' weaker runs as in READINESS (1,049/1,728/3,001/4,602 s). |
| CC-09 | CC-9; PP `C1`; PP `CR-A1`; `A3` | Summary catmix dual range is the authors' weaker duals; several displays are invalid. | NUM | Per-instance displays of the duals actually used and of the primal points (N-19, N-20). Do not use: 5.072261493982863, 5.068917341793162, −0.04806943203114456, −0.04805914560067171, −0.04805590147967565, −0.0480694320309595635, −0.0480591455801143916, −0.048056547756611555, −0.048055901330847467. Take catmix primal values only from the 60-digit enclosure ends. |
| CC-10 | CC-10 | "Exact DP"; "the discrete optimum chatters". | WORD | "rigorous DP lower bound on an exact 1-D projective reduction"; "our best feasible points chatter". Update the summary mechanism cell. |
| CC-11 | CC-12; `C4` | Per-stage w not saved. | DOC, COMP | Not rerun (C-14: skip). If mentioned: about 2.6 h single-threaded and about 17 MB for w. |
| CC-12 | CC-13; `C9` | Priority statements; Müller et al. citation. | WORD | "to the best of our knowledge". Müller et al.: arXiv:1912.00356v1 Table 5 (gap-closed fractions implying negative bounds); nothing for chain200. |
| CC-13 | `C2` | The scouting note's calibration has a sign slip. | WORD | Say so, or do not cite it as equivalent. |
| CC-14 | `C6` | "Best page dual" vs MINLPLib's listed dual. | WORD | "The best dual bound reported on the instance pages (ANTIGONE) is 0.08–0.17; MINLPLib's listed dual, the third-best reported value, is −37.1 to −286.8; catmix has one reported bound and no listed dual." Use G-05 for the rule. |
| CC-15 | `C7` | Unsourced 1e-6 gap formula. | WORD | Drop the formula or say "under either normalization"; compare gap sizes, not solved marks. |
| CC-16 | `C8` | Dates of listed duals. | WORD | 2014–2025 (chain), 2015–2020 (catmix). |
| CC-17 | `C10` | Chain GAMS = OSIL evidence. | WORD | Exact identity by inspection (0.5·h, h = 1/N, L = 4, a = 1, b = 3; η = 1/(2N)). |
| CC-18 | `C11` | Grid design incomplete. | DOC | Add the N = 400/800 grid details or cite the exact `recheck_dp.py` commands. |
| CC-19 | `C12`, `C13` | Logged loss and B&B target. | WORD | Loss logged for N of the N + 1 minimizations; both target definitions give the same doubles. |

### 4.5 small: hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck (SM)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| SM-01 | small-pricing050-gap-v1-wrong; small-pricing050-gap-inconsistent; small-unsaved-verifier-points; cost-estimates-understated | pricing050 gap appears as 4.23e-14, 1.0e-17, 2.7e-12 and (wrongly) 2.0e-17. | NUM | Use ≤ 1.92e-14 against the saved, exactly feasible authors' point (objective −1813.8290784519730769, exact; `r2/pricing_check.log`, rerun and read by the critic) (N-11). Never 2.0e-17 or 1.0e-17. No verifier rerun (C-18: skip). |
| SM-02 | small-pindyck-gap-strong-concavity; c2-dual-implementation-support | Strong concavity (μ = 0.001) gives J(p) ≤ J(p*) + ‖g‖²/(2μ); gap ≤ 1.7e-29. | PROOF, NUM | Recommended: include Theorem 6 and display gap ≤ 1.8e-29 with 34-digit displays (N-12). Both parties' gradient enclosures support < 6e-29; critic re-derived it. Lead to confirm (Section 8). |
| SM-03 | small-gibbs-single-implementation; gibbs-cert-asserts | Displayed ex6_2_* duals came from the verifier's `gibbs_bb.py`; the dossier's `gibbs_cert.py` is a third implementation, read and partly rerun by the critic. | WORD, COMP | Keep the displayed values. Say: certified by the verifier's code and confirmed by a separate implementation (code read by a second agent; asserts incomplete). Do not adopt the tighter values. Optional: add the componentwise R_p assert and an explicit vapour-form check, rerun both cases (C-16, ≈ 5 CPU-min) before calling the two fully independent. |
| SM-04 | small-etamac-single-implementation | The displayed etamac dual rests on the verifier's code alone. | WORD | State the provenance: verifier's `v_etamac.py` (read line by line in the dossier); the authors' independent code certifies −15.294675643368096 (gap 6.5e-15). No rebuild (C-17: skip). |
| SM-05 | small-unsaved-verifier-points (etamac) | Verifier's etamac point not saved. | DOC | Use the dossier's exactly feasible etamac point from the saved authors' decisions (`r2/etamac_point.py`; gap 2.5765e-15). |
| SM-06 | small-unsafe-secondary-displays; `C3` | Unsafe strings in secondary documents. | NUM | Do not copy: −70.752077833447706, −70.75207783344770758, −0.16084761546364904, −15.294675643368092, −15.294675643368092168. |
| SM-07 | small-etamac-primal-display-missing; `C1`, `C2` | Displays do not reproduce the ex6_2_5 and etamac gap cells; etamac primal missing. | NUM | ex6_2_5 primal −70.75207783344770558; etamac dual −15.29467564336809217, primal −15.29467564336808959; exact etamac gap 2.5765e-15; cells unchanged (N-08 to N-10). |
| SM-08 | small-model-provenance-decimals | Source models vs stored decimals. | WORD | The enclosures are for the stored MINLPLib models and need not contain the optima of the exactly specified source models (G-01). |
| SM-09 | small-pindyck-hessian-map-hand-derived | Hessian map Ψ hand-derived. | WORD | Cite the two derivations, the symbolic second-order step check and the 50-digit finite-difference agreement; no symbolic recursion proof (C-19: skip). |
| SM-10 | small-gibbs-prior-work-unread | Handbook and McDonald–Floudas unread. | WORD | Keep "very likely found ε-globally (not confirmed)", "partly known", "to the best of our knowledge, no rigorous certificate". Obtaining the sources is a reading task. |
| SM-11 | small-hvycrash-tolerance-artefacts | Tolerance-feasible values cluster at −0.2185 + j·0.00437. | WORD | Optional labelled remark; not a reconstruction of the COCONUT points. |
| SM-12 | `C4` | pindyck trust base misstated. | WORD | Authors: IEEE round to nearest plus γ_n padding analysis. Review: IEEE binary64 with `nextafter`, mpmath iv and Fraction. The displayed dual is certified by both codes; "none uses A1/A2" holds only for the review's code. |
| SM-13 | `C5` | Outdated literature metadata. | WORD | Cite `cuesta2025-global-optimization-of-mixed-integer` (arXiv:2510.14122v3) and the Smith excerpt slug `smith2011-smith-thesis-coconut-table-a`. |
| SM-14 | `C6` | λ·b validity. | WORD | λ·b is not a valid bound for either Gibbs instance, for separate reasons (rounded λ for ex6_2_5). |
| SM-15 | `C7` | ".solu weaker for all six". | WORD | "for the five instances that have one". |
| SM-16 | `C8`, `C9`, `C11` | Small factual slips. | WORD | Print stored coefficient digits; "with this λ no τ below about 4.19e-15 can be certified"; "shortest round-trip decimals of the binary64 products, used exactly". |
| SM-17 | `C10` | pindyck eigenvalue caption. | DOC | Correct F vs G; plot only saved samples. |
| SM-18 | etamac-tightness-interpretation; sif-soltn-labeling; pindyck-variable-count | Wording. | WORD | Label the κ remark as interpretation; SIF SOLTN values are other-N instances (hand-derived identity); 116 = 7·16 + 4 fixed initial states. |

### 4.6 eg: eg_int_s, eg_disc_s, eg_disc2_s (EG)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| EG-01 | eg-1, eg-2, eg-3; eg-crit-1; `C1`, `C5`, `C10` | Trust framing: A1 (padding analysis) unwritten; A2 (numpy/SVML exp) sampled; integer powers via SVML pow. | PROOF, COMP | L4. Appendix Lemma A1 (F1–F4 table, including the roundings of the padding operations, `C10`). After the audited rerun (C-01), the theorem rests on (H0) + Lemma A1 + code correctness for all three instances. Proposition A2′ becomes an optional remark (9.96e-14, ≥ 448 ulp). Summary verification cells change from "under A1/A2" to "Lemma A1 proved; exp and pow audited" once the rerun passes. |
| EG-02 | `C11` | Auditor independence. | COMP | See the requirements under L4. |
| EG-03 | eg-7 | Recordings for eg_int_s/eg_disc_s deleted; no tree-free coverage proof. | COMP | Part of C-01: regenerate, rerun coverage and `own_cover.py`. |
| EG-04 | eg-4; `C1` (S-F) | Lemma S not in paper form; S-F also uses pow. | WORD | Not needed for the theorem after L4. Describe S-F as a cross-check with its trust base (Lemma S, pow accurate to 1e-12). No S-F rerun (C-20: skip). |
| EG-05 | eg-crit-2; `C2` | S-I replay of eg_disc2_s part 1 ran with the pre-guard `dual_value`. | WORD | S-I ((H0) only) is a second complete proof for eg_int_s and eg_disc_s; for eg_disc2_s part 1 state the side condition (no call with S.lo ≤ 0; Σy = 1 by LP duality; guarded S-F rerun minimum Σy 0.9999999999999998). No replay (C-21: skip). |
| EG-06 | eg-5 | eg_disc_s display 5.760539610694994 is 2.4e-16 above the binary64 bound certified by the S routes. | NUM | Print 5.760539610694993 (valid under every route) (N-23). Delete the summary's paragraph about the ...994 display. |
| EG-07 | eg-6; eg-11; PP-2; PP `C12`, `C14` | "≤ 1e-9 relative" sits at the boundary; two primal proofs concern different points. | NUM, WORD | Name the sol-file decimal point (shortest-repr strings read as exact decimals). Its objective is enclosed by `eg_dyadic_check.py` (library-free; reviewed only by the critic's first pass and an mpmath-iv cross-check) and by mpmath iv. Relative gaps at most 9.997e-10 (computed here: 9.9969e-10, 9.9965e-10, 9.9957e-10). U′ (IEEE-only enclosure of the binary64 search point) gives 1.00000008e-9; mention it as the (H0)-only figure. Save the exp test of `eg_dyadic_check.py` and have the script reviewed before citing it as independent. |
| EG-08 | eg-8 | Stale eg wording in R documents. | DOC | G-08; the paper uses the summary and this register. |
| EG-09 | eg-9; `C7` | "Same tree / box for box". | WORD | "identical logged statistics, except one box in run I part 1". |
| EG-10 | eg-10; `C8` | Robustness remark. | WORD | eg_disc2_s: "about two orders of magnitude"; eg_int_s's smallest margin (7.69e-11) is below the combined padding, so its validity rests on Lemma A1. |
| EG-11 | eg-12; `C3` | Publisher correction unread. | WORD | Now read: cite J. Glob. Optim. 95 (2026) 1095–1141 (doi:10.1007/s10898-026-01614-9); eg rows unchanged; state the reversed column reading. Update the summary sentence "whether it changes Table 17 remains unchecked". |
| EG-12 | eg-13 | First-draft cost errors. | DOC | Use the revised costs (C-01). |
| EG-13 | eg-14 | Model provenance. | WORD | Describe the Gaussian-kernel structure as an observation; no physical or GP provenance. |
| EG-14 | `C4` | Listed-status note. | WORD | Show all three bold duals; listing dual = third-best (G-05). |
| EG-15 | `C6`; eg-crit-3 | Cost figures. | DOC | Interval auditor 6.8–8.9 CPU-h including recordings; option (e), ≈ 50 CPU-h, costed and rejected. |
| EG-16 | `C9` | Flush-to-zero remark. | WORD | Drop; (H0) assumes gradual underflow. |
| EG-17 | eg-crit-4 | Cody–Waite constants L1, L2. | DOC | Cite the exact check (\|ln2/64 − L1 − L2\| ≤ 1.8e-28) next to `table_exact.log`. |
| EG-18 | summary; solvers S10 | Credit and CAMINO. | WORD | Credit SCIP 8.1's floating-point solve of eg_int_s (Göß–Burlacu–Martin). CAMINO: SV-09. |

### 4.7 powerflow (PF)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| PF-01 | PF-1; `C4` | 41869.05148327244 exceeds the 0039r certificate by 6.03e-12. | NUM | Cite only 41869.05148327243 or 41869051483272433/10^12 (no change from the summary). Correct location list; credit `closing-confirm-r1.md:126`. |
| PF-02 | PF-2 | Stale "no exactly feasible point" sentences. | DOC | G-08. |
| PF-03 | PF-3; `C11`; PFC-4 | Stored 0039p certificate uses the angle rows (tan bounds); the angle-free variant is stronger. | PROOF | Replayed with the reviewer's independent code (9 s; all 6 leaves PD at ε = 0; minimum 41869.05148528834). State Theorem B for R without angle rows, so no instance uses a trigonometric step. Keep the cited value 41869.05148485014. |
| PF-04 | PF-4; PFC-4 | 0030p dual rested on one OSIL reader. | DOC | Resolved: rows reproduced by the reviewer's reader; the stored multipliers give the stored bound exactly on those rows. |
| PF-05 | PF-5 | `pf_cert.interval_cholesky` uses unreviewed padding. | WORD | Cite only the exact PSD proofs; no floating-point error analysis enters the dual bounds. |
| PF-06 | PF-6 | 0030p certificate can be replayed, not regenerated. | DOC | Ship `*.sdpcert.json` and `*.bb3t.json` with SHA-256; verification = replay. No re-solve (C-25: skip). |
| PF-07 | PF-7 | Models are not MATPOWER case30/39. | WORD | "for the MINLPLib models as distributed"; shunts and taps dropped, angle limit 0.26; case30 with shunts has a local solution 576.8923368 below our bound; never transfer bounds (also not to 0030r). |
| PF-08 | PF-8; `C6`, `C10` | Numbering and definitions. | WORD | MATPOWER numbering (bus 30, bus 2, branch 2–30) with OSIL names once; "at p1 and at x*" not "at the optimum"; define b := −b_km = 1/x > 0. |
| PF-09 | PF-9; PFC-2; PFC-3 | Numerical diagnostics. | WORD | Label as diagnostics; 0030p Shor tightness ≤ 1.17e-6 as a corollary; Clarabel's 0039r primal value lies 1.3e-7 below the certified root dual; "cuts at bus 30 alone sufficed (certificate)"; other lossless leaf buses (31, 32, 35) in one clause. |
| PF-10 | PF-10; `C3` | Positioning of the leaf cut. | WORD | Exact leaf identity plus its concave envelope; no novelty claimed. Describe Chen–Atamtürk–Oren's J_C correctly (W_ii, W_jj, phase-ratio bounds, W_ij ≥ 0); delete "affine image". Read Kocuk–Dey–Sun and Coffrin et al. before any precise comparison. |
| PF-11 | PF-11 | "Solved on MINLPLib". | WORD | "closed to a certified relative gap of 2.1e-9 / 6.4e-10 / 6.7e-10" (G-04). |
| PF-12 | PF-12 | KB metadata errors (Oustry; Josz title). | DOC | Take bibliography from the network report §10. |
| PF-13 | PF-13 | First-pass dossier text errors. | DOC | Use the r2 dossier. |
| PF-14 | PF-14; `C9` | GAMS ≡ OSIL evidence. | WORD | "checked by exact term-by-term comparison"; quote the status track's control verdict, not the jl2017 field. |
| PF-15 | `C1` | Eigenvalue "splitting". | WORD | "Inexact multipliers shift the double zero eigenvalue to a double eigenvalue of either sign (+4.0011e-9 for 0030p, −1.0943e-9 at the 0039p decisive leaf, about −6.07e-10 at 0039r)"; Proposition 6 is standard (Lavaei–Low). |
| PF-16 | `C2` | 0039r balance rows. | WORD | 0039p: x103 − x263, x195 − x273 (e581, e591); 0039r: x64 − x263, x156 − x273 (e397, e407). |
| PF-17 | `C5` | MINLPLib's infeasibility measure. | WORD | Documented: maximal absolute violation, evaluated by MINLPLib on its stored point; ours is a 50-digit evaluation of the .sol decimals. |
| PF-18 | `C7`, `C8` | Plane vertex counts; shift labels. | WORD | "at least four vertices"; label ε values as dossier recomputation or stored. |
| PF-19 | PFC-1 | 0030r wave-3 bound unverified. | WORD | Do not cite it; never use it for 0030p. |

### 4.8 waterno2 (WN)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| WN-01 | W1; W11; `C1`, `C3`, `C10`; `A2` | Period/pair bounds are not stored proof objects; `certify.py` regeneration differs for 18/24. | DOC | L5. Wording: "computed by a rigorous branch and bound and recomputed by a second, separately written branch and bound with exact rational node bounds". B&B codes are deterministic for fixed targets and a fixed software stack (identical status, bound and node count); `certify.py` is not, because it derives targets from time-limited SCIP runs. Replays: 06/09/12 exact; 18 and 24 give 4790.820086219 and 6576.150434342 (valid, weaker). Claimed values rest on the original rbb run and on vbb2 at the stored B_t; 1,564 vbb2 replays matched. Give a fixed-target replay command (`run_period.py` with the stored B_t; ≈ 8.5 CPU-h vbb2 or ≈ 5.8 CPU-h rbb). READINESS times are replay wall times. Record SciPy 1.18.0/HiGHS. A leaf checker's cost is uncertain (propagation must be re-verified). |
| WN-02 | W2; `C2` | Two code lines, not three; shared propagation. | WORD | A wrong value needs an error common to both lines on the same statement. Costs (if quoted): full certB re-bounding ≈ 20–30 CPU-h unloaded; exact-propagation replay ≈ 60–120 CPU-h (C-30: skip). |
| WN-03 | W3; W8; `A1` | Reader and GAMS ≡ OSIL. | WORD | Two formats, three parsers and both B&B builders agree exactly for all five instances. |
| WN-04 | W4; `C5` | Link-0 cell coverage via OBBT. | PROOF | Lemma 5 in the appendix with the complete row list (add e50, e516, e81, e900/e901, e924/e925, e1170, e1172, e1174/e1175, x542 ≤ 1). |
| WN-05 | W5; `C7`, `C8` | Display and wording inconsistencies. | NUM, WORD | Use the summary's upward displays (≤ 1.68%, ≤ 4.87%, ≤ 10.82%; never 1.67%, 4.90%, 10.8%). "Each period bound and each of the 49,315 pair-box (record) bounds used was recomputed with a second B&B code; the leaf-pair bounds follow by an exact linear correction (556 were also re-bounded directly)." Factors 1.68–6.22. |
| WN-06 | W6; `C9` | Solved status; Huang comparison. | WORD | MINLPLib marks only waterno2_01/02 solved. "Huang's reported 3-period optimum is incompatible with waterno2_03's listed point; either the models differ or the reported value is wrong." |
| WN-07 | W7 | Data semantics. | WORD | One sentence: decimal-exact semantics; under binary64 data, points with station A, B2 or D off are infeasible; link to the SCIP finding (G-01). |
| WN-08 | W9; `A3` | Scope for 09–24. | WORD | State that 09–24 use the wave-2 period Lagrangian only (bundles stopped early; 24 from zero multipliers). Drop the "several hundred CPU-hours to 3–5%" estimate (C-31: skip). |
| WN-09 | W10 | Literature gaps. | WORD | "new as far as found"; Huang 2011 is a Diplom thesis per the FU catalog (not obtained); read Ghaddar et al. 2015 and Carøe–Schultz, confirm Berenguel before submission; no method novelty (G-07). |
| WN-10 | W11 | Timing measures differ. | DOC | One source per table; define wall vs CPU, workers, shared machine. |
| WN-11 | W12; `C6` | Consistency evidence; per-period margins. | WORD | Cite the necessary-condition check (all 69 period-Lagrangian values ≥ B_t). Label the 06 margin chart "wave 2", or show certB pair margins along x*'s cells plus the DP term (2.205). |
| WN-12 | W13 | Tariff values. | WORD | waterno2_09 has two tariff values; 12–24 have three. |
| WN-13 | W14 | Review r1 received truncated method text. | DOC | Note in the verification table; validity rests on exact feasibility checks reproduced by r1. |
| WN-14 | `C4` | SCIP wording. | WORD | "for some random seeds, wrong optimal values on periods 0, 4 and 5 (period 0 not on master in 10 seeds) and on one cell-pair subproblem"; "up to 3.8" (periods), 9.4 (pair). |
| WN-15 | `C11` | Four small overstatements. | WORD, PROOF | Theorem 3.4's assumptions "not established; fail at practical cell sizes"; "root propagation or root OBBT, without cutoff"; one-cell Theorem 3 "is at least as strong as" Proposition 1; add s_0 = σ to Lemma 2's hypotheses. |

### 4.9 ann-kan (AK)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| AK-01 | I1; `C3`; `A3` | The verifier's KAN path relied on numpy exp (empirical 2^-50). | DOC, WORD | L3: adopt the rigorous-exp rerun (55 CPU-min; 17-line diff reviewed by the critic); archive `D/ann-kan-checks/`. Disclose that both paths now share `kan_iv.iexp_pt_fast` and `ia.NI` (read in full by the dossier author and the critic; constants checked rationally); the wave-3 numpy-exp run is an exp-independent empirical cross-check (bit-identical for five instances; r5_n3 3.2e-12 higher). |
| AK-02 | I2; `A4` | ANN re-certification region lists lost (/tmp). | DOC, COMP | Document the regeneration (review `replay.py` + `leaves.py`, acceptance test: frontier identity; ≈ 2 h one core + ≈ 2.6 CPU-h verify). Not run for the paper (C-33: optional for the release). The final open boxes can be re-verified from `ext_logs/open_run2.npz` (≈ 25 CPU-min). |
| AK-03 | I3; PP-3; PP `C9` | Summary and READINESS say ANN/KAN primal enclosures assume mpmath iv. | WORD | "proved in exact rational interval arithmetic (independent review r1); confirmed with mpmath intervals (authors)". Update the summary sentences. |
| AK-04 | I4; `C8` | R_P is simpler and stronger than R; U is an enclosure end. | WORD | Report L ≤ min R ≤ min R_P ≤ U; points of R_P with objective ≤ U (enclosure width ≤ 3.2e-89). |
| AK-05 | I5; I6 | "Intended network"; "certified to about 1e-10"; "first finite dual". | WORD | Use R/R_P with definitions; KAN gaps ≤ 2.42e-8 (r5_n3) and ≤ 1.08e-10 otherwise; "first rigorous dual bound found". |
| AK-06 | I7; `C5` | Wave-3 ANN gap roundings; rounded-down displays. | NUM | Omit the wave-3 bound from the main table, or give "19.07% of \|primal\| (absolute 644.52)"; 16.02% under the dual denominator. KAN r5_n5 relative 3.74e-10. |
| AK-07 | I8 | L is not valid for tolerance-feasible OSIL points. | WORD | State it next to the KAN result and the SCIP values. |
| AK-08 | I9 | Our ANN point lies 7.18e-8 below displayed duals on ann_cumene_exp. | WORD | At most a footnote, class (i-r) (display rounding); no solver-error claim. |
| AK-09 | I10; `C10` | ANN gap not closed. | WORD | "consistent with a constrained cluster effect of first-order bounds along a large, nearly flat valley on x772 = 0.999"; future work (C-36: skip). |
| AK-10 | I11 | GAMS vs OSIL only at sample points. | WORD, COMP | Say "OSIL model". Exact GAMS comparison optional (C-34). |
| AK-11 | I12 | tanh enclosures return [1, 1] for \|z\| ≥ 300. | PROOF | Appendix argument (every use passes an outward-rounded operation that widens by ≥ 2^-55); release code uses `nextafter(1.0, 0.0)`. |
| AK-12 | I13; `A2` | Neither KAN code read by a third party; NaN handling in path (II). | WORD | Report L (valid if either code is correct, given the shared components of AK-01). List "no NaN lower bound (unchecked)" as an assumption of path (II); path (I) is NaN-safe. Optional reading (C-35: skip). |
| AK-13 | I14 | mpmath-derived exp constants. | DOC | Resolved by `check_constants.py` (rational proofs). |
| AK-14 | I15 | r3 primal points not best known. | WORD | Claim primal improvements only for kan_r5_h1_n3/n5/n8. |
| AK-15 | I16; `C2` | Method antecedents. | WORD | Cite `ninin2015-a-reliable-affine-relaxation-method` as the direct precedent of the per-box bound, `messine2002-…`, `stolfi2003-…`, `figueiredo1997-…`, `berz2009-…`; state the differences; no method novelty. |
| AK-16 | I17 | KAN scaling row sign. | WORD | Fixed (x777 = 1.1796…·x776 + 0.00391…). |
| AK-17 | `C1` | Prior RS formulation statement wrong. | WORD | Critic's sentence (J-21): the source's RS runs may refer to a relaxation of the MINLPLib model; BARON ran the full-space model. |
| AK-18 | `C4` | "Same incumbent in all six runs". | WORD | UB bit-identical except r5_n3; r3_n4/n5 returned different nearby points with the same UB. |
| AK-19 | `C6`, `C7`, `C9`, `C11` | Proof-text precision. | PROOF | Symbol-absence asserted only in the reviewer's code (true by construction in the authors'); resultant vs gcd tests both suffice; Lemma P adds "appears only linearly with a provably nonzero total coefficient"; tolerance details of paths (I) and (II). |
| AK-20 | `C12` | Check-script docstrings and constant test. | DOC | Fix docstrings; test the actual `SILU_MIN_LO`; label the crude-bound line non-certifying. |
| AK-21 | `A1` | One OSIL reader shared by all decoders. | DOC | Resolved by the critic's exact comparison with `rosil.py` (0 differences, 8 files); add to trust lists; archive `cmp_readers.py`. |
| AK-22 | `A5` | Two infeasibility metrics for p1. | WORD | Name the metric next to each value (page: 2e-12; our maximum absolute row violation: 8.2e-12 at e790). |

### 4.10 primal-points (PP)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| PP-01 | PP-1; `C2`, `C3`, `C13`; `CR-A2`; `CR-A4` | Data-semantics convention unstated; dual-side reading unconfirmed for most families. | WORD, DOC | G-01. Check K6 (Section 7) confirms reading (b) at grep level for camshape, pindyck (review code), catmix, powerflow (reviewer's reader), waterno2 (vmodel), ANN, KAN and eg route R (decimal data converted with error ≤ u, covered by Lemma A1 F1; eg GAMS ≡ OSIL exactly); the dossiers had confirmed chain, dtoc5, optcdeg2 and the wave-2-small verifier. The final review confirms by reading (C-53). |
| PP-02 | PP-2; `C14` | eg primal points lacked an outward-rounded proof; first dossier script was invalid. | DOC | See EG-07. Save the exp test; review `eg_dyadic_check.py`, `eg_iv_check.py`, `ex62_check.py` and the catmix400 exact rerun (1–2 h) before citing them as independent proofs. |
| PP-03 | PP-3; `C9`, `C10`, `C18`; DO-2 | Trust base per instance. | WORD | G-06. Four primal claims rest on mpmath iv without an mpmath-free re-proof: hvycrash and pindyck (two implementations), etamac and pricing050 (single verifier implementation plus the dossier's evaluation). No dyadic re-proofs (C-38: skip). |
| PP-04 | PP-4; `CR-A1` | Outdated statements and unsafe displays in R documents. | DOC | G-08 (includes README powerflow primals 41869.0515113202/…208 and ANN −3379.9824, both invalid as upper bounds; `references.json` mislabel). |
| PP-05 | PP-5; `C5`, `C16`; `CR-A3` | Artifact table. | WORD | Add lnts50 p1 (LL-04). Display-rounding-only list: lnts100, lnts400, lukvle10, chain50/100/200 (the chain p1 points evaluate 6.4e-12 to 1.4e-10 above the duals). Cite the solver-campaign artifact table in full or state the selection rule ("solver optimality claims only"). |
| PP-06 | PP-6 | lnts tolerance-vector violations quoted inconsistently. | NUM | "≤ 1.3e-14" (text only). |
| PP-07 | PP-7 | Krawczyk existence theorem not self-contained. | PROOF | Use dossier Theorem C with its proof. |
| PP-08 | PP-8 | Implicitly defined points. | WORD | Define each point by its certificate data; no finite decimal vector is claimed exactly feasible for lnts, lukvle10, powerflow, ANN, KAN. |
| PP-09 | PP-9; `C7` | Rational-point remarks. | WORD, PROOF | Drop the genus-1 and "no rational parametrization" sentences; Proposition L (Lindemann–Weierstrass) for lnts is optional. |
| PP-10 | PP-10; `C15` | Multiplier mass vs weights; hvycrash paired with the wrong lemma. | WORD | See CS-05; remove hvycrash from the lower-bound lemma remark. |
| PP-11 | PP-11 | lnts gaps set by h2 margin. | — | Superseded by Theorem 3 (L1). |
| PP-12 | `C1` | catmix100/200 primal displays float-printed. | NUM | See CC-09 and N-20. |
| PP-13 | `C4` | Kearfott 1998 is in the KB. | WORD | Cite Hansen (1992, §12.3) and Kearfott (1998) as the antecedent of C2; state the differences. |
| PP-14 | `C6` | Proposition B does not cover hvycrash's alg rows. | PROOF | Generalize (x_k := φ_k(x_<k) with r_k(x_<k, φ_k) = 0 an identity on a proved domain) or treat hvycrash separately. |
| PP-15 | `C8` | Review count. | WORD | Four r1 reviews cover the 13; a fifth covers water, ANN, KAN. |
| PP-16 | `C11` | Rounding and artifact definition. | WORD | "rounded in the conservative direction"; artifacts = values outside a certified bound or impossible for an exactly feasible point. |
| PP-17 | `C17` | Small numeric/scope inaccuracies. | WORD | One rounding convention for the powerflow parentheticals; swapped-root objective for chain50 only; add the atanh tail bound to T4. |

### 4.11 audit (AU)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| AU-01 | AUD-1; `C13` | Wording and margins. | NUM, WORD | "proved by exact rational arithmetic or an interval Krawczyk existence test" (no duality certificate proves invalidity); "a screen of all 11,086 listed per-solver bounds against all 2,816 listed points"; rocket margins "at least 1.06e-7, 4.7e-8, 1.89e-7" (N-30). |
| AU-02 | AUD-2; `CRIT-A1` | Novelty unsupported. | WORD | G-07. Frame as a systematic screen of listed data with exact-feasibility proofs. Cite Vigerske 2014 (verbatim or [sic]), Neumaier et al. 2005, MIPLIB 2017, PAVER 2.0, Nowak 2008 (LaGO; BARON wrong root bound), Vigerske 2017 (SCIP), MINLPLib removal notes. A targeted search (1–2 h reading) before any priority sentence. |
| AU-03 | AUD-3; AUD-15 | GAMS/OSIL identity for audited instances is unreviewed. | DOC | Include "certificates hold for both forms" only after a reviewer reruns `gms_osil_drive*.py` on copies (C-44, minutes); otherwise say "OSIL model". methanol50 differs in 360 objective coefficients (verdict proved on both). |
| AU-04 | AUD-4; AUD-15 | Rocket second implementation unreviewed. | DOC | Include after the reviewer rerun (C-44, seconds). |
| AU-05 | AUD-5; `C8` | topopt certificate not replayable; emfl y not saved. | NUM, DOC | Display "objective ≤ 10.33548 (two independent implementations)", or ≤ 10.33547427574701. Regeneration with basis and rational y: optional for the release (C-40). |
| AU-06 | AUD-6; `CRIT-A5` | Trust base of 7 Krawczyk pairs. | WORD | List their assumptions (binary64 matrix products; mpmath iv exp or mpmath exp at 90 digits) separately from the 12 exact-rational pairs. No all-rational rerun (C-41: skip). |
| AU-07 | AUD-7 | Gap-tolerance interpretation. | WORD | "consistent with pruning or reporting at a 1e-4 gap tolerance"; mechanism statements labelled as inferences. |
| AU-08 | AUD-8; `C9` | Coverage is a lower bound; oil. | WORD | 19 (22 with rocket) is a lower bound; 3,851 display ties undecidable. oil: likely invalid but unproved (rank 1391 of 1408 at first attempt; reduced system 1131 of 1141); "could add". No computation (C-42: skip). |
| AU-09 | AUD-9 | Counting. | NUM | "19 per-solver bounds (15 distinct numerical conflicts) on 15 instances" (N-31). |
| AU-10 | AUD-10; `C3` | Display hypothesis. | PROOF | Appendix: Hypothesis H and Lemma 1 with "d(s) has at most 10 significant digits (true for \|d\| < 2^26)" and the two-step rounding for \|b\| < 10. All 22 refutations exceed one unit (min 1.069); all 19 exceed 10/9 units (min 1.1158). |
| AU-11 | AUD-11; `CRIT-A4` | emfl shortfalls. | NUM | "at least 1.41e-5 (1.36e-6 relative)" (emfl050_3_3, evaluated p2 point) and "at least 6.86e-6" (emfl100_5_5) (N-29). |
| AU-12 | AUD-12 | emfl050_3_3 S mark. | WORD | Its best listed dual lies ≥ 1.213e-5 (≥ 1.166e-6 relative) below the exact optimum; consistent only with the listed primal, which no exactly feasible point attains; do not call the S mark wrong. |
| AU-13 | AUD-13; `C1`, `C2`, `C4` | Aggregate-dual statement. | WORD | Restrict "MINLPLib's aggregate dual is not beaten beyond display rounding" to the 15 class (i) instances, rocket, emfl, spring and lop97icx. eniplac and stockcycle: the displayed aggregate dual has the same (i-r) status as its constituents. .solu rule: 589/589 with `inf` counted. G-05 for the listing rule. Use one exact f per instance and lower ends for "not beaten". |
| AU-14 | AUD-14 | Live site. | DOC | Date-stamp every table (pages 2026-09-30, site 2026-09-14, refresh of 69 instances 2026-10-02); archive pages with the release. |
| AU-15 | `C5` | OSIL byte-identity scope. | WORD | "the 69 relevant instances (status track) and those re-fetched by the verifiers". |
| AU-16 | `C6`, `C7`, `C10`, `C11`, `C12` | Small wording. | WORD | Verbatim quote; distribution sentence (seven gross pairs at 1.2e-5 to 7.3e-5 of \|d\|, eight tolerance-scale at 1.9e-9 to 3.3e-7); perturbation sizes; 113818.899052505; "best listed primal values". |
| AU-17 | `CRIT-A2` | Decimal reading. | WORD | G-01. |
| AU-18 | `CRIT-A3` | stockcycle form identity numerical only. | WORD | State the limit (C-43: skip). |

### 4.12 solvers (SV)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| SV-01 | S1; `C8`; PT `C9` | "Zero closures"; BARON camshape claims. | WORD | L7. "No solver closed an instance consistently with exact feasibility. BARON 26.5.27 closed camshape100 and camshape200 to MINLPLib's 1e-6 tolerance with valid duals (within 1.23e-7 and 4.80e-7 relative; 0.45 s and 23 s); its optimality claims are not attainable under exact feasibility." BARON pruned against incumbents below the exact optima, so its iteration counts are not clean evidence of relaxation strength. Camshape prior work: CS-10. |
| SV-02 | S2; `C9` | Sense of "feasible" in the SCIP finding. | WORD | Three readings: exact decimal (SCIP's dual invalid); SCIP's eps semantics (accepts points 7.5e-4 to 9.43 better than its declared optimum; binary64 residuals ≤ 2.9e-15); zero-tolerance binary64 (fm336 dual valid, but the returned point is infeasible and its value is not the optimum; every feasible point costs ≥ 2.247). Lead with self-inconsistency and fm336; tiny2's claim lies 9.6e-7 from its binary64 optimum. |
| SV-03 | S3; S4; `C1`; `A4` | QPLIB copy bounds and reference points. | WORD | See CS-07/CS-08. A third implementation reproduced all eight bounds; whether a further review is needed before the paper states the copy results is a lead decision (Section 8). Notifying QPLIB maintainers is a user decision. |
| SV-04 | S5; `C5` | 600-fold sentence; "worst case". | WORD | CS-05. |
| SV-05 | S6 | Campaign reference columns stale. | DOC | Use the summary's exact displays in paper tables; update the "Remaining limits" sentence; regeneration of references optional. |
| SV-06 | S7; `A7` | Deleted `report.prev.md` cited. | DOC | Cite the HEAD `report.md` (the backup was never committed). |
| SV-07 | S8 | Newer patch releases existed. | WORD | State the bundled versions (BARON 26.5.27, GUROBI 13.0.2, GAMS 54.3.1); do not call them the latest. No rerun (C-45: skip). |
| SV-08 | S9; `A3` | MINOTAUR infeasibility on QPLIB_8803. | WORD | Refuted for the model as written, assuming .nl = .gms; the default-bound question is moot (infeasibility detected in the first presolve, before default bounds; rule in the saved source). |
| SV-09 | S10; `A5`; `C4` | CAMINO wording. | WORD, NUM | "The best bound recorded for Gurobi 13.0.0 in the public CAMINO data is invalid"; the CSV has no status column, and the pipeline kept only runs AMPL labelled 'solved' or 'limit'; cause unknown; 13.0.x fixes only as context. Margins as floors: ≥ 0.2445944, 0.4312902, 5.2010558; percentages 7.48% and 80.6% (not 7.5%, 81%). |
| SV-10 | S11; `C14` | KAN contradiction. | WORD | "below the certified minimum of the network relaxation R of the same networks"; SCIP's duals for the exactly infeasible models are trivially valid; its optima are tolerance artifacts (class A). Model identity rests on counts plus the reviewer's permutation test. |
| SV-11 | S12 | No second review after fixes. | DOC | Independent review of `results_table.csv`, flags and wording (1–2 h; no solver runs) before submission. |
| SV-12 | S13 | Upstream SCIP report not filed. | OOS | User decision; never write "reported" unless filed. |
| SV-13 | S14; `A2` | SCIP mechanism traced only in 15 instrumented runs. | WORD | Keep the report's scope. No source-level fix or scan (C-46: skip); fm336/tiny2 L-substitution test optional with authorization (C-47). |
| SV-14 | S15; `C7` | pair2236 low claims. | WORD | Neither refuted nor confirmed; no run (C-48: skip). |
| SV-15 | S16; `C6` | Flag evidence. | WORD | Drop S16. Of 36 returned flags, 15 have 50-digit checks; the 17 OSIL flags beyond printing are non-feasible by Lemma 1 as printed. |
| SV-16 | S17 | Framing of the campaign. | WORD | A status check of current solvers on the stored models, not a method race; disclose certificate effort; no speed ranking. |
| SV-17 | S18; `C2`; `A1` | Exposure of listed SCIP bounds. | WORD | The syntactic scan finds binary64-inconsistent square/cube bound pairs only in waterno2; only the 0.7-station cube rows (one per period) can trigger the traced exact-intersection cutoff ("the outward-rounded binary64 enclosure of fl(0.7)³ lies entirely below fl(0.343)"); seed 11 (0.85 station) is untraced. The listed SCIP duals on waterno2_03/04 are not contradicted and are bracketed by other solvers' listed duals (if valid). No SCIP experiment (C-49: skip). |
| SV-18 | S19; `A6`; CC-01 | Campaign solved .gms files. | WORD | Footnote: GAMS ≡ OSIL exactly except catmix (coefficients differ ≤ 2.4e-16 relative); for catmix the duals transfer by Proposition M8; the smallest affected margin is 1.48e-9. |
| SV-19 | S20 | Stale cross-document statements. | DOC | G-08; cite `R/publication/scip-bug/report.md` and summary displays. |
| SV-20 | `C3` | Lemma 8 "exactly". | PROOF | Upper end equals the tightest upper end minus fl(0.343); SCIP's lower end is one ulp looser; only the upper end matters. |
| SV-21 | `C4` | Margins rounded the wrong way. | NUM | Floors for lower bounds (MINOTAUR ≥ 3.162848e-3; ANTIGONE ≥ 1.552321e-4; QPLIB_3177 shift ≥ 8.6e-5; QPLIB_2703/3177 deficits ≥ 8.15e-6 and ≥ 3.27e-5; SCIP 9.2.1 deficit ≥ 5.458882e-2); ceilings for upper bounds ("cannot lie more than 6.1e-7 and 2.4e-6 below" for camshape100/200 at ε = 1e-10). |
| SV-22 | `C10` | SCIP 9.2.1 input file. | WORD | It read `QPLIB_2703.lp.gz`; equality with the .gms copy assumed (harmless at a 5.46e-2 margin). |
| SV-23 | `C11` | Violation thresholds. | NUM | "more than 2.5e-8" (ANTIGONE), "more than 8e-9" (MINOTAUR). |
| SV-24 | `C12` | "Eight code bases agree". | WORD | "each witness is confirmed by six to eight independent exact checkers". |
| SV-25 | `C13` | Missing script names. | DOC | Rename to `pattern_scan.py/.log`; save the inline claims script. |
| SV-26 | `A8` | Notation. | PROOF | U_m(c/2) in Proposition 3. |

### 4.13 pattern-theory (PT)

| ID | sources | issue | cat | resolution |
|---|---|---|---|---|
| PT-01 | PT-1; `C11`; `X6` | Two meanings of "open". | WORD | G-04. Funnel 1633 → 1257 → 596 → 360 → 294 → 155 → 29 closed, with selection caveats (first wave post hoc; later targets ranked by tractability). relgap = 0 if p = d, else ∞ if signs differ or one value is 0. |
| PT-02 | PT-2; `C8`, `C9`; `X4` | Thesis "relaxation, not branching" untested. | WORD | "The decisive ingredient was a bounding argument adapted to the structure; branching was absent in 12 closures, at most 3-D in 15, and small or confined to the 7 original variables in the rest; in our reading (not tested) termwise relaxations were held back by free variables, nonconvex equality chains, hidden convexity or monotonicity, and cancellation." powerflow0039: SCIP and GUROBI rank the formulations in opposite orders. No experiment (C-51: skip). |
| PT-03 | PT-3; `C12`; `X5` | Pattern sentence overstates. | WORD | Taxonomy: 15 staged splits (6 of the 14 closed families), 4 chain comparisons, 3 Lagrangians over ≤ 5 dense rows, 5 global duality/convexity certificates, 1 identity, 3 Taylor-model B&B. Where an affine split cannot be exact: a richer class (quadratic, field-type, concave chord minorants) or a small exact window (lukvle10 tail, chain end values). Replace the summary's "What the pattern shows" sentence. |
| PT-04 | PT-4 | catmix rests on Lemma 1′, not Lemma 1. | PROOF | State Lemma 1′ (two-line proof); staged certificates rest on Lemma 1, Lemma 1′ and Propositions 3–4. |
| PT-05 | PT-5 | Superseded statements. | DOC | G-08. |
| PT-06 | PT-6; `C17` | Extended-value restatements unreviewed. | DOC | If included, one confirmation pass of 2–4 reviewer-hours naming Consequence 3, Remark 2, Lemma 1′ and the extended-value proofs of Theorems 5–6. |
| PT-07 | PT-7; `C1` | Census artifacts. | WORD | fct missing: 295 candidates over the full library (open count stays 155). chain's census nonlinear-primal width 2N+1 is an artifact (true value 1). Widths are heuristic upper bounds (splitting only at top-level sums). No census rerun (C-52: skip). |
| PT-08 | PT-8 | Single-tree lower bounds concern a synthetic family. | WORD | At most one paragraph as a companion result; not a theorem of this paper. |
| PT-09 | PT-9 | Proposition 8 vs camshape cell DP. | WORD | "consistent with", never "explained by". |
| PT-10 | PT-10 | Solver-log evidence includes degraded runs. | WORD | Label overloaded, memory-limit and tightened rows. Reruns not recommended (C-50: skip; user decision). |
| PT-11 | PT-11 | "At most four continuous dimensions" false. | WORD | Use the branching table: none in 12, 1–3-D in 15, the 9-box concavity proof for pindyck, the 7-variable space for eg. |
| PT-12 | PT-12 | "Reviewed, rechecked and confirmed". | WORD | Attach it to the theorem citation; the link to instances is interpretation. |
| PT-13 | PT-13; `C14`; `X3` | optcdeg2 "no affine function in the band". | WORD | "The costate-affine split cannot be exact on the u = −0.2 arcs; a quadratic split closes the gap to 9.0e-16." Cite calibration note Proposition 4.1 with its hypotheses instead of a new conditional. |
| PT-14 | `C2`, `C3`, `C16` | Proof gaps. | PROOF | Pinch regularity: V_τ and Γ_τ semiconcave. Proposition 4 Remark 2: assume b_t > −∞; finite potentials p_t(D) = min(d_t(D), M_t). Lemma 1: F_t on R^{d_t} or K′_t ⊆ dom F_t; "affine splits are the case …". |
| PT-15 | `C4`, `C5`, `C6` | Counts and quotations. | WORD | 1,564 + 4 (G-05); FAQ quote from `vigerske2026-minlplib-a-library-of-mixed`; recheck verdict "Fixes needed, all small; no proof is wrong." |
| PT-16 | `C7`, `C10` | Attributions. | WORD | lnts factor-incidence width is a heuristic bound (h in every separator, handled by monotonicity); lukvle10 box counts belong to the authors' certificate 352.238025369202, not the displayed verifier dual. |
| PT-17 | `C13`, `C15`, `C18` | Hypotheses dropped in claims. | WORD | Theorem 5 "when both sides of the separator are minimized exactly"; Proposition 8 conditions; "only-if needs f* attained"; assumptions refer to the trust-base table (G-06). |
| PT-18 | `X1` | Derived enclosures omitted from the pattern. | WORD | Add "valid enclosures for unbounded states where stage problems need them". |
| PT-19 | `X2` | Where the consistency theorems are published. | OOS | Lead decision (Section 8). Recommended layout: main text Lemma 1, Lemma 1′, Proposition 2(b)(c), Propositions 3–4; one short subsection with Theorem 5 and Proposition 8; Theorem 6 and Proposition 7 in an appendix or cited. |

---

## 5. Numbers the paper displays differently from `R/open-instances-summary.md`

"Checked" = independently checked by a second party (critic, verifier or
reviewer) or by exact arithmetic in this register. Rows N-01 to N-06 depend on
lead decisions L1 and L2, whose formal review is still planned.

| # | instance / place | quantity | summary (old) | paper (new) | basis | checked |
|---|---|---|---|---|---|---|
| N-01 | lnts50 | dual / primal / gap | 0.5546687649381 / 0.5546687649387 / ≤ 5.79e-13 | 0.5546687649386788 / 0.5546687649386789 / 0 (attained) | Theorem 3; enclosure [0.55466876493867889862209…015, …016] | yes: critic `thm3_iv.py`; 60-digit primal enclosures agree to 3.5e-58 |
| N-02 | lnts100 | same | 0.5545954011663 / 0.5545954011670 / ≤ 6.12e-13 | 0.5545954011669111 / 0.5545954011669112 / 0 | Theorem 3; [0.554595401166911161001782…226, …227] | yes (as N-01) |
| N-03 | lnts200 | same | 0.5545770161025 / 0.5545770161031 / ≤ 5.84e-13 | 0.5545770161030836 / 0.5545770161030837 / 0 | Theorem 3; [0.554577016103083672055625…005, …006] | yes (as N-01) |
| N-04 | lnts400 | same | 0.5545724137001 / 0.5545724137007 / ≤ 5.88e-13 | 0.5545724137006871 / 0.5545724137006872 / 0 | Theorem 3; [0.554572413700687108817391…456, …457] | yes (as N-01) |
| N-05 | dtoc5 | dual / primal / gap | 5.38967211918114 / 5.389672119181141 / ≤ 4.7e-16 | 5.3896721191811404674 / 5.3896721191811404675 / ≤ 7.3e-43 (certificate ends) | exact-rational certificate (`dtoc5_checks.log`: d ≥ …1868831312689, f = …1868831313409) | yes: critic two-route recomputation (gap 7.205e-43) |
| N-06 | lukvle10 | primal / gap | 352.2380254064961 / ≤ 1.5e-9 | 352.2380254064957 / ≤ 1.42e-9 (4.03e-12 rel.) | f(x*) ≤ 352.23802540649562264 (primal track) | yes: primal review r1; critic |
| N-07 | lnts50 (text) | listed relative gap | 3.9e-5 | 3.9e-5 (unchanged; the dossier's 3.8e-5 is wrong) | exact 3.8248e-5 | yes |
| N-08 | ex6_2_5 | primal display | −70.752077833447705 | −70.75207783344770558 (gap cell ≤ 2.1e-15 unchanged) | objective enclosure [−70.7520778334477055803671…] | yes: critic exact check (display difference 2.01e-15) |
| N-09 | etamac | dual display | −15.294675643368093 | −15.29467564336809217 | certified −15.2946756433680921685 | yes: critic exact check |
| N-10 | etamac | primal display | "exactly feasible point" | −15.29467564336808959 (gap cell ≤ 2.6e-15; exact 2.5765e-15) | dossier exact point from saved authors' decisions | yes: critic exact check (display difference 2.58e-15) |
| N-11 | pricing050 (max) | primal / gap | −1813.8290784519731 / ≤ 4.23e-14 | −1813.8290784519730769 (exact) / ≤ 1.92e-14 | saved authors' point, exactly feasible; upper bound −1813.8290784519730577 | yes: critic reran `pricing_check.py` and read it |
| N-12 | pindyck | dual / primal / gap | −1170.4862854360886163932 / −1170.486285436088562 / ≤ 5.44e-14 | −1170.486285436088562087577425069306 / −1170.486285436088562087577425069288 / ≤ 1.8e-29 | Theorem 6 (strong concavity, μ = 0.001; ‖g‖²/(2μ) ≤ 1.69945e-29) | yes: critic re-derived; authors' enclosure gives < 6e-29. Adoption recommended, lead to confirm |
| N-13 | chain50 | dual / primal / gap | range "5.06862 … 5.07226" / "within 1.01e-14" / ≤ 1.01e-14 | 5.0722614939828627 / 5.0722614939828723165 / ≤ 9.62e-15 | per-instance safe displays (dossier §5) | yes: critic recomputed every display and gap exactly |
| N-14 | chain100 | same | as N-13 | 5.0697846107387505 / 5.0697846107387605575 / ≤ 1.01e-14 | same | yes |
| N-15 | chain200 | same | as N-13 | 5.0689173417931616 / 5.0689173417931710002 / ≤ 9.41e-15 | same | yes |
| N-16 | chain400 | same | as N-13 | 5.068621694604009 / 5.0686216946040190144 / ≤ 1.01e-14 | same | yes |
| N-17 | catmix100 | dual / primal | range "−0.04806944 … −0.04805591" (authors' weaker duals) / "improved primal points" | −0.048069432031144562 / −0.0480694320309595629 (gap ≤ 1.85e-13 unchanged) | verifier config B dual; 60-digit enclosure end | yes: critic; `exact_display_checks.json` |
| N-18 | catmix200 | same | as N-17 | −0.048059145599072769 / −0.0480591455801143935 (≤ 1.90e-11) | verifier config A | yes |
| N-19 | catmix400 | same | as N-17 | −0.048056547824671288 / −0.0480565477566115548 (≤ 6.81e-11) | recheck dual; exact rational primal | yes |
| N-20 | catmix800 | same | as N-17 | −0.048055901479675652 / −0.0480559013312308003 (≤ 1.49e-10) | recheck dual; verifier DP-policy point | yes |
| N-21 | catmix (text) | GAMS-model gaps (new statement) | "no exact transport" (READINESS) | ≤ 1.86e-13, 1.90e-11, 6.81e-11, 1.49e-10 for c = 9a | Proposition M8; exact primal shifts | yes: critic read M8 and checked shifts |
| N-22 | catmix (mechanism cell) | label | "exact DP on a 1-D projective separator" | "rigorous DP lower bound on an exact 1-D projective reduction" | CC-10 | — |
| N-23 | eg_disc_s | dual display | 5.760539610694994 | 5.760539610694993 (relative gap ≤ 1e-9; 9.9965e-10) | valid under every route | yes: dossier `displays.log`; critic; arithmetic here |
| N-24 | eg_* (verification cells) | assumption text | "under A1/A2" | "Lemma A1 (proved); exp and pow audited" | only after C-01 passes | pending |
| N-25 | eg_* (text) | relative gap precision | "≤ 1e-9 rel." | "≤ 1e-9 (at most 9.997e-10), with the feasible point's objective enclosed exactly" | EG-07 | yes: arithmetic here |
| N-26 | ann_cumene_tanh | wave-3 gap | "(wave 3: ≤ 20%)" | omit from the table, or "19.07% of \|primal\|" | AK-06 | yes: critic exact 0.19068 |
| N-27 | camshape400/800 p2 (text) | deficit explanation | "8e-6 and 3e-5 below …, chain amplifies violations up to about 600-fold" | "at least 8.15e-6 and 3.27e-5 below; violations of size ε lower the objective by at most D_n(ε) (≤ 2.81e-5 for n = 400, ≤ 1.13e-4 for n = 800 at ε = 3e-10); explicit points reach about 87% of this bound" | CS-05 | yes: camshape check, solvers check, critic third implementation |
| N-28 | lnts50 p1 (text, new) | artifact | not listed | p1 (row violation 9.1e-10) lies 4.30e-11 below the optimum | LL-04 | yes: PP-5, critic |
| N-29 | emfl050_3_3 (text) | listed primal shortfall | "at least 1.42e-5 absolute, 1.36e-6 relative" | "at least 1.41e-5 absolute (1.36e-6 relative)" | evaluated p2: L − obj = 1.41970e-5 | yes: dossier and critic |
| N-30 | rocket100/200/400 (text) | margins | "by 1.1e-7, 4.7e-8, 1.9e-7" | "by at least 1.06e-7, 4.7e-8, 1.89e-7" | `safe_margins.log` | yes: critic |
| N-31 | audit (text) | count | "19 listed solver dual bounds on 15 instances" | add "(15 distinct numerical conflicts)" | AUD-9 | yes |
| N-32 | solvers (text) | BARON camshape100/200 | "optimality claims contradict the proved optimum intervals" | valid duals within 1.23e-7 and 4.80e-7 relative; claims not attainable under exact feasibility | SV-01 | yes: arithmetic here (1.2273e-7, 4.7977e-7) |
| N-33 | lnts (text) | gap explanation | "against N·h2 the gaps are at most 5.55e-13" | delete (gap 0 by Theorem 3) | L1 | — |
| N-34 | eg_disc_s (text) | display paragraph | "display … is 2.4e-16 above the certifier's binary64 bound; valid because …" | delete | N-23 | — |
| N-35 | camshape800 (literature table) | prior-work label | "Prior global claim false (rigorously for the MINLPLib model; …)" | "prior global claim on the rounded copy at a value not exactly attainable; first exact optimum" | CS-08 | — |
| N-36 | pattern (text) | candidate count | 294 (dossier funnel) | 294 (scout set), 295 over the full library including fct; open count 155 | PT-07 | yes: critic |
| N-37 | KAN (text, dossier) | r5_n5 relative gap | 3.73e-10 (dossier) | 3.74e-10 | AK-06 | yes: arithmetic here |
| N-38 | solvers (text) | CAMINO margins | 7.5%, 81% | 7.48%, 80.6%; absolute ≥ 0.2445944, 0.4312902, 5.2010558 | SV-09 | yes: critic `margins_floor.log` |
| N-39 | waterno2_18 / waterno2_24 (reproduction text) | regenerated bounds | not mentioned | `certify.py` regeneration gives 4790.820086219 and 6576.150434342 (valid, weaker); stated values 4790.820715 and 6576.151388 unchanged | WN-01 | yes: reproduction track logs, critic |

Unchanged: optcdeg2, camshape duals, hvycrash, ex6_2_7, powerflow (never
41869.05148327244), waterno2 duals and primals, ann_cumene_tanh main row,
KAN gaps.

---

## 6. Proposed computations: cost and recommendation

Rule applied: avoid new computational experiments unless important. Review
reruns of existing certificates count as verification, not experiments.

| # | computation | sources | cost | recommendation | reason |
|---|---|---|---|---|---|
| C-01 | eg: exp- and pow-audited rerun of route R on all leaves of all three instances, including regenerated recordings and coverage checks | L4; eg-2, eg-7, eg-crit-1, `C1`, `C6`, `C11` | 4.3–6.4 CPU-h with an fexp-type auditor (2.2–3.2 h wall on 2 cores; about 2.5× under load); 6.8–8.9 CPU-h with an IEEE-only interval auditor; pow audit ≈ 0.1 ms/piece; development 1–2 h, plus a few hours for a fresh independent auditor | do (lead decision; in preparation) | Removes A2 and the pow hypothesis from the only proof that covers all three eg instances. |
| C-02 | lnts Theorem 3: rerun of the 1-D sign check in the independent review | L1; lnts-exact-optimum | seconds; 1–2 h reading | do (review) | Already reimplemented by the critic; the planned review should rerun one implementation. |
| C-03 | dtoc5 exact certificate: review rerun | L2; DO-1 | 2.6 s; < 1 h reading | do (review) | Same as C-02. |
| C-04 | lukvle10 Krawczyk/exclusion refinement | lukvle10-refinement-optional | ≈ 1 person-day; < 15 CPU-min | skip | L6. |
| C-05 | lukvle10 B&B rerun with integer-only exp/log | lukvle10-mpmath-dependency | ≈ 0.5 day; 6–11 CPU-min | skip | L6: mpmath iv stated as trusted. |
| C-06 | lnts100/200/400 p1 comparison | lnts400-p1-check | seconds | skip (done in PP-5) | Resolved (J-04). |
| C-07 | Second exact optcdeg2 stage-minimization implementation | DO-4 | ≈ 0.5 day; < 1 min | skip | Interval bound, falsification search and all-stage exact losses already support it. |
| C-08 | Polish optcdeg2 KKT data at stages 3092 and 47291 | DO-11, `A1` | 1–2 h; < 1 min | skip | Relative gap already 3.1e-18. |
| C-09 | Proof that every optcdeg2 minimizer is bang-bang to 5.2e-9 on the middle arc | `A3` | ≈ 1 h; seconds | optional | Only if the paper discusses the optimal control structure. |
| C-10 | Fetch QPLIB_3177.nl and run the exact check | camshape-I6 | hours (an .nl reader); availability unknown | skip | After reframing (CS-08) no claim depends on it. |
| C-11 | Rational cos/π bounds for the COPS-constant enclosure | camshape-I7 | minutes | skip | State the mpmath qualifier or omit the COPS precision statement. |
| C-12 | camshape multiplier mass ‖λ‖₁ | PP-10 | minutes | skip | D_n(ε) already gives the rigorous statement. |
| C-13 | catmix: authors' code on the recheck grids | CC-2 | ≈ 5 h | skip | Would not certify the stated values (J-10). |
| C-14 | catmix: rerun with per-stage w saved and a target-driven second check | CC-12, chain-catmix `A2` | ≈ 2.6 h + 1–2 h coding + 20–70 min/instance | skip | Single-implementation status is disclosed (CC-02); gaps are already ≤ 1.5e-10. |
| C-15 | chain 2-D B&B in a third arithmetic (Arb) | CC-3 | 1–2 h coding; < 5 min | skip | mpmath iv listed as trusted; two implementations exist. |
| C-16 | `gibbs_cert.py`: componentwise R_p assert, vapour-form check, rerun both ex6_2_* cases | small-gibbs-single-implementation; gibbs-cert-asserts | minutes of coding; ≈ 5 CPU-min | optional | Needed only to call the dossier code a fully independent second implementation. |
| C-17 | Independent etamac rebuild | small-etamac-single-implementation | 3–5 h; < 1 min | skip | Provenance disclosed; weaker two-code bound gives gap 6.5e-15 if needed. |
| C-18 | Rerun `v_etamac.py`/`v_pricing050.py` with point dumps | small-unsaved-verifier-points | ≈ 15 min patching; ≈ 50 s | skip | Saved authors' points give the stated gaps (SM-01, SM-05). |
| C-19 | Symbolic check of the pindyck Hessian recursion | small-pindyck-hessian-map-hand-derived | < 1 h; seconds | skip | Two derivations and numerical checks exist. |
| C-20 | eg S-F rerun of run G parts 0, 2–7 with explicit products | eg-crit-1 | ≈ 3 CPU-h (≈ 1.5 h wall on 2 cores) | skip | Superseded by C-01. |
| C-21 | eg S-I part-1 replay under the guard | eg-crit-2 | ≈ 1.6 CPU-h | skip | Side condition stated; part 1 also certified by S-F and R. |
| C-22 | eg S-I replay of parts 0, 2–7 | eg option (g) | 11–23 CPU-h | skip | Superseded by C-01. |
| C-23 | eg: extend r1's outward-rounded certifier to all leaves | eg-crit-3 | ≈ 50 CPU-h | skip | Not competitive; may fail without the LP. |
| C-24 | powerflow angle-free 0039p replay | PF-3 | 9 s | skip (done by critic) | Resolved (J-18). |
| C-25 | powerflow 0030p SDP re-solve for regenerability | PF-6 | 5–20 s + replay | skip | Certificates are replayed from stored files. |
| C-26 | powerflow rigorous primal SDP (0039 Shor gap) | PF-9 | ≈ 0.5 day; seconds | skip | No claim needs it. |
| C-27 | powerflow `gms_vs_osil.py` reviewer rerun | PF-14 | seconds | optional | Fold into the final review if "exact term-by-term" is stated. |
| C-28 | waterno2_18/24 fixed-target or `certify.py` reruns | W1, `A2` | 6–9 CPU-h | skip | L5: document only. |
| C-29 | waterno2 per-leaf proof data and exact checker | W1 | days of coding + 25–60 CPU-h + checker of uncertain cost | skip | Two B&B lines already agree. |
| C-30 | waterno2 exact-propagation replay | W2 | ≈ 60–120 CPU-h | skip | Not needed. |
| C-31 | Separator branching / cell slopes for waterno2_09–24 | W9 | hundreds of CPU-h, no target guarantee | skip | Out of scope. |
| C-32 | KAN rigorous-exp rerun | I1 | 55 CPU-min | skip (done) | L3 adopts the existing rerun. |
| C-33 | Regenerate ANN re-certification region lists | I2, `A4` | ≈ 2 h one core + ≈ 2.6 CPU-h verify (≈ 1.3 h wall on 2 cores) | optional (release artifact only) | The review's verdict stands; document the procedure. |
| C-34 | Download the seven ANN/KAN .gms files and compare exactly | I11 | minutes (network) | optional | Only to state the results for the GAMS form. |
| C-35 | Third-party reading of `kan_bnb.py`; r3_n5 soundness sampling | I13 | ≈ 0.5 day; minutes | skip | L is valid if either path is correct; shared parts disclosed. |
| C-36 | Close the ANN gap (second-order models, SOSC) | I10 | research task | skip | Out of scope. |
| C-37 | Primal points under binary64 data | PP-1 | seconds (dtoc5, chain); ≈ 1 h (powerflow) | skip | G-01 claims nothing for binary64 data. |
| C-38 | Dyadic re-proofs of the mpmath-only primal claims | PP-3 | 1–2 h scripting each | skip | mpmath iv stated in the trust base. |
| C-39 | Save the pricing050 verifier point vector | PP-3 | small patch; < 1 min | skip | The saved authors' point is used. |
| C-40 | Regenerate topopt certificate with basis and exact c_e; save emfl rational y | AUD-5 | seconds to minutes | optional (release artifact only) | Claims unaffected. |
| C-41 | All-rational Krawczyk for ghg_3veh and nuclear14 | AUD-6 | < 1 h work; seconds to tens of minutes | skip | Assumptions disclosed. |
| C-42 | oil reduced-system existence proof | AUD-8 | several hours; uncertain | skip | Could add two pairs; not needed. |
| C-43 | stockcycle exact .gms/OSIL comparison | `CRIT-A3` | < 1 h; seconds | skip | State the limit. |
| C-44 | Reviewer rerun of `D/checks/audit/` and `D/checks/audit-r2/` (GAMS/OSIL identity, rocket second proof, aggregate rule) | AUD-3, AUD-4, AUD-15 | minutes | do (review) | Needed if the paper relies on AUD-3, AUD-4 or AUD-13. |
| C-45 | BARON 26.5.28 reruns of camshape100/200 | S8 | < 1 min solver time; authorization | skip | Versions stated. |
| C-46 | SCIP source-level fix and 122-case scan | S14 | a few hours on 2 cores | skip | The developers' task once filed. |
| C-47 | fm336/tiny2 with L = 0.6 or 0.85 on four SCIP versions | solvers `A2` | minutes; solver-run authorization | optional | Cheap falsification test of the mechanism; only if the upstream report or the paper's mechanism paragraph needs it. |
| C-48 | rbb on pair 2236 near the low SCIP claims | S15 | minutes | skip | No claim depends on it. |
| C-49 | SCIP 10.1.0 on waterno2_03/04 | S18 | ≈ 2 × 1 h; authorization | skip | Cannot answer the question (J-34). |
| C-50 | Rerun 10 overloaded and 3 memory-limited campaign runs | PT-10; READINESS decision 2 | 13 one-hour single-thread runs | skip | Rows labelled; no speed claim. |
| C-51 | Solver runs with certified bounds added; camshape in u = 1/r | PT-2, `X4` | 7–14 CPU-h; authorization | skip | Cannot separate relaxation from branching. |
| C-52 | Corrected census | PT-7 | minutes | skip | No claim needs it. |
| C-53 | Dual-side data-reading confirmation by code reading | `CR-A4` | 10–20 min per family | do (review) | Grep-level check done here (K6); a reviewer should confirm before the paper states zero and sub-1e-16 gaps as reading-(b) results. |
| C-54 | Review of dossier scripts the paper cites as proofs (`dtoc5_checks.py`, `optcdeg2_primal_int.py`, `eg_dyadic_check.py`, `ex62_check.py`, catmix400 exact rerun, `pricing_check.py`, `pindyck_sc.py`, camshape `check_exact.py`/`check_gms.py`, powerflow `r2/` scripts) | PP `C14`; camshape-I5; DO-1 | 1–2 h reading each; seconds to minutes of compute | do (review) for the scripts actually cited | Several dossier scripts become primary evidence; each needs one review before citation. |

---

## 7. Cheap checks run for this register

All checks were inline, read-only Python on files in place (no project
scripts were executed) or `grep`, on one core.

| # | check | result |
|---|---|---|
| K1 | `R/bound-audit/pages.json`: instance-list dual vs per-solver entries, half-unit display rounding | 1,633 pages; 1,576 list a dual (exactly the pages with ≥ 3 entries counting `inf`); 57 have < 3 entries (23 none, 15 one, 19 two). 8 listings are `inf`. All 1,568 numeric listings equal the third-best entry with `inf` counted; with finite entries only 1,564 match; exceptions ball_mk4_15, chp_shorttermplan2c, nuclear10a, powerflow0057r. 1,571 pages have ≥ 3 finite entries. |
| K2 | Display arithmetic with exact fractions | eg relative gaps 9.9969e-10 (int_s), 9.9965e-10 (disc_s with …993), 9.9957e-10 (disc2_s); lukvle10 352.2380254064957 − 352.2380254050784 = 1.4173e-9 (enclosure ends 1.4172e-9); ex6_2_5 display difference 2.01e-15; etamac 2.58e-15; pricing050 1.92e-14; pindyck 1.8e-29. |
| K3 | Outward binary64 enclosure of fl(L)^k vs fl(L^k) for L ∈ {0.6, 0.7, 0.85} (lower) and 0.8 (upper), k = 2, 3 | Only L = 0.7, k = 3 misses: up(fl(0.7)³) = 0.34299999999999997 < fl(0.343). Confirms solvers `C2`. |
| K4 | lnts p1 objectives vs the Theorem 3 optima | lnts50 −4.30e-11; lnts100 +1.49e-12; lnts200 +2.72e-12; lnts400 +1.49e-11. |
| K5 | `v_lukvle10_bnb.py` incumbent | line 199 `U = hi(prob.point(x0[0], x0[1]))`; confirms J-01. |
| K6 | Dual-code data reading (grep) | camshape `v_camshape.py`: `Fr(...)` of OSIL strings, exact rationals. pindyck review `own_model.py`/`own_psi.py`/`primal_check.py`: `Fr(str)`, `iv.mpf(str)`, outward floats. catmix `v_catmix_model.py`: `Fr` of strings; `v_catmix_dp.py` encloses each Fraction by outward floats. powerflow reviewer `own_osil.py`: Fractions of the decimal strings. waterno2 `vmodel.py`: osilx decimal strings → Fraction. ANN `annx.py` and KAN `kan_bnb.py`: Fractions enclosed by outward floats. eg `indep_cert.py`: `float()` of GAMS decimals, with conversion error covered by Lemma A1 fact F1; GAMS ≡ OSIL exactly. All consistent with reading (b). Grep level only. |
| K7 | BARON camshape relative distances | (−4.28414712174675 − (−4.28414764756144))/4.284… = 1.2273e-7; camshape200 4.7977e-7. |

---

## 8. Decisions still open for the lead author or the user

| # | decision | recommendation |
|---|---|---|
| O-1 | Adopt the pindyck strong-concavity gap (≤ 1.8e-29) in the table (SM-02, N-12) | Adopt: proved, re-derived by the critic, supported by both parties' enclosures, no computation. |
| O-2 | pricing050 gap 1.92e-14 vs the conservative 4.23e-14 (SM-01, N-11) | Adopt 1.92e-14; it removes the summary's special-case footnote. |
| O-3 | Whether the critics' passes count as the independent reviews for Theorem 3 (lnts), the dtoc5 certificate and uniqueness, the QPLIB copy bounds (S3) and Propositions C6/M1/M6/M8 | L1–L3 already plan later reviews; the critics' passes are AI-agent reviews and should be described as such (G-09). |
| O-4 | Placement of the consistency theorems (PT-19) | Layout of PT-19; cite the note instead if it is published separately. |
| O-5 | Optional cheap items C-09, C-16, C-27, C-33, C-34, C-40, C-47 | Run C-16 only if the paper says "two independent implementations" for ex6_2_*; C-47 only with solver-run authorization and only if the SCIP mechanism paragraph needs it. Others are for the release artifact. |
| O-6 | User: file the SCIP upstream report; notify MINLPLib, QPLIB, Mittelmann/MINOTAUR, CAMINO authors | User decision (SV-12). Under L7, BARON's camshape claims are tolerance-level closures, so READINESS's "notify BARON developers about the two contradicted optimality claims" should not be presented as an error report. |
| O-7 | User: solver reruns (READINESS decision 2) | Not recommended (C-50). |
| O-8 | Literature reading before submission: Ghaddar et al. 2015, Carøe–Schultz, Berenguel, Kocuk–Dey–Sun, Coffrin et al., Hansen 1992, the audit-novelty search, Floudas handbook / McDonald–Floudas | Reading only; required before any comparison or priority sentence in those areas (G-07). |
