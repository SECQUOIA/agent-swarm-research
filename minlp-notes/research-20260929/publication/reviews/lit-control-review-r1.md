<!-- Written to disk by the root from the structured return value of verifier round 1 of track lit-control in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review: lit-control literature check, round 1

Reviewer: independent verifier, lit-control, round 1. This is the third attempt; two earlier verifiers were interrupted by usage limits. I read their transcripts and reused their leads, but I re-fetched every source and reran every check myself.

Report reviewed: `/workspace/minlp-notes/research-20260929/publication/literature/control/report.md`

My code, data and logs: `/workspace/minlp-notes/research-20260929/publication/reviews/lit-control-r1/` (`PROGRESS.json`, `web/` with fetched pages, logs and `SHA256SUMS.txt`, `gms/` with GAMS checks, `osil_lq.py`, `qplib_read.py`, `camshape_qplib_vs_minlplib.py`).

## Verdict: issues (2 major, 9 minor, no blocker)

Most facts the report states are correct at their stated locations, and its floating-point provenance checks reproduce with my own code. However, it missed two sources that change several of its conclusions.

- **Mittelmann's Continuous Non-Convex QPLIB Benchmark, and QPLIB's copies of camshape.** These contain floating-point "solved globally" claims for **dtoc5, optcdeg2, camshape100, camshape200 and camshape800**. Some of these claims are provably false.
- **Waki, Kim, Kojima and Muramatsu (2006).** They solved the DTOC5 source model to floating-point global optimality with a sparse SDP relaxation.

Because of these, the bottom line "16 of 19 instances: no prior global result found" is wrong. The "new as far as found" label for dtoc5, optcdeg2, camshape200 and camshape800 must be revised.

## 1. Major issues

### M1. Missed: Mittelmann's Continuous Non-Convex QPLIB Benchmark and the QPLIB camshape copies

**The QPLIB camshape copies.**
- QPLIB contains camshape100/200/400/800 as QPLIB_2738, QPLIB_2480, QPLIB_2703 and QPLIB_3177 (type LCQ, donor Ruth Misener). Sizes: 199/200, 399/400, 799/800 and 1599/1600 variables/constraints.
- I compared QPLIB_2738.gms with the MINLPLib OSIL. It is the MINLPLib model with constants rounded to 8–10 digits. For example, 2cos θ is written 1.9998452 instead of 1.99984519984971, the bound on r1 is 1.000154824, and the objective coefficient is 0.03141592654.
- QPLIB's solu values (all marked `=best=`) are -4.28414627, -4.27849041, -4.27565887 and -4.27421987.
- My exact rational cross-evaluation (`camshape_qplib_vs_minlplib.py`):
  - MINLPLib point p1 (-4.284147121747) satisfies the MINLPLib model to 2e-14 but violates the QPLIB model by 3.0e-10.
  - QPLIB's point (-4.284146267805) satisfies both models to 2e-14.
  - So the 8-digit rounding probably moves the optimum by about 8.5e-7. This is consistent with the ill-conditioning the project documented, and is floating-point evidence only.

**The benchmark.** Source: https://plato.asu.edu/ftp/cnconv.html, version of 17 May 2026, fetched 2026-10-02. Its header says "All problems were solved GLOBALLY", with a 3 h limit and 8 threads; it lists only instances that at least one solver solved. I also checked Wayback snapshots: 3 Dec 2021, 7 Jan 2023, 9 Mar 2024, 21 Aug 2024, 4 Apr 2025, 11 Jul 2025 and 28 Sep 2025.

| QPLIB (MINLPLib) | listed as solved by | what the logs show |
|---|---|---|
| 2738 (camshape100) | ANTIGONE 1857 s (2021–Mar 2024), 744 s (2024–25), 852 s (2026); OCTERACT 3.6.0 37 s (2021), 4.5.1 8 s (2023), 4.7.1 17 s (2024) | 2026 ANTIGONE log: "Termination Status: Global minimum", best feasible = best possible = **-4.284302**. That is **1.55e-4 below** the exact MINLPLib optimum -4.28414712174675, so the incumbent is feasible only within tolerance. Octeract logs are no longer online and the values are unknown. |
| 2480 (camshape200) | OCTERACT 4.5.1, **6853 s** (7 Jan 2023 table) | Log not archived; the value is unknown. |
| 3177 (camshape800) | MINOTAUR 0.2.1 19 s (2021), 0.3.0 5 s, 0.4.0 16 s / 6 s, 0.4.1 3 s (2025–26) | 2026 log: "Optimal solution found", best value **-4.2774**, root LB = inf. This is **3.13e-3 below** our certified optimum -4.27427414195420, so the claim is **false**. |
| 8585 (dtoc5) | MINOTAUR 0.4.1, **1005 s** (2026) | "Optimal solution found", value 5.3897, LB = inf after the root. The log warns "Default lower bound was assumed for 99983 variables" and "Default upper bound ... for 99997 variables". So the claim holds only for an artificially bounded box; the value agrees with the certified optimum 5.38967211918114. |
| 8803 (optcdeg2) | MINOTAUR 0.2.1, **1641 s** (3 Dec 2021 table) | The 2021 log is not archived and the value is unknown. In 2026, MINOTAUR 0.4.1 reports "Detected infeasibility" in presolve. That is false: the instance has rigorously feasible points. |

Consequences for the report:
- The "16 of 19 instances: no prior global result found" bullet is false.
- Suggested labels:
  - **dtoc5:** partly known. MINOTAUR claimed optimality in floating point under assumed default bounds; ours is the first rigorous certificate.
  - **optcdeg2:** partly known. MINOTAUR 0.2.1 claimed it in 2021 (value unknown); Gurobi's 292.417 claim is a tolerance artifact; MINOTAUR 0.4.1 wrongly reports infeasibility.
  - **camshape200:** already solved in floating point, by Octeract on the QPLIB copy (value unpublished).
  - **camshape800:** a published false global claim exists (MINOTAUR), and our certificate refutes it.
  - **camshape100:** add the ANTIGONE and Octeract benchmark results. ANTIGONE's "global minimum" value is a tolerance artifact.
- The summary table's "strongest prior result" column must be corrected for these rows.
- QPLIB_2703 (camshape400) was never listed as solved.

My comparisons use our MINLPLib certificates. The QPLIB camshape copies differ by 8–10 digit rounding. A 1.5e-4 or 3e-3 shift from rounding at the 1e-10 level is implausible (the observed shift is about 8.5e-7), but for the QPLIB copies this is evidence, not proof. QPLIB 8585 and 8803 are the very sources of MINLPLib dtoc5 and optcdeg2; their coefficients match the OSIL.

### M2. Missed: Waki, Kim, Kojima and Muramatsu (2006) on the DTOC5 source model

- Reference: H. Waki, S. Kim, M. Kojima, M. Muramatsu, "Sums of squares and semidefinite program relaxations for polynomial optimization problems with structured sparsity", SIAM J. Optim. 17(1) (2006) 218–242, doi:10.1137/050623802. Preprint: Research Report B-411, Tokyo Tech, Oct 2004, rev. Feb 2005, https://optimization-online.org/wp-content/uploads/2004/10/988.pdf.
- What it shows:
  - Problem (39) on p. 30 is Coleman–Liao problem 5, with y_{i+1} = y_i + (1/M)(y_i² − x_i), y_1 = 1, objective (1/M)Σ(y_i² + x_i²). This is the h variant, i.e. the DTOC5 source model.
  - Table 12 (p. 31): the sparse SDP relaxation of order 1 (Shor) gives approximate global solutions for M = 600, 700, 800, 900 and 1000 (n up to 1998), with ε_obj from 2.5e-8 to 1.4e-7 and ε_feas around -1e-10.
  - These results are floating point (SeDuMi), and the objective carries a random perturbation |p_j| < 1e-5.
- Consequences:
  - The report's dtoc5 statement "none; local values only for the h·y² variant" is false.
  - The MINLPLib instance differs (coefficient 4h, N = 50000), so its own label can remain "new as far as found" for the instance.
  - The paper should still cite this work as prior global, relaxation-exact evidence on the source model. It is directly relevant to our "Lagrangian convex at the costate" certificate.

## 2. Minor issues

1. **QPLIB filter misdescribed.** Furini et al. (§3.2, preprint pp. 18–19) first discard instances solved by at least 30% of the complete solvers within 30 s. They then run **one** complete solver for 120 s and discard what it solves. The report says "no complete solver solved within 120 s".
2. **optcdeg2 bottom line.** It says the coefficient is 4 times that "in the original source", but Murtagh–Saunders 1982 was not read; the comparison is with OPTCNTRL.SIF (Δt = 0.2, damping 0.01, spring 0.004, which I confirmed). The bottom line should say so, as section 3 already does.
3. **"Identical to COPS 3.0".** Cross-cutting point 1 says this for camshape, chain and lnts. COPS 3.0 chain uses auxiliary states x2, x3, integrated by the trapezoidal rule, so "equivalent" is the right word. The report's own chain section says this.
4. **Mattick–Mutschler gaps.** The SCIP baseline column ("Gap Base") gives 0.074–0.226. The report's 0.076–0.226 mixes the two columns.
5. **GloMIQO not mentioned.** Misener and Floudas, JOGO 57 (2013) 3–50, doi:10.1007/s10898-012-9874-7. Its 399-instance suite includes GLOBALLib QCQPs (likely camshape and catmix), and Misener later donated the QPLIB camshape copies. My fetch was blocked (Springer returned a 3 KB bot page), so I could not check it. List it with "ANTIGONE 2014 per-instance results" as an unchecked likely source.
6. **More tolerance artifacts are available for cross-cutting point 3.** All are from 2026 Mittelmann logs and are compared with our certified optima:

   | solver | instance | value | below the certified optimum by |
   |---|---|---|---|
   | BARON | dtoc5 | 5.38966688 | 5.2e-6 |
   | BARON | optcdeg2 | 293.876075074557 | 2.1e-8 |
   | SCIP 10.0.1 | camshape400 | primal -4.33024 | 0.055 |
   | BARON | camshape800 | -4.51546 | 0.24 |
   | COPT | camshape100 / 200 / 400 / 800 | — | 4.3e-5 / 1.8e-4 / 7.4e-4 / 3.1e-3 |

   The logs also hold valid dual bounds stronger than MINLPLib's listing, for example COPT dtoc5 0.7619 (MINLPLib best 0.00243) and COPT optcdeg2 283.41.
7. **DTOC5.SIF SOLUTION lines.** The report calls them "inexact". More precisely, each lies below the converged local value: N=10 gives 1.4518939 vs 1.4519006, N=100 gives 1.5325526 vs 1.5325863, and N=1000 gives 1.527434 vs 1.534946. Waki et al. indicate the local value is global for N up to 1000. These lines are therefore not valid optimal values (a tolerance artifact or a different model version).
8. **Out-of-date open issue.** The "Open issues" section still says "report.md was NOT written".
9. **Optional citation.** Müller et al. 2019, arXiv:1912.00356 (surrogate duality), reports weak dual bounds for camshape, chain and lnts (Tables on pp. ~55 and 65 of the arXiv text). It is not a global result and is not listed among the searched sources.

## 3. Claims I verified (at the stated location, with my own code where numerical)

**Sources and bibliography**
- **Manifest:** all 65 rows have matching sha256; no unlisted files.
- **DOIs (Crossref):** all match the cited metadata: s10898-023-01345-1, s10898-026-01591-z, BF01299158, s11081-005-2068-0, s10107-005-0585-4, s12532-018-0147-4, 10.22215/etd/2011-09468.

**Papers**
- **JOGO 2026 (Göß–Burlacu–Martín)**
  - Table 17, p. 992: lnts50 Gurobi orig 5811.5 s, primal and dual both 0.6.
  - Table 11, p. 972: SCIP gaps 0.0251, 0.0334, 0.0821, 0.1033.
  - 4 h limit (14400 s); "default settings are used".
- **Göß arXiv:2603.16505v1**
  - Table 4, p. 32: PARA ε = 1e-4 (1e-3 for lnts400); dual 5.5e-1; gaps 0.00/0.00/0.00/0.01%; times 39/161/505/576 s; the "nearly zero" quote.
  - SCIP 10.0 is used (pp. 17–18).
- **Bestuzheva et al. arXiv:2301.00587v1**
  - App. B.1, pp. 36–37: Octeract 19.40, 110.89, 97.31, 111.83, 113.55 s; BARON 9.2–11.1%, Lindo 9.2–9.6%, SCIP 5.2–5.6%.
  - App. B.2, p. 49: 19.40 / 19.42 s.
  - Settings §3.2.2 (p. 22): 1e-6 absolute feasibility tolerance; Octeract 1e-6 relative and absolute gap.
  - §3.3 (p. 23): correctness checks and the test-set acceptance rule.
- **SCIP 8.0 suite report, App. A:** camshape gaps 7.3/6.1, 14.8/13.3, 18.6/18.4, 21.4/21.6% (p. 94); catmix and chain ∞ (p. 95); lukvle10 ∞ (p. 101); optcdeg2 76.3% / ∞ (p. 103).
- **COPS 2.0 Tables 3.2, 4.2, 9.2 and 14.2:** all values, violations and quotes as stated. LANCELOT's values lie below our optima for lnts100/400 and chain400 (by 7.4e-4); its camshape values exceed the optima by 0.018–0.58.
- **COPS 3.0:** Table 3.2 p. 8, Table 4.2 p. 10, Table 9.2 p. 22, Table 14.2 p. 34 (-4.80556e-02); catmix uses k = 3 collocation.
- **Coleman–Liao 1993 report:** problem 5 formula and Table 3.
- **Lukšan–Vlček V-767:** problem 5.10 on p. 25.
- **Griva–Vanderbei:** the quote is in §2.3.
- **Smith 2011 Table A.1:** none of its values for these models lies below our optima; its negative lnts values are impossible for the MINLPLib model (the objective is 50·x257 with x257 ≥ 0).

**Library data and models**
- **CUTEst SIF files**
  - DTOC5.SIF: y_{t+1} = y_t − h x_t + h y_t², objective scaled by 1/N.
  - OPTCDEG2.SIF: C2 = 0.05·DT.
- **Factor 4 in the MINLPLib models (my own OSIL reader)**
  - dtoc5: constraint coefficient 8e-5 = 4h, with h = 2e-5.
  - optcdeg2: 8e-5 = 0.2·Δt, 8e-6 = 0.02·Δt, objective 2e-4 = Δt/2.
  - QPLIB constraint Hessians: 0.00016.
- **MINLPLib**
  - Live pages (2026-10-02) for all 19 instances: every listed bound and point matches the report.
  - bounddates history: optcdeg2 GUROBI 292.417135 and p2 were both added 2023-04-11.
- **camshape model structure (OSIL):** x101 = d₁ is free, so the curvature row on (r1, r2) is omitted. At the optimum it is slack: |r2 − r1| = 3.1e-4, 7.8e-5, 2.0e-5 and 4.9e-6 against αθ, a factor of 60 to 478, both at MINLPLib p1 and at the certificate envelope arrays. This is a floating-point check.

**Numerical reproductions (my own GAMS models in `gms/`; floating-point evidence, IPOPT, one thread)**
- **dtoc5 with coefficient c = 1**
  - N = 10, 100, 500, 1000: 1.4519005669, 1.5325863389, 1.5347290450, 1.5349459875. These match Coleman–Liao Table 3.
  - N = 5000: 1.5351115283 (Smith: 1.535111532).
  - N = 50000: 1.5351477966.
- **dtoc5 with c = 4, N = 50000:** 5.389672020 (the MINLPLib value is 5.38967212).
- **optcdeg2 with damping 0.05**
  - T = 10, 40, 100, 400: 340.6053016, 253.2756336, 237.2764059, 229.5734174. These match the SIF SOLTN values.
  - T = 50000: 227.0439182.
- **optcdeg2 with damping 0.2, T = 50000:** 293.8762282.
- **lukvle10** (from MINLPLib p5, |c_j| ≤ tol): tol = 0 gives 352.2380254, 1e-6 gives 352.2376190, 1e-5 gives 352.2339619. These match the report's table.

**Derived numbers**
- ANTIGONE camshape100 gap: 1.22e-6 relative.
- lnts50 GUROBI gap: 3.8e-5 relative.
- LUKVLE10 SOLTN: 1.03e-3 below our bound.
- optcdeg2 Gurobi claim: 1.459 below the optimum (0.50%).

## 4. Overall assessment of the report

- The report says plainly what is floating point and what is rigorous.
- It records what was searched and what failed.
- It keeps copies of its sources with hashes.
- Its provenance findings are correct and valuable: the factor-4 variants of dtoc5 and optcdeg2, camshape omitting a curvature row that is slack at the optimum, and COPS 3.0 catmix being a different model.

The two missed sources are the problem. Mittelmann's QPLIB benchmark is the natural place to look for dtoc5 and optcdeg2, since both entered MINLPLib from QPLIB. Its omission changes the novelty labels of five instances. Before the paper relies on the report, it must be revised: add M1 and M2, correct the bottom line and summary table, and add the citations. The paper should then present dtoc5, optcdeg2, camshape200 and camshape800 as "first rigorous certificate; earlier floating-point claims exist (some false)", not as "new".

## 5. Commands I ran (targeted; all outcomes recorded)

- Parsed both predecessor transcripts (python, JSONL) into `pred_transcripts.txt` and read them.
- `curl` (sequential, at least 1 s apart):
  - plato.asu.edu/ftp/cnconv.html; 30 logs `cnconv_logs/{ant,bar,mnt,sci,cop}_results/QPLIB_{2738,2480,2703,3177,8585,8803}.*`; plato.asu.edu/sub/global.html.
  - Wayback CDX and 7 snapshots of cnconv.html; CDX for cnconv_logs (only 4 entries, no old logs).
  - qplib.zib.de pages, .qplib, .gms and .sol files for 2738 and 3177; pages for 2480, 2703, 8585 and 8803; qplib.solu.
  - optimization-online 5846.pdf (QPLIB paper) and 988.pdf (Waki et al.).
  - 19 live MINLPLib pages; arXiv 2508.07018; GitHub API tree of GAMS-dev/gamsworld and globalref.inc.
  - Spiral record 10044/1/15512 (it is the MISO paper, not GloMIQO); Springer GloMIQO PDF (blocked, 3 KB HTML).
  - Adjiman GOTI slides (no catalyst mixing).
  - All succeeded except the Springer fetch.
- Crossref API for 8 DOIs; OpenAlex for GloMIQO (closed access).
- WebSearch, 6 queries: QPLIB camshape IDs; camshape and global solvers; GloMIQO with camshape/catmix (twice); QPLIB 8585/8803 per-instance tables; catalyst mixing in global dynamic optimization (twice).
- `pdftotext -layout` and page-located greps on the stored sources: JOGO 2026, Göß arXiv, Bestuzheva arXiv, SCIP 8 suite, Mattick, COPS 3.0, Coleman–Liao, Lukšan–Vlček, Griva–Vanderbei, Gabrys–Sremac, Waki, QPLIB paper; also read the stored COPS 2.0 HTML text, SIF files, the Smith excerpt and COCONUT pages.
- `python3` checks:
  - manifest sha256 check;
  - `osil_lq.py` coefficient classes for dtoc5, optcdeg2, camshape100 and lnts50;
  - `camshape_qplib_vs_minlplib.py camshape100 2738` and `camshape800 3177` (exact rationals);
  - camshape slack check;
  - bounddates history parse;
  - differences between logged values and the certified optima.
- `gms/run_all.sh`: background PID 825749, log `gms/run_all.log`, finished with "ALLDONE". It ran GAMS 54.3 with IPOPT, `threads=1`: dtoc5.gms (c = 1, N = 10/100/500/1000/50000; c = 4, N = 50000), optc.gms (T = 10/40/100/400 at D = 0.05; T = 50000 at D = 0.2 and 0.05) and lv.gms (tol = 0, 1e-6, 1e-5). I also ran dtoc5.gms with N = 5000, c = 1 in the foreground. All runs ended with model status 2 (locally optimal).
- No project-wide checks, no CI inspection, no git operations. None of my processes are still running. The running dtoc5 GAMS processes (PIDs 819822/819825/819828) belong to the solver-campaign track and were not touched.
