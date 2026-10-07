# Review of track lit-network (round 1)

Reviewer: independent verifier. Date: 2026-10-01. Cores used: at most 1 at a time.
Scope: the literature check for powerflow0030p/0039p/0039r, the six KAN instances,
waterno2_06–24 and ann_cumene_tanh. I checked the author's on-disk sources
(`publication/literature/network/sources/`, `MANIFEST.md`), the author's two check
scripts, and the report text that the orchestrator passed to me. I re-ran every
substantive numerical claim with my own code, and I ran my own searches. My code, logs and
extra sources are in `publication/reviews/lit-network-r1/`.

**Verdict: issues (3 major, 6 minor).** Most of the facts I could check are correct. I
confirmed the KAN findings independently, and strengthened them. However, the report
misses the decisive prior result for ann_cumene_tanh. It also misstates the provenance of
powerflow0030p, and the full report is not available for review.

## 1. Major issues

### M1. ann_cumene_tanh: missed an exactly equivalent MINLPLib twin that is closed in floating point

MINLPLib has `ann_cumene_exp` ("In this variant of ann_cumene_tanh, the tanh(x)
activation function has been replaced by 1-2/(exp(2x)+1)"). Its page lists these dual
bounds (fetched 2026-10-01; the same values are in the 2026-09-30 copy in
`bound-audit/pages/ann_cumene_exp.html`):

| solver | dual bound for ann_cumene_exp |
|---|---|
| SCIP | −3379.982394 |
| LINDO | −3379.982394 |
| BARON | −3379.985774 |
| ANTIGONE | −73920.54157 |

The primal value is −3379.982394.

My script `lit-network-r1/cumene_twin.py` (own OSIL reader) proves that the two cached
OSIL models are the same problem. They have identical variables, bounds, objective, and
linear and quadratic coefficients, all compared exactly at 60 digits. Each of the 250
nonlinear rows is `negate(tanh(v))` in the tanh model and `2/(exp(2v)+1)` with the same v
in the exp model. Each of these rows has bounds shifted by exactly +1, which is the
identity −tanh(v) = 2/(exp(2v)+1) − 1. The feasible sets are therefore identical in exact
arithmetic.

The report says "MINLPLib lists no dual" and calls our −3386.5403 (gap 0.194%) "new as
far as found". That is not tenable. The identical problem was closed in floating point
by SCIP and LINDO, and BARON is within 3.4e-3. Our bound is the first rigorous one found,
but it is far weaker than these floating-point claims.

Required change: set the status to "partly known". State that the problem was closed in
floating point via the exp twin, and that ours is the first rigorous bound. Flag this
for the paper's ann_cumene_tanh claim and for `open-instances-summary.md`, which also
calls it "the first finite dual". No research note in the repository mentions
`ann_cumene_exp`.

### M2. powerflow0030p: the MINLPLib model is not "MATPOWER case30 plus ±0.26 rad angle rows"; the two bus shunts are dropped

MATPOWER case30 has bus shunts Bs = 0.19 MVAr at bus 5 and 0.04 MVAr at bus 24. In the
MINLPLib GAMS file these terms are missing:

- bus 5: the balance rows `e511.. x58 + x77 =E= 0` and `e535.. x140 + x159 =E= 0` have no
  V² term;
- bus 24: the rows `e527 … =E= -0.087` and `e551 … =E= -0.067` contain only flows.

The author's data-match script compares costs, voltage and generator limits, thermal
limits, taps and line charging. It does not compare loads (Pd, Qd) or shunts (Gs, Bs).

I wrote my own polar AC OPF from the MATPOWER files (`lit-network-r1/opf/opf_gams.py`)
and solved it locally with GAMS IPOPT and CONOPT:

| model | objective (IPOPT / CONOPT) |
|---|---|
| case30 as in MATPOWER | 576.8923368 / 576.8923368 |
| case30 + ±0.26 rad angle rows | 576.8923368 / 576.8923368 |
| case30 without bus shunts | 576.8934134 / 576.8934135 |
| case30 without shunts + angle rows | 576.8934134 / 576.8934134 |
| MINLPLib powerflow0030p p1 (listed) | 576.8934135 |

The MINLPLib model therefore equals MATPOWER case30 without bus shunts, with
non-binding angle rows. Its optimum differs from case30's by about 1.1e-3 (local values).

NESTA Table 1 and Bingane et al. (2018) Table I both report a 0.00% SDP gap with value
576.89. Both runs use the unmodified (shunted) case30, so, as with case39, they concern a
close relative and not the model as written. The status "partly known" can stand.
However, it must rest on the rectangular twin powerflow0030r: MINLPLib lists ANTIGONE
dual 576.8934129 for it, with the same primal 576.8934135 and also no shunt terms in the
OSIL. The NESTA and Bingane results are only a close relative.

Fix the provenance sentence and the claim that "the data match was checked". Also extend
the data-match check to loads and shunts.

### M3. The report is not on disk, and the copy given to the verifier is truncated

`publication/literature/network/report.md` does not exist. The text passed to me stops
in the middle of the summary table ("SDP gap 0.00% for MATPOWER c"). I could therefore
not check:

- the per-instance sections;
- the search log ("what was searched");
- Section 7 (checks) and Section 8 (sources not obtained), except through `MANIFEST.md`;
- the list of commands run.

The root must save the author's full text. Until then, the track's required deliverable
(one section per instance, the summary table, and the commands run) is not verifiable.
I did not write the author's report myself, because I only have the truncated text.

## 2. Minor issues

1. **Source paper of the powerflow instances is obtainable.** MANIFEST.md says only the
   2016 revision of Hijazi–Coffrin–Van Hentenryck (Optimization Online 2013/09/4057) is
   online. The Wayback Machine has the June 2014 revision (snapshot 2015-12-24; PDF
   CreationDate 2014-06-03). This is the version current when MINLPLib added the
   instances (18 Aug 2014). It is saved as
   `lit-network-r1/sources/oo_4057_wayback20151224.pdf`, sha256 `5998d8bc…2aab`.
   - **Section 6, footnote 1, and the setup paragraph.** The experiments use the
     "complete" equations, including transformers and bus shunts, with θu = π/12. The
     MINLPLib GAMS models, which have no taps and no shunts, therefore differ from the
     models solved in the source paper.
   - **Table 3.** For the 30-bus MATPOWER benchmarks (ids 5 and 6): AC 576, SDP gap
     0.00%, QC gap 0.57%. For the 39-bus benchmark (id 8): AC 41864 (the tapped value),
     SDP gap −0.06%. The authors explain the negative gaps as non-valid SDP bounds caused
     by numerical difficulties.
   - **2016 revision.** The current OO PDF (`oo_4057.pdf`) uses NESTA cases only. It is
     not in the author's sources.

   Cite the 2014 revision as the provenance source.
2. **NESTA Table 1 also covers case39.** NESTA (arXiv 1411.0359v6, Table 1) gives case39
   41864.18 with SDP gap 0.00%. Bingane 2018 Table I gives case39 41864.18 / 41862.03.
   These are further floating-point results for the tapped close relative, alongside
   Ghaddar et al. Table 4. Cite them if the full report does not already.
3. **Wording for BARON on cumene.** "BARON produced no finite lower bound in 1e5 s" is
   slightly too strong. Table 4 of Schweidtmann & Mitsos (arXiv v2, p. 21) reports an
   absolute gap of 1·10^20 for all four BARON formulations, and the text says BARON
   "does not improve its initial lower bound … at all". "No useful lower bound (absolute
   gap 1e20)" is accurate. The MAiNGO figure (absolute gap 1·10^5) is for the
   "envelope*" setting; the other reduced-space runs ended at 8e10–1e11.
4. **The author's KAN check is not independent.** `checks/kan_scip_points.py` imports
   the wave-3 certificate code (`kan_check`, `kan_model`). It also assumes that the
   Pyomo inputs x1..xd map to the [−2.048, 2.048] OSIL variables in index order. I
   reproduced the numbers with independent code and confirmed the order assumption
   (Section 3.1).
5. **Huang (2019) is unread.** The TU Darmstadt dissertation (tuprints 8657) uses "two
   real-world instances provided by Siemens and another from … Tsinghua University"
   (catalogue abstract via web search). It may contain multi-period results on the
   waterno2 network. Every fetch I tried also hit the Anubis bot check (tuprints and the
   hebis catalogue). The waterno2 claim of "new as far as found" must name this gap
   explicitly. A person with a browser can download the CC BY-SA PDF.
6. **Wording for powerflow0030p.** "The first bound on the polar instance as listed" is
   ambiguous, since MINLPLib lists a GUROBI dual of 572.84 for 0030p. Say "the first
   bound that closes the gap on the polar instance as listed".

## 3. What I verified independently (with my own code)

### 3.1 KAN: the published SCIP "optima" are below our certified minimum of R, and are tolerance artifacts

- **Model identity.** The SCIP logs report 1129/1410/2534/838/1392/2223 variables
  (288/360/648/216/360/576 integer) and 1478/1847/3323/1121/1867/2986 constraints. These
  equal the cached OSIL counts.
- **Zenodo files.** All match the md5 sums in the Zenodo metadata. I read the xlsx files
  with my own zip/XML reader (`zenodo_xlsx_check.log`).
- **Default runs.** The values are as the author states:
  - kan_r3_h1_n4: optimal 1.08116412047821e-3 (3459 s);
  - kan_r3_h1_n5: −1.30809958982354e-2 (5038 s);
  - all other runs hit 7200 s.
- **Other formulations.** For n4 there are five further "optimal" values (7.98e-4 to
  1.064e-3). For n5 there are four (−0.013476 to −0.012561), and Redundant hit the time
  limit. All are below our bounds 0.0027812371525814 and −0.011042679521782.
- **Best duals over the six formulations.** −11.376 (n9), −1587.43 (r5_n3), 0.18669
  (r5_n5), −122.67 (r5_n8). All correct.
- **Paper.** Table 5 of arXiv 2503.02807v1 (fros n0 = 3: n1 = 4 → 3459 s, n1 = 5 → 5038 s;
  n0 = 5: 7200 s) confirms the times. Section 4.1 states SCIP 9.0.1 with gap tolerance
  zero and a 2 h limit.

**Network value at SCIP's inputs.** `lit-network-r1/kan_points.py` uses my own OSIL
reader and forward propagation at 60 digits. It never uses the partition rows, and every
other row holds to ≤ 1.2e-60.

| instance, run | network value at SCIP input | SCIP's value |
|---|---|---|
| kan_r3_h1_n4, Default | 0.00286847844485 | 1.08116e-3 |
| kan_r3_h1_n5, Default | −0.0108512435423 | −0.0130810 |
| kan_r5_h1_n5, ConvexHull | 0.272924297379 | 0.2725188 |
| kan_r3_h1_n4, ConvexHull (extra) | 0.00282696148 | 7.98e-4 |

The first three rows match the author's numbers to all printed digits. The partition rows
are violated by at most 2.5e-15.

**Model identity and input order.** At time-limited runs, where SCIP's primal is far from
the optimum, the network matches SCIP to about 1e-6:

| run | network value | SCIP's value |
|---|---|---|
| n9 Default | 9.55677956 | 9.55678095 |
| r5_n8 Default | 185.1199968 | 185.1199956 |
| r5_n8 ConvexHull | 0.21407732 | 0.21407515 |

Every other ordering of the inputs gives values that differ by 2 to 2000
(`kan_points_perm.log`).

**New, stronger evidence (`kan_scip_fixed.py`).** I ran SCIP 10.0 (pyscipopt 6.2.1, one
thread) on the cached MINLPLib OSIL with the three inputs fixed at SCIP 9's reported
optimal point. In exact arithmetic everything else is then determined. SCIP 10 returns:

| instance | SCIP 10 "optimal" value | exact network value | largest row violation | rows violated > 1e-9 |
|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0026959290 | 0.0028684784 | 9.3e-7 | 38 |
| kan_r3_h1_n5 | −0.0113202912 | −0.0108512435 | 1.0e-6 | 90 |

Both SCIP 10 values are also below our certified minimum of R. I measured the row
violations with my evaluator. This directly shows, on the MINLPLib model itself, that
1e-6 row tolerance moves the objective by more than our certified gap. I recommend using
it in the paper together with the Zenodo comparison.

### 3.2 Power flow

- **powerflow0039p/r: taps dropped.** This is confirmed independently. My AC OPF gives
  41864.17779 for MATPOWER case39 with taps (IPOPT and CONOPT). This matches NESTA
  41864.18 and Ghaddar et al. 41864.18.
- **Without taps** it gives 41869.05151 (IPOPT 41869.0515108, CONOPT 41869.0515113),
  equal to MINLPLib p1 (41869.05151) and to our certified bounds. The ±0.26 rad rows do
  not change the value.
- **Spot check in the GAMS file.** Branch 2–30 (x = 0.0181, τ = 1.025) appears as
  `55.2486187845304` (= 1/0.0181) on both ends, in rows e64, e65, e156 and e157.
- **case39 has no bus shunts.** So for 0039 the only data differences from MATPOWER are
  the taps and the added angle rows.
- **Ghaddar–Mareček–Mevissen.** arXiv 1404.3626v3, Table 4: case39, MATPOWER 41864.18,
  [OP4-SH1] bound 41864.18. Correct.
- **NESTA Table 1** (case30 576.89, SDP 0.00) and **Bingane 2018 Table I** (case30
  576.89 / 576.89, SDR 0.00%) are correct as quoted, apart from M2.
- **MINLPLib powerflow0030r.** ANTIGONE dual 576.8934129, primal 576.8934135. Correct.

### 3.3 Water networks

- **ZIB-Report 12-25** (the preprint of the NACO 2012 paper). It covers stationary
  models only, of networks n25p22a18 (4 tanks, 12 pumps) and n88p64a64 (11 tanks, 55
  pumps). The pumps are fixed-speed and SCIP 2.1.1 solves them to ε-optimality. The
  waterno2 network has 3 tanks and 9 variable-speed pumps (wave-2 notes), so "two other
  networks" is consistent.
- **D'Ambrosio et al. 2015** (EJOR 243(3), postprint). Section 5.2 says: "To the best of
  our knowledge, there is no successful solution for this complete form in the
  literature". It also says that going to "only two or three time periods is
  troublesome" for SCIP, citing [27], Gleixner private communication (2013). Both are
  quoted correctly.
- **MINLPLib waterno2_06.** The best listed dual is 165.19 (SCIP). The page cites Huang
  (2011) and Gleixner et al. (2012). Correct.

### 3.4 ANN

- **Schweidtmann & Mitsos.** arXiv 1801.07114v2, Section 5.4 and Table 4: the
  full-space problem has 794 variables, 789 equalities and 1 inequality, which equals
  the MINLPLib counts (794 variables; 790 rows: 789 E, 1 L). BARON abs. gap is 1e20 for
  all formulations. "Presented solver (envelope)*" (MAiNGO) has abs. gap 1·10^5 after
  10^5 s. Correct, apart from the wording in minor issue 3.
- **The 2026 ESCAPE paper** (Izquierdo González et al., LAPSE 2026.0427) trains a new
  ANN (five hidden layers 16→32→32→32→16), so it is not the MINLPLib model. Correct.

## 4. Searches I ran

- **KAN.** "Karia Lastrucci Schweidtmann KAN deterministic global optimization journal
  2025"; "global optimization trained Kolmogorov-Arnold network MINLP … 2025 2026";
  instance names kan_r5_h1_n8 / kan_r3_h1_n4 / kan_r3_h1_n9; "optimization over trained
  KAN … 2026 arXiv". No further result on these networks. Two items were irrelevant:
  LAPSE 2026.0448 (DKL-KAN for Bayesian optimization) and arXiv 2604.03871 (polynomial
  KANs, different networks).
- **Power flow.** The Hijazi–Coffrin–Van Hentenryck QC paper (found the 2014 revision;
  minor issue 1); "Proving global optimality of ACOPF solutions" (Gopinath et al. 2020,
  PGLib/NESTA cases, not the MATPOWER data as written); instance names
  powerflow0039p/0030p/0039r (no hits).
- **Water.** Huang 2011 thesis (not found online); Huang 2019 dissertation (blocked);
  OpenAlex (no record); "waterno2 … dual bound" (only MINLPLib pages).
- **ANN.** "cumene … MAiNGO reduced space … follow-up"; "ann_cumene_tanh OR ann_cumene
  minlplib". This search led to M1.

Searches that found nothing do not prove that nothing exists.

## 5. Commands run (all from `publication/reviews/lit-network-r1/` unless stated)

| command | outcome |
|---|---|
| `ls`, `cat` of the track folder, `MANIFEST.md`, `checks/*.py`, `checks/*.log` | report.md missing; checks read |
| `grep`/`sed` on the source `.txt` files (Karia, NESTA, Bingane, Ghaddar, MERL, ZIB 12-25, D'Ambrosio, Schweidtmann, Izquierdo, Vigerske, Geißler, arXiv 2604.03871) | facts in Section 3 confirmed at the stated locations |
| `grep` of SCIP logs, `head`/`tail`, results JSON | counts and statuses as in Section 3.1 |
| `awk` over `r3/r5-opt-overview.tsv`; own xlsx reader → `zenodo_xlsx_check.log` | values as in Section 3.1 |
| `md5sum` of Zenodo files vs. `zenodo_14961066.json` | all match |
| `python3 kan_points.py` → `kan_points.log` (7.6 s) | Section 3.1 table |
| `python3 kan_points.py perm` → `kan_points_perm.log` | only the identity order matches SCIP |
| `python3 kan_scip_fixed.py kan_r3_h1_n4` and `… kan_r3_h1_n5` → `kan_scip_fixed.log` | SCIP 10.0 "optimal" 0.0026959 / −0.0113203; violations up to 1e-6 |
| `python3 opf/opf_gams.py case30 [ang026] [noshunt]`, `case39 [notap] [ang026]` → `opf/opf.log` (GAMS 54.3, IPOPT and CONOPT, threads=1) | Section 3.2 and M2 |
| `grep` on `minlplib_powerflow0030p.gms` (balance rows, angle rows), `powerflow0039p.gms` (55.2486…) | shunts absent; taps absent |
| `python3 cumene_twin.py` → `cumene_twin.log` | ann_cumene_exp ≡ ann_cumene_tanh (M1) |
| `curl` minlplib.org/ann_cumene_exp.html; Optimization Online 4057 page and PDF; archive.org availability API and Wayback PDF; tuprints and hebis (bot pages, deleted); OpenAlex API | sources saved in `lit-network-r1/sources/` |
| WebSearch (8 queries, Section 4); WebFetch of tuprints 8657 (blocked) | Section 4 |

Saved sources (`lit-network-r1/sources/`, fetched 2026-10-01, sha256):

- `minlplib_ann_cumene_exp.html` `33fa04a3…02f3`
- `oo_4057.html` `16c34191…4a60`
- `oo_4057.pdf` (2016 revision) `c28325ab…cf93`
- `oo_4057_wayback20151224.pdf` (2014 revision) `5998d8bc…2aab`
- `.txt` files: `pdftotext -layout` output of the two PDFs

All results above that come from GAMS, IPOPT, CONOPT or SCIP are floating-point
evidence, not proofs. The exact facts are the structural ones: the equivalence of the
cumene twins, the missing shunt terms, and the untapped admittances in the GAMS files.
The 60-digit KAN evaluations are high-precision numerical evaluations. The conclusion
drawn from them (differences of 4e-4 to 2e-3, against partition-row violations of
2.5e-15) does not depend on rounding.
